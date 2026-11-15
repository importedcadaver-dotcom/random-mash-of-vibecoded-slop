# Little Cub agent instructions

Read the repository-root AGENTS.md, this file, the rebuild directive, and the baseline audit before editing the game.

- Work only under games/little-cub/ unless the repository owner explicitly approves a shared-file change.
- Use an isolated branch and PR, following the root-required agent/model/game labels. Never push directly to main.
- Preserve the user's approved cozy-horror concept and all listed requirements. If a design choice is unspecified, choose a configurable default, document it, and do not silently change already approved mechanics.
- The game must remain playable without paid assets, paid APIs, a login, or recurring costs.
- Distinguish real-browser playtesting from mocked simulation tests. Do not claim a feature, screenshot, or playtime was verified unless it actually was.
- Keep main-screen health/energy/hunger math hidden in normal play; a clearly labeled developer/QA diagnostics overlay may expose values.
- Treat violence, predation, drugs, and cannibalism as fictional simulation systems. Do not include real-world preparation/dosage instructions for drugs or weapons.
- No unearned success: every player action has spatial, temporal, animation, resource, witness, and/or behavioral consequences.
- Do not import unrelated project canon without a separate explicit user decision.
- Ship incremental end-to-end playable slices and keep save migration and regression tests intact.

Workstream: ChatGPT GPT-6 / little-cub / rebuild-directive — LC-20261114-REBUILD-A.
