from mudpie.judging import FEATURES,THEMES,JUDGES, feature_scores, fingerprint, judge
from mudpie.models import Pie


def sample():
    pie=Pie();pie.add_layer(0,220,48,.45);pie.add_layer(0,160,43,.49)
    for i in range(5):
        pie.add_deco('petals',1,.12*i,.45)
        pie.add_deco('leaves',1,-.12*i,.45)
    return pie


def test_reproducible_scores():
    pie=sample()
    assert judge(pie,'Decoration')==judge(pie,'Decoration')


def test_three_judges_give_distinct_opinions():
    verdicts=judge(sample(),'Decoration').verdicts
    assert len(verdicts)==3
    assert len(set(v.score for v in verdicts))>=2
    assert {v.name for v in verdicts}=={'Petal','Boulder','Fern'}


def test_bigger_mud_pie_gets_higher_size_feature():
    small=Pie();small.add_layer(0,90,24)
    huge=Pie();huge.add_layer(0,280,85);huge.add_layer(0,260,85)
    assert feature_scores(huge)['Size']>feature_scores(small)['Size']


def test_symmetric_pattern_beats_unbalanced():
    balanced=Pie();balanced.add_layer()
    for x in (-.8,-.4,.4,.8):balanced.add_deco('petals',0,x,.5)
    messy=balanced.copy()
    for i,d in enumerate(messy.decorations):
        d.x=.2+i*.15
    assert feature_scores(balanced)['Symmetry']>feature_scores(messy)['Symmetry']


def test_repeated_pebbles_have_diminishing_returns():
    pie=Pie();pie.add_layer()
    low=pie.copy()
    for i in range(16):low.add_deco('pebbles',0,0,.5)
    high=low.copy()
    for i in range(65):high.add_deco('pebbles',0,0,.5)
    assert feature_scores(high)['Decoration']<=feature_scores(low)['Decoration']+3
    assert feature_scores(high)['Decoration']<=100


def test_varied_design_beats_identical_deco_spam():
    varied=Pie();varied.add_layer()
    repetitive=Pie();repetitive.add_layer()
    for i in range(20):
        varied.add_deco(('leaves','petals','pebbles','sticks','berries')[i%5],0,(i%5-2)*.1,.5)
        repetitive.add_deco('pebbles',0,(i%5-2)*.1,.5)
    assert feature_scores(varied)['Decoration']>feature_scores(repetitive)['Decoration']


def test_recent_identical_entries_lose_originality():
    pie=sample()
    score=feature_scores(pie)['Originality']
    repeat=feature_scores(pie,[fingerprint(pie)])['Originality']
    assert repeat<score


def test_all_features_bounded_and_explained():
    judged=judge(sample(),'Symmetry')
    assert set(judged.features)==set(FEATURES)
    assert all(0<=v<=100 for v in judged.features.values())
    assert len(judged.feedback)>=1
    assert all(v.comment for v in judged.verdicts)


def test_all_themes_have_supported_focus():
    assert len(THEMES)>=5
    assert all(t[2] in FEATURES for t in THEMES)


def test_theme_changes_weighted_score_not_underlying_design():
    p=sample()
    size=judge(p,'Size')
    deco=judge(p,'Decoration')
    assert size.features==deco.features
    assert size.total!=deco.total


def test_originality_signature_detects_real_layout_changes():
    a=sample()
    b=a.copy()
    for d in b.decorations:
        d.x=.8
    assert fingerprint(a)!=fingerprint(b)
