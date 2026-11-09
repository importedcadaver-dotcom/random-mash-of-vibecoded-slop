# Mud Pie Masters — Visual identity v0.3

## Why the v0.2 art was replaced

The original smooth vector bears had nearly circular heads, enormous shiny eyes,
uniform geometry, pink cheeks, and a generic mascot expression. The background
was an undifferentiated gradient of soft green. Pies appeared as clean cylinders.
The beige rounded panels didn't relate to the forest craft theme. It looked like
several unrelated clip-art assets composited into an interface.

## Current art direction: Woodland print-shop pixel art

- **Human-authored, restricted palette.** The colors have physical roles: dark
  pine for depth, desaturated fir green for foliage, ochre paper for information,
  brick and walnut for wood, and a small range of earthen browns for wet/dry mud.
  No gradient-filled, airbrushed, fake 3D, blurry or generic pastel surfaces.
- **Actual pixel language.** Characters are composed at 150×180 and scaled with
  nearest-neighbor sampling. Backgrounds are constructed at 640×360 and doubled.
  Avoid antialiased sprite enlargements. UI typography uses local system serif
  headings and monospaced technical labels, with solid scored plaques.
- **Distinct cubs.** Player has a rust-colored neckerchief; Bruno is dark and
  heavily browed with a work bandana and mud scuffs; Daisy is smaller in scene
  layouts, with flowers and a meadow-green scarf; three judges have visual props.
  Differences must remain visible at actual gameplay scale, not only portrait size.
- **Materials first.** Mud must appear like irregular stacked soil, including
  grit, uneven rims, rough sediment bands and visible cracks. Pebbles are heavy,
  leaves lightweight, sticks linear, berries and petals limited bright accents.
- **Crisp and functional UI.** 2–3px woodcut borders, printed-scoreboard feeling,
  muted active state, no glossy pill buttons. Existing hitboxes are preserved.
- **Do not ship generated mockups as game artwork.** All current playable images
  are constructed deterministically from `tools/generate_pixel_art.py` and are
  editable pixel-by-pixel in code. No generative-image outputs are required.

## Assets used by the game

`forest.png`, `table.png`, `player.png`, `bruno.png`, `daisy.png`,
`petal.png`, `boulder.png`, `fern.png`.

Regenerate all PNGs with `python tools/generate_art.py` after installing Pillow.
Pygame uses these PNGs at runtime; Pillow is not a gameplay dependency.

## Acceptance gates still open

1. Capture *real* Pygame screen frames on Windows and check layouts at 1280×720,
   1600×900, and a smaller 16:9 window.
2. Test zoom/resizing for pixel consistency and clickable ingredient targets.
3. Verify character expressions and environmental animation feel alive, not
   just decorative motion. The current bear sheet does **not** yet include
   distinct authored walk, blink, or celebration frames.
4. Collect actual player feedback. This is a targeted art-direction revision,
   **not** a claim of studio-quality finished animation.

## v0.4 — Soft Cub Pass (provisional candidate)

**User feedback:** v0.3 still wasn't cute enough. Baby-cub appeal needs to be visible at the size used in *actual screens*, not only in zoomed portraits. This is the next proposal, not a locked art direction.

- Replaced the three main-cub PNGs with a consistent authored pixel construction (`tools/generate_cute_cubs.py`). The cheeks and eyes are larger, muzzles shorter, paws rounder and bodies smaller relative to the head. All three cubs now have separate idle, blink, cheer and sad frames, 12 total PNGs.
- The player's spotted red kerchief, Bruno's folded ear and blue bandana, and Daisy's flower, violet scarf and clasped paws preserve recognizability even when scaled down.
- `_sprite` chooses idle-blink frames without disturbing game state, and supports an explicit cheer/sad expression in presentations/results. Reduced-motion disables idle blinking and bobbing.
- The **actual Pygame craft screen** now displays the player cub alongside the pie, with situational speech such as “Squish squish!” or “I DID THAT!” This illustration has no click hitbox and doesn't intercept crafting input.
- Generated static PNG layout previews for crafting and title are **not** a claim of captured Pygame gameplay. They are composed from the exact same runtime PNG assets.
- Build-time assets remain deterministic, open to manual refinement and editable in Python. No image-generator proof-of-concept collage was shipped, and no paid/image-API dependency exists.
- Judges still use v0.3 portraits. Environments and the basic utility UI remain more utilitarian than the main cubs; polish, walk cycles, actual Windows screenshot QA and the two-hour playtime gate are unfinished.

**Regeneration:** after installing Pillow *only for art development*, run
`python tools/generate_art.py` from the project root. It first draws the base backgrounds and judges and then installs the v0.4 main cub sprites and expressions.
