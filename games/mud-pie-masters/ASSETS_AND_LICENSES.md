# Assets, authorship and licensing — v0.3

All eight shipped PNG assets (`forest.png`, `table.png`, and six individual bear
sprites) are newly made, for this project, from authored geometric pixel-art
instructions in `tools/generate_pixel_art.py`. No downloaded stock artwork,
third-party game screenshots, AI-generated mockup pictures, or copyrighted game
assets are included in the playable image set.

All WAV files (four effects and a short music loop) were mathematically
synthesized specifically for this game using `tools/generate_audio.py`. No
prerecorded commercial loops or copyrighted songs were sampled.

Required Pygame Community Edition and optional development tools retain their
respective open-source licenses. The game uses the user's available system fonts
and distributes **no font files**.

The `docs/` visual previews are automatically composed from the game's own
assets; they are **static layout previews**, not actual Pygame captures. See
`ART_DIRECTION.md` for constraints and planned improvements.

### v0.4 cubs / expressions

`player.png`, `bruno.png`, `daisy.png` and their `_blink`, `_cheer`, and
`_sad` variants are original assets authored by this project with Pillow
vector-pixel primitives in `tools/generate_cute_cubs.py`, then exported to
PNG using nearest-neighbor scaling. The older v0.3 PNGs have been superseded.
No outside art or generated watercolor mockups are contained in these assets.
