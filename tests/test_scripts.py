"""Filesystem regression tests. Never reads or changes the user's Codex config."""
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- AI-SOFTWARE-FACTORY:START -->'
END = '<!-- AI-SOFTWARE-FACTORY:END -->'


def snapshot(root):
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            value = ('link', os.readlink(path))
        elif path.is_file():
            value = ('file', hashlib.sha256(path.read_bytes()).hexdigest(), stat.S_IMODE(path.stat().st_mode))
        else:
            value = ('dir',)
        result[str(path.relative_to(root))] = value
    return result


class Scripts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='asf tests ')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.home = self.base / 'temporary home'
        self.home.mkdir()
        self.project = self.base / 'project with spaces'
        self.project.mkdir()
        # Only tests' child processes receive this isolated environment.
        self.env = dict(os.environ, HOME=str(self.home), CODEX_HOME=str(self.home / '.codex'))
        for key in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_CONFIG', 'GIT_CONFIG_GLOBAL'):
            self.env.pop(key, None)
        self.env['GIT_CONFIG_NOSYSTEM'] = '1'
        self.bin = self.base / 'bin'
        self.bin.mkdir()
        self.put(self.bin / 'codex', '#!/bin/sh\necho "codex-cli 0.155.1"\n', 0o755)
        self.env['PATH'] = str(self.bin) + os.pathsep + os.environ['PATH']
        self.agents = self.home / '.codex/AGENTS.md'

    def put(self, path, content, mode=None):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        if mode is not None:
            path.chmod(mode)

    def run_script(self, name, *args, ok=True, root=ROOT):
        proc = subprocess.run(['bash', str(root / 'scripts' / (name + '.sh')), *args],
                              cwd=self.project, env=self.env, capture_output=True, text=True, timeout=20)
        if ok:
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        else:
            self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return proc

    def test_shell_syntax_each_file(self):
        for path in ROOT.joinpath('scripts').rglob('*.sh'):
            with self.subTest(path=path.name):
                subprocess.run(['bash', '-n', str(path)], check=True)

    def test_manifest_matches_shipped_resources(self):
        manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
        self.assertEqual(manifest['version'], '2.2.2')
        self.assertIn('**Version:** ' + manifest['version'], (ROOT / 'FACTORY_VERSION.md').read_text())
        self.assertEqual(sorted(manifest['scripts']), sorted(p.name for p in (ROOT / 'scripts').glob('*.sh')))
        self.assertEqual(sorted(manifest['core_skills']),
                         sorted(p.parent.name for p in (ROOT / 'skills/core').glob('*/SKILL.md')))

    def test_release_archive_installable_without_historical_bundle(self):
        # A disposable Git repository tests packaging without staging the user's worktree.
        candidate = self.base / 'candidate'
        shutil.copytree(ROOT, candidate, ignore=shutil.ignore_patterns('.git', '__pycache__', '.DS_Store', '.agents', '.codex'))
        env = dict(self.env, GIT_CONFIG_GLOBAL=os.devnull)

        def git(*args):
            return subprocess.run(['git', *args], cwd=candidate, env=env, check=True,
                                  capture_output=True, timeout=20).stdout

        git('init', '-q')
        git('add', '.')
        git('-c', 'user.name=Factory test', '-c', 'user.email=test@example.invalid',
            '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Temporary packaging fixture')
        unpacked = self.base / 'release with spaces'
        with zipfile.ZipFile(io.BytesIO(git('archive', '--format=zip', 'HEAD'))) as archive:
            names = archive.namelist()
            self.assertFalse(any(name.startswith('docs/archive/') for name in names))
            self.assertFalse(any(name.endswith('.zip') for name in names))
            self.assertIn('scripts/install.sh', names)
            self.assertIn('scripts/asf', names)
            self.assertIn('.github/workflows/ci.yml', names)
            self.assertTrue((archive.getinfo('scripts/asf').external_attr >> 16) & 0o111)
            self.assertTrue((archive.getinfo('scripts/install.sh').external_attr >> 16) & 0o111,
                            'The release must preserve install.sh executable permissions')
            archive.extractall(unpacked)
        self.run_script('install', root=unpacked)
        self.run_script('configure-model-profiles', root=unpacked)
        self.run_script('doctor', root=unpacked)
        self.run_script('uninstall', root=unpacked)

    def test_full_lifecycle_and_idempotence(self):
        original = '# Personal\nKeep this.\n'
        self.put(self.agents, original, 0o600)
        config = self.home / '.codex/config.toml'
        self.put(config, 'model = "personal"\n')
        skill = self.home / '.agents/skills/foreign/SKILL.md'
        self.put(skill, '# Foreign\n')
        self.run_script('install')
        first = snapshot(self.home)
        self.run_script('install')
        self.assertEqual(snapshot(self.home), first)
        self.assertEqual(self.agents.read_text().count(START), 1)
        self.assertEqual(stat.S_IMODE(self.agents.stat().st_mode), 0o600)
        self.run_script('doctor')
        self.run_script('configure-model-profiles')
        self.run_script('doctor')
        self.run_script('uninstall')
        self.assertEqual(self.agents.read_text(), original)
        self.assertEqual(config.read_text(), 'model = "personal"\n')
        self.assertEqual(skill.read_text(), '# Foreign\n')
        self.assertEqual(sorted(p.name for p in skill.parent.parent.iterdir()), ['foreign'])
        self.assertEqual(len(list(config.parent.glob('asf-*.config.toml'))), 4)
        first = snapshot(self.home)
        self.run_script('uninstall')
        self.assertEqual(first, snapshot(self.home))

    def test_dry_runs_are_read_only(self):
        for name, args in [('install', []), ('uninstall', []), ('configure-model-profiles', ['--force']),
                           ('init-project', ['--git-init']), ('adopt-project', [])]:
            with self.subTest(script=name):
                before = snapshot(self.base)
                self.run_script(name, '--dry-run', *args)
                self.assertEqual(before, snapshot(self.base))

    def test_unknown_and_extra_args_rejected_before_writes(self):
        for name in ('install', 'uninstall', 'configure-model-profiles', 'init-project', 'adopt-project', 'doctor'):
            with self.subTest(script=name):
                before = snapshot(self.base)
                self.run_script(name, '--bogus', ok=False)
                self.run_script(name, '--dry-run', '--bogus', ok=False)
                self.assertEqual(before, snapshot(self.base))

    def test_malformed_markers_preserve_everything(self):
        blocks = [START + '\nprivate\n', END + '\nprivate\n', START + '\n' + START + '\n' + END + '\n',
                  START + '\n' + END + '\n' + START + '\n' + END + '\n', 'prefix ' + START + '\n']
        for block in blocks:
            self.put(self.agents, 'Before\n' + block + 'After\n')
            for name in ('install', 'uninstall'):
                with self.subTest(block=block, script=name):
                    before = snapshot(self.base)
                    self.run_script(name, ok=False)
                    self.assertEqual(before, snapshot(self.base))

    def test_nonterminated_personal_file_not_normalized(self):
        self.put(self.agents, 'No final newline')
        before = snapshot(self.base)
        self.run_script('install', ok=False)
        self.assertEqual(before, snapshot(self.base))

    def test_predictable_new_symlink_cannot_overwrite(self):
        victim = self.base / 'victim'
        self.put(victim, 'Preserve\n')
        self.agents.parent.mkdir()
        self.agents.with_name('AGENTS.md.new').symlink_to(victim)
        self.run_script('install')
        self.assertEqual(victim.read_text(), 'Preserve\n')
        self.assertFalse(self.agents.is_symlink())

    def test_agents_symlink_and_directory_rejected(self):
        victim = self.base / 'victim'
        self.put(victim, 'Preserve\n')
        self.agents.parent.mkdir()
        self.agents.symlink_to(victim)
        for name in ('install', 'uninstall'):
            self.run_script(name, ok=False)
        self.assertEqual(victim.read_text(), 'Preserve\n')
        self.agents.unlink()
        self.agents.mkdir()
        before = snapshot(self.base)
        self.run_script('install', ok=False)
        self.assertEqual(before, snapshot(self.base))

    def test_profiles_preserved_force_backup_unique(self):
        dest = self.home / '.codex/asf-balanced.config.toml'
        self.put(dest, 'model = "original"\n', 0o600)
        self.put(self.bin / 'date', '#!/bin/sh\necho 20000101-000000\n', 0o755)
        self.run_script('configure-model-profiles')
        self.assertEqual(dest.read_text(), 'model = "original"\n')
        self.run_script('configure-model-profiles', '--force')
        self.put(dest, 'model = "second"\n')
        self.run_script('configure-model-profiles', '--force')
        backups = list(dest.parent.glob(dest.name + '.backup-*'))
        self.assertEqual(len(backups), 2)
        self.assertEqual({b.read_text() for b in backups}, {'model = "original"\n', 'model = "second"\n'})
        self.assertEqual(stat.S_IMODE(dest.stat().st_mode), 0o600)

    def test_profiles_symlinks_regular_and_dangling_rejected(self):
        dest = self.home / '.codex/asf-balanced.config.toml'
        victim = self.base / 'victim'
        self.put(victim, 'Preserve\n')
        dest.parent.mkdir()
        dest.symlink_to(victim)
        before = snapshot(self.base)
        self.run_script('configure-model-profiles', '--force', ok=False)
        self.assertEqual(before, snapshot(self.base))
        victim.unlink()
        before = snapshot(self.base)
        self.run_script('configure-model-profiles', ok=False)
        self.assertEqual(before, snapshot(self.base))

    def test_override_detected_and_preserved(self):
        self.run_script('install')
        self.put(self.agents.with_name('AGENTS.override.md'), '# Personal override\n')
        before = snapshot(self.base)
        self.run_script('install', ok=False)
        self.run_script('doctor', ok=False)
        self.assertEqual(before, snapshot(self.base))

    def test_old_codex_rejected_by_doctor(self):
        self.run_script('install')
        self.put(self.bin / 'codex', '#!/bin/sh\necho "codex-cli 0.133.0"\n', 0o755)
        self.assertIn('0.134.0', self.run_script('doctor', ok=False).stdout)

    def test_failed_codex_version_is_explicitly_unverified(self):
        self.run_script('install')
        self.put(self.bin / 'codex', '#!/bin/sh\nexit 126\n', 0o755)
        output = self.run_script('doctor').stdout
        self.assertIn('Versión Codex NO VERIFICADA', output)
        self.assertIn('STATUS: OK WITH WARNINGS', output)

    def test_doctor_rejects_empty_resume_action(self):
        self.run_script('install')
        self.run_script('init-project')
        state = self.project / 'PROJECT_STATE.md'
        lines = state.read_text().splitlines()
        state.write_text('\n'.join('- **Next action:** ' if '**Next action:**' in line else line
                                   for line in lines) + '\n')
        output = self.run_script('doctor', '--project', str(self.project), ok=False).stdout
        self.assertIn('PROJECT_STATE sin Next action concreto', output)

    def test_doctor_invalid_toml_or_explicit_unverified(self):
        self.run_script('install')
        self.put(self.home / '.codex/asf-balanced.config.toml', 'model = [BROKEN\n')
        proc = subprocess.run(['bash', str(ROOT / 'scripts/doctor.sh')], cwd=self.project,
                              env=self.env, capture_output=True, text=True, timeout=20)
        if 'TOML NO VERIFICADO' in proc.stdout:
            self.assertIn('STATUS: OK WITH WARNINGS', proc.stdout)
        else:
            self.assertNotEqual(proc.returncode, 0, proc.stdout)
            self.assertIn('Perfil inválido', proc.stdout)

    def test_new_project_resume_state_and_repeat(self):
        self.run_script('init-project', '--git-init')
        for entry in ('AGENTS.md', 'PROJECT_PROFILE.md', 'PROJECT_STATE.md', 'CAPABILITY_MAP.md',
                      'docs/requirements', '.agents/skills', '.git'):
            self.assertTrue((self.project / entry).exists(), entry)
        self.assertIn('2.2.2', (self.project / 'PROJECT_PROFILE.md').read_text())
        self.assertIn('ejecutar Project Discovery', (self.project / 'PROJECT_STATE.md').read_text())
        before = snapshot(self.project)
        self.run_script('init-project', '--git-init')
        self.assertEqual(before, snapshot(self.project))

    def test_existing_project_preserves_source_and_docs(self):
        subprocess.run(['git', 'init', '-q'], cwd=self.project, env=self.env, check=True)
        for file, body in [('AGENTS.md', '# Existing rules\n'), ('src/app.js', 'export const n = 42;\n'),
                           ('docs/OWN.md', '# Own documentation\n')]:
            self.put(self.project / file, body)
        originals = snapshot(self.project)
        self.run_script('adopt-project')
        after = snapshot(self.project)
        for file, value in originals.items():
            self.assertEqual(after[file], value)
        self.assertTrue((self.project / 'docs/AI_SOFTWARE_FACTORY_AGENTS_SNIPPET.md').exists())
        self.run_script('adopt-project')
        self.assertEqual(after, snapshot(self.project))

    def test_scaffold_symlink_rejected_before_writes(self):
        foreign = self.base / 'foreign docs'
        foreign.mkdir()
        (self.project / 'docs').symlink_to(foreign, target_is_directory=True)
        for name in ('init-project', 'adopt-project'):
            before = snapshot(self.base)
            self.run_script(name, ok=False)
            self.assertEqual(before, snapshot(self.base))

    def test_foreign_skills_and_other_factory_block_retained(self):
        skill = self.home / '.agents/skills/model-router/SKILL.md'
        self.put(skill, '# Foreign skill\n')
        self.run_script('install')
        self.agents.write_text(self.agents.read_text().replace(str(ROOT), '/another/factory'))
        before = self.agents.read_bytes()
        self.run_script('uninstall')
        self.assertEqual(before, self.agents.read_bytes())
        self.assertEqual(skill.read_text(), '# Foreign skill\n')

    def test_install_failure_preserves_config(self):
        self.put(self.agents, '# Personal\n')
        self.put(self.home / '.agents/skills', 'Conflict\n')
        before = snapshot(self.base)
        self.run_script('install', ok=False)
        self.assertEqual(before, snapshot(self.base))


if __name__ == '__main__':
    unittest.main()
