# Tool availability and workflow checks

Checks were performed on 2026-11-08 in the current Windows environment.

| Tool | Finding | What was verified |
|---|---|---|
| Godot | Not found as a runnable Godot executable | `godot`/`godot4` were not available in PATH or common install folders. `godot-ai.exe` alone did not provide a game engine runtime. |
| Node.js | Available | Node v24.19.0 parsed and ran the expanded verification harness and started a short background HTTP server smoke check. The preview server starts; a browser fetch to its local port was denied by the environment. |
| Aseprite | Installed | Aseprite 1.3.18.3-dev returned version and help output. Its batch import rejected SVG input, so no Aseprite asset pipeline was used. |
| Python | Launch failed | Python launch shims were present, but the selected runtime failed to spawn its child interpreter. |
| Krita | Installed | App folder detected; its background workflow was not exercised. |
| Word / Excel / PowerPoint | Installed but blocked for background automation | COM create/save checks for all three returned Windows access denied (80070005) before a document or workbook was created. |

| Blender, Pixelorama, Inkscape, Rive, FFmpeg | Not found as runnable commands | No runnable command was found in PATH or the checked common application folders. |
| Browser rendering | Blocked in this session | The local browser tool timed out on the local preview URL and its policy rejected `file:` URLs. The local-page restriction was respected; no alternate browser path was attempted. |

## Game verification

`node verify.js` passed for the village-map and live-raid revision. The local harness parses and executes the game's real JavaScript with a mock DOM and controllable clock and covers:

- building placement and upgrades, resource caps and production, all five unit types, squad selection, save and reload, and home defense
- deployment from trail edges, cub movement and autonomous attacks, guard counterattacks, raid rewards, and two rival wins
- climber routes, roller wall damage, screecher stun, tunnel damage, and sleepy-cub timing
- the advanced-guard loss scene, emotional response, and saved casualty
- no external network dependency in the game source

The preview server started, but the in-app browser timed out opening the local URL. Visual layout and real pointer input remain unverified.

