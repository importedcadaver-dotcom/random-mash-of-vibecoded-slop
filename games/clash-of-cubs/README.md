# Clash of Cubs — playable prototype

**Project label:** `Codex / clash-of-cubs / playable-prototype`  
**Repository:** [`importedcadaver-dotcom/random-mash-of-vibecoded-slop`](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop)  
**Repository path:** `games/clash-of-cubs/`

An offline, single-player strategy prototype set in Mosswood Valley. It runs in a modern desktop or mobile browser and stores progress in that browser's local storage.

## Run it

Open `index.html` in a browser. No server, engine installation, account, network connection, or external asset is required. For a temporary local preview server from this folder, run:

```powershell
node preview-server.js
```

Then open `http://127.0.0.1:4173`. Press Ctrl+C in the terminal to stop the preview server. Run `node verify.js` to check the main gameplay routes.

## Play

- Tap a den building to upgrade it. The Nursery raises the number of cubs your den can house; the Honey Pantry and Log Wall reduce losses on unattended nights.
- Train Roller, Climber, Screecher, Tunnel, and Sleepy cubs from **Train cubs**.
- Scout Maple-Moon Outpost, pick a cub, tap a building or guard, then send the cub.
- Roller cubs hit walls hard, Climbers bypass them, Tunnel cubs burrow underneath, Screechers briefly distract the guard, and Sleepy cubs hit harder after their first turn.
- Clear two outpost targets to bring back raid supplies. Survivors return to your roster. **End day** triggers a small scripted night raid against your stash.
- Progress saves automatically in the browser. Clear local storage for this site to start over.

Raids are staged as storybook conflicts. A scripted rare loss scene represents a cub's death without depicting injury or gore; the remaining cubs react with fear and grief, and the roster records that permanent loss.

## Decisions and limits

- Godot was not available as a runnable engine in this environment, so the prototype uses browser-native HTML, CSS, and JavaScript. That keeps the game offline and launchable without installing software.
- The rival is a fixed scripted outpost. There is no online play, backend, build timer, account, purchase, or publishing flow.
- The den has a compact upgrade loop. Some listed resources (fish, timber, toys) appear as raid and training supplies; detailed production chains are outside this slice.
- Visuals use original CSS, Unicode icons, and browser fonts. No existing game or bear-project assets are included.
- This is a prototype, not a full mobile-base strategy game. The outpost can be replayed, and upgrades carry into later days.

## Tool checks

See `tool-checks.md` for what was actually available and tested during this build.


