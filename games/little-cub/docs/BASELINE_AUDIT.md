# Little Cub v0.2 — Baseline Code Audit

This is a **static review** of the standalone prototype source examined in the originating workspace, plus the previously reported automated tests. The source is not yet imported into this GitHub folder. These are findings, not proof of user-visible browser bugs.

## Priority findings

| Severity | Evidence in the prototype | Why it fails the requested experience | Required remedy |
| --- | --- | --- | --- |
| P0 | Action functions immediately adjust player values: play adds sibling trust, rest restores energy, nursing restores fullness, and eating applies fullness instantly | Button pressing substitutes for embodied gameplay; actions can be repeated without a compelling scene | Action contracts with prerequisites, duration, animations, cooldown, animation interruption, cost, NPC consent/refusal, and consequences |
| P0 | Dialogue uses brief drawSpeech bubbles, and talk is one canned exchange | No player choice, branching narrative, persistent decisions, or paused interaction | Portrait dialogue window with 2–5 meaningful choices, nested follow-ups, dialogue state, and paused world simulation |
| P0 | Main interface displays numerical health, fullness, energy, warmth, Mama patience, and sibling health | Creates a meter-maintenance game rather than a cub-life experience | Hide values in normal mode; surface fatigue, injury, hunger, temperature and relationships through posture, sound, animations, refusals, dialogue, and visual cues |
| P0 | Mama AI largely changes among simple modes such as rest, forage, hunt, check, grief, anger, and investigate | Reactions do not yet arise from consistent motivations, obligations or relationships | Utility/goal AI with memory, schedules, danger assessments, specific opinions, resource scarcity, hunting priorities, and family routines |
| P0 | Sibling AI uses a few modes plus trust/fear and occasional random dialogue | No persistent individual identity, motives, negotiated play, complex rivalry, or meaningful agency | Name, gender, temperament, goals, memory, reciprocal actions, dialogue, affection, grudges, fights, deceit, predation and autonomous choice |
| P1 | A bear is drawn from ellipses with tiny bob movement; body parts are not articulated | Bear appears like a moving icon, not an animated infant animal | Rig/animation clips for separate limbs, head, jaw, eyes and ears; multiple emotional and perspective poses |
| P1 | Bears are y-sorted, but Mama's oversized rendered body is not prevented from visually covering the cub | Player readability and physical contact are unreliable | Collision spacing, proper visual depth, occlusion masks, outlines, camera/pose handling and explicit carrying/nursing layers |
| P1 | Rest is instantaneous, advances game time, and never closes the cub's eyes | Sleep feels like a stat button | Sleep animation with eyelid closure, settling, time transition, interruption and waking |
| P1 | Player health and warmth/fullness/energy are mostly independent counters with a few threshold death checks | Physiology is not coherent; there are few second-order consequences | Coupled hidden needs with wounds, healing, exertion, nourishment, temperature, sleep, behavioral adaptation and disease risk |
| P1 | Combat is radius-based and subtracts fixed health; player actions have no substantive directional hitboxes or parry/counter systems | Fighting Mama or the sibling is simplistic and exploitable | Real hitboxes, telegraphs, attack commitments, evasion, knockback, injury effects, posture, fear and adaptive AI |
| P1 | Cave walls, tree shapes, stones and berry bushes are painted decor without dependable terrain collision | Visual obstacles can disagree with movement | World collision geometry separated from art, spatial navigation and debug overlay |
| P1 | Mama's hunt happens on a timer and creates a return event, not a full resource-driven trip | Hunting cannot meaningfully satisfy or fail the family | Hunt decision process, route/departure, success/failure, food carrying, arrival, resource sharing, exhaustion and child-safety tradeoffs |
| P2 | Berry artwork does not necessarily change when the saved berry count is depleted | Visual feedback can contradict mechanics | Item/resource entities that visibly change and respawn by rules |
| P2 | Single mutable game-state object and localStorage snapshots with limited nested validation | Hard to test, migrate and debug as systems multiply | Versioned save schema, serialization validation, deterministic event journal, state machines and replayable tests |
| P2 | The current test harness mocks the DOM/canvas; local visual browser preview was blocked in that environment | Automated test success does not certify the game is attractive or pleasant to play | Real-browser screenshot/playtest gate on desktop and mobile, plus manual sensory inspection |

## Existing systems worth retaining as reference

- A soft storybook palette and original Mama/two-cub cover illustration.
- Two connected spaces (cave interior and forest), even though collisions and animation need work.
- Basic save/load migration, health and injury consequences, Mama hunting/departure, sibling death, and a simple event log.
- Keyboard and touch action access.

Do not convert the current prototype into a patchwork of increasingly large conditional functions. Prefer a small, clean re-architecture with tests and data-driven behavior. Preserve save identity and user-facing features whenever safely possible.
