"""Fast, offline distribution checks shared by local verification and CI."""
import json
import re
import sys
import tomllib
from pathlib import Path

root = Path(sys.argv[1])
manifest = json.loads((root / 'MANIFEST.json').read_text())
version = manifest['version']
assert version == '2.3.0-rc.1' and manifest['codename'] == 'Supervised Delegation Preview'
required = [
    'FACTORY_VERSION.md', 'README.md', 'QUICK_START.md', 'FILE_INDEX.md',
    'scripts/asf', 'scripts/asf.sh', 'scripts/doctor.sh', 'scripts/lib/runtime_doctor.py',
    '.github/workflows/ci.yml', 'docs/guides/RUNTIME_GUARDRAILS.md',
    'docs/guides/SESSION_PREFLIGHT.md', 'docs/guides/ASF_LAUNCHER.md',
    'docs/guides/UPGRADE_2_2_1_TO_2_2_2.md', 'docs/troubleshooting/PREMATURE_STOP.md',
    'docs/troubleshooting/PROFILE_MISMATCH.md', 'config/MODEL_CATALOG.md',
    'skills/core/model-router/SKILL.md', 'tests/test_runtime_guardrails.py',
    'docs/guides/GUIDED_DELEGATION.md', 'templates/slice/RUN.schema.json',
    'scripts/lib/check_execution.py', 'tests/test_delegation_contract.py',
    'tests/delegation_fixture.py', 'examples/guided-delegation/README.md',
    'examples/guided-delegation/WALKTHROUGHS.md',
    'scripts/lib/audit_workspace.py', 'tests/test_supervised_delegation.py',
    'tests/test_workspace_audit.py', 'examples/supervised-multiagent/README.md',
    'config/assistant-proposal/coordinator.toml', 'config/assistant-proposal/asf_helper.toml',
    'scripts/lib/check_assistant_proposal.py', 'tests/test_release_candidate.py',
    'docs/guides/ASSISTANT_INTEGRATION.md', 'docs/guides/UPGRADE_2_2_2_TO_2_3_0.md',
    'docs/releases/v2.3.0-rc.1.md',
    'docs/guides/CONTEXT_ECONOMY_TEXT_HELPER.md', 'scripts/lib/context_economy.py',
    'tests/test_context_economy.py',
]
for name in required:
    assert (root / name).is_file(), f'Missing required file: {name}'
for name in ['FACTORY_VERSION.md', 'README.md', 'QUICK_START.md', 'FILE_INDEX.md', 'MANIFEST.md',
             'templates/PROJECT_PROFILE.md', 'templates/AGENTS.md', 'scripts/install.sh',
             'scripts/adopt-project.sh', 'docs/maintainers/RELEASE_CHECKLIST.md']:
    assert version in (root / name).read_text(), f'Stale version: {name}'
assert sorted(manifest['scripts']) == sorted(p.name for p in (root / 'scripts').glob('*.sh'))
contract = (root / 'workflow/00_SHARED_CONTRACT.md').read_text()
for marker in ['Finalization Gate', 'PROHIBIDO FINALIZAR', 'Runtime limitation',
               'INVARIANT 1', 'INVARIANT 2', 'INVARIANT 3', 'INVARIANT 4']:
    assert marker in contract, f'Missing canonical guardrail: {marker}'
for name in ['workflow/10_RESUME.md', 'templates/AGENTS.md',
             'skills/core/requirement-state/SKILL.md', 'skills/core/slice-executor/SKILL.md',
             'skills/core/model-router/SKILL.md']:
    assert 'Finalization Gate' in (root / name).read_text(), name
context_guide = (root / 'docs/guides/CONTEXT_ECONOMY_TEXT_HELPER.md').read_text()
for marker in ['inline/local (default)', 'RUN v3', 'un solo intento', 'no reintentar']:
    assert marker in context_guide, f'Missing CE-v1 guardrail: {marker}'
run_schema = json.loads((root / 'templates/slice/RUN.schema.json').read_text())
assert set(run_schema['properties']['schema_version']['enum']) == {1, 2, 3}
catalog = (root / 'config/MODEL_CATALOG.md').read_text()
launcher = (root / 'scripts/asf.sh').read_text()
for profile, model, effort in [('economical', 'gpt-5.6-luna', 'low'),
                               ('balanced', 'gpt-5.6-terra', 'medium'),
                               ('advanced', 'gpt-5.6-sol', 'high'),
                               ('exceptional', 'gpt-6-astra', 'high')]:
    data = tomllib.loads((root / f'config/codex-profiles/asf-{profile}.config.toml').read_text())
    assert (data['model'], data['model_reasoning_effort']) == (model, effort), profile
    assert model in catalog and f"MODEL='{model}'" in launcher and f'EFFORT={effort}' in launcher
    assert not re.search(r'(?i)(?:model\s*=\s*|--model\s+)["\x27`]?gpt-5\.6["\x27`\s;]', launcher)
for path in root.rglob('*'):
    if not path.is_file() or any(p in {'.git', '.agents', '.codex', '__pycache__'} for p in path.relative_to(root).parts):
        continue
    if path.suffix not in {'.md', '.sh', '.py', '.toml', '.json', '.yml'}:
        continue
    text = path.read_text()
    assert not re.search(r'/(?:Users|home)/[A-Za-z][^/\s]*/', text), f'Personal path: {path}'
    if path.suffix == '.toml':
        assert not re.search(r'model\s*=\s*["\x27]gpt-5\.6["\x27]', text), f'Ambiguous model: {path}'
print('PASS: bash syntax, required files, version consistency, Finalization Gate, model mappings, launcher, no personal paths/ambiguous selections.')
