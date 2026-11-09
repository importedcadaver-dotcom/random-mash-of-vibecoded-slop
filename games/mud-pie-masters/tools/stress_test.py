"""Repeatable v0.5 balancing metrics. Not a human playtest or win guarantee."""
from __future__ import annotations
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mudpie.campaign import CHALLENGES, goal_progress
from mudpie.judging import judge, fingerprint
from mudpie.rivals import make_entry, make_rivals
from tools.strategy_bots import architect, florist, precision, generic


def run() -> dict:
    bots = {'architect': architect(), 'florist': florist(),
            'precision': precision(), 'unchanged_template': generic()}
    possible = []
    for challenge in CHALLENGES:
        p = bots['unchanged_template']
        available = set(challenge.allowed or ('leaves', 'petals', 'pebbles', 'sticks', 'berries'))
        if (set(d.kind for d in p.decorations).issubset(available)
                and all(goal_progress(p, g, challenge.weather)[1] for g in challenge.goals)):
            possible.append(challenge.id)
    repeat_history = []
    wins = {name: 0 for name in bots}
    for i, challenge in enumerate(CHALLENGES):
        rivals = make_rivals()
        competitor_best = max(judge(make_entry(r, i + 1, 7393,
                               allowed=challenge.allowed, weather=challenge.weather),
                               challenge.focus, weather=challenge.weather).total
                              for r in rivals)
        for name, pie in bots.items():
            recent = repeat_history if name == 'unchanged_template' else []
            if judge(pie, challenge.focus, recent,
                     weather=challenge.weather).total >= competitor_best:
                wins[name] += 1
        repeat_history.append(fingerprint(bots['unchanged_template']))
    return {
        'total_contests': len(CHALLENGES),
        'unchanged_template_goal_completions': len(possible),
        'unchanged_template_goal_completions_ids': possible,
        'scoring_wins_without_legal_mission_check': wins,
        'strategy_focus_scores': {name: {focus: judge(pie, focus).total
                                for focus in ('Size', 'Decoration', 'Symmetry')}
                                for name, pie in bots.items()},
        'caution': ('Data-model comparisons only. No mouse interaction, graphical rendering, '
                    'realistic human strategy, subjective fun, or duration measured.')
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
