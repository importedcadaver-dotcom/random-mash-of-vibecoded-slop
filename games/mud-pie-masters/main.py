"""Mud Pie Masters launcher. Requires Python 3.12+ and pygame-ce.

The internal --qa-smoke switch verifies that packaged assets can be loaded and
a frame rendered, using dummy SDL drivers. Normal game launches are unchanged.
"""
import os
import sys

QA_SMOKE = "--qa-smoke" in sys.argv
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
if QA_SMOKE:
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
from mudpie.game import Game


def main():
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.display.set_caption("Mud Pie Masters — a tiny forest contest")
    display = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    if QA_SMOKE:
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory(prefix="mudpie-packaged-qa-") as isolated_save:
            os.environ["MUDPIE_SAVE_DIR"] = isolated_save
            game = Game(display)
            game.step_frame(1 / 60)
            assert game.scene == "title"
            assert game.paint.images["forest"].get_width() > 100
            assert game.paint.images["player"].get_height() > 20
            game.start_free_build()
            if game.overlay:
                game.close_overlay()
            game.step_frame(1 / 60)
            game.pie.add_layer()
            game.submit()
            assert game.scene == "gallery"
            assert (Path(isolated_save) / "save.json").exists()
            game.step_frame(1 / 60)
            # A GUI EXE may not set PowerShell's LASTEXITCODE. Emit a
            # machine-readable sentinel only after *all* packaged checks pass.
            import json
            Path("qa_packaged_ok.json").write_text(
                json.dumps({"ok": True, "scene": game.scene,
                            "renderer": "pygame", "asset": "forest",
                            "free_build_save_verified": True}), encoding="utf-8")
            pygame.quit()
        return 0
    Game(display).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
