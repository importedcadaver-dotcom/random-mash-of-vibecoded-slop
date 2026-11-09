# MUD PIE MASTERS · Gameplay Rescue Edition v0.5.0

A fully offline Windows desktop crafting/competition game for Python 3.12 and **Pygame Community Edition**. Play as a baby brown bear competing with sibling cubs Bruno and Daisy. Nothing in the mud-pie contest is edible.

## Release status (read before playing)

**v0.5.0 is a redesigned gameplay-and-balance candidate with v0.4 provisional baby-cub artwork, NOT a verified two-hour release.** It has 36 unique main story contests, 12 optional woodland commissions, six chapters, chapter dialogue choices, scores, medals, weather challenges, a small unlock system, a free-build mode, and a finale. There are no artificial countdowns, stamina waits, or paywalls.

**Content target:** at least two hours of meaningful first-time gameplay for a typical player who completes the story and commissions. The content plan would reach 120 minutes at an **assumed** average of 2.5 minutes per 48 contests; this is only an illustrative planning assumption, **not a measured completion time**. Actual duration varies based on skill, retry attempts and design exploration. A human playthrough on Windows is still required before promising a two-hour experience.

The project was built in a sandbox that cannot install pygame-ce or launch a Windows window. Python logic tests ran successfully; the graphical interaction smoke tests are shipped but need execution on your Windows PC. No genuine gameplay FPS, sound playback, or real input latency was measured here. See `QA_REPORT.md`, `ART_DIRECTION.md` and `GAMEPLAY_TARGET.md`.

## Install/update on Windows

The earlier setup was completed at `C:\Users\theam\MudPieMasters\.venv` with Python 3.12 and pygame-ce. **Keep that `.venv`**; the new ZIP contains source and assets, not its own Python environment.

1. Download `MudPieMasters-v0.5.0.zip`.
2. Extract the **contents** into `C:\Users\theam\MudPieMasters` (allow source file replacement). Back up your own edited source first, if you modified the previous version.
3. In PowerShell, run the automated test command below. When ready to play, double-click `play.bat` or use the direct Python launch command.

```powershell
Set-Location "$HOME\MudPieMasters"
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe tools\simulate_campaign.py
.\.venv\Scripts\python.exe main.py
```

The launch command is optional until you are ready to play. These tests **do not require** you to play the game, and the Pygame smoke tests are designed to work with SDL dummy video/audio drivers.

If dependencies are missing, `powershell -ExecutionPolicy Bypass -File .\setup.ps1` installs them. An optional Windows PyInstaller build script is at `build_windows.ps1`. The resulting `.exe` was not built/validated here.

## What the story includes

| Chapter | Six main contests | Two optional commissions | New focus |
|---|---|---|---|
| 1. The First Puddle | Early sculpting, patterns, small towers | Beetle's Pebble Hotel / Mama's Leaf Basket | Four tools and essential skills |
| 2. The Petal Picnic | Floral crowns, leaves-only designs, picnic art | Rabbit's Flower Stand / Picnic Table Parade | **M** twin-decoration shortcut; more colors |
| 3. Rocky Ridge | Wind, structural balance, wide supports | Mossy Miniature / Badger's Bridge | Unusual silhouettes and wind penalties |
| 4. Storm Season | Rain-softened mud, careful supports | Duckling's Umbrella / Stormy Color Test | **D** gentle mud-drying technique |
| 5. The Moonlit Fair | Mirrored patterns, starry designs, many colors | Owl's Moon Dial / Firefly Welcome | Night atmosphere and creative precision |
| 6. The Golden Mud Cup | Finals, towers, sibling homage, grand finale | Auntie's Trophy Stand / Secret Sibling Gift | Final mastery, awards and ending |

The campaign contains **48 authored contest briefs**, each with at least two actual craft goals. Later contests may restrict ingredients. There are 144 possible stars across all challenges. Win/loss scores are still calculated from the same physical pie model as in v0.1.

**How progression works:** A contest awards one star for a submitted attempt, two for completing all its listed design goals, and three for completing all goals **and** reaching the contest's published score target. You must earn two stars on the current story contest to unlock the next. You **do not have to beat Bruno or Daisy**. Goal progress is visible while crafting; after judging, open **CHALLENGE REPORT** to understand which goals passed. Replays can improve your medal record without revoking previous stars.

## Main controls

| Action | Input |
|---|---|
| Add mud tier | Drag mud from the ingredient tray onto the table; each scoop supplies fixed mud volume |
| Scoop / Mix | 1; drag across a tier to knead it. Some mixing improves strength; excessive stirring makes it soupy |
| Shape / Flatten | 2; drag sideways to spread/flatten, or up to thicken/narrow the SAME amount of mud; right-click to change shape |
| Stack | 3; drag tier sideways to offset it, or up to reorder |
| Decorate | 4; drag leaves, flower petals, pebbles, sticks or berries onto a tier; drag existing decorations to move |
| Remove decoration | Right-click an existing decoration |
| Rotate last decoration | R |
| Choose decoration color | C or the COLOR button; more colors unlock during Chapters 1–4 |
| Twin mirrored decoration placement | M, unlocked after finishing Chapter 1; requires off-center placement |
| Dry mud | Hover over a tier and press D; unlocked in Chapter 4 |
| Undo/redo | Ctrl+Z / Ctrl+Y or right-side buttons |
| Submit | Submit/Enter; must have at least one mud tier |
| Tutorial | H or F1, or HELP button |
| Pause/settings | Esc |
| Fullscreen | F11 |
| Screenshot | F12, saved under `%USERPROFILE%\.mud_pie_masters\screenshots` |

All crafting uses a structured data model (mud tiers, coordinates, wetness, weight, and individual decorations); it isn't a preset slideshow. A deliberate symmetry shortcut can place actual mirrored items. Wind changes structural scoring, rain changes starting mud wetness, and chapter missions enforce ingredient restrictions. Free-build mode saves unscored creations to the scrapbook. All three judges give deterministic, explainable ratings for Size, Decoration, Symmetry, Originality and Integrity.

Before crafting, choose to CHEER ON or DARE THEM next to each sibling. This genuinely changes their next entry and relationship.

The game saves local progress to `%USERPROFILE%\.mud_pie_masters\save.json`, including chapter and star progress, gallery, unlocked ability state, and sibling memories. The old v0.1 save format is recognized, preserving prior information when present.

## Code and testing

- `mudpie/campaign.py`: mission content, rules, chapter state, medal logic and unlocks.
- `mudpie/models.py`: mud/decorations and deterministic wind/collapse physics.
- `mudpie/judging.py`: explainable judging features and personalized verdicts.
- `mudpie/rivals.py`: sibling strategies and evolving memories.
- `mudpie/game.py`: Pygame UI, scenes, tool input, overlays, campaign and free-build flows.
- `mudpie/save.py`: backward-compatible persistent saves.
- `mudpie/rendering.py`: original vector-textured pies, decorations, responsive UI and sprites.
- `tools/challenge_bot.py`: data-model-only synthetic mission feasibility helper, **not used in gameplay**.
- `tools/simulate_campaign.py`: autonomous 48-contest judging and progression validation, **not a human playtime benchmark**.
- `tests/`: pure-Python rules/data tests and Pygame SDL-dummy interaction smoke tests.
- `assets/`: original visual assets and synthesized sounds/music. `docs/title_art_preview.png` is a **static illustration**, not a captured runtime screenshot.

### Known gaps

- Actual on-screen rendering, window resizing, audio balance, FPS, and Windows packaging still need Windows execution.
- Two-hour real completion time **is not verified**; we have designed enough objectives to target it, not proved a duration.
- Cub actions are primarily presentation sequences and persistent generated entries, not a whole-body simulation of two cubs walking to fully independent physics craft stations.
- Subjective aesthetic judging is a deterministic geometric scoring model, not neural aesthetic perception.
- Original art is an attractive first-pass illustration set, not hand-animated production-studio artwork.
- The campaign is content-rich in distinct objectives but retains one main mud-crafting mechanic; its long-form fun factor still needs human testing.

The game is designed for private play, using only built-in Python and pygame-ce at runtime. No accounts, monetization or network connections.

## Artwork regeneration

Pixel assets are already included. To regenerate them from source, install Pillow into the developer environment, then run `python tools/generate_art.py`. This does **not** require an image-generation service. The v0.2 vector artwork is retired; v0.3 cubs are replaced by the v0.4 baby-cub expression set. The PNGs must not be smoothed during gameplay scale-up.


## v0.4 cuteness review

The three siblings are now visibly baby-shaped: plush cheeks, bright expressive
faces, short arms and legs, oversized paws, and small personal accessories.
The crafting table includes a small animated player cub, and presentation /
results use real expression sprites for a win or embarrassing collapse.
There are 12 original cub frames and editable deterministic generator source.
See `docs/v04_cub_reveal.png`, `docs/v04_before_after.png`, and
`docs/craft_layout_preview.png` for **static composited previews**, not captured
Pygame screens. This art style is awaiting player approval rather than being
labeled final. The 120-minute gameplay requirement is still *not proven*.

## v0.5.0 — Gameplay rescue / fun audit implementation

This patch addresses the **verified** v0.4 design failures without changing the
provisional extra-cute cub sprites. It is not a measured human playtest.

**What is different during play:**

- **Finite mud scoops.** Each drag of MUD produces one defined-volume scoop. Shape
  (2) can stretch it flat or press it taller, but cannot create additional mud.
  Stretching unworked mud too aggressively introduces real structural damage.
- **Knead with a purpose.** Scoop/Mix (1) increases cohesion through direct
  stirring; good consistency improves structure. Excessively wet mud slumps.
  Later, D dries the tiers again in the Storm Season chapter.
- **Clearer judging.** Empty tiers no longer earn elite symmetry ratings.
  Mirrored placement and angles matter; decorative distribution matters more
  than repeat-clicking a single spot. The current competition theme makes up
  65% of the scoring weights, while each judge retains 35% individual taste.
  These are the same weights shown on the clearing screen.
- **No free infinite-winning recipe.** Competitions deduct up to 38 points for
  repeating the same recognizable silhouette and decoration layout within the
  recent history. The deduction is stated in the judge's comment.
- **Sibling decisions.** While in the clearing, click CHEER ON or DARE THEM beside
  Bruno or Daisy (one choice per sibling per round). Encouraging can improve
  their building discipline and your relationship; daring increases ambition,
  rivalry and possible embarrassing failure. The generated entry changes, and
  subsequent wins/losses alter confidence, embarrassment and rivalry.
- **Teaching skill-based objectives.** 21 story missions now add a third,
  genuinely manipulable requirement: shaping tier steps, kneading mud,
  arranging details over several areas or tiers, or rotating decorations.
  Existing 36+12 campaign structure, two rivals and story progress remain.
- **Feedback.** Tiny transient mud flecks appear while sculpting/squishing;
  reduced-motion mode disables the extra particles.

A reproducible QA comparison, which **does not** measure human fun, is included
in `tools/stress_test.py`. The old generic pie now clears 12/48 mission goal
sets versus 20/48 in the v0.4 audit. Static sample architectural, decorative,
and symmetry-focused designs each win and lose against seeded rivals in scoring
comparisons. A 48-contest synthetic campaign also completes successfully.

### Verify without playing

The Windows check below runs automated tests (including SDL dummy-mode Pygame
mouse, graphics, save and flow checks) and synthetic competition checks, without
opening a normal interactive window:

```powershell
Set-Location "$HOME\MudPieMasters"
powershell -ExecutionPolicy Bypass -File .\verify_no_play.ps1
```

The game itself is launched separately with `play.bat` **only when you choose**.
Windows execution, a measured two-hour run and actual subjective fun are still
release gates. As requested, this version remains **pre-release**.