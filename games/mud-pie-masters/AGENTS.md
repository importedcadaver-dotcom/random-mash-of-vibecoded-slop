# Agent instructions: Mud Pie Masters

**Canonical project:** `games/mud-pie-masters/` — Python 3.12 + Pygame Community Edition.
**Contribution label:** `ChatGPT GPT-6 / mud-pie-masters / import-v0.5`.
The GitHub operations are performed through the repository owner's linked GitHub account, **not** through a unique assistant account.

Read the repository-level `../../AGENTS.md` first. Follow its branches, worktrees, project isolation and PR review rules.

## Game invariants
- Single-player offline Windows game; protagonist is a cute baby brown bear; rivals are sibling cubs Bruno and Daisy.
- Six ingredients: mud, leaves, petals, pebbles, sticks, berries (contest decorations, not food).
- Four tactile tool modes: scoop/mix, shape/flatten, stack, decorate.
- Three judges have distinct preferences; scores must derive from constructed pie geometry and be explained.
- Existing content: 36 main story contests, 12 optional commissions, six chapters, relationships, campaign progression, saves.
- v0.4 expressive infant sprites are **provisional** artwork, not locked final art.
- **Never claim 2 hours of fun are verified** until an actual observed human full playthrough supports that claim. Synthetic 48-contest simulations are NOT a time benchmark.
- The v0.5 source package is the authoritative import source, not an excuse to silently replace the game or invent a new version.

## Key code areas (after full source import)
- `mudpie/models.py` pie representation, mud-volume conservation and stability.
- `mudpie/judging.py` judge weights and anti-exploit scoring.
- `mudpie/rivals.py` siblings' entry generation and relationship state.
- `mudpie/campaign.py` authored contests and progression.
- `mudpie/game.py` Pygame state, controls and UI.
- `mudpie/rendering.py` actual gameplay drawing and sprites.
- `tools/` offline generators, simulations and regression scripts.

## Parallel agents
Use a **new unique branch and worktree for each task**. Prefer module-specific scopes: physics, scoring, UI, art, campaign, QA. Do not push directly to main or edit another game's folder. If two agents need the same module, coordinate via PR/issue comments before changes.

## QA baseline
Run `python -m pytest -q` and `python tools/simulate_campaign.py` from this game folder after import. Include Windows SDL/Pygame smoke tests. Historical 116 pure-Python tests passed during v0.5 construction; do not present these as new GitHub CI results.

## Import status
**Source imported.** All 76 source-archive files, including `main.py`, `mudpie/`, `tests/`, `assets/`, and Windows scripts, are present as individual Git objects on the import branch. The project remains an unverified pre-release until real Windows/Pygame and two-hour human testing. See `IMPORT_VERIFICATION.md`.

## Current agent identity / context

The current chat's assistant alias is **Mossbyte — ChatGPT GPT-6**, project-agent ID `MPM-MOSSBYTE-GPT6-001`, workstream alias `MPM-CHAT-20261109-A`. For a full and dated handoff, read [`AGENT_IDENTITY.md`](AGENT_IDENTITY.md) and [`PROJECT_MEMORY.md`](PROJECT_MEMORY.md). These are public **GitHub continuity records**, not an actual GitHub bot or guaranteed ChatGPT account memory. A later agent must use its own session identifier and may update memory only with supported evidence.

## v0.6 runtime reliability gate

Use `python tools/runtime_walkthrough.py --output qa-artifacts/runtime` (with SDL dummy video/audio drivers) as well as pytest and campaign simulation for future gameplay changes. The bot injects events through production `Game.step_frame()`, captures real Pygame frames, and checks first-mission progression and free-build saving. Check `QA_RUNTIME_v0.6.md` before interpreting results. Screenshots do not constitute an OS-level or human playtest. Preserve `game.json` gameplay-hours-verified=false until observed human playtime justifies changing it.
