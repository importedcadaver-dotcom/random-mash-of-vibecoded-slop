"""Regression tests for production SDL event routing and letterboxed inputs."""
from __future__ import annotations

import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pytest
pygame = pytest.importorskip("pygame")
from mudpie.game import Game


@pytest.fixture
def game(tmp_path, monkeypatch):
    monkeypatch.setenv("MUDPIE_SAVE_DIR", str(tmp_path))
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    result = Game(screen)
    result.draw()
    yield result
    pygame.quit()


def post_and_frame(game, *events):
    for event in events:
        pygame.event.post(event)
    game.step_frame(1 / 60)


def click(game, pos, button=1):
    post_and_frame(
        game,
        pygame.event.Event(pygame.MOUSEMOTION, pos=pos, rel=(0, 0), buttons=(0, 0, 0)),
        pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=button),
        pygame.event.Event(pygame.MOUSEBUTTONUP, pos=pos, button=button),
    )


def test_title_button_routes_queued_mouse_events_to_chapter_overlay(game):
    assert game.scene == "title"
    click(game, (190, 480))
    assert game.scene == "clearing"
    assert game.overlay == "chapter"
    click(game, (390, 585))
    assert game.overlay is None


def test_keyboard_events_drive_actual_crafting_mode_and_pause(game):
    game.start_free_build()
    if game.overlay:
        game.close_overlay()
    game.draw()
    post_and_frame(game, pygame.event.Event(pygame.KEYDOWN, key=pygame.K_2, mod=0, unicode=""))
    assert game.tool == 1
    post_and_frame(game, pygame.event.Event(pygame.KEYDOWN, key=pygame.K_4, mod=0, unicode=""))
    assert game.tool == 3
    post_and_frame(game, pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode=""))
    assert game.overlay == "settings"
    post_and_frame(game, pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode=""))
    assert game.overlay is None


def test_letterbox_click_conversion_and_black_bars_are_safe(game):
    post_and_frame(game, pygame.event.Event(pygame.VIDEORESIZE, w=900, h=900, size=(900, 900)))
    assert game.display.get_size() == (900, 900)
    click(game, (10, 450))
    assert game.scene == "title"
    # In 900x900, logical 190,480 maps to display (134,464).
    scale = min(900 / 1280, 900 / 720)
    offset_y = (900 - 720 * scale) / 2
    click(game, (round(190 * scale), round(offset_y + 480 * scale)))
    assert game.scene == "clearing"


def test_production_step_frame_creates_real_rendered_pixels(game, tmp_path):
    game.step_frame(1 / 60)
    target = tmp_path / "actual_sdl_render.png"
    pygame.image.save(game.display, str(target))
    assert target.exists() and target.stat().st_size > 5000
    assert game.display.get_at((100, 100)) != game.display.get_at((600, 600))


def test_quit_event_stops_main_loop_flag_without_killing_test(game):
    assert game.running
    post_and_frame(game, pygame.event.Event(pygame.QUIT))
    assert not game.running
