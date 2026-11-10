"""Gravity, support, saved debris and reversible collapse regression tests."""
from __future__ import annotations
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pytest
pygame = pytest.importorskip("pygame")
from mudpie.game import Game, TABLE_Y
from mudpie.models import Pie


@pytest.fixture
def game(monkeypatch,tmp_path):
    monkeypatch.setenv("MUDPIE_SAVE_DIR",str(tmp_path))
    pygame.init()
    screen=pygame.display.set_mode((1280,720),pygame.RESIZABLE)
    app=Game(screen)
    app.start_free_build()
    if app.overlay:
        app.close_overlay()
    app.draw()
    yield app
    pygame.quit()


def gesture(app, from_pos, to_pos):
    # The production SDL queue, not direct calls into on_down/on_up.
    for typ,pos in ((pygame.MOUSEBUTTONDOWN,from_pos),
                    (pygame.MOUSEMOTION,to_pos),(pygame.MOUSEBUTTONUP,to_pos)):
        kw={"pos":pos}
        if typ==pygame.MOUSEMOTION:
            kw.update(rel=(to_pos[0]-from_pos[0],to_pos[1]-from_pos[1]),
                      buttons=(1,0,0))
        else:
            kw["button"]=1
        pygame.event.post(pygame.event.Event(typ,**kw))
        app.step_frame(1/60)


def finish_fall(app):
    for _ in range(60):
        app.step_frame(1/60)


def test_model_gravity_drops_unsupported_upper_tiers_and_cascades():
    pie=Pie()
    pie.add_layer(0)
    pie.add_layer(110)
    pie.add_layer(112)
    dropped=pie.settle_unsupported()
    assert dropped==[1,2]
    assert [l.fallen for l in pie.layers]==[False,True,True]
    assert all(l.damage>=.68 for l in pie.layers[1:])


def test_model_near_center_stack_stays_supported():
    pie=Pie()
    pie.add_layer(0)
    pie.add_layer(90)
    assert pie.settle_unsupported()==[]
    assert all(not layer.fallen for layer in pie.layers)


def test_new_scoop_after_collapse_is_inserted_before_table_debris_and_keeps_decorations():
    pie=Pie()
    pie.add_layer(0)
    pie.add_layer(160)
    pie.add_deco("petals",1,.4,.4)
    pie.settle_unsupported()
    fresh=pie.add_layer(0)
    assert pie.layers[1] is fresh
    assert [l.fallen for l in pie.layers]==[False,False,True]
    assert pie.decorations[0].layer==2
    assert pie.settle_unsupported()==[]
    clone=Pie.from_dict(pie.to_dict())
    assert clone.to_dict()==pie.to_dict()


def test_real_sdl_unsupported_scoop_falls_visibly_and_lands(game,tmp_path):
    gesture(game,(65,405),(655,553))
    assert len(game.pie.layers)==1
    gesture(game,(65,405),(810,509))
    assert len(game.pie.layers)==2
    assert game.pie.layers[1].fallen
    assert len(game.fall_animations)==1
    anim=game.fall_animations[0]
    assert anim["origin"]<TABLE_Y
    initial=anim["elapsed"]
    for _ in range(5):
        game.step_frame(1/60)
    assert anim["elapsed"]>initial and anim["elapsed"]<anim["duration"]
    mid=tmp_path/"fall_in_progress.png"
    pygame.image.save(game.canvas,str(mid))
    assert mid.stat().st_size>5000
    finish_fall(game)
    assert game.fall_animations==[]
    assert game.pie.layers[1].fallen
    ended=tmp_path/"settled_mud.png"
    pygame.image.save(game.canvas,str(ended))
    assert ended.stat().st_size>5000


def test_undo_returns_fallen_scoop_to_previous_pie_state(game):
    gesture(game,(65,405),(655,553))
    gesture(game,(65,405),(810,509))
    assert game.pie.layers[1].fallen
    game.undo()
    assert len(game.pie.layers)==1
    assert not game.fall_animations
    game.redo()
    assert len(game.pie.layers)==2
    assert game.pie.layers[1].fallen
    assert not game.fall_animations


def test_rebuild_after_falling_does_not_make_another_scoop_float(game):
    gesture(game,(65,405),(655,553))
    gesture(game,(65,405),(810,509))
    finish_fall(game)
    gesture(game,(65,405),(652,507))
    assert len(game.pie.layers)==3
    assert [l.fallen for l in game.pie.layers]==[False,False,True]
    assert game.focus_layer_index==1
    assert game._display_tier_bounds()[2][2:]==(0,0)
    assert not game.fall_animations


def test_real_stack_drag_outside_support_initiates_fall(game):
    gesture(game,(65,405),(655,553))
    gesture(game,(65,405),(655,507))
    assert len(game.pie.layers)==2
    assert not game.pie.layers[1].fallen
    assert game.tool==2
    gesture(game,(655,510),(810,510))
    assert game.pie.layers[1].fallen
    assert game.fall_animations


def test_new_scoop_is_deferred_while_an_older_tier_is_falling(game):
    gesture(game,(65,405),(655,553))
    gesture(game,(65,405),(810,509))
    assert len(game.fall_animations)==1
    assert len(game.pie.layers)==2
    gesture(game,(65,405),(655,508))
    assert len(game.pie.layers)==2
    assert "falling mud land" in game.toast.lower()
    finish_fall(game)
    gesture(game,(65,405),(655,508))
    assert len(game.pie.layers)==3


def test_mid_fall_reposition_is_rechecked_after_last_tier_lands(game):
    """An edit during a fall must not strand another unsupported floating tier."""
    base=game.pie.add_layer(0)
    lower=game.pie.add_layer(0)
    upper=game.pie.add_layer(170)
    game.settle_pie_support()
    assert upper.fallen and game.fall_animations
    # The second standing tier loses contact while the first drop is animating.
    lower.x = 170
    assert game.settle_pie_support() == []  # Deferred during animation.
    assert not lower.fallen
    finish_fall(game)
    assert lower.fallen
    assert not game.fall_animations


def test_falling_snapshot_is_after_actual_gravity_displacement(game):
    """The QA screenshot must depict movement rather than frame-zero hovering."""
    game.pie.add_layer(0)
    game.pie.add_layer(160)
    game.settle_pie_support()
    assert game.fall_animations
    anim=game.fall_animations[0]
    assert anim['elapsed'] == 0
    for _ in range(8):
        game.step_frame(1/60)
    assert 0 < anim['elapsed'] < anim['duration']
    t=anim['elapsed']/anim['duration']
    assert (TABLE_Y-anim['origin']) * t*t > 0


def test_normal_sculpting_waits_until_gravity_lands(game):
    """No player gesture can reorder the indices while falling art is active."""
    gesture(game,(65,405),(655,553))
    gesture(game,(65,405),(810,509))
    assert game.fall_animations
    before=game.pie.to_dict()
    gesture(game,(655,555),(805,555))
    gesture(game,(65,405),(655,507))
    assert game.pie.to_dict()==before
    assert "falling mud land" in game.toast.lower()
    finish_fall(game)
    gesture(game,(65,405),(655,507))
    assert len(game.pie.layers)==3
