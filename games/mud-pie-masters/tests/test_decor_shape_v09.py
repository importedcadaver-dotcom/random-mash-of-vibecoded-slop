"""Decorative petal/stick shaping: SDL mouse gestures, undo, rendering, old saves."""
from __future__ import annotations
import os
os.environ.setdefault("SDL_VIDEODRIVER","dummy")
os.environ.setdefault("SDL_AUDIODRIVER","dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT","1")

import pytest
pygame=pytest.importorskip("pygame")
from mudpie.game import Game, TABLE_X, TABLE_Y
from mudpie.models import Pie
from mudpie.rendering import decoration_anchor


@pytest.fixture
def app(monkeypatch,tmp_path):
    monkeypatch.setenv("MUDPIE_SAVE_DIR",str(tmp_path))
    pygame.init()
    display=pygame.display.set_mode((1280,720),pygame.RESIZABLE)
    game=Game(display)
    game.start_free_build()
    if game.overlay:
        game.close_overlay()
    game.pie.add_layer(x=0,wetness=.42)
    game.draw()
    yield game
    pygame.quit()


def drag(game,start,end):
    """Send a real SDL press/move/release, not Game.on_motion directly."""
    for typ,pos in ((pygame.MOUSEBUTTONDOWN,start),(pygame.MOUSEMOTION,end),
                    (pygame.MOUSEBUTTONUP,end)):
        payload={"pos":pos}
        if typ==pygame.MOUSEMOTION:
            payload.update(rel=(end[0]-start[0],end[1]-start[1]),buttons=(1,0,0))
        else:
            payload["button"]=1
        pygame.event.post(pygame.event.Event(typ,**payload))
        game.step_frame(1/60)


def _anchor(app,deco):
    px,py=decoration_anchor(app.pie,deco,TABLE_X,TABLE_Y,app._work_scale())
    return (round(px),round(py))


def test_old_saves_keep_normal_decorative_proportions():
    old=Pie.from_dict({"layers":[{"x":0}], "decorations":[{
        "kind":"petals","layer":0,"x":0,"y":0.5,"angle":30,"color":1}]})
    assert (old.decorations[0].stretch_x,old.decorations[0].stretch_y)==(1.,1.)


def test_petal_stretch_and_flatten_are_visible_and_undoable(app):
    petal=app.pie.add_deco("petals",0,0,.5,color=1)
    app.tool=1
    app.draw()
    anchor=_anchor(app,petal)
    crop=pygame.Rect(anchor[0]-52,anchor[1]-50,104,100)
    before=pygame.image.tostring(app.canvas.subsurface(crop),"RGB")
    drag(app,anchor,(anchor[0]+62,anchor[1]))
    assert petal.stretch_x>1.9
    assert petal.stretch_y==1.
    app.draw()
    after=pygame.image.tostring(app.canvas.subsurface(crop),"RGB")
    assert before!=after, "Petal stretching must change actual pixels."
    drag(app,anchor,(anchor[0],anchor[1]+35))
    assert petal.stretch_y<.7
    assert "Petals reshaped" in app.toast
    clone=Pie.from_dict(app.pie.to_dict())
    assert clone.decorations[0].stretch_x==petal.stretch_x
    assert clone.decorations[0].stretch_y==petal.stretch_y
    app.undo()
    assert app.pie.decorations[0].stretch_y==1.
    app.undo()
    assert app.pie.decorations[0].stretch_x==1.
    app.redo()
    assert app.pie.decorations[0].stretch_x>1.9


def test_stick_flattens_but_shape_tool_remains_valid_for_mud(app):
    stick=app.pie.add_deco("sticks",0,.3,.3,angle=0)
    app.tool=1
    app.draw()
    anchor=_anchor(app,stick)
    drag(app,anchor,(anchor[0],anchor[1]+38))
    assert stick.stretch_y<.6
    assert stick.stretch_x==1.
    app.pie.decorations.clear()
    app.tool=1
    app.draw()
    bounds=app._display_tier_bounds()[0]
    p=(round(bounds[0]+bounds[2]/2),round(bounds[1]+bounds[3]/2))
    old=app.pie.layers[0].width
    drag(app,p,(p[0]+64,p[1]))
    assert app.pie.layers[0].width>old


def test_stretch_multipliers_are_clamped_when_loading_untrusted_save():
    data={"layers":[{"x":0}],"decorations":[
        {"kind":"sticks","layer":0,"x":0,"y":0.5,"stretch_x":300,"stretch_y":-5}
    ]}
    d=Pie.from_dict(data).decorations[0]
    assert (d.stretch_x,d.stretch_y)==(2.3,.5)
