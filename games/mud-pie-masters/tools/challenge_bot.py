"""Synthetic goal-satisfying pie constructor for QA, never used to play the game.

WARNING: It does not simulate mouse motions or aesthetic quality. Only checks
that every data-defined mission has an attainable geometry/decorations state.
"""
from __future__ import annotations
from collections import Counter
from mudpie.models import Pie

def design_for(challenge):
    """Builds a data-model solution to check goals aren't logically contradictory.

    It is a construction oracle, NOT evidence that a human player can easily do it.
    """
    wants = {g.rule: g.target for g in challenge.goals if g.rule not in ('kind_min','feature_min')}
    count = max(2, int(wants.get('tiers_min', 1)), int(wants.get('layer_pattern_min', 0)), int(wants.get('workability_min', 0)))
    count = min(7, count)
    if 'tiers_max' in wants:
        count = min(count, int(wants['tiers_max']))
    count = max(count, int(wants.get('shapes_min',1)))
    while count * 72 < wants.get('height_min', 0):
        count += 1
    pie = Pie(title=challenge.title)
    for i in range(count):
        shape = ('round','oval','craggy')[i % 3]
        offset = int(wants.get('offset_min', 0)) if i == count - 1 and count>1 else 0
        width = max(190, int(wants.get('width_min', 0)))
        if 'compact_max' in wants:
            width = min(width, int(wants['compact_max']))
        if wants.get('taper_min', 0) and i == 1:
            width -= int(wants['taper_min']) + 4
        layer = pie.add_layer(x=offset, width=width, height=72,wetness=.47,shape=shape)
        if i < int(wants.get('workability_min', 0)):
            layer.mix(185)

    allowed = set(challenge.allowed or ('mud','leaves','petals','pebbles','sticks','berries'))
    kinds = [k for k in ('petals','leaves','berries','pebbles','sticks') if k in allowed]
    desired_kinds = int(wants.get('kinds_min', 0))
    for g in challenge.goals:
        if g.rule == 'kind_min' and g.kind not in kinds:
            raise ValueError('Impossible requirement: '+challenge.id)

    # Add balanced pairs of each ingredient, coloring within a newly unlocked palette.
    required = Counter()
    for g in challenge.goals:
        if g.rule == 'kind_min': required[g.kind] = max(required[g.kind], int(g.target))
    for kind in kinds[:desired_kinds]:
        required[kind] = max(required[kind], 2)
    symmetry_required = any(g.rule == 'feature_min' and g.kind == 'Symmetry' for g in challenge.goals)
    target_pairs = max(int(wants.get('pair_min', 0)), 3 if symmetry_required else 0)
    required[kinds[0]] = max(required[kinds[0]], 2 * target_pairs)
    total_needed = int(wants.get('decos_min', 0))
    if total_needed and sum(required.values()) < total_needed:
        required[kinds[0]] += total_needed - sum(required.values())
    top_needed = int(wants.get('top_decos_min', 0))
    if top_needed and sum(required.values()) < top_needed:
        required[kinds[0]] += top_needed - sum(required.values())
    colors_needed = int(wants.get('colors_min', 0))
    if colors_needed and sum(required.values()) < colors_needed:
        required[kinds[0]] += colors_needed - sum(required.values())
    for i in range(int(wants.get('layer_pattern_min', 0))):
        pie.add_deco(kinds[0], i, .2, .4)
    color_i = 0
    requires_pairs = target_pairs > 0
    for kind, n in required.items():
        for j in range(n):
            layer = count - 1 if 'top_decos_min' in wants else (j // 2 if requires_pairs else j) % count
            # Consecutive pairs have equal colors and opposite X.
            x = .49 if j % 2 == 0 else -.49
            color = (j // 2 if requires_pairs else color_i) % max(1, colors_needed)
            angle = 60 * (j % max(1, int(wants.get('angle_variants_min', 1))))
            pie.add_deco(kind, layer, x, .35, angle=angle, color=color)
            color_i += 1
    if top_needed and sum(d.layer==count-1 for d in pie.decorations) < top_needed:
        remaining = top_needed - sum(d.layer==count-1 for d in pie.decorations)
        for j in range(remaining):
            pie.add_deco(kinds[0],count-1, .3 if j%2 else -.3,.42,color=j%6)
    while len({(d.layer, min(2, max(0, int((d.x + 1) * 1.5))), min(1, int(d.y * 2))) for d in pie.decorations}) < int(wants.get('zones_min', 0)):
        index = len(pie.decorations)
        pie.add_deco(kinds[index % len(kinds)], index % count,
                     (-.7, 0, .7)[(index // count) % 3], .2 if (index // 3) % 2 == 0 else .8)
        if index > 100:
            raise AssertionError('Oracle cannot satisfy required areas')
    if 'angle_variants_min' in wants:
        for i in range(int(wants['angle_variants_min'])):
            pie.add_deco(kinds[0], i % count, .7, .6, angle=i * 60)
    return pie

