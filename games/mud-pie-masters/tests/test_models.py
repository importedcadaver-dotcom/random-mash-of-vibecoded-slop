import json
import pytest
from mudpie.models import Pie, collapse_if_needed, evaluate_stability


def test_six_ingredients_are_real():
    from mudpie.models import INGREDIENTS, DECORATIONS, TOOLS
    assert INGREDIENTS == ('mud','leaves','petals','pebbles','sticks','berries')
    assert set(DECORATIONS) == set(INGREDIENTS)-{'mud'}
    assert len(TOOLS)==4


def test_create_edit_stack_and_decorate():
    pie=Pie()
    lower=pie.add_layer(0,220,58,.51)
    upper=pie.add_layer(2,165,44,.48)
    for item in ('leaves','petals','pebbles','sticks','berries'):
        pie.add_deco(item,1,.18,.55,angle=30)
    assert len(pie.layers)==2 and len(pie.decorations)==5
    assert pie.height==102
    assert pie.footprint==220
    assert lower.mass>upper.mass


def test_save_roundtrip_normalizes_structural_data():
    pie=Pie()
    pie.add_layer(-8,250,81,.56,shape='craggy')
    pie.add_layer(10,165,40,.42,shape='oval')
    pie.add_deco('berries',1,-.48,.58,45,3)
    pie.add_deco('petals',0,.31,.8,315,1)
    out=Pie.from_dict(json.loads(json.dumps(pie.to_dict())))
    assert out.to_dict()==pie.to_dict()


def test_invalid_decoration_is_blocked():
    pie=Pie()
    with pytest.raises(ValueError):pie.add_deco('waffles',0,0,0)
    with pytest.raises(ValueError):pie.add_deco('berries',0,0,0)
    pie.add_layer()
    with pytest.raises(ValueError):pie.add_deco('berries',11,0,0)


def test_clamps_and_max_seven_tiers():
    pie=Pie()
    for _ in range(7):pie.add_layer(0,10,400,2)
    assert all(l.width>=68 and l.height<=93 and l.wetness<=1 for l in pie.layers)
    with pytest.raises(ValueError):pie.add_layer()


def test_bad_support_more_unstable():
    balanced=Pie()
    balanced.add_layer(0,240,60,.44)
    balanced.add_layer(0,155,42,.44)
    offset=balanced.copy()
    offset.layers[1].x=155
    assert evaluate_stability(balanced).score>evaluate_stability(offset).score
    assert evaluate_stability(offset).risk=='critical'


def test_overwet_cake_worse_than_dry():
    pie=Pie();pie.add_layer(0,200,60,.45);pie.add_layer(0,150,55,.42)
    worse=pie.copy();worse.layers[0].wetness=.99;worse.layers[1].wetness=.99
    assert evaluate_stability(pie).score>evaluate_stability(worse).score


def test_collapse_is_deterministic_and_keeps_lower_tier():
    pie=Pie();pie.add_layer(0,270,55,.45);pie.add_layer(175,190,65,.6);pie.add_layer(175,100,40,.5)
    displayed,fallen=collapse_if_needed(pie)
    assert fallen is True
    assert not displayed.layers[0].fallen
    assert any(l.fallen for l in displayed.layers[1:])
    assert not any(l.fallen for l in pie.layers)  # original preserved
    assert displayed.to_dict()==collapse_if_needed(pie)[0].to_dict()


def test_stable_pie_doesnt_collapse():
    pie=Pie();pie.add_layer(0,200,50,.52);pie.add_layer(0,150,39,.43)
    _,fall=collapse_if_needed(pie)
    assert fall is False


def test_malformed_old_decorations_are_discarded():
    obj={'layers':[{'width':200,'height':40}],
         'decorations':[{'kind':'unicorn','layer':0,'x':0,'y':0},
                        {'kind':'petals','layer':999,'x':0,'y':0}]}
    assert len(Pie.from_dict(obj).decorations)==0


def test_tier_bounds_stay_consistent():
    pie=Pie();pie.add_layer(0,240,60);pie.add_layer(15,160,42)
    bounds=pie.tier_bounds(660,580)
    assert bounds[0]==(540,520,240,60)
    assert bounds[1]==(595,478,160,42)
