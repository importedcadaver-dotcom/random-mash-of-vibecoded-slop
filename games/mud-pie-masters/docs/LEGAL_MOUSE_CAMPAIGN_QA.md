# Mud Pie Masters — 48-contest legal-input gameplay QA

**Date:** November 11, 2026 (Pacific).  
**Workstream:** Mossbyte / ChatGPT GPT-6 / PR #26.  
**Evidence commit:** [`195cadd`](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/commit/195cadd056d364b946854634f970445cb9a4e972).  
**CI:** [Windows + Linux workflow #43160489313](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/actions/runs/43160489313).  
**Outcome:** **48/48 goal-feasible contests and commissions through scripted SDL keyboard/mouse events on both OSes**, subject to the exact scope below. No release/playtime certification.

## What the new proof actually demonstrates

Previous `tools/full_campaign_runtime.py` used `challenge_bot.design_for()` to **assign prebuilt Pie objects** directly into the live game's model. It validated the Pygame scene/presentation loop, 48 goal sets, medals, save persistence and finale, but did not establish that player gestures could assemble those objects.

PR #26 adds `tools/legal_mouse_campaign.py` and `tests/test_legal_mouse_campaign.py`, which construct **all 36 authored story pies and all 12 side-commission pies through ordered SDL events delivered to the production `Game.step_frame()` dispatcher**:

- Drag mud from the real ingredient tray to the workbench to create each layer.
- Drag real tiers with Scoop/Mix to knead mud to workable state.
- Shape/Flatten actual tiers to satisfy width, taper, overall height and silhouette requirements.
- Right-click to cycle the game's three existing mud shapes.
- Move an actual tier with Stack to satisfy offset.
- Drag leaves, petals, pebbles, sticks and berries from their real tray positions to physical tiers, respecting `mission.allowed`.
- Shape placed petals and sticks by draggable selection; check that changed stretches persist.
- Use only chapter-available decoration colors and the existing keyboard `C`, `R`, `M` shortcuts for color, rotation and mirrored placement.
- Inspect `goal_progress` *read-only* for all requested constraints (counts, symmetry, distribution, workability, material restrictions, dimensions and stability).
- Click the real Submit button, step through all presentation results, verify a two-or-three-medal result, and read back story progression from the on-disk save.

**Forbidden shortcuts:** no `Pie.add_layer`, `Pie.add_deco`, direct `game.pie` replacement, `challenge_bot` injection, direct medal awards or direct campaign advancement. Every constructed ingredient and its transformations go through the production mouse/keyboard handler. Test scripts may **read** model geometry and objective values to choose coordinates, but not mutate gameplay state.

**Explicit shortcut that remains:** the test fixture calls `Game.begin_round(challenge.id)` to select each authored mission without navigating the chapter map's mouse menus. Once the clearing opens, chapter response, Workbench entry, crafting, submission and presentation are all dispatched through SDL. Therefore the result establishes **crafted-goal reachability**, not comprehensive 48-mission **menu-navigation** proof.

## Repeatable results

| Evidence | Outcome |
| --- | --- |
| Windows Python 3.12 + SDL-dummy `python -m pytest -q` | **227 passed**, including the 48-round legal-input test |
| Linux Python 3.12 + SDL-dummy `python -m pytest -q` | **227 passed**, including the same new test |
| Legacy 48-round oracle Pygame competition/save pipeline | Passed on both OSes; independent of new input bot |
| Real-event Pygame first-play walkthrough/screenshots | Passed on both OSes |
| Windows PyInstaller package/SDL smoke | Passed ([build workflow #43160489293](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/actions/runs/43160489293)) |
| Protected PR governance | Passed |
| Actual human played for 120 active meaningful minutes | **NOT TESTED / NOT CERTIFIED** |

The **first draft** bot failed the second story contest: shaping the lower layer wider for the tapered look conserved volume, reducing the height from the expected 92 to about **83.88 px** against a required **85 px**. This was a **test-planning error**, not proof of an unreachable goal. A subsequent revision re-measures the resulting geometry and physically drags a top layer vertically to restore the height. The revised whole-campaign test then passed on both platforms.

## How to reproduce

From the game directory after installing `requirements-dev.txt`:

```bash
python -m pytest -q tests/test_legal_mouse_campaign.py
python tools/legal_mouse_campaign.py --output qa-artifacts/legal-mouse --limit 48
```

The CLI saves `legal_mouse_campaign.json` with each challenge's individual goal values, player score, awarded medals, SDL event/action counts, and provenance caveats. It also captures representative real Pygame workbench frames. If a mission fails, the script preserves a failure JSON, last 30 scripted actions and a failure screenshot. Run with `--limit 8` to focus on the first chapter.

## What this does NOT establish

1. **No independent player usability measurement.** The bot sees exact internal goal values and layer bounds rather than making decisions from visible UI alone. A human may not discover the interaction or understand its feedback.
2. **No real physical Windows hardware acceptance.** GitHub-hosted Windows runner uses SDL dummy video/audio; no personal display, physical cursor or audible sound was evaluated.
3. **No proof of 120 enjoyable active minutes.** Automated iteration is much faster than normal player interaction. Measuring script runtime or authored contest count would fabricate the requested entertainment-duration result.
4. **No guarantee of three stars or win against both siblings.** Goal completion earns at least two medals; the competitive judge score and creative quality are a separate balancing question.
5. **No exhaustive input/UI combinations.** This proves one successful programmed gesture path per contest; it does not certify all alternate solutions, accessibility, tutorial discoveries or exploit-resistance.
6. **No final artwork approval.** Existing original cub/sprite and judge art stays intact.

## Current gates and next steps

- [x] All 48 authored mission goals mechanically reachable through legal SDL input, with no direct pie injection.
- [x] Save progression, score publication and contest presentation on both Windows and Linux automated runners.
- [ ] Confirm complete map/menu/mission selection through real clicks for all 48; the current fixture bypasses this only.
- [ ] Adversarial scoring stress that accounts for legal color/material and physical crafting actions (not only goal feasibility).
- [ ] Human first-time onboarding observation, full campaign gameplay pacing and 120 **meaningful active** minutes.
- [ ] Physical Windows DPI, mouse, keyboard, audio and visual quality test; final creator art approval.

**Release issue [#2](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/issues/2) remains open; `gameplay_hours_verified=false` remains unchanged.** This evidence advances a real risk-reduction milestone, not the final launch gate.
