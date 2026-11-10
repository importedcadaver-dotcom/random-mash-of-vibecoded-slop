"""Headless, event-driven Pygame walkthrough with genuine rendered screenshots.

This is SDL event injection into the production Game.step_frame path, not OS
mouse automation and not a human playtest. Designed for Windows/Linux CI.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mudpie.game import Game, W, H


class Walkthrough:
    def __init__(self, output: Path):
        self.output = output
        self.output.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="mudpie-e2e-")
        os.environ["MUDPIE_SAVE_DIR"] = self.temp.name
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.display.set_caption("Mud Pie Masters — automated gameplay QA")
        screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
        self.game = Game(screen)
        self.game.draw()
        self.snapshots = []
        self.actions = []
        self.input_events = 0

    def close(self):
        pygame.quit()
        self.temp.cleanup()

    def window_pos(self, logical):
        dw, dh = self.game.display.get_size()
        scale = min(dw / W, dh / H)
        return (int(round((dw - W * scale) / 2 + logical[0] * scale)),
                int(round((dh - H * scale) / 2 + logical[1] * scale)))

    def send(self, *events):
        for event in events:
            pygame.event.post(event)
            self.input_events += 1
        self.game.step_frame(1 / 60)

    def click(self, x, y, button=1):
        pos = self.window_pos((x, y))
        self.send(pygame.event.Event(pygame.MOUSEMOTION, pos=pos, rel=(0, 0), buttons=(0, 0, 0)))
        self.send(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=button))
        self.send(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=pos, button=button))
        self.actions.append(["click", x, y, button])

    def drag(self, source, destination, n=5):
        a = self.window_pos(source)
        b = self.window_pos(destination)
        self.send(pygame.event.Event(pygame.MOUSEMOTION, pos=a, rel=(0, 0), buttons=(0, 0, 0)))
        self.send(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=a, button=1))
        for i in range(1, n + 1):
            p = (int(round(a[0] + (b[0] - a[0]) * i / n)),
                 int(round(a[1] + (b[1] - a[1]) * i / n)))
            self.send(pygame.event.Event(pygame.MOUSEMOTION, pos=p, rel=(0, 0), buttons=(1, 0, 0)))
        self.send(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=b, button=1))
        self.actions.append(["drag", list(source), list(destination)])

    def key(self, key, mod=0):
        self.send(pygame.event.Event(pygame.KEYDOWN, key=key, mod=mod, unicode=""))
        self.send(pygame.event.Event(pygame.KEYUP, key=key, mod=mod))
        self.actions.append(["key", pygame.key.name(key), mod])

    def require(self, condition, message):
        if not condition:
            raise AssertionError(message + f" [scene={self.game.scene}, overlay={self.game.overlay}]")

    def capture(self, name):
        path = self.output / f"{len(self.snapshots)+1:02d}_{name}.png"
        pygame.image.save(self.game.display, str(path))
        data = path.read_bytes()
        self.require(len(data) > 5000, f"Screenshot is suspiciously tiny: {path}")
        size = self.game.display.get_size()
        points = ((size[0]//8, size[1]//8), (size[0]//2, size[1]//2),
                  (size[0]*7//8, size[1]*7//8), (size[0]//3, size[1]*2//3))
        colors = {tuple(self.game.display.get_at(point)[:3]) for point in points}
        self.require(len(colors) >= 2, f"Rendered image appears to be a single flat color: {path}")
        self.snapshots.append({"file": path.name, "scene": self.game.scene,
                               "overlay": self.game.overlay, "size": list(size),
                               "bytes": len(data)})

    def play(self):
        g = self.game
        self.capture("title")
        self.click(190, 480)
        self.require(g.scene == "clearing" and g.overlay == "chapter", "Title start or chapter intro broken")
        self.capture("chapter_intro")
        self.click(388, 581)
        self.require(g.overlay is None, "Chapter intro cannot be dismissed")
        self.capture("clearing")
        bruno_before = g.rival_pies[0].to_dict()
        self.click(160, 622)
        self.require("Bruno" in g.sibling_actions, "Sibling encouragement did not register")
        self.require(g.rival_pies[0].to_dict() != bruno_before, "Bruno ignored encouragement")
        self.click(1100, 622)
        self.require("Daisy" in g.sibling_actions, "Daisy challenge did not register")
        self.capture("siblings_react")
        self.click(1015, 665)
        self.require(g.scene == "craft", "Clearing -> craft button failed")
        if g.overlay == "tutorial":
            self.capture("tutorial")
            self.click(625, 566)
        self.require(g.overlay is None, "Tutorial close failed")
        self.capture("empty_workbench")
        self.drag((64, 406), (651, 553))
        self.require(len(g.pie.layers) == 1, "Mud palette drag did not create first tier")
        self.capture("first_mud_scoop")
        self.key(pygame.K_1)
        # 170 px of stirring reaches the .30 worked threshold without
        # over-wetting; the first story objective requires a WORKABLE tier.
        self.drag((654, 561), (825, 562))
        self.require(g.pie.layers[0].workable, "First-contest mixing did not reach WORKABLE")
        self.capture("workable_mix_indicator")
        self.key(pygame.K_2)
        before = g.pie.layers[0].volume
        self.drag((653, 554), (730, 552))
        self.require(abs(g.pie.layers[0].volume - before) < .01,
                     "Shape gesture invented or lost mud")
        self.key(pygame.K_z, pygame.KMOD_CTRL)
        self.key(pygame.K_y, pygame.KMOD_CTRL)
        self.drag((64, 406), (655, 510))
        self.require(len(g.pie.layers) == 2, "Second scoop did not stack")
        self.key(pygame.K_3)
        start_x = g.pie.layers[1].x
        self.drag((660, 515), (698, 515))
        self.require(g.pie.layers[1].x != start_x, "Stack drag did not offset tier")
        self.key(pygame.K_4)
        for kind_y, pos in ((497, (630, 505)), (497, (655, 508)),
                            (497, (676, 508)), (450, (618, 510)),
                            (545, (683, 517)), (591, (648, 518)),
                            (638, (653, 502))):
            self.drag((65, kind_y), pos)
        self.require(len(g.pie.decorations) >= 3, "Decorations failed to attach")
        self.capture("decorated_workbench")
        self.click(1135, 343)
        self.require(g.overlay == "goals", "Full crafting-goals panel did not open")
        self.capture("full_crafting_goals")
        self.click(644, 572)
        self.require(g.overlay is None, "Crafting goals panel could not close")
        self.key(pygame.K_ESCAPE)
        self.require(g.overlay == "settings", "Escape did not open settings")
        self.capture("settings")
        self.click(639, 585)
        self.require(g.overlay is None, "Could not exit settings")
        self.click(1150, 41)
        self.require(g.scene == "presentation", "Submit button did not enter presentation")
        self.require(len(g.judgments) == 3, "Not all competitors were scored")
        self.capture("presentation_player")
        self.key(pygame.K_SPACE)
        self.capture("presentation_bruno")
        self.key(pygame.K_SPACE)
        self.capture("presentation_daisy")
        self.key(pygame.K_SPACE)
        self.require(g.scene == "results" and len(g.history) == 1, "Judging could not complete")
        self.require(g.campaign["next_story"] >= 1, "First quest cannot unlock through UI events")
        self.capture("results")
        self.click(1021, 647)
        self.require(g.overlay == "judge_notes", "Full judge comments did not open")
        self.capture("full_judge_comments")
        self.click(644, 603)
        self.require(g.overlay is None, "Judge comments could not close")
        self.click(570, 692)
        self.require(g.overlay == "report", "Results report button broken")
        self.capture("challenge_report")
        self.click(624, 576)
        self.require(g.overlay is None, "Report dismissal broken")
        self.click(190, 693)
        self.require(g.scene == "title", "Results -> title button broken")
        self.click(565, 479)
        self.require(g.scene == "campaign", "Title -> campaign button broken")
        self.capture("campaign_map")
        self.click(1145, 44)
        self.require(g.scene == "title", "Campaign -> title broken")
        self.click(201, 546)
        self.require(g.scene == "craft" and g.mode == "free", "Free-build entry failed")
        self.drag((65, 406), (658, 555))
        self.click(1143, 39)
        self.require(g.scene == "gallery" and g.gallery[-1].get("free"),
                     "Free-build save/gallery failed")
        self.capture("scrapbook")
        # Real resize event, followed by coordinate conversion and button click.
        self.send(pygame.event.Event(pygame.VIDEORESIZE, w=900, h=900, size=(900, 900)))
        self.require(g.display.get_size() == (900, 900), "Resize event failed")
        self.capture("resized_900x900")
        prev = g.scene
        self.send(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(10, 450), button=1))
        self.require(g.scene == prev, "Black letterbox margin triggered a button")
        self.click(1100, 44)
        self.require(g.scene == "title", "Letterboxed click failed")
        self.capture("title_letterboxed")
        g.save()
        self.require((Path(self.temp.name) / "save.json").exists(), "Save file missing")
        return {
            "success": True,
            "screenshot_count": len(self.snapshots),
            "input_event_count": self.input_events,
            "action_count": len(self.actions),
            "snapshots": self.snapshots,
            "actions": self.actions,
            "round": g.round_no,
            "story_next": g.campaign["next_story"],
            "history_entries": len(g.history),
            "free_build_saved": True,
            "platform": sys.platform,
            "video_driver": pygame.display.get_driver(),
            "note": "SDL synthetic input and real pygame.rendered frames; not an OS-level or human playtest.",
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("qa-artifacts/runtime"))
    args = parser.parse_args()
    runner = Walkthrough(args.output)
    try:
        report = runner.play()
        (args.output / "walkthrough.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
        print("PASS: game loop, UI input, first story goal, free build, resize, screenshots")
        print(f"{report['screenshot_count']} actual SDL screenshots saved to {args.output}")
    except Exception as exc:
        # Preserve last frame and traceback for CI artifact inspection.
        try:
            runner.capture("failure_frame")
        except Exception:
            pass  # Never hide the original gameplay failure.
        checks = getattr(runner.game, "mission_checks", [])
        report = {"success": False, "error": repr(exc),
                  "scene": runner.game.scene, "overlay": runner.game.overlay,
                  "mission_checks": [[g.rule, g.kind, val, ok] for g, val, ok in checks],
                  "snapshots": runner.snapshots, "actions": runner.actions}
        (args.output / "walkthrough.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
        raise
    finally:
        runner.close()


if __name__ == "__main__":
    main()
