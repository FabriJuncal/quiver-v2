"""Real temporary filesystem tests, not real workers or isolation certification."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import test_scripts as lifecycle
sys.path.insert(0, str(lifecycle.ROOT / 'scripts/lib'))
from audit_workspace import AuditError, compare, inventory, load_document, validate_manifest


class WorkspaceAudit(unittest.TestCase):
    setUp = lifecycle.Scripts.setUp
    put = lifecycle.Scripts.put

    def initial(self):
        self.put(self.project / 'src/a.txt', 'base\n', 0o644)
        return inventory(self.project, 'attempt-1:copy')

    def test_m05_m23_clean_deterministic_read_only(self):
        before = self.initial()
        untouched = lifecycle.snapshot(self.base)
        after = inventory(self.project, 'attempt-1:copy')
        self.assertEqual(before, after)
        self.assertEqual(compare(before, after)['result'], 'clean')
        self.assertEqual(untouched, lifecycle.snapshot(self.base))

    def test_m06_add_modify_remove(self):
        before = self.initial()
        self.put(self.project / 'src/a.txt', 'new\n')
        self.put(self.project / 'new.txt', 'added\n')
        result = compare(before, inventory(self.project, 'attempt-1:copy'))
        self.assertEqual(result['changes'], [{'path': 'new.txt', 'change': 'added'}, {'path': 'src/a.txt', 'change': 'modified'}])
        (self.project / 'src/a.txt').unlink()
        self.assertIn({'path': 'src/a.txt', 'change': 'removed'}, compare(before, inventory(self.project, 'attempt-1:copy'))['changes'])

    def test_m07_permission_and_type_change(self):
        before = self.initial()
        (self.project / 'src/a.txt').chmod(0o600)
        self.assertEqual(compare(before, inventory(self.project, 'attempt-1:copy'))['result'], 'changed')
        (self.project / 'src/a.txt').unlink()
        (self.project / 'src/a.txt').mkdir()
        self.assertIn({'path': 'src/a.txt', 'change': 'modified'}, compare(before, inventory(self.project, 'attempt-1:copy'))['changes'])

    def test_m08_links_special_files_not_followed(self):
        outside = self.base / 'outside.txt'
        self.put(outside, 'SYNTHETIC OUTSIDE\n')
        target = self.project / 'link'
        target.symlink_to(outside)
        with self.assertRaises(AuditError):
            inventory(self.project, 'scope')
        target.unlink()
        os.link(outside, target)
        with self.assertRaises(AuditError):
            inventory(self.project, 'scope')
        target.unlink()
        os.mkfifo(target)
        with self.assertRaises(AuditError):
            inventory(self.project, 'scope')
        self.assertEqual(outside.read_text(), 'SYNTHETIC OUTSIDE\n')

    def test_root_symlink_rejected(self):
        target = self.base / 'root-link'
        target.symlink_to(self.project, target_is_directory=True)
        with self.assertRaises(AuditError):
            inventory(target, 'scope')

    def test_symlink_ancestor_of_root_or_document_rejected(self):
        self.initial()
        alias = self.base / 'alias'
        alias.symlink_to(self.project, target_is_directory=True)
        with self.assertRaises(AuditError):
            inventory(alias / 'src', 'scope')
        self.put(self.project / 'manifest.json', '{}')
        with self.assertRaises(AuditError):
            load_document(alias / 'manifest.json')

    def test_m08_bad_manifest_paths_and_types(self):
        original = self.initial()
        for value in ('../escape', '/absolute', 'src/../escape', 'src//a.txt', 'src\\a.txt', '', 'bad\x00'):
            manifest = copy.deepcopy(original)
            manifest['entries'][-1]['path'] = value
            with self.assertRaises(AuditError):
                validate_manifest(manifest)
        manifest = copy.deepcopy(original)
        manifest['entries'].append(manifest['entries'][-1])
        with self.assertRaises(AuditError):
            validate_manifest(manifest)
        for key, value in [('kind', 'symlink'), ('mode', True), ('sha256', 'bad'), ('size', -1)]:
            manifest = copy.deepcopy(original)
            manifest['entries'][-1][key] = value
            with self.assertRaises(AuditError):
                validate_manifest(manifest)

    def test_m09_unreadable_is_incomplete_not_clean(self):
        self.initial()
        with patch('audit_workspace.os.read', side_effect=PermissionError('simulated denial')):
            with self.assertRaises(AuditError):
                inventory(self.project, 'scope')

    def test_m09_change_while_reading_detected(self):
        self.initial()
        real_read = os.read
        modified = False
        def changing_read(fd, size):
            nonlocal modified
            data = real_read(fd, size)
            if not modified:
                modified = True
                self.put(self.project / 'src/a.txt', 'changed during read\n')
            return data
        with patch('audit_workspace.os.read', side_effect=changing_read):
            with self.assertRaises(AuditError):
                inventory(self.project, 'scope')

    def test_m10_transient_change_is_not_detectable_by_final_snapshot(self):
        before = self.initial()
        self.put(self.project / 'src/a.txt', 'transient\n')
        self.put(self.project / 'src/a.txt', 'base\n')
        self.assertEqual(compare(before, inventory(self.project, 'attempt-1:copy'))['result'], 'clean')

    def test_m11_original_not_restored_by_comparison(self):
        before = self.initial()
        self.put(self.project / 'src/a.txt', 'human change\n')
        result = compare(before, inventory(self.project, 'attempt-1:copy'))
        self.assertEqual(result['result'], 'changed')
        self.assertEqual((self.project / 'src/a.txt').read_text(), 'human change\n')

    def test_m21_inventory_is_not_a_secret_scanner(self):
        before = self.initial()
        self.put(self.project / 'innocent.txt', 'SYNTHETIC_SECRET_NOT_REAL\n')
        after = inventory(self.project, 'attempt-1:copy')
        self.assertEqual(compare(before, after)['result'], 'changed')
        self.assertNotIn('SYNTHETIC_SECRET_NOT_REAL', json.dumps(after))
        self.assertIn('innocent.txt', [e['path'] for e in after['entries']])

    def test_m22_different_scope_malformed_json_rejected(self):
        before = self.initial()
        after = copy.deepcopy(before)
        after['scope_id'] = 'wrong'
        with self.assertRaises(AuditError):
            compare(before, after)
        path = self.base / 'duplicate.json'
        self.put(path, '{"x":1,"x":2}')
        with self.assertRaises(AuditError):
            load_document(path)

    def test_m23_cli_spaces_codes_and_no_writes(self):
        before = self.initial()
        before_file = self.base / 'before.json'
        after_file = self.base / 'after.json'
        self.put(before_file, json.dumps(before))
        self.put(self.project / 'src/a.txt', 'new\n')
        self.put(after_file, json.dumps(inventory(self.project, 'attempt-1:copy')))
        untouched = lifecycle.snapshot(self.base)
        command = [sys.executable, '-I', '-B', str(lifecycle.ROOT / 'scripts/lib/audit_workspace.py')]
        for _ in range(2):
            result = subprocess.run(command + ['snapshot', '--root', str(self.project), '--scope-id', 'attempt-1:copy'], env=self.env, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('NO VERIFICADOS', result.stderr)
            result = subprocess.run(command + ['compare', '--before', str(before_file), '--after', str(after_file)], env=self.env, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(json.loads(result.stdout)['result'], 'changed')
        self.assertEqual(untouched, lifecycle.snapshot(self.base))
        self.put(after_file, '{}')
        result = subprocess.run(command + ['compare', '--before', str(before_file), '--after', str(after_file)], env=self.env, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 1)


if __name__ == '__main__':
    unittest.main()
