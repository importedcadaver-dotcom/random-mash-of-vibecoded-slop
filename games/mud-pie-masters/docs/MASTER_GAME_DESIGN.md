# Mud Pie Masters — Master Game Design & Canon Register

**Edition:** retrospective v0.10 source-of-truth reconstruction, November 11, 2026 (Pacific).  
**Implementation baseline:** game version `0.10.0-dev` with inspected main after PR #23 (`6e4b632`).  
**Status:** **reconstructed working document, NOT a fresh creative approval, release certification, or assertion of completeness**.  
**Game:** offline, single-player Windows Python 3.12 / Pygame Community Edition.  
**Owner of creative direction:** the project's human creator; an AI may document and implement approved decisions but cannot silently replace them.

## 1. How to interpret this document

For every material design claim, use these labels:

- **[APPROVED]** Explicitly requested, decided, corrected or accepted by the creator. A later explicit correction supersedes earlier proposals.
- **[IMPLEMENTED]** Present in the inspected production code, not necessarily proven delightful in an independent human test.
- **[OBSERVED]** Actual player feedback or measured CI/runtime evidence, with its limited scope.
- **[PROPOSED]** Candidate design or engineering change only; requires a decision before altering core creative behavior.
- **[REJECTED]** Explicitly declined or visually rejected; do not revive without a new instruction.
- **[DEFERRED] / [UNKNOWN]** Not decided or not established from the inspected sources. Do not invent facts.

**Evidence precedence:** latest creator statements and corrections for creative canon; production code and reproducible tests for actual behavior; issues and versioned history for dated context. A historical audit is not an acceptance of all its suggestions.

Companion sources: [archaeology/provenance index](ARCHAEOLOGY_INDEX.md), [original asset gallery](ASSET_VISUAL_INDEX.md), [project memory](../PROJECT_MEMORY.md), [first human playtest Issue #9](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/issues/9), and [release gate Issue #2](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/issues/2).

## 2. Game identity and core promise

**[APPROVED]** Play as an adorable, expressive baby brown bear creating **decorative, inedible mud pies** and competing against two siblings, Bruno and Daisy, before woodland judges. Make it a genuinely interactive crafting game, not a text checklist masquerading as a game. Preserve charming cub personalities, humorous family competition, tactile squishing and physically meaningful shaping.

**[APPROVED + OBSERVED]** The human first-session feedback positively identified mud squishing, the original Shape/Flatten interaction, Bruno's facial/emotional expressiveness, Daisy's personality/designs and useful judge commentary. These successes are to be protected while fixing confusion around mixing, control discovery and menus.

**[APPROVED]** Target at least **two hours of meaningful gameplay** before the creator is asked to treat the game as ready for their own first full playthrough. The requirement is a release-validation gate—not permission to pad with waiting or repetitive quotas.

**[IMPLEMENTED]** A chapter-based, offline single-player adventure with a craft bench, competition presentation, results, unlocks, optional commissions, free build, gallery and finale. Its content length does **not** prove 120 enjoyable active minutes.

### Design pillars (restated from explicit requirements; not new features)

1. **Tactile mud:** Players can visibly scoop, mix, shape, flatten and stack actual pie geometry, with understandable response.
2. **Physical consequence:** Unsupported mud **falls under gravity** and settles or collapses; unsupported static floating tiers are unacceptable.
3. **Expressive bear family:** Cub art and reactions should be distinctive and endearing. Rival behavior should depend on character and history, not merely score labels.
4. **Legible creative evaluation:** Different construction approaches should matter, judges should have explainable preferences and criticism should help players learn.
5. **Agency without false playtime:** Have actual craft freedom, optional commissions and free build; test meaningful engagement with real people.

## 3. Existing player journey

**[IMPLEMENTED]** As shown in `mudpie/game.py` and `mudpie/campaign.py`:

1. Start or continue the story, visit the chapter map, or select free build.
2. Enter an authored contest, see its theme, judge priorities and construction goals.
3. Encounter the siblings at the clearing. Where appropriate, make an optional chapter-wide Encourage/Challenge choice and a separate per-sibling Cheer/Dare interaction. These are **two different systems**.
4. Use the workbench to build and modify mud geometry and arrange five decorative materials.
5. Submit the pie; view the player's and siblings' actual constructed entries in presentation and their individual judging comments.
6. See score, feature breakdown, winner, mission goals and medal results. Save the pie into the scrapbook.
7. If the published construction goals are fulfilled, story progression can advance; otherwise the current contest can be retried. Visit optional commissions and unlocked chapters as they become available.

**[IMPLEMENTED]** Free build is a no-points construction mode with scrapbook saving and no obligatory quest goals. The game retains a pause/settings menu, reopenable tutorial, undo/redo and local save state.

**[UNKNOWN]** How independently a fresh player understands this loop at first contact after recent UI fixes. Source-level and SDL-event tests do not substitute for the human first-time retest.

## 4. Crafting, ingredients and physics

**[APPROVED + IMPLEMENTED]** Exactly six base materials: **mud** (tier construction) plus **leaves, petals, pebbles, sticks and berries** (decoration). The pies and berries here are craft/game materials, not an eating mechanic.

**[APPROVED + IMPLEMENTED]** Four central tools: **Scoop/Mix, Shape/Flatten, Stack, Decorate**. Visible color palette selection, rotation, undo/redo, Help and chapter unlocks supplement them. The explicit request to shape/flatten **placed petals and sticks** was implemented in PR #14; their size modifications persist in saves and are undoable.

**[IMPLEMENTED]** Model in `mudpie/models.py`:

- Each mud scoop has a material volume; reshaping changes height/width while conserving that scoop's volume. There is a maximum of seven total layer objects and 120 decorations.
- Mixing increases worked/kneaded state and wetness. A workable band balances improved handling against oversaturation; the workbench shows knead and moisture separately.
- An upper layer whose center is outside the lower supporting layer's horizontal footprint transitions to a fallen state; falling/cascading animations are rendered and fallen debris remains. Undo restores previous pie state. The implementation is **a deterministic center-support approximation**, not a real soft-body/rigid-body solver.
- Wind and rain affect actual stability/conditions; a separate presentation collapse model evaluates weakened structures.
- Decorations attach to layers; the five categories differ in appearance and score-relevant mass/arrangement. Original artwork, sprites and gravity behavior must not be replaced casually.

**[APPROVED]** Desired physical principle is **falling YES, unsupported hovering NO**. Do not reinterpret that correction as an instruction to disable gravity.

**[DEFERRED]** Whether more granular adhesion, partial collapse, collision or soft-body fidelity is desirable. Such changes require visual proof and user creative review, not speculative physics rewrites.

## 5. Contests, scoring and fairness

**[IMPLEMENTED]** Three named judges with distinct weights: **Petal** (decoration emphasis), **Boulder** (large/tall pie emphasis), **Fern** (symmetry emphasis). See `mudpie/judging.py`. Each evaluates five disclosed features: **Size, Decoration, Symmetry, Originality, Integrity**.

**[IMPLEMENTED]** Current scoring is deterministic and depends on actual pie geometry/decorations, theme and recent signatures. A contest's announced feature is given substantial weight (65%); individual judge preferences influence the remainder. Mirrored patterns, decoration distribution and material variety contribute; bare mud does not earn high intentional-symmetry credit. Repeated design signatures incur a visible penalty. Judges give character-specific comments, and the result screen exposes component scores.

**[IMPLEMENTED]** Published challenge goals and judge score are different gates: a pie with goals fulfilled receives at least **two medals/stars**; meeting the contest score target as well earns **three**. A submitted pie lacking goal completion receives **one**. Main-story advancement requires fulfilled construction goals, not victory over both siblings. A zero-tier pie cannot be submitted.

**[OBSERVED]** First-session player feedback considered a judge's suggestion about color/clusters understandable, even though the player's score and three-star threshold needed better communication.

**[HISTORICAL, NOT CURRENT BUG CLAIM]** The v0.4 stress audit identified generic-template dominance, excessive bare symmetry, irrelevant angles and nonconserving mud. The v0.5 implementation addressed several of these and its **data-model** stress report found 12 of 48 goals met by an unchanged template and distinct strategy performance. Both sets of results are historical model evidence, **not** a legality-checked current mouse strategy or proof of human fun. Preserve regression tests but rerun adversarial gameplay analysis before introducing new balance changes.

## 6. Family characters, rivals and behavioral scope

**[APPROVED]** Main player: baby brown bear with an approachable expressive presence. **Bruno:** older, bold, competitive brother. **Daisy:** younger, playful/imaginative sister whose creative presentations and shy moments matter. Do not discard the established identities for generic NPCs.

**[IMPLEMENTED]** `mudpie/rivals.py` creates actual pie objects for both competitors, not magic predetermined scores. Bruno's generator tends toward taller/riskier constructions; Daisy favors decorative combinations and mirrored petal-like patterns. Rival state stores affection, confidence, rivalry, wins/losses, embarrassment and a bounded list of memories. Chapter-level choices and per-sibling interactions affect some state and next-entry generation; prior player pie ingredients can influence Daisy. Both rivals are evaluated by the same judge pipeline as the player.

**[IMPLEMENTED LIMITATION]** Rival designs are largely generated for a contest before actual player crafting, with reaction/regeneration after limited interactions. This is **not a full independently simulated cub AI with continuous visible goals, pathfinding or autonomous conversations during every mouse action**. Do not claim that such rich behavior exists merely because personality variables are stored.

**[DEFERRED]** Whether to deepen visible independent activities, memories, relationships or family story consequences—and which exact mechanics to add. No AI may add a new major personality or relationship arc without creative authorization.

## 7. Authored progression and chapter outline

**[IMPLEMENTED]** Six chapters, **36 main story contests** (six per chapter) and **12 optional woodland commissions** (two per chapter). Current names are:

| Chapter | Existing theme | Gameplay context |
|---|---|---|
| 1. The First Puddle | Introduction to the sibling contest | First scoop, mixing, forms and goals |
| 2. The Petal Picnic | Forest picnic and decorations | Patterns and mirrored arrangements |
| 3. Rocky Ridge | Uphill construction | Tall pieces, wind and support |
| 4. Storm Season | Rain and mud handling | Wetness, stability and drying |
| 5. The Moonlit Fair | Nighttime woodland fair | Color, arrangement and expressive details |
| 6. The Golden Mud Cup | Final competition | Multi-skill craft mastery and sibling payoff |

**[IMPLEMENTED]** Two initial decoration color variants, further colors by completed chapters up to six; mirror-placement unlock after Chapter 1 (six story rounds); drying unlock during Chapter 4 (after 18 story rounds). There are six chapter keepsakes, a scrapbook, optional commissions and finale. Later briefs include real petal/stick transformation goals, not just unmodified object counts.

**[PROPOSED / NOT AUTHORIZED]** Additional chapter formats, commission types, physical minigames, time gates, new economy or narrative branches. These may be researched but are not part of approved canon absent owner approval.

## 8. Visual and audio identity

**[OBSERVED / APPROVED]** The v0.4 cub art was accepted as a **genuinely appealing usable placeholder**, not the final production art. Later comparative creator feedback established **Bruno as the strongest individual cuteness reference**, followed by player and Daisy. Earlier positive remarks about Daisy's character/art remain valid, but the old Daisy-first replacement benchmark has been superseded.

**[APPROVED PREFERENCE]** For any future sprite study, favor a deliberately layered **cutout/collage appearance**: purposeful overlapping masses, clear shoulder-to-paw anatomy, low short ears, asymmetry and expressive faces. The creator cited `South Park: The Stick of Truth` as an example of cutout construction, **not** a request to copy its characters.

**[REJECTED]** Generic circular mascot/teddy-bear replacement art, E1 face variants, E2 circular/lumpy silhouette experiments, unrequested blush stickers on new cubs, and treating a generated static mockup as an editable or production-ready sprite. Bramble was **not** the positive anatomy benchmark. E3 reconstruction and alternative quadruped poses remain **unapproved studies**.

**[IMPLEMENTED]** The game includes twelve tracked player/Bruno/Daisy PNG expression frames, three legacy judge PNGs, a forest and table background, and five WAV files. Current judge appearance is assembled programmatically at runtime from cub-style imagery and need not match the legacy judge PNGs. Original files, visual history and source/preview distinctions are indexed in [ASSET_VISUAL_INDEX.md](ASSET_VISUAL_INDEX.md).

**[UNKNOWN]** Current judge-art acceptance, physical Windows text sharpness/resizing, aesthetic reaction to the pale Chapter 1 area, animation feel, sound quality and input feedback after the newest fixes. SDL-dummy screenshots are valid render evidence, not human acceptance.

## 9. QA and release acceptance

**[IMPLEMENTED EVIDENCE]** Windows/Linux Python tests, SDL event-driven walkthroughs, a 48-round **oracle-built** Pygame judging/save sequence, screenshot artifacts, and Windows PyInstaller package with dummy-SDL smoke. See [current QA history](../QA_REVIEW_2026-11-11.md), later PR checks and [archaeology Issue #18](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/issues/18). These establish tested execution paths, not a full two-hour personal experience.

**[NOT SATISFIED]** Actual physical Windows mouse, keyboard, audio, focus/resizing/DPI/latency checks; first-time blind onboarding; broad design-acceptance review; and an **independently observed 120-active-minute enjoyable playtest**. The release flag must remain `gameplay_hours_verified=false` and the human release issue **#2 must remain open**.

**[REQUIRED PROCESS]** Preserve originals and approved rules. Every code change needs a source-verified defect or authorized goal, focused regression, protected PR with per-platform evidence, and clear scope. Do not claim a synthetic run has tested what it did not test.

## 10. Open decisions and prohibited silent assumptions

| Question | Status | Next acceptable evidence/action |
|---|---|---|
| Is current judge art finally cute and consistent enough? | **[UNKNOWN]** | Actual gameplay-size side-by-side review; do not overwrite tracked PNGs without approval |
| Is the newest tutorial understandable to a true first-time player? | **[UNKNOWN]** | Observe an independent user completing Contest 1 with real mouse/keyboard |
| Are judging scores and goals fair under legal, chapter-available mouse inputs? | **[UNKNOWN]** | New adversarial tests plus actual player strategy observations |
| Is the full 48-contest campaign sufficiently varied? | **[UNKNOWN]** | Real full progression playtest, not simply an oracle-built counter |
| Should siblings have deeper autonomous behavior? | **[DEFERRED]** | Present concrete simulated behavior/prototypes for approval before core changes |
| Should mud physics become a larger collision/soft-body engine? | **[DEFERRED]** | Demonstrate concrete failing current interactions and compatible previews |
| Should new sprite experiments replace the original cubs? | **[DEFERRED]** | E3 editable source, neutral same-size comparison and explicit approval |
| Is the game eligible for a two-hour release claim? | **[NOT VERIFIED]** | Physical Windows QA and observed 120 meaningful active minutes with qualitative feedback |

**No claims are made about specific cub ages, hidden canon, future story arcs, multiplayer, paid monetization or features not supported by the sources inspected.** Leave such matters undefined.

## 11. Ownership and maintenance

This is the **single forward-looking creative/gameplay design register**. It supplements rather than overwrites:
- `../PROJECT_MEMORY.md`: chronological owner decisions and agent handoffs;
- `ARCHAEOLOGY_INDEX.md`: source inventory, evidence ledger, risks and historical validation;
- `../README.md`: installation, actual controls and current build information;
- `../GAMEPLAY_TARGET.md`: dated two-hour requirement and its proposed measurement gate;
- `../ART_DIRECTION.md` and `FUN_AUDIT_v0.4.md`: useful **historical** art/design analyses, not later creative approvals.

Only revise approved-canon entries with a later explicit owner decision and date. Update implemented behavior after verifying a merged code change. Keep uncertainty visible rather than filling it with invention.