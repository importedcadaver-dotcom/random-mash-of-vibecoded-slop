# Clash of Cubs — base-builder prototype

**Work label:** `Codex / clash-of-cubs / base-builder-expansion`  
**Repository:** [`importedcadaver-dotcom/random-mash-of-vibecoded-slop`](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop)  
**Project folder:** `games/clash-of-cubs/`  
**Branch:** `agent/clash-of-cubs/base-view-redesign`

## Visual direction

The first pass looked like a management dashboard. This revision puts the den map first: an original, storybook isometric meadow with visible buildings, walls, trees, building levels, and resource yields. Resource counters stay at the top; Attack, End day, build shortcuts, squad status, and building upgrades sit around the map. The map is built from inline SVG and CSS, so it stays self-contained and uses no copied game art.

An original, offline, single-player den-building and raiding prototype set in Mosswood Valley. It runs in a modern desktop or mobile browser, uses original CSS and Unicode art, and saves progress in that browser.

## Run it

Open `index.html` in a browser. No installation, account, network connection, or external assets are required.

For a local preview server, run `node preview-server.js` from this folder and open `http://127.0.0.1:4173`. Run `node verify.js` to check the main gameplay routes.

## Play

- **Build:** Open Build or use the den workshop shortcuts, select a blueprint, then tap an open diamond plot on the village map. Tap a placed building to inspect and upgrade it. Each resource has a visible storage cap.
- **Gather:** Honey hives, berry patches, fish ponds, toy workshops, and timber mills produce supplies when you end the day. Supply burrows increase storage capacity.
- **Train:** Recruit Roller, Climber, Screecher, Tunnel, and Sleepy cubs. Use plus and minus to choose your expedition squad; the Nursery and Training Grove upgrades raise their capacities.
- **Raid:** Tap Attack, scout a rival, select a cub, then tap a trail edge to deploy it. Cub units pick and fight targets automatically; walls and guards answer back in real time. Clear two loot spots to earn a full haul and unlock another rival. Retreat to keep part of the loot already gathered.
- **Defend:** End the day to resolve a scripted home raid, calculate protection from walls, lookouts, and traps, gather production, and advance the day.
- **Bear Book:** Review cub abilities and dialogue, rival wins, and any cubs lost in dangerous expeditions.

The Attack button on the home den opens the rival trail map. During a raid, choose a cub, choose a trail edge, and deploy. Cubs move to targets on their own, use specialist behavior, and take return fire while the 75-second raid clock runs. Clear two supply stores for a full haul; retreat to bring back part of any loot already collected.

## Specialist abilities

- Roller cubs deal heavy damage to walls.
- Climbers bypass active walls and guards to reach loot.
- Screechers stun nearby lookouts for a brief stretch of the raid.
- Tunnel cubs burrow through walls or emerge under structures.
- Sleepy cubs start with a small attack. Wake one before deployment to charge a stronger move.

Advanced rival guards can cause permanent cub losses. Loss scenes show the litter's fear and grief without graphic injury or gore.

## Save and verification

The game stores a versioned save in browser local storage and migrates basic progress from the earlier prototype save. Clear this site's local storage to start over.

`node verify.js` uses a local mock DOM and clock to exercise map placement and upgrades, training, squad assignment, save and reload, edge deployment, autonomous raid ticks, guard stun and casualty outcomes, raid rewards, nighttime production, and home defense. The local preview server started successfully, but the in-app browser timed out opening it, so visual rendering and pointer input remain unverified.

## Scope

Rival dens are scripted and replayable. There are no accounts, online battles, purchases, timers, server, or publishing flow. This is a compact prototype; it does not include a full-time multiplayer ecosystem or production-ready art pipeline.

