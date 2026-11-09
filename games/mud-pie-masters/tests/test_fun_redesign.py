"""Adversarial game-design regression tests for the v0.5 mechanics."""
from math import isclose

import pytest

from mudpie.campaign import CHALLENGES, Goal, goal_progress
from mudpie.judging import effective_weights, feature_scores, fingerprint, judge
from mudpie.models import MudLayer, Pie, evaluate_stability
from mudpie.rivals import make_entry, make_rivals, respond_to_player, update_relationships
from tools.strategy_bots import architect, florist, precision, generic
from tools.stress_test import run


def test_shaping_preserves_the_actual_material_amount():
    layer = MudLayer(width=190, height=46, wetness=.51)
    original_volume = layer.volume
    layer.reshape(270)
    assert layer.width == 270
    assert layer.height < 46
    assert isclose(layer.width * layer.height, original_volume, abs_tol=1e-7)
    layer.reshape(90)
    assert layer.height > 46
    assert isclose(layer.width * layer.height, original_volume, abs_tol=1e-7)


def test_shaping_obeys_physical_bounds_without_new_mud():
    layer = MudLayer(width=190, height=46)
    layer.reshape(10000)
    assert layer.width <= 310
    assert layer.height >= 23
    assert isclose(layer.width * layer.height, layer.volume, abs_tol=.001)
    layer.reshape(-10000)
    assert layer.width >= 68
    assert layer.height <= 93
    assert isclose(layer.width * layer.height, layer.volume, abs_tol=.001)


def test_scoop_and_geometry_survive_copy_and_save():
    pie = Pie()
    layer = pie.add_layer()
    layer.mix(205)
    layer.reshape(242)
    clone = Pie.from_dict(pie.to_dict())
    assert clone.to_dict() == pie.to_dict()
    assert clone.layers[0].workable
    assert isclose(clone.layers[0].volume, 190*49)


def test_old_saves_without_volume_get_a_derived_scoop_amount():
    old = Pie.from_dict({'layers': [{'width': 170, 'height': 47, 'wetness': .5}]})
    assert old.layers[0].volume == 170 * 47
    assert old.layers[0].worked == 0


def test_stirring_helps_but_oversaturation_hurts():
    pie = Pie()
    layer = pie.add_layer(wetness=.42)
    initial = evaluate_stability(pie).score
    layer.mix(195)
    assert layer.workable
    worked = evaluate_stability(pie).score
    assert worked > initial
    layer.mix(960)
    assert layer.wetness > .73
    assert evaluate_stability(pie).score < worked


def test_empty_centered_pie_does_not_win_symmetry():
    pie = Pie(); pie.add_layer()
    assert feature_scores(pie)['Symmetry'] <= 40


def test_actual_mirrored_pattern_is_rewarded():
    a = Pie(); a.add_layer()
    b = a.copy()
    for i in range(6):
        a.add_deco('petals', 0, .35 + i*.07, .2 + i*.1)
        a.add_deco('petals', 0, -(.35 + i*.07), .2 + i*.1)
        b.add_deco('petals', 0, .35 + i*.07, .2 + i*.1)
        b.add_deco('petals', 0, .50 + i*.06, .2 + i*.1)
    assert feature_scores(a)['Symmetry'] > feature_scores(b)['Symmetry'] + 30


def test_visual_rotation_changes_real_aesthetic_scoring():
    pie = Pie(); pie.add_layer()
    for i in range(8):
        pie.add_deco('sticks',0,-.75+i*.21,.2+(.3 if i%2 else 0))
    rotated = pie.copy()
    for i,d in enumerate(rotated.decorations):
        d.angle = i * 45
    assert feature_scores(rotated)['Originality'] > feature_scores(pie)['Originality']
    assert fingerprint(rotated) != fingerprint(pie)


def test_actual_decorative_spread_beats_singular_pile():
    pile = Pie(); pile.add_layer()
    spread = Pie(); spread.add_layer()
    for i in range(25):
        kind = ('petals','pebbles','leaves','berries','sticks')[i%5]
        pile.add_deco(kind,0,0,.5)
        spread.add_deco(kind,0,(-.9,-.3,.3,.9)[i%4],(.15,.45,.75)[(i//4)%3])
    assert feature_scores(spread)['Decoration'] > feature_scores(pile)['Decoration']+12


def test_theme_priorities_are_public_and_substantial():
    base = (.07, .17, .49, .08, .19)
    weights = effective_weights(base,'Size')
    assert isclose(sum(weights.values()),1)
    assert weights['Size'] >= .65
    assert weights['Symmetry'] > 0


def test_repeated_recipe_receives_visible_competition_penalty():
    pie = precision()
    recent = [fingerprint(pie)]*3
    first = judge(pie,'Symmetry')
    repeated = judge(pie,'Symmetry',recent)
    assert first.total - repeated.total >= 35
    assert any('Repeat recipe' in v.comment for v in repeated.verdicts)


def test_sibling_cheering_builds_affection_and_confidence():
    rival = make_rivals()[0]
    before = make_entry(rival,8,7393)
    msg = respond_to_player(rival,'cheer')
    after = make_entry(rival,8,7393)
    assert 'Bruno' in msg and rival.affection>55 and rival.confidence>50
    assert before.to_dict()!=after.to_dict()


def test_daring_an_older_brother_increases_rivalry_and_risk():
    rival = make_rivals()[0]
    prior = (rival.rivalry,rival.affection)
    before = make_entry(rival,8,7393)
    respond_to_player(rival,'dare')
    after = make_entry(rival,8,7393)
    assert before.to_dict() != after.to_dict()
    assert rival.rivalry>prior[0] and rival.affection<prior[1]
    scores={'You':80.,'Bruno':52.,'Daisy':61.}
    update_relationships([rival],scores,{'Bruno':True},2)
    assert rival.embarrassment==1
    assert rival.affection<prior[1]
    assert rival.confidence<55


def test_player_cannot_max_affection_just_by_beating_everyone():
    rival=make_rivals()[1]
    for i in range(10):
        update_relationships([rival],{'You':90.,'Daisy':35.}, {'Daisy':False},i+1)
    assert rival.affection<=55
    assert rival.rivalry>20


def test_new_campaign_skills_are_different_types_of_mastery():
    goals = {g.rule for c in CHALLENGES for g in c.goals}
    assert {'taper_min','zones_min','workability_min','angle_variants_min',
            'layer_pattern_min'}.issubset(goals)
    assert sum(len(c.goals)==3 for c in CHALLENGES)>=20


def test_workability_goal_requires_real_kneading():
    pie = Pie(); layer = pie.add_layer(wetness=.44)
    goal = Goal('workability_min',1)
    assert not goal_progress(pie,goal)[1]
    layer.mix(170)
    assert goal_progress(pie,goal)[1]


def test_all_three_strategy_archetypes_can_win_and_lose():
    metrics=run()
    for name in ('architect','florist','precision'):
        assert 1 <= metrics['scoring_wins_without_legal_mission_check'][name] < 48
    scores=metrics['strategy_focus_scores']
    assert scores['architect']['Size']>scores['florist']['Size']
    assert scores['florist']['Decoration']>scores['architect']['Decoration']
    assert scores['precision']['Symmetry']>scores['florist']['Symmetry']


def test_unchanged_template_does_not_dominate_campaign_or_rivals():
    metrics=run()
    assert metrics['unchanged_template_goal_completions']<=12
    assert metrics['scoring_wins_without_legal_mission_check']['unchanged_template']<=28
