"""Runtime contract regression: real scripts, isolated HOME, no paid model calls."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib
import unittest

import test_scripts as lifecycle

ROOT = lifecycle.ROOT
snapshot = lifecycle.snapshot


class RuntimeGuardrails(unittest.TestCase):
    setUp = lifecycle.Scripts.setUp
    put = lifecycle.Scripts.put
    run_script = lifecycle.Scripts.run_script

    def fixture(self, next_action='Relevar D01-D30 y contrato P05.'):
        self.run_script('install')
        self.run_script('init-project', '--git-init')
        path = self.project / 'PROJECT_STATE.md'
        path.write_text(path.read_text().replace('**Active requirement:** none',
                        '**Active requirement:** docs/requirements/demo/STATE.md')
                        .replace('**Current slice:** none', '**Current slice:** S05'))
        state = self.project / 'docs/requirements/demo/STATE.md'
        self.put(state, '# Requirement\n'
                 '- **Status:** in-progress\n- **Current slice:** S05\n'
                 '- **Pending slices:** S05\n'
                 f'- **Next action:** {next_action}\n'
                 '- **Why this is next:** S04 cerrada, S05 autorizada.\n'
                 '- **User action required:** false\n- **Decision required:** none\n'
                 '- **Expected output:** inventario y contrato\n'
                 '- **After this:** validar inventario contra criterios\n'
                 '- **Blocked by:** none\n- **Runtime limitation:** none\n'
                 '- **Resume instruction:** leer STATE y ejecutar S05\n')
        self.put(state.parent / 'slices/S05/SPEC.md', '# S05\n- **Status:** active\n')
        return state

    def mock_capture(self):
        capture = self.base / 'argv.json'
        self.env['ASF_TEST_CAPTURE'] = str(capture)
        self.put(self.bin / 'codex', f'#!{sys.executable}\n'
                 'import json, os, sys\n'
                 'with open(os.environ["ASF_TEST_CAPTURE"], "w") as f: json.dump(sys.argv[1:], f)\n', 0o755)
        return capture

    def test_launcher_all_profiles_dry_run_no_writes(self):
        for profile, model, effort in [('economical', 'gpt-5.6-luna', 'low'),
                                      ('balanced', 'gpt-5.6-terra', 'medium'),
                                      ('advanced', 'gpt-5.6-sol', 'high'),
                                      ('exceptional', 'gpt-6-astra', 'high')]:
            before = snapshot(self.base)
            output = self.run_script('asf', profile, '--dry-run').stdout
            self.assertIn(model, output)
            self.assertIn(effort, output)
            self.assertIn('DRY RUN', output)
            self.assertEqual(before, snapshot(self.base))

    def test_launcher_literal_arguments_and_override_priority(self):
        capture = self.mock_capture()
        self.put(self.project / '.codex/config.toml', 'model_reasoning_effort = "high"\n')
        prompt = 'Continue $(touch NEVER) `uname` $HOME; literal text'
        self.run_script('asf', 'balanced', '--cd', str(self.project), '--no-alt-screen', '--', prompt)
        self.assertEqual(json.loads(capture.read_text()), ['--model', 'gpt-5.6-terra',
                         '--config', 'model_reasoning_effort="medium"', '--cd', str(self.project),
                         '--no-alt-screen', '--', prompt])
        self.assertFalse((self.project / 'NEVER').exists())
        self.assertEqual((self.project / '.codex/config.toml').read_text(), 'model_reasoning_effort = "high"\n')

    def test_launcher_entrypoint_from_factory_path_with_spaces(self):
        clone = self.base / 'Factory with spaces'
        shutil.copytree(ROOT / 'scripts', clone / 'scripts')
        capture = self.mock_capture()
        result = subprocess.run(['bash', str(clone / 'scripts/asf'), 'advanced', '--', 'Continue work'],
                                env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('gpt-5.6-sol', json.loads(capture.read_text()))

    def test_launcher_conflicting_flags_rejected_before_launch(self):
        capture = self.mock_capture()
        for args in [('--model', 'other'), ('-mfoo',), ('--config=model=x',), ('-c', 'model=x'),
                     ('--profile', 'other'), ('--remote', 'host'), ('--oss',), ('--cd',)]:
            self.run_script('asf', 'balanced', *args, ok=False)
        self.assertFalse(capture.exists())

    def test_launcher_missing_codex(self):
        empty_bin = self.base / 'no codex'
        empty_bin.mkdir()
        for utility in ('dirname', 'tr'):
            (empty_bin / utility).symlink_to(shutil.which(utility))
        self.env['PATH'] = str(empty_bin)
        result = subprocess.run(['/bin/bash', str(ROOT / 'scripts/asf.sh'), 'balanced'],
                                env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 127)
        self.assertIn('Codex CLI no está instalado', result.stderr)
        self.assertIn('NO SE PUDO INICIAR EL PERFIL', result.stdout)

    def test_launcher_unavailable_model_preserves_exit_and_error(self):
        self.put(self.bin / 'codex', '#!/bin/sh\necho "model unavailable" >&2\nexit 42\n', 0o755)
        result = self.run_script('asf', 'balanced', ok=False)
        self.assertEqual(result.returncode, 42)
        self.assertIn('model unavailable', result.stderr)
        self.assertIn('/model', result.stdout)
        self.assertIn('gpt-5.6-terra', result.stdout)
        self.assertIn('continuar', result.stdout)

    def test_active_slice_without_next_action_fails_read_only(self):
        self.fixture('')
        before = snapshot(self.base)
        result = self.run_script('doctor', '--project', str(self.project), ok=False)
        self.assertIn('INVARIANT 1/3', result.stdout)
        self.assertEqual(before, snapshot(self.base))

    def test_active_slice_with_action_passes_read_only(self):
        self.fixture()
        before = snapshot(self.base)
        result = self.run_script('doctor', '--project', str(self.project))
        self.assertIn('CONTINUAR:', result.stdout)
        self.assertIn('active slice: S05', result.stdout)
        self.assertEqual(before, snapshot(self.base))

    def test_doctor_validates_optional_variant_manifest_and_staleness(self):
        self.fixture()
        subprocess.run(['git', 'config', 'user.name', 'Factory Test'], cwd=self.project, env=self.env, check=True)
        subprocess.run(['git', 'config', 'user.email', 'factory@example.invalid'], cwd=self.project, env=self.env, check=True)
        subprocess.run(['git', 'add', '.'], cwd=self.project, env=self.env, check=True)
        subprocess.run(['git', 'commit', '-qm', 'fixture'], cwd=self.project, env=self.env, check=True)
        branch = subprocess.check_output(['git', 'symbolic-ref', 'HEAD'], cwd=self.project, env=self.env, text=True).strip()
        task = self.base / 'variant-task.json'
        task.write_text(json.dumps({
            'objective': 'doctor fixture', 'paths': ['PROJECT_STATE.md'],
            'required_paths': ['PROJECT_STATE.md'], 'max_bytes': 65536,
        }))
        output = self.base / 'variant-context'
        self.run_script('discover-variants', 'context', '--repo', str(self.project),
                        '--target', branch, '--task', str(task), '--output', str(output))
        manifest = output / 'CONTEXT_MANIFEST.json'
        before = snapshot(self.base)
        result = self.run_script('doctor', '--project', str(self.project),
                                 '--variant-manifest', str(manifest))
        self.assertIn('Variant context PASS:', result.stdout)
        self.assertEqual(before, snapshot(self.base))
        self.put(self.project / 'new-overlay.txt', 'changed\n')
        stale = self.run_script('doctor', '--project', str(self.project),
                                '--variant-manifest', str(manifest), ok=False)
        self.assertIn('Variant context inválido u obsoleto', stale.stdout)

    def test_completed_requirement_with_active_slice_fails(self):
        state = self.fixture()
        state.write_text(state.read_text().replace('in-progress', 'completed'))
        self.assertIn('INVARIANT 3', self.run_script('doctor', '--project', str(self.project), ok=False).stdout)

    def test_repeated_strategy_profiles_are_not_conflicting_state(self):
        state = self.fixture()
        state.write_text(state.read_text() + '\n## Planning\n- **Profile:** BALANCED\n'
                         '\n## Review\n- **Profile:** ADVANCED\n')
        self.run_script('doctor', '--project', str(self.project))

    def test_closed_requirement_still_selected_fails(self):
        state = self.fixture()
        (state.parent / 'slices/S05/SPEC.md').write_text('# S05\n- **Status:** completed\n')
        state.write_text(state.read_text().replace('in-progress', 'completed')
                         .replace('**Current slice:** S05', '**Current slice:** none')
                         .replace('**Pending slices:** S05', '**Pending slices:** none'))
        output = self.run_script('doctor', '--project', str(self.project), ok=False).stdout
        self.assertIn('apunta a un requirement cerrado', output)

    def test_malformed_fallback_configuration_guided_error(self):
        self.fixture()
        self.put(self.home / '.codex/config.toml', 'project_doc_fallback_filenames = 42\n')
        output = self.run_script('doctor', '--project', str(self.project), ok=False).stdout
        self.assertIn('debe ser una lista', output)
        self.assertNotIn('Traceback', output)

    def test_outdated_project_and_agents_guided_no_overwrite(self):
        self.fixture()
        for name in ('PROJECT_PROFILE.md', 'AGENTS.md'):
            path = self.project / name
            current = json.loads((ROOT / 'MANIFEST.json').read_text())['version']
            path.write_text(path.read_text().replace(current, '2.2.1'))
        before = snapshot(self.base)
        result = self.run_script('doctor', '--project', str(self.project))
        self.assertIn('PROJECT FACTORY LAYER OUTDATED', result.stdout)
        self.assertIn('UPGRADE_2_2_2_TO_2_3_0.md', result.stdout)
        self.assertEqual(before, snapshot(self.base))

    def test_global_size_near_limit_warning(self):
        self.run_script('install')
        self.agents.write_text(self.agents.read_text() + '\n' + 'x' * 27000 + '\n')
        result = self.run_script('doctor')
        self.assertIn('cerca del límite', result.stdout)
        self.assertIn('32768', result.stdout)

    def test_explicit_instruction_cap_exceeded_errors(self):
        self.fixture()
        self.put(self.home / '.codex/config.toml', 'project_doc_max_bytes = 100\n')
        output = self.run_script('doctor', '--project', str(self.project), ok=False).stdout
        self.assertIn('límites explícitos', output)

    def test_unselected_profile_limit_does_not_prove_truncation(self):
        self.fixture()
        self.put(self.home / '.codex/asf-exceptional.config.toml',
                 'model = "gpt-6-astra"\nmodel_reasoning_effort = "high"\nproject_doc_max_bytes = 100\n')
        output = self.run_script('doctor', '--project', str(self.project)).stdout
        self.assertIn('cerca del límite', output)
        self.assertNotIn('ERROR:', output)

    def test_instruction_chain_override_and_nested_paths(self):
        self.fixture()
        nested = self.project / 'src/nested'
        nested.mkdir(parents=True)
        self.put(self.project / 'src/AGENTS.md', 'Parent rules\n')
        self.put(nested / 'AGENTS.md', 'Ignored rules\n')
        self.put(nested / 'AGENTS.override.md', 'Actual override\n')
        result = subprocess.run([sys.executable, '-I', '-B', str(ROOT / 'scripts/lib/runtime_doctor.py'),
                                 '--root', str(ROOT), '--codex-home', str(self.agents.parent),
                                 '--project', str(nested)], env=self.env, capture_output=True, text=True)
        selected = [line for line in result.stdout.splitlines() if line.startswith('Instruction candidate:')]
        self.assertEqual(len(selected), 4)
        self.assertTrue(any('src/AGENTS.md' in line for line in selected))
        self.assertTrue(any('AGENTS.override.md' in line for line in selected))
        self.assertFalse(any('nested/AGENTS.md' in line for line in selected))

    def test_config_conflict_and_legacy_profiles_guided(self):
        self.fixture()
        self.run_script('configure-model-profiles')
        self.put(self.project / '.codex/config.toml', 'model_reasoning_effort = "high"\n')
        self.put(self.home / '.codex/config.toml', '[profiles.old]\nmodel = "custom"\n')
        output = self.run_script('doctor', '--project', str(self.project)).stdout
        self.assertIn('prevalece sobre --profile', output)
        self.assertIn('Perfiles legacy', output)

    def test_runtime_limitation_requires_details(self):
        state = self.fixture()
        state.write_text(state.read_text().replace('**Runtime limitation:** none', '**Runtime limitation:** tool-failure'))
        self.assertIn('sin causa/evidencia', self.run_script('doctor', '--project', str(self.project), ok=False).stdout)
        state.write_text(state.read_text() + '- **Runtime limitation detail:** herramienta caída; pendiente S05, reintentar lectura\n')
        self.run_script('doctor', '--project', str(self.project))

    def test_new_project_has_guardrails_and_version(self):
        self.run_script('init-project')
        agents = (self.project / 'AGENTS.md').read_text()
        current = json.loads((ROOT / 'MANIFEST.json').read_text())['version']
        for marker in ('Finalization Gate', 'Guided Mode', 'Factory version: ' + current, 'Conversation Recap'):
            self.assertIn(marker, agents)
        self.assertIn('Runtime limitation', (self.project / 'PROJECT_STATE.md').read_text())

    def test_managed_global_block_is_compact(self):
        self.run_script('install')
        self.assertLess(len(self.agents.read_bytes()), 3000)
        self.assertIn('Finalization Gate', self.agents.read_text())

    def test_routing_policy_reaches_installed_skill_and_new_project(self):
        self.run_script('install')
        self.run_script('init-project')
        installed = self.home / '.agents/skills/model-router/SKILL.md'
        self.assertEqual(installed.resolve(), ROOT / 'skills/core/model-router/SKILL.md')
        for path in (self.agents, installed, self.project / 'AGENTS.md'):
            with self.subTest(path=path.name):
                self.assertIn('routing-v1', path.read_text())
        # Installed relative policy link must resolve to the canonical catalog.
        self.assertTrue((installed.resolve().parent / '../../../config/MODEL_CATALOG.md').resolve().is_file())
        agents = (self.project / 'AGENTS.md').read_text()
        self.assertIn('obligatoriamente', agents)
        self.assertIn('referencia vigente', agents)

    def test_routing_adoption_preserves_local_instructions(self):
        existing = '# Local rules\nPreserve project-specific decisions.\n'
        self.put(self.project / 'AGENTS.md', existing)
        self.run_script('adopt-project')
        self.assertEqual((self.project / 'AGENTS.md').read_text(), existing)
        snippet = self.project / 'docs/AI_SOFTWARE_FACTORY_AGENTS_SNIPPET.md'
        self.assertIn('model-router / routing-v1', snippet.read_text())
        self.assertIn('referencia vigente', snippet.read_text())
        before = snapshot(self.project)
        self.run_script('adopt-project')
        self.assertEqual(before, snapshot(self.project))

    def test_catalog_pairs_match_profiles_and_actual_launcher_arguments(self):
        # Compare independent shipped artifacts, not unordered model/effort substrings.
        catalog = (ROOT / 'config/MODEL_CATALOG.md').read_text()
        rows = re.findall(
            r'^\| (ECONOMICAL|BALANCED|ADVANCED|Exceptional Override) \| '
            r'\*\*[^|]+\*\* \| `([^`]+)` \| (Low|Medium|High)(?: o XHigh)? \|',
            catalog, re.MULTILINE)
        self.assertEqual(len(rows), 4)
        self.assertEqual(len({label for label, _, _ in rows}), 4)
        capture = self.mock_capture()
        for label, model, effort in rows:
            profile = 'exceptional' if label == 'Exceptional Override' else label.lower()
            with self.subTest(profile=profile):
                data = tomllib.loads((ROOT / f'config/codex-profiles/asf-{profile}.config.toml').read_text())
                self.assertEqual((data['model'], data['model_reasoning_effort']), (model, effort.lower()))
                self.run_script('asf', profile, '--', 'Routing fixture; no inference.')
                self.assertEqual(json.loads(capture.read_text()),
                                 ['--model', model, '--config',
                                  f'model_reasoning_effort="{effort.lower()}"',
                                  '--', 'Routing fixture; no inference.'])

    def test_release_checks(self):
        self.run_script('check-release')


if __name__ == '__main__':
    unittest.main()
