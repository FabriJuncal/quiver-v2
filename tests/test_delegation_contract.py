"""Offline data/contract tests, not model obedience or runtime isolation evals."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import unittest

import test_scripts as lifecycle
from delegation_fixture import fixture_files, digest, REQ, SLICE, RUN

ROOT = lifecycle.ROOT
sys.path.insert(0, str(ROOT / 'scripts/lib'))
from check_execution import ExecutionCheck, Invalid, load_json, validate_shape


class DelegationContract(unittest.TestCase):
    setUp = lifecycle.Scripts.setUp
    put = lifecycle.Scripts.put
    run_script = lifecycle.Scripts.run_script

    def fixture(self, status='prepared', number=1):
        for name, body in fixture_files(status, number).items():
            self.put(self.project / name, body)
        return json.loads((self.project / SLICE / f'runs/attempt-{number}.json').read_text())

    def save(self, run):
        self.put(self.project / SLICE / 'runs' / (run['attempt_id'] + '.json'), json.dumps(run))

    def check(self, ok=True, contains=None):
        before = lifecycle.snapshot(self.project)
        result = ExecutionCheck(self.project, now=datetime(2026, 9, 20, tzinfo=timezone.utc)).scan()
        self.assertEqual(before, lifecycle.snapshot(self.project))
        if ok:
            self.assertEqual(result.errors, [], result.errors)
        else:
            self.assertTrue(result.errors, 'expected invalid record')
        if contains:
            self.assertIn(contains, '\n'.join(result.errors + result.warnings))
        return result

    def rewrite_artifact(self, run, key, data):
        path = run[key]['path']
        body = json.dumps(data)
        self.put(self.project / path, body)
        run[key]['sha256'] = digest(body)
        self.save(run)

    def test_v01_legacy_no_metadata_no_writes(self):
        self.assertEqual(self.check().records, [])

    def test_legacy_symlinked_docs_not_followed_or_required(self):
        outside = self.base / 'legacy-docs'
        outside.mkdir()
        (self.project / 'docs').symlink_to(outside, target_is_directory=True)
        self.check(contains='NO VERIFICADO')

    def test_declared_attempt_missing_and_retry_time(self):
        self.put(self.project / SLICE / 'EXECUTION_BRIEF.md', 'Current attempt: ' + RUN + '\n')
        self.check(False, 'inexistente')
        self.fixture('failed')
        run = self.fixture('prepared', 2)
        run['history'][0]['at'] = '2026-09-20T11:00:00Z'
        self.save(run)
        self.check(False, 'antes de terminar')

    def test_v03_empty_project_write_scope_required(self):
        run = self.fixture()
        run['project_write_scope'] = ['PROJECT_STATE.md']
        self.save(run)
        self.check(False, 'cantidad')

    def test_all_supported_record_states(self):
        for state in ('prepared', 'running', 'submitted', 'accepted', 'failed', 'cancelled'):
            with self.subTest(state=state):
                self.fixture(state)
                self.check()

    def test_v05_no_opt_in_or_authorization(self):
        self.fixture()
        for text in ('Status: active\n', 'Delegation policy: supervised-sequential-v1\nDelegation authorization: pending\n'):
            self.put(self.project / REQ / 'STATE.md', text)
            self.check(False, 'opt-in')

    def dependency(self, run, completed=False):
        spec = REQ + '/slices/S00/SPEC.md'
        self.put(self.project / spec, 'Slice ID: S00\nStatus: ' + ('completed' if completed else 'active') + '\nDependency refs: []\n')
        self.put(self.project / SLICE / 'SPEC.md', 'Slice ID: S01\nStatus: active\nDependency refs: ' + json.dumps([spec]) + '\n')
        run['dependencies'] = [{'slice_ref': spec, 'criteria': [],
            'evidence_ref': run['authorization_ref'], 'partial_approval_ref': None}]
        self.save(run)
        return spec

    def test_v06_dependency_not_freed_by_partial_attempt(self):
        run = self.fixture()
        spec = self.dependency(run)
        self.check(False, 'dependencia pendiente')
        run['dependencies'][0]['criteria'] = ['AC01']
        run['dependencies'][0]['partial_approval_ref'] = run['authorization_ref']
        self.save(run)
        self.check()
        self.put(self.project / spec, 'Status: completed\nDependency refs: []\n')
        self.check()

    def test_v07_dependency_cycle_and_missing_target(self):
        run = self.fixture()
        spec = self.dependency(run, completed=True)
        self.put(self.project / spec, 'Status: completed\nDependency refs: ' + json.dumps([SLICE + '/SPEC.md']) + '\n')
        self.check(False, 'ciclo')
        self.put(self.project / spec, 'Dependency refs: ["absent/SPEC.md"]\n')
        self.check(False, 'inexistente')

    def test_v07_external_paths_and_symlinks_rejected(self):
        run = self.fixture()
        original = run['base_refs'][0]['path']
        for name in ('../outside', '/etc/passwd', 'src//example.txt', 'src/../src/example.txt'):
            run['base_refs'][0]['path'] = name
            self.save(run)
            self.check(False, 'referencia')
        outside = self.base / 'private'
        self.put(outside, 'Do not read\n')
        (self.project / 'outside-link').symlink_to(outside)
        run['base_refs'][0]['path'] = 'outside-link'
        self.save(run)
        self.check(False, 'symlink')
        run['base_refs'][0]['path'] = original

    def test_v07_symlinked_run_directory_not_traversed(self):
        outside = self.base / 'external-runs'
        outside.mkdir()
        self.put(outside / 'private.json', 'not JSON; must never parse')
        parent = self.project / SLICE
        parent.mkdir(parents=True)
        (parent / 'runs').symlink_to(outside, target_is_directory=True)
        self.check(False, 'symlink')

    def test_v08_manifest_scope_and_digest(self):
        run = self.fixture()
        run['read_scope'] = ['src/example.txt']
        self.save(run)
        self.check(False, 'read_scope')
        self.fixture()
        self.put(self.project / 'src/example.txt', 'Changed base\n')
        self.check(False, 'digest obsoleto')

    def test_v09_obvious_secret_paths_excluded(self):
        run = self.fixture()
        self.put(self.project / '.env', 'SYNTHETIC=not-a-secret\n')
        run['base_refs'][0] = {'path': '.env', 'sha256': digest('SYNTHETIC=not-a-secret\n')}
        self.save(run)
        self.check(False, 'privados')

    def test_v10_done_without_delivery_and_stop(self):
        run = self.fixture('submitted')
        run['delivery_ref'] = None
        self.save(run)
        self.check(False, 'DONE')
        run = self.fixture('submitted')
        run['runtime']['stop_confirmed'] = False
        self.save(run)
        self.check(False, 'detención')

    def test_v11_acceptance_requires_coordinator_evidence(self):
        run = self.fixture('accepted')
        for key, value in (('validation_refs', []), ('integration_ref', None), ('acceptance_ref', None)):
            original = run[key]
            run[key] = value
            self.save(run)
            self.check(False, 'aceptación sin')
            run[key] = original
        self.save(run)
        self.check()

    def test_v12_proposal_out_of_scope(self):
        run = self.fixture('submitted')
        delivery = json.loads((self.project / run['delivery_ref']['path']).read_text())
        delivery['proposed_files'] = ['PROJECT_STATE.md']
        self.rewrite_artifact(run, 'delivery_ref', delivery)
        self.check(False, 'fuera de scope')

    def test_v13_unknown_dispatch_is_not_completion(self):
        run = self.fixture()
        run['runtime']['observation'] = 'unknown'
        self.save(run)
        self.check(contains='NO VERIFICADO')
        self.fixture('prepared', 2)
        # Align claimed snapshots so this case isolates overlap, not stale brief detection.
        run['brief_ref']['sha256'] = digest((self.project / SLICE / 'EXECUTION_BRIEF.md').read_text())
        self.save(run)
        self.check(False, 'más de un encargo')

    def test_v14_cancel_requires_stop_observation(self):
        run = self.fixture('cancelled')
        run['runtime']['observation'] = 'unknown'
        self.save(run)
        self.check(False, 'detención declarada')

    def test_v15_wrong_attempt_or_base_in_delivery(self):
        for key, value in (('attempt_id', 'old-attempt'), ('base_digest', '0' * 64)):
            run = self.fixture('submitted')
            delivery = json.loads((self.project / run['delivery_ref']['path']).read_text())
            delivery[key] = value
            self.rewrite_artifact(run, 'delivery_ref', delivery)
            self.check(False, 'intento/base')

    def test_v15_duplicate_check_does_not_apply_any_patch(self):
        self.fixture('accepted')
        self.check()
        self.check()
        self.assertEqual((self.project / 'src/example.txt').read_text(), fixture_files()['src/example.txt'])

    def test_v16_retry_valid_after_failed_stopped_attempt(self):
        self.fixture('failed', 1)
        self.fixture('prepared', 2)
        self.check()

    def test_v04_retry_cannot_overlap_running_attempt(self):
        first = self.fixture('running', 1)
        self.fixture('prepared', 2)
        first['brief_ref']['sha256'] = digest((self.project / SLICE / 'EXECUTION_BRIEF.md').read_text())
        self.save(first)
        self.check(False, 'más de un encargo')

    def test_v16_no_third_attempt_or_id_reset(self):
        self.fixture('failed', 1)
        second = self.fixture('prepared', 2)
        second['assignment_id'] = 'new-budget'
        self.save(second)
        self.check(False, 'resetear presupuesto')
        self.fixture('prepared', 3)
        self.check(False, 'fuera de límite')

    def test_v17_recursion_and_expired_checkpoint(self):
        run = self.fixture()
        run['no_recursion'] = False
        self.save(run)
        self.check(False, 'constante')
        run['no_recursion'] = True
        run['review_at'] = '2000-01-01T00:00:00Z'
        self.save(run)
        self.check(contains='Checkpoint vencido')

    def test_v18_model_observation_requires_evidence(self):
        run = self.fixture()
        self.check(contains='Modelo efectivo: unknown')
        run['observed_config'] = {'model': 'fixture-model', 'reasoning': 'medium'}
        self.save(run)
        self.check(False, 'modelo observado sin evidencia')

    def test_v19_runtime_capability_evidence_missing(self):
        run = self.fixture()
        run['runtime']['capability_ref']['path'] = 'missing.txt'
        self.save(run)
        self.check(False, 'inexistente')

    def test_v21_bad_types_enums_json_and_reopening(self):
        for key, value in (('schema_version', True), ('attempt_number', False), ('status', 'DONE'), ('unrecognized', 1)):
            run = self.fixture()
            run[key] = value
            self.save(run)
            self.check(False)
        self.put(self.project / RUN, '{"status": "prepared", "status": "accepted"}')
        self.check(False, 'JSON')
        run = self.fixture('accepted')
        run['history'].append({'status': 'running', 'at': '2026-09-20T12:04:00Z',
                               'evidence_ref': run['runtime']['capability_ref']})
        run['status'] = 'running'
        self.save(run)
        self.check(False, 'transición')

    def test_invalid_timestamp_and_duplicate_markdown_fields(self):
        run = self.fixture()
        run['review_at'] = 'tomorrow'
        self.save(run)
        self.check(False, 'timestamp')
        self.fixture()
        path = self.project / REQ / 'STATE.md'
        self.put(path, path.read_text() + 'Delegation authorization: denied\n')
        self.check(False, 'contradictorio')

    def test_live_attempt_cannot_outlive_slice_or_requirement(self):
        for relative in (SLICE + '/SPEC.md', REQ + '/STATE.md'):
            self.fixture()
            path = self.project / relative
            self.put(path, path.read_text().replace('Status: active', 'Status: completed')
                     .replace('Status: in-progress', 'Status: completed'))
            self.check(False, 'slice activa')

    def test_cancelled_prepared_with_runtime_id_requires_stop(self):
        run = self.fixture()
        run['status'] = 'cancelled'
        run['history'].append({'status': 'cancelled', 'at': '2026-09-20T12:01:00Z',
                               'evidence_ref': run['runtime']['capability_ref']})
        run['runtime']['thread_id'] = 'dispatch-interrupted-before-running'
        self.save(run)
        self.check(False, 'detención')

    def test_contradictory_plan_version_is_rejected(self):
        self.fixture()
        path = self.project / REQ / 'STATE.md'
        self.put(path, path.read_text() + 'Plan version: v0\n')
        self.check(False, 'contradictorio')

    def test_current_pointer_plan_version_and_handoff(self):
        run = self.fixture()
        run['plan_version'] = 'v2'
        self.save(run)
        self.check(False, 'versión de plan')
        self.fixture('failed')
        second = self.fixture('prepared', 2)
        second['coordinator_id'] = 'different-owner'
        self.save(second)
        self.check(False, 'handoff')

    def test_v22_cli_read_only_and_doctor_integration(self):
        self.fixture('accepted')
        before = lifecycle.snapshot(self.project)
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/lib/check_execution.py'),
                                 '--project', str(self.project)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('STATIC PASS', result.stdout)
        self.assertIn('NO VERIFICADOS', result.stdout)
        self.assertEqual(before, lifecycle.snapshot(self.project))
        self.run_script('install')
        self.run_script('init-project')
        run = self.fixture()
        run['max_attempts'] = 100
        self.save(run)
        output = self.run_script('doctor', '--project', str(self.project), ok=False).stdout
        self.assertIn('Delegación: reconciliá registros', output)

    def test_schema_examples_and_supported_keyword_subset(self):
        check = ExecutionCheck(self.project)
        keys = {'$schema', '$defs', '$ref', 'title', 'description', 'type', 'const', 'enum',
                'properties', 'required', 'additionalProperties', 'items', 'minItems', 'maxItems',
                'minLength', 'pattern', 'minimum', 'maximum', 'oneOf', 'not'}
        def walk(rule):
            self.assertFalse(set(rule) - keys)
            for key in ('properties', '$defs'):
                for child in rule.get(key, {}).values():
                    walk(child)
            if 'items' in rule:
                walk(rule['items'])
            for branch in rule.get('oneOf', []):
                walk(branch)
            if 'not' in rule:
                walk(rule['not'])
        walk(check.schema)
        for status in ('prepared', 'running', 'submitted', 'accepted', 'failed', 'cancelled'):
            files = fixture_files(status)
            validate_shape(json.loads(files[RUN]), check.schema, check.schema)

    def test_shipped_example_matches_fixture_and_validates_read_only(self):
        example = ROOT / 'examples/guided-delegation/project'
        for relative, content in fixture_files('accepted').items():
            self.assertEqual((example / relative).read_text(), content, relative)
        before = lifecycle.snapshot(example)
        checked = ExecutionCheck(example).scan()
        self.assertFalse(checked.errors, checked.errors)
        self.assertEqual(len(checked.records), 1)
        self.assertEqual(before, lifecycle.snapshot(example))


if __name__ == '__main__':
    unittest.main()
