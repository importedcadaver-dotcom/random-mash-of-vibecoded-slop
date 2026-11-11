"""Campaign depth and honest opt-in playtest measurement regression tests."""
from __future__ import annotations

import json
import os
from pathlib import Path
import pytest
from mudpie.campaign import CHALLENGES, Goal, goal_progress
from mudpie.models import Pie
from tools.challenge_bot import design_for


def test_four_story_or_side_creative_briefs_use_real_decoration_shaping():
    """Shaped missions remain visible without dropping the finale's skill goal."""
    shaped=[c for c in CHALLENGES if any(g.rule=="shaped_decos_min" for g in c.goals)]
    assert len(shaped)==4
    assert {"story-02-01","story-03-02","story-05-06","side-03-01"}=={c.id for c in shaped}
    assert all(len(c.goals)<=3 for c in shaped)
    assert max(len(c.goals) for c in CHALLENGES)==4  # Finale adds a legacy skill goal.


@pytest.mark.parametrize("kind",["petals","sticks"])
def test_shape_goal_requires_actual_widening_or_flattening(kind):
    """A shape goal counts altered geometry and survives a save round trip."""
    pie=Pie()
    pie.add_layer()
    d1=pie.add_deco(kind,0,-.3,.4)
    d2=pie.add_deco(kind,0,.3,.4)
    goal=Goal("shaped_decos_min",2,kind)
    assert goal_progress(pie,goal)==(0,False)
    d1.stretch_x=1.35
    assert goal_progress(pie,goal)==(1,False)
    d2.stretch_y=.6
    assert goal_progress(pie,goal)==(2,True)
    restored=Pie.from_dict(pie.to_dict())
    assert goal_progress(restored,goal)==(2,True)


def test_each_added_mission_is_achievable_in_data_model_oracle():
    """Every added brief has a reachable synthetic pie for logic QA."""
    for challenge in CHALLENGES:
        if not any(g.rule=="shaped_decos_min" for g in challenge.goals):
            continue
        design=design_for(challenge)
        assert all(goal_progress(design,g,challenge.weather)[1] for g in challenge.goals)


def test_playtest_report_is_explicit_local_opt_in_not_an_enjoyment_certification(monkeypatch,tmp_path):
    """Real SDL input exports timing without treating it as human validation."""
    os.environ.setdefault("SDL_VIDEODRIVER","dummy")
    os.environ.setdefault("SDL_AUDIODRIVER","dummy")
    pygame=pytest.importorskip("pygame")
    from mudpie.game import Game
    monkeypatch.setenv("MUDPIE_SAVE_DIR",str(tmp_path))
    pygame.init()
    try:
        display=pygame.display.set_mode((1280,720))
        game=Game(display)
        game.campaign["seconds"]=7300  # Two hours alone proves nothing.
        game.begin_round()
        if game.overlay=="chapter":
            game.choose_chapter(False)
        game.start_crafting()
        if game.overlay:
            game.close_overlay()
        game.pie.add_layer()
        for _ in range(60):
            game.step_frame(.25)
        game.submit()
        for _ in range(3):
            game.advance_presentation()
        assert game.timer==pytest.approx(3.0)  # Animation remains capped.
        assert game.campaign["seconds"]>=7315  # Measurement uses uncapped time.
        assert game.history and game.history[-1]["craft_seconds"]>=14
        assert game.history[-1]["round_seconds"]>=14
        file=game.export_playtest_report()
        assert file is not None and file.is_file()
        report=json.loads(file.read_text(encoding="utf-8"))
        assert report["recorded_contests"]==1
        assert report["observed_human_enjoyment_certified"] is False
        assert report["recorded_craft_seconds"]>=14
        assert "idle" in report["caveat"].lower()
        assert not (tmp_path/"upload.json").exists()
        # F10 must invoke that local export from a real SDL keyboard event.
        file.unlink()
        game.draw()
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,key=pygame.K_F10,mod=0,unicode=""))
        game.step_frame(1/60)
        assert (tmp_path/"playtest_report.json").is_file()
        game.history.extend([None, {"scores": None, "craft_seconds": "bad"}])
        assert game.export_playtest_report() is not None
        damaged=json.loads((tmp_path/"playtest_report.json").read_text(encoding="utf-8"))
        assert damaged["recorded_contests"]==2
        assert damaged["recorded_craft_seconds"]>=14
        assert damaged["rounds"][-1]["player_score"] is None
    finally:
        pygame.quit()
