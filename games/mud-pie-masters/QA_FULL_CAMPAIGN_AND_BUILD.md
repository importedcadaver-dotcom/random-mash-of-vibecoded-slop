# Mud Pie Masters — Complete Campaign Runtime QA & Windows Package

**Agent:** Mossbyte — ChatGPT GPT-6, project agent MPM-MOSSBYTE-GPT6-001
**Date:** 2026-11-09 America/Los_Angeles (CI logs UTC Nov 10)
**PR:** https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/pull/8
**Status:** v0.6.1-QA preview. **NOT** certified for two hours of enjoyable human gameplay.

## Research

See [GENRE_RESEARCH_AND_REVIEW.md](GENRE_RESEARCH_AND_REVIEW.md) for primary-game descriptions, Reddit discussion, and supportive/critical Steam reviews of Papa's Bakeria, Sticky Business, Passpartout 2, and SuchArt.

Most significant findings: player-created designs must be intrinsically pleasant; full judge feedback must be accessible; avoid 48 repetitive ingredient checklists disguised as content; callbacks/character moments are important; tool controls should make sense without reading a long manual.

## Latest verified automated runs

- **Windows/Linux tests and complete-game scenes:** https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/actions/runs/42744247759
  - **138 pytest tests passed** on **each OS**.
  - Existing single-round SDL mouse/keyboard walkthrough passed with screenshots.
  - Synthetic campaign data-model tests passed.
  - New full-campaign runtime loop: **36 story contests + 12 side commissions** through the actual Pygame game engine's clearing, workbench, presentation, judging, and results scenes. Automated **48 real results and save/reload checks** passed, including six chapter transitions.
  - Mouse events place the **first scoop** and submit through actual GUI hitboxes; **the remaining complex test pie geometry is injected from the challenge oracle** (explicit limitation, not natural human crafting).
  - All six chapters and optional commissions, final epilogue scene, gallery pagination and new Game() process-level restart state verified.
  - Screenshot artifacts capture actual SDL/Pygame rendered scenes, NOT a physical monitor. The earlier full-run sample recorded 1104 injected SDL events and 16 screenshots; the newer ending extension adds final-scene, gallery and restart captures.
- **Windows native executable build and launch:** https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/actions/runs/42744247649
  - PyInstaller --onedir --windowed built **MudPieMasters.exe** and its required _internal folder on a real Windows GitHub Actions runner.
  - A Python subprocess waited for the GUI executable to finish an internal **--qa-smoke** check.
  - Smoke rendered a title frame from packaged assets, loaded bear/forest art, launched free build, saved a pie to an isolated save directory, and wrote a success marker. Exit code and marker verified.
  - This verifies **packaged headless launch**, not actual user hardware, speaker output, frame rate, SmartScreen prompts, full game duration or aesthetic enjoyment.
- **Required governance check:** passed for these changes; shared multi-agent repository structure remains intact.

## Player-facing Windows install

The downloadable CI artifact is **MudPieMasters-Windows-PreRelease.zip** (actual executable + _internal, no Python required). Extract the entire ZIP to a standalone new folder; keep the _internal directory beside the executable. Double-click **MudPieMasters.exe**.

Suggested PowerShell:
```powershell
New-Item -ItemType Directory -Force "$HOME\MudPieMastersPreview" | Out-Null
Expand-Archive "$HOME\Downloads\MudPieMasters-Windows-PreRelease.zip" -DestinationPath "$HOME\MudPieMastersPreview" -Force
& "$HOME\MudPieMastersPreview\MudPieMasters.exe"
```

The ZIP is produced by [Windows GitHub Actions](https://github.com/importedcadaver-dotcom/random-mash-of-vibecoded-slop/actions) and is currently unsigned; if Windows SmartScreen warns, verify the archive's provenance before deciding whether to allow execution. For extra caution, test the source version using the user's existing Python 3.12 and pygame-ce environment.

## Outcome and limits

- Real runtime completion and save stability: **passing under automated SDL test drivers on Windows/Linux**.
- Windows packaged application loading assets / launching headless: **passing**.
- Human interactive controls, speaker output, accessibility in varied desktop DPI settings, actual Windows GPU frame rate, the full campaign with genuine mouse-crafted pies, and meaningful player feedback: **NOT verified**.
- **No human time-to-completion was measured.** Bot execution time is an automation metric only; synthetic 48-contest progression does not certify the target **2 enjoyable hours**.
- Keep `game.json` field `gameplay_hours_verified` set to **false**.
- Player asked not to play before the target is proven; do not portray a QA build as the final release.

## Next quality actions

1. Commission an independent observed human first-time full-game playtest (not necessarily the repository owner), record actual active minutes and engagement, identify repetitious moments and softlocks.
2. Verify on a real Windows desktop that drag-and-drop, audio, full-screen, save files and keyboard controls are reliable at the actual DPI scale.
3. Balance judging and story diversity based on actual observed human behavior, not only the challenge oracle.
4. Only after human evidence verifies **>= 120 meaningful minutes** and Windows release QA, change `gameplay_hours_verified` and issue the final release.
