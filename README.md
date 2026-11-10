# Random Mash of Vibecoded Slop

A collection of small, standalone games built with AI coding agents.

## Games

| Game | Status | Location |
|---|---|---|
| Clash of Cubs | Playable prototype | [`games/clash-of-cubs/`](games/clash-of-cubs/) |
| Mud Pie Masters | v0.5 source imported; Windows/two-hour verification pending | [`games/mud-pie-masters/`](games/mud-pie-masters/) |

## Working with agents

Read [`AGENTS.md`](AGENTS.md) before starting. Each game owns a separate folder and has its own agent instructions. Use a distinct branch and Git worktree per chat or agent, keep changes scoped to one game, and use pull requests for integration.

**Agent workstreams:** `Codex / clash-of-cubs / playable-prototype` (existing); `ChatGPT GPT-6 / mud-pie-masters / import-v0.5` (new). These identify contributions, not separate authenticated GitHub users. See [collaboration workflow](docs/MULTI_AGENT_WORKFLOW.md).

## Agent roster and long-term project notes

- [Agent registry](docs/AGENT_REGISTRY.md) — separate workstream identities across games.
- [Mud Pie Masters project memory](games/mud-pie-masters/PROJECT_MEMORY.md) — approved decisions, implementation status, release gates, and handoff.
- [PR governance](.github/workflows/agent-governance.yml) — always-on attribution and cross-game scope check.
- [GitHub branch protection setup](docs/BRANCH_PROTECTION_SETUP.md) — GitHub Settings action still required before these process rules are enforced on `main`.
