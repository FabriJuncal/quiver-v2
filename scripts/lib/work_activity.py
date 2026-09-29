"""Private, prospective activity receipts and conservative Kev classification.

This module never opens a Codex session source. Callers supply small, structured
receipts created while a supported local action is running. Raw file contents,
diffs, prompts, command arguments and summaries are deliberately not persisted.
"""
from __future__ import annotations

import datetime as dt
import http.client
import json
import math
import re
from typing import Any
from urllib.parse import urlsplit


ACTIVITY_KINDS = ("feature", "bug", "test", "explanation", "documentation")
KEV_TIMEOUT_SECONDS = 180
DISPLAY_KINDS = (*ACTIVITY_KINDS, "implementation_unspecified", "mixed", "unassigned")
ACTION_KINDS = ("code", "test", "explanation", "documentation")
OUTCOMES = ("completed", "failed", "cancelled", "unknown")
OPAQUE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
ROLE = re.compile(r"[a-z][a-z0-9_-]{0,63}\Z")


class ActivityError(RuntimeError):
    """Expected validation error for an activity receipt or Kev response."""


def _json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def _timestamp(value: Any, label: str) -> tuple[str, dt.datetime]:
    if not isinstance(value, str) or not value:
        raise ActivityError(f"{label} ausente")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ActivityError(f"{label} inválido") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ActivityError(f"{label} requiere zona horaria")
    normalized = parsed.astimezone(dt.timezone.utc)
    return normalized.isoformat().replace("+00:00", "Z"), normalized


def _opaque(value: Any, label: str) -> str:
    if not isinstance(value, str) or not OPAQUE_ID.fullmatch(value):
        raise ActivityError(f"{label} inválido")
    return value


def _roles(value: Any) -> list[str]:
    if not isinstance(value, list) or len(value) > 32 or any(
            not isinstance(item, str) or not ROLE.fullmatch(item) for item in value):
        raise ActivityError("roles de archivo inválidos")
    return sorted(set(value))


def normalize_receipt(value: Any) -> dict[str, Any]:
    """Return a minimal, persistable receipt. `summary` is never an input here."""
    if not isinstance(value, dict) or set(value) - {
            "activity_id", "operation_id", "response_id", "actions", "manifest_complete",
            "started_at", "ended_at", "outcome", "tool_seconds"}:
        raise ActivityError("recibo de actividad inválido")
    activity_id = _opaque(value.get("activity_id"), "activity_id")
    operation_id = _opaque(value.get("operation_id"), "operation_id")
    response_id = _opaque(value.get("response_id"), "response_id")
    actions = value.get("actions")
    if not isinstance(actions, list) or not actions or len(actions) > 32:
        raise ActivityError("acciones inválidas")
    clean_actions = []
    for action in actions:
        if not isinstance(action, dict) or set(action) != {"kind", "file_roles"}:
            raise ActivityError("acción inválida")
        if action["kind"] not in ACTION_KINDS:
            raise ActivityError("tipo de acción inválido")
        clean_actions.append({"kind": action["kind"], "file_roles": _roles(action["file_roles"])})
    if type(value.get("manifest_complete")) is not bool:
        raise ActivityError("manifest_complete debe ser booleano")
    started, started_dt = _timestamp(value.get("started_at"), "started_at")
    ended, ended_dt = _timestamp(value.get("ended_at"), "ended_at")
    if ended_dt < started_dt:
        raise ActivityError("ended_at anterior a started_at")
    if value.get("outcome") not in OUTCOMES:
        raise ActivityError("outcome inválido")
    tool_seconds = value.get("tool_seconds")
    if tool_seconds is not None and (type(tool_seconds) not in {int, float}
                                     or not math.isfinite(tool_seconds) or tool_seconds < 0):
        raise ActivityError("tool_seconds inválido")
    return {
        "activity_id": activity_id,
        "operation_id": operation_id,
        "response_id": response_id,
        "actions": clean_actions,
        "manifest_complete": value["manifest_complete"],
        "started_at": started,
        "ended_at": ended,
        "elapsed_seconds": format(ended_dt.timestamp() - started_dt.timestamp(), ".6f"),
        "tool_seconds": None if tool_seconds is None else format(tool_seconds, ".6f"),
        "outcome": value["outcome"],
    }


def rule_classify(receipt: dict[str, Any]) -> dict[str, str]:
    """Classify only explicit action evidence; code needs a separate inference."""
    kinds = {item["kind"] for item in receipt["actions"]}
    explicit = kinds - {"code"}
    if len(explicit) > 1 or ("code" in kinds and explicit):
        return {"kind": "mixed", "provenance": "rule", "validation": "not_applicable"}
    if explicit:
        return {"kind": next(iter(explicit)), "provenance": "rule", "validation": "not_applicable"}
    if kinds == {"code"}:
        return {"kind": "implementation_unspecified", "provenance": "unknown",
                "validation": "not_applicable"}
    return {"kind": "unassigned", "provenance": "unknown", "validation": "not_applicable"}


def _local_endpoint(endpoint: Any) -> int:
    if not isinstance(endpoint, str):
        raise ActivityError("endpoint Kev inválido")
    try:
        url = urlsplit(endpoint)
        port = url.port
    except (TypeError, ValueError) as exc:
        raise ActivityError("endpoint Kev inválido") from exc
    if (url.scheme != "http" or url.hostname not in {"127.0.0.1", "localhost"}
            or port is None or url.username is not None or url.password is not None
            or url.path not in {"", "/"} or url.query or url.fragment):
        raise ActivityError("Kev requiere endpoint HTTP local con puerto explícito")
    return port


def kev_classify(*, summary: str, endpoint: str, _transport: Any = None) -> dict[str, Any]:
    """Return independent Kev signals. The summary is never returned or persisted."""
    if not isinstance(summary, str) or not summary.strip() or len(summary) > 512 or "\x00" in summary:
        raise ActivityError("resumen breve requerido (máximo 512 caracteres)")
    port = _local_endpoint(endpoint)
    request = {"state": summary, "model": "kev-latest", "questions": {
        kind: {"type": "noul", "instructions": f"Is this activity {kind}?"}
        for kind in ACTIVITY_KINDS}}
    body = _json_bytes(request)
    if _transport is None:
        connection = http.client.HTTPConnection("127.0.0.1", port, timeout=KEV_TIMEOUT_SECONDS)
        try:
            connection.request("POST", "/v1/systemone", body, {"Content-Type": "application/json"})
            response = connection.getresponse()
            raw = response.read(65537)
            if response.status != 200 or len(raw) > 65536:
                raise ActivityError("respuesta Kev no soportada")
        except OSError as exc:
            raise ActivityError("servidor Kev local no disponible") from exc
        finally:
            connection.close()
    else:
        raw = _transport(body, port)
    try:
        value = json.loads(raw, parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (TypeError, UnicodeError, ValueError) as exc:
        raise ActivityError("respuesta Kev malformada") from exc
    answers = value.get("answers") if isinstance(value, dict) else None
    if not isinstance(answers, dict) or set(answers) != set(ACTIVITY_KINDS):
        raise ActivityError("respuesta Kev incompleta")
    signals: dict[str, float] = {}
    for kind, answer in answers.items():
        score = answer.get("noul") if isinstance(answer, dict) and answer.get("type") == "noul" else None
        if type(score) not in {int, float} or not math.isfinite(score) or not 0 <= score <= 1:
            raise ActivityError("señal Kev inválida")
        signals[kind] = float(score)
    return {"signals": signals, "provenance": "kev_inferred", "validation": "unvalidated"}


def classify(receipt: dict[str, Any], kev: dict[str, Any] | None = None,
             threshold: float = 0.9) -> dict[str, Any]:
    """Rules win; Kev can classify a code-only activity but must be unambiguous."""
    base = rule_classify(receipt)
    if base["kind"] != "implementation_unspecified" or kev is None:
        return base
    signals = kev.get("signals") if isinstance(kev, dict) else None
    if (type(threshold) not in {int, float} or not 0 < threshold <= 1
            or not isinstance(signals, dict) or set(signals) != set(ACTIVITY_KINDS)):
        raise ActivityError("clasificación Kev inválida")
    accepted = [kind for kind, score in signals.items()
                if type(score) in {int, float} and math.isfinite(score) and score >= threshold]
    if len(accepted) == 1:
        return {"kind": accepted[0], "provenance": "kev_inferred", "validation": "unvalidated"}
    return {"kind": "mixed" if len(accepted) > 1 else "implementation_unspecified",
            "provenance": "kev_inferred", "validation": "unvalidated"}
