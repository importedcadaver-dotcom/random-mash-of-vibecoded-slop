# Agent instructions

This repository contains separate AI-assisted game projects. Read this file and the game-specific AGENTS.md before changing code.

## Identity and labels

Every workstream uses a clear label in its commit or pull request title:

- Format: `<agent or model> / <game-id> / <short-task>`; examples: `Codex / clash-of-cubs / playable-prototype`, `ChatGPT GPT-6 / mud-pie-masters / import-v0.5`
- Workstreams: `Codex / clash-of-cubs / playable-prototype` and `ChatGPT GPT-6 / mud-pie-masters / import-v0.5`. These are labels, not separate authenticated GitHub user accounts.

## Parallel work

- Give every chat or agent its own Git branch and Git worktree. Never let multiple agents write to one checkout.
- Use branches such as `agent/clash-of-cubs/<short-task>`.
- Keep each agent's changes inside one game's folder. Within a game, split concurrent tasks by file ownership to reduce conflicts.
- Treat root files and shared game-index files as coordinator-owned; ask the repository owner before changing shared conventions.
- Integrate through pull requests. Do not push directly to `main`.
- Before handoff, report the agent label, changed paths, verification performed, and unresolved issues.

## Folder layout

- Put each game in `games/<game-id>/`.
- Give every game its own README.md, AGENTS.md, and game.json.
- Keep saves, generated build output, and dependencies local to that game; do not check in personal saves or secrets.
