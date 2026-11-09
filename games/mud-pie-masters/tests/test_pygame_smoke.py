"""Run automatically on Windows when pygame-ce is installed.

These tests are skipped in bare environments. They exercise actual pygame
input and drawing with a virtual SDL display, not a human playtest.
"""
import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('SDL_AUDIODRIVER','dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT','1')
import pytest
pygame=pytest.importorskip('pygame')
from mudpie.game import Game


@pytest.fixture
def app(tmp_path,monkeypatch):
    monkeypatch.setenv('MUDPIE_SAVE_DIR',str(tmp_path))
    pygame.init()
    screen=pygame.display.set_mode((1280,720),pygame.RESIZABLE)
    g=Game(screen)
    yield g
    pygame.quit()


def drag(g,source,destination):
    g.on_down(source,1)
    g.on_motion(destination)
    g.on_up(destination,1)


def prepare(g):
    g.begin_round()
    if g.overlay == 'chapter':
        g.choose_chapter(True)
    g.scene='craft'
    g.draw()
    drag(g,(62,402),(654,553))
    assert len(g.pie.layers)==1
    g.draw()


def test_scene_draws_and_competition_starts(app):
    app.draw()
    assert app.scene=='title'
    app.begin_round()
    assert app.overlay == 'chapter'
    app.choose_chapter(True)
    app.draw()
    assert app.scene=='clearing'
    app.on_down((1012,664),1)
    assert app.scene=='craft'


def test_real_mouse_drag_creates_layers_and_all_materials(app):
    prepare(app)
    drag(app,(62,404),(668,506))
    assert len(app.pie.layers)==2
    for i,material in enumerate(('leaves','petals','pebbles','sticks','berries'),start=1):
        drag(app,(62,386+i*46+20),(660,509))
    assert set(d.kind for d in app.pie.decorations)=={'leaves','petals','pebbles','sticks','berries'}
    app.draw()


def test_shape_mix_stack_and_undo(app):
    prepare(app)
    first=app.pie.layers[0]
    original_width=first.width
    app.tool=1
    drag(app,(660,563),(707,537))
    assert app.pie.layers[0].width>original_width
    app.undo()
    assert app.pie.layers[0].width==original_width
    app.redo()
    assert app.pie.layers[0].width>original_width
    app.tool=0
    original_wetness=app.pie.layers[0].wetness
    drag(app,(660,558),(688,557))
    assert app.pie.layers[0].wetness>=original_wetness
    drag(app,(62,402),(653,506))
    app.tool=2
    original_x=app.pie.layers[-1].x
    drag(app,(660,513),(710,513))
    assert app.pie.layers[-1].x>original_x


def test_submit_presentation_results_and_replay(app):
    prepare(app)
    app.submit()
    app.draw()
    assert app.scene=='presentation'
    assert len(app.judgments)==3
    for _ in range(3):
        app.advance_presentation()
    assert app.scene=='results'
    assert len(app.history)==1
    assert app.round_no==2
    assert len(app.gallery)==1
    app.draw()
    app.begin_round()
    assert app.scene=='clearing'
    assert len(app.rival_pies)==2
    assert app.round_no==2


def test_letterboxing_input_conversion(app):
    app.display=pygame.display.set_mode((900,900),pygame.RESIZABLE)
    p=app.to_logical((450,450))
    assert abs(p[0]-640)<=1 and abs(p[1]-360)<=1
    app.draw()


def test_settings_reset_and_screenshot(app,tmp_path):
    prepare(app)
    app.show_overlay('reset')
    app.draw()
    app.reset_pie()
    assert not app.pie.layers
    app.undo()
    assert app.pie.layers
    app.show_overlay('settings')
    app.toggle_setting('reduced_motion')
    assert app.settings['reduced_motion']
    app.draw()
    target=tmp_path/'smoke.png'
    pygame.image.save(app.canvas,str(target))
    assert target.is_file() and target.stat().st_size>1000


def test_campaign_map_and_locked_missions(app):
    app.scene='campaign'
    app.draw()
    assert app.chapter_view==0
    assert app.campaign['next_story']==0
    app.on_down((500,109+24),1)  # Third chapter tab is locked.
    assert app.chapter_view==0
    app.on_down((482,329),1)  # First-row play button is below; no crash.
    app.draw()


def test_complete_story_contest_awards_medal_and_report(app):
    prepare(app)
    app.submit()
    for _ in range(3):
        app.advance_presentation()
    assert app.scene=='results'
    assert app.campaign['next_story']==0  # A plain tier misses the petal goal.
    assert app.campaign['story_medals']['story-01-01']==1
    app.show_overlay('report')
    app.draw()
    app.close_overlay()
    app.draw()


def test_restricted_contest_disallows_other_ingredients(app):
    app.campaign['next_story']=8
    app.begin_round('story-02-03')
    if app.overlay == 'chapter':app.choose_chapter(True)
    assert app.mission.allowed == ('mud','leaves')
    app.scene='craft'
    app.draw()
    app.on_down((62,386+2*46+20),1)  # petals
    assert app.drag is None
    app.draw()


def test_free_build_and_crafting_palette_unlocks(app):
    app.campaign['next_story']=6
    app.start_free_build()
    if app.overlay:
        app.close_overlay()
    app.draw()
    drag(app,(62,404),(660,548))
    assert app.pie.layers
    app.toggle_mirror()
    assert app.mirror_mode
    app.cycle_color()
    app.snapshot()
    app.place_decoration('petals',0,.48,.4)
    assert len(app.pie.decorations)==2
    assert app.pie.decorations[0].x==-app.pie.decorations[1].x
    app.submit()
    assert app.scene=='gallery'
    assert app.gallery[-1]['free'] is True


def test_weather_and_chapter_overlay_draw(app):
    app.campaign['next_story']=18
    app.begin_round('story-04-01')
    assert app.overlay=='chapter'
    app.draw()
    app.choose_chapter(True)
    assert app.overlay is None
    assert app.campaign['choices']['3']=='encourage'
    app.scene='craft'
    app.draw()
    drag(app,(62,404),(660,550))
    assert app.pie.layers[0].wetness>.55
    app.mouse=(660,550)
    old=app.pie.layers[0].wetness
    app.dry_layer()
    assert app.pie.layers[0].wetness<old


def test_gallery_can_page_through_more_than_nine_pies(app):
    from mudpie.models import Pie
    pie=Pie()
    pie.add_layer()
    app.gallery=[{'round':i+1, 'theme':'Scrapbook test',
                  'score':30.5, 'pie':pie.to_dict()} for i in range(20)]
    app.scene='gallery'
    app.draw()
    assert app.gallery_page==0
    app.turn_gallery_page(1)
    app.draw()
    assert app.gallery_page==1
    app.turn_gallery_page(1)
    app.draw()
    assert app.gallery_page==2
    app.turn_gallery_page(1)
    assert app.gallery_page==2
    app.turn_gallery_page(-10)
    assert app.gallery_page==0


def test_real_mouse_shaping_cannot_invent_mud(app):
    from math import isclose
    prepare(app)
    app.tool=1
    layer=app.pie.layers[0]
    old=(layer.width,layer.height,layer.volume)
    drag(app,(660,558),(752,558))
    layer=app.pie.layers[0]
    assert layer.width>old[0] and layer.height<old[1]
    assert isclose(layer.volume,old[2])
    assert isclose(layer.width*layer.height,old[2],abs_tol=.001)
    app.undo()
    assert isclose(app.pie.layers[0].volume,old[2])


def test_player_can_knead_a_real_tier_into_a_workable_state(app):
    prepare(app)
    app.tool=0
    layer=app.pie.layers[0]
    app.on_down((659,560),1)
    for x in range(660,880,10):
        app.on_motion((x,560))
    app.on_up((879,560),1)
    assert layer.workable
    assert 'kneaded' in app.toast.lower()


def test_sibling_choice_changes_both_opponent_entry_and_relationship(app):
    app.begin_round()
    if app.overlay=='chapter':
        app.choose_chapter(True)
    before=app.rival_pies[0].to_dict()
    old_affinity=app.rivals[0].affection
    app.interact_sibling('Bruno','cheer')
    assert app.rivals[0].affection>old_affinity
    assert app.rival_pies[0].to_dict()!=before
    assert len(app.sibling_actions)==1
    app.interact_sibling('Bruno','dare')
    assert len(app.sibling_actions)==1
    app.draw()
