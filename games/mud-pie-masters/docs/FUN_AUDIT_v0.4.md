# Mud Pie Masters v0.4 — Game Design & Fun Audit

**Status:** Design/logic audit, 2026-11-08. The project was not modified. This is **not** a human playtest or Windows gameplay certification. Previous v0.4 character sprites remain a provisional art direction.

## Evidence reviewed

- Source: `mudpie/game.py`, `models.py`, `judging.py`, `campaign.py`, `rivals.py`, `rendering.py`, campaign simulation and test suite.
- `python -m pytest -q`: **98 passed, 1 module skipped** (Pygame absent in audit environment).
- `python tools/simulate_campaign.py`: **36 story + 12 side contests completed by a synthetic goal-construction oracle**, with 12/13/23 wins for You/Bruno/Daisy and 4 presentation collapses across 144 entries. This does NOT simulate human controls, enjoyment, or duration.
- Extra data-model adversarial scoring tests were performed without modifying source.

## Fun verdict

**Promising 10–20 minute crafting prototype, insufficient evidence and insufficient meaningful variation to recommend a two-hour debut.** The first 2–3 contests could be charming; extended play likely risks repeating the same actions and optimizing goal counters. This is a hypothesis based on source analysis, not a measured user reaction.

## Stress tests

- A deliberately generic four-tier, broad, symmetric pie with five material types and extensive decorations scored **above 90 under all five judge focus themes on its first use**. In a raw model exercise it met **29/48** mission-goal sets after accounting for material bans, though this construction used five color variants unavailable in early chapters; **29/48 must not be treated as a legally achievable full-campaign strategy**.
- A comparable, legal-for-starting-palette **two-color** generic recipe met **20/48** mission conditions after material restrictions (41.7%). Still too reusable for 48 allegedly distinct design challenges.
- Against seeded rival generation, reusing one strong generic pie won **39/48 judging comparisons** even with historical originality penalties. This **scoring-only** experiment disregarded some mission ingredient restrictions and should not be presented as a legitimate playthrough.
- A completely undecorated, centered, single-tier mud pie scores **99/100 for Symmetry**; this indicates that the formula confuses lack of imbalance with a deliberate symmetrical arrangement.
- Rotation (`Decoration.angle`) has **no influence on feature scoring**. Decoration colors mainly matter for matched-pair symmetry and explicit campaign counters, not aesthetic evaluation.
- Dragging a tier to enlarge both its width and height does not consume mud or preserve volume; the player receives more size score with no resource trade-off.
- Stirring increases wetness; the stability function penalizes excessive wetness without a compensating advantage in another gameplay rule. As implemented, more mixing is usually strategically harmful or irrelevant.
- All **48 challenges** express requirements using the same **14 goal-rule types**; 47 of 48 have exactly 2 checklist goals. Six contests restrict material types. The same **three judges** evaluate every round; changing theme adds only a modest weight bonus.
- The game exposes two siblings, but rival entries are generated ahead of time and their activity during crafting is not meaningfully interactive. Relationship updates mostly add +1 affection after defeats and +2 after wins; there are few meaningful trade-offs or branching consequences.

## Framework-specific diagnosis

### MDA: Mechanics → Dynamics → Aesthetics

**Desired experience:** physical squishing, making something personally expressive, sibling surprise and humor, suspense of collapse, judging that recognizes the player's design.

**Current dynamics:** adding and stretching tiers, dragging countable decorations, meeting thresholds, selecting the dominant construction pattern. Structural collapses and differing judge weights exist, but many of the emotional goals are not yet realized by the runtime systems.

### GameFlow

- **Clear goals:** Strong; visible goal counters, themes, and judging priorities.
- **Control:** Partial; mouse drag/undo exist, but sculpting lacks conservation and predictable material trade-offs.
- **Feedback:** Partial; live stability and results exist, but not sufficiently specific per-gesture or per-decoration aesthetic feedback.
- **Challenge/mastery:** Weak for 2 hours; checklist inflation is not a sustained rise in player skill.
- **Concentration/immersion:** Unknown until running the game; UI density and limited cub presence are possible friction.
- **Social interaction / relatedness:** Thin; siblings are mostly predictable competition output rather than reactive characters.

### Self-Determination Theory

- **Autonomy:** Free build is a genuine strength, but progression often rewards following decoration counts rather than pursuing a personal style.
- **Competence:** Players can understand scoring, but the mechanical system doesn't yet support expressive mastery and interesting counterplay.
- **Relatedness:** Personalities, memories, and sibling presence are promising; relationship consequences currently have too little range to be emotionally significant.

### Game Feel

Immediate drag response, visual mud deformation, meaningful texture/viscosity, sound synced to interactions, animation follow-through and undoability should form a cohesive response loop. Timing and tactile enjoyment require actual running Pygame playtests.

## Highest-priority design changes

**P0 — Repair core crafting before adding content.**
- Introduce fixed mud quantities per scoop, volume conservation while shaping, and clear viscosity trade-offs. Mixing should have a purposeful benefit and risk, not simply a wetness penalty.
- Add draggable shaping handles, tool-specific strokes, early stability warnings, forgiving correction of mistakes, and conspicuous per-action feedback.

**P1 — Repair judge dominance.**
- Score composition and intention, not raw object counts alone. Distinguish bare symmetry from intentionally organized symmetry, require coherent patterns, evaluate material/shape synergy, and vary judge preference *within transparent bounds*.
- Give real strategic trade-offs (size vs stability; detail vs crowding; symmetry vs asymmetry-based creativity), and validate strategy diversity with automated bots.

**P1 — Make siblings characters.**
- Show real-time progress and individual behavior; allow a small number of contextual interactions while crafting. Memory should influence tactics and dialogue. Relationships should respond differently to kindness, taunts, help, rivalry, and embarrassment; avoid automatically increasing affection on every loss.

**P2 — Redesign campaign to introduce new play decisions.**
- Replace some nearly interchangeable goal counters with special judge briefs, materials with unique handling, 2-3 construction approaches per objective, dynamic event cards, and craft showcases with emotional stakes.
- Avoid compulsory timers, grind, forced waits, or arbitrary penalties. Keep free build permanently available.

**P2 — Content polish after mechanics.**
- New expressive cub pose frames, reaction timing, better ingredient readability, mud squish/weight audio, calmer workbench layout and animated presentation sequences.

## Proposed release gates (targets, not observed results)

1. No one reusable general-purpose design should clear more than about 25% of structured missions without adapting to their distinctive goals.
2. With diverse bots, no one static pie should beat both rivals in more than 60% of compatible contests; rivalry should retain viable winning styles.
3. Every crafting mode must offer an understandable positive capability, a trade-off, and an immediate feedback loop.
4. Three different player strategies (architectural, decorative, symmetrical/precision) must each win at least one seeded contest and lose at least one *for explainable reasons*.
5. All 48 mission goals must be reachable by legal mouse controls and chapter-available materials; data-model oracles alone do not satisfy this gate.
6. Pygame UI automated smoke tests and actual Windows graphics/audio/input checks must pass.
7. At least two independent human sessions should demonstrate understandable onboarding, distinct 30+ minute play patterns and voluntary continued play. To call it **two hours of enjoyable gameplay**, a measured full-run and qualitative feedback are needed, not an assumed average of 2.5 minutes per contest.
8. No forced waiting, exploit farming, cosmetic reskins of the same challenge, or playtime padding is permitted.

## Proposed 120-minute campaign rhythm

| Chapter | New source of interest | Why it matters |
|---|---|---|
| 1. First Puddle | Satisfying scooping, shaping and first sibling contest | Discover the toy itself |
| 2. Petal Picnic | Pattern creation, new materials, first close friendship choice | Deliberate creativity |
| 3. Rocky Ridge | Load-bearing tall designs, wobble prediction, recovery | Physical mastery |
| 4. Storm Season | Wet/dry material trade-offs, environmental constraints | Different choices |
| 5. Moonlit Fair | Client personalities, visual storytelling, audience reactions | Expressive interpretation |
| 6. Golden Mud Cup | Multi-round final, sibling personal stakes, unique awards | Payoff and closure |

Do not assign fabricated minutes per chapter; confirm actual pace from observed sessions.

## Research used

- Hunicke, LeBlanc & Zubek, *MDA: A Formal Approach to Game Design and Game Research* (2004): https://aaai.org/papers/ws04-04-001-mda-a-formal-approach-to-game-design-and-game-research/
- Sweetser & Wyeth, *GameFlow: A Model for Evaluating Player Enjoyment in Games* (2005): https://doi.org/10.1145/1077246.1077253
- Ryan, Rigby & Przybylski, *The Motivational Pull of Video Games* (2006): https://selfdeterminationtheory.org/SDT/documents/2006_RyanRigbyPrzybylski_MandE.pdf
- *Designing Game Feel: A Survey* (2021): https://doi.org/10.1109/TG.2021.3072241
- Games User Research, *Choose the right playtest method* (2023): https://gamesuserresearch.com/choose-the-right-playtest-method/
- Game Developer, *How supporting core loops and early prototyping are key to your game's success* (2022): https://www.gamedeveloper.com/design/how-supporting-core-loops-and-early-prototyping-are-key-to-your-game-s-success
- Player Research, *Getting More From Usability Testing Your Game* (2021): https://www.playerresearch.com/learn/getting-more-from-usability-testing-your-game/