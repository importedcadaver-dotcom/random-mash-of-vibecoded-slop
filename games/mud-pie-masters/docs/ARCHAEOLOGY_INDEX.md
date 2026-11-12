# Mud Pie Masters — Archaeology evidence index (initial baseline)

**Audit owner:** Mossbyte — ChatGPT GPT-6 / MPM-MOSSBYTE-GPT6-001  
**Snapshot:** November 11, 2026; main SHA 9d5bfc8d1985ab7b24a3139c320068c3ef1a3a22  
**Tracking:** [Issue #18 — archaeology](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/issues/18)  
**Status:** IN-PROGRESS EVIDENCE INDEX, not a completed exhaustive audit. A separate source-labeled Master GDD now exists; physical Windows/human release gate remains open.

This is a **navigation, provenance and exceptions index**, not a replacement for the already substantive project documents. The imaginary 20-year handoff is a method for skepticism, not the project's real age.

**Creative design and canon:** [Master Game Design & Canon Register](MASTER_GAME_DESIGN.md) is the sole forward-looking design reconstruction; it labels approved, implemented, rejected, deferred and unknown claims.
\n**Visual asset gallery:** [original sprite/expression contact gallery, historic previews and runtime provenance](ASSET_VISUAL_INDEX.md). This links all original tracked images directly without replacing them and distinguishes current judges from legacy judge files.

## 1. Source-of-truth order and how to avoid duplicate documents

1. **Latest explicit creator decisions** (including later corrections) govern creative direction; proposals from AI agents are not approvals.
2. **Current game source, automated tests and reproduced runtime behavior** establish implemented mechanics—not whether they are enjoyable.
3. [game.json](../game.json) records machine release/version metadata. Its two-hour flag is FALSE and is not inferred from content length.
4. [MASTER_GAME_DESIGN.md](MASTER_GAME_DESIGN.md) is the single source-labeled creative reconstruction; it does not override later creator corrections or the actual source. [PROJECT_MEMORY.md](../PROJECT_MEMORY.md) preserves dated approvals, limitations and change logs.
5. [README.md](../README.md) explains current features, controls and how to run the latest pre-release build.
6. [QA_REVIEW_2026-11-11.md](../QA_REVIEW_2026-11-11.md) describes the post-merge regression/CI evidence and known gaps.
7. [ART_DIRECTION.md](../ART_DIRECTION.md) and [GAMEPLAY_TARGET.md](../GAMEPLAY_TARGET.md) include historical proposals, some pre-v0.10 statements. Their dates matter. The original v0.4 research remains at [FUN_AUDIT_v0.4.md](FUN_AUDIT_v0.4.md); it must not override current code.
8. Existing [genre/review research](../GENRE_RESEARCH_AND_REVIEW.md) and [campaign QA](../QA_CAMPAIGN_v0.10.md) are reference reports, not proof of personal artistic or human playtime acceptance.

**Avoid parallel or competing master specs.** The Master GDD now fills the previously missing role; the other records retain historical, technical, QA or usage scopes. For each future claim, cite a creator decision, actual implementation/test, or clearly labeled proposal.

## 2. Evidence inventory (current audit pass)

| Source | Verified scope | Limits |
|---|---|---|
| GitHub tree at main SHA above | 122 repository tree entries; 102 game subtree entries including directories; all tracked paths located | Source files not all line-by-line reviewed yet |
| Game source | game.py (~88 KB), campaign.py, models.py, judging.py, rivals.py, rendering.py, save.py, initial tests and tooling | Performance on real desktop unknown |
| History | Relevant issues #2/#5/#9/#10 and merged PRs #1/#4/#6/#8/#11–17 | Other-game PRs are intentionally excluded |
| CI | Main Actions #43121174266 green on Windows and Linux: 174 pytest tests/OS, 26 headless SDL walkthrough screenshots, 48 oracle-assisted presentation/save/reload rounds | Dummy SDL; not OS mouse or audio testing; synthetic pies not real craft playtime |
| Packaging | Main Windows artifact run #43121174232 passed packaged EXE headless smoke | Physical device user-facing reliability not certified |
| Art | All 17 tracked PNGs inspected via SHA-matched archival bytes; five WAV sources inventoried; main Windows screenshot artifact #13899914721, 26 rendered frames | Runtime judge portraits are generated and may not match the tracked judge PNGs; owner has not accepted them |
| Owner context | Original Nov 8/9 development directive, pre-v0.5 fun audit, original Windows Chapter 1 spoken playtest, explicit correction on falling mud, newer proposed bear-cub sprite design brief | Other conversations and image generations not assumed exhaustive; do not publish full transcripts in a public repo |
| Outside research | Existing repo research plus Steam's SuchArt, Sticky Business, Passpartout 2 pages/reviews, Apple game-onboarding guidance | Genre analogies are hypotheses, not permission to clone another game's mechanics |

**Conversation-only assets:** current-main SHA-verified contact sheet and three current Windows runtime screenshot sheets were created as downloadable ChatGPT artifacts alongside this audit. They are **not** committed into GitHub by this Markdown PR. Preserve source run identifiers and original tracked PNGs.

## 3. Reconstructed game identity, with authority labels

| Statement | Classification | Evidence |
|---|---|---|
| Offline Windows Python 3.12 / Pygame CE mud-pie-building game, playing a cute baby brown bear | Approved creator intent; implemented | Original development directive, AGENTS.md, README |
| Six craft materials; scoop/mix, shape/flatten, stack, decorate; actual pie geometry determines outcomes | Approved baseline; implemented | Original directive; models.py/game.py |
| Bruno is competitive, Daisy playful; distinct reactions and persistent affinity, confidence and rivalry | Approved character identities; partially implemented in rivals.py | Owner praise; rivals.py |
| Three judges evaluate Size, Decoration, Symmetry, Originality and Integrity | Approved baseline; implemented | Original directive, judging.py |
| 36 story contests and 12 optional commissions across six chapters | Implemented scope, **not** evidence of 120 enjoyable minutes | campaign.py, QA |
| Falling mud YES; unsupported static floating mud NO | Latest explicit owner correction, partially implemented | Issue #9, PR #13, models.py |
| Mud squish, shape/flatten, Daisy/Bruno expressions are attractive features | Confirmed positive player feedback | First Windows Chapter 1 session |
| Petals/sticks may be reshaped, rotated and saved | Explicit user request; implemented | PR #14, Decoration fields in models.py |
| Existing Mud Pie Masters cub sprites are valued production placeholders; **Bruno** is the leading individual cuteness benchmark (preferred over player and Daisy) | Latest explicit creator preference; **new sprite replacements not approved** | Newer Nov 11 character-art feedback, after initial Windows feedback |
| Every mission is pleasurable, and two-hour duration has passed | **Unverified** (do not state as fact) | Issue #2 stays open |
| 20-year game history exists | **Fictional audit framing only** | Current directive |

## 4. Architecture and current risk register

- **High / maintainability:** game.py is ~88 KB and owns scene transitions, input, layout, animations, sound and gameplay coordination. This is a *coupling risk*, not proof that a rewrite would be safer. Inventory entry points and introduce seam-level tests before proposing a split.
- **Medium / historical scoring concern requiring rerun:** original v0.4 fun audit found a generic recipe effective across too many contests, bare tiers scoring 99 symmetry, and limited rotation effect. Current judging.py now caps bare symmetry, scores angle-aware pairs, applies repetition penalties and theme weights. **Do not repeat those old findings as current bugs without rerunning adversarial strategies**.
- **Medium / gameplay experience:** craft, judge and rival systems are largely deterministic, but actual player satisfaction, challenge variety and living sibling agency remain unverified. The former 48-round oracle bypassed mouse crafting; [PR #26's test](LEGAL_MOUSE_CAMPAIGN_QA.md) now proves 48/48 goal reachability by scripted SDL gestures, not human usability.
- **Medium / art approval:** current judges are programmatic color variants of cub art at runtime; the original tracked Petal/Boulder/Fern PNGs are NOT necessarily what the game presents. The user rejected generic teddy-bear judges in the first test. **Bruno is now the preferred reference**, despite Daisy also receiving earlier praise. Confirm new portraits at display size before claiming accepted.
- **Medium / text and layout:** current SDL screenshots show a much more structured interface than the first Windows build; their small text, visual density and resized behavior still require real human usability testing. Passing a screenshot generation check is not proof of legibility.
- **Low / stale documentation:** older ART_DIRECTION.md says UI labels are monospaced, while current rendering.py uses a minimum 14 px Verdana body font. Historical document should remain dated and be clearly tagged as not authoritative for current typography.
- **Resolved / metadata:** PR #19 corrected the obsolete game.json 20-screenshot description to the verified 26-screen main SDL-dummy walkthrough; keep future counts tied to specific run IDs.
- **Low / root instructions stale:** root AGENTS.md refers to branch protection still needing setup, but repository ruleset #26908579 is active and Issue #5 closed. Root is a shared file; coordinate before altering.
- **Resolved / determinism:** PR #19 merged sorted iteration for Daisy's borrowed ingredients and a cross-process PYTHONHASHSEED regression test. The original defect had been reproduced with 4 hash seeds.

### Current creator-art decisions — chronological correction

The first Windows playtest praised **both Bruno and Daisy's expressive characterization and designs**, but later comparative sprite feedback (November 11, 2026) established a more specific ordering: **Bruno is cuter than the player cub, and Daisy is the least cute of the three**. This later preference supersedes an earlier *Daisy-first* benchmark used during experimental art ideation; it does **not** revoke the favorable playtest observations or authorize deleting Daisy's assets.

- **Approved preference:** preserve all current Mud Pie Masters cubs as attractive, usable placeholders. Treat Bruno as the primary individual character-art reference. Aim for purposefully overlapping, asymmetric, individually shaped cutout/collage parts with clear attached limbs and readable expressions, rather than uniform circular/elliptical mascot construction. `South Park: The Stick of Truth` is a *structural visual analogy*, not permission to reproduce licensed characters.
- **Explicitly rejected:** both E1 face variants; all three E2 circular/lumpy silhouettes; blush added to new sprites. Relative praise for the wider eyes of one rejected E1 variant was **not** approval. Do not cite Bramble as a preferred art benchmark.
- **Unapproved / experimental:** any new E3 layered reconstruction, new judge portraits, replacements of production cub sprites, or quadruped variants. Standing and all-fours may both be explored later; neither a new pose nor a new E3 asset has cleared owner review.
- **Source boundary:** latest art feedback was recovered from creator-authored project history/notes outside this public repository. The detailed personal chat and unrelated image artifacts are **not** embedded here. This is a compact decision register, not a claim every historical conversation/image was recovered.

### Feature-to-implementation-to-test matrix (source inspection)

| Behavior | Production source | Relevant automated evidence | Unverified acceptance |
|---|---|---|---|
| Mud scoop, knead/workable threshold and finite-volume shape/flatten | `mudpie/models.py`, `mudpie/game.py` | `test_models.py`, `test_first_play_rescue.py`, `test_pygame_smoke.py` | Physical mouse feel, tutorial comprehension without coaching |
| Unsupported tier falling/cascades and continuing after collapse | `mudpie/models.py`, `mudpie/game.py`, `mudpie/rendering.py` | `test_falling_mud.py` (model + real queued SDL events) | Believable full contact/stacking on physical Windows; this is a center-support approximation, not soft-body physics |
| Petal/stick reshape, rotation, color picker and undo | `mudpie/models.py`, `mudpie/game.py`, `mudpie/rendering.py` | `test_decor_shape_v09.py`, `test_ui_controls_v07.py` | Discoverability and quality of actual artwork |
| Authored missions, unlock conditions and scoring objectives | `mudpie/campaign.py` | `test_campaign.py`, `test_campaign_pacing_v010.py` | Whether 48 contests avoid repetition for real people |
| Deterministic judges, geometry-aware scores, repeat penalties | `mudpie/judging.py` | `test_judging.py`, `test_fun_redesign.py` | Perceived fairness, exploit resilience with real legal mouse strategies |
| Sibling response, next-round pie design and relationship memory | `mudpie/rivals.py` | `test_rivals_save.py`, `test_daisy_determinism.py` | Whether Bruno/Daisy feel genuinely autonomous and distinct over extended play |
| JSON save history, recovery and campaign persistence | `mudpie/save.py` | `test_rivals_save.py`, `test_damaged_save_recovery.py`, `test_save_root_validation.py` (**merged PR #20**) | Real user save migration/compatibility; physical Windows re-test remains open |
| Menus, contextual guide, mouse hitboxes, aspect letterboxing | `mudpie/game.py` | `test_runtime_events.py`, `test_first_play_rescue.py`, `test_pygame_smoke.py` | First-time navigation, text readability, touch/OS mouse behavior |
| Full story loop, screenshots and Windows package | `tools/runtime_walkthrough.py`, `tools/challenge_bot.py`, `tools/legal_mouse_campaign.py`, GitHub Actions | 48 oracle-built Pygame contests **plus independent 48 SDL-event-built contest pies**, PR #26 (227 tests/OS); headless screenshots; Windows EXE smoke | Physical Windows/audio, full human discoverability, **120 meaningful active human minutes** |

**Interpretation:** a passing automated test establishes only what its assertions actually check. These links are a *coverage navigation map*, not a full independent review of test quality. Prior `FUN_AUDIT_v0.4.md` exploit findings require fresh reproduction against the current rules and input paths rather than automatic carryover.

## 5. Historical milestones (verified repo chronology)

- **Nov 8–9:** Creator's autonomous development directive set the concrete offline Windows/Pygame game fantasy, 6 materials, tactile tools, grounded scoring, and no paid dependencies.
- **Nov 8:** v0.4 historical fun audit showed serious concerns about two-hour depth, superficial recipes and judging exploits; it was a source-code/model analysis, not a human playtest.
- **Nov 9:** PR #1 imported v0.5 source; PR #4 added multi-agent identity/memory/governance; PR #6 introduced real SDL event walkthrough; PR #8 supplied 48 oracle-generated campaign rounds and a Windows EXE smoke build.
- **Nov 9/10:** First unscripted Windows test reached Chapter 1 first results and exposed mixing, text/goal collision, choice bias, early locked drying guidance, and artwork issues. User praised specific squish/shaping and sibling moments.
- **Nov 9–11:** PRs #11–15 integrated first-play fixes, UI controls, falling mud, art/decoration shaping, and four additional shape-based challenge conditions with local report timing.
- **Nov 11:** PR #16 repaired malformed save handling, title-report hint collision, and CI diagnostic dependencies. PR #17 corrected the root game status. Main ruleset is active and baseline main CI is green.
- **Nov 11 (later):** PRs #19–22 merged: archaeology evidence index, Daisy deterministic replay, non-object JSON root recovery, corrected Bruno-first art chronology, system/test coverage and preserved original asset gallery. PR #23 further repaired partial save recovery; Windows/Linux CI passed 192 tests per OS.
- **Nov 11 (late):** PR #26 adds separate scripted SDL mouse/keyboard construction for all 48 authored missions; no Pie injection. See [legal-input campaign QA](LEGAL_MOUSE_CAMPAIGN_QA.md). It bypasses chapter-map selection through a fixture and does not certify human play.
- **Current:** Human 120-minute completion, actual Windows/audio input and final subjective art acceptance remain open.

## 6. Genre research — transferable, not automatically approved

- [SuchArt — Steam](https://store.steampowered.com/app/1293180/SuchArt_Genius_Artist_Simulator/): physics/material response and a broad tool vocabulary; **candidate lesson** is that immediate material feedback should be inherently satisfying.
- [Sticky Business — Steam/reviews](https://store.steampowered.com/app/2303350/Sticky_Business/): player-made designs, customization and emotional customer stories; user reviews also describe ambiguous requests and limited feedback. **Candidate lesson**: recognize creative choices, avoid tedious quota loops.
- [Passpartout 2 — Steam](https://store.steampowered.com/app/1571100/Passpartout_2_The_Lost_Artist/): art commissions and critics; **candidate lesson**: explain judging and allow stylistic identity.
- [Apple Game Onboarding](https://developer.apple.com/app-store/onboarding-for-games/): teach short steps when relevant and allow early hands-on experimentation. **Candidate lesson**: retest the v0.7 tutorial with a new user, not merely verify a five-page panel exists.
- Existing [GENRE_RESEARCH_AND_REVIEW.md](../GENRE_RESEARCH_AND_REVIEW.md) provides Papa's Bakeria and community discussion context; avoid duplicating it unless source findings are new.

## 7. Next checkpoints and gates

1. Maintain merged PRs #19–23 (Daisy determinism, save recovery, art provenance/asset catalog and test coverage). Keep this index and [Master GDD](MASTER_GAME_DESIGN.md) synchronized with later verified corrections.
2. Recover remaining historical sprite generations with provenance; compare only at gameplay scale. Do not silently replace Daisy or use a generic mockup as a production asset.
3. Build a current feature-to-code-to-test matrix, actual scene-by-scene visual audit and reproducible profiling. Separate known bugs from aesthetic opinions.
4. **Goal reachability completed (narrow automated proof):** 48/48 contests constructed using actual legal SDL keyboard/mouse gestures (PR #26). **Still open:** adversarial judge-exploit and strategy testing under legal inputs, independent human usability, and the old v0.4 balance hypotheses.
5. Carry out independent human onboarding, audio/input and measured 120+ active-minute playtests, honoring the user's choice not to be the first forced tester.
6. Reconcile old spec/doc duplication, implement only verified high-impact changes in scoped PRs, and keep [Issue #18](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/issues/18) as the archaeology ledger.

**No code-quality cleanup should erase an owner-approved behavior without explicit authorization. No artifact in this index certifies enjoyment or an actual 20-year project history.**
