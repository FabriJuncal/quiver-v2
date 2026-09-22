"""Static inactive proposal check, NOT a dispatcher or effective runtime preflight.

Exit 1: invalid proposal. Exit 2: syntactically valid, live delegation NOT VERIFIED.
Never returns live-ready, runs commands, reads personal config or installs anything.
"""
import argparse
import json
from pathlib import Path
import sys
import tomllib

FLAGS = ('apps', 'hooks', 'browser_use', 'browser_use_external',
         'browser_use_full_cdp_access', 'computer_use', 'remote_plugin')


def validate(directory):
    for filename in ('coordinator.toml', 'asf_helper.toml'):
        path = directory / filename
        if path.is_symlink() or not path.is_file():
            raise ValueError(f'{filename}: regular file required')
        config = tomllib.loads(path.read_text())
        expected = {
            'approval_policy': 'never', 'approvals_reviewer': 'user',
            'allow_login_shell': False, 'web_search': 'disabled',
            'sandbox_mode': 'read-only',
            'agents': {'enabled': False, 'max_concurrent_threads_per_session': 1},
            'features': dict.fromkeys(FLAGS, False), 'mcp_servers': {}, 'plugins': {},
        }
        if filename == 'asf_helper.toml':
            for field in ('description', 'developer_instructions'):
                if not isinstance(config.get(field), str) or not config[field].strip():
                    raise ValueError(f'{filename}: missing {field}')
                expected[field] = config[field]
            expected['name'] = 'asf_helper'
            expected['features'].update(shell_tool=False, unified_exec=False)
        # Exact shape deliberately rejects unrelated inherited settings and model copies.
        # It does not resolve Codex's effective configuration or tool inventory.
        if json.dumps(config, sort_keys=True) != json.dumps(expected, sort_keys=True):
            raise ValueError(f'{filename}: differs from the inactive proposal contract')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path,
                        default=Path(__file__).resolve().parents[2] / 'config/assistant-proposal')
    args = parser.parse_args()
    try:
        validate(args.directory)
    except (ValueError, OSError, UnicodeError) as error:
        print(json.dumps({'static_result': 'FAIL', 'delegation': 'DISABLED', 'error': str(error)}))
        return 1
    print(json.dumps({
        'static_result': 'PASS', 'delegation': 'DISABLED', 'pilot': 'NOT RUN',
        'runtime_controls': 'NOT VERIFIED',
        'missing': ['effective child role and permission binding',
                    'effective absence of recursive and external mutation tools',
                    'observable identity and effective termination'],
        'next_action': 'Keep inline. Follow docs/guides/ASSISTANT_INTEGRATION.md; do not enable from this result.',
    }, indent=2))
    return 2


if __name__ == '__main__':
    sys.exit(main())
