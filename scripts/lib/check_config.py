"""Validate optional Codex profile TOML without loading credentials or a model."""
import sys
import tomllib
from pathlib import Path


def main():
    path = Path(sys.argv[1])
    try:
        with path.open("rb") as stream:
            config = tomllib.load(stream)
        if "profiles" in config or "profile" in config:
            raise ValueError("Use top-level keys in separate profile files (Codex >= 0.134.0).")
        for key in ("model", "review_model"):
            if key in config and (not isinstance(config[key], str) or not config[key].strip()):
                raise ValueError(f"{key} must be a nonempty string.")
        if "model_reasoning_effort" in config and config["model_reasoning_effort"] not in (
            "none", "minimal", "low", "medium", "high", "xhigh", "max", "ultra"
        ):
            raise ValueError("Invalid model_reasoning_effort; availability remains model-dependent.")
    except (OSError, tomllib.TOMLDecodeError):
        print(f"ERROR: cannot parse TOML: {path}", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"ERROR: {path}: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
