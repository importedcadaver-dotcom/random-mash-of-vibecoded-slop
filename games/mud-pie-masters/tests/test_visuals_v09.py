"""Character-art and text readability regressions after first real playtest."""
from __future__ import annotations
import os
os.environ.setdefault("SDL_VIDEODRIVER","dummy")
os.environ.setdefault("SDL_AUDIODRIVER","dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT","1")
import pytest
pygame=pytest.importorskip("pygame")
from mudpie.game import Game
from mudpie.rendering import ASSETS,Painter


@pytest.fixture
def app(monkeypatch,tmp_path):
    monkeypatch.setenv("MUDPIE_SAVE_DIR",str(tmp_path))
    pygame.init()
    display=pygame.display.set_mode((1280,720),pygame.RESIZABLE)
    g=Game(display)
    g.draw()
    yield g
    pygame.quit()


def test_legacy_judges_replaced_with_distinct_art_from_sibling_visual_language(app):
    """Three different forest bear portraits replace the original teddy faces."""
    for judge in ("petal","boulder","fern"):
        output=app.paint.images[judge]
        legacy=pygame.image.load(str(ASSETS/f"{judge}.png")).convert_alpha()
        assert output.get_size()==legacy.get_size()
        assert pygame.image.tostring(output,"RGBA")!=pygame.image.tostring(legacy,"RGBA")
        assert output.get_at((0,0)).a==0
    assert pygame.image.tostring(app.paint.images["petal"],"RGBA") != pygame.image.tostring(app.paint.images["fern"],"RGBA")


def test_judge_cards_still_render_at_original_layout_coordinates(app,tmp_path):
    app.begin_round()
    app.draw()
    assert app.scene=="clearing" and app.overlay=="chapter"
    app.choose_chapter(False)
    app.draw()
    target=tmp_path/"matching_judges.png"
    pygame.image.save(app.canvas,str(target))
    assert target.stat().st_size>10000


def test_ui_font_minimum_size_and_bruno_no_edge_hugging(app):
    """Body text is no longer drawn as unreadable 10px characters."""
    assert app.paint.font(10).get_height()>=14
    assert app.paint.font(12).get_height()>=14
    assert app.paint.font(20).get_height()>=20
    surface=pygame.Surface((400,400),pygame.SRCALPHA)
    bruno=app.paint.image(surface,"bruno",(200,190),(200,230),center=True)
    daisy=app.paint.image(surface,"daisy",(200,190),(200,230),center=True)
    assert bruno.width < daisy.width
    assert bruno.height < daisy.height


def test_clearing_notifications_do_not_cover_the_round_title(app,monkeypatch):
    """The old global toast obscured the round heading in actual screenshots."""
    app.begin_round()
    app.choose_chapter(False)
    app.notify("Bruno grins at your challenge; Daisy looks determined.")
    texts=[]
    rects=[]
    paint_text=app.paint.text
    paint_rect=app.paint.rect
    def monitor_text(surface,value,*args,**kwargs):
        texts.append(str(value))
        return paint_text(surface,value,*args,**kwargs)
    def monitor_rect(surface,rect,*args,**kwargs):
        rects.append(tuple(rect))
        return paint_rect(surface,rect,*args,**kwargs)
    monkeypatch.setattr(app.paint,"text",monitor_text)
    monkeypatch.setattr(app.paint,"rect",monitor_rect)
    app.draw()
    assert any("Round 1" in t for t in texts)
    assert any("Bruno grins" in t for t in texts)
    assert (295,32,668,50) not in rects
