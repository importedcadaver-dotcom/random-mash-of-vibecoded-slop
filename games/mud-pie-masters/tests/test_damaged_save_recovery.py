"""Damaged old save entries must not interrupt the next real contest."""

import json

import pygame

from mudpie.game import Game
from mudpie.save import load_game


def test_malformed_history_and_gallery_do_not_crash_judging_or_report(monkeypatch, tmp_path):
    """Keep valid history while safely ignoring damaged entries during play."""
    monkeypatch.setenv("MUDPIE_SAVE_DIR", str(tmp_path))
    (tmp_path / "save.json").write_text(json.dumps({
        "version": 1,
        "round": 1,
        "history": [None, 12, {"signatures": None}, {"signatures": {"You": "older-pie"}}],
        "gallery": [None, {"signature": "older-gallery"}],
    }), encoding="utf-8")
    loaded = load_game()
    assert len(loaded["history"]) == 2
    assert len(loaded["gallery"]) == 1

    pygame.init()
    try:
        game = Game(pygame.display.set_mode((1280, 720)))
        game.begin_round()
        game.pie.add_layer()
        game.submit()
        assert game.scene == "presentation"
        for _ in range(3):
            game.advance_presentation()
        assert game.history[-1]["round"] == 1
        assert game.export_playtest_report().is_file()
    finally:
        pygame.quit()

