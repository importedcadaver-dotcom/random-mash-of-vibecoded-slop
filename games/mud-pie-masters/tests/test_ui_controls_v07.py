"""SDL UI controls and overlap regressions from first Windows playtest Issue #9."""
from __future__ import annotations
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pytest
pygame = pytest.importorskip("pygame")
from mudpie.game import Game


@pytest.fixture
def app(monkeypatch, tmp_path):
    monkeypatch.setenv("MUDPIE_SAVE_DIR", str(tmp_path))
    pygame.init()
    display=pygame.display.set_mode((1280,720),pygame.RESIZABLE)
    game=Game(display)
    game.start_free_build()
    if game.overlay:
        game.close_overlay()
    game.draw()
    yield game
    pygame.quit()


def click(app, pos):
    for typ in (pygame.MOUSEMOTION,pygame.MOUSEBUTTONDOWN,pygame.MOUSEBUTTONUP):
        args={"pos":pos}
        if typ==pygame.MOUSEMOTION:
            args.update(rel=(0,0),buttons=(0,0,0))
        else:
            args["button"]=1
        pygame.event.post(pygame.event.Event(typ, **args))
        app.step_frame(1/60)


def test_color_button_opens_real_swatches_and_selects_explicit_color(app):
    assert app.color_variant==0
    click(app,(1134,448))
    assert app.overlay=="colors"
    app.draw()
    click(app,(457,355))  # Second swatch in the 2-color Chapter 1 palette.
    assert app.overlay is None
    assert app.color_variant==1
    app.draw()
    click(app,(1134,448))
    app.draw()
    click(app,(620,480))  # Back without modifying color.
    assert app.overlay is None
    assert app.color_variant==1


def test_visible_rotate_is_undoable_and_keyboard_uses_same_action(app):
    app.pie.add_layer()
    app.pie.add_deco("petals",0,.25,.4,angle=0)
    app.draw()
    click(app,(1134,543))
    assert app.pie.decorations[-1].angle==30
    click(app,(1090,500))  # New prominent Undo position.
    assert app.pie.decorations[-1].angle==0
    click(app,(1195,500))  # Redo.
    assert app.pie.decorations[-1].angle==30
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN,key=pygame.K_r,mod=0,unicode="r"))
    app.step_frame(1/60)
    assert app.pie.decorations[-1].angle==60


def test_pause_keeps_reset_available_but_workbench_less_crowded(app):
    app.pie.add_layer()
    app.draw()
    click(app,(1134,630))
    assert app.overlay=="settings"
    app.draw()
    click(app,(768,503))
    assert app.overlay=="reset"
    app.draw()
    click(app,(480,444))  # Keep my pie.
    assert app.overlay is None
    assert app.pie.layers


def test_goals_summary_not_clipped_while_full_goals_open_via_button(app,monkeypatch):
    app.begin_round()
    app.choose_chapter(False)
    app.start_crafting()
    if app.overlay:
        app.close_overlay()
    app.draw()
    texts=[]
    original=app.paint.text
    def capture(surf,value,*args,**kw):
        texts.append(str(value))
        return original(surf,value,*args,**kw)
    monkeypatch.setattr(app.paint,"text",capture)
    app.draw()
    assert any("GOALS 0/3" in s for s in texts)
    assert "At least 1 mud tiers" not in texts
    click(app,(1120,344))
    assert app.overlay=="goals"
    texts.clear()
    app.draw()
    assert any("At least 1 mud tiers" in s for s in texts)
    click(app,(630,570))
    assert app.overlay is None


def test_medal_badge_is_outside_all_three_result_cards(app, monkeypatch):
    app.begin_round()
    app.choose_chapter(False)
    app.start_crafting()
    if app.overlay:
        app.close_overlay()
    app.pie.add_layer()
    app.submit()
    for _ in range(3):
        app.advance_presentation()
    assert app.scene=="results"
    drawn=[]
    original=app.paint.rect
    def capture(surf,rect,*args,**kw):
        drawn.append(pygame.Rect(rect))
        return original(surf,rect,*args,**kw)
    monkeypatch.setattr(app.paint,"rect",capture)
    app.draw()
    medal=[r for r in drawn if r.size==(327,61)]
    cards=[r for r in drawn if r.size==(385,270)]
    assert len(medal)==1 and len(cards)==3
    assert all(not medal[0].colliderect(card) for card in cards)


def test_guide_next_page_clamp_stays_bounded(app):
    app.guide_page=4
    app.show_overlay("tutorial")
    app.draw()
    assert app.guide_page==4
    # Only BACK is active on the last guide page.
    click(app,(335,567))
    assert app.guide_page==3
