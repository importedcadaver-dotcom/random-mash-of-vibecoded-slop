"""Deterministic, explainable scoring. No arbitrary random judgement."""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from math import exp
from .models import Pie, clamp, evaluate_stability

FEATURES = ("Size", "Decoration", "Symmetry", "Originality", "Integrity")
JUDGES = (
    ("Petal", "The Flower Collector", (0.08, 0.52, 0.16, 0.19, 0.05)),
    ("Boulder", "The Giant-Pie Fan", (0.49, 0.05, 0.05, 0.25, 0.16)),
    ("Fern", "The Perfectly Even", (0.07, 0.17, 0.49, 0.08, 0.19)),
)
THEMES = (
    ("Festival of Flowers", "Decorations are in fashion!", "Decoration"),
    ("The Tallest Tale", "Go BIG, but don't topple!", "Size"),
    ("Neat as a Leaf", "Beautiful balance is the theme.", "Symmetry"),
    ("Wild Imagination", "Try something wonderfully unusual.", "Originality"),
    ("The Great Sturdy Bake", "Structural brilliance wins praise.", "Integrity"),
)


@dataclass
class Verdict:
    name: str
    title: str
    score: float
    breakdown: dict[str, float]
    comment: str


@dataclass
class Judgment:
    features: dict[str, float]
    verdicts: list[Verdict]
    total: float
    feedback: list[str]


def fingerprint(pie: Pie) -> str:
    """Stable, interpretable design signature; excludes exact pixel placement."""
    counts = Counter(d.kind for d in pie.decorations)
    # Broad placement regions make intentionally different arrangements
    # different designs, without rewarding meaningless one-pixel adjustments.
    spatial = ''.join(
        ''.join(str(min(3, sum(d.kind == kind and side(d.x) == region
                               for d in pie.decorations) // 2)) for region in (-1, 0, 1))
        for kind in ("leaves", "petals", "pebbles", "sticks", "berries")
    )
    tier_offsets = ''.join(str(side(layer.x / max(1,layer.width*.35))+1) for layer in pie.layers)
    angle_profile = "".join(str(min(3, sum(d.angle // 60 == bucket for d in pie.decorations) // 3)) for bucket in range(6))
    silhouette = "".join(str(min(4, int(layer.width // 62))) for layer in pie.layers)
    return f"{len(pie.layers)}-{int(pie.height // 65)}-{silhouette}-{angle_profile}-" + "".join(
        str(min(5, counts.get(k, 0) // 3)) for k in ("leaves", "petals", "pebbles", "sticks", "berries")
    ) + "-" + "".join(layer.shape[0] for layer in pie.layers) + '-' + tier_offsets + '-' + spatial


def side(x: float) -> int:
    return -1 if x < -.25 else 1 if x > .25 else 0


def _mirror_pairs(pie: Pie) -> tuple[int, float]:
    """Return intentionally matched pairs and their angle-aware precision."""
    unused = list(range(len(pie.decorations)))
    count = 0
    precision = 0.0
    while unused:
        i = unused.pop(0)
        a = pie.decorations[i]
        if abs(a.x) < .19:
            continue
        matches = [j for j in unused if (pie.decorations[j].kind == a.kind
                   and pie.decorations[j].layer == a.layer
                   and pie.decorations[j].color == a.color)]
        if not matches:
            continue
        j = min(matches, key=lambda k: abs(pie.decorations[k].x + a.x)
                + abs(pie.decorations[k].y - a.y))
        b = pie.decorations[j]
        pos_error = abs(a.x + b.x) + abs(a.y - b.y)
        rotation_error = min(abs((a.angle + b.angle) % 360),
                             360 - abs((a.angle + b.angle) % 360)) / 180.
        if pos_error < .28 and rotation_error <= .30:
            count += 1
            precision += max(0., 1. - pos_error * 1.5 - rotation_error * .35)
            unused.remove(j)
    return count, precision


def feature_scores(pie: Pie, recent_signatures: list[str] | None = None,
                   weather: str = "clear") -> dict[str, float]:
    if not pie.layers:
        return dict.fromkeys(FEATURES, 0.0)
    stability = evaluate_stability(pie, weather=weather).score
    counts = Counter(d.kind for d in pie.decorations)
    n = sum(counts.values())
    kinds = len(counts)
    color_count = len({d.color for d in pie.decorations})
    angles = len({int(d.angle // 45) for d in pie.decorations})
    # Occupancy, not raw quantity: scattering 30 identical pebbles on one pixel
    # cannot create the illusion of thoughtful composition.
    occupied = {(d.layer, min(2, max(0, int((d.x + 1) * 1.5))),
                 min(2, int(d.y * 3))) for d in pie.decorations}
    density = n / max(1, len(occupied))
    pairs, paired_precision = _mirror_pairs(pie)
    coverage = min(1., len(occupied) / 9.)
    # Curated detail: material combinations + distribution + motifs. Unvarying
    # clusters eventually LOSE points as they become overcrowded.
    decoration = clamp(6 + kinds * 8.3 + 14 * coverage
            + min(13, n * 1.0) + 7 * min(1., max(0, color_count - 1) / 3)
            + min(12, pairs * 3.0) - min(28., max(0., density - 3.) * 3.5), 0, 100)
    if n < 3:
        decoration *= .55
    # Size is bounded by *actual scooped material*, not free geometry stretching.
    volume = sum(l.volume for l in pie.layers if not l.fallen)
    size = clamp(9 + 23 * (1 - exp(-pie.height / 190.))
                 + 12 * (1 - exp(-pie.footprint / 185.))
                 + 43 * (1 - exp(-volume / 30000.))
                 + 2 * len(pie.layers), 0, 100)
    offsets = sum(abs(l.x) / max(1., l.width / 2) for l in pie.layers) / len(pie.layers)
    if n < 2:
        # An empty plate is visually balanced, but shows no demonstrated skill.
        symmetry = clamp(22 + 10 * (1 - min(1, offsets)), 0, 40)
    else:
        ratio = 2 * paired_precision / n
        deliberate = min(1., n / 6.)
        symmetry = clamp(18 + 72 * ratio * deliberate
                         + 10 * (1 - min(1, offsets)), 0, 100)
    # Originality encourages distinctive silhouettes, placements, material
    # combinations and angled motifs, without awarding point for every pebble.
    shapes = len({l.shape for l in pie.layers})
    silhouette = len({int(l.width // 42) for l in pie.layers})
    offbeat = min(14., max(0., 80. - symmetry) * .25)
    ingenuity = clamp(17 + 7 * shapes + 4 * min(4, silhouette - 1)
                     + 7 * kinds + 5 * min(3, angles - 1)
                     + 8 * coverage + offbeat, 0, 100)
    repeats = (recent_signatures or [])[-8:].count(fingerprint(pie))
    originality = clamp(ingenuity - 24 * repeats, 0, 100)
    return dict(zip(FEATURES, (round(size, 1), round(decoration, 1),
                               round(symmetry, 1), round(originality, 1),
                               round(stability, 1))))

def effective_weights(base_weights: tuple[float, ...], theme: str) -> dict[str, float]:
    """A contest focus is consequential without erasing individual tastes.

    65% reflects the public competition brief; the remaining 35% expresses
    each judge's distinct preferences. Displayed weights are the true weights.
    """
    weights = dict(zip(FEATURES, base_weights))
    if theme in FEATURES:
        return {key: value * .35 + (.65 if key == theme else 0.)
                for key, value in weights.items()}
    return weights

def judge(pie: Pie, theme: str, recent_signatures: list[str] | None = None,
          weather: str = "clear") -> Judgment:
    scores = feature_scores(pie, recent_signatures, weather=weather)
    verdicts = []
    repeats = (recent_signatures or [])[-8:].count(fingerprint(pie))
    # Transparent repetition fatigue applies to all judges, not merely the
    # originality specialist. Otherwise generic templates win every round.
    repeat_penalty = min(38., repeats * 13.)
    for name, title, base_weights in JUDGES:
        weights = effective_weights(base_weights, theme)
        score = clamp(sum(scores[k] * weights[k] for k in FEATURES) - repeat_penalty, 0, 100)
        if name == "Petal":
            comment = ("What a sweet little masterpiece of detail!" if scores["Decoration"] >= 68
                       else "More colors and thoughtful little clusters, please!")
        elif name == "Boulder":
            comment = ("That is a MOUNTAIN of mud!" if scores["Size"] >= 65
                       else "A handsome pie. Could it be twice as tall?")
        else:
            comment = ("Every little piece is in its place!" if scores["Symmetry"] >= 75
                       else "One side is heavier. Balance your lovely details!")
        if repeats:
            comment = f"Repeat recipe (-{repeat_penalty:.0f}). " + comment
        verdicts.append(Verdict(name, title, round(score, 1), scores.copy(), comment))
    feedback = []
    if scores["Integrity"] < 32:
        feedback.append("Your top tiers were unsupported; your tower collapsed!")
    elif scores["Integrity"] < 58:
        feedback.append("A little wobble! Wider, drier lower tiers will help.")
    else:
        feedback.append("Your mud layers are standing strong.")
    if scores["Symmetry"] < 65:
        feedback.append("Try placing matching decorations on opposite sides.")
    if scores["Decoration"] < 55:
        feedback.append("Mix several ingredients into clear, deliberate patterns.")
    if repeats:
        feedback.append(f"Repeat design: all judges deduct {repeat_penalty:.0f} points. Change your silhouette or arrangement!")
    if scores["Symmetry"] < 45:
        feedback.append("Bare tiers are not a symmetry pattern. Place deliberate mirrored pairs.")
    if scores["Decoration"] < 50:
        feedback.append("Spread details into different areas; piling objects in one spot does not help.")
    return Judgment(scores, verdicts, round(sum(v.score for v in verdicts) / len(verdicts), 1), feedback)
