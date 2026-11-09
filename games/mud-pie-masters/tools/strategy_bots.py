"""Inspectably distinct QA strategies; never autoplay the human game."""
from __future__ import annotations

from mudpie.models import Pie


def architect() -> Pie:
    pie = Pie(title='Architect - six brave levels')
    for i in range(6):
        pie.add_layer(0, 220 - i * 22, 60, .50,
                      shape=('round', 'oval', 'craggy')[i % 3])
    for i in range(8):
        pie.add_deco(('leaves', 'sticks', 'pebbles')[i % 3], i % 6,
                     (-.65, .6)[i % 2], .5)
    return pie


def florist() -> Pie:
    pie = Pie(title='Floral panorama')
    pie.add_layer(0, 190, 45, .53)
    pie.add_layer(0, 165, 52, .51)
    for i in range(26):
        pie.add_deco(('petals', 'leaves', 'pebbles', 'berries', 'sticks')[i % 5],
                     i % 2, (-.75, -.35, .35, .75)[i % 4],
                     (.17, .38, .65, .82)[(i // 3) % 4], color=i % 4)
    return pie


def precision() -> Pie:
    pie = Pie(title='Perfect paired flower crown')
    pie.add_layer(0, 210, 49, .52)
    pie.add_layer(0, 170, 52, .51)
    for i in range(7):
        kind = ('petals', 'leaves', 'sticks')[i % 3]
        x = .30 + i * .062
        y = .24 + i % 4 * .17
        pie.add_deco(kind, i % 2, x, y, color=i % 3)
        pie.add_deco(kind, i % 2, -x, y, color=i % 3)
    return pie


def generic() -> Pie:
    """Large, decorated template from the v0.4 game-design audit."""
    pie = Pie(title='Never-changing generic pie')
    pie.add_layer(0, 220, 52, .48)
    for i in range(4):
        pie.add_layer(0, 200 - i * 14, 60, .48,
                      shape=('round', 'oval', 'craggy')[i % 3])
    for i in range(28):
        pie.add_deco(('petals', 'leaves', 'berries', 'sticks', 'pebbles')[i % 5],
                     i % 5, (-.70, -.36, .36, .70)[i % 4],
                     .2 if i % 2 else .65, color=(i // 4) % 2)
    return pie
