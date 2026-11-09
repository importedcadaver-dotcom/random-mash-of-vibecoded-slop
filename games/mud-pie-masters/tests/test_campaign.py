"""Campaign progression, objectives, fair rules, and backwards save compatibility."""
from __future__ import annotations
import json
import pytest
from mudpie.campaign import (
    BY_ID, CHALLENGES, CHAPTERS, SIDES, STORY, Goal, available_side,
    available_story, campaign_statistics, goal_progress, initial_campaign,
    medals_for, normalized_campaign, paired_decorations, record_result,
    unlocked_colors,
)
from mudpie.judging import judge
from mudpie.models import Pie, evaluate_stability
from mudpie.rivals import make_entry, make_rivals
from mudpie.save import load_game, save_game
from tools.challenge_bot import design_for


def test_scope_is_36_stories_12_side_quests_six_distinct_chapters():
    assert len(STORY) == 36
    assert len(SIDES) == 12
    assert len(CHAPTERS) == 6
    assert len(CHALLENGES) == 48
    assert len(BY_ID) == 48
    assert len({c.title for c in CHALLENGES}) == 48
    assert all(len(c.goals)>=2 for c in CHALLENGES)
    assert {c.focus for c in CHALLENGES} == {'Size','Decoration','Symmetry','Originality','Integrity'}
    assert {c.weather for c in CHALLENGES} == {'clear','rain','wind','night'}


@pytest.mark.parametrize('challenge',CHALLENGES,ids=lambda c:c.id)
def test_every_goal_can_be_satisfied_in_an_actual_pie(challenge):
    pie=design_for(challenge)
    assert pie.layers
    assert set(d.kind for d in pie.decorations).issubset(set(challenge.allowed or ('leaves','petals','pebbles','sticks','berries')))
    for g in challenge.goals:
        actual,met=goal_progress(pie,g,challenge.weather)
        assert met, f'{challenge.id}: {g.label} = {actual}'
    medal,_=medals_for(challenge,pie,0)
    assert medal>=2


def test_campaign_advances_when_all_objectives_met_even_if_score_is_low():
    state=initial_campaign()
    for challenge in STORY:
        assert available_story(state)==challenge
        state=record_result(state,challenge,2)
    assert state['next_story']==36
    assert available_story(state) is None
    assert len(state['story_medals'])==36
    assert len(state['chapter_rewards'])==6
    assert all(x in state['chapter_rewards'] for x in range(6))


def test_replay_never_revokes_stars_or_advances_story():
    state=initial_campaign()
    first=STORY[0]
    state=record_result(state,first,3)
    state=record_result(state,first,1)
    assert state['story_medals'][first.id]==3
    assert state['next_story']==1


def test_side_commissions_unlock_by_chapter_and_do_not_advance_story():
    state=initial_campaign()
    assert available_side(state,SIDES[0])
    assert not available_side(state,SIDES[2])
    state=record_result(state,SIDES[0],2)
    assert state['next_story']==0
    for c in STORY[:6]:
        state=record_result(state,c,2)
    assert available_side(state,SIDES[2])
    assert not available_side(state,SIDES[4])


def test_palette_unlocks_in_steps_and_ends_at_six():
    state=initial_campaign()
    assert unlocked_colors(state)==2
    for i,challenge in enumerate(STORY):
        state=record_result(state,challenge,2)
        if (i+1)%6==0:
            assert unlocked_colors(state)==min(6,2+(i+1)//6)


def test_mirrored_pair_requires_same_kind_color_tier():
    p=Pie()
    p.add_layer()
    p.add_deco('petals',0,.5,.4,color=1)
    p.add_deco('petals',0,-.5,.4,color=1)
    p.add_deco('petals',0,.5,.4,color=2)
    assert paired_decorations(p)==1


def test_wind_penalty_is_deterministic_and_meaningful():
    p=Pie()
    for i in range(5):p.add_layer(0,200,70,.55)
    clear=evaluate_stability(p).score
    windy=evaluate_stability(p,weather='wind').score
    assert 0<windy<clear
    assert judge(p,'Integrity',weather='wind').features['Integrity']==windy


def test_rivals_respect_restricted_ingredients_and_rain():
    bruno,daisy=make_rivals()
    for rival in (bruno,daisy):
        pie=make_entry(rival,13,7393,allowed=('mud','leaves'),weather='rain')
        assert pie.layers
        assert set(d.kind for d in pie.decorations)=={'leaves'}
        assert all(l.wetness >= .35 for l in pie.layers)


def test_backward_compatible_campaign_load(tmp_path):
    path=tmp_path/'old.json'
    data={'version':1,'round':4,'gallery':[], 'history':[],
          'rivals':[r.__dict__ for r in make_rivals()], 'settings':{}}
    path.write_text(json.dumps(data),encoding='utf-8')
    result=load_game(path)
    assert result['round']==4
    assert result['campaign']==initial_campaign()


def test_campaign_state_roundtrip(tmp_path):
    state=initial_campaign()
    state=record_result(state,STORY[0],3)
    state=record_result(state,SIDES[0],2)
    state['choices']={'1':'encourage'}
    state['seconds']=754.3
    path=tmp_path/'save.json'
    loaded=load_game(path)
    save_game(3,make_rivals(),[],[],loaded['settings'],path=path,campaign=state)
    loaded=load_game(path)
    assert loaded['campaign']==state
    assert loaded['campaign']['story_medals'][STORY[0].id]==3


def test_corrupt_campaign_state_is_bounded():
    state=normalized_campaign({'next_story':999999, 'seconds':-55,
                               'story_medals':{'junk':999,STORY[0].id:99},
                               'seen_chapters':[0,99,-4],
                               'choices':{'0':'encourage','99':'oh no'}})
    assert state['next_story']==36
    assert state['seconds']==0
    assert state['story_medals']=={STORY[0].id:3}
    assert state['seen_chapters']==[0]
    assert state['choices']=={'0':'encourage'}


def test_campaign_statistics_are_bounded_and_additive():
    state=initial_campaign()
    state=record_result(state,STORY[0],3)
    state=record_result(state,SIDES[0],2)
    result=campaign_statistics(state)
    assert result['stars']==5
    assert result['possible_stars']==144
    assert result['story_done']==1
    assert result['side_done']==1


def test_incomplete_contest_is_replayable_but_cannot_be_skipped():
    state=initial_campaign()
    state=record_result(state,STORY[0],1)
    assert available_story(state)==STORY[0]
    assert campaign_statistics(state)['story_done']==0
    assert state['story_medals'][STORY[0].id]==1
    state=record_result(state,STORY[0],2)
    assert available_story(state)==STORY[1]
    assert campaign_statistics(state)['story_done']==1
