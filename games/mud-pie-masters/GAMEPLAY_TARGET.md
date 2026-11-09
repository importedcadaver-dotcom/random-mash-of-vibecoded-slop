# Two-hour gameplay requirement · v0.2.0

## Goal

The intended player does **not** want to start the game until it can offer at least **two hours of meaningful, varied gameplay**. Do not interpret this as a request for forced waiting, replay grinding, time gates, or empty repetition.

## Implemented content inventory

- **36 required story contests**, in six chapters of six episodes each.
- **12 optional woodland commissions**, two per chapter, with client-specific goals.
- **48 unique challenge names and written briefs**, each with 2–3 validated design requirements (all 48 tested for a reachable data-model solution).
- **3 named, personality-distinct judges** and **5 transparent score properties**.
- **2 persistent sibling rivals**, each generating actual mud-pie objects and retaining memories, wins/losses and affection.
- **4 crafting tools** and **6 physical ingredients** (mud and five decorations).
- Chapter dialogue decisions, six cosmetic color variants, two unlocked craft abilities, weather variants and construction restrictions.
- **144 collectible stars**, plus six keepsakes, a scrapbook, free-build, repeatable contests and a final scene.
- Main progression requires completing the **two/three published construction goals** for each chapter episode; simply submitting one unadorned tier no longer skips the campaign. Losing the judges' overall vote does not block advancement.

## Duration hypothesis, not a claim

If 48 distinct authored contests take a typical player **2.5 minutes each**, the full story plus optional commissions would take about **120 minutes**, not counting tutorial, chapter choices, experiments, scrapbook viewing or replay for three stars. The average time-per-contest assumption is **unmeasured**, so **2h playtime has not been certified**. Fast or experienced players may finish quicker; exploratory players may take much longer.

## Pre-release gates to certify two hours

1. Run every Pygame SDL-dummy smoke test on Windows and fix failures.
2. Conduct a full, human-interactive *blind* playthrough on Windows from a fresh save, recording actual elapsed active play (exclude breaks and idle time).
3. Log the per-contest duration and percentage of time doing actual creative work versus navigation, retrying, waiting or repetitive copying.
4. Confirm median and full-playthrough duration: story + recommended side commissions should contain **at least 120 minutes of active meaningful play** for a representative first-time player.
5. If too short, **add original actions, challenges, story choices and variety**, not forced countdowns; then repeat duration and enjoyment tests.
6. Verify that three-star scoring is fair and that every challenge's requirements are understandable in the Pygame UI, not merely satisfiable via a synthetic test model.
7. Review art, interactive clarity, scene transitions, soundtrack volume and performance before marking the release ready.

**Current status:** content expanded and logically validated; two-hour guarantee and Windows graphical experience not yet verified. This document is an honesty gate, not evidence of a human playtest.


## v0.5 gameplay-balance audit

The 48-contest structure remains intact, but 21 story contests now involve
actual kneading, tapering, distributed arrangements, rotation, or placing details
on several tiers. Shaping now conserves mud and mixing has meaningful tradeoffs.
Automated adversarial tests show multiple viable score archetypes and fewer
reusable generic-template challenges (12/48). See `QA_REPORT_v0.5.md`.

This **does not certify** two hours of enjoyable gameplay. Human hands-on
measurements are unavailable; the user prefers not to start playing yet.