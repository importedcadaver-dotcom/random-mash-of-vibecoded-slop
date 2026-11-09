from collections import Counter
from mudpie.judging import THEMES,judge
from mudpie.models import Pie
from mudpie.rivals import make_entry,make_rivals,update_relationships
from mudpie.save import load_game,save_game


def test_two_real_sibling_entries_have_tiers_and_decorations():
    for rival in make_rivals():
        entry=make_entry(rival,1,7393)
        assert len(entry.layers)>=1
        assert len(entry.decorations)>=1
        assert entry.signature


def test_rivals_are_personality_driven():
    b,d=make_rivals()
    # Compare aggregate structures, not a single one-off outcome.
    bdata=[make_entry(b,i,7393) for i in range(1,30)]
    ddata=[make_entry(d,i,7393) for i in range(1,30)]
    assert sum(p.height for p in bdata)>sum(p.height for p in ddata)
    assert sum(sum(x.kind=='petals' for x in p.decorations) for p in ddata)>sum(sum(x.kind=='petals' for x in p.decorations) for p in bdata)


def test_rival_creation_is_reproducible():
    a=make_entry(make_rivals()[0],5,777)
    b=make_entry(make_rivals()[0],5,777)
    assert a.to_dict()==b.to_dict()


def test_both_rivals_can_win_in_different_rounds():
    rivals=make_rivals()
    winners=Counter()
    for i in range(1,36):
        scores=[judge(make_entry(r,i,7393),THEMES[(i-1)%5][2]).total for r in rivals]
        winners[rivals[scores.index(max(scores))].name]+=1
    assert winners['Bruno']>0
    assert winners['Daisy']>0


def test_family_memories_update():
    rivals=make_rivals()
    msgs=update_relationships(rivals,{'You':79,'Bruno':31,'Daisy':88},
                              {'Bruno':True,'Daisy':False},1)
    assert len(msgs)==2
    assert rivals[0].embarrassment==1
    assert rivals[1].victories==1
    assert len(rivals[0].memories)==1


def test_genuine_entries_use_same_judging():
    rivals=make_rivals()
    for r in rivals:
        p=make_entry(r,2,7393)
        assert 0<=judge(p,'Size').total<=100


def test_save_load_complete_and_atomic(tmp_path):
    save=tmp_path/'nested'/'save.json'
    rivals=make_rivals()
    pie=Pie();pie.add_layer();pie.add_deco('petals',0,.25,.5)
    gallery=[{'round':1,'pie':pie.to_dict(),'signature':'1-xx','score':82}]
    history=[{'round':1,'winner':'You','scores':{'You':82,'Bruno':71,'Daisy':63}}]
    save_game(2,rivals,gallery,history,{'sound':False,'music':True},save)
    loaded=load_game(save)
    assert loaded['round']==2
    assert loaded['gallery']==gallery
    assert loaded['history']==history
    assert loaded['settings']['sound'] is False
    assert not save.with_suffix('.tmp').exists()


def test_missing_or_bad_save_is_safe(tmp_path):
    path=tmp_path/'save.json'
    assert load_game(path)['round']==1
    path.write_text('{broken JSON',encoding='utf-8')
    assert load_game(path)['round']==1
