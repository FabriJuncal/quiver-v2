"""Read-only static guardrail checks. Never infers a live Codex session/model."""
import argparse
import re
import subprocess
import sys
import tomllib
from pathlib import Path

LIMITATIONS = {'none', 'context-limit', 'tool-failure', 'permission', 'unavailable-model',
               'unavailable-runtime-capability', 'other'}
EMPTY = {'', 'none', 'n/a', '-', 'ninguna', 'ninguno', 'sin pendientes', 'no pending work'}
FINISHED = {'completed', 'closed', 'cancelled', 'canceled', 'archived'}
STATE_FIELDS = {'status', 'current slice', 'pending slices', 'next action', 'why this is next',
                'expected output', 'after this', 'resume instruction', 'user action required',
                'blocked by', 'decision required', 'runtime limitation', 'runtime limitation detail',
                'active requirement', 'factory version'}
MAPPINGS = {
    'economical': ('gpt-5.6-luna', 'low'),
    'balanced': ('gpt-5.6-terra', 'medium'),
    'advanced': ('gpt-5.6-sol', 'high'),
    'exceptional': ('gpt-6-astra', 'high'),
}

# Distribution versions support stable releases and numeric release candidates.
# A stable version sorts AFTER every RC of the same base; rc.10 > rc.2.
VERSION = r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-rc\.(0|[1-9]\d*))?'


def version_key(value):
    match = re.fullmatch(VERSION, value)
    if not match:
        raise ValueError('Unsupported Factory version: ' + value)
    major, minor, patch, rc = match.groups()
    return (int(major), int(minor), int(patch), rc is None, int(rc or 0))


class Doctor:
    def __init__(self):
        self.errors = 0

    def warn(self, message):
        print('WARN: ' + message)

    def error(self, message):
        self.errors += 1
        print('ERROR: ' + message)

    def read(self, path):
        try:
            return path.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as error:
            self.error(f'No se puede leer {path}: {type(error).__name__}; revisá acceso/formato.')
            return ''

    def fields(self, path):
        # Support Factory bullets, plain fields and heading/value state formats.
        text = self.read(path)
        fields = {}
        lines = text.splitlines()
        for index, line in enumerate(lines):
            line = re.sub(r'^\s*(?:[-*]\s+|#{1,6}\s+)', '', line).replace('**', '').strip()
            match = re.match(r'^([A-Za-z][A-Za-z /-]*):\s*(.*)$', line)
            if match:
                key, value = match.groups()
                if not value and index + 1 < len(lines):
                    following = lines[index + 1].strip()
                    if following and not re.match(r'[-*#]|[A-Za-z][A-Za-z /-]*:', following):
                        value = following
                key = key.lower()
                if key in STATE_FIELDS and key in fields and fields[key] != value:
                    self.error(f'{path}: campo duplicado contradictorio: {key}. Reconciliá STATE.')
                fields[key] = value.strip('` ')
        return fields

    def config(self, path):
        if not path.exists():
            return {}
        try:
            return tomllib.loads(path.read_text(encoding='utf-8'))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError):
            self.error(f'TOML inválido o ilegible: {path}; corregilo y repetí doctor.')
            return {}

    def state(self, path, slice_active=False):
        fields = self.fields(path)
        status = fields.get('status', '').lower()
        active = status not in FINISHED
        has_slice = fields.get('current slice', '').lower() not in EMPTY or slice_active
        pending = fields.get('pending slices', '').lower() not in EMPTY
        if status in FINISHED and (has_slice or pending):
            self.error(f'{path}: INVARIANT 3: completado con slice activa/pendiente. Reconciliá evidencia y STATE.')
        if active or has_slice or pending:
            for key in ('next action', 'why this is next', 'expected output', 'after this', 'resume instruction'):
                if fields.get(key, '').lower() in EMPTY:
                    label = 'PROJECT_STATE' if path.name == 'PROJECT_STATE.md' else str(path)
                    self.error(f'{label} sin {key.capitalize()} concreto; trabajo activo exige Next action (INVARIANT 1/3).')
            user = fields.get('user action required', '').lower()
            if user not in {'true', 'false'}:
                self.error(f'{path}: User action required debe ser true o false, sin placeholder.')
            for key in ('blocked by', 'decision required'):
                if key not in fields:
                    self.warn(f'{path}: falta {key}; completar sin inferir aprobación.')
            if user == 'false' and fields.get('decision required', 'none').lower() not in EMPTY:
                self.error(f'{path}: decisión pendiente con usuario false; reconciliá autorización.')
            limitation = fields.get('runtime limitation')
            if limitation is None:
                self.warn(f'{path}: falta Runtime limitation; seguir guía de upgrade, sin cambios automáticos.')
            elif limitation not in LIMITATIONS:
                self.error(f'{path}: Runtime limitation inválida: usar enum del contrato.')
            elif limitation != 'none' and fields.get('runtime limitation detail', '').lower() in EMPTY:
                self.error(f'{path}: Runtime limitation sin causa/evidencia y pendiente.')
            if user == 'false' and fields.get('next action', '').lower() not in EMPTY:
                print(f'CONTINUAR: {path}: Next action presente; Finalization Gate exige ejecución si es viable.')
        return fields

    def project(self, project, version):
        metadata = project / 'PROJECT_PROFILE.md'
        agents = project / 'AGENTS.md'
        versions = {}
        for label, path in (('Project', metadata), ('AGENTS', agents)):
            value = self.fields(path).get('factory version', '') if path.exists() else ''
            token = value.split()[0] if value.split() else ''
            versions[label] = token if re.fullmatch(VERSION, token) else 'unknown'
        print(f'Installed factory: {version}\nProject factory layer: {versions["Project"]}\nAGENTS version: {versions["AGENTS"]}')
        old = [v for v in versions.values() if v != 'unknown' and version_key(v) < version_key(version)]
        if old:
            self.warn(f'PROJECT FACTORY LAYER OUTDATED\nInstalled: {version}\nProject: {versions["Project"]}\nAGENTS: {versions["AGENTS"]}')
        elif 'unknown' in versions.values():
            self.warn('PROJECT FACTORY LAYER UNKNOWN: falta metadata o integración de AGENTS; no declarar actualizado.')
        elif any(v != version for v in versions.values()):
            self.warn('Versiones diferentes: no hacer downgrade. Verificá la instalación canónica requerida por el proyecto.')
        if old or 'unknown' in versions.values():
            print('QUÉ HACER\nEjecutá en Codex:\n'
                  f'Actualizá únicamente la capa AI Software Factory de este proyecto a v{version} siguiendo '
                  'docs/guides/UPGRADE_2_2_2_TO_2_3_0.md de la instalación canónica. '
                  'Preservá código, decisiones, criterios, arquitectura y slices cerradas. '
                  'Validá con doctor.sh --project . y continuá el trabajo ya autorizado.\n'
                  'ACCIÓN DEL USUARIO: requerida')
        state = project / 'PROJECT_STATE.md'
        if not state.is_file():
            self.error(f'{state} no encontrado; completar estado antes de reanudar.')
            return
        project_fields = self.state(state)
        active_ref = project_fields.get('active requirement', '')
        selected = None
        if active_ref.lower() not in EMPTY:
            selected = (project / active_ref).resolve()
            if not selected.is_relative_to(project):
                self.error('Active requirement sale del proyecto; corregí la referencia sin leer archivos externos.')
                selected = None
            elif not selected.is_file():
                self.error('Active requirement debe apuntar a un STATE.md existente relativo al proyecto.')
        requirement_root = project / 'docs/requirements'
        candidates = set(requirement_root.glob('*/STATE.md')) if requirement_root.is_dir() else set()
        if selected and selected.is_file():
            candidates.add(selected)
        for req in sorted(candidates):
            if req.is_symlink() or not req.resolve().is_relative_to(project):
                self.warn(f'STATE externo/symlink no inspeccionado: {req}')
                continue
            fields = self.fields(req)
            slices = []
            slice_files = {p for name in ('SPEC.md', 'STATE.md', 'EXECUTION_BRIEF.md')
                           for p in req.parent.glob('slices/**/' + name)}
            for spec in sorted(slice_files):
                if spec.is_symlink() or not spec.resolve().is_relative_to(project):
                    continue
                if self.fields(spec).get('status', '').lower() in {'active', 'in-progress'}:
                    slices.append(spec)
            if fields.get('status', '').lower() in FINISHED and not slices:
                if selected and req.resolve() == selected:
                    self.error('Active requirement apunta a un requirement cerrado; reconciliá PROJECT_STATE con evidencia.')
                # Completed records with stale Current/Pending slice still violate invariant 3.
                if fields.get('current slice', '').lower() in EMPTY and fields.get('pending slices', '').lower() in EMPTY:
                    continue
            checked = self.state(req, slice_active=bool(slices))
            if selected and req.resolve() == selected:
                if project_fields.get('current slice', 'none') != checked.get('current slice', 'none'):
                    self.error('PROJECT_STATE y requirement discrepan en Current slice; reconciliá con evidencia, STATE tiene prioridad.')
            print(f'Requirement: {req.parent.name}; active slice: {checked.get("current slice", "unknown")}')

    def instructions(self, codex_home, project):
        global_agents = codex_home / 'AGENTS.md'
        print(f'Global AGENTS size: {global_agents.stat().st_size if global_agents.is_file() else 0} bytes')
        base = self.config(codex_home / 'config.toml')
        if 'profiles' in base or 'profile' in base:
            self.warn('Perfiles legacy en config.toml: Codex >= 0.134.0 usa archivos separados; migrá según CODEX_MODEL_PROFILES.md.')
        configs = [base]
        for profile, expected in MAPPINGS.items():
            path = codex_home / f'asf-{profile}.config.toml'
            if path.is_file():
                data = self.config(path)
                if (data.get('model'), data.get('model_reasoning_effort')) != expected:
                    self.warn(f'{path.name}: perfil personalizado/conflictivo; preservado. Usá asf {profile} o revisá el archivo con backup.')
                configs.append(data)
            else:
                self.warn(f'{path.name} no instalado (opcional); configure-model-profiles.sh o asf {profile}.')
        selected = []
        for name in ('AGENTS.override.md', 'AGENTS.md'):
            path = codex_home / name
            if path.is_file() and path.stat().st_size:
                selected.append(path)
                break
        directories = []
        if project:
            root = project
            try:
                run = subprocess.run(['git', '-C', str(project), 'rev-parse', '--show-toplevel'],
                                     capture_output=True, text=True, timeout=5)
                if run.returncode == 0:
                    root = Path(run.stdout.strip()).resolve()
            except (OSError, subprocess.TimeoutExpired):
                self.warn('Git root NO VERIFICADO; estimación usa directorio del proyecto.')
            if root in (project, *project.parents):
                directories = list(reversed([project, *list(project.parents)[:list(project.parents).index(root)]])) if root != project else [project]
                if root != project:
                    directories.insert(0, root)
            for directory in directories:
                config_path = directory / '.codex/config.toml'
                data = self.config(config_path)
                configs.append(data)
                if any(k in data for k in ('model', 'model_reasoning_effort', 'plan_mode_reasoning_effort')):
                    self.warn(f'{config_path}: modelo/reasoning del proyecto prevalece sobre --profile si es confiable. '
                              'Usá asf balanced; si la fase depende materialmente, /status y pegá resultado si difiere.')
            # Conservative union: profile/trust/CLI unknown. Never claim exact live instruction set.
            fallbacks = []
            for config in configs:
                names = config.get('project_doc_fallback_filenames', [])
                if not isinstance(names, list) or any(not isinstance(n, str) for n in names):
                    self.error('project_doc_fallback_filenames debe ser una lista de nombres de archivo.')
                    continue
                for name in names:
                    if isinstance(name, str) and Path(name).name == name and name not in fallbacks:
                        fallbacks.append(name)
            for directory in directories:
                for name in ['AGENTS.override.md', 'AGENTS.md', *fallbacks]:
                    path = directory / name
                    if path.is_file() and path.stat().st_size:
                        selected.append(path)
                        break
            path = project / 'AGENTS.md'
            print(f'Project AGENTS size: {path.stat().st_size if path.is_file() else 0} bytes')
        limits = [c['project_doc_max_bytes'] for c in configs if 'project_doc_max_bytes' in c]
        valid = [n for n in limits if isinstance(n, int) and not isinstance(n, bool) and n >= 0]
        if len(valid) != len(limits):
            self.error('project_doc_max_bytes inválido: se requiere entero no negativo.')
        limit = min(valid) if valid else 32768
        total = sum(p.stat().st_size for p in selected) + max(0, len(selected) - 1) * 2
        print(f'AGENTS combined estimate: {total} bytes; reference limit: {limit} bytes '
              '(32 KiB default oficial; selección efectiva/CLI/trust NO VERIFICADOS).')
        for path in selected:
            print(f'Instruction candidate: {path} ({path.stat().st_size} bytes)')
        if total >= limit * 0.8:
            self.warn('Las instrucciones AGENTS están cerca del límite o lo superan.\n'
                      'Impacto posible: reglas de Factory podrían truncarse.\n'
                      'Próxima acción: reducir AGENTS global y mover detalle a docs/skills.\n'
                      'Estimación, no prueba de truncamiento efectivo; confirmar project_doc_max_bytes y fuentes cargadas.')
        # Only an explicitly configured cap exceeded by the project chain in every observed
        # configuration yields an error. Default-only or uncertain global inclusion stays WARN.
        project_bytes = sum(p.stat().st_size for p in selected if p.parent != codex_home)
        base_limit = base.get('project_doc_max_bytes', 32768)
        possible_limits = valid + ([base_limit] if isinstance(base_limit, int) and not isinstance(base_limit, bool) and base_limit >= 0 else [32768])
        if valid and len(valid) == len(limits) and project_bytes > max(possible_limits):
            self.error('AGENTS del proyecto supera todos los límites explícitos observados (condición estática verificada). '
                       'Reducí instrucciones o revisá project_doc_max_bytes; overrides CLI no observables.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--codex-home', type=Path, required=True)
    parser.add_argument('--project', type=Path)
    parser.add_argument('--variant-manifest', type=Path)
    args = parser.parse_args()
    doctor = Doctor()
    version = doctor.fields(args.root / 'FACTORY_VERSION.md').get('version', '')
    if not re.fullmatch(VERSION, version):
        doctor.error('Factory version inválida.')
        return 1
    project = args.project.resolve() if args.project else None
    if args.variant_manifest and not project:
        doctor.error('--variant-manifest requiere --project.')
    doctor.instructions(args.codex_home, project)
    if project:
        doctor.project(project, version)
        # doctor invokes Python -I; load only the packaged sibling, never project cwd.
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from check_execution import ExecutionCheck, Invalid
        try:
            execution = ExecutionCheck(project).scan()
            if execution.report():
                doctor.error('Delegación: reconciliá registros; no despachar ni aceptar hasta resolver errores.')
        except (Invalid, OSError) as error:
            doctor.error(f'Delegación NO VERIFICADA: {error}')
        if args.variant_manifest:
            try:
                from branch_discovery import DiscoveryError, validate_context_file
                manifest = validate_context_file(project, args.variant_manifest)
                print(f"Variant context PASS: {manifest['target_ref']}@{manifest['target_oid']}")
            except (DiscoveryError, OSError, ValueError) as error:
                doctor.error(f'Variant context inválido u obsoleto: {error}')
    print('Runtime guardrails: validación estática; continuidad real del agente requiere ejecución en sesión.')
    return int(bool(doctor.errors))


if __name__ == '__main__':
    sys.exit(main())
