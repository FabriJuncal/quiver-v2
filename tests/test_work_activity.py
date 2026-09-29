"""A01-A03 artificial fixtures. No real session, Kev server, or source is opened."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("plan_usage_activity", ROOT / "scripts/lib/plan_usage.py")
plan_usage = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(plan_usage)
import work_activity
SPEC_DATASET = importlib.util.spec_from_file_location("work_activity_kev_dataset", ROOT / "tests/work_activity_kev_dataset.py")
work_activity_kev_dataset = importlib.util.module_from_spec(SPEC_DATASET)
assert SPEC_DATASET.loader
SPEC_DATASET.loader.exec_module(work_activity_kev_dataset)


def line(value):
    return json.dumps(value, separators=(",", ":")) + "\n"


def session_meta(session):
    return {"type": "session_meta", "payload": {"id": session, "cli_version": "0.156.1"}}


def token(response, *, session, thread, root, amount=130):
    usage = {"input_tokens": amount - 30, "cached_input_tokens": 60,
             "output_tokens": 30, "reasoning_output_tokens": 20,
             "cache_write_input_tokens": 0, "total_tokens": amount}
    return {"type": "token_usage_record", "payload": {
        "response_id": response, "session_id": session, "thread_id": thread,
        "root_turn_id": root, "turn_id": "turn-" + response, "usage": usage,
        "turn_token_usage": dict(usage), "thread_token_usage": dict(usage)}}


class WorkActivity(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="activity fixtures ")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.project = self.base / "project"
        self.project.mkdir()
        self.private = self.base / "private"
        self.private.mkdir(mode=0o700)
        self.ledger = self.private / "usage.json"
        self.sources = {}

    def bind(self, number=1, *, project="project-a", work="work-a"):
        session = f"session-{number}"
        source = self.private / f"fixture-{number}.jsonl"
        source.write_text(line(session_meta(session)))
        self.sources[number] = source
        return plan_usage.bind(
            ledger_path=self.ledger, project_root=self.project, project_id=project,
            requirement_ref="docs/requirements/example/STATE.md", plan_version="v2",
            plan_digest="a" * 64, execution_id=f"execution-{number}",
            attempt_id=f"attempt-{number}", slice_id="A01", source_path=source,
            source_version="0.156.1", session_id=session, thread_id=f"thread-{number}",
            root_turn_id=f"root-{number}", work_id=work, activity_mode=True)

    def response(self, number, response="response-1", amount=130):
        with self.sources[number].open("a") as stream:
            stream.write(line(token(response, session=f"session-{number}",
                                    thread=f"thread-{number}", root=f"root-{number}", amount=amount)))

    def refresh(self, binding):
        return plan_usage.refresh(ledger_path=self.ledger, project_root=self.project,
                                  binding_id=binding)

    def receipt(self, activity, response="response-1", actions=None, complete=True,
                start="2026-09-25T10:00:00Z", end="2026-09-25T10:00:05Z", outcome="completed"):
        return {"activity_id": activity, "operation_id": "op-" + activity,
                "response_id": response, "actions": actions or [{"kind": "code", "file_roles": ["source"]}],
                "manifest_complete": complete, "started_at": start, "ended_at": end,
                "outcome": outcome, "tool_seconds": 2.0}

    def record(self, binding, receipt, classification=None):
        return plan_usage.record_activity(ledger_path=self.ledger, project_root=self.project,
                                          binding_id=binding, receipt=receipt,
                                          classification=classification)

    def snapshot(self, binding):
        return plan_usage.snapshot_activity_report(ledger_path=self.ledger,
                                                   project_root=self.project,
                                                   binding_id=binding)

    def history(self, project="project-a"):
        return plan_usage.activity_history_report(ledger_path=self.ledger,
                                                  project_root=self.project,
                                                  project_id=project)

    def test_t01_t03_receipt_is_minimized_and_activity_binding_has_no_global_kind(self):
        binding = self.bind()
        self.assertEqual(plan_usage._read_json(self.ledger)["bindings"][binding]["work_kind"], None)
        self.response(1)
        self.refresh(binding)
        receipt = self.receipt("docs-1", actions=[{"kind": "documentation", "file_roles": ["guide"]}])
        self.assertEqual(self.record(binding, receipt), {"recorded": True})
        saved = self.ledger.read_text()
        self.assertNotIn("/private/secret.md", saved)
        self.assertNotIn("summary", saved)
        event = plan_usage._read_json(self.ledger)["activity_events"]["docs-1"]
        self.assertEqual(event["classification"]["kind"], "documentation")
        self.assertEqual(event["elapsed_seconds"], "5.000000")
        with self.assertRaisesRegex(plan_usage.UsageError, "recibo"):
            self.record(binding, {**receipt, "summary": "do not persist"})

    def test_t02_identity_and_manifest_coverage_are_required(self):
        binding = self.bind()
        self.response(1)
        self.refresh(binding)
        with self.assertRaisesRegex(plan_usage.UsageError, "no observado"):
            self.record(binding, self.receipt("missing", response="other-response"))
        self.record(binding, self.receipt("partial", complete=False))
        self.snapshot(binding)
        row = next(item for item in self.history()["categories"] if item["kind"] == "unassigned")
        self.assertEqual(row["usage"]["responses"], 1)
        self.assertEqual(row["usage"]["total_tokens"], 130)
        self.assertEqual(self.record(binding, self.receipt("partial", complete=False)), {"recorded": False})

    def test_t04_t09_mixed_response_is_counted_once_and_conciles(self):
        binding = self.bind()
        self.response(1, amount=170)
        self.refresh(binding)
        self.record(binding, self.receipt("feature", actions=[{"kind": "code", "file_roles": ["source"]}]),
                    {"signals": {"feature": .95, "bug": .01, "test": .01, "explanation": .01, "documentation": .01}})
        self.record(binding, self.receipt("docs", actions=[{"kind": "documentation", "file_roles": ["guide"]}]))
        self.snapshot(binding)
        report = self.history()
        rows = {row["kind"]: row for row in report["categories"]}
        self.assertEqual(rows["mixed"]["usage"]["responses"], 1)
        self.assertEqual(rows["mixed"]["usage"]["total_tokens"], 170)
        self.assertEqual(rows["feature"]["usage"]["responses"], 0)
        self.assertEqual(sum(row["usage"]["total_tokens"] for row in report["categories"]), 170)
        self.assertEqual(report["usage"]["total_tokens"], 170)

    def test_t05_project_isolation_and_v1_binding_remain_compatible(self):
        first = self.bind(1, project="project-a")
        second = self.bind(2, project="project-b")
        self.response(1)
        self.response(2)
        self.refresh(first)
        self.refresh(second)
        self.record(first, self.receipt("a"))
        self.record(second, self.receipt("b"))
        self.snapshot(first)
        self.snapshot(second)
        self.assertEqual(self.history("project-a")["usage"]["responses"], 1)
        self.assertEqual(self.history("project-b")["usage"]["responses"], 1)
        self.assertIn("activity_mode", plan_usage._read_json(self.ledger)["bindings"][first])

    def test_t06_t07_kev_indicators_abstain_or_mark_unvalidated(self):
        seen = {}
        def fake(body, port):
            seen["body"] = json.loads(body)
            seen["port"] = port
            return line({"answers": {kind: {"type": "noul", "noul": (.94 if kind == "feature" else .01)}
                                      for kind in work_activity.ACTIVITY_KINDS}})
        kev = work_activity.kev_classify(summary="Small code change", endpoint="http://127.0.0.1:8009", _transport=fake)
        classified = work_activity.classify(work_activity.normalize_receipt(self.receipt("classify")), kev)
        self.assertEqual(classified, {"kind": "feature", "provenance": "kev_inferred", "validation": "unvalidated"})
        self.assertEqual(seen["port"], 8009)
        self.assertNotIn("Small code change", json.dumps(kev))
        ambiguous = work_activity.classify(work_activity.normalize_receipt(self.receipt("ambiguous")),
            {"signals": {kind: .95 for kind in work_activity.ACTIVITY_KINDS}})
        self.assertEqual(ambiguous["kind"], "mixed")
        with self.assertRaisesRegex(work_activity.ActivityError, "malformada"):
            work_activity.kev_classify(summary="x", endpoint="http://127.0.0.1:8009",
                _transport=lambda _body, _port: b'{"answers":{"feature":{"type":"noul","noul":NaN}}}')

    def test_t07_t08_rejects_external_or_sensitive_transport_inputs(self):
        with self.assertRaisesRegex(work_activity.ActivityError, "local"):
            work_activity.kev_classify(summary="safe", endpoint="https://outside.example:8009", _transport=lambda *_: b"{}")
        with self.assertRaisesRegex(work_activity.ActivityError, "máximo"):
            work_activity.kev_classify(summary="x" * 513, endpoint="http://127.0.0.1:8009", _transport=lambda *_: b"{}")
        with self.assertRaisesRegex(work_activity.ActivityError, "incompleta"):
            work_activity.kev_classify(summary="safe", endpoint="http://127.0.0.1:8009", _transport=lambda *_: b'{"answers":{}}')

    def test_t10_time_unknown_active_unknown_and_stale_snapshot_visible(self):
        binding = self.bind()
        self.response(1)
        self.refresh(binding)
        self.record(binding, self.receipt("first", end="2026-09-25T10:00:10Z"))
        self.snapshot(binding)
        self.record(binding, self.receipt("second", actions=[{"kind": "test", "file_roles": ["test"]}]))
        stale = self.history()
        self.assertEqual(stale["stale_reports"], 1)
        self.assertIsNone(stale["active_time_seconds"])
        self.snapshot(binding)
        row = next(item for item in self.history()["categories"] if item["kind"] == "implementation_unspecified")
        self.assertEqual(row["known_elapsed_seconds"], "10.000000")

    def test_t11_usd_is_unknown_and_v1_synthetic_cost_never_enters_activity_history(self):
        binding = self.bind()
        self.response(1)
        self.refresh(binding)
        self.record(binding, self.receipt("code"))
        self.snapshot(binding)
        self.assertIsNone(self.history()["usd"]["amount"])
        self.assertEqual(self.history()["usd"]["provenance"], "unknown")

    def test_t12_cli_history_reads_ledger_only_after_source_is_removed(self):
        binding = self.bind()
        self.response(1)
        self.refresh(binding)
        self.record(binding, self.receipt("docs", actions=[{"kind": "documentation", "file_roles": ["guide"]}]))
        self.snapshot(binding)
        self.sources[1].unlink()
        command = [sys.executable, "-I", "-B", str(ROOT / "scripts/lib/plan_usage.py"),
                   "--project-root", str(self.project), "--ledger", str(self.ledger),
                   "activity-history", "--project-id", "project-a"]
        complete = subprocess.run(command + ["--format", "json"], check=True, capture_output=True, text=True)
        self.assertEqual(json.loads(complete.stdout), self.history())
        text = subprocess.run(command + ["--format", "text"], check=True, capture_output=True, text=True)
        self.assertIn("documentation: activities=1 responses=1 tokens=130", text.stdout)
        self.assertNotIn(str(self.sources[1]), complete.stdout)

    def test_t13_cli_record_accepts_only_minimized_receipt(self):
        binding = self.bind()
        self.response(1)
        self.refresh(binding)
        command = [sys.executable, "-I", "-B", str(ROOT / "scripts/lib/plan_usage.py"),
                   "--project-root", str(self.project), "--ledger", str(self.ledger),
                   "activity-record", "--binding-id", binding]
        receipt = self.receipt("cli-docs", actions=[{"kind": "documentation", "file_roles": ["guide"]}])
        done = subprocess.run(command, input=json.dumps(receipt), check=True,
                              capture_output=True, text=True)
        self.assertEqual(json.loads(done.stdout), {"recorded": True})
        bad = subprocess.run(command, input=json.dumps({**receipt, "summary": "SECRET_CANARY"}),
                             capture_output=True, text=True)
        self.assertEqual(bad.returncode, 2)
        self.assertNotIn("SECRET_CANARY", self.ledger.read_text())

    def test_a02_frozen_synthetic_dataset_contract_for_a04(self):
        development = work_activity_kev_dataset.development_cases()
        evaluation = work_activity_kev_dataset.evaluation_cases()
        self.assertEqual(len(development), 100)
        self.assertEqual(len(evaluation), 200)
        self.assertEqual(sum(item["family"] == "clear" for item in evaluation), 150)
        self.assertEqual(sum(item["family"] == "mixed" for item in evaluation), 25)
        self.assertEqual(sum(item["family"] == "insufficient" for item in evaluation), 25)
        self.assertEqual(len(work_activity_kev_dataset.digest(development)), 64)
        self.assertEqual(len(work_activity_kev_dataset.digest(evaluation)), 64)


if __name__ == "__main__":
    unittest.main()
