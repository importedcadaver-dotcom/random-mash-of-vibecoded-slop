"""Two siblings compete using exactly the same pie data and judges as the player."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
from random import Random
from .models import Pie
from .judging import fingerprint


@dataclass
class Rival:
    name: str
    personality: str
    affection: int = 55
    victories: int = 0
    defeats: int = 0
    embarrassment: int = 0
    memories: list[str] = field(default_factory=list)
    last_signature: str = ""
    confidence: int = 50
    rivalry: int = 20
    last_interaction: str = ""

    def remember(self, event: str) -> None:
        self.memories.append(event)
        self.memories = self.memories[-7:]


RIVALS = (
    Rival("Bruno", "Your bold, competitive older brother"),
    Rival("Daisy", "Your playful, imaginative little sister"),
)


def make_rivals() -> list[Rival]:
    return [Rival(**asdict(r)) for r in RIVALS]


def respond_to_player(rival: Rival, action: str) -> str:
    """Two honest trade-offs: encourage a stronger ally or provoke ambition."""
    if action == 'cheer':
        rival.affection = min(100, rival.affection + 7)
        rival.confidence = min(100, rival.confidence + 12)
        rival.rivalry = max(0, rival.rivalry - 8)
        msg = (f'{rival.name} beams at your encouragement. Their next entry will be steadier!'
               if rival.name == 'Bruno' else
               'Daisy smiles shyly and plans an extra-careful flower arrangement.')
    elif action == 'dare':
        rival.affection = max(0, rival.affection - 6)
        rival.confidence = min(100, rival.confidence + 5)
        rival.rivalry = min(100, rival.rivalry + 19)
        msg = ("Bruno vows to make an even taller tower. This might go badly!"
               if rival.name == 'Bruno' else
               'Daisy huffs. She wants to prove she has ideas of her own.')
    else:
        raise ValueError('Unknown sibling interaction')
    rival.last_interaction = action
    rival.remember(msg)
    return msg


def make_entry(rival: Rival, round_number: int, seed: int,
               player_previous: Pie | None = None, allowed: tuple[str, ...] = (),
               weather: str = "clear") -> Pie:
    """Reproducible character-led pie generator, not precomputed scores."""
    rng = Random(seed * 67 + round_number * 4099 + sum(map(ord, rival.name)))
    pie = Pie(title=f"{rival.name}'s muddy marvel")
    is_bruno = rival.name == "Bruno"
    count = rng.choice((2, 3, 3, 4)) if is_bruno else rng.choice((1, 2, 2, 3))
    if is_bruno and (rival.defeats > rival.victories or rival.rivalry >= 36) and rng.random() < .46:
        count = min(5, count + 1)  # Competitive escalation with consequences
    for i in range(count):
        if is_bruno:
            width = rng.randint(170, 265) - i * rng.randint(4, 18)
            height = rng.randint(56, 85)
            x = rng.randint(-15, 15) + i * rng.randint(-24, 27)
            if rival.confidence >= 62 and rival.rivalry < 36:
                x *= .48  # Cheer gives Bruno the patience to build stable foundations.
            elif rival.rivalry >= 36:
                x *= 1.0 + min(.65, rival.rivalry / 120)
                height = min(93, height + 7)
            wetness = rng.uniform(.35, .72 if rival.confidence >= 62 else .85) + (.14 if weather == "rain" else 0)
        else:
            width = rng.randint(145, 240) - i * rng.randint(12, 27)
            height = rng.randint(33, 60)
            x = rng.randint(-10, 10) * (1.6 if rival.rivalry >= 36 else .7)
            wetness = rng.uniform(.37, .65) + (.14 if weather == "rain" else 0)
        tier = pie.add_layer(x, width, height, wetness,
                      shape=rng.choice(("round", "oval", "craggy")))
        # Confident cubs remember to knead the bottom tiers, not magic bonuses.
        if rival.confidence >= 62 and tier.wetness < .71:
            tier.worked = .42
    if player_previous and rival.name == "Daisy" and rng.random() < (.55 if rival.affection>=65 else .3):
        kinds = list({d.kind for d in player_previous.decorations}) or ["petals"]
        rival.remember("I borrowed a decoration idea from your last pie!")
    else:
        kinds = (["sticks", "pebbles", "leaves", "berries"] if is_bruno else
                 ["petals", "leaves", "berries", "pebbles", "sticks"])
    if allowed:
        kinds = [kind for kind in kinds if kind in allowed]
        if not kinds:
            kinds = [kind for kind in allowed if kind != 'mud']
    if not kinds:
        kinds = ['leaves']
    amount = rng.randint(6, 13) if is_bruno else rng.randint(9, 21)
    if not is_bruno and rival.confidence >= 62:
        amount += 4
    for _ in range(amount):
        layer_index = rng.randrange(len(pie.layers))
        kind = rng.choice(kinds if is_bruno or (allowed and "petals" not in allowed) else kinds + ["petals", "petals"])
        x = rng.uniform(-.80, .80)
        y = rng.uniform(.12, .78)
        if not is_bruno and rng.random() < (.28 if rival.rivalry >= 36 else .74 if rival.confidence >= 62 else .4):
            # Daisy likes petal pairing and patterns.
            pie.add_deco(kind, layer_index, x, y, rng.randrange(0, 360, 30))
            pie.add_deco(kind, layer_index, -x, y, rng.randrange(0, 360, 30))
        else:
            pie.add_deco(kind, layer_index, x, y, rng.randrange(0, 360, 30))
    pie.signature = fingerprint(pie)
    rival.last_signature = pie.signature
    return pie


def update_relationships(rivals: list[Rival], scores: dict[str, float],
                         collapsed: dict[str, bool], round_number: int) -> list[str]:
    """Results alter confidence and rivalries, not unconditional affection gains."""
    messages = []
    max_score = max(scores.values())
    for rival in rivals:
        won = scores[rival.name] >= max_score
        lost_to_player = scores['You'] > scores[rival.name]
        if won:
            rival.victories += 1
            rival.confidence = min(100, rival.confidence + 7)
            rival.rivalry = max(0, rival.rivalry - 3)
            text = f'{rival.name} grins at the first-place ribbon and promises to try a new design.'
        else:
            rival.defeats += 1
            rival.confidence = max(5, rival.confidence - (6 if lost_to_player else 3))
            if lost_to_player:
                rival.rivalry = min(100, rival.rivalry + 4)
                if rival.last_interaction == 'dare' or rival.rivalry >= 45:
                    rival.affection = max(0, rival.affection - 4)
                    text = f'{rival.name} is prickly after your win and takes the challenge personally.'
                else:
                    text = f'{rival.name} studies your pie and wonders how to catch up.'
            else:
                text = f'{rival.name} is disappointed, but cheers for the winner.'
        if collapsed.get(rival.name):
            rival.embarrassment += 1
            rival.confidence = max(5, rival.confidence - 8)
            rival.affection = max(0, rival.affection - (3 if rival.last_interaction == 'dare' else 1))
            text = f"{rival.name}'s tower collapses! They blush and remember who challenged them."
        rival.last_interaction = ''
        rival.remember(text)
        messages.append(text)
    return messages
