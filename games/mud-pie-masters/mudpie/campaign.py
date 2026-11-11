"""A finite, data-driven forest-fair campaign, with meaningful craft challenges.

The 36 story contests and 12 optional commissions are deliberately handcrafted.
The campaign never adds idle timers, energy gates, or pay-to-skip padding.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from typing import Any

from .judging import feature_scores
from .models import Pie, evaluate_stability


@dataclass(frozen=True)
class Goal:
    rule: str
    target: float
    kind: str = ""

    @property
    def label(self) -> str:
        name = {
            "tiers_min": f"At least {int(self.target)} mud tiers",
            "tiers_max": f"At most {int(self.target)} mud tiers",
            "decos_min": f"At least {int(self.target)} decorations",
            "kinds_min": f"Use {int(self.target)} decoration types",
            "colors_min": f"Use {int(self.target)} color variants",
            "shapes_min": f"Use {int(self.target)} different mud shapes",
            "kind_min": f"Place {int(self.target)} {self.kind}",
            "kind_max": f"At most {int(self.target)} {self.kind}",
            "feature_min": f"{self.kind} at least {int(self.target)}",
            "height_min": f"Build {int(self.target)}px tall",
            "width_min": f"Make a {int(self.target)}px wide tier",
            "offset_min": f"Offset one tier by {int(self.target)}px",
            "pair_min": f"Create {int(self.target)} mirrored pairs",
            "top_decos_min": f"Put {int(self.target)} details on top",
            "wetness_max": f"Keep mud wetness at most {self.target:.2f}",
            "taper_min": f"Make a step-down of {int(self.target)}px in tier widths",
            "zones_min": f"Decorate {int(self.target)} different areas",
            "workability_min": f"Mix {int(self.target)} workable mud tier(s)",
            "angle_variants_min": f"Use {int(self.target)} decoration angles (R key)",
            "compact_max": f"Keep the pie at most {int(self.target)}px wide",
            "layer_pattern_min": f"Decorate {int(self.target)} separate mud tiers",
            "shaped_decos_min": f"Shape or flatten {int(self.target)} placed {self.kind}",
        }
        return name[self.rule]


def paired_decorations(pie: Pie) -> int:
    """Pairs must match type, color, tier, mirrored x and comparable y."""
    used: set[int] = set()
    pairs = 0
    for i, a in enumerate(pie.decorations):
        if i in used or abs(a.x) < .19:
            continue
        for j in range(i + 1, len(pie.decorations)):
            if j in used:
                continue
            b = pie.decorations[j]
            if (a.kind == b.kind and a.color == b.color and a.layer == b.layer
                    and abs(a.x + b.x) < .22 and abs(a.y - b.y) < .23):
                used.update((i, j))
                pairs += 1
                break
    return pairs


def goal_progress(pie: Pie, goal: Goal, weather: str = "clear") -> tuple[float, bool]:
    counts = Counter(d.kind for d in pie.decorations)
    occupied = {(d.layer, max(0, min(2, int((d.x + 1) * 1.5))),
                 min(1, int(d.y * 2))) for d in pie.decorations}
    taper = max((pie.layers[i].width - pie.layers[i + 1].width
                 for i in range(len(pie.layers) - 1)), default=0)
    rules: dict[str, Any] = {
        "tiers_min": len(pie.layers), "tiers_max": len(pie.layers),
        "decos_min": len(pie.decorations), "kinds_min": len(counts),
        "colors_min": len({d.color for d in pie.decorations}),
        "shapes_min": len({l.shape for l in pie.layers}),
        "kind_min": counts[goal.kind], "kind_max": counts[goal.kind],
        "height_min": pie.height,
        "width_min": max((l.width for l in pie.layers), default=0),
        "offset_min": max((abs(l.x) for l in pie.layers), default=0),
        "pair_min": paired_decorations(pie),
        "top_decos_min": sum(d.layer == len(pie.layers) - 1 for d in pie.decorations),
        "wetness_max": max((l.wetness for l in pie.layers), default=1),
        "taper_min": max(0, taper),
        "zones_min": len(occupied),
        "workability_min": sum(l.workable for l in pie.layers),
        "angle_variants_min": len({int(d.angle // 45) for d in pie.decorations}),
        "compact_max": pie.footprint,
        "layer_pattern_min": len({d.layer for d in pie.decorations}),
        "shaped_decos_min": sum(
            d.kind == goal.kind and
            (abs(d.stretch_x-1.0) >= .22 or abs(d.stretch_y-1.0) >= .22)
            for d in pie.decorations
        ),
    }
    if goal.rule == "feature_min":
        value = feature_scores(pie, weather=weather)[goal.kind]
    else:
        value = rules[goal.rule]
    met = value <= goal.target if goal.rule.endswith("_max") else value >= goal.target
    return round(value, 2), met


@dataclass(frozen=True)
class Chapter:
    name: str
    introduction: str
    bruno_line: str
    daisy_line: str
    keepsake: str


CHAPTERS = (
    Chapter("THE FIRST PUDDLE", "A fallen log becomes a stage. Your siblings agree to hold a grand competition. Nobody has asked the grownups.",
            "Bruno: I'm going to build the tallest pie in FOREST HISTORY!", "Daisy: Can we put flowers on yours? Pretty please?", "First muddy pawprint"),
    Chapter("THE PETAL PICNIC", "The woodland picnic is approaching. The cubs are hired to decorate the clearing, despite their qualifications being mostly mud.",
            "Bruno: Someone called mine a 'mud avalanche'. That's a compliment.", "Daisy: I saved the prettiest petal for you!", "Flower-crown ribbon"),
    Chapter("ROCKY RIDGE", "The contest moves uphill, where pebbles are plentiful, structures wobble, and even the big kids are nervous.",
            "Bruno: We need an engineering department. That's me.", "Daisy: I built a staircase for a beetle. He hasn't used it.", "Ridge-builder badge"),
    Chapter("STORM SEASON", "Rain drums on the leaves. Wet mud is easier to sculpt and much, much harder to balance. A storm can make a disaster memorable.",
            "Bruno: This is a controlled experimental collapse.", "Daisy: Your pie looks like it's dancing!", "Little rain-cloud charm"),
    Chapter("THE MOONLIT FAIR", "Lanterns glow between the trees. The forest animals are here to see sculptures that feel like stories, not just points.",
            "Bruno: I'm inventing a new style. No looking!", "Daisy: Let's make something the stars would love.", "Star-petal medal"),
    Chapter("THE GOLDEN MUD CUP", "The final six contests will decide the Golden Mud Cup. Winning is exciting; making something only you could make is better.",
            "Bruno: If you win, I'll clap. Probably.", "Daisy: We're all mud-pie masters, aren't we?", "Golden mud-cup trophy"),
)


def g(rule: str, amount: float, kind: str = "") -> Goal:
    return Goal(rule, amount, kind)


@dataclass(frozen=True)
class Challenge:
    id: str
    chapter: int
    title: str
    description: str
    focus: str
    goals: tuple[Goal, ...]
    side: bool = False
    allowed: tuple[str, ...] = ()  # empty = all six ingredients
    weather: str = "clear"
    target: int = 60
    story: str = ""


# Each entry: title, focus, short creative brief, pair of independent goals,
# allowed materials, weather, 3-star target, and end-of-contest story beat.
STORY_DATA = (
    (
        ("First Squish", "Decoration", "Prove that a little dirt can be beautiful.", (g("tiers_min", 1), g("kind_min", 3, "petals")), (), "clear", 51, "Daisy names your creation the very first masterpiece."),
        ("Bruno's Big Idea", "Size", "Your brother bets nobody can make a two-tier cake.", (g("tiers_min", 2), g("height_min", 85)), (), "clear", 51, "Bruno insists he thought of stacking first."),
        ("Matching Pawprints", "Symmetry", "Fern wants a design with a proper left and right.", (g("pair_min", 1), g("feature_min", 60, "Symmetry")), (), "clear", 52, "Fern puts your pie on the balancing log."),
        ("The Tiny Garden", "Decoration", "Make a flower patch with at least three plants.", (g("kinds_min", 3), g("decos_min", 7)), (), "clear", 53, "Daisy tries to move in. She says it's a fairy house."),
        ("The Wobble Trial", "Integrity", "Two stories, no falling: a serious engineering challenge.", (g("tiers_min", 2), g("feature_min", 64, "Integrity")), (), "clear", 54, "Bruno considers building a support beam."),
        ("Puddle Parade", "Originality", "The first parade is underway. Make something nobody expected.", (g("kinds_min", 4), g("shapes_min", 2)), (), "clear", 55, "The forest votes to make the contest a tradition."),
    ),
    (
        ("Petal Collector", "Decoration", "Give the judges a crown of petals you have shaped yourself.", (g("kind_min", 9, "petals"), g("top_decos_min", 5), g("shaped_decos_min", 2, "petals")), (), "clear", 55, "Petal admits she has never seen so many flowers in one place."),
        ("Berry Confetti", "Decoration", "The decorations must be delicious-looking. Don't eat them!", (g("kind_min", 5, "berries"), g("colors_min", 2)), (), "clear", 55, "A hungry squirrel is politely turned away."),
        ("Only Leaves", "Symmetry", "The picnic ran out of petals. Get creative with leaves.", (g("kind_min", 8, "leaves"), g("pair_min", 2)), ("mud", "leaves"), "clear", 53, "Daisy calls the matching leaves little green wings."),
        ("Twin Towers", "Size", "Build two beautiful-looking stories with different heights.", (g("tiers_min", 3), g("feature_min", 58, "Integrity")), (), "clear", 57, "Bruno announces he is taking your structural notes."),
        ("Pebble Path", "Symmetry", "A tidy trail of pebbles impresses Fern.", (g("kind_min", 7, "pebbles"), g("pair_min", 2)), ("mud", "leaves", "pebbles"), "clear", 55, "Fern checks each pebble as though it were a gemstone."),
        ("Picnic Crown", "Originality", "A grand centerpiece for the entire picnic.", (g("kinds_min", 5), g("decos_min", 15)), (), "clear", 59, "The judges place their napkins around your pie."),
    ),
    (
        ("Ridge Monument", "Size", "A tall stack to mark the way up the ridge.", (g("tiers_min", 3), g("height_min", 155)), (), "wind", 58, "Bruno appoints himself the official hill architect."),
        ("The No-Flower Rule", "Originality", "The flowers blew away. Flatten some sticks into a bold pattern.", (g("kind_min", 5, "sticks"), g("kinds_min", 2), g("shaped_decos_min", 2, "sticks")), ("mud", "pebbles", "sticks"), "wind", 57, "Daisy discovers sticks can look just as fancy."),
        ("Stone Spiral", "Symmetry", "Balance stones so the tower doesn't lean.", (g("kind_min", 10, "pebbles"), g("feature_min", 63, "Integrity")), (), "wind", 58, "Boulder tries to carry the sculpture home."),
        ("Wide as a Log", "Size", "Height isn't everything. Build a glorious wide base.", (g("width_min", 245), g("feature_min", 68, "Integrity")), (), "clear", 58, "Even Bruno admits your foundation is impressive."),
        ("The Crooked Crown", "Originality", "Lean on purpose, but keep it standing.", (g("offset_min", 30), g("feature_min", 48, "Integrity")), (), "wind", 59, "Daisy declares it a very fashionable bend."),
        ("Ridge Championship", "Integrity", "One last test before the judges return downhill.", (g("tiers_min", 4), g("feature_min", 66, "Integrity")), (), "wind", 60, "The ridge echoes with three tiny cheers."),
    ),
    (
        ("Rainy Day Pies", "Integrity", "Today's mud is wetter. Keep the base trustworthy.", (g("tiers_min", 2), g("feature_min", 70, "Integrity")), (), "rain", 58, "A raindrop rolls off the top like a pearl."),
        ("Flower Rescue", "Decoration", "Save the picnic flowers by arranging them on mud.", (g("kind_min", 10, "petals"), g("colors_min", 3)), (), "rain", 58, "Daisy is relieved her little flowers found shelter."),
        ("Storm Shelter", "Integrity", "Make a broad, squat structure that won't topple.", (g("tiers_max", 2), g("width_min", 255)), (), "rain", 58, "Bruno tries to take shelter beneath your masterpiece."),
        ("Thunder Cake", "Size", "Boulder wants a daring tall tower despite the storm.", (g("tiers_min", 4), g("height_min", 200)), (), "rain", 59, "Nobody knew mud could make such a dramatic silhouette."),
        ("The Dry Mix", "Integrity", "Master the mix: keep the mud carefully balanced.", (g("wetness_max", .73), g("feature_min", 68, "Integrity")), (), "rain", 59, "Fern says your careful mixing saved the day."),
        ("After the Rain", "Originality", "Use everything nature left behind.", (g("kinds_min", 5), g("shapes_min", 3)), (), "rain", 61, "The first sunbeam catches the raindrops on your pie."),
    ),
    (
        ("Lantern Petals", "Decoration", "Make a bright design to match the forest lanterns.", (g("colors_min", 4), g("kind_min", 8, "petals")), (), "night", 59, "Daisy proudly declares yours the prettiest lantern."),
        ("Moon Mirror", "Symmetry", "Build a mirror-image cake beneath the moon.", (g("pair_min", 4), g("feature_min", 75, "Symmetry")), (), "night", 60, "Fern admires the reflection in the pond."),
        ("Stick Constellation", "Originality", "Rotate sticks into constellations among the berries.", (g("kind_min", 6, "sticks"), g("kind_min", 6, "berries")), ("mud", "sticks", "berries"), "night", 59, "Boulder sees a bear-shaped constellation."),
        ("The Little Giant", "Size", "Keep it small in width, enormous in ambition.", (g("tiers_min", 5), g("feature_min", 42, "Integrity")), (), "night", 61, "Bruno is both furious and deeply impressed."),
        ("Many-Colored Woods", "Decoration", "Every color and ingredient should tell a story.", (g("colors_min", 5), g("kinds_min", 5)), (), "night", 61, "Daisy says she could stare at it all night."),
        ("The Forest Gala", "Originality", "The animals are here. Shape petals into something theatrical.", (g("shapes_min", 3), g("top_decos_min", 10), g("shaped_decos_min", 2, "petals")), (), "night", 63, "The entire woodland audience stamps their paws."),
    ),
    (
        ("Finalist's Breakfast", "Symmetry", "Begin the finals with neat and careful work.", (g("pair_min", 5), g("feature_min", 78, "Symmetry")), (), "clear", 63, "Fern announces you belong among the finalists."),
        ("The Hundred Petals", "Decoration", "A tiny floral masterpiece worthy of the cup.", (g("kind_min", 18, "petals"), g("colors_min", 5)), (), "clear", 63, "Petal drops her clipboard in amazement."),
        ("Leaning Wonder", "Integrity", "Engineering meets artistic audacity.", (g("tiers_min", 4), g("offset_min", 42)), (), "wind", 63, "Bruno asks if he can study your design afterward."),
        ("Beyond the Sky", "Size", "Reach for the sky. Mind the weight.", (g("tiers_min", 6), g("height_min", 290)), (), "clear", 64, "Boulder tears up. It's his favorite kind of mountain."),
        ("Sibling Masterpiece", "Originality", "Make a pie that celebrates all three littermates.", (g("kinds_min", 5), g("pair_min", 3)), (), "clear", 64, "Bruno and Daisy promise they'll never forget this one."),
        ("THE GOLDEN MUD CUP", "Originality", "Your final work: ambitious, beautiful and unmistakably yours.", (g("tiers_min", 3), g("kinds_min", 5), g("feature_min", 60, "Integrity")), (), "night", 65, "The judges crown a new champion of mud. The sibling rivalry lives on!"),
    ),
)

SIDE_DATA = (
    (("Beetle's Pebble Hotel", "Symmetry", "Build neat rooms for a very picky beetle.", (g("kind_min", 6, "pebbles"), g("pair_min", 2)), (), "clear", 54),
     ("Mama's Leaf Basket", "Decoration", "A little gift made with leaves and berries.", (g("kind_min", 6, "leaves"), g("kind_min", 4, "berries")), (), "clear", 54)),
    (("Rabbit's Flower Stand", "Decoration", "Make an attractive display for a rabbit friend.", (g("kind_min", 11, "petals"), g("colors_min", 3)), (), "clear", 56),
     ("Picnic Table Parade", "Size", "Create the best centerpiece without going tall.", (g("tiers_max", 2), g("width_min", 250)), (), "clear", 56)),
    (("Mossy Miniature", "Originality", "A tiny ridge village. Shape its stick beams; only sticks and leaves.", (g("kind_min", 5, "sticks"), g("kind_min", 6, "leaves"), g("shaped_decos_min", 2, "sticks")), ("mud", "sticks", "leaves"), "wind", 57),
     ("Badger's Bridge", "Integrity", "A stacked, off-center bridge for a badger.", (g("tiers_min", 3), g("offset_min", 25)), (), "wind", 58)),
    (("Duckling's Umbrella", "Integrity", "A sturdy rain-day sculpture.", (g("tiers_min", 3), g("feature_min", 72, "Integrity")), (), "rain", 58),
     ("Stormy Color Test", "Decoration", "Only leaves and pebbles in wild weather.", (g("kind_min", 6, "pebbles"), g("colors_min", 3)), ("mud", "leaves", "pebbles"), "rain", 58)),
    (("Owl's Moon Dial", "Symmetry", "Build a moon clock with mirrored markings.", (g("pair_min", 4), g("kind_min", 6, "sticks")), (), "night", 61),
     ("Firefly Welcome", "Decoration", "Lights and petals for shy fireflies.", (g("top_decos_min", 9), g("colors_min", 4)), (), "night", 60)),
    (("Auntie's Trophy Stand", "Integrity", "Give the forest's trophy a stable stand.", (g("tiers_min", 4), g("feature_min", 82, "Integrity")), (), "clear", 62),
     ("Secret Sibling Gift", "Originality", "Make a grand surprise for Bruno and Daisy.", (g("kinds_min", 5), g("shapes_min", 3)), (), "night", 64)),
)


# Chapters progressively teach handling, proportion, surface composition and detail.
CAMPAIGN_SKILL_GOALS = {(0, 0): ('workability_min', 1), (0, 1): ('taper_min', 32), (0, 4): ('workability_min', 1), (1, 2): ('zones_min', 4), (1, 3): ('taper_min', 22), (1, 5): ('zones_min', 5), (2, 0): ('taper_min', 20), (2, 3): ('workability_min', 1), (2, 4): ('zones_min', 3), (3, 0): ('workability_min', 1), (3, 2): ('workability_min', 1), (3, 4): ('workability_min', 1), (3, 5): ('zones_min', 5), (4, 0): ('zones_min', 4), (4, 2): ('angle_variants_min', 3), (4, 4): ('zones_min', 5), (5, 1): ('zones_min', 5), (5, 2): ('taper_min', 25), (5, 3): ('taper_min', 25), (5, 4): ('layer_pattern_min', 2), (5, 5): ('workability_min', 2)}

def all_challenges() -> tuple[Challenge, ...]:
    out: list[Challenge] = []
    for ci, rows in enumerate(STORY_DATA):
        for ri, (title, focus, description, goals, allowed, weather, target, story) in enumerate(rows):
            bonus = CAMPAIGN_SKILL_GOALS.get((ci, ri))
            enriched = goals + (g(*bonus),) if bonus else goals
            out.append(Challenge(f"story-{ci + 1:02d}-{ri + 1:02d}", ci, title, description,
                                 focus, enriched, False, tuple(allowed), weather, target, story))
    for ci, rows in enumerate(SIDE_DATA):
        for ri, (title, focus, description, goals, allowed, weather, target) in enumerate(rows):
            out.append(Challenge(f"side-{ci + 1:02d}-{ri + 1:02d}", ci, title, description,
                                 focus, goals, True, tuple(allowed), weather, target,
                                 "The grateful woodland client adds your design to their collection."))
    return tuple(out)


CHALLENGES = all_challenges()
STORY = tuple(c for c in CHALLENGES if not c.side)
SIDES = tuple(c for c in CHALLENGES if c.side)
BY_ID = {c.id: c for c in CHALLENGES}


def initial_campaign() -> dict:
    return {"next_story": 0, "story_medals": {}, "side_medals": {}, "seconds": 0.0,
            "seen_chapters": [], "choices": {}, "chapter_rewards": []}


def normalized_campaign(data: dict | None) -> dict:
    state = initial_campaign()
    if not isinstance(data, dict):
        return state
    try:
        state["next_story"] = max(0, min(len(STORY), int(data.get("next_story", 0))))
        state["seconds"] = max(0., min(10000000., float(data.get("seconds", 0))))
    except (ValueError, TypeError):
        pass
    for key in ("story_medals", "side_medals"):
        if isinstance(data.get(key), dict):
            allowed = STORY if key == "story_medals" else SIDES
            ids = {c.id for c in allowed}
            state[key] = {k: max(1, min(3, int(v))) for k, v in data[key].items()
                          if k in ids and str(v).isdigit()}
    for key in ("seen_chapters", "chapter_rewards"):
        if isinstance(data.get(key), list):
            state[key] = [int(x) for x in data[key] if isinstance(x, int) and 0 <= x < 6][:6]
    if isinstance(data.get("choices"), dict):
        state["choices"] = {str(k): str(v)[:32] for k, v in data["choices"].items()
                            if str(k).isdigit() and int(k) in range(6)}
    return state


def available_story(state: dict) -> Challenge | None:
    index = state["next_story"]
    return STORY[index] if index < len(STORY) else None


def available_side(state: dict, challenge: Challenge) -> bool:
    return challenge.side and challenge.chapter <= min(5, state["next_story"] // 6)


def medals_for(challenge: Challenge, pie: Pie, score: float) -> tuple[int, list[tuple[Goal, float, bool]]]:
    checks = [(goal, *goal_progress(pie, goal, challenge.weather))
              for goal in challenge.goals]
    if not pie.layers:
        return 0, checks
    fulfilled = all(ok for _, _, ok in checks)
    medals = 3 if fulfilled and score >= challenge.target else 2 if fulfilled else 1
    return medals, checks


def record_result(state: dict, challenge: Challenge, medal: int) -> dict:
    state = normalized_campaign(state)
    category = "side_medals" if challenge.side else "story_medals"
    state[category][challenge.id] = max(medal, state[category].get(challenge.id, 0))
    if not challenge.side and medal >= 2:
        index = STORY.index(challenge)
        if index == state["next_story"]:
            state["next_story"] += 1
            if state["next_story"] % 6 == 0 and challenge.chapter not in state["chapter_rewards"]:
                state["chapter_rewards"].append(challenge.chapter)
    return state


def unlocked_colors(state: dict) -> int:
    """Two base tones, unlocking another at each new chapter, up to six."""
    return min(6, 2 + state["next_story"] // 6)


def campaign_statistics(state: dict) -> dict:
    return {"story_done": sum(v >= 2 for v in state["story_medals"].values()),
            "side_done": sum(v >= 2 for v in state["side_medals"].values()),
            "stars": sum(state["story_medals"].values()) + sum(state["side_medals"].values()),
            "possible_stars": len(CHALLENGES) * 3, "chapters": min(6, state["next_story"] // 6)}
