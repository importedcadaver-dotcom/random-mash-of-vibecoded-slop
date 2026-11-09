# Mud Pie Masters — v0.5 Gameplay QA Evidence

**Release gate:** NOT READY for a confirmed two-hour enjoyable first playthrough.
This release is a tested source candidate, not an executable proven on Windows.

## Executed in isolated Python environment

| Check | Actual result |
|---|---|
| `python -m compileall -q mudpie tools tests main.py` | Passed |
| `python -m pytest -q` | 116 passed, 1 Pygame module skipped |
| `python tools/simulate_campaign.py` | 36 story and 12 side contests simulated successfully |
| `python tools/stress_test.py` | Finished; strategy metrics below |
| `pygame-ce` package install in sandbox | Failed: package host inaccessible / DNS resolution |
| Pygame on-screen and SDL dummy input | Not run here; included for Windows |
| Actual measured human playtime | Not run |

### Data-model campaign simulation

48 synthetic goal-satisfying entries; medals 127 cumulative (not a quality score);
11 You wins, 13 Bruno wins, 24 Daisy wins; 14 collapses across 144 presentation
entries. Automated construction is *not* an imitation of real mouse input, and
this distribution does not represent human skill, perceived fairness or duration.

### Audited strategy metrics

The v0.4-representative generic pie completes **12/48** objective sets (25%)
versus **20/48** in the previous stricter audit. The comparison includes both
material bans and newly skill-specific third goals.

Scoring-only wins versus seeded generated rivals (48 themes; no mission-goal
legality check for these sample pies): architect **11**, florist **21**, precision
**27**, fixed-template repeat **0**. The fixed-template comparison includes the
repeat-history penalty; its zero wins should not be generalized to every
potential exploitable recipe or to real humans.

For a first-try construction with no repetition, score by focus:

| Strategy | Size focus | Decoration focus | Symmetry focus |
|---|---:|---:|---:|
| Architect | 77.7 | 53.1 | 40.0 |
| Florist | 53.9 | 75.3 | 40.5 |
| Precision | 59.2 | 74.6 | 91.1 |

This is evidence of design *trade-offs*, **not proof that the game is fun**.

## Untested or incomplete

- 15 Pygame smoke tests shipped (`tests/test_pygame_smoke.py`) but not executed
  in this sandbox; test on Windows with existing pygame-ce installation.
- UI readability, controls, animation pacing, audio mix, manual text overflow,
  60 FPS target, Windows packaging, and save-file upgrade need Windows checks.
- The 48 contests still share one physical crafting table and three judges;
  scene-to-scene novelty and sibling depth may not yet sustain two hours.
- Player skill, strategic adaptation, fatigue, and 120-minute completion time
  cannot be certified from scripted model simulations.

## How to test without spoiling the campaign

Run `verify_no_play.ps1` in the project directory on the user's Windows PC.
This invokes pytest under dummy SDL video and audio drivers plus both pure-
Python simulation/stress scripts. It doesn't start the normal full game window.
Keep screenshots and user feedback separate from synthetic claims.

## Release decision

**Gameplay redesign implemented and mechanically sanity-checked.** Do not
represent this as a final polished release or as verified two-hour entertainment.
The player has not played and wants the full experience verified first.
