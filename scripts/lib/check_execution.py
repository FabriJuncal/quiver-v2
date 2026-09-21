"""Read-only validation of opt-in delegation records. No tools, dispatch or model calls.

Schema is the single structural contract. This deliberately implements only its
small documented subset, not a general JSON Schema engine. References stay local.
Recorded evidence is not proof of real process termination, permissions or tests.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

# Python -I omits the script directory. Load only this distribution's sibling.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_workspace import AuditError, compare, load_document, validate_manifest

SCHEMA = Path(__file__).resolve().parents[2] / 'templates/slice/RUN.schema.json'
TERMINAL = {'accepted', 'failed', 'cancelled'}
TRANSITIONS = {
    'prepared': {'running', 'failed', 'cancelled'},
    'running': {'submitted', 'failed', 'cancelled'},
    'submitted': {'accepted', 'failed', 'cancelled'},
    'accepted': set(), 'failed': set(), 'cancelled': set(),
}


class Invalid(ValueError):
    pass


def load_json(path):
    def pairs(items):
        data = {}
        for key, value in items:
            if key in data:
                raise Invalid('JSON con clave duplicada')
            data[key] = value
        return data
    try:
        return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(Invalid('JSON no finito')))
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        raise Invalid(f'JSON ilegible/inválido: {path.name} ({type(exc).__name__})') from exc


def validate_shape(value, rule, schema, label='run'):
    if '$ref' in rule:
        rule = schema['$defs'][rule['$ref'].removeprefix('#/$defs/')]
    if 'oneOf' in rule:
        matched = 0
        for branch in rule['oneOf']:
            try:
                validate_shape(value, branch, schema, label)
                matched += 1
            except Invalid:
                pass
        if matched != 1:
            raise Invalid(f'{label}: versión/contrato ambiguo o campos incompatibles')
    if 'not' in rule:
        try:
            validate_shape(value, rule['not'], schema, label)
        except Invalid:
            pass
        else:
            raise Invalid(f'{label}: campos prohibidos para esta versión')
    kind = rule.get('type')
    allowed = kind if isinstance(kind, list) else [kind] if kind else []
    types = {'object': lambda x: isinstance(x, dict), 'array': lambda x: isinstance(x, list),
             'string': lambda x: isinstance(x, str), 'integer': lambda x: type(x) is int,
             'boolean': lambda x: type(x) is bool, 'null': lambda x: x is None}
    if allowed and not any(types[t](value) for t in allowed):
        raise Invalid(f'{label}: tipo inválido')
    if 'const' in rule and (type(value) is not type(rule['const']) or value != rule['const']):
        raise Invalid(f'{label}: valor constante requerido')
    if 'enum' in rule and value not in rule['enum']:
        raise Invalid(f'{label}: enum desconocido')
    if value is None:
        return
    if isinstance(value, dict):
        props = rule.get('properties', {})
        if set(rule.get('required', [])) - value.keys():
            raise Invalid(f'{label}: faltan campos obligatorios')
        if rule.get('additionalProperties') is False and value.keys() - props.keys():
            raise Invalid(f'{label}: campos desconocidos')
        for key, item in value.items():
            if key in props:
                validate_shape(item, props[key], schema, f'{label}.{key}')
    elif isinstance(value, list):
        if len(value) < rule.get('minItems', 0) or len(value) > rule.get('maxItems', len(value)):
            raise Invalid(f'{label}: cantidad de elementos inválida')
        for item in value:
            validate_shape(item, rule['items'], schema, label + '[]')
    elif isinstance(value, str):
        if len(value.strip()) < rule.get('minLength', 0):
            raise Invalid(f'{label}: texto vacío')
        if 'pattern' in rule and not re.fullmatch(rule['pattern'], value):
            raise Invalid(f'{label}: formato inválido')
    elif type(value) is int:
        if value < rule.get('minimum', value) or value > rule.get('maximum', value):
            raise Invalid(f'{label}: fuera de límite')


def fields(path):
    """Operational single-line fields only; duplicate keys fail closed."""
    try:
        result = {}
        for line in path.read_text(encoding='utf-8').splitlines():
            line = re.sub(r'^\s*(?:[-*]\s+|#{1,6}\s+)', '', line).replace('**', '').strip()
            match = re.match(r'^([A-Za-z][A-Za-z /-]*):\s*(.*)$', line)
            if match:
                key, value = match[1].lower(), match[2].strip('` ')
                if key in result and result[key] != value:
                    # AI Strategy repeats profile names, not execution fields.
                    if key in {'current attempt', 'dependency refs', 'delegation policy',
                               'delegation authorization', 'status', 'slice id', 'plan version'}:
                        raise Invalid(f'{path.name}: campo operativo contradictorio')
                result[key] = value
        return result
    except (OSError, UnicodeError) as exc:
        raise Invalid(f'{path.name}: Markdown ilegible') from exc


def instant(value):
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if dt.tzinfo is None:
            raise ValueError('timezone missing')
        return dt
    except (ValueError, TypeError) as exc:
        raise Invalid('timestamp inválido; usar ISO-8601 con zona horaria') from exc


def base_digest(refs):
    return hashlib.sha256(json.dumps(refs, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


class ExecutionCheck:
    def __init__(self, project, now=None):
        self.project = Path(project).resolve()
        self.schema = load_json(SCHEMA)
        self.now = now or datetime.now(timezone.utc)
        self.errors = []
        self.warnings = []
        self.records = []

    def path(self, relative, exists=True):
        if not isinstance(relative, str) or not relative or '\\' in relative:
            raise Invalid('referencia inválida')
        p = Path(relative)
        if p.is_absolute() or '..' in p.parts or p.as_posix() != relative:
            raise Invalid('referencia no canónica o fuera del proyecto')
        if any(x == '.git' or x == '.env' or x.startswith('.env.') for x in p.parts):
            raise Invalid('referencia a datos privados excluidos del contexto')
        if p.as_posix() in {'.codex/auth.json', '.codex/credentials.json'}:
            raise Invalid('referencia a credenciales excluida del contexto')
        current = self.project
        for component in p.parts:
            current = current / component
            if current.is_symlink():
                raise Invalid('symlink no permitido en referencias de ejecución')
        if not current.resolve().is_relative_to(self.project):
            raise Invalid('referencia externa')
        if exists and not current.is_file():
            raise Invalid('referencia de archivo inexistente/no regular: ' + relative)
        if exists and current.stat().st_nlink != 1:
            raise Invalid('hardlink no permitido en referencias de ejecución')
        return current

    def artifact(self, ref, live=True):
        p = self.path(ref['path'])
        try:
            actual = hashlib.sha256(p.read_bytes()).hexdigest()
        except OSError as exc:
            raise Invalid('evidencia ilegible') from exc
        if actual != ref['sha256']:
            if live:
                raise Invalid('digest obsoleto/conflictivo: ' + ref['path'])
            self.warnings.append('Snapshot histórico cambió: ' + ref['path'])
        return p

    def dependency_graph(self, start):
        graph, todo = {}, [start]
        while todo:
            node = todo.pop()
            if node in graph:
                continue
            spec = fields(self.path(node))
            try:
                deps = json.loads(spec.get('dependency refs', '[]'))
            except ValueError as exc:
                raise Invalid('Dependency refs debe ser array JSON') from exc
            if not isinstance(deps, list) or any(not isinstance(d, str) for d in deps):
                raise Invalid('Dependency refs debe contener paths de SPEC')
            for dep in deps:
                if self.path(dep).name != 'SPEC.md':
                    raise Invalid('dependencia debe apuntar a SPEC.md')
            if len(set(deps)) != len(deps):
                raise Invalid('dependencia duplicada')
            graph[node] = deps
            todo.extend(deps)
        # Iterative topological removal avoids recursion on large/cyclic graphs.
        pending = {k: set(v) for k, v in graph.items()}
        while pending:
            ready = {k for k, v in pending.items() if not v}
            if not ready:
                raise Invalid('ciclo de dependencias')
            pending = {k: v - ready for k, v in pending.items() if k not in ready}
        return graph[start]

    def record(self, file):
        run = load_json(file)
        validate_shape(run, self.schema, self.schema)
        if file.stem != run['attempt_id']:
            raise Invalid('attempt_id no coincide con nombre del archivo')
        req = self.path(run['requirement_ref'])
        if req.name != 'STATE.md' or not file.is_relative_to(req.parent / 'slices'):
            raise Invalid('requirement_ref no corresponde a la slice')
        spec_path = file.parent.parent / 'SPEC.md'
        spec_rel = spec_path.relative_to(self.project).as_posix()
        spec = fields(self.path(spec_rel))
        if spec.get('slice id') != run['slice_id']:
            raise Invalid('Slice ID no coincide')
        if file.parent.name != 'runs':
            raise Invalid('run fuera de runs/')
        state = fields(req)
        policies = {1: 'supervised-sequential-v1', 2: 'supervised-audited-v1',
                    3: 'text-helper-v1'}
        policy = policies[run['schema_version']]
        if state.get('delegation policy') != policy or state.get('delegation authorization') != 'approved':
            raise Invalid('opt-in/autorización de delegación ausentes; mantener inline')
        if run['schema_version'] == 3:
            if 'runtime' in run or 'supervision' in run:
                raise Invalid('RUN v3 API no puede fingir runtime de thread/supervisión de copia')
        elif 'api_runtime' in run:
            raise Invalid('RUN v1/v2 no admite runtime API')
        live = run['status'] not in TERMINAL
        if live and (spec.get('status') != 'active' or state.get('status') == 'completed'):
            raise Invalid('intento vigente requiere slice activa y requirement no completado')
        if live and state.get('plan version') != run['plan_version']:
            raise Invalid('versión de plan no vigente')
        runtime = run['api_runtime'] if run['schema_version'] == 3 else run['runtime']
        for ref in [run['authorization_ref'], runtime['capability_ref'],
                    *run['criteria_refs']]:
            self.artifact(ref)
        for ref in [run['brief_ref'], *run['base_refs'], *run['context_refs'], *run['instruction_refs']]:
            self.artifact(ref, live=live)
        brief = self.path(run['brief_ref']['path'])
        if brief != file.parent.parent / 'EXECUTION_BRIEF.md':
            raise Invalid('brief_ref no pertenece a la slice')
        for scope in ('read_scope', 'proposal_scope'):
            for path in run[scope]:
                self.path(path, exists=(scope == 'read_scope'))
        read_set = set(run['read_scope'])
        if any(ref['path'] not in read_set for ref in run['base_refs'] + run['context_refs'] + run['instruction_refs']):
            raise Invalid('manifest fuera de read_scope')
        expected_deps = self.dependency_graph(spec_rel)
        if sorted(expected_deps) != sorted(d['slice_ref'] for d in run['dependencies']):
            raise Invalid('dependencias del run y SPEC discrepan')
        for dep in run['dependencies']:
            completed = fields(self.path(dep['slice_ref'])).get('status') == 'completed'
            if dep['evidence_ref'] is None:
                raise Invalid('dependencia sin aceptación documentada')
            self.artifact(dep['evidence_ref'])
            if not completed:
                if not dep['criteria'] or dep['partial_approval_ref'] is None:
                    raise Invalid('dependencia pendiente; entrega parcial no habilita slice')
                self.artifact(dep['partial_approval_ref'])
        history = run['history']
        if history[0]['status'] != 'prepared' or history[-1]['status'] != run['status']:
            raise Invalid('historial sin prepared inicial o estado final discordante')
        for i, event in enumerate(history):
            when = instant(event['at'])
            if i and (event['status'] not in TRANSITIONS[history[i-1]['status']] or when < instant(history[i-1]['at'])):
                raise Invalid('transición inválida, reapertura terminal o tiempo invertido')
            if i and event['evidence_ref'] is None:
                raise Invalid('transición sin evidencia')
            if event['evidence_ref']:
                self.artifact(event['evidence_ref'])
        observed = instant(runtime['observed_at'])
        if observed < instant(history[-1]['at']):
            raise Invalid('observación anterior al último estado')
        if instant(run['review_at']) < self.now and live:
            self.warnings.append('Checkpoint vencido: comprobar runtime; no asumir detención ni reintentar.')
        if runtime['observation'] == 'unknown':
            self.warnings.append('NO VERIFICADO: ejecución desconocida; reconciliar antes de despachar/reasignar.')
        launched = any(e['status'] == 'running' for e in history)
        if run['schema_version'] == 3:
            needs_id = (run['status'] in {'submitted', 'accepted'}
                        or ((launched or run['status'] == 'running')
                            and runtime['observation'] != 'unknown'))
            if needs_id and not runtime['response_id']:
                raise Invalid('request API iniciado sin response_id correlacionable')
            if runtime['terminal_observed']:
                if runtime['observation'] != 'known' or runtime['terminal_evidence_ref'] is None:
                    raise Invalid('terminal API declarado sin observación/evidencia')
                self.artifact(runtime['terminal_evidence_ref'])
            if run['status'] in {'submitted', 'accepted'} and not runtime['terminal_observed']:
                raise Invalid('entrega API sin estado terminal observado')
            if run['status'] == 'cancelled' and runtime['observation'] == 'unknown':
                raise Invalid('cancelación API con resultado remoto desconocido')
        else:
            if (launched or run['status'] in {'running', 'submitted', 'accepted'}) and not runtime['thread_id']:
                raise Invalid('ejecución sin ID del runtime')
            if runtime['stop_confirmed']:
                if runtime['observation'] != 'known' or runtime['stop_evidence_ref'] is None:
                    raise Invalid('detención declarada sin observación/evidencia')
                self.artifact(runtime['stop_evidence_ref'])
            if run['status'] in {'submitted', 'accepted', 'cancelled'} and (launched or runtime['thread_id'] or run['status'] != 'cancelled') and not runtime['stop_confirmed']:
                raise Invalid('entrega/cancelación sin detención confirmada')
            if run['status'] == 'cancelled' and runtime['observation'] == 'unknown':
                raise Invalid('cancelación con despacho desconocido')
        if run['observed_config'] is not None:
            if run['model_evidence_ref'] is None:
                raise Invalid('modelo observado sin evidencia')
            self.artifact(run['model_evidence_ref'])
        else:
            self.warnings.append('Modelo efectivo: unknown; no inferirlo de requested_profile.')
        if run['delivery_ref'] is not None:
            delivery = load_json(self.artifact(run['delivery_ref']))
            validate_shape(delivery, self.schema['$defs']['delivery'], self.schema, 'delivery')
            if delivery['attempt_id'] != run['attempt_id'] or delivery['base_digest'] != base_digest(run['base_refs']):
                raise Invalid('entrega de intento/base diferentes')
            if not set(delivery['proposed_files']) <= set(run['proposal_scope']):
                raise Invalid('propuesta fuera de scope')
            for command in delivery['commands']:
                if command['result'] != 'not-run' and command['evidence_ref'] is None:
                    raise Invalid('comando sin evidencia; usar not-run')
                if command['evidence_ref']:
                    self.artifact(command['evidence_ref'])
        elif run['status'] in {'submitted', 'accepted'}:
            raise Invalid('DONE sin entrega verificable')
        for ref in run['validation_refs']:
            self.artifact(ref)
        for key in ('integration_ref', 'acceptance_ref', 'handoff_ref'):
            if run[key] is not None:
                self.artifact(run[key])
        if run['status'] == 'accepted' and (not run['validation_refs'] or not run['integration_ref'] or not run['acceptance_ref']):
            raise Invalid('aceptación sin validación/integración/evidencia central')
        if run['schema_version'] == 2:
            self.supervision(run)
        self.records.append((file, run))

    def supervision(self, run):
        """Validate supplied observations only. Never probes runtime or manifest paths."""
        sup = run['supervision']
        for key in ('risk_acceptance_ref', 'context_review_ref'):
            self.artifact(sup[key])
        incident = False
        for name, control in sup['controls'].items():
            mechanism, observed = control['mechanism'], control['observed']
            if control['evidence_ref'] is not None:
                self.artifact(control['evidence_ref'])
            if observed != 'unknown' and control['evidence_ref'] is None:
                raise Invalid('control observado sin evidencia: ' + name)
            if name == 'no_copy_writes':
                if mechanism != 'instruction':
                    raise Invalid('v2 no_copy_writes es instrucción supervisada, no enforcement')
            elif mechanism == 'instruction' or (observed == 'satisfied' and mechanism != 'runtime'):
                raise Invalid('control obligatorio no sustituible por instrucciones: ' + name)
            if observed == 'unknown' or mechanism == 'unknown':
                self.warnings.append('NO APTO PARA PILOTO: control no verificado: ' + name)
            incident |= observed == 'violated'
        complete = run['status'] in {'submitted', 'accepted'} or run['runtime']['stop_confirmed']
        copy_result = None
        try:
            for label in ('copy', 'original'):
                before = load_document(self.artifact(sup[label + '_before_ref']))
                initial = validate_manifest(before)
                if before['scope_id'] != run['attempt_id'] + ':' + label:
                    raise Invalid('manifest no pertenece al intento/alcance ' + label)
                required_refs = run['base_refs'] + run['context_refs'] + run['instruction_refs']
                if any(ref['path'] not in initial or initial[ref['path']]['sha256'] != ref['sha256'] for ref in required_refs):
                    raise Invalid('manifest inicial no cubre base/contexto/instrucciones: ' + label)
                if label == 'copy' and {p for p, entry in initial.items() if entry['kind'] == 'file'} != set(run['read_scope']):
                    raise Invalid('manifest de copia no coincide con read_scope')
                after_ref, report_ref = sup[label + '_after_ref'], sup[label + '_audit_ref']
                if (after_ref is None) != (report_ref is None):
                    raise Invalid('auditoría incompleta: ' + label)
                if after_ref is None:
                    if complete:
                        if run['status'] not in {'failed', 'cancelled'} or not sup['incident_refs']:
                            raise Invalid('fin/entrega sin auditoría final: ' + label)
                        incident = True
                        self.warnings.append('INCIDENTE: auditoría incompleta documentada; copia en cuarentena: ' + label)
                    self.warnings.append('Auditoría final pendiente: ' + label)
                    continue
                expected = compare(before, load_document(self.artifact(after_ref)))
                actual = load_document(self.artifact(report_ref))
                # Canonical JSON comparison also rejects bool/int coercion in reports.
                if json.dumps(actual, sort_keys=True) != json.dumps(expected, sort_keys=True):
                    raise Invalid('informe de auditoría discrepa de manifests: ' + label)
                changed = expected['result'] == 'changed'
                incident |= changed
                if label == 'copy':
                    copy_result = expected['result']
                if changed:
                    self.warnings.append('INCIDENTE: diferencias en ' + label + '; preservar evidencia, no restaurar original.')
        except AuditError as exc:
            raise Invalid('auditoría inválida: ' + str(exc)) from exc
        claim = sup['controls']['no_copy_writes']['observed']
        if claim == 'satisfied' and copy_result != 'clean':
            raise Invalid('sin escritura observada requiere comparación final limpia')
        for ref in sup['incident_refs']:
            self.artifact(ref)
        incident |= bool(sup['incident_refs'])
        if incident:
            if not sup['incident_refs']:
                raise Invalid('incidente sin evidencia de reconciliación')
            if run['status'] in {'submitted', 'accepted'}:
                raise Invalid('entrega rechazada por incidente; preservar copia y original')
            self.warnings.append('INCIDENTE documentado: entrega rechazada; copia no reutilizable, no rollback automático.')
        self.warnings.append('V2 supervisada: snapshots no prueban ausencia de cambios transitorios/externos ni permisos efectivos.')

    def scan(self):
        # Explicit levels: reject symlinks before descending, never recurse outside project.
        def children(directory):
            if directory.is_symlink():
                raise Invalid('symlink en estructura de requirements')
            return sorted(directory.iterdir()) if directory.is_dir() else []
        try:
            docs = self.project / 'docs'
            if docs.is_symlink():
                self.warnings.append('NO VERIFICADO: docs es symlink; no inspeccionar fuera del proyecto.')
                return self
            for req in children(docs / 'requirements'):
                if req.is_symlink():
                    self.warnings.append('NO VERIFICADO: requirement symlink no inspeccionado.')
                    continue
                for slice_dir in children(req / 'slices'):
                    if slice_dir.is_symlink():
                        raise Invalid('slice symlink no inspeccionada')
                    for file in children(slice_dir / 'runs'):
                        if file.suffix != '.json':
                            continue
                        try:
                            self.path(file.relative_to(self.project).as_posix())
                            self.record(file)
                        except Invalid as exc:
                            self.errors.append(f'{file.name}: {exc}')
                    brief = slice_dir / 'EXECUTION_BRIEF.md'
                    if brief.is_file() and not brief.is_symlink():
                        pointer = fields(brief).get('current attempt', '')
                        if pointer and pointer != 'none':
                            target = self.path(pointer)
                            if target.parent != slice_dir / 'runs' or target.suffix != '.json':
                                raise Invalid('Current attempt apunta fuera de runs/ de la slice')
            self.groups()
        except (Invalid, OSError) as exc:
            self.errors.append(str(exc))
        return self

    def groups(self):
        groups, ids, threads, occupied = {}, set(), set(), []
        for file, run in self.records:
            if run['attempt_id'] in ids:
                self.errors.append('attempt_id duplicado')
            ids.add(run['attempt_id'])
            runtime = run['api_runtime'] if run['schema_version'] == 3 else run['runtime']
            runtime_id = runtime['response_id'] if run['schema_version'] == 3 else runtime['thread_id']
            if runtime_id and runtime_id in threads:
                self.errors.append(('response_id' if run['schema_version'] == 3 else 'thread_id') +
                                   ' reutilizado entre intentos')
            if runtime_id:
                threads.add(runtime_id)
            groups.setdefault((run['requirement_ref'], run['slice_id']), []).append((file, run))
            terminal = (runtime['terminal_observed'] if run['schema_version'] == 3
                        else runtime['stop_confirmed'])
            if run['status'] not in TERMINAL or (not terminal and runtime_id) or runtime['observation'] == 'unknown':
                occupied.append(run)
        if len(occupied) > 1:
            self.errors.append('más de un encargo no reconciliado; no despachar')
        for items in groups.values():
            items.sort(key=lambda x: x[1]['attempt_number'])
            runs = [r for _, r in items]
            budget = runs[0]['max_attempts']
            if [r['attempt_number'] for r in runs] != list(range(1, len(runs)+1)) or len(runs) > budget:
                self.errors.append('presupuesto/secuencia de intentos inválido; no resetear IDs')
            if len({r['assignment_id'] for r in runs}) != 1 or len({r['plan_version'] for r in runs}) != 1 or len({r['schema_version'] for r in runs}) != 1:
                self.errors.append('encargo/plan cambió para resetear presupuesto; requiere reconciliación explícita')
            for previous, current in zip(runs, runs[1:]):
                previous_runtime = (previous['api_runtime'] if previous['schema_version'] == 3
                                    else previous['runtime'])
                previous_id = (previous_runtime['response_id'] if previous['schema_version'] == 3
                               else previous_runtime['thread_id'])
                previous_terminal = (previous_runtime['terminal_observed'] if previous['schema_version'] == 3
                                     else previous_runtime['stop_confirmed'])
                if previous['status'] not in {'failed', 'cancelled'} or previous_runtime['observation'] != 'known' or (previous_id and not previous_terminal):
                    self.errors.append('reintento sin cierre/detención del anterior')
                if previous['coordinator_id'] != current['coordinator_id'] and current['handoff_ref'] is None:
                    self.errors.append('nuevo coordinador sin handoff reconciliado')
                if instant(current['history'][0]['at']) < instant(previous['history'][-1]['at']):
                    self.errors.append('reintento preparado antes de terminar el anterior')
            file, latest = items[-1]
            pointer = fields(self.path(latest['brief_ref']['path'])).get('current attempt')
            if pointer != file.relative_to(self.project).as_posix():
                self.errors.append('Current attempt no apunta al intento vigente')

    def report(self):
        for error in self.errors:
            print('ERROR: ' + error)
        for warning in sorted(set(self.warnings)):
            print('WARN: ' + warning)
        print(f'Delegation records: {len(self.records)}; ' + ('INVALID' if self.errors else 'STATIC PASS'))
        print('Runtime/API remota, permisos, tests reales y modelo efectivo: NO VERIFICADOS. '
              'No es autorización de dispatch. Reconciliar evidencia antes de ejecutar.')
        return int(bool(self.errors))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    args = parser.parse_args()
    if not args.project.is_dir():
        parser.error('directorio de proyecto inexistente')
    try:
        return ExecutionCheck(args.project).scan().report()
    except (Invalid, OSError) as exc:
        print('ERROR: ' + str(exc))
        return 1


if __name__ == '__main__':
    sys.exit(main())
