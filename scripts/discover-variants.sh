#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

for candidate in python3.14 python3.13 python3.12 python3.11 python3; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -I -B -c 'import argparse, pathlib' >/dev/null 2>&1; then
    exec "$candidate" -I -B "$SCRIPT_DIR/lib/branch_discovery.py" "$@"
  fi
done

echo "ERROR: discover-variants requiere Python >= 3.11" >&2
exit 1
