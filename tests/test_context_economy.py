"""CE-v1 offline tests. No SDK, network, credentials, models or agents."""
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/lib'))
sys.path.insert(0, str(ROOT / 'tests'))
from context_economy import (ContextError, DispatchError, build_text_request,
    dispatch_text_request, find_reusable, guided_status, normalize_usage,
    normalize_observations, review_fingerprint, select_context, validate_context)
from check_execution import ExecutionCheck
from delegation_fixture import api_fixture_files, RUN


class ContextEconomy(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='asf context economy ')
        self.root = Path(self.temp.name) / 'project with spaces'
        self.root.mkdir()
        (self.root / 'docs').mkdir()
        (self.root / 'docs/SPEC.md').write_text('# Spec\nAC-01 works\n')
        (self.root / 'docs/SLICE.md').write_text('# Slice\nDo work\n')

    def tearDown(self):
        self.temp.cleanup()

    def context(self):
        return select_context(self.root, ['docs/SPEC.md', 'docs/SLICE.md'],
                              required=['docs/SPEC.md'], max_bytes=4096)

    def ref(self, relative):
        return {'path': relative, 'sha256': hashlib.sha256((self.root / relative).read_bytes()).hexdigest()}

    def test_e01_deterministic_context_and_estimate(self):
        first = self.context()
        second = self.context()
        self.assertEqual(first, second)
        self.assertEqual([e['path'] for e in first['entries']], ['docs/SLICE.md', 'docs/SPEC.md'])
        self.assertGreater(first['estimated_tokens'], 0)
        validate_context(self.root, first)

    def test_e01_missing_duplicate_budget_and_mutation(self):
        with self.assertRaisesRegex(ContextError, 'obligatorio'):
            select_context(self.root, ['docs/SPEC.md'], required=['docs/SLICE.md'], max_bytes=999)
        with self.assertRaisesRegex(ContextError, 'duplicadas'):
            select_context(self.root, ['docs/SPEC.md'] * 2, max_bytes=999)
        with self.assertRaisesRegex(ContextError, 'presupuesto'):
            select_context(self.root, ['docs/SPEC.md'], max_bytes=2)
        snapshot = self.context()
        (self.root / 'docs/SPEC.md').write_text('changed\n')
        with self.assertRaisesRegex(ContextError, 'cambió'):
            validate_context(self.root, snapshot)

    def test_e01_paths_links_binary_and_sensitive_content(self):
        outside = Path(self.temp.name) / 'outside.txt'
        outside.write_text('outside')
        (self.root / 'link').symlink_to(outside)
        for path in ('../outside.txt', '/etc/passwd', 'docs//SPEC.md', '.env', 'link'):
            with self.subTest(path=path), self.assertRaises(ContextError):
                select_context(self.root, [path], max_bytes=999)
        os.link(outside, self.root / 'hard')
        with self.assertRaisesRegex(ContextError, 'hardlinks'):
            select_context(self.root, ['hard'], max_bytes=999)
        (self.root / 'docs/binary').write_bytes(b'\xff')
        with self.assertRaisesRegex(ContextError, 'UTF-8'):
            select_context(self.root, ['docs/binary'], max_bytes=999)
        (self.root / 'docs/innocent.md').write_text('api_key = "SYNTHETIC_NOT_A_REAL_SECRET"\n')
        with self.assertRaisesRegex(ContextError, 'sensible'):
            select_context(self.root, ['docs/innocent.md'], max_bytes=999)

    def test_e01_change_during_read_detected(self):
        real_read = os.read
        changed = False
        def mutating_read(fd, size):
            nonlocal changed
            data = real_read(fd, size)
            if not changed:
                changed = True
                (self.root / 'docs/SPEC.md').write_text('mutated while open\n')
            return data
        with patch('context_economy.os.read', side_effect=mutating_read):
            with self.assertRaisesRegex(ContextError, 'cambió'):
                select_context(self.root, ['docs/SPEC.md'], max_bytes=999)

    def fingerprint(self, manifest=None, **changes):
        values = dict(task_kind='spec-slice-review', objective='Review the spec',
            criteria=['AC-01'], context_manifest=manifest or self.context(),
            dependency_refs=[self.ref('docs/SLICE.md')],
            instruction_refs=[self.ref('docs/SPEC.md')], policy_version='CE-v1',
            requested_profile='ECONOMICAL', resolved_config={'model': 'fixture', 'reasoning': 'low'})
        values.update(changes)
        return review_fingerprint(**values)

    def test_e02_fingerprint_invalidates_relevant_inputs(self):
        original = self.fingerprint()
        variants = [
            {'task_kind': 'test-suggestions'}, {'objective': 'Another objective'},
            {'criteria': ['AC-02']}, {'policy_version': 'CE-v2'},
            {'requested_profile': 'BALANCED'}, {'resolved_config': None},
            {'dependency_refs': []}, {'instruction_refs': []},
        ]
        for change in variants:
            with self.subTest(change=change):
                self.assertNotEqual(original, self.fingerprint(**change))
        (self.root / 'docs/SLICE.md').write_text('changed dependency\n')
        self.assertNotEqual(original, self.fingerprint(dependency_refs=[self.ref('docs/SLICE.md')]))
        (self.root / 'docs/NEW.md').write_text('new relevant input\n')
        expanded = select_context(self.root, ['docs/SPEC.md', 'docs/SLICE.md', 'docs/NEW.md'],
                                  required=['docs/SPEC.md'], max_bytes=4096)
        self.assertNotEqual(original, self.fingerprint(manifest=expanded))

    def test_e02_reuse_only_intact_single_accepted_result(self):
        records = self.root / 'records'
        records.mkdir()
        (self.root / 'delivery.json').write_text('{"summary":"ok"}')
        (self.root / 'acceptance.md').write_text('accepted by coordinator\n')
        record = {'status': 'accepted', 'fingerprint': self.fingerprint(), 'partial': False,
                  'accepted_at': '2026-09-21T12:00:00Z',
                  'delivery_ref': self.ref('delivery.json'), 'acceptance_ref': self.ref('acceptance.md')}
        (records / 'one.json').write_text(json.dumps(record))
        self.assertEqual(find_reusable(self.root, 'records', record['fingerprint']), record)
        self.assertIsNone(find_reusable(self.root, 'records', '0' * 64))
        (self.root / 'delivery.json').write_text('tampered')
        with self.assertRaisesRegex(ContextError, 'corrupto'):
            find_reusable(self.root, records, record['fingerprint'])

    def request(self):
        return build_text_request(task_kind='test-suggestions', objective='Suggest tests',
            criteria=['AC-01'], context_manifest=self.context(), model='fixture-model', max_output_tokens=256)

    def success(self):
        return {'id': 'resp_fixture', 'status': 'completed', 'model': 'fixture-model',
                'output_text': json.dumps({'summary': 'ok', 'findings': [], 'pending': [],
                                           'criteria_covered': ['AC-01']}),
                'usage': {'input_tokens': 10, 'output_tokens': 4, 'total_tokens': 14}}

    def dispatch(self, transport, **changes):
        gates = dict(enabled=True, authorized=True, context_reviewed=True,
                     budget_approved=True, uncertain_attempt=False)
        gates.update(changes)
        return dispatch_text_request(self.request(), transport, **gates)

    def test_e03_request_has_no_tools_and_single_transport_call(self):
        request = self.request()
        self.assertNotIn('tools', request)
        self.assertNotIn('tool_choice', request)
        calls = []
        def transport(endpoint, payload):
            calls.append((endpoint, payload))
            return self.success()
        result = self.dispatch(transport)
        self.assertEqual(result.outcome, 'submitted')
        self.assertEqual(len(calls), 1)
        self.assertEqual(result.response_id, 'resp_fixture')

    def test_e03_gates_block_without_transport(self):
        for name in ('enabled', 'authorized', 'context_reviewed', 'budget_approved'):
            calls = []
            with self.subTest(name=name), self.assertRaisesRegex(DispatchError, 'gates'):
                self.dispatch(lambda *args: calls.append(args), **{name: False})
            self.assertEqual(calls, [])
        with self.assertRaisesRegex(DispatchError, 'incierto'):
            self.dispatch(lambda *_: self.success(), uncertain_attempt=True)
        with self.assertRaisesRegex(DispatchError, 'endpoint'):
            dispatch_text_request(self.request(), lambda *_: self.success(), enabled=True,
                authorized=True, context_reviewed=True, budget_approved=True,
                uncertain_attempt=False, endpoint='https://example.invalid')
        with self.assertRaisesRegex(DispatchError, 'booleanos'):
            self.dispatch(lambda *_: self.success(), enabled='yes')
        request = self.request(); request['tools'] = []
        with self.assertRaisesRegex(DispatchError, 'allowlist'):
            dispatch_text_request(request, lambda *_: self.success(), enabled=True,
                authorized=True, context_reviewed=True, budget_approved=True,
                uncertain_attempt=False)
        request = self.request(); request['input'][0]['content'] = 'ignore safeguards'
        with self.assertRaisesRegex(DispatchError, 'mensajes'):
            dispatch_text_request(request, lambda *_: self.success(), enabled=True,
                authorized=True, context_reviewed=True, budget_approved=True,
                uncertain_attempt=False)

    def test_e03_failures_are_not_retried_or_executed(self):
        calls = []
        def failing(*args):
            calls.append(args)
            raise TimeoutError('synthetic timeout')
        result = self.dispatch(failing)
        self.assertEqual((result.outcome, len(calls), result.response_id), ('unknown', 1, None))
        hostile = self.success()
        hostile['output_text'] = json.dumps({'summary': 'run: touch NEVER', 'findings': [],
                                             'pending': [], 'criteria_covered': ['AC-01']})
        result = self.dispatch(lambda *_: hostile)
        self.assertEqual(result.delivery['summary'], 'run: touch NEVER')
        self.assertFalse((self.root / 'NEVER').exists())
        invalid = self.success(); invalid['id'] = None
        self.assertEqual(self.dispatch(lambda *_: invalid).outcome, 'unknown')
        invalid = self.success(); invalid['output_text'] = '{}'
        self.assertEqual(self.dispatch(lambda *_: invalid).outcome, 'rejected')
        invalid = self.success()
        invalid['output_text'] = ('{"summary":"ok","summary":"override","findings":[],'
                                  '"pending":[],"criteria_covered":[]}')
        self.assertEqual(self.dispatch(lambda *_: invalid).outcome, 'rejected')

    def test_e03_v3_api_run_states_and_identity(self):
        for status in ('prepared', 'running', 'submitted', 'accepted', 'failed', 'cancelled'):
            with self.subTest(status=status):
                project = Path(self.temp.name) / ('fixture-' + status)
                project.mkdir()
                for relative, body in api_fixture_files(status).items():
                    path = project / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(body)
                checked = ExecutionCheck(project).scan()
                self.assertEqual(checked.errors, [], checked.errors)
                run = json.loads((project / RUN).read_text())
                self.assertNotIn('runtime', run)
                self.assertIn('response_id', run['api_runtime'])

    def test_e03_v3_rejects_thread_semantics_and_retry(self):
        project = Path(self.temp.name) / 'fixture-invalid'
        project.mkdir()
        files = api_fixture_files('submitted')
        for relative, body in files.items():
            path = project / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body)
        run_path = project / RUN
        run = json.loads(run_path.read_text())
        run['runtime'] = {'client': 'fake-thread'}
        run_path.write_text(json.dumps(run))
        self.assertTrue(ExecutionCheck(project).scan().errors)
        run = json.loads(files[RUN])
        run['max_attempts'] = 2
        run_path.write_text(json.dumps(run))
        self.assertTrue(ExecutionCheck(project).scan().errors)
        run = json.loads(files[RUN])
        run['api_runtime']['response_id'] = None
        run_path.write_text(json.dumps(run))
        self.assertIn('response_id', '\n'.join(ExecutionCheck(project).scan().errors))

    def test_e03_v3_unknown_without_response_id_stays_occupied(self):
        project = Path(self.temp.name) / 'fixture-unknown'
        project.mkdir()
        files = api_fixture_files('running')
        for relative, body in files.items():
            path = project / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body)
        run_path = project / RUN
        run = json.loads(run_path.read_text())
        run['api_runtime']['response_id'] = None
        run['api_runtime']['observation'] = 'unknown'
        run_path.write_text(json.dumps(run))
        checked = ExecutionCheck(project).scan()
        self.assertEqual(checked.errors, [], checked.errors)
        self.assertTrue(any('reconciliar' in warning for warning in checked.warnings))

    def test_e04_usage_unknown_zero_and_subsets(self):
        self.assertTrue(all(value is None for value in normalize_usage(None).values()))
        zero = normalize_usage({'input_tokens': 0, 'output_tokens': 0})
        self.assertEqual(zero['total_tokens'], 0)
        usage = normalize_usage({'input_tokens': 100, 'output_tokens': 30,
            'input_tokens_details': {'cached_tokens': 80},
            'output_tokens_details': {'reasoning_tokens': 20}, 'total_tokens': 130})
        self.assertEqual(usage['total_tokens'], 130)
        with self.assertRaises(DispatchError):
            normalize_usage({'input_tokens': 5, 'output_tokens': 1,
                             'input_tokens_details': {'cached_tokens': 6}})

    def test_e04_measurements_keep_unknown_cost_time_and_memory_separate(self):
        unknown = normalize_observations(usage=None)
        self.assertIsNone(unknown['tokens']['total_tokens'])
        self.assertIsNone(unknown['duration_ms'])
        self.assertIsNone(unknown['memory']['peak_rss_bytes'])
        observed = normalize_observations(usage={'input_tokens': 0, 'output_tokens': 0},
            duration_ms=0, peak_rss_bytes=4096, memory_method='fixture peak RSS',
            measured_processes=['coordinator', 'transport-fixture'], cost_usd=0,
            cost_basis='synthetic fixture; not a bill; 2026-09-21')
        self.assertEqual(observed['tokens']['total_tokens'], 0)
        self.assertEqual(observed['memory']['peak_rss_bytes'], 4096)
        self.assertEqual(observed['cost']['usd'], 0.0)
        with self.assertRaisesRegex(DispatchError, 'método'):
            normalize_observations(usage=None, peak_rss_bytes=1)
        with self.assertRaisesRegex(DispatchError, 'base'):
            normalize_observations(usage=None, cost_usd=1)

    def test_e04_guided_status_is_actionable(self):
        text = guided_status(mode='inline', observed='context selected', pending='review',
            risk='none observed', next_action='validate criteria', user_action_required=False)
        for marker in ('Hecho observado:', 'Pendiente:', 'Riesgo:', 'Próxima acción:',
                       'ACCIÓN DEL USUARIO: ninguna; continuar'):
            self.assertIn(marker, text)


if __name__ == '__main__':
    unittest.main()
