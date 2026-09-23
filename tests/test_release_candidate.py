"""RC lifecycle and inactive helper checks; no live tools, model calls or agents."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest

import test_scripts as lifecycle

ROOT = lifecycle.ROOT


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts/lib' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReleaseCandidate(unittest.TestCase):
    setUp = lifecycle.Scripts.setUp
    put = lifecycle.Scripts.put
    run_script = lifecycle.Scripts.run_script

    def test_version_order_and_validation(self):
        key = load('runtime_doctor').version_key
        versions = ['2.2.2', '2.3.0-rc.1', '2.3.0-rc.2', '2.3.0-rc.10', '2.3.0', '2.3.1']
        self.assertEqual(sorted(reversed(versions), key=key), versions)
        for invalid in ('2.3', '2.3.0-rc', '2.3.0-rc.01', '02.3.0', '2.3.0-unknown'):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                key(invalid)

    def test_doctor_current_rc_and_newer_stable_no_downgrade(self):
        self.run_script('install')
        self.run_script('init-project')
        for version in ('2.3.0-rc.2', '2.3.0'):
            for name in ('AGENTS.md', 'PROJECT_PROFILE.md'):
                path = self.project / name
                path.write_text(path.read_text().replace('2.3.0-rc.2', version))
            before = lifecycle.snapshot(self.base)
            output = self.run_script('doctor', '--project', str(self.project)).stdout
            self.assertNotIn('LAYER OUTDATED', output)
            self.assertNotIn('LAYER UNKNOWN', output)
            if version == '2.3.0':
                self.assertIn('no hacer downgrade', output)
            self.assertEqual(before, lifecycle.snapshot(self.base))

    def test_upgrade_installed_layer_preserves_config_code_and_old_project(self):
        self.run_script('install')
        self.run_script('init-project', '--git-init')
        for path in (self.agents, self.project / 'AGENTS.md', self.project / 'PROJECT_PROFILE.md'):
            path.write_text(path.read_text().replace('2.3.0-rc.2', '2.2.2'))
        self.put(self.home / '.codex/config.toml', 'model = "user-choice"\n[agents]\nenabled = false\n')
        self.put(self.home / '.codex/asf-balanced.config.toml', 'model = "custom-profile"\n')
        self.put(self.project / 'src/app.txt', 'existing application\n')
        self.put(self.project / 'docs/decisions/approved.md', 'Approved decision\n')
        before_project = lifecycle.snapshot(self.project)
        before_config = (self.home / '.codex/config.toml').read_bytes()
        self.run_script('install', '--dry-run')
        self.run_script('install')
        self.run_script('install')
        self.run_script('configure-model-profiles')
        self.assertIn('Factory version: 2.3.0-rc.2', self.agents.read_text())
        self.assertEqual(before_project, lifecycle.snapshot(self.project))
        self.assertEqual(before_config, (self.home / '.codex/config.toml').read_bytes())
        self.assertEqual('model = "custom-profile"\n', (self.home / '.codex/asf-balanced.config.toml').read_text())
        self.assertFalse((self.home / '.codex/agents').exists())
        output = self.run_script('doctor', '--project', str(self.project)).stdout
        self.assertIn('PROJECT FACTORY LAYER OUTDATED', output)
        self.assertIn('UPGRADE_2_2_2_TO_2_3_0.md', output)

    def test_proposal_is_read_only_and_never_live_ready(self):
        directory = self.base / 'proposal with spaces'
        shutil.copytree(ROOT / 'config/assistant-proposal', directory)
        before = lifecycle.snapshot(self.base)
        result = subprocess.run([sys.executable, '-I', '-B', str(ROOT / 'scripts/lib/check_assistant_proposal.py'),
                                 '--directory', str(directory)], capture_output=True, text=True, env=self.env)
        self.assertEqual(result.returncode, 2, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data['static_result'], 'PASS')
        self.assertEqual(data['delegation'], 'DISABLED')
        self.assertEqual(data['pilot'], 'NOT RUN')
        self.assertEqual(before, lifecycle.snapshot(self.base))

    def test_proposal_rejects_activation_and_unknown_overrides(self):
        directory = self.base / 'proposal'
        shutil.copytree(ROOT / 'config/assistant-proposal', directory)
        validate = load('check_assistant_proposal').validate
        for filename in ('coordinator.toml', 'asf_helper.toml'):
            path = directory / filename
            original = path.read_text()
            mutations = [original.replace('enabled = false', 'enabled = true'),
                         original.replace('enabled = false', 'enabled = 0'),
                         original.replace('= 1', '= 2'),
                         original.replace('read-only', 'danger-full-access'),
                         original.replace('"never"', '"on-request"'),
                         original.replace('apps = false', 'apps = true'),
                         'model = "unexpected"\n' + original,
                         'default_permissions = ":read-only"\n' + original,
                         original + '\n[plugins.extra]\nenabled = true\n']
            for mutation in mutations:
                path.write_text(mutation)
                with self.subTest(filename=filename, mutation=mutation), self.assertRaises(ValueError):
                    validate(directory)
            path.write_text(original)
        validate(directory)

    def test_proposal_missing_and_symlink_rejected(self):
        directory = self.base / 'proposal'
        directory.mkdir()
        validate = load('check_assistant_proposal').validate
        with self.assertRaises(ValueError):
            validate(directory)
        (directory / 'coordinator.toml').symlink_to(ROOT / 'config/assistant-proposal/coordinator.toml')
        with self.assertRaises(ValueError):
            validate(directory)


if __name__ == '__main__':
    unittest.main()
