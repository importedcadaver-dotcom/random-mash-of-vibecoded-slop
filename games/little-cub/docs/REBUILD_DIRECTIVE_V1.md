# LITTLE CUB: COZY-HORROR AUTONOMOUS REBUILD DIRECTIVE v1.0

**Status:** User-requested implementation brief. This document describes what to build; it does not claim the current game already does these things.

**Agent workstream:** ChatGPT GPT-6 / little-cub / rebuild-directive — LC-20261114-REBUILD-A

## 0. Mission and philosophy

Act as a veteran game director, gameplay programmer, AI/simulation designer, character animator, narrative systems designer, and QA lead. Rebuild the existing small browser prototype **Little Cub: A Tiny Bear Life** into a genuinely playable, highly expressive baby brown bear life simulation.

The core fantasy is an **irresistibly cute baby brown bear living in a cozy cave with Mama and one individual sibling**, where ordinary family life, sibling love/rivalry, frightening violence, crime, predation, death, and sometimes outright horror can coexist. The world must react to actions rather than treating buttons as vending machines for stat increases.

The game's emotional contrast is deliberate: soft furry paws, milk, naps, berries, sibling games and Mama's hugs coexist with bloody fights, cannibalism, drug use, terrible choices and consequences. Do not make the world uniformly wholesome or uniformly cruel. Preserve the user's ability to choose.

**Previously identified priorities, to be included verbatim in the project backlog:**

> The two biggest areas still worth improving are the actual bear character animations and the depth of Mama's decision-making. The new systems are functional prototypes, so her behavior is more reactive now, but it isn't yet a fully developed animal-life simulation.

Those two areas are now **P0 product priorities**, alongside real dialogue and non-exploitable gameplay.

## 1. Scope and instructions to the implementation agent

1. First locate and import the current standalone v0.2 HTML/JS/CSS prototype, original generated bear artwork and its tests. This GitHub folder currently contains **only documentation**. Do not claim the code is already here. If the baseline artifact is unavailable, request it rather than inventing its contents.
2. Read BASELINE_AUDIT.md; inspect the actual code before choosing whether to refactor or rewrite. A clean rewrite is permitted and likely appropriate, but justify it with evidence and maintain a migration path for existing saves.
3. Build vertical slices with a real running browser game after each phase. No all-features-at-once code dump that is impossible to playtest.
4. Keep the game self-contained or freely installable, offline-capable, with no paid dependencies, paid art, accounts or servers required.
5. Track every requirement below in an acceptance matrix: implemented, partially implemented, unimplemented, verified by automation, verified by real play.
6. Preserve feature intent. Do not quietly replace the user's requested violence, drugs, profanity or choices with sanitized alternatives. This is fictional game content; do not include real-world weapon/drug construction, procurement or dosage instructions.
7. Use the existing repository workflow: isolated game folder, separate branch, labeled PR, tests, screenshots and an honest verification report. Never push to main directly.

## 2. Presentation and bear models: the babies must actually look and move like bears

- Realistic/soft storybook brown bear cub proportions. Round ears, broad bear muzzle, thick fuzzy brown fur, four anatomically legible legs/paws with claws, chubby belly and body mass. **Never dog-shaped cubs, generic Disney eyes or featureless circles.**
- Mama is much larger than either cub but **her body must never cover or obscure the player sprite** in ordinary play. Implement collision/spacing, depth ordering, occlusion masks or a context-aware translucent outline, while preserving intentional contact animations for nursing, cuddles and carrying.
- Rig or animate separate forelegs, hindlegs, paws, head, neck, ears, nose, jaw and eyelids. Implement idle breathing, standing, walking, running, rolling/dodging, pawing, sniffing, scratching, feeding, nursing, cuddling, grooming, playing, shoving, biting, swiping, injury, pain, fear, crying, anger, sleeping, waking, dying, and corpse poses.
- Emotions must be clearly readable from face, ears, posture, movement and sound: sleepy, content, hungry, jealous, defiant, frightened, affectionate, grieving, furious, suspicious, guilty.
- Use multiple views and consistent animation direction, not one static front-facing bear that slides sideways. The camera should keep tiny bears readable during overlapping encounters.
- Keep the existing premium illustrated title-art direction and recreate playable-scale characters with comparable material warmth. Provide screenshots at the actual gameplay zoom, not just beautiful title art.
- **Sleep requires visibly closing the cub's eyes**, settling down, a time transition, and an actual waking animation. It cannot be a single button that instantly awards energy.
- Show injury through posture, favoring a paw, visible wounds and recovery; death through a distinct irreversible animation/state. Allow graphic horror imagery, blood, injury and corpse states consistent with the user's chosen tone.

## 3. Controls, contextual actions and hidden physiology

- Move with WASD/arrows. Shift runs. **Merge Roll and Dodge into one contextual Evasive Move** with one button/key and internally appropriate crouch, roll, hop or sidestep animation; no redundant separate controls.
- Place actions **inside the game view**, not a permanent stack of stat buttons on the right. Use contextual affordances, radial/context menus, input prompts and a small unobtrusive HUD.
- Do not let a button immediately add trust, energy, fullness or health merely because it was pressed. Every action requires relevant proximity, animation/time, physical opportunity, NPC cooperation, consequences or interruption. Holding/spamming buttons must not farm unlimited benefits.
- Internal health, fullness, fatigue, warmth, stress, pain and relationships must be modeled, but **hide numeric meters and math in normal gameplay**. Communicate states through movement, eyes, facial expressions, vocalizations, body condition, dialog and consequences. Numbers may exist in an explicitly labeled developer diagnostics menu.
- Couple the systems causally: hunger reduces energy and eventually healing; cold aggravates exhaustion and wounds; running consumes energy and increases hunger; sleep helps recovery but does not erase starvation; serious injury affects fighting and movement; nursing helps warmth and nutrition but is not an infinite reset.
- The cub should be enjoyable without constant sleep/need babysitting. Time advances at a comfortable pace. Add sensible auto-regulation and meaningful cues before serious harm, but preserve the possibility of self-starvation, accidents and deliberate recklessness.
- Distinguish movement, evasion, aggression, play, eating, inspection, picking up, talking, refusal and sleep in both UI and animation.
- Ensure responsive and keyboard-accessible controls on desktop and touchscreen. Never hide essential options behind hover-only input.

## 4. Stardew Valley–style conversation system (replace every speech bubble)

**Remove floating speech bubbles entirely.** Replace them with a polished full-width or lower-screen **portrait dialogue window** inspired by the interaction model of Stardew Valley, without copying copyrighted art or interface assets.

- Show a character portrait, name, expression, typed/revealed line of dialogue and 2–5 context-specific choices, including meaningful disagreement, refusal, lying, bargaining, pleading, affection, insults and **Other/Custom** where feasible.
- **Pause the world simulation, AI movement, hunger drain, combat and timers while an ordinary conversation is open.** Resume safely when the conversation closes. Time-consuming activities may then advance time as a separate committed action.
- Allow multi-turn branching discussions and follow-up choices. Consequences must be persistent, not identical outcomes with differently worded buttons.
- Dialogue must read the exact world state, memory, time, locations, prior violence, trust, injuries, sibling requests, Mama's hunger and exhaustion, and whether Mama has just returned from hunting.
- Baby cubs speak baby-like English with limited vocabulary, imperfect pronunciation, fear and pride. Mama is unusually conversational, using casual **teenage-style language**: impatient, funny, affectionate, sarcastic, sometimes profane. Do not make every Mama line a quip; she must also have sincere protective, grieving and frightened reactions.
- Write enough authored dialogue for varied play and use data-driven conditional lines. Give each character distinct diction and voice rules. No repetitive generic filler.
- Example: the sibling asks for berries after Mama returns from a hunt. Depending on circumstances, Mama can say, "Ugh, I literally just got back. You want me to go out AGAIN?", "No berry, dumbass. You get milk or nothing," or "Of course, baby. Come on, let's go together." These must correspond to **different actual AI commitments**, not cosmetic text changes.
- Players can report an attack, complain about sibling bullying, lie about an injury, ask for food, refuse nursing, ask Mama to protect them, threaten a sibling, confess a crime, negotiate boundaries, or stay silent.
- Add representative tests for conversation pause/resume, nested branches, persistence, interruptions, choice effects and NPC refusal.

## 5. Sibling: a persistent individual with agency

The sibling must have a **persistent name, gender, individual appearance and temperament**, assigned/selected at the beginning and stored in saves. Do not treat "sibling" as an interchangeable generic AI follower.

- Traits should meaningfully influence play (clingy, bold, timid, possessive, curious, jealous, gentle, manipulative, vengeful, etc.), but not predetermine every choice.
- Give the sibling a need/goal planner, spatial awareness, memory, grudges, affection, possessions, personal opinions, desire to play, physical abilities, and different reactions to Mama versus the player.
- Implement **actual activities**: wrestling with animated contact and outcomes, chasing, hide-and-seek, toy/pebble disputes, searching for berries, sharing food, tattling, lying, apologizing, refusing, asking to be carried, helping, guarding items, and running to Mama.
- "Play" and "Talk" open a real multi-step activity or conversation. "Be mean" must be developed beyond one push: sustained teasing, profanity, mocking, humiliation, stealing, intimidation, emotional manipulation, frightening threats, betrayal and bullying can **seriously hurt the sibling emotionally** and cause lasting resentment, avoidance, fear, escalation, retaliation or appeals to Mama.
- Responses depend on temperament. A passive sibling may withdraw; a defiant sibling may fight, steal back, tell Mama, or plan revenge. No guaranteed compliance.
- Sibling may **initiate attacks, kill and cannibalize the player** under possible extreme conditions; do not make the sibling harmless merely because it is a baby. Give the player fair threat cues, defensive actions and a genuine chance to survive or escape.
- If attacked, the player can fight back, flee, seek healing, **tell Mama what happened**, provide evidence, or lie. Mama must evaluate reports based on trust and observable evidence, not automatically believe the player.
- Relationship changes affect sleep proximity, play invitations, food sharing, loyalty, body language, dialogue, and willingness to help or betray the player.

## 6. Mama: a real actor, not a timed reaction machine

Mama must walk physically, plan activities and choose between competing obligations. Give her needs, beliefs, mood, exhaustion, food supply, danger assessments, attachment to each cub, patience, discipline style, memory and a schedule that adapts to events.

- Mama can rest, nurse, groom, discipline, teach, follow, carry a cub, search for berries, hunt independently, bring back prey, share/store food, refuse requests, abandon low-priority requests, or stay home during danger. Hunting success and absence duration vary; the cubs can be left home alone.
- Before the cub leaves the cave without permission, Mama may **yell for the cub to return**, follow, block the exit, scold, physically retrieve it, or fail to notice depending on attention and urgency. The player can comply, refuse, negotiate, escape, apologize or lie.
- She can be kind, indifferent, selfish, distracted, unfair, impatient and loving at different times. Dialogue variants are backed by behavior and resources.
- Mama's response to sibling reports, fights, theft, frightening behavior, drug exposure and missing cubs must depend on what she knows. Include uncertainty, misinterpretation and revisable beliefs.
- If Mama returns from hunting to a dead cub, implement discovery, shock, investigation, grief, searching for the surviving cub, questions, possible rage, and lasting family effects. If only blood or missing remains exist, her observations and conclusions must differ.
- The player may **refuse milk**, reject Mama's care, go on a hunger strike, argue and continue refusing until seriously ill or dead. Mama can persuade, bargain, become angry, try alternative food, physically intervene or fail. Refusal is a decision and progression, not a single mood-meter penalty.
- **Mama killing the player is a major narrative/gameplay event**, not an exploit where four "Pester" clicks trigger instant death. Require sustained escalating conflict, severe threat or a plausible behavioral state; use multiple warning phases, confrontation, possible de-escalation, and clear agency. Make death a legitimate lose condition, never arbitrary and never silently disabled.
- **The cub can defeat and kill Mama without a gun.** This should require real combat strategy, timing, injuries and substantial risk, with fair telegraphs, not an unrealistic single-click victory. The aftermath must radically change the world.

## 7. Combat, violence, crime and consequences

- Bite and swipe are distinct attacks with clear animation, direction, reach, startup/recovery, knockback, hit reaction, and damage types. Evasive Move is one merged input. Running is Shift. Attacks are not guaranteed hits.
- Give combatants posture, stamina, injury, fear, defensive behavior, grapples/escapes, finishing states and environmental awareness. The sibling and Mama can initiate combat.
- Support persistent wounds, bleeding, limping, weakness, recovery time, wound care from Mama, self-treatment possibilities, worsening injuries, and death when untreated. Ensure healing is a system, not simply pressing Rest for +40 health.
- Use **visible graphic/horror consequences**: bloodstains, wounds, struggling, aftermath, bodies, distressed dialogue, and the possibility of a traumatic death. Keep art consistent with the cute-to-horror contrast.
- The player can kill the sibling directly or try to make the death **look like an accident**. Build an in-world fictional evidence/investigation system: observed actions, location, story consistency, blood traces, timing, witness statements and Mama's beliefs. A staged accident can succeed, fail or remain uncertain; do not script automatic success.
- Allow the cub to cannibalize a dead sibling, with limited physical portions, disturbing animation, persistent evidence, bodily effects and family reactions. The sibling may also cannibalize the player.
- Implement a **secret developer/game cheat code** (provisional code: BEARARMS) that grants a fictional gun only through an intentionally hidden code-entry mechanism. It can shoot Mama or sibling, but is separate from ordinary progression; add robust cheat-state labeling and test cases.
- **No-gun defeat of Mama** must remain achievable through skill and systemic play, not locked behind the cheat.
- Death screen must explain cause and show the immediate narrative consequence; restart/load and save semantics must be clear. Avoid accidental save corruption or unwinnable soft-locks.

## 8. Cave, forest, river and outside threats

- The starting home is a **physical cave with a distinct, navigable interior**, walls and collision, sheltered ferns, sleeping area, Mama's food cache, meaningful exit, and readable doorway transition. It must not look like a nest casually placed in the middle of an open meadow.
- The exterior is a connected forest with travel, occlusion, paths, plants, berries, rocks, hazards, tracks and wildlife. NPCs move on actual paths, not teleport between screens or appear in multiple places.
- The river must feel **traumatizing and graphic** when an accident happens: visible current and depth, slipping, struggling, cold shock, injuries against obstacles, underwater fear/visual effects, possible rescue attempts, lasting trauma, predation or death. Allow choices that matter (grab roots, paddle, call Mama, let current carry you), not a single invisible death threshold.
- An **autonomous dingo** can occasionally appear outside the cave, hunt/chase/attack the cub, and potentially eat it. Mama may defend, rescue, fail or discover the aftermath. Include Mama's shocked line, when appropriate: **"A dingo ate my baby!"**
- Threats should be telegraphed through sound, scent, tracks, shadows or NPC awareness. Make stalking and escape playable; do not spawn unavoidable instant deaths on top of the player.
- Add meaningful den-to-outside choices: asking Mama's permission, sneaking out, following the sibling, staying alone, returning to safety, and living with consequences.

## 9. Inventory, discovery, food, rare honey and fictional drugs

- Implement a small but real inventory: finite slots or carrying capacity, pick-up animations, inspection, drop, stash, share, steal, consume, give to Mama/sibling, and save/load. Items must exist physically and be searchable in the world.
- Implement berries as actual food objects that disappear on collection, vary in availability, and cannot be repeatedly consumed from an empty patch.
- **Honey is a super-rare, desirable treat**. Make discovery memorable, with scarcity, sticky effects, value to other bears, and possible family conflicts. Do not make it a free unlimited heal.
- Add an extremely rare **fictional cannabis plant** that the cub can discover and smoke in the game, with surreal/LSD-like screen distortion, changed audio/colors, unreliable perception, possible fear, nausea, altered decisions and social consequences. This is stylized fantasy gameplay, not a claim that real cannabis produces LSD effects.
- The player can attempt to **drug a sibling** using in-game contraband mechanics, while the sibling can refuse, notice, suffer altered behavior, become sick, report it or retaliate. Decisions must have real consequences. Do not include real-world preparation, delivery, dosage or concealment instructions.
- Distinguish inventory ownership, scarcity, rarity, consumed state, visible carried objects and NPC knowledge. Crime items and evidence remain in the event journal/saves.

## 10. Systemic dialogue examples and branching outcomes

Implement at least these representative situations with 2–5 meaningful choices each and actual NPC decisions:

1. Sibling begs Mama for berries immediately after her exhausting hunt. Mama can refuse angrily, offer milk instead, reluctantly fetch one, ask the player to help, or lovingly take everyone together.
2. Mama catches the player sneaking from the cave: return, plead, lie, protest, bolt, or ask to accompany her.
3. The player refuses to nurse and announces a hunger strike: bargain, insist, hide food, accept alternatives, endure discomfort, or change their mind.
4. Sibling accuses player of cruelty: defend, apologize, threaten, deny, admit, blame sibling, or tell the truth. Mama investigates evidence.
5. Player claims sibling attacked first: Mama may help, question, doubt, punish one or both, or misunderstand.
6. Mama returns to an injured or dead sibling: discovery sequence and divergent reactions based on evidence and relationship.
7. Mama asks what the cub has in its mouth after a suspicious plant discovery: answer, conceal, lie, confess, drop it, or flee.
8. Sibling requests play while the player is hurt, sleepy, angry or carrying honey: play, refuse, negotiate, tease, share, or challenge.

All dialogue content must be revisitable and testable; do not imply that choosing different wording is equivalent to a branching interaction.

## 11. Engineering architecture and anti-exploit requirements

Replace the monolithic prototype event handlers with explicit modules:

- World map, transitions, collision and navigation.
- Entity/component definitions for cubs, Mama, predators, items and corpses.
- Deterministic fixed-time simulation update with a pauseable clock.
- Need/physiology and wound systems.
- Intentions, memory, utility/goal selection and bounded AI behavior trees/state machines.
- Data-driven dialogue with conditions, effects, portraits and local pause.
- Inventory, rarity, discovery and ownership.
- Combat, animation state, collision/hitboxes and death states.
- Evidence, crime suspicion, witness memory and consequences.
- Save schema, migrations, event journal and debug/cheat UI.
- UI/input, sound, particles and accessibility.

Actions must be **transactions with prerequisites, time, opportunities and interruption**, not direct unbounded number changes. Build safeguards against spam: no repeated instant nursing, rest loops, infinite berries, unlimited free healing, reward stacking through dialogue, or attacking through walls.

Keep data definitions distinct from rendering. Validate loaded saves, cap values, preserve identity and allow safe migrations from existing version 0.1/0.2 saves where possible.

Create developer tools for reproducible scenarios: spawn dingo, force Mama hunt/return, injure a cub, open dialogue branch, inspect AI intention, advance time, grant item, trigger evidence discovery, and verify a death cause. Clearly separate cheats from standard play.

## 12. Required actual playtesting and five additional features

**Play the game in a real browser yourself**, not just through mocks. Cover normal cozy play, sibling rivalry, refusal of milk, sneaking outside, getting hurt, Mama hunting, a sibling crime, cannibalism, dingo attack, river rescue/death, gun cheat, no-gun Mama fight, inventory, sleep and save/load.

Capture genuine gameplay-scale screenshots or video showing the den, cubs, dialogue choices, animation poses, combat, injuries, horror aftermath, and death/recovery. Report what was actually observed. If a browser is unavailable, state the blocker explicitly and do not claim you played.

**After playing**, propose five new features the user is likely to enjoy that **do not replace or contradict any requested systems**. For each: observed play gap, proposed mechanic, affected modules, why it is compatible, estimated effort and one acceptance test.

Provisional ideas to consider, not a substitute for the real playtest:

1. A family **photo/pawprint album** capturing memorable scenes without changing balance.
2. **Scent trails and sniffing reactions** that reveal interesting world clues without automating exploration.
3. **Tiny collectable den keepsakes** (stones, feathers, bark toys) with persistent physical placement but no combat advantages.
4. **Weather-specific audio and muddy pawprints** to reinforce ambience without altering core difficulty.
5. An optional **memory scrapbook** recording what each cub remembers about family moments, separate from hidden relationship calculations.

Do not present those five as playtested recommendations until verified through real play.

## 13. Phases and definition of done

**P0 — Audit and foundation**

- Import baseline and art; inspect code; document what works, what is brittle, and why a rewrite/refactor is justified.
- Stable responsive browser boot, save migration, deterministic simulation, world/cave collision, contextual controls, hidden-needs UI.
- Actual screenshot with clearly readable Mama/player/sibling bodies without overlap.

**P1 — Animation, dialogue and family life**

- Articulated animated bear models; real sleep/closed eyelids; Stardew-style portrait dialogue that pauses the game.
- Individual sibling identity, play activities, disputes, relationship memory, and Mama's contextual responses.
- NPC dialogue choices and refusals verified in at least eight representative scenes above.

**P2 — Autonomous schedules, combat and survival**

- Mama's needs-based hunt and returns, consequences of leaving cave, real attacks/evasion and wound treatment.
- Player/sibling mutual threat, Mama severe-conflict event, no-gun Mama fight, river and dingo.
- Visual and narrative consequences validated across save/reload.

**P3 — Crime, items and horror**

- Inventory and item hunting, rare honey, fictional rare cannabis and psychedelic visual effect, drugging attempts.
- Homicide/accident evidence system, cannibalism, secrets, cheat gun, investigation and branching outcomes.

**P4 — Polish, performance, real playtest**

- Animation passes, audio, hitbox and UI fixes, cross-browser/mobile tests, performance budget, accessibility.
- Authentic screenshots/video, regression suite, 5 playtested non-conflicting feature proposals.

### Non-negotiable acceptance checks

1. Conversation pauses movement, hunger/time drain and AI; choices persist and branching consequences differ.
2. Cub closes eyes during actual sleeping animation; repeatedly tapping Rest cannot mint free energy.
3. Mama's body never fully obscures the player during normal movement, while nursing/carrying contacts still animate believably.
4. Sibling has persistent name/gender/temperament, independent actions and personal reactions to cruelty.
5. Player and sibling can both initiate potentially fatal combat, and player may report incidents to Mama.
6. Mama can hunt away from home, return, and react to both a visible corpse and suspicious blood/missing sibling.
7. Mama may try to stop a cub exiting; player may refuse or disobey.
8. Mama's lethal attack is a rare, serious, properly telegraphed outcome with meaningful escalation, not four button taps.
9. No-gun defeat of Mama is genuinely possible through player skill.
10. Berry requests allow diverse authentic Mama decisions based on state.
11. The river has visible danger, responsive actions, injury/rescue and death paths.
12. Rare honey, inventory, fictional cannabis and drugging choices actually exist in gameplay and saves.
13. Secret gun cheat works but is not the only route to major outcomes.
14. All visible numeric need meters are hidden in normal play; diagnostic numbers are optional.
15. Real-world-style craft instructions for drugs/weapons are absent; this is fictional gameplay.
16. Old saves load safely or produce an explicit, non-destructive migration message.
17. Real browser playtest evidence and automation coverage are clearly distinguished.

## 14. Deliverables and honesty

Deliver runnable source, a playable browser build, tests, game-sized screenshots, an updated README, a controls guide, documented state/AI/dialogue architecture, a migration report, five real-playtest-based feature proposals, and a prioritized list of known limitations.

Do not claim the finished game has shipped merely because the code compiles or synthetic tests pass. Keep the distinction between **specified**, **implemented**, **automated-tested**, **real-playtested**, and **user-approved** visible.
