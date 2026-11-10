"""Real SDL first-play regression tests from the owner's Windows playtest #9.

No human enjoyment or real monitor is simulated by these checks.
"""
from __future__ import annotations

import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pytest
pygame = pytest.importorskip("pygame")
from mudpie.game import Game
from mudpie.campaign import goal_progress


@pytest.fixture
def game(monkeypatch, tmp_path):
    monkeypatch.setenv("MUDPIE_SAVE_DIR", str(tmp_path))
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    instance = Game(screen)
    instance.draw()
    yield instance
    pygame.quit()


def send(game, *events):
    for event in events:
        pygame.event.post(event)
    game.step_frame(1 / 60)


def mouse(game, kind, pos, button=1):
    fields = {"pos": pos}
    if kind == pygame.MOUSEMOTION:
        fields.update(rel=(0, 0), buttons=(1, 0, 0))
    else:
        fields["button"] = button
    send(game, pygame.event.Event(kind, **fields))


def click(game, pos):
    mouse(game, pygame.MOUSEBUTTONDOWN, pos)
    mouse(game, pygame.MOUSEBUTTONUP, pos)


def begin_craft(game):
    game.begin_round()
    assert game.overlay == "chapter"
    game.choose_chapter(False)
    game.start_crafting()
    if game.overlay == "tutorial":
        game.close_overlay()
    game.draw()
    # Scoop through the production SDL event path.
    mouse(game, pygame.MOUSEBUTTONDOWN, (65, 405))
    mouse(game, pygame.MOUSEMOTION, (654, 553))
    mouse(game, pygame.MOUSEBUTTONUP, (654, 553))
    assert len(game.pie.layers) == 1
    assert game.pie.layers[0].wetness == pytest.approx(.42)
    assert not game.pie.layers[0].workable


def test_first_launch_says_start_and_resume_says_continue(game, monkeypatch):
    labels = []
    original = game.button

    def capture(rect, text, callback, **kw):
        labels.append(text)
        return original(rect, text, callback, **kw)

    monkeypatch.setattr(game, "button", capture)
    game.draw()
    assert "START THE STORY" in labels
    assert "CONTINUE THE STORY" not in labels
    game.campaign["next_story"] = 1
    labels.clear()
    game.draw()
    assert "CONTINUE THE STORY" in labels


def test_chapter_buttons_have_equal_visual_priority_and_challenge_is_valid(game, monkeypatch):
    game.begin_round()
    observed = []
    original = game._overlay_button

    def track(rect, label, callback, primary=False):
        if "SIBLINGS" in label or "COMPETE" in label:
            observed.append((label, primary))
        return original(rect, label, callback, primary)

    monkeypatch.setattr(game, "_overlay_button", track)
    game.draw()
    assert len(observed) == 2
    assert all(not primary for _, primary in observed)
    before = [(r.affection, r.confidence, r.rivalry) for r in game.rivals]
    game.choose_chapter(False)
    assert game.campaign["choices"]["0"] == "challenge"
    for rival, (affection, confidence, rivalry) in zip(game.rivals, before):
        assert rival.affection >= affection
        assert rival.confidence > confidence
        assert rival.rivalry > rivalry


def test_tutorial_opens_one_page_at_a_time_and_is_reopenable(game):
    game.begin_round()
    game.choose_chapter(False)
    game.start_crafting()
    assert game.overlay == "tutorial"
    assert game.guide_page == 0
    game.draw()
    click(game, (926, 568))  # NEXT
    assert game.overlay == "tutorial"
    assert game.guide_page == 1
    game.draw()
    click(game, (640, 568))  # LET ME TRY IT
    assert game.overlay is None
    send(game, pygame.event.Event(pygame.KEYDOWN, key=pygame.K_h, mod=0, unicode=""))
    assert game.overlay == "tutorial"
    game.draw()
    assert game.guide_page == 1
    click(game, (343, 568))  # BACK
    assert game.guide_page == 0


def test_clear_weather_scoop_kneads_then_can_overmix_and_undo(game, monkeypatch):
    begin_craft(game)
    goal = next(g for g in game.mission.goals if g.rule == "workability_min")
    layer = game.pie.layers[0]
    assert not goal_progress(game.pie, goal)[1]

    # Staying inside the mud tier while covering >123 px should become workable.
    mouse(game, pygame.MOUSEBUTTONDOWN, (655, 560))
    for i in range(5):
        mouse(game, pygame.MOUSEMOTION, (705 if i % 2 == 0 else 657, 560))
    mouse(game, pygame.MOUSEBUTTONUP, (705, 560))
    assert layer.workable
    assert goal_progress(game.pie, goal)[1]
    assert "WORKABLE" in game.toast.upper()

    messages = []
    original_text = game.paint.text
    def capture(surf, message, pos, size=24, color=None, bold=False, center=False, max_w=None):
        messages.append(str(message))
        if color is None:
            return original_text(surf, message, pos, size, bold=bold, center=center, max_w=max_w)
        return original_text(surf, message, pos, size, color, bold, center, max_w)
    monkeypatch.setattr(game.paint, "text", capture)
    game.draw()
    assert any("KNEAD" in m for m in messages)
    assert any("MOISTURE" in m for m in messages)
    assert any("WORKABLE" in m for m in messages)

    mouse(game, pygame.MOUSEBUTTONDOWN, (655, 560))
    for i in range(15):
        mouse(game, pygame.MOUSEMOTION, (705 if i % 2 == 0 else 655, 560))
    mouse(game, pygame.MOUSEBUTTONUP, (705, 560))
    assert layer.wetness > .73
    assert not layer.workable
    assert not goal_progress(game.pie, goal)[1]
    assert "UNDO" in game.toast.upper()
    assert "D from Storm Season" not in game.toast

    game.undo()
    assert game.pie.layers[0].workable
    assert goal_progress(game.pie, goal)[1]


def test_actual_d_key_is_locked_but_never_recommended_as_immediate_recovery(game):
    begin_craft(game)
    game.mouse = (656, 560)
    before = game.pie.layers[0].wetness
    send(game, pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d, mod=0, unicode="d"))
    assert game.pie.layers[0].wetness == before
    assert "unlocks" in game.toast.lower()
