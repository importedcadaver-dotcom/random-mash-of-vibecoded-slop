# Multi-agent workflow

This is a **monorepo of multiple independent AI-assisted games**, not a single game's codebase. Existing Codex/Clash of Cubs conventions in `AGENTS.md` are preserved.

## Isolation and attribution
Each game uses `games/<slug>/`, has its own `README.md`, `AGENTS.md`, `game.json`, environment, assets and tests. A contribution label identifies the model/team, affected game and task; it does **not** imply a separate GitHub account. Use labels like `ChatGPT GPT-6 / mud-pie-masters / import-v0.5` and `Codex / clash-of-cubs / playable-prototype`.

## Work in parallel safely
- Never share a working directory between simultaneous agents. Use branches plus `git worktree add` for each.
- Branch names: `agent/<game>/<short-task>` or `agents/<model>/<game>-<task>`; never reuse another workstream's branch.
- Own only explicitly assigned game paths. Shared root files and `.github/` must be coordinated separately.
- Create a PR to `main` for review, even when only an AI agent worked on the change.
- Do not force push, silently resolve conflicts by overwriting teammates, or push to `main`.
- Explain test commands, evidence and missing verification. Do not say a game "passed QA" solely because a model checked its own logic.

## Local example (PowerShell)
```powershell
git fetch origin
git worktree add ..\work-mudpie -b agents/gpt6/mud-pie-masters-ui origin/main
Set-Location ..\work-mudpie\games\mud-pie-masters
```

## Changes that overlap
When two agents must modify `mudpie/game.py`, coordinate the second agent via PR/issue first. Avoid blind merges. Prefer split modules and unit tests to improve parallelism.

## Importing new games
Never unpack a game's ZIP at repository root, never overwrite `games/<other-game>/`. Use a per-game folder. Mud Pie Masters v0.5 was imported directly as individual Git files, with its original PNG/WAV assets; keep future games isolated to their own folder. Avoid leaving one-game-only importer utilities in shared root indefinitely.

## Release gate
Each game defines its own acceptance tests. Mud Pie Masters remains an unverified two-hour pre-release; Windows interactive playtesting is outstanding. Keep honest release labels in the catalog and PR.
