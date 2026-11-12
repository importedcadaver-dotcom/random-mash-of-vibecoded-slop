"""Source- and screenshot-driven workbench text fitting regression tests."""
from __future__ import annotations

import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pytest
pygame = pytest.importorskip("pygame")

from mudpie.game import Game
from mudpie.rendering import Painter


@pytest.mark.parametrize("budget", [0, 5, 14, 18, 25, 32, 44, 70, 100, 160, 210])
@pytest.mark.parametrize("label", [
    "WWWWWWWWWWWWWWWWWW",
    "COLOR 1/2 - CHOOSE",
    "A perfectly ordinary long paragraph",
])
def test_ellipsis_and_text_fit_inside_pixel_budget(budget, label):
    pygame.font.init()
    # Font-only test: no display or asset loading is needed.
    painter = Painter.__new__(Painter)
    painter.fonts = {}
    surf = pygame.Surface((600, 80))
    rect = painter.text(surf, label, (10, 10), size=16, bold=True, max_w=budget)
    assert rect.width <= budget, (label, budget, rect.width)
    pygame.font.quit()


def test_craft_palette_and_mud_hint_fit_existing_sidebar(monkeypatch, tmp_path):
    monkeypatch.setenv("MUDPIE_SAVE_DIR", str(tmp_path))
    pygame.init()
    try:
        game = Game(pygame.display.set_mode((1280, 720)))
        game.start_free_build()
        if game.overlay:
            game.close_overlay()
        game.draw()

        seen = []
        original_text = game.paint.text

        def capture(surf, value, pos, *args, **kwargs):
            rect = original_text(surf, value, pos, *args, **kwargs)
            if str(value) in ("drag to add", "COLOR 1/2 · PICK"):
                seen.append((str(value), rect))
            return rect

        monkeypatch.setattr(game.paint, "text", capture)
        game.draw()
        assert {value for value, _ in seen} == {"drag to add", "COLOR 1/2 · PICK"}
        # Neither label should require truncation in the actual supported font.
        assert game.paint.font(16, True).size("COLOR 1/2 · PICK")[0] <= 174
        assert game.paint.font(12).size("drag to add")[0] <= 233 - 135 - 8
        mud_rect = game._palette_rect(0)
        hint = next(rect for value, rect in seen if value == "drag to add")
        picker = next(rect for value, rect in seen if value == "COLOR 1/2 · PICK")
        assert hint.right <= mud_rect.right - 6
        assert picker.left >= 1054 + 8
        assert picker.right <= 1054 + 190 - 8
    finally:
        pygame.quit()
