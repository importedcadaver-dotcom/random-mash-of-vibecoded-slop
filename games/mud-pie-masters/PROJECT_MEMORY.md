# Mud Pie Masters — Project memory / canonical handoff

**Recorded:** 2026-11-09 (America/Los_Angeles)
**Project:** `games/mud-pie-masters/` in `importedcadaver-dotcom/random-mash-of-vibecoded-slop`
**Coordinator alias:** Mossbyte — ChatGPT GPT-6 (`MPM-MOSSBYTE-GPT6-001`)
**Source conversation alias:** `MPM-CHAT-20261109-A` (human-readable workstream label, not a platform conversation ID)

> **Authority and precedence:** The actual GitHub source, tests, issue/PR history, and the owner's latest explicit decisions are authoritative. This is a compact continuity record, **not** a substitute for checking code. Mark unverified items as such and never invent acceptance.

## Owner's explicit decisions

- Build **Mud Pie Masters** as an offline Windows Python 3.12 / Pygame Community Edition game in a shared monorepo of many independent AI games.
- Player is a cute **baby brown bear** making decorative *inedible* mud pies. Two sibling rivals are Bruno (competitive older brother) and Daisy (playful younger sister).
- Core gameplay: manipulate six materials (mud, leaves, petals, pebbles, sticks, berries) using scoop/mix, shape/flatten, stack, decorate, and compete before three judges with differing tastes.
- The owner wants **at least two hours of meaningful gameplay before their first personal playthrough**. Don't pressure them to play an unverified build.
- The first visual designs were rejected as generic "AI slop." v0.4 redesigned baby cub sprites were judged **cuter and acceptable as a possible placeholder**, **not final art approval**. Preserve the improved cuteness target; do not reintroduce generic storybook AI look.
- The owner approved the game-design audit fixes and requested implementation. The v0.5 source is a **candidate**, not an accepted two-hour release.
- This game belongs in `games/mud-pie-masters/`, leaving other games untouched, with multi-agent branches, worktrees, PRs, and clear attribution.
- The owner requested an agent nickname plus version and distinct chat/project identifiers: **Mossbyte — ChatGPT GPT-6**, `MPM-MOSSBYTE-GPT6-001`, `MPM-CHAT-20261109-A`.

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
- Do **not** set `gameplay_hours_verified` to true without actual observed evidence.

## Working with many agents safely

- One isolated folder per game, branch + worktree per parallel task, PR integration; never allow multiple agents to share a checkout.
- Root instructions: `AGENTS.md`, `docs/MULTI_AGENT_WORKFLOW.md`, `docs/AGENT_REGISTRY.md`.
- Project instructions: `games/mud-pie-masters/AGENTS.md`, `AGENT_IDENTITY.md`, this file.
- Coordinate shared `mudpie/game.py` modifications and other overlapping work in issue/PR comments.
- **Repository protection is now active.** On 2026-11-09, ruleset #26908579 was verified active for `main` with required PRs, `agent-governance`, non-fast-forward/deletion protection, and no bypass actors. Issue #5 is closed. The connected GitHub integration still cannot **edit** rulesets.
- Do not store personal info or conversation transcripts here; this repository is **public**.

## Handoff checklist for each agent completing a task

Add a dated entry below with: task, author label, branch/PR, files changed, verified tests and environment, new decisions **explicitly approved by the owner** versus proposed ideas, outstanding issues, and next step. Do not overwrite old entries.

### 2026-11-09 — Mossbyte / agent identity and collaboration governance

- Established stable public names, identity registry, project memory, and documented enforcement instructions.
- Scope limited to documentation and collaboration mechanics; **no gameplay code or playtime claim changed**.
- GitHub branch/ruleset actual enforcement must be verified independently; documentation alone is not protection.

### 2026-11-09 — Mossbyte / v0.6 automated gameplay reliability

- Workstream: `MPM-CHAT-20261109-A/v0.6-reliability`; PR [#6](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/pull/6), branch `agent/mud-pie-masters/mossbyte-v06-runtime-qa`.
- **Implemented:** shared real-game SDL event dispatcher and frame step; automated mouse/keyboard/resize walkthrough with screenshot artifacts; additional Pygame event regression tests; legible full crafting-goal panel; full judge-comment panel; safer notification transitions; numeric star labels; fix for false chapter-completion message at progress zero.
- **Evidence as of latest checked run:** [GitHub Actions #42740408609](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/actions/runs/42740408609), 137 tests passed on Windows and Linux, campaign simulation passed, 20 actual SDL/Pygame screenshots and a trace of 186 injected events from Windows. Test used SDL dummy video/audio; screenshots are actual game renderings but **not physical Windows screen captures**.
- **Verified gameplay path:** title -> chapter -> clearing/siblings -> tutorial -> crafting with tools/decorations -> judging -> 3-star story advancement -> report -> map -> free-build save -> gallery -> resize and letterboxed click.
- **Not verified:** two hours of enjoyable human play, physical Windows display/input/audio, exe packaging, performance. `gameplay_hours_verified` remains **false**. The project is **v0.6.0-dev**, not a player-ready release. Continue to use Issue #2.
- **Documentation:** [`QA_RUNTIME_v0.6.md`](QA_RUNTIME_v0.6.md) includes reproducible commands, artifact links and findings.
- **No new game canon or final art approval introduced.** Previous v0.4 cub artwork remains a possible placeholder. All user-approved prior constraints preserved.

### 2026-11-09 — Mossbyte / external reviews, full-campaign QA & Windows build (PR #8)

- Workstream: `MPM-CHAT-20261109-A/full-campaign-and-windows-package`; branch `agent/mud-pie-masters/mossbyte-full-campaign-qa-20261109`.
- **Research**: looked at official descriptions and reviews of Papa's Bakeria, Sticky Business, SuchArt and Passpartout 2 plus CozyGamers discussions. Main priority from reviews is satisfying tactile creativity over repetitive ingredient quotas. [GENRE_RESEARCH_AND_REVIEW.md](GENRE_RESEARCH_AND_REVIEW.md).
- **Automated QA**: 138 tests passed on Windows and Linux; 48 Pygame scene/judging/presentation/save-reload cycles completed with 36 story and 12 side contests. Captured actual headless SDL screenshots including finale, scrapbook pages and restart. **All complex pie designs were constructed by the test oracle, not physically made through mouse gestures**. Existing v0.6 walkthrough exercises real SDL input and gestures for a sample round.
- **Build**: PyInstaller onedir Windows executable created and **headless smoke launched** on GitHub Windows CI. Actual EXE loads original art, draws and saves a free-build pie, successfully exits. Downloadable CI artifact supplied as **MudPieMasters-Windows-PreRelease.zip**; keep executable together with `_internal` assets.
- **Evidence**: [QA_FULL_CAMPAIGN_AND_BUILD.md](QA_FULL_CAMPAIGN_AND_BUILD.md); full run [#42744247759](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/actions/runs/42744247759); Windows executable [#42744247649](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/actions/runs/42744247649).
- **Limitations**: NO physical Windows manual or audio/fullscreen/hardware performance test, NO observed human full playthrough, and **NO verified 2-hour enjoyable first-play experience**. This is a **v0.6.1-QA pre-release**. Never tell the user it is ready for first play until evidence exists. `gameplay_hours_verified=false` remains in `game.json`.
- Existing cute baby cub art remains a provisional possible placeholder; game identity and other games untouched. No new unapproved canon.

### 2026-11-09 — Mossbyte / first human-playtest rescue, PR A

- Owner provided **direct real Windows first-session feedback** (Chapter 1, first contest and sibling presentations); primary account is [Issue #9](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/issues/9). Unlike the earlier simulated 48-round campaign, this was a real first-time user's interaction and revealed serious UX flaws.
- Tracking roadmap: [Issue #10](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/issues/10). **Explicit correction:** **falling mud YES, floating mud NO**; do not remove falling physics to hide unsupported tiers.
- PR A: [#11](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/pull/11), branch `agent/mud-pie-masters/mossbyte-v07-first-play-rescue-20261109`, modifies Chapter 1 title, choice fairness, compact tutorial, mixing guidance, observable KNEAD + MOISTURE bars, attainable UNDO recovery for soupy mud. New SDL event tests and mixing screenshot checkpoint. **No game art/falling physics fixes in PR A.**
- Code constraints: real clear-weather first scoop starts wetness **0.42**, rainy scoop **0.55**, model dataclass default **0.55**. Layer is workable after >=.30 work and moisture .42-.73; overmixing can revert it. Avoid recommending drying in Chapter 1; D remains locked until Chapter 4.
- Previously passing v0.6.1 automated QA still does NOT certify human enjoyment; player found tutorial, control, visual and physical-system problems in first actual session.
- Preserve praised parts: squish feedback, shape/flatten, cute Bruno/Daisy personalities, Daisy's decorations. Keep unfinished items in Issues #9 and #10; **do not mark the 2-hour goal complete**.
- Tests and PR status: see PR #11 Actions for the actual most recent results; document future PR B/C/D/E evidence separately, not by assuming PR A covers them.

### 2026-11-09 — Mossbyte / PR B: UI and controls (first-play recovery)

- Branch `agent/mud-pie-masters/mossbyte-v07-ui-controls-20261109`, [PR #12](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/pull/12), following merged PR A #11.
- Compact goal sidebar no longer renders clipped 10px full labels and overlapping values; it shows goal count/status while the full description remains in `VIEW GOALS`.
- Replaced color cycling-only mouse UI with clickable swatch picker. Keyboard C still cycles. Added **visible undoable Rotate Last (R)**; Undo/Redo moved into editing cluster, destructive Start Over requires Pause/Settings confirmation, and Help stays visible.
- Results medal badge moved into top-right header to avoid overlapping third competitor's score card.
- Fixed CodeRabbit PR A guide navigation page-count clamp (uses actual `len(pages)`).
- Verified first run: [CI #42752180885](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/actions/runs/42752180885): **149 pytest tests passed on Windows and Linux**, event walkthrough and full 48-round oracle-assisted runtime passed. [Windows EXE #42752180893](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/actions/runs/42752180893) smoke passed. Added new screenshot checkpoints for color swatches and Rotate; use latest PR head CI for final confirmation.
- The full 2-hour enjoyable human release criterion is still **unverified**, falling mud, fonts, sprite clipping, judge art and petal/stick reshaping remain open. Do not close [Issue #9](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/issues/9) before real retest.
