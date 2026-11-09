# Source import verification · ChatGPT GPT-6 · v0.5.0

**Repository:** `importedcadaver-dotcom/random-mash-of-vibecoded-slop`
**Path:** `games/mud-pie-masters/`
**Source:** `MudPieMasters-v0.5.0.zip` generated in this conversation.
**Authoring agent label:** `ChatGPT GPT-6 / mud-pie-masters / import-v0.5`.
**Import result:** 76 files copied into Git objects, plus 3 new game-specific metadata/handoff files. The complete game source, tests, generated artwork PNGs, original WAV audio, and Windows support scripts are present.

## Example Git object checksums
- `main.py`: `a3375a764fe359f64a55b363b3328f88c36849b3`
- `mudpie/game.py`: `d0d3c6ebcbc6aeb1f177e758c222685b996e6fd5`
- `mudpie/models.py`: `f2ff9ab74be0869dd23766da0fbdbd460b0a470b`
- `assets/music.wav`: `61c087c31c34c6a73990be72a0f66314e10e9b03`
- `assets/player.png`: `fe49df9e0361e25271f0ed7e114b8d106a2e9b4e`
- `tests/test_fun_redesign.py`: `dcc6c999915f83336c0c9c26033ad6b9844a7aa9`

These six SHA-1 Git blob object IDs were independently calculated from the local ZIP and compared to the remote Git tree.

## Executed in isolated Python 3.13 environment
- `python -m pytest -q`: **116 passed, one module skipped** (pygame-ce unavailable in the sandbox).
- `python tools/simulate_campaign.py`: simulated 48 authored contests, 127 goal stars, 14 deterministic collapse events; not a real playtime measurement.
- ZIP archive integrity check: no errors.

## Not yet verified
- Running pygame-ce game on Windows, UI input, audio playback and animation.
- PyInstaller executable built and run on Windows.
- A real human first playthrough with **two enjoyable hours**, which is still the owner's release gate.

Use GitHub Actions' Windows+Ubuntu workflow for the first remote automated validation and clearly report any failures. Source import is complete; game release QA is not.
