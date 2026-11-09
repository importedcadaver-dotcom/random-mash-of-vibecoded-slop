> **Current verification:** See `QA_REPORT_v0.5.md` for the latest gameplay redesign test results. This file is the historical v0.4 report.

# MUD PIE MASTERS — QA report v0.4.0

## Verified in authoring sandbox

- `python -m compileall -q .`: successful syntax/bytecode compilation.
- `python -m pytest -q`: **91 passed, 1 skipped**. The skipped module is `tests/test_pygame_smoke.py` because pygame-ce is not installed in the authoring sandbox. That module currently contains **12 additional Pygame interaction tests** to run on Windows.
- Campaign data inventory: **36 story contests + 12 optional commissions; 48 unique names, at least two goals each**.
- All 48 missions have automated model-only constructibility tests: goal requirements can be satisfied together in a `Pie` model under their defined ingredients/weather, without exceeding normal tier/decorative limits.
- A pure-Python autonomous simulation completed all 48 missions using actual `Pie`, rival, judge, collapse, medal and campaign-progression functions. Outcome for one deterministic run: 48 evaluated contests, 133/144 possible stars for the goal-satisfying QA construction approach, winner distribution You 12 / Bruno 13 / Daisy 23, and 4 deterministic collapses across entries. **These are synthetic QA outcomes, not human gameplay statistics.**
- Pure tests additionally cover campaign replay vs. skipping, chapter/side quest unlocking, maximum medals, save compatibility with v0.1, corrupted campaign data, cosmetic unlocking, wind effects, rival material constraints, old scorer/model behavior, and sound-independent world rules.
- Static title illustration regenerated for the v0.2 menu layout. It is **not a live Pygame screenshot**.

## Not verified here

- Pygame-ce installation and real UI rendering (unavailable in this isolated build environment).
- The **12 Pygame SDL-dummy smoke tests** on Windows.
- Windows PowerShell launch and PyInstaller package.
- Fullscreen/letterbox pointer accuracy after updated campaign screen and overlays.
- Human perception of craft responsiveness, challenge fairness, UI readability, sound volume, and animation polish.
- **Two hours of actual gameplay.** The content design aims for ≥120 minutes, but no human completion time was collected. The player has explicitly asked not to play before that duration is established, so do not call it confirmed.

## Recommended automated Windows checks without starting a manual playthrough

```powershell
Set-Location "$HOME\MudPieMasters"
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe tools\simulate_campaign.py
.\.venv\Scripts\python.exe -m ruff check .
```

`pytest` uses the SDL dummy video/audio drivers for graphics smoke tests. Normal manual playtesting is a separate gate, not a substitute for test suites.

## Current known caveats

- Achieving both objectives unlocks each story stage; this is a meaningful campaign gate rather than a forced clock. All challenges have programmatically reachable states but human difficulty has not been calibrated.
- The forest story and new settings use the same original illustrated art set; animation is subtle and not the same as a fully animated character rig.
- One mud-crafting activity underpins all 48 challenges; objective/theme variety may or may not sustain two hours of enjoyment, still requires real-user evaluation.
- Score measurements use transparent geometry heuristics. Originality reward is approximated through variety/composition/signature differences, not actual artistic taste.

The v0.1 project was preserved in source control history; this edition adds extensive new story systems and tests.

## v0.3 visual redesign QA note

- All 94 pure-Python gameplay/campaign/art-pack tests pass after the rendering revisions (91 existing tests + 3 asset checks).
- New PNG assets rendered deterministically by Pillow from original pixel-art
  source; full static layout previews were rebuilt and visually inspected.
- `python -m compileall` succeeded for core modules.
- Pygame runtime is **not installed in this sandbox** and pip cannot reach its
  package host. Therefore real on-screen click, display, audio, frame-time and
  resized-window validation remains **not executed** and should not be confused
  with preview-based inspection.
- The project remains a **candidate**, not a certified two-hour experience.


## v0.4 visual-expression QA addendum

- 3 × 4 PNG cub frames generated locally with `tools/generate_cute_cubs.py`.
- Character expressions are actual runtime PNGs and selected by `Game._sprite`, not art-only mockups.
- Static title/craft/results previews were rendered directly from those assets.
- `python -m compileall -q mudpie tools tests main.py`: passed.
- `python -m pytest -q`: **98 passed, 1 skipped**. Four additional pure-Python art regression checks protect the expression assets; the skipped module is the Pygame graphical smoke suite because pygame-ce is unavailable in this sandbox.
- The v0.3 title, crafting, results and six-chapter gameplay logic remain intact.
- **Not yet verified:** live Pygame face animation, occlusion under large player-built pies, mouse accuracy under resizing, Windows package, human visual approval, or a real ≥120-minute playthrough.
- v0.4 is a **candidate for user review**, not the final approved style or a two-hour-certified release.
