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