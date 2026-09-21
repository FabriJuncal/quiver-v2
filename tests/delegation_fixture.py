"""Synthetic evidence for offline tests/examples. Never represents a real worker."""
import hashlib
import json

REQ = 'docs/requirements/demo'
SLICE = REQ + '/slices/S01'
RUN = SLICE + '/runs/attempt-1.json'


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def fixture_files(status='prepared', number=1):
    attempt = f'attempt-{number}'
    run_path = SLICE + f'/runs/{attempt}.json'
    files = {
        'AGENTS.md': '# Synthetic fixture\nFactory version: 2.2.2\n',
        'src/example.txt': 'Original input; synthetic offline fixture.\n',
        REQ + '/STATE.md': '# Synthetic requirement\nStatus: in-progress\nPlan version: v1\n'
        'Delegation policy: supervised-sequential-v1\nDelegation authorization: approved\n'
        'Current slice: S01\nNext action: inspect synthetic fixture, never dispatch\n'
        'Why this is next: offline example only\nUser action required: true\n'
        'Decision required: none\nExpected output: static validation report\n'
        'After this: return to the real project state\nBlocked by: none\n'
        'Runtime limitation: none\nResume instruction: inspect fixture only; do not execute agents\n',
        REQ + '/AUTHORIZATION.md': '# FIXTURE ONLY\nSimulated authorization, not a user approval.\n',
        REQ + '/CRITERIA.md': '# AC01\nExplain the input; proposals only.\n',
        SLICE + '/SPEC.md': '# Synthetic slice\nSlice ID: S01\nStatus: active\nDependency refs: []\n',
        SLICE + '/EXECUTION_BRIEF.md': '# Fixture brief\nCurrent attempt: ' + run_path + '\n',
        SLICE + '/CLOSURE_BRIEF.md': '# SYNTHETIC closure example — slice still active\n'
        'Attempt: ' + run_path + '\n'
        'Delivery acceptance: simulated only; see acceptance.txt\n'
        'Integration: analysis only, no source patch; see integration.txt\n'
        'Validation: synthetic evidence in validation.txt; real worker tests NOT RUN\n'
        'Pending: coordinator must evaluate remaining criteria before slice closure\n'
        'Next action: inspect fixture only; never dispatch from this example\n',
        SLICE + '/runtime.txt': 'SYNTHETIC: fixture event, no real process/model/permission checked.\n',
        SLICE + '/validation.txt': 'SYNTHETIC coordinator validation of analysis; not actual test evidence.\n',
        SLICE + '/integration.txt': 'SYNTHETIC analysis accepted without modifying source.\n',
        SLICE + '/acceptance.txt': 'SYNTHETIC coordinator acceptance for AC01.\n',
    }

    def ref(path):
        return {'path': path, 'sha256': digest(files[path])}

    base = [ref('src/example.txt')]
    stages = ['prepared']
    if status != 'prepared':
        stages += ['running']
    if status in {'submitted', 'accepted'}:
        stages += ['submitted']
    if status in {'accepted', 'failed', 'cancelled'}:
        stages += [status]
    hour = 11 + number
    history = [{'status': s, 'at': f'2026-09-20T{hour:02}:0{i}:00Z',
                'evidence_ref': ref(SLICE + '/runtime.txt') if i else None}
               for i, s in enumerate(stages)]
    stopped = status in {'submitted', 'accepted', 'failed', 'cancelled'}
    delivery_ref = None
    if status in {'submitted', 'accepted'}:
        delivery = {
            'attempt_id': attempt,
            'base_digest': digest(json.dumps(base, sort_keys=True, separators=(',', ':'))),
            'kind': 'analysis', 'proposed_files': [], 'worker_write_paths': [],
            'criteria_covered': ['AC01'], 'commands': [{'command': 'none (analysis only)',
                'result': 'not-run', 'evidence_ref': None}],
            'findings': [], 'pending': [], 'summary': 'SYNTHETIC response for offline validation.',
        }
        name = SLICE + f'/{attempt}-delivery.json'
        files[name] = json.dumps(delivery, indent=2) + '\n'
        delivery_ref = ref(name)
    run = {
        'schema_version': 1, 'requirement_ref': REQ + '/STATE.md', 'slice_id': 'S01',
        'assignment_id': 'assignment-S01', 'attempt_id': attempt, 'attempt_number': number,
        'plan_version': 'v1', 'authorization_ref': ref(REQ + '/AUTHORIZATION.md'),
        'coordinator_id': 'fixture-coordinator', 'handoff_ref': None,
        'brief_ref': ref(SLICE + '/EXECUTION_BRIEF.md'), 'base_refs': base,
        'context_refs': [ref(REQ + '/CRITERIA.md')], 'instruction_refs': [ref('AGENTS.md')],
        'factory_version': '2.2.2', 'objective': 'Explain input without writing files.',
        'criteria_refs': [ref(REQ + '/CRITERIA.md')],
        'read_scope': ['src/example.txt', REQ + '/CRITERIA.md', 'AGENTS.md'],
        'proposal_scope': ['src/example.txt'], 'project_write_scope': [], 'dependencies': [],
        'max_attempts': 2, 'no_recursion': True, 'review_at': '2099-09-20T12:00:00Z',
        'runtime': {'client': 'offline-fixture', 'version': 'synthetic',
            'capability_ref': ref(SLICE + '/runtime.txt'),
            'thread_id': 'fixture-thread-' + str(number) if status != 'prepared' else None,
            'observation': 'known', 'observed_at': f'2026-09-20T{hour:02}:05:00Z',
            'stop_confirmed': stopped, 'stop_evidence_ref': ref(SLICE + '/runtime.txt') if stopped else None},
        'requested_profile': 'BALANCED', 'resolved_config': None, 'observed_config': None,
        'model_evidence_ref': None, 'status': status, 'reason': 'SYNTHETIC fixture, not runtime evidence.',
        'history': history, 'delivery_ref': delivery_ref,
        'validation_refs': [ref(SLICE + '/validation.txt')] if status == 'accepted' else [],
        'integration_ref': ref(SLICE + '/integration.txt') if status == 'accepted' else None,
        'acceptance_ref': ref(SLICE + '/acceptance.txt') if status == 'accepted' else None,
    }
    files[run_path] = json.dumps(run, indent=2) + '\n'
    return files


def audited_fixture_files(status='prepared', number=1):
    """V2 synthetic records; all runtime evidence remains invented test data."""
    from audit_workspace import compare
    files = fixture_files(status, number)
    name = SLICE + f'/runs/attempt-{number}.json'
    run = json.loads(files[name])
    files[REQ + '/STATE.md'] = files[REQ + '/STATE.md'].replace(
        'supervised-sequential-v1', 'supervised-audited-v1')

    def put_ref(path, value):
        files[path] = json.dumps(value, indent=2) + '\n'
        return {'path': path, 'sha256': digest(files[path])}

    evidence = run['runtime']['capability_ref']
    complete = status in {'submitted', 'accepted', 'failed', 'cancelled'}
    controls = {key: {'requested': True, 'mechanism': 'runtime', 'observed': 'unknown',
                      'evidence_ref': None} for key in
                ('original_protection', 'external_mutations', 'no_recursion', 'observation_and_stop')}
    controls['no_copy_writes'] = {'requested': True, 'mechanism': 'instruction',
        'observed': 'satisfied' if complete else 'unknown', 'evidence_ref': evidence if complete else None}
    sup = {'policy': 'supervised-audited-v1', 'risk_acceptance_ref': run['authorization_ref'],
           'context_review_ref': evidence, 'controls': controls, 'incident_refs': []}
    for scope in ('copy', 'original'):
        entries = {'.': {'path': '.', 'kind': 'directory', 'mode': 0o755, 'size': None, 'sha256': None}}
        from pathlib import PurePosixPath
        for path in run['read_scope']:
            for parent in PurePosixPath(path).parents:
                p = parent.as_posix()
                entries[p] = {'path': p, 'kind': 'directory', 'mode': 0o755, 'size': None, 'sha256': None}
            entries[path] = {'path': path, 'kind': 'file', 'mode': 0o644,
                             'size': len(files[path].encode()), 'sha256': digest(files[path])}
        manifest = {'manifest_version': 1, 'scope_id': run['attempt_id'] + ':' + scope,
                    'entries': [entries[p] for p in sorted(entries)]}
        prefix = SLICE + f'/attempt-{number}-{scope}'
        sup[scope + '_before_ref'] = put_ref(prefix + '-before.json', manifest)
        sup[scope + '_after_ref'] = put_ref(prefix + '-after.json', manifest) if complete else None
        sup[scope + '_audit_ref'] = put_ref(prefix + '-audit.json', compare(manifest, manifest)) if complete else None
    run['schema_version'] = 2
    run['supervision'] = sup
    files[name] = json.dumps(run, indent=2) + '\n'
    return files


def api_fixture_files(status='prepared'):
    """V3 synthetic API records; no request, SDK, credentials or model execution."""
    files = fixture_files(status, 1)
    name = RUN
    run = json.loads(files[name])
    files[REQ + '/STATE.md'] = files[REQ + '/STATE.md'].replace(
        'supervised-sequential-v1', 'text-helper-v1')
    run['schema_version'] = 3
    run['max_attempts'] = 1
    runtime = run.pop('runtime')
    run['api_runtime'] = {
        'client': 'openai-responses',
        'version': 'synthetic-offline',
        'capability_ref': runtime['capability_ref'],
        'endpoint': 'https://api.openai.com/v1/responses',
        'response_id': 'resp_fixture_1' if status != 'prepared' else None,
        'observation': runtime['observation'],
        'observed_at': runtime['observed_at'],
        'terminal_observed': status in {'submitted', 'accepted', 'failed', 'cancelled'},
        'terminal_evidence_ref': (runtime['capability_ref']
                                  if status in {'submitted', 'accepted', 'failed', 'cancelled'} else None),
        'request_fingerprint': digest('SYNTHETIC request; never sent.'),
    }
    files[name] = json.dumps(run, indent=2) + '\n'
    return files
