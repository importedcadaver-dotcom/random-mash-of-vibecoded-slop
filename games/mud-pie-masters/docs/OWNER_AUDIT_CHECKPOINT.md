# Mud Pie Masters — technical and design audit checkpoint

Baseline: main at fdd2ef8. Judge art and clearing fix are tracked separately in #28. Local browser and Windows prototypes are separate evidence.

The full title-to-two-contest scripted browser-source route succeeded, as did 48/48 contests through legal scripted input. These checks do not establish player comfort, replay motivation, or two hours of meaningful human play. Release gate #2 remains open.

## Findings

- Main retained the older desktop music and enabled audio on fresh profiles. The audit candidate defaults to silence, replaces the music WAV and its generator, and uses explicit start/stop for music. Existing save preferences and optional desktop effects remain supported.
- A historical local browser launcher had a stale archive path. The cleaned local preview has one package and the replacement WAV. The local browser code and package are not shipped by this PR.
- Decorative glyphs in buttons rendered as empty boxes in the browser. The equivalent desktop labels now use words.
- The Golden Mud Cup framing refers to six deciding contests. The existing final-round winner and campaign-completion epilogue leave a separate cup outcome unestablished. Resolving it requires a design decision.
- Seven non-bear creature types are referenced in text. The checked asset manifest has no dedicated non-bear character or Mama sprite. Narrated audience activity and commission titles are distinct from visible or voiced characters.
- Repeated feedback, dense opening choices, early submission, and the size of the game scene controller are follow-up review items. Preserve pie handling, save compatibility, existing competition rules, and approved art.

## Roadmap

1. Verify package provenance, accessibility and audio behavior through both launch paths. Establish a player-facing text inventory and maintenance check.
2. Settle the owner-directed opening, family roles and visual direction before changing story or art.
3. Test a small crafting and relationship slice before extending the full campaign. Compare player comprehension and voluntary replay with the current first two contests.
4. Resolve materials, contest organization and finale semantics through direct owner review.
5. Use a category-specific scorecard, with independent owner and reviewer ratings, and keep the physical and human QA gates open until met.

The private owner roadmap and its open creative decisions are maintained in the owner handoff. No new lore or gameplay decisions are established here.
