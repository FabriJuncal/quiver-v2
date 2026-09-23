#!/usr/bin/env python3
"""Read-only Git variant discovery with explicit provenance and stale checks."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


SCHEMA_VERSION = 1
DEFAULT_MAX_CONTEXT_BYTES = 128 * 1024
MAX_CONTEXT_BYTES = 2 * 1024 * 1024
MAX_MANIFEST_BYTES = 1024 * 1024
REF_PREFIXES = ("refs/heads/", "refs/remotes/")
STACK_KEYS = (
    "@angular/core",
    "@ionic/angular",
    "@capacitor/core",
    "@capacitor/android",
    "@capacitor/ios",
)
SENSITIVE_PATH = re.compile(
    r"(?:^|/)(?:\.env(?:\..*)?|[^/]*\.(?:pem|key|p12|pfx|jks|keystore))$",
    re.IGNORECASE,
)
SENSITIVE_CONTENT = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\b(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"),
)


class DiscoveryError(RuntimeError):
    """Expected, user-actionable discovery failure."""


@dataclass(frozen=True)
class Repository:
    requested: Path
    root: Path
    common_dir: Path
    bare: bool
    object_format: str
    repository_id: str


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat()


def _json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"


def _digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def _git_env() -> dict[str, str]:
    env = dict(os.environ)
    env.update(
        GIT_NO_LAZY_FETCH="1",
        GIT_OPTIONAL_LOCKS="0",
        GIT_NO_REPLACE_OBJECTS="1",
        GIT_TERMINAL_PROMPT="0",
        GIT_CONFIG_NOSYSTEM=env.get("GIT_CONFIG_NOSYSTEM", "1"),
    )
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(name, None)
    return env


def _run_git(path: Path, *args: str, timeout: int = 30, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    try:
        result = subprocess.run(
            ["git", "--no-pager", "-c", "core.fsmonitor=false", "-C", str(path), *args],
            env=_git_env(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise DiscoveryError(f"Git no disponible o excedió el tiempo en {args[0] if args else 'comando'}") from exc
    if check and result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip().splitlines()
        message = detail[-1] if detail else f"exit {result.returncode}"
        raise DiscoveryError(f"Git {args[0] if args else 'command'} falló: {message}")
    return result


def open_repository(path: Path | str) -> Repository:
    requested = Path(path).expanduser().resolve()
    bare_raw = _run_git(requested, "rev-parse", "--is-bare-repository").stdout.strip()
    bare = bare_raw == b"true"
    root_command = ("rev-parse", "--absolute-git-dir") if bare else ("rev-parse", "--show-toplevel")
    root = Path(os.fsdecode(_run_git(requested, *root_command).stdout.strip())).resolve()
    common_raw = os.fsdecode(_run_git(requested, "rev-parse", "--git-common-dir").stdout.strip())
    common = Path(common_raw)
    if not common.is_absolute():
        common = (root / common).resolve()
    else:
        common = common.resolve()
    object_format = _run_git(requested, "rev-parse", "--show-object-format").stdout.decode().strip()
    if object_format not in {"sha1", "sha256"}:
        raise DiscoveryError(f"Formato de objetos Git no soportado: {object_format or 'vacío'}")
    repository_id = hashlib.sha256(os.fsencode(str(common))).hexdigest()
    partial = _run_git(requested, "config", "--local", "--get", "extensions.partialClone", check=False)
    if partial.returncode == 0 and partial.stdout.strip():
        raise DiscoveryError(
            "Clones parciales no están soportados en modo offline: completá objetos explícitamente o usá un clon completo"
        )
    return Repository(requested, root, common, bare, object_format, repository_id)


def _outside_repository(repo: Repository, output: Path | str) -> Path:
    raw = Path(output).expanduser()
    if not raw.is_absolute():
        raw = Path.cwd() / raw
    for candidate in (raw, *raw.parents):
        if candidate.exists():
            if candidate.is_symlink():
                raise DiscoveryError("El output no puede atravesar symlinks")
            break
    target = raw.resolve(strict=False)
    if target == repo.root or target.is_relative_to(repo.root):
        raise DiscoveryError("El output debe estar fuera del worktree/repositorio analizado")
    if target == repo.common_dir or target.is_relative_to(repo.common_dir):
        raise DiscoveryError("El output no puede escribirse dentro del common Git dir")
    current = target
    while not current.exists() and current != current.parent:
        current = current.parent
    if not current.is_dir():
        raise DiscoveryError("El ancestro existente del output debe ser un directorio real")
    return target


def _prepare_output(repo: Repository, output: Path | str) -> Path:
    target = _outside_repository(repo, output)
    target.mkdir(parents=True, exist_ok=True)
    if target.is_symlink() or not target.is_dir():
        raise DiscoveryError("El output debe ser un directorio real")
    return target


def _atomic_write(path: Path, data: bytes) -> None:
    if path.exists() and (path.is_symlink() or not path.is_file()):
        raise DiscoveryError(f"Destino inseguro: {path.name}")
    descriptor, temporary = tempfile.mkstemp(prefix=".branch-discovery-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def _write_json(path: Path, value: Any) -> None:
    _atomic_write(path, _json_bytes(value))


def _decode_path(raw: bytes) -> str:
    return raw.decode("utf-8", "surrogateescape")


def capture_refs(repo: Repository) -> list[dict[str, Any]]:
    result = _run_git(
        repo.requested,
        "for-each-ref",
        "--format=%(refname)%00%(objectname)%00%(symref)%00%(upstream)%00",
        "refs/heads",
        "refs/remotes",
    ).stdout
    refs: list[dict[str, Any]] = []
    for row in result.splitlines():
        fields = row.split(b"\0")
        if len(fields) != 5 or fields[-1] != b"":
            raise DiscoveryError("Salida inesperada de git for-each-ref")
        ref, oid, symbolic, upstream = (_decode_path(value) for value in fields[:4])
        if not ref.startswith(REF_PREFIXES):
            continue
        refs.append(
            {
                "name": ref,
                "oid": oid,
                "symbolic_target": symbolic or None,
                "upstream": upstream or None,
                "kind": "local" if ref.startswith("refs/heads/") else "remote",
            }
        )
    return sorted(refs, key=lambda item: item["name"])


def _tree_entries(repo: Repository, oid: str) -> dict[str, dict[str, Any]]:
    raw = _run_git(repo.requested, "ls-tree", "-r", "-z", "-l", oid, timeout=60).stdout
    entries: dict[str, dict[str, Any]] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        try:
            header, raw_path = record.split(b"\t", 1)
            mode, object_type, object_oid, size = header.split(b" ", 3)
        except ValueError as exc:
            raise DiscoveryError("Salida inesperada de git ls-tree") from exc
        path = _decode_path(raw_path)
        normalized_size = size.strip()
        if normalized_size == b"BAD":
            raise DiscoveryError(f"Objeto Git faltante para la ruta: {path}")
        try:
            byte_size = None if normalized_size == b"-" else int(normalized_size)
        except ValueError as exc:
            raise DiscoveryError(f"Tamaño de objeto Git inválido para la ruta: {path}") from exc
        entries[path] = {
            "mode": mode.decode("ascii"),
            "type": object_type.decode("ascii"),
            "oid": object_oid.decode("ascii"),
            "bytes": byte_size,
        }
    return entries


def _blob(repo: Repository, oid: str, *, max_bytes: int) -> bytes:
    size_raw = _run_git(repo.requested, "cat-file", "-s", oid).stdout.strip()
    try:
        size = int(size_raw)
    except ValueError as exc:
        raise DiscoveryError("Tamaño de blob inválido") from exc
    if size > max_bytes:
        raise DiscoveryError(f"Blob excede límite ({size} > {max_bytes} bytes)")
    content = _run_git(repo.requested, "cat-file", "blob", oid, timeout=30).stdout
    if len(content) != size:
        raise DiscoveryError("Longitud de blob inconsistente")
    return content


def _package_metadata(repo: Repository, entries: dict[str, dict[str, Any]]) -> dict[str, Any]:
    package = entries.get("package.json")
    result: dict[str, Any] = {
        "package_name": None,
        "declared_dependencies": {},
        "technical_signature": None,
        "lockfiles": [name for name in ("package-lock.json", "yarn.lock", "pnpm-lock.yaml") if name in entries],
    }
    if not package or package["type"] != "blob" or (package["bytes"] or 0) > MAX_MANIFEST_BYTES:
        return result
    try:
        value = json.loads(_blob(repo, package["oid"], max_bytes=MAX_MANIFEST_BYTES))
    except (DiscoveryError, UnicodeError, ValueError):
        return result
    if not isinstance(value, dict):
        return result
    dependencies: dict[str, Any] = {}
    for section in ("dependencies", "devDependencies"):
        current = value.get(section, {})
        if isinstance(current, dict):
            dependencies.update({key: current[key] for key in STACK_KEYS if isinstance(current.get(key), str)})
    result["package_name"] = value.get("name") if isinstance(value.get("name"), str) else None
    result["declared_dependencies"] = dict(sorted(dependencies.items()))
    result["technical_signature"] = _digest(result["declared_dependencies"])
    return result


def _platform(entries: dict[str, dict[str, Any]]) -> dict[str, Any]:
    evidence = []
    if any(path == "ios" or path.startswith("ios/") for path in entries):
        evidence.append("tracked ios tree")
    if any(path == "android" or path.startswith("android/") for path in entries):
        evidence.append("tracked android tree")
    if not evidence:
        return {"value": None, "status": "unknown", "evidence": []}
    value = "+".join(item.split()[1] for item in evidence)
    return {"value": value, "status": "inferred", "evidence": evidence}


def _head_overlay(repo: Repository) -> dict[str, Any]:
    head_run = _run_git(repo.requested, "rev-parse", "--verify", "HEAD", check=False)
    head = head_run.stdout.decode().strip() if head_run.returncode == 0 else None
    branch_run = _run_git(repo.requested, "symbolic-ref", "-q", "HEAD", check=False)
    branch = branch_run.stdout.decode().strip() if branch_run.returncode == 0 else None
    if repo.bare:
        status = b""
        applicability = "not-applicable-bare"
    else:
        status = _run_git(repo.requested, "status", "--porcelain=v1", "-z", "--untracked-files=all").stdout
        applicability = "recorded-not-included"
    return {
        "head_oid": head,
        "head_ref": branch,
        "status_sha256": hashlib.sha256(status).hexdigest(),
        "status_bytes": len(status),
        "applicability": applicability,
    }


def _repo_characteristics(repo: Repository) -> dict[str, Any]:
    shallow = _run_git(repo.requested, "rev-parse", "--is-shallow-repository", check=False)
    partial = _run_git(repo.requested, "config", "--local", "--get", "extensions.partialClone", check=False)
    version = _run_git(repo.requested, "--version").stdout.decode().strip()
    return {
        "bare": repo.bare,
        "shallow": shallow.stdout.strip() == b"true",
        "partial_clone_filter": partial.stdout.decode().strip() or None,
        "git_version": version,
    }


def _same_name_relations(repo: Repository, refs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    local = {item["name"].removeprefix("refs/heads/"): item for item in refs if item["kind"] == "local"}
    relations: list[dict[str, Any]] = []
    for item in refs:
        if item["kind"] != "remote" or item["symbolic_target"]:
            continue
        rest = item["name"].removeprefix("refs/remotes/")
        if "/" not in rest:
            continue
        remote, short = rest.split("/", 1)
        if short not in local:
            continue
        left, right = local[short]["oid"], item["oid"]
        count = _run_git(repo.requested, "rev-list", "--left-right", "--count", f"{left}...{right}", check=False)
        if count.returncode:
            values = (None, None)
        else:
            pieces = count.stdout.decode().strip().split()
            values = (int(pieces[0]), int(pieces[1])) if len(pieces) == 2 else (None, None)
        relations.append(
            {
                "local_ref": local[short]["name"],
                "remote_ref": item["name"],
                "remote": remote,
                "local_only_commits": values[0],
                "remote_only_commits": values[1],
                "tracking_configured": local[short]["upstream"] == item["name"],
            }
        )
    return relations


def build_inventory(repo: Repository) -> tuple[dict[str, Any], dict[str, Any], str, bool]:
    before = capture_refs(repo)
    non_symbolic = [item for item in before if not item["symbolic_target"]]
    snapshots: dict[str, Any] = {}
    tree_cache: dict[str, dict[str, dict[str, Any]]] = {}
    errors = []
    for oid in sorted({item["oid"] for item in non_symbolic}):
        try:
            tree_oid = _run_git(repo.requested, "rev-parse", f"{oid}^{{tree}}").stdout.decode().strip()
            entries = tree_cache.setdefault(tree_oid, _tree_entries(repo, tree_oid))
            metadata = _package_metadata(repo, entries)
            snapshots[oid] = {
                "commit_oid": oid,
                "tree_oid": tree_oid,
                "entry_count": len(entries),
                "blob_count": sum(value["type"] == "blob" for value in entries.values()),
                "total_blob_bytes": sum(value["bytes"] or 0 for value in entries.values() if value["type"] == "blob"),
                "package": metadata,
                "platform": _platform(entries),
            }
        except DiscoveryError as exc:
            errors.append({"oid": oid, "error": str(exc)})
    after = capture_refs(repo)
    stale = before != after
    if stale:
        errors.append({"scope": "refs", "error": "references changed during capture"})
    coverage = "complete" if not errors and len(snapshots) == len({item["oid"] for item in non_symbolic}) else "partial"
    blob_occurrences = 0
    unique_blobs: dict[str, int] = {}
    for snapshot in snapshots.values():
        for entry in tree_cache[snapshot["tree_oid"]].values():
            if entry["type"] != "blob":
                continue
            blob_occurrences += 1
            unique_blobs.setdefault(entry["oid"], entry["bytes"] or 0)
    inventory = {
        "schema_version": SCHEMA_VERSION,
        "artifact_type": "branch-inventory",
        "observed_at": _now(),
        "repository_id": repo.repository_id,
        "object_format": repo.object_format,
        "scope": {"include": ["refs/heads/*", "refs/remotes/*"], "exclude": ["symbolic refs as variants"]},
        "repository": _repo_characteristics(repo),
        "overlay": _head_overlay(repo),
        "refs": before,
        "snapshots": snapshots,
        "relations": _same_name_relations(repo, before),
        "deduplication": {
            "scope": "distinct commit tips successfully read",
            "blob_occurrences": blob_occurrences,
            "unique_blob_oids": len(unique_blobs),
            "occurrence_bytes": sum(
                entry["bytes"] or 0
                for snapshot in snapshots.values()
                for entry in tree_cache[snapshot["tree_oid"]].values()
                if entry["type"] == "blob"
            ),
            "unique_blob_bytes": sum(unique_blobs.values()),
            "content_read_policy": "read selected blob OIDs once and preserve every ref/path provenance",
        },
        "coverage": {
            "inventory": coverage,
            "refs_total": len(non_symbolic),
            "refs_symbolic": len(before) - len(non_symbolic),
            "tips_distinct": len({item["oid"] for item in non_symbolic}),
            "tips_read": len(snapshots),
            "semantic": "partial",
            "runtime": "not-run",
        },
        "errors": errors,
        "refs_stale": stale,
    }
    variants = []
    for item in non_symbolic:
        snapshot = snapshots.get(item["oid"])
        variants.append(
            {
                "variant_id": "ref-" + hashlib.sha256(item["name"].encode()).hexdigest()[:16],
                "ref": item["name"],
                "oid": item["oid"],
                "dimensions": {
                    "client": {"value": None, "status": "unknown", "evidence": []},
                    "platform": snapshot["platform"] if snapshot else {"value": None, "status": "unknown", "evidence": []},
                    "technical_signature": {
                        "value": snapshot["package"]["technical_signature"] if snapshot else None,
                        "status": "inferred" if snapshot and snapshot["package"]["technical_signature"] else "unknown",
                        "evidence": ["package.json declared dependency subset"] if snapshot and snapshot["package"]["technical_signature"] else [],
                    },
                    "channel": {"value": None, "status": "unknown", "evidence": []},
                    "activity": {"value": None, "status": "unknown", "evidence": []},
                },
            }
        )
    matrix = {
        "schema_version": SCHEMA_VERSION,
        "artifact_type": "variant-matrix",
        "repository_id": repo.repository_id,
        "generated_from": {"observed_at": inventory["observed_at"], "refs_digest": _digest(before)},
        "classification_policy": "technical evidence may be inferred; client/channel/activity remain unknown until reviewed",
        "variants": variants,
    }
    map_text = _repository_map(inventory, matrix)
    return inventory, matrix, map_text, stale


def _repository_map(inventory: dict[str, Any], matrix: dict[str, Any]) -> str:
    refs = inventory["refs"]
    local = sum(item["kind"] == "local" and not item["symbolic_target"] for item in refs)
    remote = sum(item["kind"] == "remote" and not item["symbolic_target"] for item in refs)
    signatures: dict[str, int] = {}
    for item in matrix["variants"]:
        value = item["dimensions"]["technical_signature"]["value"]
        if value:
            signatures[value] = signatures.get(value, 0) + 1
    lines = [
        "# Repository variant map",
        "",
        f"Observed: `{inventory['observed_at']}`",
        f"Repository ID: `{inventory['repository_id']}`",
        "",
        "## Coverage",
        "",
        f"- Local refs: {local}",
        f"- Remote refs: {remote}",
        f"- Symbolic refs excluded as variants: {inventory['coverage']['refs_symbolic']}",
        f"- Distinct/read tips: {inventory['coverage']['tips_distinct']}/{inventory['coverage']['tips_read']}",
        f"- Inventory: {inventory['coverage']['inventory']}",
        f"- Technical signatures from declared dependencies: {len(signatures)}",
        "- Client, channel and activity: unknown until reviewed.",
        "- Static presence does not prove runtime enablement.",
        "",
        "## Refs",
        "",
        "| Ref | OID | Kind | Snapshot |",
        "|---|---|---|---|",
    ]
    for item in refs:
        state = "symbolic alias" if item["symbolic_target"] else ("read" if item["oid"] in inventory["snapshots"] else "unavailable")
        lines.append(f"| `{item['name']}` | `{item['oid']}` | {item['kind']} | {state} |")
    if inventory["errors"]:
        lines.extend(["", "## Limitations", ""])
        lines.extend(f"- {item.get('oid', item.get('scope', 'unknown'))}: {item['error']}" for item in inventory["errors"])
    return "\n".join(lines) + "\n"


def inspect_command(args: argparse.Namespace) -> int:
    repo = open_repository(args.repo)
    output = _prepare_output(repo, args.output)
    inventory, matrix, map_text, stale = build_inventory(repo)
    _write_json(output / "BRANCH_INVENTORY.json", inventory)
    _write_json(output / "VARIANTS.json", matrix)
    _atomic_write(output / "REPOSITORY_MAP.md", map_text.encode())
    print(
        f"Inventory: {inventory['coverage']['refs_total']} refs, "
        f"{inventory['coverage']['tips_read']}/{inventory['coverage']['tips_distinct']} tips; "
        f"coverage={inventory['coverage']['inventory']}; output={output}"
    )
    return 3 if stale else 0


def _full_ref(value: str) -> str:
    if not value.startswith(REF_PREFIXES) or value.endswith("/") or ".." in value or "@{" in value:
        raise DiscoveryError("Usá una ref completa bajo refs/heads/ o refs/remotes/")
    return value


def _resolve_ref(repo: Repository, value: str) -> str:
    ref = _full_ref(value)
    run = _run_git(repo.requested, "show-ref", "--verify", "--hash", ref, check=False)
    if run.returncode:
        raise DiscoveryError(f"Ref inexistente o no verificable: {ref}")
    oid = run.stdout.decode().strip()
    commit = _run_git(repo.requested, "rev-parse", "--verify", f"{oid}^{{commit}}", check=False)
    if commit.returncode:
        raise DiscoveryError(f"La ref no apunta a un commit: {ref}")
    return commit.stdout.decode().strip()


def compare(repo: Repository, left_ref: str, right_ref: str) -> dict[str, Any]:
    left_oid, right_oid = _resolve_ref(repo, left_ref), _resolve_ref(repo, right_ref)
    left, right = _tree_entries(repo, left_oid), _tree_entries(repo, right_oid)
    paths = sorted(set(left) | set(right))
    changes = []
    for path in paths:
        if left.get(path) == right.get(path):
            continue
        if path not in left:
            status = "added-right"
        elif path not in right:
            status = "removed-right"
        else:
            status = "changed"
        changes.append({"path": path, "status": status, "left": left.get(path), "right": right.get(path)})
    bases_run = _run_git(repo.requested, "merge-base", "--all", left_oid, right_oid, check=False)
    bases = bases_run.stdout.decode().split() if bases_run.returncode == 0 else []
    counts_run = _run_git(repo.requested, "rev-list", "--left-right", "--count", f"{left_oid}...{right_oid}", check=False)
    counts = counts_run.stdout.decode().split() if counts_run.returncode == 0 else []
    return {
        "schema_version": SCHEMA_VERSION,
        "artifact_type": "tip-comparison",
        "repository_id": repo.repository_id,
        "observed_at": _now(),
        "left": {"ref": _full_ref(left_ref), "oid": left_oid},
        "right": {"ref": _full_ref(right_ref), "oid": right_oid},
        "merge_bases": bases,
        "history_complete": not _repo_characteristics(repo)["shallow"],
        "left_only_commits": int(counts[0]) if len(counts) == 2 else None,
        "right_only_commits": int(counts[1]) if len(counts) == 2 else None,
        "rename_detection": "not-run",
        "changed_paths": len(changes),
        "changes": changes,
    }


def compare_command(args: argparse.Namespace) -> int:
    repo = open_repository(args.repo)
    result = compare(repo, args.left, args.right)
    data = _json_bytes(result)
    if args.output:
        output = _outside_repository(repo, args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.parent.is_symlink():
            raise DiscoveryError("Directorio de output inseguro")
        _atomic_write(output, data)
    else:
        sys.stdout.buffer.write(data)
    return 0


def _path(value: str) -> str:
    pure = PurePosixPath(value)
    if not value or pure.is_absolute() or ".." in pure.parts or value.endswith("/"):
        raise DiscoveryError(f"Ruta Git inválida: {value!r}")
    return value


def _unique_json(path: Path, *, max_bytes: int = MAX_MANIFEST_BYTES) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > max_bytes:
        raise DiscoveryError(f"JSON ausente, inseguro o demasiado grande: {path}")

    def pairs(items: Iterable[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in items:
            if key in value:
                raise DiscoveryError(f"JSON con clave duplicada: {key}")
            value[key] = item
        return value

    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs)
    except (OSError, UnicodeError, ValueError) as exc:
        if isinstance(exc, DiscoveryError):
            raise
        raise DiscoveryError(f"JSON inválido: {path.name}") from exc
    if not isinstance(value, dict):
        raise DiscoveryError("El JSON debe ser un objeto")
    return value


def _task(path: Path) -> dict[str, Any]:
    task = _unique_json(path)
    allowed = {"objective", "paths", "required_paths", "max_bytes"}
    if set(task) - allowed:
        raise DiscoveryError("Tarea contiene campos fuera del contrato")
    objective = task.get("objective")
    paths = task.get("paths")
    required = task.get("required_paths", paths)
    maximum = task.get("max_bytes", DEFAULT_MAX_CONTEXT_BYTES)
    if not isinstance(objective, str) or not objective.strip():
        raise DiscoveryError("Tarea sin objective")
    if not isinstance(paths, list) or not paths or any(not isinstance(item, str) for item in paths):
        raise DiscoveryError("Tarea sin paths explícitos")
    if not isinstance(required, list) or any(not isinstance(item, str) for item in required):
        raise DiscoveryError("required_paths inválido")
    if type(maximum) is not int or maximum < 1 or maximum > MAX_CONTEXT_BYTES:
        raise DiscoveryError(f"max_bytes debe ser entero entre 1 y {MAX_CONTEXT_BYTES}")
    selected = [_path(item) for item in paths]
    required_paths = [_path(item) for item in required]
    if len(selected) != len(set(selected)) or len(required_paths) != len(set(required_paths)):
        raise DiscoveryError("Rutas duplicadas en tarea")
    if not set(required_paths) <= set(selected):
        raise DiscoveryError("required_paths debe ser subconjunto de paths")
    return {"objective": objective.strip(), "paths": selected, "required_paths": required_paths, "max_bytes": maximum}


def build_context(repo: Repository, target_ref: str, task: dict[str, Any]) -> dict[str, Any]:
    target_oid = _resolve_ref(repo, target_ref)
    tree_oid = _run_git(repo.requested, "rev-parse", f"{target_oid}^{{tree}}").stdout.decode().strip()
    tree = _tree_entries(repo, tree_oid)
    selected = []
    total = 0
    missing = []
    for path in task["paths"]:
        entry = tree.get(path)
        if not entry:
            missing.append(path)
            continue
        if entry["type"] != "blob" or entry["mode"] in {"120000", "160000"}:
            raise DiscoveryError(f"Contexto no regular rechazado: {path}")
        if SENSITIVE_PATH.search(path):
            raise DiscoveryError(f"Ruta potencialmente sensible rechazada: {path}")
        remaining = task["max_bytes"] - total
        if remaining < 0 or (entry["bytes"] or 0) > remaining:
            raise DiscoveryError(f"Presupuesto de contexto excedido en {path}")
        raw = _blob(repo, entry["oid"], max_bytes=remaining)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise DiscoveryError(f"Contexto no textual UTF-8: {path}") from exc
        if any(marker.search(text) for marker in SENSITIVE_CONTENT):
            raise DiscoveryError(f"Contenido potencialmente sensible rechazado: {path}")
        total += len(raw)
        selected.append(
            {
                "path": path,
                "mode": entry["mode"],
                "blob_oid": entry["oid"],
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "text": text,
            }
        )
    required_missing = sorted(set(task["required_paths"]) & set(missing))
    if required_missing:
        raise DiscoveryError("Falta contexto obligatorio: " + ", ".join(required_missing))
    if not selected:
        raise DiscoveryError("La selección no produjo contexto utilizable")
    overlay = _head_overlay(repo)
    material = [{key: item[key] for key in ("path", "mode", "blob_oid", "bytes", "sha256")} for item in selected]
    return {
        "schema_version": SCHEMA_VERSION,
        "artifact_type": "branch-context",
        "created_at": _now(),
        "repository_id": repo.repository_id,
        "object_format": repo.object_format,
        "target_ref": _full_ref(target_ref),
        "target_oid": target_oid,
        "tree_oid": tree_oid,
        "overlay": overlay,
        "objective": task["objective"],
        "entries": selected,
        "missing_optional_paths": missing,
        "total_bytes": total,
        "budget_bytes": task["max_bytes"],
        "selection_digest": _digest(material),
        "coverage": "complete" if not missing else "partial",
        "runtime_verified": False,
    }


def context_command(args: argparse.Namespace) -> int:
    repo = open_repository(args.repo)
    output = _prepare_output(repo, args.output)
    manifest = build_context(repo, args.target, _task(Path(args.task).expanduser().resolve()))
    destination = output / "CONTEXT_MANIFEST.json"
    _write_json(destination, manifest)
    print(f"Context: {len(manifest['entries'])} files, {manifest['total_bytes']} bytes; output={destination}")
    return 0


def validate_context(repo: Repository, manifest: dict[str, Any]) -> None:
    required = {
        "schema_version", "artifact_type", "created_at", "repository_id", "object_format",
        "target_ref", "target_oid", "tree_oid", "overlay", "objective", "entries",
        "missing_optional_paths", "total_bytes", "budget_bytes", "selection_digest",
        "coverage", "runtime_verified",
    }
    if set(manifest) != required or manifest.get("schema_version") != SCHEMA_VERSION or manifest.get("artifact_type") != "branch-context":
        raise DiscoveryError("Manifest de contexto fuera del contrato")
    if manifest["repository_id"] != repo.repository_id or manifest["object_format"] != repo.object_format:
        raise DiscoveryError("Contexto pertenece a otro repositorio/formato")
    current_oid = _resolve_ref(repo, manifest["target_ref"])
    if current_oid != manifest["target_oid"]:
        raise DiscoveryError("Contexto obsoleto: la ref objetivo cambió")
    current_tree = _run_git(repo.requested, "rev-parse", f"{current_oid}^{{tree}}").stdout.decode().strip()
    if current_tree != manifest["tree_oid"]:
        raise DiscoveryError("Contexto obsoleto: el árbol objetivo cambió")
    if _head_overlay(repo) != manifest["overlay"]:
        raise DiscoveryError("Contexto obsoleto: HEAD o overlay local cambió")
    entries = manifest["entries"]
    if not isinstance(entries, list) or not entries:
        raise DiscoveryError("Manifest sin entradas")
    tree = _tree_entries(repo, current_tree)
    material, paths, total = [], set(), 0
    for item in entries:
        keys = {"path", "mode", "blob_oid", "bytes", "sha256", "text"}
        if not isinstance(item, dict) or set(item) != keys or item["path"] in paths:
            raise DiscoveryError("Entrada de contexto inválida o duplicada")
        paths.add(item["path"])
        actual = tree.get(item["path"])
        raw = item["text"].encode("utf-8") if isinstance(item["text"], str) else b""
        if not actual or actual["mode"] != item["mode"] or actual["oid"] != item["blob_oid"]:
            raise DiscoveryError(f"Procedencia de contexto inválida: {item['path']}")
        if item["bytes"] != len(raw) or hashlib.sha256(raw).hexdigest() != item["sha256"]:
            raise DiscoveryError(f"Integridad de contexto inválida: {item['path']}")
        total += len(raw)
        material.append({key: item[key] for key in ("path", "mode", "blob_oid", "bytes", "sha256")})
    if total != manifest["total_bytes"] or total > manifest["budget_bytes"] or _digest(material) != manifest["selection_digest"]:
        raise DiscoveryError("Totales o digest de selección inconsistentes")


def validate_context_file(repo_path: Path | str, manifest_path: Path | str) -> dict[str, Any]:
    """Load and validate one context manifest for doctor and CLI consumers."""
    repo = open_repository(repo_path)
    manifest = _unique_json(Path(manifest_path).expanduser().resolve(), max_bytes=8 * 1024 * 1024)
    validate_context(repo, manifest)
    return manifest


def check_command(args: argparse.Namespace) -> int:
    manifest = validate_context_file(args.repo, args.manifest)
    print(
        f"Context PASS: {manifest['target_ref']}@{manifest['target_oid']} "
        f"({len(manifest['entries'])} files, {manifest['total_bytes']} bytes)"
    )
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Read-only discovery for Git repositories with branch variants")
    commands = root.add_subparsers(dest="command", required=True)
    inspect_parser = commands.add_parser("inspect", help="write inventory, matrix and map")
    inspect_parser.add_argument("--repo", type=Path, required=True)
    inspect_parser.add_argument("--output", type=Path, required=True)
    inspect_parser.set_defaults(run=inspect_command)
    compare_parser = commands.add_parser("compare", help="compare two exact full refs")
    compare_parser.add_argument("--repo", type=Path, required=True)
    compare_parser.add_argument("--left", required=True)
    compare_parser.add_argument("--right", required=True)
    compare_parser.add_argument("--output", type=Path)
    compare_parser.set_defaults(run=compare_command)
    context_parser = commands.add_parser("context", help="select explicit textual context at one ref")
    context_parser.add_argument("--repo", type=Path, required=True)
    context_parser.add_argument("--target", required=True)
    context_parser.add_argument("--task", type=Path, required=True)
    context_parser.add_argument("--output", type=Path, required=True)
    context_parser.set_defaults(run=context_command)
    check_parser = commands.add_parser("check", help="validate context provenance and freshness")
    check_parser.add_argument("--repo", type=Path, required=True)
    check_parser.add_argument("--manifest", type=Path, required=True)
    check_parser.set_defaults(run=check_command)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return args.run(args)
    except DiscoveryError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
