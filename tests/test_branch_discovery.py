"""Synthetic offline coverage for branch-aware Git discovery."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/lib"))

from branch_discovery import (  # noqa: E402
    DiscoveryError,
    build_context,
    build_inventory,
    compare,
    open_repository,
    validate_context,
)


class BranchDiscovery(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="branch discovery ")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.repo = self.base / "variant repo"
        self.repo.mkdir()
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Variant Test")
        self.git("config", "user.email", "variant@example.invalid")
        (self.repo / "src").mkdir()
        (self.repo / "src/shared.ts").write_text("export const shared = 1;\n")
        (self.repo / "src/main.ts").write_text("export const client = 'base';\n")
        (self.repo / "package.json").write_text(json.dumps({
            "name": "synthetic-app",
            "dependencies": {"@angular/core": "^14.3.0", "@capacitor/core": "^6.0.0"},
        }) + "\n")
        self.git("add", ".")
        self.git("commit", "-qm", "base")
        base = self.git("rev-parse", "HEAD", text=True).strip()
        self.git("branch", "client-a")
        self.git("update-ref", "refs/remotes/origin/main", base)
        self.git("update-ref", "refs/remotes/origin/client-remote", base)
        self.git("symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
        self.git("checkout", "-qb", "client-b")
        (self.repo / "src/main.ts").write_text("export const client = 'b';\n")
        (self.repo / "src/line\nbreak.ts").write_text("export const odd = true;\n")
        self.git("add", ".")
        self.git("commit", "-qm", "client b")
        self.git("checkout", "-q", "main")

    def git(self, *args, text=False):
        result = subprocess.run(
            ["git", *args], cwd=self.repo, env=self.env, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        return result.stdout.decode() if text else result.stdout

    def state(self):
        return {
            "head": self.git("rev-parse", "HEAD"),
            "refs": self.git("for-each-ref", "--format=%(refname)%00%(objectname)%00%(symref)%00%(upstream)%00", "refs/heads", "refs/remotes"),
            "status": self.git("status", "--porcelain=v1", "-z", "--untracked-files=all"),
            "index": hashlib.sha256((self.repo / ".git/index").read_bytes()).hexdigest(),
        }

    def cli(self, *args, ok=True):
        result = subprocess.run(
            ["bash", str(ROOT / "scripts/discover-variants.sh"), *map(str, args)],
            cwd=ROOT, env=self.env, capture_output=True, text=True, timeout=30,
        )
        if ok:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def test_inspect_preserves_repository_and_reports_all_refs(self):
        before = self.state()
        output = self.base / "analysis output"
        self.cli("inspect", "--repo", self.repo, "--output", output)
        self.assertEqual(before, self.state())
        inventory = json.loads((output / "BRANCH_INVENTORY.json").read_text())
        matrix = json.loads((output / "VARIANTS.json").read_text())
        self.assertEqual(inventory["coverage"]["refs_total"], 5)
        self.assertEqual(inventory["coverage"]["refs_symbolic"], 1)
        self.assertEqual(inventory["coverage"]["inventory"], "complete")
        self.assertEqual(len(matrix["variants"]), 5)
        self.assertTrue(all(item["dimensions"]["client"]["status"] == "unknown" for item in matrix["variants"]))
        self.assertLess(inventory["deduplication"]["unique_blob_oids"], inventory["deduplication"]["blob_occurrences"])
        self.assertIn("Client, channel and activity: unknown", (output / "REPOSITORY_MAP.md").read_text())

    def test_output_inside_repository_is_rejected_without_side_effect(self):
        before = self.state()
        result = self.cli("inspect", "--repo", self.repo, "--output", self.repo / "analysis", ok=False)
        self.assertIn("fuera", result.stderr)
        self.assertFalse((self.repo / "analysis").exists())
        self.assertEqual(before, self.state())

        real = self.base / "real output"
        real.mkdir()
        linked = self.base / "linked output"
        linked.symlink_to(real, target_is_directory=True)
        result = self.cli("inspect", "--repo", self.repo, "--output", linked, ok=False)
        self.assertIn("symlinks", result.stderr)

    def test_compare_requires_full_refs_and_reports_exact_tip_delta(self):
        repository = open_repository(self.repo)
        result = compare(repository, "refs/heads/main", "refs/heads/client-b")
        self.assertEqual(result["changed_paths"], 2)
        self.assertEqual(result["rename_detection"], "not-run")
        self.assertEqual(len(result["merge_bases"]), 1)
        self.assertTrue(any(item["path"] == "src/line\nbreak.ts" for item in result["changes"]))
        with self.assertRaisesRegex(DiscoveryError, "ref completa"):
            compare(repository, "main", "refs/heads/client-b")

    def test_compare_preserves_multiple_merge_bases(self):
        base = self.git("rev-parse", "refs/heads/main", text=True).strip()
        left = self.git("rev-parse", "refs/heads/client-b", text=True).strip()
        self.git("checkout", "-qb", "right-base", base)
        (self.repo / "src/right.ts").write_text("export const right = 1;\n")
        self.git("add", ".")
        self.git("commit", "-qm", "right")
        right = self.git("rev-parse", "HEAD", text=True).strip()

        def commit_tree(tree, *parents):
            command = ["git", "commit-tree", tree]
            for parent in parents:
                command.extend(["-p", parent])
            return subprocess.run(
                command, cwd=self.repo, env=self.env, check=True, input=b"synthetic merge\n",
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            ).stdout.decode().strip()

        left_tree = self.git("rev-parse", f"{left}^{{tree}}", text=True).strip()
        right_tree = self.git("rev-parse", f"{right}^{{tree}}", text=True).strip()
        merge_left = commit_tree(left_tree, left, right)
        merge_right = commit_tree(right_tree, right, left)
        self.git("update-ref", "refs/heads/criss-left", merge_left)
        self.git("update-ref", "refs/heads/criss-right", merge_right)
        result = compare(open_repository(self.repo), "refs/heads/criss-left", "refs/heads/criss-right")
        self.assertEqual(set(result["merge_bases"]), {left, right})

    def test_context_has_provenance_budget_and_stale_overlay_guard(self):
        repository = open_repository(self.repo)
        task = {
            "objective": "inspect explicit files",
            "paths": ["src/main.ts", "src/shared.ts", "missing.ts"],
            "required_paths": ["src/main.ts"],
            "max_bytes": 2048,
        }
        manifest = build_context(repository, "refs/heads/main", task)
        self.assertEqual(manifest["coverage"], "partial")
        self.assertEqual(manifest["missing_optional_paths"], ["missing.ts"])
        self.assertTrue(all(item["blob_oid"] for item in manifest["entries"]))
        validate_context(repository, manifest)
        (self.repo / "untracked note.txt").write_text("scope changed\n")
        with self.assertRaisesRegex(DiscoveryError, "overlay"):
            validate_context(repository, manifest)

    def test_context_detects_ref_move_and_tampering(self):
        repository = open_repository(self.repo)
        task = {"objective": "one file", "paths": ["src/main.ts"], "required_paths": ["src/main.ts"], "max_bytes": 1024}
        manifest = build_context(repository, "refs/heads/main", task)
        tampered = json.loads(json.dumps(manifest))
        tampered["entries"][0]["text"] += "tampered"
        with self.assertRaisesRegex(DiscoveryError, "Integridad"):
            validate_context(repository, tampered)
        self.git("update-ref", "refs/heads/main", self.git("rev-parse", "refs/heads/client-b", text=True).strip())
        with self.assertRaisesRegex(DiscoveryError, "ref objetivo"):
            validate_context(repository, manifest)

    def test_context_rejects_secret_symlink_binary_and_budget(self):
        (self.repo / ".env").write_text("TOKEN=not-a-real-secret\n")
        (self.repo / "src/secret.ts").write_text('const api_key = "synthetic";\n')
        (self.repo / "src/binary.bin").write_bytes(b"\xff\x00")
        (self.repo / "src/link.ts").symlink_to("main.ts")
        self.git("add", ".env", "src/secret.ts", "src/binary.bin", "src/link.ts")
        self.git("commit", "-qm", "unsafe fixtures")
        repository = open_repository(self.repo)
        base = {"objective": "reject", "required_paths": [], "max_bytes": 1024}
        cases = [
            (".env", "sensible"),
            ("src/secret.ts", "sensible"),
            ("src/binary.bin", "UTF-8"),
            ("src/link.ts", "no regular"),
        ]
        for path, message in cases:
            with self.subTest(path=path):
                with self.assertRaisesRegex(DiscoveryError, message):
                    build_context(repository, "refs/heads/main", dict(base, paths=[path], required_paths=[path]))
        with self.assertRaisesRegex(DiscoveryError, "Presupuesto"):
            build_context(repository, "refs/heads/main", dict(base, paths=["src/main.ts"], required_paths=["src/main.ts"], max_bytes=1))

    def test_context_cli_and_check_fail_closed(self):
        task = self.base / "task.json"
        task.write_text(json.dumps({
            "objective": "cli round trip", "paths": ["src/main.ts"],
            "required_paths": ["src/main.ts"], "max_bytes": 1024,
        }))
        output = self.base / "context output"
        self.cli("context", "--repo", self.repo, "--target", "refs/heads/main", "--task", task, "--output", output)
        manifest = output / "CONTEXT_MANIFEST.json"
        result = self.cli("check", "--repo", self.repo, "--manifest", manifest)
        self.assertIn("Context PASS", result.stdout)
        value = json.loads(manifest.read_text())
        value["extra"] = True
        manifest.write_text(json.dumps(value))
        self.assertIn("fuera del contrato", self.cli("check", "--repo", self.repo, "--manifest", manifest, ok=False).stderr)

    def test_empty_bare_detached_and_partial_metadata_are_explicit(self):
        empty = self.base / "empty"
        empty.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=empty, env=self.env, check=True)
        inventory, matrix, _, stale = build_inventory(open_repository(empty))
        self.assertFalse(stale)
        self.assertEqual(inventory["coverage"]["refs_total"], 0)
        self.assertEqual(matrix["variants"], [])

        self.git("checkout", "--detach", "-q")
        detached, _, _, _ = build_inventory(open_repository(self.repo))
        self.assertIsNone(detached["overlay"]["head_ref"])
        bare = self.base / "bare.git"
        subprocess.run(["git", "clone", "-q", "--bare", str(self.repo), str(bare)], env=self.env, check=True)
        bare_inventory, _, _, _ = build_inventory(open_repository(bare))
        self.assertTrue(bare_inventory["repository"]["bare"])
        self.assertEqual(bare_inventory["overlay"]["applicability"], "not-applicable-bare")

        self.git("config", "extensions.partialClone", "origin")
        with self.assertRaisesRegex(DiscoveryError, "Clones parciales"):
            open_repository(self.repo)

    def test_missing_object_becomes_partial_coverage(self):
        oid = self.git("rev-parse", "refs/heads/client-b:src/line\nbreak.ts", text=True).strip()
        loose = self.repo / ".git/objects" / oid[:2] / oid[2:]
        self.assertTrue(loose.is_file())
        loose.unlink()
        inventory, _, _, stale = build_inventory(open_repository(self.repo))
        self.assertFalse(stale)
        self.assertEqual(inventory["coverage"]["inventory"], "partial")
        self.assertLess(inventory["coverage"]["tips_read"], inventory["coverage"]["tips_distinct"])
        self.assertTrue(any("Objeto Git faltante" in item["error"] for item in inventory["errors"]))


if __name__ == "__main__":
    unittest.main()
