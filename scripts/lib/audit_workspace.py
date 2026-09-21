"""Read-only inventories/comparisons, not a sandbox, secret scanner or atomic snapshot.

No writes, models, subprocesses, network, patch application or restoration. Caller
selects a reviewed root and persists stdout outside it. Clean means no FINAL differences.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys


class AuditError(ValueError):
    pass


def checked_path(path):
    """Reject existing symlink components, including parents of an explicit root.

    A precheck, not a guarantee against malicious concurrent path replacement.
    Use canonical paths (e.g. /private/tmp on macOS rather than its /tmp alias).
    """
    path = Path(path).absolute()
    if '..' in path.parts or any(p.is_symlink() for p in (path, *path.parents)):
        raise AuditError('raíz/documento contiene enlace o ..; usar path canónico')
    return path


def fingerprint(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def read_regular(name, parent_fd=None):
    """Do not follow the final link; compare opened inode before/after reading."""
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    fd = os.open(name, flags, dir_fd=parent_fd)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise AuditError('archivo no regular o hardlink')
        chunks = []
        while block := os.read(fd, 65536):
            chunks.append(block)
        if fingerprint(before) != fingerprint(os.fstat(fd)):
            raise AuditError('archivo cambió durante lectura')
        if fingerprint(before) != fingerprint(os.stat(name, dir_fd=parent_fd, follow_symlinks=False)):
            raise AuditError('archivo reemplazado durante lectura')
        return b''.join(chunks), before
    finally:
        os.close(fd)


def load_document(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise AuditError('clave JSON duplicada')
            result[key] = value
        return result
    try:
        raw, _ = read_regular(checked_path(path))
        return json.loads(raw, object_pairs_hook=unique,
                          parse_constant=lambda _: (_ for _ in ()).throw(AuditError('JSON no finito')))
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        raise AuditError('documento inválido o ilegible') from exc


def canonical_path(value):
    if not isinstance(value, str) or not value or '\\' in value or '\x00' in value:
        raise AuditError('path inválido')
    path = Path(value)
    if value != '.' and (path.is_absolute() or '..' in path.parts or path.as_posix() != value):
        raise AuditError('path no canónico o externo')
    return value


def validate_manifest(value):
    if not isinstance(value, dict) or set(value) != {'manifest_version', 'scope_id', 'entries'}:
        raise AuditError('manifest incompleto o campos desconocidos')
    if type(value['manifest_version']) is not int or value['manifest_version'] != 1:
        raise AuditError('versión de manifest desconocida')
    if not isinstance(value['scope_id'], str) or not value['scope_id'].strip():
        raise AuditError('scope_id vacío')
    if not isinstance(value['entries'], list) or not value['entries']:
        raise AuditError('manifest sin entradas')
    entries = {}
    for item in value['entries']:
        if not isinstance(item, dict) or set(item) != {'path', 'kind', 'mode', 'size', 'sha256'}:
            raise AuditError('entrada de manifest inválida')
        name = canonical_path(item['path'])
        if name in entries:
            raise AuditError('path duplicado')
        if type(item['mode']) is not int or not 0 <= item['mode'] <= 0o7777:
            raise AuditError('permisos inválidos')
        if item['kind'] == 'directory':
            if item['size'] is not None or item['sha256'] is not None:
                raise AuditError('metadata de directorio inválida')
        elif item['kind'] == 'file':
            if type(item['size']) is not int or item['size'] < 0 or not isinstance(item['sha256'], str) or not re.fullmatch('[a-f0-9]{64}', item['sha256']):
                raise AuditError('metadata de archivo inválida')
        else:
            raise AuditError('tipo no permitido; enlaces y archivos especiales excluidos')
        entries[name] = item
    if '.' not in entries or entries['.']['kind'] != 'directory':
        raise AuditError('falta raíz del manifest')
    for name in entries:
        parent = Path(name).parent.as_posix()
        if parent not in entries or entries[parent]['kind'] != 'directory':
            raise AuditError('jerarquía de manifest inválida')
    if list(entries) != sorted(entries):
        raise AuditError('manifest no ordenado')
    return entries


def inventory(root, scope_id):
    root = checked_path(root)
    entries = []

    def walk(fd, relative):
        before = os.fstat(fd)
        entries.append({'path': relative, 'kind': 'directory',
                        'mode': stat.S_IMODE(before.st_mode), 'size': None, 'sha256': None})
        names = sorted(os.listdir(fd))
        for name in names:
            rel = name if relative == '.' else relative + '/' + name
            canonical_path(rel)
            info = os.stat(name, dir_fd=fd, follow_symlinks=False)
            if stat.S_ISDIR(info.st_mode):
                child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                try:
                    if fingerprint(info) != fingerprint(os.fstat(child)):
                        raise AuditError('directorio reemplazado durante lectura')
                    walk(child, rel)
                    if fingerprint(info) != fingerprint(os.stat(name, dir_fd=fd, follow_symlinks=False)):
                        raise AuditError('directorio cambió durante inventario')
                finally:
                    os.close(child)
            elif stat.S_ISREG(info.st_mode) and info.st_nlink == 1:
                raw, opened = read_regular(name, fd)
                if fingerprint(info) != fingerprint(opened):
                    raise AuditError('archivo cambió durante inventario')
                entries.append({'path': rel, 'kind': 'file', 'mode': stat.S_IMODE(info.st_mode),
                                'size': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
            else:
                raise AuditError('enlace o archivo especial no permitido: ' + rel)
        if names != sorted(os.listdir(fd)) or fingerprint(before) != fingerprint(os.fstat(fd)):
            raise AuditError('directorio cambió durante inventario')

    try:
        fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            root_before = os.fstat(fd)
            walk(fd, '.')
            if fingerprint(root_before) != fingerprint(root.stat(follow_symlinks=False)):
                raise AuditError('raíz cambió durante inventario')
        finally:
            os.close(fd)
    except (OSError, RecursionError) as exc:
        raise AuditError('inventario incompleto; raíz/archivo ilegible, enlace o profundidad excesiva') from exc
    result = {'manifest_version': 1, 'scope_id': scope_id,
              'entries': sorted(entries, key=lambda item: item['path'])}
    validate_manifest(result)
    return result


def document_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def compare(before, after):
    left, right = validate_manifest(before), validate_manifest(after)
    if before['scope_id'] != after['scope_id']:
        raise AuditError('scope_id diferentes; no comparar bases distintas')
    changes = []
    for name in sorted(left.keys() | right.keys()):
        if left.get(name) != right.get(name):
            changes.append({'path': name, 'change': 'added' if name not in left else
                            'removed' if name not in right else 'modified'})
    return {'audit_version': 1, 'scope_id': before['scope_id'],
            'before_digest': document_digest(before), 'after_digest': document_digest(after),
            'result': 'changed' if changes else 'clean', 'changes': changes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='operation', required=True)
    snap = subs.add_parser('snapshot')
    snap.add_argument('--root', type=Path, required=True)
    snap.add_argument('--scope-id', required=True)
    diff = subs.add_parser('compare')
    diff.add_argument('--before', type=Path, required=True)
    diff.add_argument('--after', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.operation == 'snapshot':
            result = inventory(args.root, args.scope_id)
        else:
            result = compare(load_document(args.before), load_document(args.after))
        print(json.dumps(result, indent=2, ensure_ascii=True))
        print('OBSERVACIÓN FINAL solamente; permisos, cambios transitorios y efectos externos NO VERIFICADOS.', file=sys.stderr)
        return 2 if result.get('result') == 'changed' else 0
    except (AuditError, OSError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
