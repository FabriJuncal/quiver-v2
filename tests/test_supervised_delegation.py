"""Offline v2 tests: validate records and observations, never real agents/permissions."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import unittest

import test_scripts as lifecycle
sys.path.insert(0, str(lifecycle.ROOT / 'scripts/lib'))
from audit_workspace import compare
from check_execution import ExecutionCheck
from delegation_fixture import audited_fixture_files, fixture_files, digest, REQ, SLICE, RUN


class SupervisedDelegation(unittest.TestCase):
    setUp = lifecycle.Scripts.setUp
    put = lifecycle.Scripts.put
    run_script = lifecycle.Scripts.run_script

    def fixture(self, status='prepared', number=1):
        for path, body in audited_fixture_files(status, number).items():
            self.put(self.project / path, body)
        return json.loads((self.project / SLICE / f'runs/attempt-{number}.json').read_text())

    def save(self, run):
        self.put(self.project / SLICE / f"runs/{run['attempt_id']}.json", json.dumps(run))

    def check(self, expected=None):
        before = lifecycle.snapshot(self.project)
        result = ExecutionCheck(self.project, now=datetime(2026, 9, 21, tzinfo=timezone.utc)).scan()
        self.assertEqual(before, lifecycle.snapshot(self.project))
        if expected:
            self.assertIn(expected, '\n'.join(result.errors))
        else:
            self.assertEqual(result.errors, [])
        return result

    def document(self, ref):
        return json.loads((self.project / ref['path']).read_text())

    def rewrite(self, ref, value):
        body = json.dumps(value)
        self.put(self.project / ref['path'], body)
        ref['sha256'] = digest(body)

    def incident(self, run, scope='copy'):
        sup = run['supervision']
        after = self.document(sup[scope + '_after_ref'])
        next(e for e in after['entries'] if e['kind'] == 'file')['sha256'] = '0' * 64
        self.rewrite(sup[scope + '_after_ref'], after)
        self.rewrite(sup[scope + '_audit_ref'], compare(self.document(sup[scope + '_before_ref']), after))
        sup['controls']['no_copy_writes']['observed'] = 'unknown'
        sup['incident_refs'] = [run['runtime']['capability_ref']]
        self.save(run)

    def test_m01_m02_legacy_and_all_v2_states(self):
        self.check()
        for status in ('prepared', 'running', 'submitted', 'accepted', 'failed', 'cancelled'):
            with self.subTest(status=status):
                self.fixture(status)
                result = self.check()
                self.assertIn('NO APTO PARA PILOTO', '\n'.join(result.warnings))

    def test_m03_version_policy_optin_risk(self):
        for key, value in [('schema_version', 3), ('schema_version', True), ('schema_version', 1)]:
            run = self.fixture()
            run[key] = value
            self.save(run)
            self.check('versión/contrato')
        run = self.fixture()
        del run['supervision']['risk_acceptance_ref']
        self.save(run)
        self.check('faltan campos')
        run = self.fixture()
        self.put(self.project / REQ / 'STATE.md', 'Delegation policy: supervised-sequential-v1\nDelegation authorization: approved\n')
        self.check('opt-in')
        self.fixture()
        self.put(self.project / REQ / 'STATE.md', 'Delegation policy: supervised-audited-v1\nDelegation authorization: pending\n')
        self.check('opt-in')

    def test_v1_cannot_silently_gain_supervision(self):
        for path, body in fixture_files().items():
            self.put(self.project / path, body)
        self.check()
        run = json.loads((self.project / RUN).read_text())
        run['supervision'] = None
        self.save(run)
        self.check('versión/contrato')

    def test_m04_m18_controls_do_not_certify_enforcement(self):
        run = self.fixture()
        control = run['supervision']['controls']['original_protection']
        control['enforced'] = True
        self.save(run)
        self.check('campos desconocidos')
        for name in ('original_protection', 'external_mutations', 'no_recursion', 'observation_and_stop'):
            run = self.fixture()
            run['supervision']['controls'][name]['mechanism'] = 'instruction'
            self.save(run)
            self.check('no sustituible')
        run = self.fixture()
        run['supervision']['controls']['no_copy_writes']['mechanism'] = 'runtime'
        self.save(run)
        self.check('no enforcement')
        run = self.fixture()
        run['supervision']['controls']['original_protection']['observed'] = 'satisfied'
        self.save(run)
        self.check('sin evidencia')

    def test_m05_m22_audits_must_match_manifests_and_attempt(self):
        run = self.fixture('accepted')
        self.check()
        ref = run['supervision']['copy_audit_ref']
        report = self.document(ref)
        report['changes'] = [{'path': 'src/example.txt', 'change': 'removed'}]
        self.rewrite(ref, report)
        self.save(run)
        self.check('discrepa')
        run = self.fixture('accepted')
        ref = run['supervision']['copy_before_ref']
        manifest = self.document(ref)
        manifest['scope_id'] = 'another-attempt:copy'
        self.rewrite(ref, manifest)
        self.save(run)
        self.check('intento/alcance')

    def test_m11_m14_incidents_reject_delivery_preserve_original(self):
        for scope in ('copy', 'original'):
            run = self.fixture('accepted')
            self.incident(run, scope)
            self.check('entrega rechazada')
            run = self.fixture('failed')
            self.incident(run, scope)
            result = self.check()
            self.assertIn('INCIDENTE', '\n'.join(result.warnings))
            run['supervision']['incident_refs'] = []
            self.save(run)
            self.check('incidente sin evidencia')

    def test_m12_missing_audit_stop_delivery_validation(self):
        for scope in ('copy', 'original'):
            run = self.fixture('submitted')
            run['supervision'][scope + '_after_ref'] = None
            run['supervision'][scope + '_audit_ref'] = None
            self.save(run)
            self.check('sin auditoría final')
        for key, value, expected in [('delivery_ref', None, 'DONE'), ('validation_refs', [], 'aceptación sin')]:
            run = self.fixture('accepted')
            run[key] = value
            self.save(run)
            self.check(expected)
        run = self.fixture('submitted')
        run['runtime']['stop_confirmed'] = False
        self.save(run)
        self.check('sin detención')

    def test_m13_m17_stale_delivery_and_scope(self):
        run = self.fixture('submitted')
        ref = run['delivery_ref']
        data = self.document(ref)
        data['attempt_id'] = 'old-attempt'
        self.rewrite(ref, data)
        self.save(run)
        self.check('intento/base')
        run = self.fixture('submitted')
        ref = run['delivery_ref']
        data = self.document(ref)
        data['proposed_files'] = ['PROJECT_STATE.md']
        self.rewrite(ref, data)
        self.save(run)
        self.check('fuera de scope')

    def test_m17_command_in_delivery_is_data_not_execution(self):
        run = self.fixture('submitted')
        ref = run['delivery_ref']
        data = self.document(ref)
        marker = self.base / 'must-not-exist'
        data['commands'] = [{'command': f'touch "{marker}"', 'result': 'not-run', 'evidence_ref': None}]
        self.rewrite(ref, data)
        self.save(run)
        self.check()
        self.assertFalse(marker.exists())

    def test_v2_hardlink_evidence_is_rejected(self):
        import os
        run = self.fixture()
        ref = run['supervision']['context_review_ref']
        source = self.project / ref['path']
        alias = self.base / 'outside-evidence'
        os.link(source, alias)
        self.check('hardlink')

    def test_m15_m16_unknown_and_retry_limits(self):
        run = self.fixture('failed')
        run['runtime']['observation'] = 'unknown'
        run['runtime']['stop_confirmed'] = False
        self.save(run)
        self.fixture('prepared', 2)
        self.check('más de un encargo')

    def test_m16_no_recursion_no_budget_reset(self):
        run = self.fixture()
        run['no_recursion'] = False
        self.save(run)
        self.check('constante')
        run = self.fixture()
        run['attempt_number'] = 3
        self.save(run)
        self.check('límite')

    def test_m20_unknown_model_never_becomes_observed(self):
        self.fixture('accepted')
        self.assertIn('Modelo efectivo: unknown', '\n'.join(self.check().warnings))

    def test_m22_tampered_evidence(self):
        run = self.fixture('accepted')
        self.put(self.project / run['supervision']['copy_before_ref']['path'], '{}')
        self.check('digest obsoleto')

    def test_incomplete_audit_can_record_failure_not_acceptance(self):
        run = self.fixture('failed')
        sup = run['supervision']
        sup['copy_after_ref'] = sup['copy_audit_ref'] = None
        sup['controls']['no_copy_writes']['observed'] = 'unknown'
        sup['incident_refs'] = [run['runtime']['capability_ref']]
        self.save(run)
        self.assertIn('auditoría incompleta', '\n'.join(self.check().warnings))

    def test_initial_manifest_must_cover_declared_input(self):
        run = self.fixture()
        ref = run['supervision']['copy_before_ref']
        value = self.document(ref)
        value['entries'] = [e for e in value['entries'] if e['path'] != 'src/example.txt']
        self.rewrite(ref, value)
        self.save(run)
        self.check('no cubre base')

    def test_false_clean_claim_with_changed_snapshot(self):
        run = self.fixture('failed')
        self.incident(run)
        run['supervision']['controls']['no_copy_writes']['observed'] = 'satisfied'
        self.save(run)
        self.check('comparación final limpia')

    def test_shipped_v2_example_matches_generator(self):
        root = lifecycle.ROOT / 'examples/supervised-multiagent/project'
        for path, body in audited_fixture_files('accepted').items():
            self.assertEqual((root / path).read_text(), body, path)
        before = lifecycle.snapshot(root)
        result = ExecutionCheck(root).scan()
        self.assertEqual(result.errors, [])
        self.assertEqual(len(result.records), 1)
        self.assertEqual(before, lifecycle.snapshot(root))

    def test_m23_cli_and_doctor_read_only(self):
        run = self.fixture('accepted')
        before = lifecycle.snapshot(self.project)
        command = [sys.executable, '-I', '-B', str(lifecycle.ROOT / 'scripts/lib/check_execution.py'), '--project', str(self.project)]
        for _ in range(2):
            result = subprocess.run(command, env=self.env, capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn('NO VERIFICADOS', result.stdout)
            self.assertNotIn('READY', result.stdout)
        self.assertEqual(before, lifecycle.snapshot(self.project))
        self.run_script('install')
        self.run_script('init-project')
        before = lifecycle.snapshot(self.project)
        out = self.run_script('doctor', '--project', str(self.project)).stdout
        self.assertIn('NO APTO PARA PILOTO', out)
        self.assertEqual(before, lifecycle.snapshot(self.project))
        self.incident(run)
        before = lifecycle.snapshot(self.project)
        out = self.run_script('doctor', '--project', str(self.project), ok=False).stdout
        self.assertIn('entrega rechazada por incidente', out)
        self.assertEqual(before, lifecycle.snapshot(self.project))


if __name__ == '__main__':
    unittest.main()
