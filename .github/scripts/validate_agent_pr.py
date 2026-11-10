"""Validate attribution and game-folder isolation for every pull request."""
import json
import os
import re
import subprocess
from pathlib import Path


def check() -> list[str]:
    event = json.loads(Path(os.environ['EVENT_PATH']).read_text(encoding='utf-8'))
    body = event['pull_request'].get('body') or ''
    errors = []
    required = ('Agent', 'Model', 'Game', 'Workstream ID', 'Files owned', 'Tests performed', 'Known gaps', 'Shared-file coordination')
    for key in required:
        found = re.search(r'^\*\*' + re.escape(key) + r':\*\*\s*(.+)$', body, re.MULTILINE)
        if not found or not found.group(1).strip() or '<' in found.group(1) or found.group(1).strip().lower() in ('tbd', 'todo', 'n/a'):
            errors.append(f'Missing or placeholder PR field: {key}')

    diff = subprocess.run(
        ['git', 'diff', '--name-only', os.environ['BASE_SHA'], 'HEAD'],
        check=True, capture_output=True, text=True, encoding='utf-8'
    )
    paths = [p.strip() for p in diff.stdout.splitlines() if p.strip()]
    game_ids = {parts[1] for p in paths if (parts := p.split('/'))[0] == 'games' and len(parts) >= 3}
    if len(game_ids) > 1 and '**Cross-game approval:** owner-approved' not in body:
        errors.append('Multiple games changed without explicit owner cross-game approval field')
    if game_ids:
        found_game = re.search(r'^\*\*Game:\*\*\s*(.+)$', body, re.MULTILINE)
        if not found_game or (len(game_ids) == 1 and next(iter(game_ids)) not in found_game.group(1)):
            errors.append('PR Game field does not name the changed game')
    shared = [p for p in paths if not p.startswith('games/')]
    if shared and game_ids and '**Shared-file coordination:** owner-requested' not in body and '**Shared-file coordination:** coordinated' not in body:
        errors.append('Shared root or CI changes alongside game files require explicit coordination')
    forbidden = ('.venv/', 'node_modules/', '__pycache__/', '.pytest_cache/', '.env', 'save.json')
    for p in paths:
        parts = p.split('/')
        if any(seg in ('.venv', 'node_modules', '__pycache__', '.pytest_cache') for seg in parts) or p.endswith(('.pyc', '.pyo')) or Path(p).name in ('.env', 'save.json'):
            errors.append(f'Likely local or secret file tracked: {p}')
    print('Changed files:', len(paths), '; game scopes:', sorted(game_ids), '; shared files:', len(shared))
    return errors


if __name__ == '__main__':
    problems = check()
    if problems:
        for problem in problems:
            print('ERROR:', problem)
        raise SystemExit(1)
    print('PASS: PR attribution and file isolation checked')
