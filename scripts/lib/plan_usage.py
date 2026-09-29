#!/usr/bin/env python3
"""Offline, opt-in accounting for one explicitly bound Codex rollout.

The ledger is private local state. Reports never include source paths, prompts,
responses, tool arguments, or credentials. Lifecycle and pricing are explicit:
missing evidence remains unknown and pricing snapshots must be synthetic.
"""
from __future__ import annotations

import argparse
import datetime as dt
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN
import fcntl
import hashlib
import http.client
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tempfile
from typing import Any
from urllib.parse import urlsplit
try:
    from work_activity import (ActivityError, DISPLAY_KINDS, classify as classify_activity,
                               normalize_receipt)
except ModuleNotFoundError:  # Loaded by tests through importlib, outside script directory.
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from work_activity import (ActivityError, DISPLAY_KINDS, classify as classify_activity,
                               normalize_receipt)


LEDGER_VERSION = 1
REPORT_VERSION = 2
HISTORY_VERSION = 1
ACTIVITY_HISTORY_VERSION = 2
SUPPORTED_SOURCE_VERSION = "0.156.1"
MAX_SOURCE_BYTES = 64 * 1024 * 1024
MAX_RECORDS = 100_000
COUNTERS = (
    "input_tokens",
    "cached_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "cache_write_input_tokens",
    "total_tokens",
)
IDENTIFIERS = ("response_id", "thread_id", "turn_id", "session_id", "root_turn_id")
IDENTITY_FIELDS = ("effective_model", "service_tier", "payment_mode")
WORK_KINDS = ("feature", "bug", "test", "explanation", "documentation")
OPAQUE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
SHA256_HEX = re.compile(r"[a-f0-9]{64}\Z")
LIFECYCLE_KINDS = {
    "started", "paused", "resumed", "technical_closed", "accepted",
    "failed", "retry", "cancelled",
}
TOKEN_TYPE = re.compile(br'^\s*\{.{0,384}?"type"\s*:\s*"token_usage_record"', re.DOTALL)
SESSION_TYPE = re.compile(br'^\s*\{.{0,384}?"type"\s*:\s*"session_meta"', re.DOTALL)


class UsageError(RuntimeError):
    """Expected, user-actionable observer failure."""


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _timestamp(value: str, label: str = "timestamp") -> tuple[str, dt.datetime]:
    if not isinstance(value, str) or not value:
        raise UsageError(f"{label} ausente")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise UsageError(f"{label} inválido") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise UsageError(f"{label} requiere zona horaria")
    normalized = parsed.astimezone(dt.timezone.utc)
    return normalized.isoformat().replace("+00:00", "Z"), normalized


def _decimal(value: Any, label: str) -> Decimal:
    if not isinstance(value, str):
        raise UsageError(f"{label} debe ser decimal textual")
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise UsageError(f"{label} inválido") from exc
    if not parsed.is_finite() or parsed < 0:
        raise UsageError(f"{label} inválido")
    return parsed


def _json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def _digest(value: Any) -> str:
    return hashlib.sha256(_json_bytes(value)).hexdigest()


def _path_digest(path: Path) -> str:
    return hashlib.sha256(os.fsencode(str(path))).hexdigest()


def _safe_regular(path: Path, label: str) -> os.stat_result:
    try:
        info = path.lstat()
    except OSError as exc:
        raise UsageError(f"{label} inexistente o ilegible") from exc
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise UsageError(f"{label} debe ser un archivo regular sin enlaces")
    return info


def _reject_symlink_ancestors(path: Path, label: str) -> None:
    for candidate in (path.parent, *path.parents):
        if candidate.exists() and candidate.is_symlink():
            raise UsageError(f"{label} no puede atravesar symlinks")


def _safe_parent(path: Path) -> Path:
    parent = path.parent
    current = parent
    while not current.exists() and current != current.parent:
        current = current.parent
    if not current.is_dir() or current.is_symlink():
        raise UsageError("el almacén privado requiere un directorio real")
    _reject_symlink_ancestors(path, "el almacén privado")
    if not parent.is_dir():
        raise UsageError("el directorio privado del ledger debe existir")
    return parent


def _private_ledger(path: Path | str, project_root: Path | str) -> Path:
    ledger = Path(path).expanduser()
    if not ledger.is_absolute() or ledger.suffix != ".json":
        raise UsageError("el ledger debe ser una ruta JSON absoluta")
    requested_root = Path(project_root).expanduser()
    if not requested_root.is_dir() or requested_root.is_symlink():
        raise UsageError("raíz de proyecto inválida")
    _reject_symlink_ancestors(requested_root, "la raíz de proyecto")
    root = requested_root.resolve()
    resolved = ledger.resolve(strict=False)
    if resolved == root or resolved.is_relative_to(root):
        raise UsageError("el ledger privado debe quedar fuera del worktree")
    _safe_parent(ledger)
    if ledger.exists() and ledger.is_symlink():
        raise UsageError("ledger symlink no permitido")
    return ledger


def _source(path: Path | str) -> tuple[Path, os.stat_result]:
    source = Path(path).expanduser()
    if not source.is_absolute() or source.suffix != ".jsonl":
        raise UsageError("la fuente debe ser un JSONL absoluto")
    _reject_symlink_ancestors(source, "la fuente")
    return source, _safe_regular(source, "fuente")


def _unique_json(raw: bytes | str, label: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in items:
            if key in value:
                raise UsageError(f"{label} contiene claves duplicadas")
            value[key] = item
        return value
    try:
        return json.loads(raw, object_pairs_hook=pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except UsageError:
        raise
    except (UnicodeError, ValueError) as exc:
        raise UsageError(f"{label} malformado") from exc


def _relative_ref(value: str, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise UsageError(f"{label} inválida")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != value or "//" in value:
        raise UsageError(f"{label} debe ser relativa y canónica")
    return value


def _prefix(path: Path, limit: int) -> tuple[bytes, str]:
    if type(limit) is not int or limit < 0 or limit > MAX_SOURCE_BYTES:
        raise UsageError("fuente excede el límite soportado de S01")
    digest = hashlib.sha256()
    chunks: list[bytes] = []
    remaining = limit
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
        try:
            while remaining:
                chunk = os.read(descriptor, min(1024 * 1024, remaining))
                if not chunk:
                    raise UsageError("fuente truncada durante la lectura")
                remaining -= len(chunk)
                chunks.append(chunk)
                digest.update(chunk)
        finally:
            os.close(descriptor)
    except OSError as exc:
        raise UsageError("lectura de fuente fallida") from exc
    return b"".join(chunks), digest.hexdigest()


def _captured_prefix(path: Path) -> tuple[os.stat_result, bytes, str]:
    before = _safe_regular(path, "fuente")
    first, first_digest = _prefix(path, before.st_size)
    second, second_digest = _prefix(path, before.st_size)
    after = path.stat()
    if ((before.st_dev, before.st_ino) != (after.st_dev, after.st_ino)
            or after.st_size < before.st_size or first_digest != second_digest or first != second):
        raise UsageError("prefijo capturado cambió durante la lectura")
    return before, first, first_digest


def _session_contract(prefix: bytes) -> tuple[str, str]:
    for raw in prefix.splitlines():
        if not SESSION_TYPE.match(raw[:448]):
            continue
        try:
            value = _unique_json(raw, "session_meta")
        except UsageError:
            raise
        payload = value.get("payload") if isinstance(value, dict) else None
        if value.get("type") != "session_meta" or not isinstance(payload, dict):
            raise UsageError("session_meta fuera de contrato")
        session_id = payload.get("id")
        version = payload.get("cli_version")
        if not isinstance(session_id, str) or not session_id or not isinstance(version, str):
            raise UsageError("session_meta incompleto")
        return session_id, version
    raise UsageError("session_meta ausente")


def _read_json(path: Path) -> dict[str, Any]:
    _safe_regular(path, "ledger")
    try:
        value = _unique_json(path.read_text(encoding="utf-8"), "ledger")
    except (OSError, UnicodeError, UsageError) as exc:
        raise UsageError("ledger ilegible; no se reinicia automáticamente") from exc
    if (not isinstance(value, dict) or value.get("ledger_version") != LEDGER_VERSION
            or not isinstance(value.get("bindings"), dict)
            or not isinstance(value.get("records"), dict)):
        raise UsageError("versión de ledger no soportada")
    if "rate_snapshots" not in value:
        value["rate_snapshots"] = {}
    if "activity_events" not in value:
        value["activity_events"] = {}
    if not isinstance(value["rate_snapshots"], dict) or not isinstance(value["activity_events"], dict):
        raise UsageError("snapshots tarifarios inválidos")
    for binding in value["bindings"].values():
        if not isinstance(binding, dict):
            raise UsageError("binding inválido")
        binding.setdefault("lifecycle_events", {})
        binding.setdefault("report_revisions", [])
        binding.setdefault("activity_report_revisions", [])
        if not isinstance(binding["lifecycle_events"], dict) or not isinstance(
                binding["report_revisions"], list) or not isinstance(
                binding["activity_report_revisions"], list):
            raise UsageError("estado S02 inválido")
    return value


def _atomic_json(path: Path, value: dict[str, Any], fault: str | None = None) -> None:
    data = _json_bytes(value) + b"\n"
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".plan-usage-", dir=path.parent)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if fault == "before_replace":
            raise OSError("injected failure before replace")
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
        if fault == "after_replace":
            raise OSError("injected failure after replace")
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


class _Lock:
    def __init__(self, ledger: Path):
        self.path = ledger.with_suffix(ledger.suffix + ".lock")
        self.descriptor: int | None = None

    def __enter__(self) -> "_Lock":
        if self.path.exists() and self.path.is_symlink():
            raise UsageError("lock symlink no permitido")
        flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
        try:
            self.descriptor = os.open(self.path, flags, 0o600)
            os.fchmod(self.descriptor, 0o600)
            fcntl.flock(self.descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (OSError, BlockingIOError) as exc:
            if self.descriptor is not None:
                os.close(self.descriptor)
                self.descriptor = None
            raise UsageError("otro importador mantiene el lock") from exc
        return self

    def __exit__(self, *_: Any) -> None:
        if self.descriptor is not None:
            fcntl.flock(self.descriptor, fcntl.LOCK_UN)
            os.close(self.descriptor)
            self.descriptor = None


def _initial_ledger() -> dict[str, Any]:
    return {"ledger_version": LEDGER_VERSION, "bindings": {}, "records": {},
            "rate_snapshots": {}, "activity_events": {}, "updated_at": _now()}


def _binding_id(project_id: str, requirement_ref: str, plan_digest: str,
                execution_id: str, attempt_id: str) -> str:
    fields = (project_id, requirement_ref, plan_digest, execution_id, attempt_id)
    if any(not isinstance(item, str) or not item.strip() for item in fields):
        raise UsageError("identidad de binding incompleta")
    if not re.fullmatch(r"[a-f0-9]{64}", plan_digest):
        raise UsageError("plan_digest debe ser SHA-256")
    return _digest(fields)


def bind(*, ledger_path: Path | str, project_root: Path | str, project_id: str,
         requirement_ref: str, plan_version: str, plan_digest: str, execution_id: str,
         attempt_id: str, slice_id: str | None, source_path: Path | str,
         source_version: str, session_id: str, thread_id: str, root_turn_id: str,
         allow_root_turn_change: bool = False, work_kind: str | None = None,
         work_id: str | None = None, activity_mode: bool = False) -> str:
    """Bind one dedicated root session before attributable usage begins."""
    ledger_path = _private_ledger(ledger_path, project_root)
    source_path, _ = _source(source_path)
    if source_version != SUPPORTED_SOURCE_VERSION:
        raise UsageError("versión de fuente no soportada")
    requirement_ref = _relative_ref(requirement_ref, "requirement_ref")
    if not isinstance(plan_version, str) or not plan_version.strip():
        raise UsageError("plan_version inválida")
    if slice_id is not None and (not isinstance(slice_id, str) or not slice_id.strip()):
        raise UsageError("slice_id inválida")
    identities = (session_id, thread_id, root_turn_id)
    if any(not isinstance(item, str) or not item for item in identities):
        raise UsageError("identidad runtime incompleta")
    if type(allow_root_turn_change) is not bool:
        raise UsageError("allow_root_turn_change inválido")
    if type(activity_mode) is not bool:
        raise UsageError("activity_mode inválido")
    if activity_mode:
        if work_kind is not None or not isinstance(work_id, str) or not OPAQUE_ID.fullmatch(work_id):
            raise UsageError("modo actividad requiere work_id opaco y ninguna categoría global")
    elif (work_kind is None) != (work_id is None):
        raise UsageError("work_kind y work_id deben indicarse juntos")
    if not activity_mode and work_kind is not None and (work_kind not in WORK_KINDS
                                   or not isinstance(work_id, str)
                                   or not OPAQUE_ID.fullmatch(work_id)):
        raise UsageError("categoría o identificador de trabajo inválido")
    binding_id = _binding_id(project_id, requirement_ref, plan_digest, execution_id, attempt_id)
    with _Lock(ledger_path):
        ledger = _read_json(ledger_path) if ledger_path.exists() else _initial_ledger()
        if binding_id in ledger["bindings"]:
            raise UsageError("binding ya existe")
        if any(item.get("session_id") == session_id for item in ledger["bindings"].values()):
            raise UsageError("sesión ya vinculada; no se comparte entre planes")
        source_info, prefix, _ = _captured_prefix(source_path)
        observed_session, observed_version = _session_contract(prefix)
        if observed_session != session_id or observed_version != source_version:
            raise UsageError("session_meta no coincide con el binding")
        baseline = prefix.rfind(b"\n") + 1
        prefix_digest = hashlib.sha256(prefix[:baseline]).hexdigest()
        ledger["bindings"][binding_id] = {
            "binding_id": binding_id,
            "project_id": project_id,
            "requirement_ref": requirement_ref,
            "plan_version": plan_version,
            "plan_digest": plan_digest,
            "execution_id": execution_id,
            "attempt_id": attempt_id,
            "slice_id": slice_id,
            "source_path": str(source_path),
            "source_path_digest": _path_digest(source_path),
            "source_version": source_version,
            "source_identity": {"device": source_info.st_dev, "inode": source_info.st_ino},
            "session_id": session_id,
            "thread_id": thread_id,
            "root_turn_id": root_turn_id,
            "allow_root_turn_change": allow_root_turn_change,
            "work_kind": work_kind,
            "work_id": work_id,
            "activity_mode": activity_mode,
            "enabled": True,
            "bound_at": _now(),
            "checkpoint": {"byte_offset": baseline, "prefix_sha256": prefix_digest},
            "anomalies": [],
            "data_state": "provisional",
            "lifecycle_events": {},
            "report_revisions": [],
            "activity_report_revisions": [],
        }
        ledger["updated_at"] = _now()
        _atomic_json(ledger_path, ledger)
    return binding_id


def _usage(value: Any) -> dict[str, int]:
    if not isinstance(value, dict):
        raise UsageError("bloque de contadores ausente")
    result: dict[str, int] = {}
    for key in COUNTERS:
        item = value.get(key, 0 if key == "cache_write_input_tokens" else None)
        if type(item) is not int or item < 0:
            raise UsageError("contador inválido")
        result[key] = item
    if result["total_tokens"] != result["input_tokens"] + result["output_tokens"]:
        raise UsageError("total_tokens no coincide con input + output")
    if result["cached_input_tokens"] > result["input_tokens"]:
        raise UsageError("cached_input_tokens excede input_tokens")
    if result["reasoning_output_tokens"] > result["output_tokens"]:
        raise UsageError("reasoning_output_tokens excede output_tokens")
    return result


def _record(raw: bytes, binding: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    try:
        value = _unique_json(raw, "registro token_usage_record")
    except UsageError:
        raise
    payload = value.get("payload") if isinstance(value, dict) else None
    if value.get("type") != "token_usage_record" or not isinstance(payload, dict):
        raise UsageError("registro de uso fuera de contrato")
    ids = {key: payload.get(key) for key in IDENTIFIERS}
    if any(not isinstance(item, str) or not item for item in ids.values()):
        raise UsageError("identificadores de respuesta incompletos")
    if ids["session_id"] != binding["session_id"]:
        raise UsageError("sesión ajena al binding")
    if ids["thread_id"] != binding["thread_id"] or (
            not binding.get("allow_root_turn_change", False)
            and ids["root_turn_id"] != binding["root_turn_id"]):
        raise UsageError("fork, child o thread fuera del binding")
    usage = _usage(payload.get("usage"))
    _usage(payload.get("turn_token_usage"))
    _usage(payload.get("thread_token_usage"))
    key = ":".join((binding["source_version"], ids["session_id"], ids["thread_id"], ids["response_id"]))
    record = {
        "binding_id": binding["binding_id"],
        "source_version": binding["source_version"],
        **ids,
        "usage": usage,
    }
    identity: dict[str, str] = {}
    for field in IDENTITY_FIELDS:
        item = payload.get(field)
        if item is not None:
            if not isinstance(item, str) or not item.strip() or len(item) > 128:
                raise UsageError(f"{field} inválido")
            identity[field] = item
    record["cost_identity"] = identity
    record["record_digest"] = _digest(record)
    return key, record


def _commit(ledger_path: Path, ledger: dict[str, Any], fault: str | None) -> None:
    expected = _digest(ledger)
    try:
        _atomic_json(ledger_path, ledger, fault)
    except OSError as exc:
        if ledger_path.exists():
            try:
                if _digest(_read_json(ledger_path)) == expected:
                    return
            except UsageError:
                pass
        raise UsageError("commit del ledger falló; snapshot previo preservado") from exc


def refresh(*, ledger_path: Path | str, project_root: Path | str, binding_id: str,
            _fault: str | None = None) -> dict[str, int]:
    """Import complete allowed records from a stable captured prefix."""
    ledger_path = _private_ledger(ledger_path, project_root)
    with _Lock(ledger_path):
        ledger = _read_json(ledger_path)
        binding = ledger.get("bindings", {}).get(binding_id)
        if not isinstance(binding, dict):
            raise UsageError("binding inexistente")
        if binding.get("enabled") is not True:
            return {"imported": 0, "duplicates": 0, "excluded": 0}
        source_path, before = _source(binding["source_path"])
        identity = binding["source_identity"]
        if (before.st_dev, before.st_ino) != (identity["device"], identity["inode"]):
            raise UsageError("identidad de fuente cambió")
        offset = binding["checkpoint"]["byte_offset"]
        if before.st_size < offset:
            raise UsageError("fuente truncada desde el checkpoint")
        first, prefix_digest = _prefix(source_path, before.st_size)
        if hashlib.sha256(first[:offset]).hexdigest() != binding["checkpoint"]["prefix_sha256"]:
            raise UsageError("prefijo previo fue reescrito")
        second, second_digest = _prefix(source_path, before.st_size)
        after = source_path.stat()
        if ((after.st_dev, after.st_ino) != (before.st_dev, before.st_ino)
                or after.st_size < before.st_size or prefix_digest != second_digest or first != second):
            raise UsageError("prefijo capturado cambió durante la lectura")
        delta = first[offset:]
        boundary = delta.rfind(b"\n") + 1
        complete = delta[:boundary]
        imported = duplicates = excluded = 0
        anomalies = list(binding.get("anomalies", []))
        for raw in complete.splitlines():
            if not TOKEN_TYPE.match(raw[:448]):
                continue
            try:
                key, record = _record(raw, binding)
            except UsageError as exc:
                excluded += 1
                anomalies.append({"kind": "excluded_record", "reason": str(exc)})
                continue
            if (binding.get("allow_root_turn_change", False)
                    and record["root_turn_id"] == binding["root_turn_id"]):
                # The bind command runs in this root turn. Its later response is
                # outside the prospectively observed user task.
                continue
            existing = ledger["records"].get(key)
            if existing is not None:
                if existing.get("record_digest") == record["record_digest"]:
                    duplicates += 1
                else:
                    excluded += 1
                    anomalies.append({"kind": "conflicting_response_id"})
                continue
            if len(ledger["records"]) >= MAX_RECORDS:
                raise UsageError("ledger excede el límite de registros de S01")
            if record["usage"]["cache_write_input_tokens"]:
                anomalies.append({"kind": "cache_write_semantics_unqualified"})
            ledger["records"][key] = record
            imported += 1
        new_offset = offset + boundary
        binding["checkpoint"] = {
            "byte_offset": new_offset,
            "prefix_sha256": hashlib.sha256(first[:new_offset]).hexdigest(),
        }
        binding["anomalies"] = anomalies
        binding["data_state"] = "incomplete" if anomalies or boundary != len(delta) else "provisional"
        binding["last_refresh_at"] = _now()
        ledger["updated_at"] = _now()
        _commit(ledger_path, ledger, _fault)
        return {"imported": imported, "duplicates": duplicates, "excluded": excluded}


def disable(*, ledger_path: Path | str, project_root: Path | str, binding_id: str) -> None:
    ledger_path = _private_ledger(ledger_path, project_root)
    with _Lock(ledger_path):
        ledger = _read_json(ledger_path)
        binding = ledger.get("bindings", {}).get(binding_id)
        if not isinstance(binding, dict):
            raise UsageError("binding inexistente")
        binding["enabled"] = False
        binding["disabled_at"] = _now()
        ledger["updated_at"] = _now()
        _atomic_json(ledger_path, ledger)


def record_lifecycle_event(*, ledger_path: Path | str, project_root: Path | str,
                           binding_id: str, event_id: str, kind: str, at: str,
                           reference: str | None = None, response_id: str | None = None,
                           usage_observed: bool | None = None,
                           _fault: str | None = None) -> dict[str, Any]:
    """Persist one explicit lifecycle observation without inferring activity."""
    if not isinstance(event_id, str) or not re.fullmatch(r"[A-Za-z0-9._-]{1,128}", event_id):
        raise UsageError("event_id inválido")
    if kind not in LIFECYCLE_KINDS:
        raise UsageError("evento lifecycle no soportado")
    normalized_at, parsed_at = _timestamp(at)
    if kind == "accepted":
        if reference is None:
            raise UsageError("aceptación requiere referencia")
        reference = _relative_ref(reference, "referencia de aceptación")
    elif reference is not None:
        reference = _relative_ref(reference, "referencia")
    if kind in {"failed", "retry"} and (
            not isinstance(response_id, str) or not response_id):
        raise UsageError(f"{kind} requiere response_id")
    if usage_observed is not None and type(usage_observed) is not bool:
        raise UsageError("usage_observed debe ser booleano")
    event = {"event_id": event_id, "kind": kind, "at": normalized_at,
             "reference": reference, "response_id": response_id,
             "usage_observed": usage_observed}
    event["event_digest"] = _digest(event)
    ledger_path = _private_ledger(ledger_path, project_root)
    with _Lock(ledger_path):
        ledger = _read_json(ledger_path)
        binding = ledger.get("bindings", {}).get(binding_id)
        if not isinstance(binding, dict):
            raise UsageError("binding inexistente")
        existing = binding["lifecycle_events"].get(event_id)
        if existing is not None:
            if existing.get("event_digest") != event["event_digest"]:
                raise UsageError("event_id lifecycle conflictivo")
            return {"recorded": False, "late": bool(existing.get("late"))}
        previous_times = [_timestamp(item["at"])[1]
                          for item in binding["lifecycle_events"].values()]
        event["late"] = bool(previous_times and parsed_at < max(previous_times))
        event["sequence"] = len(binding["lifecycle_events"]) + 1
        event["recorded_at"] = _now()
        binding["lifecycle_events"][event_id] = event
        ledger["updated_at"] = _now()
        _commit(ledger_path, ledger, _fault)
        return {"recorded": True, "late": event["late"]}


def register_rate_snapshot(*, ledger_path: Path | str, project_root: Path | str,
                           snapshot: dict[str, Any],
                           _fault: str | None = None) -> str:
    """Register one immutable synthetic rate card; commercial cards are rejected."""
    if not isinstance(snapshot, dict) or snapshot.get("kind") != "synthetic":
        raise UsageError("solo se admiten tarifas sintéticas")
    snapshot_id = snapshot.get("snapshot_id")
    if not isinstance(snapshot_id, str) or not re.fullmatch(r"[A-Za-z0-9._-]{1,128}", snapshot_id):
        raise UsageError("snapshot_id tarifario inválido")
    if snapshot.get("currency") != "USD" or snapshot.get("unit") != "per_1m_tokens":
        raise UsageError("snapshot sintético requiere USD por millón de tokens")
    rates = snapshot.get("rates")
    if not isinstance(rates, list) or not rates:
        raise UsageError("snapshot sintético sin tarifas")
    normalized_rates: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for rate in rates:
        if not isinstance(rate, dict):
            raise UsageError("tarifa sintética inválida")
        model = rate.get("effective_model")
        tier = rate.get("service_tier")
        if not isinstance(model, str) or not model or not isinstance(tier, str) or not tier:
            raise UsageError("tarifa sintética requiere modelo y tier")
        key = (model, tier)
        if key in seen:
            raise UsageError("tarifa sintética duplicada")
        seen.add(key)
        item = {"effective_model": model, "service_tier": tier}
        for field in ("input_tokens", "cached_input_tokens", "output_tokens"):
            parsed = _decimal(rate.get(field), f"tarifa {field}")
            item[field] = format(parsed, "f")
        cache_write = rate.get("cache_write_input_tokens")
        if cache_write is not None:
            item["cache_write_input_tokens"] = format(
                _decimal(cache_write, "tarifa cache_write_input_tokens"), "f")
        normalized_rates.append(item)
    normalized = {"snapshot_id": snapshot_id, "kind": "synthetic", "currency": "USD",
                  "unit": "per_1m_tokens", "rates": normalized_rates}
    normalized["snapshot_digest"] = _digest(normalized)
    ledger_path = _private_ledger(ledger_path, project_root)
    with _Lock(ledger_path):
        ledger = _read_json(ledger_path)
        existing = ledger["rate_snapshots"].get(snapshot_id)
        if existing is not None:
            if existing.get("snapshot_digest") != normalized["snapshot_digest"]:
                raise UsageError("snapshot tarifario es inmutable")
            return snapshot_id
        ledger["rate_snapshots"][snapshot_id] = normalized
        ledger["updated_at"] = _now()
        _commit(ledger_path, ledger, _fault)
    return snapshot_id


def _lifecycle(binding: dict[str, Any], observed_response_ids: set[str]) -> tuple[
        dict[str, Any], dict[str, Any], dict[str, int], list[dict[str, Any]]]:
    events = list(binding.get("lifecycle_events", {}).values())
    events.sort(key=lambda item: (_timestamp(item["at"])[1], item.get("sequence", 0)))
    anomalies: list[dict[str, Any]] = []
    state = "not_started"
    start: dt.datetime | None = None
    end: dt.datetime | None = None
    paused_at: dt.datetime | None = None
    paused_seconds = Decimal(0)
    technical_status = "unobserved"
    acceptance_status = "pending"
    acceptance_reference: str | None = None
    outcomes = {"failures": 0, "retries": 0, "cancellations": 0,
                "missing_usage_events": 0}
    for event in events:
        _, moment = _timestamp(event["at"])
        kind = event["kind"]
        if event.get("late"):
            anomalies.append({"kind": "late_lifecycle_event", "event_id": event["event_id"]})
        if kind == "started":
            if state != "not_started":
                anomalies.append({"kind": "invalid_lifecycle_transition", "event_id": event["event_id"]})
            else:
                state, start, technical_status = "running", moment, "open"
        elif kind == "paused":
            if state != "running":
                anomalies.append({"kind": "invalid_lifecycle_transition", "event_id": event["event_id"]})
            else:
                state, paused_at = "paused", moment
        elif kind == "resumed":
            if state != "paused" or paused_at is None:
                anomalies.append({"kind": "invalid_lifecycle_transition", "event_id": event["event_id"]})
            else:
                paused_seconds += Decimal(str((moment - paused_at).total_seconds()))
                state, paused_at = "running", None
        elif kind in {"technical_closed", "cancelled"}:
            if state not in {"running", "paused"}:
                anomalies.append({"kind": "invalid_lifecycle_transition", "event_id": event["event_id"]})
            else:
                if state == "paused" and paused_at is not None:
                    paused_seconds += Decimal(str((moment - paused_at).total_seconds()))
                    paused_at = None
                state, end = "terminal", moment
                technical_status = "closed" if kind == "technical_closed" else "cancelled"
                if kind == "cancelled":
                    outcomes["cancellations"] += 1
                    if (event.get("usage_observed") is not True
                            or event.get("response_id") not in observed_response_ids):
                        outcomes["missing_usage_events"] += 1
                        anomalies.append({"kind": "cancelled_usage_unknown"})
        elif kind == "accepted":
            if technical_status != "closed":
                anomalies.append({"kind": "acceptance_without_technical_close",
                                  "event_id": event["event_id"]})
            else:
                acceptance_status = "accepted"
                acceptance_reference = event.get("reference")
        elif kind == "failed":
            outcomes["failures"] += 1
            if (event.get("usage_observed") is not True
                    or event.get("response_id") not in observed_response_ids):
                outcomes["missing_usage_events"] += 1
                anomalies.append({"kind": "failed_response_usage_unknown",
                                  "response_id": event.get("response_id")})
        elif kind == "retry":
            outcomes["retries"] += 1
            if (event.get("usage_observed") is not True
                    or event.get("response_id") not in observed_response_ids):
                outcomes["missing_usage_events"] += 1
                anomalies.append({"kind": "retry_response_usage_unknown",
                                  "response_id": event.get("response_id")})
    elapsed: Decimal | None = None
    unpaused: Decimal | None = None
    if start is not None and end is not None:
        candidate = Decimal(str((end - start).total_seconds()))
        if candidate < 0 or paused_seconds < 0 or paused_seconds > candidate:
            anomalies.append({"kind": "invalid_clock_boundaries"})
        else:
            elapsed = candidate
            unpaused = candidate - paused_seconds
    if technical_status in {"open", "unobserved"}:
        anomalies.append({"kind": "technical_end_unknown"})
    lifecycle = {"technical_status": technical_status,
                 "acceptance_status": acceptance_status,
                 "acceptance_reference": acceptance_reference,
                 "event_count": len(events)}
    times = {
        "started_at": start.isoformat().replace("+00:00", "Z") if start else None,
        "ended_at": end.isoformat().replace("+00:00", "Z") if end else None,
        "elapsed_seconds": format(elapsed, "f") if elapsed is not None else None,
        "paused_seconds": format(paused_seconds, "f") if start is not None else None,
        "unpaused_seconds": format(unpaused, "f") if unpaused is not None else None,
        "active_time_seconds": None,
        "wait_time_seconds": None,
        "agent_time_seconds": None,
    }
    return lifecycle, times, outcomes, anomalies


def _identity(records: list[dict[str, Any]]) -> tuple[dict[str, str | None], list[str]]:
    result: dict[str, str | None] = {}
    unknowns: list[str] = []
    for field in IDENTITY_FIELDS:
        values = {item.get("cost_identity", {}).get(field) for item in records}
        if records and None not in values and len(values) == 1:
            result[field] = next(iter(values))
        else:
            result[field] = None
            unknowns.append(field)
    return result, unknowns


def _cost(records: list[dict[str, Any]], snapshot: dict[str, Any] | None) -> dict[str, Any]:
    if snapshot is None:
        return {"currency": "USD", "nature": "unknown", "amount": None,
                "billed_amount": None, "rate_snapshot_id": None,
                "priced_responses": 0, "unpriced_responses": len(records)}
    rates = {(item["effective_model"], item["service_tier"]): item
             for item in snapshot["rates"]}
    amount = Decimal(0)
    priced = 0
    for record in records:
        identity = record.get("cost_identity", {})
        rate = rates.get((identity.get("effective_model"), identity.get("service_tier")))
        usage = record["usage"]
        if rate is None or (usage["cache_write_input_tokens"]
                            and "cache_write_input_tokens" not in rate):
            continue
        uncached = usage["input_tokens"] - usage["cached_input_tokens"]
        response_cost = Decimal(uncached) * _decimal(rate["input_tokens"], "tarifa input")
        response_cost += Decimal(usage["cached_input_tokens"]) * _decimal(
            rate["cached_input_tokens"], "tarifa cached input")
        response_cost += Decimal(usage["output_tokens"]) * _decimal(
            rate["output_tokens"], "tarifa output")
        if usage["cache_write_input_tokens"]:
            response_cost += Decimal(usage["cache_write_input_tokens"]) * _decimal(
                rate["cache_write_input_tokens"], "tarifa cache write")
        amount += response_cost / Decimal(1_000_000)
        priced += 1
    rendered = (format(amount.quantize(Decimal("0.000000001"), rounding=ROUND_HALF_EVEN), "f")
                if priced else None)
    return {"currency": "USD",
            "nature": "synthetic_api_equivalent_subtotal" if priced else "unknown",
            "amount": rendered, "billed_amount": None,
            "rate_snapshot_id": snapshot["snapshot_id"], "priced_responses": priced,
            "unpriced_responses": len(records) - priced}


def _report_v1(binding: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    totals = {key: sum(item["usage"][key] for item in records) for key in COUNTERS}
    anomalies = binding.get("anomalies", [])
    return {
        "report_version": 1,
        "binding": {key: binding.get(key) for key in (
            "binding_id", "project_id", "requirement_ref", "plan_version", "plan_digest",
            "execution_id", "attempt_id", "slice_id", "source_version", "enabled",
        )},
        "usage": {"responses": len(records), **totals},
        "data_state": "incomplete" if anomalies else binding.get("data_state", "provisional"),
        "unknowns": ["effective_model", "service_tier", "payment_mode", "usd",
                     "elapsed_time", "active_time"],
        "anomalies": anomalies,
        "source": {"kind": "codex_rollout_jsonl", "adapter_version": 1},
    }


def _build_report(ledger: dict[str, Any], binding: dict[str, Any], *,
                  rate_snapshot_id: str | None, revision_number: int,
                  persisted: bool) -> dict[str, Any]:
    records = [item for item in ledger["records"].values()
               if item["binding_id"] == binding["binding_id"]]
    totals = {key: sum(item["usage"][key] for item in records) for key in COUNTERS}
    identity, unknowns = _identity(records)
    snapshot = None
    if rate_snapshot_id is not None:
        snapshot = ledger["rate_snapshots"].get(rate_snapshot_id)
        if snapshot is None:
            raise UsageError("snapshot tarifario inexistente")
    cost = _cost(records, snapshot)
    if cost["unpriced_responses"] or cost["rate_snapshot_id"] is None:
        unknowns.append("usd")
    unknowns.extend(("billed_usd", "active_time", "wait_time", "agent_time"))
    lifecycle, times, outcomes, lifecycle_anomalies = _lifecycle(
        binding, {item["response_id"] for item in records})
    if times["elapsed_seconds"] is None:
        unknowns.append("elapsed_time")
    anomalies = list(binding.get("anomalies", [])) + lifecycle_anomalies
    if cost["unpriced_responses"]:
        anomalies.append({"kind": "unpriced_responses", "count": cost["unpriced_responses"]})
    prior = binding.get("report_revisions", [])
    reason = "late_event" if any(item.get("late") for item in
                                 binding.get("lifecycle_events", {}).values()) else (
        "initial" if not prior else "update")
    return {
        "report_version": REPORT_VERSION,
        "revision": {"number": revision_number, "persisted": persisted,
                     "supersedes": prior[-1]["revision"]["number"] if prior else None,
                     "reason": reason},
        "binding": {key: binding.get(key) for key in (
            "binding_id", "project_id", "requirement_ref", "plan_version", "plan_digest",
            "execution_id", "attempt_id", "slice_id", "source_version", "enabled",
        )},
        "identity": identity,
        "usage": {"responses": len(records), **totals},
        "lifecycle": lifecycle,
        "times": times,
        "outcomes": outcomes,
        "cost": cost,
        "data_state": "incomplete" if anomalies or binding.get("data_state") == "incomplete"
        else "provisional",
        "unknowns": sorted(set(unknowns)),
        "anomalies": anomalies,
        "source": {"kind": "codex_rollout_jsonl", "adapter_version": 1},
    }


def report(*, ledger_path: Path | str, project_root: Path | str,
           binding_id: str, report_version: int = 1,
           rate_snapshot_id: str | None = None,
           revision: int | None = None) -> dict[str, Any]:
    ledger_path = _private_ledger(ledger_path, project_root)
    with _Lock(ledger_path):
        ledger = _read_json(ledger_path)
        binding = ledger.get("bindings", {}).get(binding_id)
        if not isinstance(binding, dict):
            raise UsageError("binding inexistente")
        records = [item for item in ledger["records"].values() if item["binding_id"] == binding_id]
        if report_version == 1:
            if revision is not None or rate_snapshot_id is not None:
                raise UsageError("reporte v1 no admite revisión ni tarifa")
            return _report_v1(binding, records)
        if report_version != REPORT_VERSION:
            raise UsageError("versión de reporte no soportada")
        if revision is not None:
            for saved in binding["report_revisions"]:
                if saved["revision"]["number"] == revision:
                    return saved
            raise UsageError("revisión de reporte inexistente")
        if rate_snapshot_id is None and binding["report_revisions"]:
            rate_snapshot_id = binding["report_revisions"][-1]["cost"]["rate_snapshot_id"]
        return _build_report(ledger, binding, rate_snapshot_id=rate_snapshot_id,
                             revision_number=len(binding["report_revisions"]) + 1,
                             persisted=False)


def snapshot_report(*, ledger_path: Path | str, project_root: Path | str,
                    binding_id: str, rate_snapshot_id: str | None = None,
                    _fault: str | None = None) -> dict[str, Any]:
    ledger_path = _private_ledger(ledger_path, project_root)
    with _Lock(ledger_path):
        ledger = _read_json(ledger_path)
        binding = ledger.get("bindings", {}).get(binding_id)
        if not isinstance(binding, dict):
            raise UsageError("binding inexistente")
        prior = binding["report_revisions"]
        fixed_ids = {item["cost"]["rate_snapshot_id"] for item in prior
                     if item["cost"]["rate_snapshot_id"] is not None}
        if fixed_ids:
            fixed = next(iter(fixed_ids))
            if rate_snapshot_id is None:
                rate_snapshot_id = fixed
            elif rate_snapshot_id != fixed:
                raise UsageError("la tarifa de una serie de revisiones es inmutable")
        value = _build_report(ledger, binding, rate_snapshot_id=rate_snapshot_id,
                              revision_number=len(prior) + 1, persisted=True)
        prior.append(value)
        ledger["updated_at"] = _now()
        _commit(ledger_path, ledger, _fault)
        return value


def record_actual_usd(*, ledger_path: Path | str, project_root: Path | str,
                      binding_id: str, amount: str, evidence_id: str,
                      evidence_sha256: str, complete_for_binding: bool,
                      _fault: str | None = None) -> dict[str, bool]:
    """Attach one direct USD charge attested by the user; do not inspect invoices."""
    if not isinstance(amount, str) or not re.fullmatch(
            r"(?:0|[1-9][0-9]{0,11})(?:\.[0-9]{1,9})?", amount):
        raise UsageError("importe USD requiere decimal textual acotado")
    parsed = _decimal(amount, "importe USD")
    if parsed <= 0:
        raise UsageError("importe USD debe ser positivo")
    if not isinstance(evidence_id, str) or not OPAQUE_ID.fullmatch(evidence_id):
        raise UsageError("evidence_id opaco inválido")
    if not isinstance(evidence_sha256, str) or not SHA256_HEX.fullmatch(evidence_sha256):
        raise UsageError("evidence_sha256 inválido")
    if type(complete_for_binding) is not bool:
        raise UsageError("complete_for_binding debe ser booleano")
    evidence = {"amount": format(parsed, "f"), "evidence_id": evidence_id,
                "evidence_sha256": evidence_sha256,
                "complete_for_binding": complete_for_binding,
                "source_kind": "user_attested_direct_charge"}
    ledger_path = _private_ledger(ledger_path, project_root)
    with _Lock(ledger_path):
        ledger = _read_json(ledger_path)
        binding = ledger["bindings"].get(binding_id)
        if not isinstance(binding, dict) or binding.get("work_kind") not in WORK_KINDS:
            raise UsageError("binding histórico inexistente o sin categoría")
        previous = binding.get("actual_cost_evidence")
        if previous is not None:
            if not isinstance(previous, dict):
                raise UsageError("evidencia USD previa inválida")
            if {key: previous.get(key) for key in evidence} == evidence:
                return {"recorded": False}
            raise UsageError("evidencia USD del binding es inmutable")
        if any(isinstance(item.get("actual_cost_evidence"), dict)
               and item["actual_cost_evidence"].get("evidence_id") == evidence_id
               for item in ledger["bindings"].values() if isinstance(item, dict)):
            raise UsageError("evidence_id USD ya asignado")
        binding["actual_cost_evidence"] = {**evidence, "recorded_at": _now()}
        ledger["updated_at"] = _now()
        _commit(ledger_path, ledger, _fault)
        return {"recorded": True}


def suggest_work_kind(*, summary: str, endpoint: str,
                      _transport: Any = None) -> dict[str, Any]:
    """Ask an opted-in local Kev server for a suggestion; never persist the text."""
    if (not isinstance(summary, str) or not summary.strip() or len(summary) > 512
            or "\x00" in summary):
        raise UsageError("resumen breve requerido (máximo 512 caracteres)")
    if not isinstance(endpoint, str):
        raise UsageError("endpoint Kev inválido")
    try:
        url = urlsplit(endpoint)
        port = url.port
    except (TypeError, ValueError) as exc:
        raise UsageError("endpoint Kev inválido") from exc
    if (url.scheme != "http" or url.hostname not in {"127.0.0.1", "localhost"}
            or port is None or url.username is not None or url.password is not None
            or url.path not in {"", "/"} or url.query or url.fragment):
        raise UsageError("Kev requiere endpoint HTTP local con puerto explícito")
    request = {"state": summary, "model": "kev-latest", "questions": {
        "work_kind": {"type": "choice",
                      "instructions": "Choose the primary purpose of this work item.",
                      "criteria": {
                          "feature": "Implement a new feature",
                          "bug": "Diagnose or fix a bug",
                          "test": "Run or develop tests",
                          "explanation": "Explain or answer a question",
                          "documentation": "Write or update documentation",
                      }}}}
    body = _json_bytes(request)
    if _transport is None:
        connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
        try:
            connection.request("POST", "/v1/systemone", body,
                               {"Content-Type": "application/json"})
            response = connection.getresponse()
            raw = response.read(65537)
            if response.status != 200 or len(raw) > 65536:
                raise UsageError("respuesta Kev no soportada")
        except OSError as exc:
            raise UsageError("servidor Kev local no disponible") from exc
        finally:
            connection.close()
    else:
        raw = _transport(body, port)
    value = _unique_json(raw, "respuesta Kev")
    answers = value.get("answers") if isinstance(value, dict) else None
    answer = answers.get("work_kind") if isinstance(answers, dict) else None
    if not isinstance(answer, dict) or answer.get("type") != "choice":
        raise UsageError("respuesta Kev sin elección válida")
    choice, probabilities = answer.get("choice"), answer.get("probabilities")
    if (choice not in WORK_KINDS or not isinstance(probabilities, dict)
            or set(probabilities) != set(WORK_KINDS)
            or any(type(item) not in {int, float} or not 0 <= item <= 1
                   for item in probabilities.values())):
        raise UsageError("categoría o probabilidades Kev inválidas")
    confidence = answer.get("confidence")
    if confidence is not None and (type(confidence) not in {int, float}
                                   or not 0 <= confidence <= 1):
        raise UsageError("confianza Kev inválida")
    return {"suggested_kind": choice, "confidence": confidence,
            "probabilities": probabilities, "confirmed": False}


def record_activity(*, ledger_path: Path | str, project_root: Path | str,
                    binding_id: str, receipt: dict[str, Any],
                    classification: dict[str, Any] | None = None,
                    _fault: str | None = None) -> dict[str, bool]:
    """Store one minimized receipt linked to an imported native response.

    The caller may supply a Kev-derived classification, but no summary or raw
    Kev request is accepted or stored here.
    """
    try:
        clean = normalize_receipt(receipt)
        derived = classify_activity(clean, classification)
    except ActivityError as exc:
        raise UsageError(str(exc)) from exc
    ledger_path = _private_ledger(ledger_path, project_root)
    with _Lock(ledger_path):
        ledger = _read_json(ledger_path)
        binding = ledger["bindings"].get(binding_id)
        if not isinstance(binding, dict) or binding.get("activity_mode") is not True:
            raise UsageError("binding de actividad inexistente")
        records = [item for item in ledger["records"].values()
                   if isinstance(item, dict) and item.get("binding_id") == binding_id
                   and item.get("response_id") == clean["response_id"]]
        if len(records) != 1:
            raise UsageError("response_id de actividad no observado en este binding")
        event = {**clean, "binding_id": binding_id, "classification": derived,
                 "recorded_at": _now()}
        existing = ledger["activity_events"].get(clean["activity_id"])
        if existing is not None:
            fields = {key: value for key, value in event.items() if key != "recorded_at"}
            if {key: existing.get(key) for key in fields} == fields:
                return {"recorded": False}
            raise UsageError("activity_id conflictivo")
        ledger["activity_events"][clean["activity_id"]] = event
        ledger["updated_at"] = _now()
        _commit(ledger_path, ledger, _fault)
        return {"recorded": True}


def _activity_usage() -> dict[str, int]:
    return {"responses": 0, **{key: 0 for key in COUNTERS}}


def _add_usage(target: dict[str, int], usage: dict[str, int]) -> None:
    target["responses"] += 1
    for key in COUNTERS:
        target[key] += usage[key]


def _activity_summary(records: list[dict[str, Any]], events: list[dict[str, Any]]) -> dict[str, Any]:
    rows = {kind: {"kind": kind, "activities": 0, "usage": _activity_usage(),
                   "elapsed_seconds": None, "known_elapsed_seconds": "0", "unknown_elapsed_activities": 0,
                   "unvalidated_inferred_activities": 0}
            for kind in DISPLAY_KINDS}
    per_response: dict[str, list[dict[str, Any]]] = {}
    for event in events:
        if (not isinstance(event, dict) or event.get("classification", {}).get("kind") not in DISPLAY_KINDS
                or not isinstance(event.get("response_id"), str)):
            raise UsageError("evento de actividad inválido")
        kind = event["classification"]["kind"]
        row = rows[kind]
        row["activities"] += 1
        try:
            elapsed = _decimal(event.get("elapsed_seconds"), "elapsed_seconds")
        except UsageError:
            elapsed = None
        if elapsed is None:
            row["unknown_elapsed_activities"] += 1
        else:
            known = Decimal(row["known_elapsed_seconds"]) + elapsed
            row["known_elapsed_seconds"] = format(known, "f")
        if event["classification"].get("validation") == "unvalidated":
            row["unvalidated_inferred_activities"] += 1
        per_response.setdefault(event["response_id"], []).append(event)
    for row in rows.values():
        if row["activities"] and not row["unknown_elapsed_activities"]:
            row["elapsed_seconds"] = row["known_elapsed_seconds"]
        if not row["activities"]:
            row["known_elapsed_seconds"] = None
    for record in records:
        response_id, usage = record["response_id"], record["usage"]
        linked = per_response.get(response_id, [])
        if not linked or any(item.get("manifest_complete") is not True for item in linked):
            bucket = "unassigned"
        else:
            kinds = {item["classification"]["kind"] for item in linked}
            bucket = next(iter(kinds)) if len(kinds) == 1 else "mixed"
        _add_usage(rows[bucket]["usage"], usage)
    all_usage = _activity_usage()
    for row in rows.values():
        for key, value in row["usage"].items():
            all_usage[key] += value
    return {"categories": [rows[kind] for kind in DISPLAY_KINDS], "usage": all_usage,
            "active_time_seconds": None,
            "usd": {"amount": None, "known_subtotal": None, "provenance": "unknown"}}


def snapshot_activity_report(*, ledger_path: Path | str, project_root: Path | str,
                             binding_id: str, _fault: str | None = None) -> dict[str, Any]:
    """Persist a v2 activity report; it reads only private ledger data."""
    ledger_path = _private_ledger(ledger_path, project_root)
    with _Lock(ledger_path):
        ledger = _read_json(ledger_path)
        binding = ledger["bindings"].get(binding_id)
        if not isinstance(binding, dict) or binding.get("activity_mode") is not True:
            raise UsageError("binding de actividad inexistente")
        records = [item for item in ledger["records"].values()
                   if isinstance(item, dict) and item.get("binding_id") == binding_id]
        events = [item for item in ledger["activity_events"].values()
                  if isinstance(item, dict) and item.get("binding_id") == binding_id]
        prior = binding["activity_report_revisions"]
        value = {"activity_history_version": ACTIVITY_HISTORY_VERSION,
                 "binding_id": binding_id, "project_id": binding["project_id"],
                 "work_id": binding["work_id"], "revision": len(prior) + 1,
                 "persisted": True, "record_count": len(records), "event_count": len(events),
                 **_activity_summary(records, events)}
        prior.append(value)
        ledger["updated_at"] = _now()
        _commit(ledger_path, ledger, _fault)
        return value


def _saved_activity(binding: dict[str, Any], record_count: int, event_count: int) -> dict[str, Any] | None:
    revisions = binding.get("activity_report_revisions", [])
    if not revisions:
        return None
    saved = revisions[-1]
    if (not isinstance(saved, dict) or saved.get("activity_history_version") != ACTIVITY_HISTORY_VERSION
            or saved.get("binding_id") != binding.get("binding_id")
            or saved.get("project_id") != binding.get("project_id")
            or saved.get("record_count") != record_count or saved.get("event_count") != event_count):
        return {**saved, "_activity_stale": True}
    return {**saved, "_activity_stale": False}


def activity_history_report(*, ledger_path: Path | str, project_root: Path | str,
                            project_id: str) -> dict[str, Any]:
    """Aggregate the latest activity snapshots without opening their sources."""
    if not isinstance(project_id, str) or not project_id.strip():
        raise UsageError("project_id requerido")
    ledger_path = _private_ledger(ledger_path, project_root)
    with _Lock(ledger_path):
        ledger = _read_json(ledger_path)
        bindings = [item for item in ledger["bindings"].values()
                    if isinstance(item, dict) and item.get("project_id") == project_id
                    and item.get("activity_mode") is True]
        categories = {kind: {"kind": kind, "activities": 0, "usage": _activity_usage(),
                             "known_elapsed_seconds": Decimal(0), "unknown_elapsed_activities": 0,
                             "unvalidated_inferred_activities": 0}
                      for kind in DISPLAY_KINDS}
        missing = stale = 0
        for binding in bindings:
            records = [item for item in ledger["records"].values()
                       if isinstance(item, dict) and item.get("binding_id") == binding["binding_id"]]
            events = [item for item in ledger["activity_events"].values()
                      if isinstance(item, dict) and item.get("binding_id") == binding["binding_id"]]
            saved = _saved_activity(binding, len(records), len(events))
            if saved is None:
                missing += 1
                continue
            stale += saved["_activity_stale"]
            for row in saved.get("categories", []):
                if not isinstance(row, dict) or row.get("kind") not in categories:
                    raise UsageError("revisión de actividad inválida")
                target = categories[row["kind"]]
                target["activities"] += row["activities"]
                target["unknown_elapsed_activities"] += row["unknown_elapsed_activities"]
                target["unvalidated_inferred_activities"] += row["unvalidated_inferred_activities"]
                if row["known_elapsed_seconds"] is not None:
                    target["known_elapsed_seconds"] += _decimal(row["known_elapsed_seconds"], "elapsed_seconds")
                for key, value in row["usage"].items():
                    target["usage"][key] += value
        output = []
        total = _activity_usage()
        for kind in DISPLAY_KINDS:
            row = categories[kind]
            row["known_elapsed_seconds"] = (format(row["known_elapsed_seconds"], "f")
                                            if row["activities"] else None)
            row["elapsed_seconds"] = (row["known_elapsed_seconds"] if row["activities"]
                                       and not row["unknown_elapsed_activities"] else None)
            for key, value in row["usage"].items():
                total[key] += value
            output.append(row)
        return {"activity_history_version": ACTIVITY_HISTORY_VERSION, "project_id": project_id,
                "bindings": len(bindings), "missing_reports": missing, "stale_reports": stale,
                "data_state": "empty" if not bindings else ("incomplete" if missing or stale else "provisional"),
                "categories": output, "usage": total, "active_time_seconds": None,
                "usd": {"amount": None, "known_subtotal": None, "provenance": "unknown"},
                "source_access": "none"}


def render_activity_history_text(value: dict[str, Any]) -> str:
    lines = [f"Project activity history · {value['project_id']}",
             "Time: elapsed wall-clock only; active time=unknown",
             "USD: unknown without activity-scoped direct evidence"]
    for row in value["categories"]:
        lines.append(f"{row['kind']}: activities={row['activities']} responses={row['usage']['responses']} "
                     f"tokens={row['usage']['total_tokens']} elapsed={row['elapsed_seconds'] or 'unknown'} "
                     f"unvalidated={row['unvalidated_inferred_activities']}")
    return "\n".join(lines)


def _saved_measurement(binding: dict[str, Any], record_count: int) -> dict[str, Any] | None:
    revisions = binding["report_revisions"]
    if not revisions:
        return None
    for number, saved in enumerate(revisions, 1):
        if (not isinstance(saved, dict) or saved.get("report_version") != REPORT_VERSION
                or not isinstance(saved.get("revision"), dict)
                or saved["revision"].get("number") != number
                or saved["revision"].get("persisted") is not True
                or not isinstance(saved.get("binding"), dict)
                or saved["binding"].get("binding_id") != binding["binding_id"]
                or saved["binding"].get("project_id") != binding["project_id"]):
            raise UsageError("revisión histórica incompatible")
    saved = revisions[-1]
    usage = saved.get("usage")
    if (not isinstance(usage, dict) or type(usage.get("responses")) is not int
            or usage["responses"] < 0):
        raise UsageError("uso histórico inválido")
    _usage(usage)
    if saved.get("data_state") not in {"provisional", "incomplete"}:
        raise UsageError("estado histórico inválido")
    if not isinstance(saved.get("times"), dict):
        raise UsageError("tiempos históricos inválidos")
    for field in ("elapsed_seconds", "unpaused_seconds"):
        value = saved["times"].get(field)
        if value is not None:
            _decimal(value, field)
    lifecycle = saved.get("lifecycle")
    if (not isinstance(lifecycle, dict) or type(lifecycle.get("event_count")) is not int
            or lifecycle["event_count"] < 0):
        raise UsageError("lifecycle histórico inválido")
    return {**saved, "_history_stale": (
        usage["responses"] != record_count
        or lifecycle["event_count"] != len(binding["lifecycle_events"]))}


def _history_summary(entries: list[tuple[dict[str, Any], dict[str, Any] | None]]) -> dict[str, Any]:
    usage = {"responses": 0, **{key: 0 for key in COUNTERS}}
    reports = incomplete = stale = 0
    time_sums = {"elapsed_seconds": Decimal(0), "unpaused_seconds": Decimal(0)}
    time_known = {key: 0 for key in time_sums}
    usd_subtotal = Decimal(0)
    usd_known = usd_complete = 0
    for binding, saved in entries:
        if saved is None:
            continue
        reports += 1
        incomplete += saved["data_state"] == "incomplete"
        stale += saved["_history_stale"]
        for key in usage:
            usage[key] += saved["usage"][key]
        for key in time_sums:
            value = saved["times"].get(key)
            if value is not None:
                time_sums[key] += _decimal(value, key)
                time_known[key] += 1
        evidence = binding.get("actual_cost_evidence")
        if evidence is not None:
            if (not isinstance(evidence, dict)
                    or evidence.get("source_kind") != "user_attested_direct_charge"
                    or not isinstance(evidence.get("evidence_id"), str)
                    or not OPAQUE_ID.fullmatch(evidence["evidence_id"])
                    or not isinstance(evidence.get("evidence_sha256"), str)
                    or not SHA256_HEX.fullmatch(evidence["evidence_sha256"])
                    or type(evidence.get("complete_for_binding")) is not bool):
                raise UsageError("evidencia USD histórica inválida")
            usd_subtotal += _decimal(evidence.get("amount"), "USD declarado")
            usd_known += 1
            usd_complete += evidence.get("complete_for_binding") is True
    count = len(entries)
    times = {
        key: {
            "seconds": format(time_sums[key], "f") if count and time_known[key] == count else None,
            "known_subtotal_seconds": format(time_sums[key], "f") if time_known[key] else None,
            "known_bindings": time_known[key],
            "unknown_bindings": count - time_known[key],
        } for key in time_sums
    }
    return {
        "bindings": count,
        "reports": reports,
        "missing_reports": count - reports,
        "incomplete_reports": incomplete,
        "stale_reports": stale,
        "data_state": "empty" if not count else (
            "incomplete" if reports != count or incomplete or stale else "provisional"),
        "usage": usage,
        "times": times,
        "active_time_seconds": None,
        "usd": {
            "amount": format(usd_subtotal, "f") if count and usd_complete == count else None,
            "known_subtotal": format(usd_subtotal, "f") if usd_known else None,
            "known_bindings": usd_known,
            "unknown_bindings": count - usd_complete,
            "provenance": "user_attested_direct_charge" if usd_known else "unknown",
        },
    }


def history_report(*, ledger_path: Path | str, project_root: Path | str,
                   project_id: str) -> dict[str, Any]:
    """Summarize only prospectively marked bindings using persisted revisions."""
    if not isinstance(project_id, str) or not project_id.strip():
        raise UsageError("project_id requerido")
    ledger_path = _private_ledger(ledger_path, project_root)
    with _Lock(ledger_path):
        ledger = _read_json(ledger_path)
        groups: dict[tuple[str, str], list[tuple[dict[str, Any], dict[str, Any] | None]]] = {}
        record_counts: dict[str, int] = {}
        for record in ledger["records"].values():
            if not isinstance(record, dict) or not isinstance(record.get("binding_id"), str):
                raise UsageError("registro histórico inválido")
            binding_id = record.get("binding_id")
            record_counts[binding_id] = record_counts.get(binding_id, 0) + 1
        legacy = 0
        evidence_ids: set[str] = set()
        for binding in ledger["bindings"].values():
            if binding["project_id"] != project_id:
                continue
            kind, work_id = binding.get("work_kind"), binding.get("work_id")
            if kind is None and work_id is None:
                legacy += 1
                continue
            if (kind not in WORK_KINDS or not isinstance(work_id, str)
                    or not OPAQUE_ID.fullmatch(work_id)):
                raise UsageError("marca histórica inválida")
            evidence = binding.get("actual_cost_evidence")
            if isinstance(evidence, dict):
                evidence_id = evidence.get("evidence_id")
                if not isinstance(evidence_id, str) or not OPAQUE_ID.fullmatch(evidence_id):
                    raise UsageError("evidencia USD histórica inválida")
                if evidence_id in evidence_ids:
                    raise UsageError("evidencia USD duplicada en historial")
                evidence_ids.add(evidence_id)
            groups.setdefault((kind, work_id), []).append(
                (binding, _saved_measurement(binding,
                    record_counts.get(binding["binding_id"], 0))))
        items = [{"work_kind": kind, "work_id": work_id,
                  **_history_summary(groups[(kind, work_id)])}
                 for kind, work_id in sorted(groups)]
        categories = [{"work_kind": kind,
                       **_history_summary([entry for (category, _), group in groups.items()
                                           if category == kind for entry in group])}
                      for kind in WORK_KINDS]
        all_entries = [entry for group in groups.values() for entry in group]
        return {"history_version": HISTORY_VERSION, "project_id": project_id,
                "work_items": items, "categories": categories,
                "overall": _history_summary(all_entries),
                "legacy_bindings_excluded": legacy,
                "source_access": "none"}


def render_history_text(value: dict[str, Any]) -> str:
    lines = [f"Project work history · {value['project_id']}",
             f"Bindings: {value['overall']['bindings']} "
             f"(legacy excluded: {value['legacy_bindings_excluded']})",
             "Time: elapsed wall-clock only; active time=unknown",
             "USD_declared: user-attested direct charge only; unknown without complete evidence"]
    for row in value["categories"]:
        elapsed = row["times"]["elapsed_seconds"]["seconds"]
        usd = row["usd"]["amount"]
        lines.append(f"{row['work_kind']}: work={sum(item['work_kind'] == row['work_kind'] for item in value['work_items'])} "
                     f"responses={row['usage']['responses']} tokens={row['usage']['total_tokens']} "
                     f"elapsed={'unknown' if elapsed is None else elapsed + 's'} "
                     f"USD_declared={'unknown' if usd is None else usd} "
                     f"missing={row['missing_reports']} stale={row['stale_reports']} "
                     f"state={row['data_state']}")
    return "\n".join(lines)


def render_text(value: dict[str, Any]) -> str:
    usage = value["usage"]
    binding = value["binding"]
    lines = [
        f"Plan usage · {binding['requirement_ref']} · {binding['attempt_id']}",
        f"State: {value['data_state']}",
        f"Responses: {usage['responses']}",
        f"Tokens: input={usage['input_tokens']} cached_input={usage['cached_input_tokens']} "
        f"output={usage['output_tokens']} reasoning={usage['reasoning_output_tokens']} "
        f"cache_write={usage['cache_write_input_tokens']} total={usage['total_tokens']}",
    ]
    if value["report_version"] >= 2:
        lines.extend((
            f"Revision: {value['revision']['number']} "
            f"({'persisted' if value['revision']['persisted'] else 'preview'})",
            f"Lifecycle: technical={value['lifecycle']['technical_status']} "
            f"acceptance={value['lifecycle']['acceptance_status']}",
            f"Time: elapsed={value['times']['elapsed_seconds'] or 'unknown'}s "
            f"paused={value['times']['paused_seconds'] or 'unknown'}s",
            f"Cost: {value['cost']['amount'] or 'unknown'} USD "
            f"({value['cost']['nature']}; billed=unknown)",
        ))
    lines.extend(("Unknown: " + ", ".join(value["unknowns"]),
                  f"Anomalies: {len(value['anomalies'])}"))
    return "\n".join(lines)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Offline plan token observer")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--ledger", required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    bind_parser = sub.add_parser("bind")
    for name in ("project-id", "requirement-ref", "plan-version", "plan-digest",
                 "execution-id", "attempt-id", "source", "source-version", "session-id",
                 "thread-id", "root-turn-id"):
        bind_parser.add_argument("--" + name, required=True)
    bind_parser.add_argument("--slice-id")
    bind_parser.add_argument("--allow-root-turn-change", action="store_true")
    bind_parser.add_argument("--work-kind", choices=WORK_KINDS)
    bind_parser.add_argument("--work-id")
    bind_parser.add_argument("--activity-mode", action="store_true")
    for command in ("refresh", "disable", "report", "snapshot"):
        item = sub.add_parser(command)
        item.add_argument("--binding-id", required=True)
    for command in ("report", "snapshot"):
        sub.choices[command].add_argument("--format", choices=("json", "text"), default="text")
        sub.choices[command].add_argument("--rate-snapshot-id")
    history = sub.add_parser("history")
    history.add_argument("--project-id", required=True)
    history.add_argument("--format", choices=("json", "text"), default="text")
    activity_history = sub.add_parser("activity-history")
    activity_history.add_argument("--project-id", required=True)
    activity_history.add_argument("--format", choices=("json", "text"), default="text")
    activity_record = sub.add_parser("activity-record")
    activity_record.add_argument("--binding-id", required=True)
    activity_snapshot = sub.add_parser("activity-snapshot")
    activity_snapshot.add_argument("--binding-id", required=True)
    activity_snapshot.add_argument("--format", choices=("json", "text"), default="text")
    usd = sub.add_parser("record-usd")
    usd.add_argument("--binding-id", required=True)
    usd.add_argument("--amount", required=True)
    usd.add_argument("--evidence-id", required=True)
    usd.add_argument("--evidence-sha256", required=True)
    usd.add_argument("--complete-for-binding", action="store_true")
    suggest = sub.add_parser("suggest-kind")
    suggest.add_argument("--endpoint", required=True)
    sub.choices["report"].add_argument("--report-version", type=int, choices=(1, 2), default=2)
    sub.choices["report"].add_argument("--revision", type=int)
    lifecycle = sub.add_parser("lifecycle")
    lifecycle.add_argument("--binding-id", required=True)
    lifecycle.add_argument("--event-id", required=True)
    lifecycle.add_argument("--kind", required=True, choices=sorted(LIFECYCLE_KINDS))
    lifecycle.add_argument("--at", required=True)
    lifecycle.add_argument("--reference")
    lifecycle.add_argument("--response-id")
    observed = lifecycle.add_mutually_exclusive_group()
    observed.add_argument("--usage-observed", dest="usage_observed", action="store_true")
    observed.add_argument("--usage-unknown", dest="usage_observed", action="store_false")
    lifecycle.set_defaults(usage_observed=None)
    rates = sub.add_parser("register-rates")
    rates.add_argument("--rates-file", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    common = {"ledger_path": args.ledger, "project_root": args.project_root}
    try:
        if args.command == "bind":
            binding_id = bind(**common, project_id=args.project_id,
                requirement_ref=args.requirement_ref, plan_version=args.plan_version,
                plan_digest=args.plan_digest, execution_id=args.execution_id,
                attempt_id=args.attempt_id, slice_id=args.slice_id, source_path=args.source,
                source_version=args.source_version, session_id=args.session_id,
                thread_id=args.thread_id, root_turn_id=args.root_turn_id,
                allow_root_turn_change=args.allow_root_turn_change,
                work_kind=args.work_kind, work_id=args.work_id, activity_mode=args.activity_mode)
            print(binding_id)
        elif args.command == "refresh":
            print(json.dumps(refresh(**common, binding_id=args.binding_id), sort_keys=True))
        elif args.command == "disable":
            disable(**common, binding_id=args.binding_id)
        elif args.command == "lifecycle":
            value = record_lifecycle_event(**common, binding_id=args.binding_id,
                event_id=args.event_id, kind=args.kind, at=args.at,
                reference=args.reference, response_id=args.response_id,
                usage_observed=args.usage_observed)
            print(json.dumps(value, sort_keys=True))
        elif args.command == "register-rates":
            rates_path = Path(args.rates_file)
            _safe_regular(rates_path, "archivo de tarifas")
            snapshot_id = register_rate_snapshot(**common,
                snapshot=_unique_json(rates_path.read_bytes(), "archivo de tarifas"))
            print(snapshot_id)
        elif args.command == "history":
            value = history_report(**common, project_id=args.project_id)
            print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
                  if args.format == "json" else render_history_text(value))
        elif args.command == "activity-history":
            value = activity_history_report(**common, project_id=args.project_id)
            print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
                  if args.format == "json" else render_activity_history_text(value))
        elif args.command == "activity-record":
            receipt = _unique_json(os.sys.stdin.read(65537), "recibo de actividad")
            value = record_activity(**common, binding_id=args.binding_id, receipt=receipt)
            print(json.dumps(value, sort_keys=True))
        elif args.command == "activity-snapshot":
            value = snapshot_activity_report(**common, binding_id=args.binding_id)
            print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
                  if args.format == "json" else render_activity_history_text(
                      {"project_id": value["project_id"], "categories": value["categories"]}))
        elif args.command == "record-usd":
            value = record_actual_usd(**common, binding_id=args.binding_id,
                amount=args.amount, evidence_id=args.evidence_id,
                evidence_sha256=args.evidence_sha256,
                complete_for_binding=args.complete_for_binding)
            print(json.dumps(value, sort_keys=True))
        elif args.command == "suggest-kind":
            value = suggest_work_kind(summary=os.sys.stdin.read(513),
                                      endpoint=args.endpoint)
            print(json.dumps(value, sort_keys=True))
        elif args.command == "snapshot":
            value = snapshot_report(**common, binding_id=args.binding_id,
                                    rate_snapshot_id=args.rate_snapshot_id)
            print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
                  if args.format == "json" else render_text(value))
        else:
            value = report(**common, binding_id=args.binding_id,
                           report_version=args.report_version,
                           rate_snapshot_id=args.rate_snapshot_id,
                           revision=args.revision)
            print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
                  if args.format == "json" else render_text(value))
    except UsageError as exc:
        print(f"plan-usage: {exc}", file=os.sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
