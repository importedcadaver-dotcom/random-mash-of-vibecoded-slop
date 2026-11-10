# Mud Pie Masters — Project memory / canonical handoff

**Recorded:** 2026-11-09 (America/Los_Angeles)
**Project:** \`games/mud-pie-masters/\` in \`importedcadaver-dotcom/random-mash-of-vibecoded-slop\`
**Coordinator alias:** Mossbyte — ChatGPT GPT-6 (\`MPM-MOSSBYTE-GPT6-001\`)
**Source conversation alias:** \`MPM-CHAT-20261109-A\` (user-authored workstream label, not a platform conversation ID)

> **Authority and precedence:** The actual GitHub source, tests, issue/PR history, and the owner's latest explicit decisions are authoritative. This is a compact continuity record, **not** a substitute for checking code. Mark unverified items as such and never invent acceptance.

## Owner's explicit decisions

- Build **Mud Pie Masters** as an offline Windows Python 3.12 / Pygame Community Edition game in a shared monorepo of many independent AI games.
- Player is a cute **baby brown bear** making decorative *inedible* mud pies. Two sibling rivals are Bruno (competitive older brother) and Daisy (playful younger sister).
- Core gameplay: manipulate six materials (mud, leaves, petals, pebbles, sticks, berries) using scoop/mix, shape/flatten, stack, decorate, and compete before three judges with differing tastes.
- The owner wants **at least two hours of meaningful gameplay before their first personal playthrough**. Don't pressure them to play an unverified build.
- The first visual designs were rejected as generic "AI slop." v0.4 redesigned baby cub sprites were judged **cuter and acceptable as a possible placeholder**, **not final art approval**. Preserve the improved cuteness target; do not reintroduce generic storybook AI look.
- The owner approved the game-design audit fixes and requested implementation. The v0.5 source is a **candidate**, not an accepted two-hour release.
- This game belongs in \`games/mud-pie-masters/\`, leaving other games untouched, with multi-agent branches, worktrees, PRs, and clear attribution.
- The owner requested an agent nickname plus version and distinct chat/project identifiers: **Mossbyte — ChatGPT GPT-6**, \`MPM-MOSSBYTE-GPT6-001\`, \`MPM-CHAT-20261109-A\`.

## Implemented in v0.5 source (verify current code before repeating claims)

- 6 chapters, 36 authored main contests, 12 optional commissions; story and free-build, judges, sibling state, save system, core actions, headless automated tests.
- Design changes claimed and tested during v0.5 creation: mud-volume conservation during shaping; kneading improves cohesion but over-wet mud loses stability; reduced empty-tier symmetry bias; competition theme impacts judge weights; sibling encouragement/dare affects next entry; more challenge objectives and particles.
- Source imported to GitHub as individual files with CI for Windows and Linux headless Pygame.
- Historical test results: 116 pure-Python tests at v0.5 construction; previous GitHub Actions headless tests reported 131 passing on both Windows and Linux. These are **historical observations**, not fresh tests or human playtime verification.

## Known gaps / non-negotiable release gate

- **NOT VERIFIED**: two enjoyable hours of real gameplay. 48 contests and scripted simulations are not sufficient evidence.
- **NOT VERIFIED**: full manual Windows visual/sound/input playthrough, actual frame-rate, packaging of a confirmed working Windows executable.
- The project may contain usability problems despite passing deterministic tests; treat this as a pre-release candidate.
- GitHub Issue [#2 — Windows playability and two-hour validation](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/issues/2) tracks the acceptance gate.
- Future priority: run real Windows Pygame and PyInstaller checks, collect truthful screenshots and time measurements, watch first-time user behavior (without requiring the owner to be the first tester), and only then decide readiness.
- Do **not** set \`gameplay_hours_verified\` to true without actual observed evidence.

## Working with many agents safely

- One isolated folder per game, branch + worktree per parallel task, PR integration; never allow multiple agents to share a checkout.
- Root instructions: \`AGENTS.md\`, \`docs/MULTI_AGENT_WORKFLOW.md\`, \`docs/AGENT_REGISTRY.md\`.
- Project instructions: \`games/mud-pie-masters/AGENTS.md\`, \`AGENT_IDENTITY.md\`, this file.
- Coordinate shared \`mudpie/game.py\` modifications and other overlapping work in issue/PR comments.
- The GitHub integration **cannot currently edit repository rulesets or branch-protection settings**. Public-ruleset read reported none as of this record. See \`docs/BRANCH_PROTECTION_SETUP.md\` for the owner action still needed.
- Do not store personal info or conversation transcripts here; this repository is **public**.

## Handoff checklist for each agent completing a task

Add a dated entry below with: task, author label, branch/PR, files changed, verified tests and environment, new decisions **explicitly approved by the owner** versus proposed ideas, outstanding issues, and next step. Do not overwrite old entries.

### 2026-11-09 — Mossbyte / agent identity and collaboration governance

- Established stable public names, identity registry, project memory, and documented enforcement instructions.
- Scope limited to documentation and collaboration mechanics; **no gameplay code or playtime claim changed**.
- GitHub branch/ruleset actual enforcement must be verified independently; documentation alone is not protection.
