# Mud Pie Masters v0.10 — Campaign and playtest QA

**Workstream:** Mossbyte — ChatGPT GPT-6, PR [#15](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/pull/15)  
**Date:** 2026-11-11 (America/Los_Angeles)  
**Status:** Pre-release candidate. `gameplay_hours_verified=false`.

## Scope

Four later story or side briefs require a player to actually reshape placed petals or sticks. The challenge oracle alters the same saved decoration geometry for logic checks. F10 exports a local `playtest_report.json` with per-contest craft and round duration, score and medals. The report makes no network request. Timers include idle time and cannot measure enjoyment.

The finale already had four goals because its older skill goal is appended to three authored goals. The goals panel now spaces four rows above its Back button; the new shaped briefs remain at three or fewer goals. Real elapsed frame time records play duration while the 0.05-second cap remains on animation updates. The export skips malformed history entries and handles missing score maps or invalid craft durations.

## Automated evidence

The first PR run, [Windows and Linux #42890752283](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/actions/runs/42890752283), had **171 passing and two failing pytest tests on each OS**. The failures were the four-goal assumption and capped duration. Its SDL event walkthrough and oracle-assisted 48-contest Pygame run passed on both OSes. The separate [Windows package run #42890752311](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/actions/runs/42890752311) passed, but predates the fixes above.

Use [PR #15 checks](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/pull/15/checks) for the latest post-fix Windows/Linux pytest, campaign simulation, SDL walkthrough, 48-contest runtime, Windows EXE smoke, governance and CodeRabbit results. Do not infer a pass from the earlier runs. The 48-contest pies use an oracle for complex geometry; those runs are neither 48 human-crafted rounds nor a duration benchmark.

## Independent human and physical Windows release gate

1. Install the latest successful Windows package in a fresh folder, keeping `MudPieMasters.exe` beside `_internal`. Preserve any existing personal save before testing; use a fresh save or isolated test account for first-time pacing.
2. An independent first-time tester should play the story and optional commissions on a real Windows desktop. Observe actual tool use, explanations, color/rotate controls, reshaping, falling mud, judging, sibling choices, save/resume and finale. Check both 1280x720 and a smaller window, including 900x900 if practical. Record audio, window and hardware performance issues.
3. Record start/stop times and **active** play minutes separately from breaks and idle periods. Export F10's local timing report as supporting evidence, never as a substitute for observation. Note contest retries, confusion, repeated tasks and when the player chooses to keep creating freely.
4. Collect the tester's own assessment of enjoyment and variety across chapters. The owner need not be the first tester. Only an observed 120+ meaningful-minute first-time playthrough plus physical Windows QA can support the two-hour release claim.

The Chapter 1 feedback in [Issue #9](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/issues/9) is real human evidence of earlier problems, but it does not establish the full release gate. Keep [Issue #2](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/issues/2) open until that gate is met.
