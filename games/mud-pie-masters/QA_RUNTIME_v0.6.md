# Mud Pie Masters — v0.6 Gameplay Reliability QA

**Agent:** Mossbyte (ChatGPT GPT-6) · `MPM-MOSSBYTE-GPT6-001`
**Date:** 2026-11-09 (America/Los_Angeles; CI on 2026-11-10 UTC)
**PR:** [#6](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/pull/6)
**Status:** Automated runtime reliability milestone; **NOT a validated two-hour game release**.

## Test evidence

- [Windows + Linux GitHub Actions run #42740408609](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/actions/runs/42740408609): **137 pytest tests passed on each OS**, and the campaign simulation completed.
- `python tools/runtime_walkthrough.py --output qa-artifacts/runtime`: passes on Windows and Linux under Pygame-ce with `SDL_VIDEODRIVER=dummy` and `SDL_AUDIODRIVER=dummy`.
- **20 genuine Pygame-rendered screenshots per OS**, plus action trace (`walkthrough.json`). Screenshot validation checks PNG size, dimensions, and sample color variation.
- **Windows artifact:** [20 screenshots and event trace](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/actions/runs/42740408609/artifacts/13729385856)
- **Linux artifact:** [20 screenshots and event trace](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/actions/runs/42740408609/artifacts/13729206172)
- Full walkthrough: title -> first-chapter intro -> clearing -> sibling choices -> tutorial -> crafting -> results -> fully explained scoring -> campaign map -> free build -> scrapbook -> window resize -> letterboxed title.
- **186 SDL events** in the Windows trace, including queued mouse-move, down/up, drag, keyboard, ctrl+undo/redo, Escape, and SDL resize, sharing the same `Game.handle_event` and `Game.step_frame` methods as the production loop.
- First campaign goal progressed to `next_story=1` through queued events; free-built pie saved. All three competitors were judged.
- `agent-governance` GitHub CI also passed.

## Actual bugs and usability issues uncovered

1. **False chapter-completion announcement (fixed).** An uncompleted first contest could say "Chapter complete!" because progress `0 % 6 == 0`. We now require that story progress increased and reached a nonzero chapter boundary; regression test included.
2. **First story objective incomplete in initial automated gestures (test fixed, design feedback recorded).** The first mission includes a third "knead one workable tier" objective. Initial bot stirred too little. With a valid longer stir gesture the real Pygame UI awards 3/3 challenge stars and advances story. This initial failure exposed insufficiently explicit test coverage, not an automatic chapter skip.
3. **Crafting notification obscured heading (fixed).** Shaping toasts are now placed in the work area rather than on top of the heading.
4. **Stale crafting notification obscured presentation/results headings (fixed).** Scene transitions clear the previous toast.
5. **Goal labels truncated in crafting panel (mitigated).** The UI now has a clickable **VIEW ALL GOALS** overlay with full current goal text and numeric progress; event test and screenshot cover opening/closing it.
6. **Judge comments truncated (mitigated).** Results now have **FULL JUDGE COMMENTS** with full opinions plus sibling memory beat, screenshot and regression test.
7. **Star icons rendered as square missing glyphs on Windows (fixed).** Critical scoring labels use numeric stars (`3 / 3`) and ASCII-readable champion text.

Screenshots from Windows and Linux were inspected manually as images. They show coherent scene rendering and the accessible detail panels. **They are not proof of visual perfection**; pixel-art placeholders and small sidebar text remain candidates for further polish.

## What automation does and does not establish

**Verified:** Noncrashing Pygame rendering under SDL dummy driver, event routing in the production game loop, repeatable first contest with actual input events, objective-based advancement, judge result panels, save and free-build gallery, 1280×720 and 900×900 letterbox event handling, CI artifact availability.

**NOT verified:** OS-level Windows mouse or actual interactive display, input lag, real audio output, fullscreen on physical monitors, PyInstaller .exe behavior, performance on user's hardware, visual accessibility at small sizes, complete human campaign playtime or enjoyment.

The GitHub Actions runners execute the actual Python game code but use a **dummy SDL video/audio driver**. They do not send system-level mouse clicks. No genuine two-hour human playthrough was run or implied. No change to `gameplay_hours_verified=false`.

## Remaining non-blocking warnings / recommendations

- GitHub Actions logs contain deprecation warnings for Node 20 in `actions/checkout@v4`, `actions/setup-python@v5`, and `actions/upload-artifact@v4`, currently forced to Node 24. Upgrade these Actions in a separate, verified CI-maintenance PR.
- Some side-panel information is still dense; consider an accessibility pass after real playtesting.
- Existing provisional baby-bear artwork remains approved only as a *possible placeholder*, not locked final.
- For release, follow [Issue #2](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/issues/2) and perform an observed Windows playtest with real player feedback and **measured meaningful time >= 2 hours**, plus executable verification.

## Repeatable commands

From `games/mud-pie-masters` with Python 3.12 and pygame-ce installed:

```powershell
python -m pytest -q
python tools/simulate_campaign.py
$env:SDL_VIDEODRIVER="dummy"
$env:SDL_AUDIODRIVER="dummy"
python tools/runtime_walkthrough.py --output qa-artifacts/runtime
```

The bot's screenshots and save data are isolated from user save files by a temporary directory. Normal gameplay is not launched for the owner.
