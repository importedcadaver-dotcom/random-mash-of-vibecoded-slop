"""Pure-Python autonomous campaign simulation (NOT a human duration/playtest).

Usage: python tools/simulate_campaign.py
Tests 48 judging sessions and complete persistence progression without pygame.
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mudpie.campaign import STORY, SIDES, initial_campaign, record_result, medals_for
from mudpie.judging import judge
from mudpie.models import Pie, collapse_if_needed
from mudpie.rivals import make_rivals, make_entry, update_relationships
from tools.challenge_bot import design_for


def make_player_pie(index: int) -> Pie:
    """Purposefully varied, valid model pies, not optimized solutions."""
    pie=Pie(title=f'Automated test sculpture {index+1}')
    for k in range(1+index%6):
        pie.add_layer(x=0 if k%3 else 10, width=210-5*k,
                      height=40+index%30, wetness=.4)
    for j in range(5+index%16):
        kinds=('petals','leaves','berries','pebbles','sticks')
        pie.add_deco(kinds[(j+index)%5],j%len(pie.layers),(-.6 if j%2 else .6),.45,
                     color=(j//2)%6)
    return pie


def simulate() -> dict:
    rivals=make_rivals()
    state=initial_campaign()
    previous=None
    wins={'You':0,'Bruno':0,'Daisy':0}
    collapses=0
    medals=0
    for i,challenge in enumerate((*STORY,*SIDES)):
        player=design_for(challenge)
        entries=[player,*[make_entry(r,i+1,7393,previous,challenge.allowed,challenge.weather)
                          for r in rivals]]
        scores={}
        collapsed={}
        for name,pie in zip(('You','Bruno','Daisy'),entries):
            result=judge(pie,challenge.focus,weather=challenge.weather)
            scores[name]=result.total
            collapsed[name]=collapse_if_needed(pie,challenge.weather)[1]
            collapses+=int(collapsed[name])
        wins[max(scores,key=scores.get)]+=1
        medal,checks=medals_for(challenge,player,scores['You'])
        assert medal >= 2, f'Unsolvable mission: {challenge.id}'
        state=record_result(state,challenge,medal)
        update_relationships(rivals,scores,collapsed,i+1)
        previous=player
        medals+=medal
    assert state['next_story']==36
    assert len(state['story_medals'])==36
    assert len(state['side_medals'])==12
    assert sum(wins.values())==48
    return {'story_contests':36,'optional_commissions':12,'stars_in_constructed_goals_run':medals,
            'automated_rounds':48,'wins':wins,'deterministic_collapses':collapses,
            'siblings_memory':{r.name:len(r.memories) for r in rivals},
            'note':'No graphics, crafting input or human play duration measured.'}


if __name__=='__main__':
    import json
    print(json.dumps(simulate(),indent=2))
