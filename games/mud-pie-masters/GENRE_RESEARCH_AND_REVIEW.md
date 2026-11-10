# Mud Pie Masters — Crafting Genre and Player Review Research

**Research date:** November 9, 2026
**Research owner:** Mossbyte (ChatGPT GPT-6), agent MPM-MOSSBYTE-GPT6-001
**Scope:** Actual public game descriptions and user reviews, not claims that the reviewer played those games. User-requested 2-hour meaningful-gameplay gate preserved.

## Comparable games and what to adopt / avoid

| Game | Source evidence | Positive lessons | Negative lessons / risks for Mud Pie Masters |
| --- | --- | --- | --- |
| Papa's Bakeria | [Flipline official game description](https://www.flipline.com/games/papasbakeria/info.html) lists mouse controls, crust, fillings, topping station, 40 recipes and progression systems | Each physical action has understandable purpose; station-specific precision and many visual combinations | Don't blindly copy timed orders; mud art needs creative autonomy, not only procedure accuracy |
| Sticky Business | [Steam store & reviews](https://store.steampowered.com/app/2303350/Sticky_Business/) + [recent community reviews](https://steamcommunity.com/app/2303350/reviews/) | Creating with many components is fun; cute art and customer stories encourage attachment | Users report repetition after stories and a desire for more custom options |
| Sticky Business (critical review contrast) | [Negative user review samples](https://steamcommunity.com/app/2303350/negativereviews/) and [most helpful critical reviews](https://steamcommunity.com/app/2303350/negativereviews/?browsefilter=toprated&l=english) | Clear creative freedom is valuable | Some players find the gameplay grindy, shallow, the UI confusing, and reward loops tedious; avoid padding 2 hours with repeated crafts |
| Passpartout 2: The Lost Artist | [Official Steam page](https://store.steampowered.com/app/1571100/Passpartout_2_The_Lost_Artist/) | Commissions, varied townspeople and critical feedback make art socially meaningful | Mud Pie Masters judging must retain explainable weights and avoid meaningless score surprises |
| SuchArt: Genius Artist Simulator | [Steam store/reviews](https://store.steampowered.com/app/1293180/SuchArt_Genius_Artist_Simulator/) | Material/tools react predictably and the canvas is free-form, with optional commissions | The 2D mud model must feel tactile; feature checklists cannot substitute for responsive manipulation |

### Community perspective

A [October 27, 2026 Reddit CozyGamers thread](https://www.reddit.com/r/CozyGamers/comments/1xh2n3l/is_sticky_business_just_as_fun_as_thrifty_business/) contrasts Sticky Business as primarily a component-combination creator with little management gameplay; users differ on whether this is enough. Treat design goals and objective density as preferences, not universal needs. A [January 2025 CozyGamers thread](https://www.reddit.com/r/CozyGamers/comments/1hzw648) praises its addictive sticker-making but some commenters find controls and onboarding difficult.

## Specific design acceptance requirements

1. **The moment-to-moment craft must be satisfying** without a mission: wet texture, clear cursor feedback, predictable reshaping, and audible but not repetitive squelches.
2. **Agency:** at least three viable creative strategies; one generic pie must not dominate all themes.
3. **Readable feedback:** always show the mission goals and progress without ellipsis on the detailed view; show full judge rationale in a dedicated panel.
4. **Sibling memory:** choices and wins/losses should visibly influence Bruno/Daisy across later rounds, not only a number.
5. **Pacing:** chapter progression introduces a novel skill or constraint, not a higher decoration-count demand alone. Side commissions should matter as stories or experiments.
6. **No fake two-hour claim:** objective count, synthetic test duration, and automated 48-contest completion do not establish player engagement or time.
7. **Player protection:** save at every finished round, proper restart/retry paths, crash reporting and archive tests, no hidden requirement to spend money.

## Gap audit at start of this round

- Game already had 36 main story challenges and 12 optional commissions, plus v0.6 single-contest event-driven Pygame reliability tests.
- A true *entire campaign through actual Game scenes* and a packaged Windows EXE with headless launch test had not yet been performed.
- The new full-campaign test explicitly distinguishes mouse-generated first scoop + submit/presentation from oracle-generated remaining pie geometry. It is not evidence of 48 rounds of natural mouse crafting, and does not certify the 2-hour human experience.
- Existing cute cub art is provisional, not final; no user approval to add stylistically different art assets.
- Further human playtesting is necessary to establish whether controls feel pleasant or whether boredom sets in before 2 hours.

## Source quality / limitations

These are qualitative reviews from the games' own communities plus developer descriptions, not a statistically representative study. Review counts and ratings change, so this document intentionally avoids freezing a numeric sentiment score as a permanent fact. No copyrighted assets or mechanics have been copied from competitors.
