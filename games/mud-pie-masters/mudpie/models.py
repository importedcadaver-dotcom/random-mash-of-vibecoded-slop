"""Pure, frame-rate-independent world data for Mud Pie Masters.

Coordinates: layer.x is horizontal offset in table pixels; decorations are attached
in normalized (-1..1) horizontal and (0..1) vertical coordinates to a layer.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

INGREDIENTS = ("mud", "leaves", "petals", "pebbles", "sticks", "berries")
DECORATIONS = INGREDIENTS[1:]
TOOLS = ("Scoop / Mix", "Shape / Flatten", "Stack", "Decorate")
SHAPES = ("round", "oval", "craggy")


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


@dataclass
class MudLayer:
    x: float = 0.0
    width: float = 190.0
    height: float = 49.0
    wetness: float = 0.55
    shape: str = "round"
    damage: float = 0.0
    fallen: bool = False
    # A scoop owns a fixed amount of material. Old saves derive it from geometry.
    volume: float = 0.0
    worked: float = 0.0

    def __post_init__(self) -> None:
        self.width = clamp(float(self.width), 68, 310)
        self.height = clamp(float(self.height), 23, 93)
        self.wetness = clamp(float(self.wetness), 0.0, 1.0)
        self.damage = clamp(float(self.damage), 0.0, 1.0)
        self.worked = clamp(float(self.worked), 0.0, 1.0)
        self.volume = float(self.volume) if self.volume else self.width * self.height
        self.volume = clamp(self.volume, 68 * 23, 310 * 93)
        # Corrupt/outdated dimensions cannot silently manufacture material.
        if abs(self.width * self.height - self.volume) > 0.1:
            self.width = clamp(self.volume / self.height, 68, 310)
            self.height = self.volume / self.width
        if self.shape not in SHAPES:
            self.shape = "round"

    @property
    def mass(self) -> float:
        return self.volume * (0.75 + 0.35 * self.wetness) / 3000

    @property
    def workable(self) -> bool:
        return 0.42 <= self.wetness <= 0.73 and self.worked >= 0.3

    def reshape(self, width: float) -> None:
        """Spread or compress the same scoop; width times height stays invariant."""
        low = max(68., self.volume / 93.)
        high = min(310., self.volume / 23.)
        self.width = clamp(float(width), low, high)
        self.height = self.volume / self.width

    def mix(self, distance: float, starting_wetness: float | None = None,
            starting_worked: float | None = None) -> None:
        """Moderate stirring improves cohesion; overworking causes wetness risk."""
        start_w = self.wetness if starting_wetness is None else starting_wetness
        start_k = self.worked if starting_worked is None else starting_worked
        travel = max(0., float(distance))
        self.wetness = clamp(start_w + travel * .00055, 0, .98)
        self.worked = clamp(start_k + travel / 410., 0, 1)


@dataclass
class Decoration:
    kind: str
    layer: int
    x: float
    y: float
    angle: float = 0.0
    color: int = 0
    # Shape/flatten gestures on petals and sticks are persistent and reversible.
    # Defaults preserve appearance of existing saves without these fields.
    stretch_x: float = 1.0
    stretch_y: float = 1.0

    def __post_init__(self) -> None:
        if self.kind not in DECORATIONS:
            raise ValueError(f"Invalid decoration: {self.kind}")
        self.x = clamp(float(self.x), -1.05, 1.05)
        self.y = clamp(float(self.y), 0.0, 1.0)
        self.angle = float(self.angle) % 360
        self.color = int(self.color) % 6
        self.stretch_x = clamp(float(self.stretch_x), .5, 2.3)
        self.stretch_y = clamp(float(self.stretch_y), .5, 2.3)


@dataclass
class Pie:
    layers: list[MudLayer] = field(default_factory=list)
    decorations: list[Decoration] = field(default_factory=list)
    moves: int = 0
    title: str = "A very serious mud pie"
    signature: str = ""

    def add_layer(self, x: float = 0, width: float = 190, height: float = 49,
                  wetness: float = 0.55, shape: str = "round") -> MudLayer:
        if len(self.layers) >= 7:
            raise ValueError("Maximum seven tiers. The forest has limits!")
        layer = MudLayer(x=x, width=width, height=height, wetness=wetness, shape=shape)
        # Fallen clumps live at the end of the array as table debris. Insert
        # new scoops BEFORE debris so a player can rebuild on a standing base.
        first_debris = next((i for i,l in enumerate(self.layers) if l.fallen),len(self.layers))
        self.layers.insert(first_debris,layer)
        for deco in self.decorations:
            if deco.layer >= first_debris:
                deco.layer += 1
        self.moves += 1
        return layer

    def settle_unsupported(self) -> list[int]:
        """Drop upper tiers with no physical center-of-mass support.

        A tier is not supported merely because two edges happen to overlap:
        its center must project over the supporting layer. Cascades are
        deterministic, persistent and reversible through normal Pie snapshots.
        This checks placement, not the separate weather/judging collapse score.
        """
        dropped = []
        for i,layer in enumerate(self.layers):
            if layer.fallen or i == 0:
                continue
            below = self.layers[i-1]
            if below.fallen or abs(layer.x-below.x) > below.width / 2:
                layer.fallen = True
                layer.damage = max(layer.damage,.68)
                dropped.append(i)
        return dropped

    def add_deco(self, kind: str, layer: int, x: float, y: float,
                 angle: float = 0, color: int = 0) -> Decoration:
        if not 0 <= layer < len(self.layers):
            raise ValueError("Place decorations on an existing mud tier")
        if len(self.decorations) >= 120:
            raise ValueError("The table has reached its decoration limit")
        deco = Decoration(kind, layer, x, y, angle, color)
        self.decorations.append(deco)
        self.moves += 1
        return deco

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Pie":
        if not isinstance(data, dict):
            raise ValueError("Invalid pie data")
        layers = [MudLayer(**item) for item in data.get("layers", [])[:7]]
        decorations = []
        for item in data.get("decorations", [])[:120]:
            try:
                d = Decoration(**item)
                if 0 <= d.layer < len(layers):
                    decorations.append(d)
            except (TypeError, ValueError):
                continue
        return cls(layers=layers, decorations=decorations,
                   moves=int(data.get("moves", 0)),
                   title=str(data.get("title", "A very serious mud pie"))[:100],
                   signature=str(data.get("signature", ""))[:100])

    def copy(self) -> "Pie":
        return Pie.from_dict(self.to_dict())

    @property
    def height(self) -> float:
        return sum(layer.height for layer in self.layers if not layer.fallen)

    @property
    def footprint(self) -> float:
        if not self.layers:
            return 0.0
        return max(l.width for l in self.layers if not l.fallen) if any(not l.fallen for l in self.layers) else 0.0

    def tier_bounds(self, base_x: float, base_y: float) -> list[tuple[float, float, float, float]]:
        """AABB for each standing tier (left, top, width, height)."""
        total = 0.0
        bounds = []
        for layer in self.layers:
            if layer.fallen:
                bounds.append((base_x + layer.x, base_y, 0, 0))
                continue
            total += layer.height
            bounds.append((base_x + layer.x - layer.width / 2,
                           base_y - total, layer.width, layer.height))
        return bounds


@dataclass
class Stability:
    score: float
    risk: str
    weak_layer: int | None
    notes: list[str]


def evaluate_stability(pie: Pie, weather: str = "clear") -> Stability:
    """Support-overlap and top-mass model. No random failures."""
    if not pie.layers:
        return Stability(0, "empty", None, ["No mud yet."])
    worst = 100.0
    weak = None
    notes = []
    for i, layer in enumerate(pie.layers):
        if layer.fallen:
            worst = min(worst, 8)
            weak = i
            notes.append(f"Tier {i + 1} has fallen.")
            continue
        score = 91.0 + 8 * layer.worked - layer.damage * 64
        # Wet enough to bind, but soupy mud slumps and dry mud cracks.
        score -= max(0, .36 - layer.wetness) * 37
        score -= max(0, layer.wetness - 0.72) * 105
        if i:
            below = pie.layers[i - 1]
            if below.fallen:
                score = min(score, 4)
            else:
                delta = abs(layer.x - below.x)
                overlap = max(0, (layer.width + below.width) / 2 - delta)
                support_fraction = clamp(overlap / max(layer.width, 1), 0, 1)
                score -= (1 - support_fraction) * 116
                # Narrow supporting tier with an oversized tier above.
                ratio = layer.width / max(below.width, 1)
                score -= max(0, ratio - 1.1) * 24
                # An increasingly tall structure is more vulnerable.
                score -= max(0, i - 1) * 4
                score -= max(0, below.wetness - 0.7) * i * 21
        deco_mass = sum({"pebbles": 1.7, "sticks": 1.0, "berries": .5,
                         "leaves": .1, "petals": .05}.get(d.kind, 0)
                        for d in pie.decorations if d.layer == i)
        score -= max(0, deco_mass - 10) * .8
        if score < worst:
            worst = score
            weak = i
    if weather == "wind":
        # Public, deterministic weather rule: tall and off-center shapes sway.
        extra = max(0., pie.height - 150) * .09
        extra += max((abs(l.x) for l in pie.layers), default=0) * .13
        worst -= extra
        if extra > 1:
            notes.append(f"Ridge wind reduces stability by {extra:.0f} points.")
    worst = clamp(worst, 0, 100)
    risk = "stable" if worst >= 58 else "wobbly" if worst >= 32 else "critical"
    if risk == "wobbly":
        notes.append(f"Tier {weak + 1} is leaning; try centering or flattening it.")
    elif risk == "critical":
        notes.append(f"Tier {weak + 1} has too little support!")
    else:
        notes.append("This creation should stand through judging.")
    return Stability(round(worst, 2), risk, weak, notes)


def collapse_if_needed(pie: Pie, weather: str = "clear") -> tuple[Pie, bool]:
    """Deterministic presentation failure; damages only unsupported upper tiers."""
    out = pie.copy()
    state = evaluate_stability(out, weather=weather)
    if state.score >= 32 or state.weak_layer is None:
        return out, False
    for layer in out.layers[state.weak_layer:]:
        layer.fallen = True
        layer.damage = max(layer.damage, 0.68)
    return out, True


def deco_color(kind: str) -> tuple[int, int, int]:
    return {"leaves": (77, 119, 54), "petals": (228, 126, 137),
            "pebbles": (141, 146, 140), "sticks": (117, 81, 54),
            "berries": (151, 54, 86)}[kind]
