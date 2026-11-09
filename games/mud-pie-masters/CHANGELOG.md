# Changelog

## v0.2.0 — Forest Fair Storybook expansion

- Expanded from endlessly repeating five themes to a defined six-chapter, 36-contest story, plus 12 optional woodland commissions.
- Each of 48 unique briefs has 2–3 data-validated craft objectives and a themed story beat. Challenge data lives outside the UI in `mudpie/campaign.py`.
- Added chapter map, mission selection/replay, visible goals and progress, challenge reports, one/two/three-star awards, six collectible keepsakes and forest finale.
- A story stage needs completion of its published craft objectives to unlock the next; losing a judge vote does not stop progress. No countdown padding or paywalls.
- Added material restrictions, wind-modified structural stability, rainy mud, night atmosphere, unique chapter introductions and persistent sibling dialogue choices.
- Added cosmetic palette unlocks (six actual color variants), twin-decoration shortcut (M), and later mud-drying ability (D).
- Added true unscored free-build sessions that save to the scrapbook.
- Saved campaign progress while maintaining compatibility with the earlier v0.1 save format.
- Added 61 campaign/design tests and six new Pygame graphical smoke tests; 91 pure Python tests pass, 12 graphics tests pending Windows execution.
- Added a 48-mission model-based simulation; **no two-hour playtime or Windows graphical run has been verified**.

## v0.1.0 — First playable source

- Initial complete PyGame competition loop, original illustrated assets, synthesized sound, judge system, rival cubs, undo/redo, saves, options, tests, and scripts.
- Initial source compiled; initial pure-Python tests passed, Pygame graphical runtime unverified.

## 0.3.0 — Forest Print visual overhaul (art-focused iteration)

- Replaced the entire original vector-illustrated sprite set with six original,
  restricted-palette, hand-authored pixel-art character images.
- Rebuilt forest and crafting-table backdrops with consistent 2× pixel scaling,
  fir trees, meadow plants, packed earth, and wooden workshop details.
- Replaced shiny cake-cylinder rendering with soil-textured irregular mud tiers,
  visible sediment bands, grains and uneven silhouettes.
- Re-themed all reusable UI panels and buttons as angular inked placards with a
  serif headline and monospaced labels; preserved the actual game control hitboxes.
- Reworked mock layout previews with the new in-game assets. No generated images
  from concept experiments were put in the game.
- Visual changes only: all 48 campaign challenges and gameplay rules retained.
- Windows Pygame visual/runtime verification still pending.

## v0.4.0 — Max-cuteness cub candidate (2026-11-08)

- New original pixel-art sprite source and 12 consistent PNGs: You, Bruno and Daisy each receive idle, blink, cheer and sad frames.
- Replaced the three original in-game cub sprites with baby-proportioned characters, shorter legs, oversized round paws, softer faces, and individual accessories.
- Gameplay scenes now select actual expression frames, including reactions to pie collapse and results. Reduced-motion option disables idle blinking.
- Crafting screen now visibly includes the little player bear and a responsive one-line reaction plaque; all existing pie interactions are unchanged.
- Static layout previews and a character reveal / v0.3 vs v0.4 art comparison regenerated from included art assets. All previews are explicitly NOT live Pygame screenshots.
- Generator and tests included so this version remains editable rather than being a single composited AI image.
- Art direction is **provisional** awaiting user review; unverified two-hour playtime requirement remains unchanged.

## v0.5.0 — Fun-audit mechanical redesign (pre-release, 2026-11-08)

- Replaced free mud creation by conservation of material during shaping.
- Implemented worked/cohesive mud and two-sided mixing vs. oversaturation tradeoff.
- Added explicit harsh reshaping damage and tiny reduced-motion-aware splat particles.
- Rebalanced judging around the announced contest theme (65%) and individual judges (35%).
- Corrected symmetry exploit (a blank centered mud tier no longer earns 99/100).
- Made rotation, spatial coverage, mirrored details and crowding matter to scoring.
- Made recent exact recipe repetition penalize all judges, with an explained deduction.
- Made player interactions with Bruno and Daisy change their craft plans and persistent
  confidence/affection/rivalry; loss and collapse now have consequences.
- Added 21 distinct skill checks to existing campaign missions: taper, workability,
  composition coverage, rotation and multi-tier detail.
- Shipped extra adversarial stress tests and a Windows no-play automated check.
- 116 pure-Python tests passing in the isolated build environment; Pygame graphical
  tests and two-hour hands-on verification still outstanding.