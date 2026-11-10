# AI agent registry — Random Mash of Vibecoded Slop

This is the **public, repo-local attribution registry**. Its records are descriptive labels for workstreams, **not** authenticated GitHub bot accounts, model guarantees, or proof of long-term ChatGPT memory.

| Project | Agent / version | Stable project-agent ID | Current workstream | Notes |
| --- | --- | --- | --- | --- |
| Mud Pie Masters | **Mossbyte — ChatGPT GPT-6** | **MPM-MOSSBYTE-GPT6-001** | \`MPM-CHAT-20261109-A\` | This conversation's assistant alias; new work must carry a task suffix and branch |
| Mud Pie Masters | ChatGPT GPT-6 | \`MPM-IMPORT-V05\` | Original v0.5 import | Historical label: \`ChatGPT GPT-6 / mud-pie-masters / import-v0.5\` |
| Clash of Cubs | Codex | \`COC-CODEX-LEGACY\` | Existing playable prototype | Historical descriptive label, **not** a claim of persistent Codex identity |

## Identity rules

- Every PR must declare **Agent name**, **model/version as reported in that session**, **game ID**, **workstream/session label**, **task**, **owned file paths**, **tests run**, and **verification still missing**.
- New assistants should choose a distinct agent instance/session label. Do not impersonate Mossbyte's session, other agents, or a GitHub account.
- Agent names are optional nicknames; identity is established by commits, PRs, and GitHub account metadata, not by self-reported names.
- Keep **one game per \`games/<slug>/\`**; each game owns its \`AGENTS.md\`, \`game.json\`, and \`PROJECT_MEMORY.md\` where applicable.
- Don't publish private chat transcripts, access tokens, personal Windows paths, private assets, or sensitive user details in this public repository.
- If a model version or task changes, append a dated handoff entry; never silently rewrite historical attribution.
- See [multi-agent workflow](MULTI_AGENT_WORKFLOW.md) and [branch protection setup](BRANCH_PROTECTION_SETUP.md).

## Mossbyte workstream

- Public name: **Mossbyte**
- Model: **ChatGPT GPT-6** (as named by the assistant for this chat)
- Stable project-agent ID: **MPM-MOSSBYTE-GPT6-001**
- Chat/workstream label: **MPM-CHAT-20261109-A** (human-authored alias, **not** an OpenAI conversation ID)
- Game/project: \`mud-pie-masters\`
- Working branch (for this task): \`agent/mud-pie-masters/mossbyte-identity-20261109\`
- Canonical game memory: [\`games/mud-pie-masters/PROJECT_MEMORY.md\`](../games/mud-pie-masters/PROJECT_MEMORY.md)
- Canonical agent details: [\`games/mud-pie-masters/AGENT_IDENTITY.md\`](../games/mud-pie-masters/AGENT_IDENTITY.md)

**Note:** This repository file enables reliable *retrieval* of project context. It does not alter or guarantee ChatGPT's product Memory feature.
