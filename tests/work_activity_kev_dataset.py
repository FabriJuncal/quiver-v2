"""Frozen synthetic corpus contract for A04; no real project text is included."""
from __future__ import annotations

import hashlib
import json


KINDS = ("feature", "bug", "test", "explanation", "documentation")


def _case(prefix: str, number: int, label: str, family: str) -> dict[str, object]:
    return {"id": f"{prefix}-{label}-{number:03}", "state":
            f"Synthetic {family} scenario number {number}; no project content.",
            "label": label, "family": family}


def development_cases() -> list[dict[str, object]]:
    return [_case("dev", number, kind, "clear")
            for kind in KINDS for number in range(1, 21)]


def evaluation_cases() -> list[dict[str, object]]:
    clear = [_case("eval", number, kind, "clear")
             for kind in KINDS for number in range(1, 31)]
    mixed = [{"id": f"eval-mixed-{number:03}",
              "state": f"Synthetic combined code, test and guide scenario {number}; no project content.",
              "label": "mixed", "family": "mixed"}
             for number in range(1, 26)]
    insufficient = [{"id": f"eval-unknown-{number:03}",
                     "state": f"Synthetic ambiguous operation scenario {number}; no project content.",
                     "label": "implementation_unspecified", "family": "insufficient"}
                    for number in range(1, 26)]
    return [*clear, *mixed, *insufficient]


def digest(cases: list[dict[str, object]]) -> str:
    raw = json.dumps(cases, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()
