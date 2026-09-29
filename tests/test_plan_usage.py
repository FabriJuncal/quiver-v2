"""S01 offline tests. All rollout fixtures are synthetic and private temporary files."""
from __future__ import annotations

import fcntl
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("plan_usage", ROOT / "scripts/lib/plan_usage.py")
plan_usage = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(plan_usage)


def line(value):
    return json.dumps(value, separators=(",", ":")) + "\n"


def session_meta(session="session-1"):
    return {"timestamp": "2026-09-24T00:00:00Z", "type": "session_meta", "ordinal": 0,
            "payload": {"id": session, "cli_version": "0.156.1"}}


def token_record(response="response-1", *, session="session-1", thread="thread-1",
                 root="root-1", turn="turn-1", input_tokens=100, cached=60,
                 output=30, reasoning=20, cache_write=0, extra=None):
    usage = {"input_tokens": input_tokens, "cached_input_tokens": cached,
             "output_tokens": output, "reasoning_output_tokens": reasoning,
             "cache_write_input_tokens": cache_write,
             "total_tokens": input_tokens + output}
    payload = {"response_id": response, "session_id": session, "thread_id": thread,
               "root_turn_id": root, "turn_id": turn, "usage": usage,
               "turn_token_usage": dict(usage), "thread_token_usage": dict(usage)}
    if extra:
        payload.update(extra)
    return {"timestamp": "2026-09-24T00:00:01Z", "type": "token_usage_record",
            "ordinal": 1, "payload": payload}


class PlanUsage(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="plan usage tests ")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.project = self.base / "project"
        self.project.mkdir()
        self.private = self.base / "private"
        self.private.mkdir(mode=0o700)
        self.ledger = self.private / "usage.json"
        self.source = self.private / "rollout.jsonl"
        self.source.write_text(line(session_meta()))

    def append(self, value):
        with self.source.open("a") as stream:
            stream.write(line(value) if not isinstance(value, str) else value)

    def bind(self, **changes):
        values = dict(ledger_path=self.ledger, project_root=self.project,
                      project_id="project-1", requirement_ref="docs/requirements/example/STATE.md",
                      plan_version="v1", plan_digest="a" * 64, execution_id="execution-1",
                      attempt_id="attempt-1", slice_id="S01", source_path=self.source,
                      source_version="0.156.1", session_id="session-1",
                      thread_id="thread-1", root_turn_id="root-1")
        values.update(changes)
        return plan_usage.bind(**values)

    def refresh(self, binding, **changes):
        return plan_usage.refresh(ledger_path=self.ledger, project_root=self.project,
                                  binding_id=binding, **changes)

    def report(self, binding):
        return plan_usage.report(ledger_path=self.ledger, project_root=self.project,
                                 binding_id=binding)

    def test_simple_semantics_report_and_privacy(self):
        binding = self.bind()
        self.append(token_record(cache_write=5,
                                 extra={"prompt": "SECRET_CANARY", "tool_args": "PRIVATE"}))
        original = self.source.read_bytes()
        self.assertEqual(self.refresh(binding), {"imported": 1, "duplicates": 0, "excluded": 0})
        self.assertEqual(self.source.read_bytes(), original)
        report = self.report(binding)
        self.assertEqual(report["usage"], {"responses": 1, "input_tokens": 100,
            "cached_input_tokens": 60, "output_tokens": 30,
            "reasoning_output_tokens": 20, "cache_write_input_tokens": 5,
            "total_tokens": 130})
        self.assertEqual(report["data_state"], "incomplete")
        self.assertEqual(report["anomalies"], [{"kind": "cache_write_semantics_unqualified"}])
        self.assertIn("usd", report["unknowns"])
        persisted = self.ledger.read_text()
        self.assertNotIn("SECRET_CANARY", persisted)
        self.assertNotIn("PRIVATE", persisted)
        self.assertNotIn(str(self.source), json.dumps(report))
        self.assertIn("Tokens: input=100", plan_usage.render_text(report))

    def test_baseline_excluded_and_reimport_is_idempotent(self):
        self.append(token_record("before-binding"))
        binding = self.bind()
        event = token_record("after-binding")
        self.append(event)
        self.append(event)
        result = self.refresh(binding)
        self.assertEqual(result, {"imported": 1, "duplicates": 1, "excluded": 0})
        self.assertEqual(self.refresh(binding)["imported"], 0)
        self.assertEqual(self.report(binding)["usage"]["responses"], 1)

    def test_conflicting_response_id_is_incomplete(self):
        binding = self.bind()
        self.append(token_record("same"))
        self.append(token_record("same", input_tokens=110, cached=60, output=30))
        result = self.refresh(binding)
        self.assertEqual((result["imported"], result["excluded"]), (1, 1))
        report = self.report(binding)
        self.assertEqual(report["usage"]["responses"], 1)
        self.assertEqual(report["data_state"], "incomplete")
        self.assertEqual(report["anomalies"][0]["kind"], "conflicting_response_id")

    def test_session_cannot_be_shared_between_plans(self):
        self.bind()
        other = self.private / "other.jsonl"
        other.write_text(line(session_meta()))
        with self.assertRaisesRegex(plan_usage.UsageError, "sesión ya vinculada"):
            self.bind(source_path=other, execution_id="execution-2", attempt_id="attempt-2")

    def test_two_plans_do_not_cross(self):
        first = self.bind()
        other = self.private / "other.jsonl"
        other.write_text(line(session_meta("session-2")))
        second = self.bind(source_path=other, execution_id="execution-2", attempt_id="attempt-2",
                           session_id="session-2", thread_id="thread-2", root_turn_id="root-2")
        self.append(token_record("first"))
        with other.open("a") as stream:
            stream.write(line(token_record("second", session="session-2", thread="thread-2", root="root-2")))
        self.refresh(first)
        self.refresh(second)
        self.assertEqual(self.report(first)["usage"]["responses"], 1)
        self.assertEqual(self.report(second)["usage"]["responses"], 1)

    def test_partial_line_waits_for_completion(self):
        binding = self.bind()
        raw = line(token_record()).encode()
        split = len(raw) // 2
        with self.source.open("ab") as stream:
            stream.write(raw[:split])
        self.assertEqual(self.refresh(binding)["imported"], 0)
        with self.source.open("ab") as stream:
            stream.write(raw[split:])
        self.assertEqual(self.refresh(binding)["imported"], 1)

    def test_malformed_allowed_record_is_sanitized_anomaly(self):
        binding = self.bind()
        self.append('{"type":"token_usage_record",broken SECRET_CANARY}\n')
        result = self.refresh(binding)
        self.assertEqual(result["excluded"], 1)
        persisted = self.ledger.read_text()
        self.assertNotIn("SECRET_CANARY", persisted)
        self.assertIn("malformado", persisted)

    def test_truncation_and_unknown_version_fail_closed(self):
        binding = self.bind()
        self.source.write_text("")
        with self.assertRaisesRegex(plan_usage.UsageError, "truncada"):
            self.refresh(binding)
        other = self.private / "unknown.jsonl"
        other.write_text(line(session_meta()))
        with self.assertRaisesRegex(plan_usage.UsageError, "versión"):
            self.bind(source_path=other, execution_id="e2", attempt_id="a2",
                      session_id="s2", thread_id="t2", root_turn_id="r2",
                      source_version="0.999.0")

    def test_session_meta_must_match_declared_binding(self):
        with self.assertRaisesRegex(plan_usage.UsageError, "session_meta"):
            self.bind(session_id="different-session")

    def test_report_matches_schema_surface(self):
        binding = self.bind()
        self.append(token_record())
        self.refresh(binding)
        report = self.report(binding)
        schema = json.loads((ROOT / "templates/usage/MEASUREMENT.v1.schema.json").read_text())
        self.assertEqual(set(report), set(schema["required"]))
        self.assertEqual(set(report["binding"]), set(schema["properties"]["binding"]["required"]))
        self.assertEqual(set(report["usage"]), set(schema["properties"]["usage"]["required"]))

    def test_child_or_fork_is_excluded(self):
        binding = self.bind()
        self.append(token_record("child", thread="thread-child", root="root-child"))
        result = self.refresh(binding)
        self.assertEqual(result, {"imported": 0, "duplicates": 0, "excluded": 1})
        self.assertEqual(self.report(binding)["data_state"], "incomplete")

    def test_s03_successive_root_turns_same_thread_are_counted_when_opted_in(self):
        binding = self.bind(slice_id="S03", allow_root_turn_change=True)
        self.append(token_record("binding-turn", root="root-1", turn="turn-1"))
        self.append(token_record("next-turn", root="root-2", turn="turn-2"))
        self.assertEqual(self.refresh(binding)["imported"], 1)
        self.assertEqual(self.report(binding)["usage"]["responses"], 1)

    def test_s03_child_thread_remains_excluded_with_root_turn_opt_in(self):
        binding = self.bind(slice_id="S03", allow_root_turn_change=True)
        self.append(token_record("child", thread="thread-child", root="root-2"))
        self.assertEqual(self.refresh(binding)["excluded"], 1)
        self.assertEqual(self.report(binding)["usage"]["responses"], 0)

    def test_disable_does_not_read_source(self):
        binding = self.bind()
        plan_usage.disable(ledger_path=self.ledger, project_root=self.project, binding_id=binding)
        self.source.unlink()
        self.assertEqual(self.refresh(binding), {"imported": 0, "duplicates": 0, "excluded": 0})

    def test_private_paths_and_symlinks_are_rejected(self):
        inside = self.project / "usage.json"
        with self.assertRaisesRegex(plan_usage.UsageError, "fuera del worktree"):
            self.bind(ledger_path=inside)
        victim = self.private / "victim.jsonl"
        victim.write_text(line(session_meta()))
        linked = self.private / "linked.jsonl"
        linked.symlink_to(victim)
        with self.assertRaisesRegex(plan_usage.UsageError, "regular"):
            self.bind(source_path=linked)
        real_parent = self.base / "real-parent"
        real_parent.mkdir()
        ancestor_link = self.base / "linked-parent"
        ancestor_link.symlink_to(real_parent, target_is_directory=True)
        nested = ancestor_link / "source.jsonl"
        nested.write_text(line(session_meta()))
        with self.assertRaisesRegex(plan_usage.UsageError, "atravesar symlinks"):
            self.bind(source_path=nested)

    def test_duplicate_json_keys_and_noncanonical_ref_fail_closed(self):
        binding = self.bind()
        self.append('{"type":"token_usage_record","type":"token_usage_record","payload":{}}\n')
        result = self.refresh(binding)
        self.assertEqual(result["excluded"], 1)
        self.assertIn("claves duplicadas", self.ledger.read_text())
        other = self.private / "other.jsonl"
        other.write_text(line(session_meta("s2")))
        with self.assertRaisesRegex(plan_usage.UsageError, "canónica"):
            self.bind(source_path=other, execution_id="e2", attempt_id="a2", session_id="s2",
                      thread_id="t2", root_turn_id="r2", requirement_ref="../STATE.md")

    def test_corrupt_ledger_is_not_reset(self):
        binding = self.bind()
        self.ledger.write_text('{"ledger_version":1,"bindings":{},"bindings":{}}')
        with self.assertRaisesRegex(plan_usage.UsageError, "ilegible"):
            self.report(binding)

    def test_crash_before_replace_preserves_and_retry_counts_once(self):
        binding = self.bind()
        self.append(token_record())
        with self.assertRaisesRegex(plan_usage.UsageError, "commit"):
            self.refresh(binding, _fault="before_replace")
        self.assertEqual(self.report(binding)["usage"]["responses"], 0)
        self.assertEqual(self.refresh(binding)["imported"], 1)
        self.assertEqual(self.report(binding)["usage"]["responses"], 1)

    def test_crash_after_replace_is_reconciled(self):
        binding = self.bind()
        self.append(token_record())
        self.assertEqual(self.refresh(binding, _fault="after_replace")["imported"], 1)
        self.assertEqual(self.report(binding)["usage"]["responses"], 1)
        self.assertEqual(self.refresh(binding)["imported"], 0)

    def test_busy_lock_fails_without_writing(self):
        binding = self.bind()
        self.append(token_record())
        lock_path = self.ledger.with_suffix(".json.lock")
        descriptor = os.open(lock_path, os.O_RDWR)
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaisesRegex(plan_usage.UsageError, "lock"):
                self.refresh(binding)
        finally:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)
        self.assertEqual(self.report(binding)["usage"]["responses"], 0)

    def test_ledger_and_lock_permissions_are_private(self):
        self.bind()
        self.assertEqual(self.ledger.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.ledger.with_suffix(".json.lock").stat().st_mode & 0o777, 0o600)

    def test_cli_binding_refresh_and_text_report(self):
        command = [sys.executable, "-I", "-B", str(ROOT / "scripts/lib/plan_usage.py"),
                   "--project-root", str(self.project), "--ledger", str(self.ledger)]
        bound = subprocess.run(command + ["bind", "--project-id", "project-1",
            "--requirement-ref", "docs/requirements/example/STATE.md", "--plan-version", "v1",
            "--plan-digest", "a" * 64, "--execution-id", "execution-1",
            "--attempt-id", "attempt-1", "--slice-id", "S01", "--source", str(self.source),
            "--source-version", "0.156.1", "--session-id", "session-1",
            "--thread-id", "thread-1", "--root-turn-id", "root-1"],
            check=True, capture_output=True, text=True)
        binding = bound.stdout.strip()
        self.append(token_record())
        refreshed = subprocess.run(command + ["refresh", "--binding-id", binding],
                                   check=True, capture_output=True, text=True)
        self.assertEqual(json.loads(refreshed.stdout)["imported"], 1)
        rendered = subprocess.run(command + ["report", "--binding-id", binding, "--format", "text"],
                                  check=True, capture_output=True, text=True)
        self.assertIn("Responses: 1", rendered.stdout)


class PlanUsageS02(unittest.TestCase):
    """S02 T2 fixtures: lifecycle, revisions and synthetic prices only."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="plan usage s02 tests ")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.project = self.base / "project"
        self.project.mkdir()
        self.private = self.base / "private"
        self.private.mkdir(mode=0o700)
        self.ledger = self.private / "usage.json"
        self.source = self.private / "rollout.jsonl"
        self.source.write_text(line(session_meta()))
        self.binding = plan_usage.bind(
            ledger_path=self.ledger, project_root=self.project, project_id="project-1",
            requirement_ref="docs/requirements/example/STATE.md", plan_version="v1",
            plan_digest="a" * 64, execution_id="execution-1", attempt_id="attempt-1",
            slice_id="S02", source_path=self.source, source_version="0.156.1",
            session_id="session-1", thread_id="thread-1", root_turn_id="root-1")

    def append(self, value):
        with self.source.open("a") as stream:
            stream.write(line(value))

    def event(self, event_id, kind, at, **values):
        return plan_usage.record_lifecycle_event(
            ledger_path=self.ledger, project_root=self.project, binding_id=self.binding,
            event_id=event_id, kind=kind, at=at, **values)

    def report(self, **values):
        values.setdefault("report_version", 2)
        return plan_usage.report(ledger_path=self.ledger, project_root=self.project,
                                 binding_id=self.binding, **values)

    def rates(self, snapshot_id="fixture-rates-v1", **changes):
        rate = {"effective_model": "fixture-model", "service_tier": "fixture-tier",
                "input_tokens": "1", "cached_input_tokens": "0.5",
                "output_tokens": "2"}
        rate.update(changes)
        snapshot = {"snapshot_id": snapshot_id, "kind": "synthetic", "currency": "USD",
                    "unit": "per_1m_tokens", "rates": [rate]}
        return plan_usage.register_rate_snapshot(
            ledger_path=self.ledger, project_root=self.project, snapshot=snapshot)

    def close_lifecycle(self):
        self.event("start", "started", "2026-09-24T10:00:00Z")
        self.event("close", "technical_closed", "2026-09-24T10:00:10Z")

    def test_t11_explicit_boundaries_pause_and_acceptance_are_separate(self):
        self.event("start", "started", "2026-09-24T10:00:00-03:00")
        self.event("pause", "paused", "2026-09-24T13:00:02Z")
        self.event("resume", "resumed", "2026-09-24T13:00:05Z")
        self.event("close", "technical_closed", "2026-09-24T13:00:10Z")
        before = self.report()
        self.assertEqual(before["lifecycle"]["technical_status"], "closed")
        self.assertEqual(before["lifecycle"]["acceptance_status"], "pending")
        self.assertEqual(before["times"]["elapsed_seconds"], "10.0")
        self.assertEqual(before["times"]["paused_seconds"], "3.0")
        self.assertEqual(before["times"]["unpaused_seconds"], "7.0")
        self.assertIsNone(before["times"]["active_time_seconds"])
        self.event("accept", "accepted", "2026-09-24T13:00:12Z",
                   reference="docs/requirements/example/STATE.md")
        after = self.report()
        self.assertEqual(after["lifecycle"]["acceptance_status"], "accepted")
        self.assertEqual(after["lifecycle"]["acceptance_reference"],
                         "docs/requirements/example/STATE.md")

    def test_t06_t11_late_event_creates_revision_and_preserves_previous_report(self):
        self.close_lifecycle()
        first = plan_usage.snapshot_report(ledger_path=self.ledger,
            project_root=self.project, binding_id=self.binding)
        self.assertEqual(first["revision"], {"number": 1, "persisted": True,
                                             "supersedes": None, "reason": "initial"})
        self.assertEqual(self.event("late-pause", "paused", "2026-09-24T10:00:03Z"),
                         {"recorded": True, "late": True})
        self.event("late-resume", "resumed", "2026-09-24T10:00:04Z")
        second = plan_usage.snapshot_report(ledger_path=self.ledger,
            project_root=self.project, binding_id=self.binding)
        preserved = self.report(revision=1)
        self.assertEqual(preserved, first)
        self.assertEqual(second["revision"]["supersedes"], 1)
        self.assertEqual(second["revision"]["reason"], "late_event")
        self.assertEqual(second["times"]["paused_seconds"], "1.0")
        self.assertTrue(any(item["kind"] == "late_lifecycle_event"
                            for item in second["anomalies"]))

    def test_t11_regressive_clock_and_missing_close_stay_unknown(self):
        self.event("start", "started", "2026-09-24T10:00:10Z")
        self.event("close", "technical_closed", "2026-09-24T10:00:05Z")
        value = self.report()
        self.assertIsNone(value["times"]["elapsed_seconds"])
        self.assertIn("elapsed_time", value["unknowns"])
        self.assertEqual(value["data_state"], "incomplete")

    def test_t05_failures_retries_and_missing_usage_are_explicit(self):
        self.event("start", "started", "2026-09-24T10:00:00Z")
        self.append(token_record("failed-with-usage"))
        self.append(token_record("retry-with-usage", turn="turn-2"))
        plan_usage.refresh(ledger_path=self.ledger, project_root=self.project,
                           binding_id=self.binding)
        self.event("failure-1", "failed", "2026-09-24T10:00:02Z",
                   response_id="failed-with-usage", usage_observed=True)
        self.event("retry-1", "retry", "2026-09-24T10:00:03Z",
                   response_id="retry-with-usage", usage_observed=True)
        self.event("failure-2", "failed", "2026-09-24T10:00:04Z",
                   response_id="failed-without-usage", usage_observed=False)
        self.event("close", "technical_closed", "2026-09-24T10:00:05Z")
        value = self.report()
        self.assertEqual(value["usage"]["responses"], 2)
        self.assertEqual(value["outcomes"], {"failures": 2, "retries": 1,
                                              "cancellations": 0,
                                              "missing_usage_events": 1})
        self.assertEqual(value["data_state"], "incomplete")

    def test_t05_claimed_usage_without_matching_record_is_rejected(self):
        self.event("start", "started", "2026-09-24T10:00:00Z")
        self.event("failure", "failed", "2026-09-24T10:00:01Z",
                   response_id="absent-response", usage_observed=True)
        self.event("close", "technical_closed", "2026-09-24T10:00:02Z")
        value = self.report()
        self.assertEqual(value["outcomes"]["missing_usage_events"], 1)
        self.assertTrue(any(item["kind"] == "failed_response_usage_unknown"
                            for item in value["anomalies"]))

    def test_t05_cancellation_closes_technical_time_without_acceptance(self):
        self.event("start", "started", "2026-09-24T10:00:00Z")
        self.event("cancel", "cancelled", "2026-09-24T10:00:04Z",
                   usage_observed=False)
        value = self.report()
        self.assertEqual(value["lifecycle"]["technical_status"], "cancelled")
        self.assertEqual(value["lifecycle"]["acceptance_status"], "pending")
        self.assertEqual(value["outcomes"]["cancellations"], 1)
        self.assertEqual(value["outcomes"]["missing_usage_events"], 1)
        self.assertEqual(value["times"]["elapsed_seconds"], "4.0")
        self.assertEqual(value["data_state"], "incomplete")

    def test_t07_decimal_synthetic_subtotal_never_claims_billed_cost(self):
        self.append(token_record(extra={"effective_model": "fixture-model",
                                        "service_tier": "fixture-tier",
                                        "payment_mode": "fixture-mode"}))
        plan_usage.refresh(ledger_path=self.ledger, project_root=self.project,
                           binding_id=self.binding)
        self.close_lifecycle()
        self.rates()
        value = plan_usage.snapshot_report(ledger_path=self.ledger,
            project_root=self.project, binding_id=self.binding,
            rate_snapshot_id="fixture-rates-v1")
        self.assertEqual(value["identity"], {"effective_model": "fixture-model",
                                             "service_tier": "fixture-tier",
                                             "payment_mode": "fixture-mode"})
        self.assertEqual(value["cost"]["amount"], "0.000130000")
        self.assertEqual(value["cost"]["nature"], "synthetic_api_equivalent_subtotal")
        self.assertIsNone(value["cost"]["billed_amount"])
        self.assertIn("billed_usd", value["unknowns"])
        self.assertNotIn("usd", value["unknowns"])

    def test_t07_unknown_identity_rate_and_immutable_history_do_not_become_zero(self):
        self.append(token_record())
        plan_usage.refresh(ledger_path=self.ledger, project_root=self.project,
                           binding_id=self.binding)
        self.close_lifecycle()
        self.rates()
        first = plan_usage.snapshot_report(ledger_path=self.ledger,
            project_root=self.project, binding_id=self.binding,
            rate_snapshot_id="fixture-rates-v1")
        self.assertIsNone(first["identity"]["effective_model"])
        self.assertIsNone(first["cost"]["amount"])
        self.assertEqual(first["cost"]["unpriced_responses"], 1)
        self.assertIn("usd", first["unknowns"])
        with self.assertRaisesRegex(plan_usage.UsageError, "inmutable"):
            self.rates(input_tokens="9")
        self.rates(snapshot_id="fixture-rates-v2", input_tokens="2")
        with self.assertRaisesRegex(plan_usage.UsageError, "serie de revisiones"):
            plan_usage.snapshot_report(ledger_path=self.ledger,
                project_root=self.project, binding_id=self.binding,
                rate_snapshot_id="fixture-rates-v2")
        with self.assertRaisesRegex(plan_usage.UsageError, "solo se admiten"):
            plan_usage.register_rate_snapshot(ledger_path=self.ledger,
                project_root=self.project,
                snapshot={"snapshot_id": "commercial", "kind": "commercial"})

    def test_t07_model_or_tier_change_yields_only_an_explicit_partial_subtotal(self):
        self.append(token_record("priced", extra={"effective_model": "fixture-model",
            "service_tier": "fixture-tier", "payment_mode": "fixture-mode"}))
        self.append(token_record("rerouted", turn="turn-2", extra={
            "effective_model": "unresolved-alias", "service_tier": "other-tier",
            "payment_mode": "fixture-mode"}))
        plan_usage.refresh(ledger_path=self.ledger, project_root=self.project,
                           binding_id=self.binding)
        self.close_lifecycle()
        self.rates()
        value = self.report(rate_snapshot_id="fixture-rates-v1")
        self.assertIsNone(value["identity"]["effective_model"])
        self.assertEqual(value["cost"]["amount"], "0.000130000")
        self.assertEqual(value["cost"]["priced_responses"], 1)
        self.assertEqual(value["cost"]["unpriced_responses"], 1)
        self.assertEqual(value["cost"]["nature"], "synthetic_api_equivalent_subtotal")
        self.assertIn("usd", value["unknowns"])

    def test_t04_atomic_event_and_report_failures_preserve_previous_revision(self):
        self.close_lifecycle()
        first = plan_usage.snapshot_report(ledger_path=self.ledger,
            project_root=self.project, binding_id=self.binding)
        with self.assertRaisesRegex(plan_usage.UsageError, "commit"):
            self.event("accept", "accepted", "2026-09-24T10:00:12Z",
                       reference="docs/requirements/example/STATE.md", _fault="before_replace")
        self.assertEqual(self.report(revision=1), first)
        self.event("accept", "accepted", "2026-09-24T10:00:12Z",
                   reference="docs/requirements/example/STATE.md")
        with self.assertRaisesRegex(plan_usage.UsageError, "commit"):
            plan_usage.snapshot_report(ledger_path=self.ledger,
                project_root=self.project, binding_id=self.binding,
                _fault="before_replace")
        self.assertEqual(self.report(revision=1), first)
        with self.assertRaisesRegex(plan_usage.UsageError, "revisión"):
            self.report(revision=2)

    def test_t04_lifecycle_writer_respects_existing_lock(self):
        lock_path = self.ledger.with_suffix(".json.lock")
        descriptor = os.open(lock_path, os.O_RDWR)
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaisesRegex(plan_usage.UsageError, "lock"):
                self.event("start", "started", "2026-09-24T10:00:00Z")
        finally:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)
        self.assertEqual(self.report()["lifecycle"]["event_count"], 0)

    def test_t12_report_v2_schema_and_v1_compatibility(self):
        self.append(token_record())
        plan_usage.refresh(ledger_path=self.ledger, project_root=self.project,
                           binding_id=self.binding)
        self.close_lifecycle()
        current = self.report()
        schema_v2 = json.loads((ROOT / "templates/usage/MEASUREMENT.schema.json").read_text())
        self.assertEqual(set(current), set(schema_v2["required"]))
        previous = self.report(report_version=1)
        schema_v1 = json.loads((ROOT / "templates/usage/MEASUREMENT.v1.schema.json").read_text())
        self.assertEqual(set(previous), set(schema_v1["required"]))
        self.assertEqual(previous["report_version"], 1)
        self.assertNotIn("cost", previous)
        rendered = plan_usage.render_text(current)
        self.assertIn("Lifecycle: technical=closed acceptance=pending", rendered)
        self.assertIn("billed=unknown", rendered)

    def test_t12_cli_lifecycle_and_versioned_snapshot(self):
        command = [sys.executable, "-I", "-B", str(ROOT / "scripts/lib/plan_usage.py"),
                   "--project-root", str(self.project), "--ledger", str(self.ledger)]
        for event_id, kind, at in (("start", "started", "2026-09-24T10:00:00Z"),
                                   ("close", "technical_closed", "2026-09-24T10:00:03Z")):
            completed = subprocess.run(command + ["lifecycle", "--binding-id", self.binding,
                "--event-id", event_id, "--kind", kind, "--at", at], check=True,
                capture_output=True, text=True)
            self.assertTrue(json.loads(completed.stdout)["recorded"])
        saved = subprocess.run(command + ["snapshot", "--binding-id", self.binding,
            "--format", "json"], check=True, capture_output=True, text=True)
        report = json.loads(saved.stdout)
        self.assertEqual(report["revision"]["number"], 1)
        self.assertTrue(report["revision"]["persisted"])
        self.assertEqual(report["times"]["elapsed_seconds"], "3.0")


class ProjectWorkHistory(unittest.TestCase):
    """Prospective history uses only artificial rollouts and a private ledger."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="work history tests ")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.project = self.base / "project"
        self.project.mkdir()
        self.private = self.base / "private"
        self.private.mkdir(mode=0o700)
        self.ledger = self.private / "usage.json"
        self.sources = {}

    def bind(self, number, *, project_id="project-1", kind="feature", work_id="work-1"):
        source = self.private / f"rollout-{number}.jsonl"
        source.write_text(line(session_meta(f"session-{number}")))
        self.sources[number] = source
        return plan_usage.bind(
            ledger_path=self.ledger, project_root=self.project, project_id=project_id,
            requirement_ref="docs/requirements/example/STATE.md", plan_version="v1",
            plan_digest="a" * 64, execution_id=f"execution-{number}",
            attempt_id=f"attempt-{number}", slice_id="H01", source_path=source,
            source_version="0.156.1", session_id=f"session-{number}",
            thread_id=f"thread-{number}", root_turn_id=f"root-{number}",
            work_kind=kind, work_id=work_id)

    def add_response(self, number, response):
        with self.sources[number].open("a") as stream:
            stream.write(line(token_record(response, session=f"session-{number}",
                                           thread=f"thread-{number}", root=f"root-{number}")))

    def snapshot(self, binding):
        plan_usage.refresh(ledger_path=self.ledger, project_root=self.project,
                           binding_id=binding)
        return plan_usage.snapshot_report(ledger_path=self.ledger,
                                          project_root=self.project, binding_id=binding)

    def history(self, project_id="project-1"):
        return plan_usage.history_report(ledger_path=self.ledger,
                                         project_root=self.project, project_id=project_id)

    def test_h01_latest_revision_and_project_filter(self):
        self.bind(0, kind=None, work_id=None)  # Legacy remains unclassified.
        feature = self.bind(1)
        self.add_response(1, "one")
        self.snapshot(feature)
        self.add_response(1, "two")
        self.snapshot(feature)
        bug = self.bind(2, project_id="project-2", kind="bug", work_id="bug-2")
        self.add_response(2, "other")
        self.snapshot(bug)
        result = self.history()
        self.assertEqual(result["legacy_bindings_excluded"], 1)
        self.assertEqual(result["overall"]["usage"]["responses"], 2)
        self.assertEqual(result["overall"]["usage"]["total_tokens"], 260)
        self.assertEqual(result["overall"]["reports"], 1)
        self.assertEqual(result["work_items"][0]["work_kind"], "feature")
        self.assertEqual(self.history("project-2")["overall"]["usage"]["responses"], 1)

    def test_h01_explicit_time_and_missing_coverage(self):
        first = self.bind(1)
        self.add_response(1, "one")
        for event_id, kind, at in (("start", "started", "2026-09-25T10:00:00Z"),
                                   ("close", "technical_closed", "2026-09-25T10:00:10Z")):
            plan_usage.record_lifecycle_event(ledger_path=self.ledger,
                project_root=self.project, binding_id=first, event_id=event_id,
                kind=kind, at=at)
        self.snapshot(first)
        second = self.bind(2)
        self.add_response(2, "two")
        self.snapshot(second)
        row = self.history()["work_items"][0]
        self.assertIsNone(row["times"]["elapsed_seconds"]["seconds"])
        self.assertEqual(row["times"]["elapsed_seconds"]["known_subtotal_seconds"], "10.0")
        self.assertEqual(row["times"]["elapsed_seconds"]["unknown_bindings"], 1)
        self.assertIsNone(row["active_time_seconds"])
        self.assertIsNone(row["usd"]["amount"])

    def test_h01_marks_are_explicit_and_work_can_have_multiple_kinds(self):
        with self.assertRaisesRegex(plan_usage.UsageError, "juntos"):
            self.bind(1, kind="feature", work_id=None)
        with self.assertRaisesRegex(plan_usage.UsageError, "inválido"):
            self.bind(1, kind="feature", work_id="contains spaces")
        feature = self.bind(1)
        bug = self.bind(2, kind="bug", work_id="work-1")
        self.add_response(1, "feature")
        self.add_response(2, "bug")
        self.snapshot(feature)
        self.snapshot(bug)
        items = self.history()["work_items"]
        self.assertEqual([(item["work_kind"], item["work_id"]) for item in items],
                         [("bug", "work-1"), ("feature", "work-1")])

    def test_h01_history_reads_ledger_only_and_cli_matches(self):
        binding = self.bind(1)
        self.add_response(1, "one")
        self.snapshot(binding)
        self.sources[1].unlink()
        expected = self.history()
        command = [sys.executable, "-I", "-B", str(ROOT / "scripts/lib/plan_usage.py"),
                   "--project-root", str(self.project), "--ledger", str(self.ledger),
                   "history", "--project-id", "project-1"]
        actual = subprocess.run(command + ["--format", "json"], check=True,
                                capture_output=True, text=True)
        self.assertEqual(json.loads(actual.stdout), expected)
        rendered = subprocess.run(command + ["--format", "text"], check=True,
                                  capture_output=True, text=True)
        self.assertIn("feature: work=1 responses=1 tokens=130", rendered.stdout)
        self.assertNotIn(str(self.sources[1]), actual.stdout)

    def test_h01_snapshot_staleness_is_visible(self):
        binding = self.bind(1)
        self.add_response(1, "one")
        self.snapshot(binding)
        self.add_response(1, "two")
        plan_usage.refresh(ledger_path=self.ledger, project_root=self.project,
                           binding_id=binding)
        row = self.history()["work_items"][0]
        self.assertEqual(row["usage"]["responses"], 1)
        self.assertEqual(row["stale_reports"], 1)
        self.assertEqual(row["data_state"], "incomplete")
        plan_usage.snapshot_report(ledger_path=self.ledger, project_root=self.project,
                                   binding_id=binding)
        self.assertEqual(self.history()["work_items"][0]["stale_reports"], 0)

    def test_h01_empty_and_missing_snapshot_are_explicit(self):
        self.bind(0, project_id="other-project")
        empty = self.history()
        self.assertEqual(empty["overall"]["data_state"], "empty")
        self.assertEqual(empty["overall"]["bindings"], 0)
        self.assertIsNone(empty["overall"]["usd"]["amount"])
        binding = self.bind(1)
        self.add_response(1, "one")
        plan_usage.refresh(ledger_path=self.ledger, project_root=self.project,
                           binding_id=binding)
        missing = self.history()["overall"]
        self.assertEqual(missing["missing_reports"], 1)
        self.assertEqual(missing["data_state"], "incomplete")
        self.assertEqual(missing["usage"]["responses"], 0)
        self.assertIsNone(missing["times"]["elapsed_seconds"]["seconds"])

    def test_h02_direct_usd_requires_unique_evidence_and_complete_coverage(self):
        first = self.bind(1)
        second = self.bind(2)
        self.add_response(1, "one")
        self.add_response(2, "two")
        self.snapshot(first)
        self.snapshot(second)
        common = dict(ledger_path=self.ledger, project_root=self.project,
                      evidence_sha256="b" * 64)
        self.assertEqual(plan_usage.record_actual_usd(binding_id=first, amount="1.25",
            evidence_id="invoice-line-1", complete_for_binding=True, **common),
            {"recorded": True})
        self.assertEqual(plan_usage.record_actual_usd(binding_id=first, amount="1.25",
            evidence_id="invoice-line-1", complete_for_binding=True, **common),
            {"recorded": False})
        partial = self.history()["work_items"][0]["usd"]
        self.assertIsNone(partial["amount"])
        self.assertEqual(partial["known_subtotal"], "1.25")
        self.assertEqual(partial["unknown_bindings"], 1)
        with self.assertRaisesRegex(plan_usage.UsageError, "ya asignado"):
            plan_usage.record_actual_usd(binding_id=second, amount="2.00",
                evidence_id="invoice-line-1", complete_for_binding=True, **common)
        plan_usage.record_actual_usd(binding_id=second, amount="2.00",
            evidence_id="invoice-line-2", complete_for_binding=True, **common)
        total = self.history()["work_items"][0]["usd"]
        self.assertEqual(total["amount"], "3.25")
        self.assertEqual(total["provenance"], "user_attested_direct_charge")
        self.assertNotIn("invoice-line-1", json.dumps(self.history()))

    def test_h02_partial_cost_never_becomes_a_total(self):
        binding = self.bind(1)
        self.add_response(1, "one")
        self.snapshot(binding)
        plan_usage.record_actual_usd(ledger_path=self.ledger, project_root=self.project,
            binding_id=binding, amount="0.50", evidence_id="line-1",
            evidence_sha256="c" * 64, complete_for_binding=False)
        row = self.history()["work_items"][0]
        self.assertIsNone(row["usd"]["amount"])
        self.assertEqual(row["usd"]["known_subtotal"], "0.50")
        with self.assertRaisesRegex(plan_usage.UsageError, "inmutable"):
            plan_usage.record_actual_usd(ledger_path=self.ledger,
                project_root=self.project, binding_id=binding, amount="9.99",
                evidence_id="line-1", evidence_sha256="c" * 64,
                complete_for_binding=False)
        with self.assertRaisesRegex(plan_usage.UsageError, "positivo"):
            plan_usage.record_actual_usd(ledger_path=self.ledger,
                project_root=self.project, binding_id=binding, amount="0",
                evidence_id="line-2", evidence_sha256="d" * 64,
                complete_for_binding=True)
        with self.assertRaisesRegex(plan_usage.UsageError, "acotado"):
            plan_usage.record_actual_usd(ledger_path=self.ledger,
                project_root=self.project, binding_id=binding, amount="1e999999",
                evidence_id="line-2", evidence_sha256="d" * 64,
                complete_for_binding=True)

    def test_h02_kev_suggests_without_persisting_or_auto_confirming(self):
        seen = {}
        def fake(body, port):
            seen["request"] = json.loads(body)
            seen["port"] = port
            return line({"answers": {"work_kind": {"type": "choice",
                "choice": "documentation", "confidence": 0.8,
                "probabilities": {kind: (0.8 if kind == "documentation" else 0.05)
                                  for kind in plan_usage.WORK_KINDS}}}})
        result = plan_usage.suggest_work_kind(summary="Update guide",
            endpoint="http://127.0.0.1:8009", _transport=fake)
        self.assertEqual(result["suggested_kind"], "documentation")
        self.assertFalse(result["confirmed"])
        self.assertEqual(seen["port"], 8009)
        self.assertEqual(seen["request"]["state"], "Update guide")
        self.assertFalse(self.ledger.exists())
        self.assertNotIn("Update guide", json.dumps(result))
        with self.assertRaisesRegex(plan_usage.UsageError, "local"):
            plan_usage.suggest_work_kind(summary="Update guide",
                endpoint="https://example.com:8009", _transport=fake)
        with self.assertRaisesRegex(plan_usage.UsageError, "local"):
            plan_usage.suggest_work_kind(summary="Update guide",
                endpoint="http://127.0.0.1:8009/redirect", _transport=fake)
        with self.assertRaisesRegex(plan_usage.UsageError, "elección válida"):
            plan_usage.suggest_work_kind(summary="Update guide",
                endpoint="http://127.0.0.1:8009",
                _transport=lambda _body, _port: b'{"answers":{}}')

    def test_h02_synthetic_price_never_becomes_actual_usd(self):
        binding = self.bind(1)
        with self.sources[1].open("a") as stream:
            stream.write(line(token_record("one", session="session-1",
                thread="thread-1", root="root-1",
                extra={"effective_model": "fixture-model", "service_tier": "fixture-tier"})))
        plan_usage.refresh(ledger_path=self.ledger, project_root=self.project,
                           binding_id=binding)
        rate_id = plan_usage.register_rate_snapshot(ledger_path=self.ledger,
            project_root=self.project, snapshot={"snapshot_id": "synthetic-1",
                "kind": "synthetic", "currency": "USD", "unit": "per_1m_tokens",
                "rates": [{"effective_model": "fixture-model", "service_tier": "fixture-tier",
                           "input_tokens": "1", "cached_input_tokens": "0.5",
                           "output_tokens": "2"}]})
        saved = plan_usage.snapshot_report(ledger_path=self.ledger,
            project_root=self.project, binding_id=binding, rate_snapshot_id=rate_id)
        self.assertIsNotNone(saved["cost"]["amount"])
        self.assertIsNone(self.history()["overall"]["usd"]["amount"])

    def test_h02_cli_records_cost_without_reading_source(self):
        binding = self.bind(1)
        self.add_response(1, "one")
        self.snapshot(binding)
        self.sources[1].unlink()
        command = [sys.executable, "-I", "-B", str(ROOT / "scripts/lib/plan_usage.py"),
                   "--project-root", str(self.project), "--ledger", str(self.ledger)]
        completed = subprocess.run(command + ["record-usd", "--binding-id", binding,
            "--amount", "1.00", "--evidence-id", "line-1",
            "--evidence-sha256", "e" * 64, "--complete-for-binding"], check=True,
            capture_output=True, text=True)
        self.assertEqual(json.loads(completed.stdout), {"recorded": True})
        self.assertEqual(self.history()["overall"]["usd"]["amount"], "1.00")


if __name__ == "__main__":
    unittest.main()
