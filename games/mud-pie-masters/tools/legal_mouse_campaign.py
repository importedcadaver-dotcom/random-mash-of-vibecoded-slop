"""48-challenge legal-input crafting probe, without model-generated player pies.

Mission selection uses Game.begin_round as a *test fixture* (not mouse menu
navigation). After entering the clearing, all player crafting, chapter
decisions, submission, and presentation actions use pygame SDL events passed
through Game.step_frame(). No Pie.add_layer/add_deco, direct state mutation,
challenge_bot or medal injection is permitted.

This is an adaptive scripted bot; it demonstrates mechanical reachability only,
NOT human discoverability, enjoyment, physical Windows interaction or 120 min.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import Counter
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mudpie.campaign import STORY, SIDES, goal_progress, unlocked_colors
from mudpie.models import DECORATIONS
from mudpie.rendering import decoration_anchor
from mudpie.save import load_game
from tools.runtime_walkthrough import Walkthrough


class LegalMouse(Walkthrough):
    """Batch ordered SDL events into one real frame for CI speed."""

    def gesture(self, *events):
        self.send(*events)

    def click(self, x, y, button=1):
        pos = self.window_pos((int(round(x)), int(round(y))))
        self.gesture(
            pygame.event.Event(pygame.MOUSEMOTION, pos=pos, rel=(0, 0), buttons=(0, 0, 0)),
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=button),
            pygame.event.Event(pygame.MOUSEBUTTONUP, pos=pos, button=button),
        )
        self.actions.append(["click", int(round(x)), int(round(y)), button])

    def drag(self, source, destination, n=1):
        a = self.window_pos(source)
        b = self.window_pos(destination)
        motions = [
            pygame.event.Event(
                pygame.MOUSEMOTION,
                pos=(int(round(a[0] + (b[0] - a[0]) * i / n)),
                     int(round(a[1] + (b[1] - a[1]) * i / n))),
                rel=(0, 0), buttons=(1, 0, 0),
            )
            for i in range(1, n + 1)
        ]
        self.gesture(
            pygame.event.Event(pygame.MOUSEMOTION, pos=a, rel=(0, 0), buttons=(0, 0, 0)),
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=a, button=1),
            *motions,
            pygame.event.Event(pygame.MOUSEBUTTONUP, pos=b, button=1),
        )
        self.actions.append(["drag", list(source), list(destination)])

    def key(self, key, mod=0):
        self.gesture(
            pygame.event.Event(pygame.KEYDOWN, key=key, mod=mod, unicode=""),
            pygame.event.Event(pygame.KEYUP, key=key, mod=mod),
        )
        self.actions.append(["key", pygame.key.name(key), mod])


def missions_in_order():
    missions = []
    for chapter in range(6):
        missions.extend(STORY[chapter * 6:(chapter + 1) * 6])
        missions.extend(SIDES[chapter * 2:(chapter + 1) * 2])
    assert len(missions) == 48
    return missions


class CraftPlanner:
    def __init__(self, bot: LegalMouse, challenge):
        self.bot = bot
        self.game = bot.game
        self.mission = challenge
        self.added = 0
        self.alphabet = tuple(k for k in DECORATIONS
                              if not challenge.allowed or k in challenge.allowed)
        assert self.alphabet

    def goals(self, rule):
        return [g for g in self.mission.goals if g.rule == rule]

    def target(self, rule, fallback=0):
        return max((g.target for g in self.goals(rule)), default=fallback)

    def unmet(self):
        return [(g.rule, g.kind, goal_progress(self.game.pie, g, self.mission.weather))
                for g in self.mission.goals if not goal_progress(
                    self.game.pie, g, self.mission.weather)[1]]

    def center(self, layer):
        x, y, w, h = self.game._display_tier_bounds()[layer]
        return int(round(x + w / 2)), int(round(y + h / 2))

    def pos(self, layer, nx, ny):
        p = self.game.pie
        tier = p.layers[layer]
        scale = self.game._work_scale()
        h = sum(a.height for a in p.layers[:layer + 1] if not a.fallen)
        return (int(round(660 + scale * (tier.x + nx * tier.width * .44))),
                int(round(584 - scale * h + scale * tier.height * ny * .77)))

    def add_mud(self):
        p = self.game.pie
        # Drop into the emerging top tier; no direct model mutation.
        height = p.height
        scale = self.game._work_scale()
        y = int(round(584 - (height + 23) * scale))
        old = len(p.layers)
        self.bot.drag((65, 406), (660, y))
        self.bot.require(len(p.layers) == old + 1,
                         f"{self.mission.id}: input did not add mud tier {old + 1}")
        self.bot.require(not p.layers[-1].fallen,
                         f"{self.mission.id}: centered new mud tier fell")

    def shape_width(self, layer, width):
        current = self.game.pie.layers[layer].width
        self.bot.key(pygame.K_2)
        start = self.center(layer)
        dx = int(round((width - current) / 1.1 * self.game._work_scale()))
        if dx:
            self.bot.drag(start, (start[0] + dx, start[1]))
        return self.game.pie.layers[layer].width

    def knead(self, layer):
        self.bot.key(pygame.K_1)
        start = self.center(layer)
        self.bot.drag(start, (start[0] + 175, start[1]))
        self.bot.require(self.game.pie.layers[layer].workable,
                         f"{self.mission.id}: layer {layer} not workable after mouse stirring")

    def shape_type(self, layer, count):
        self.bot.key(pygame.K_2)
        for _ in range(count):
            self.bot.click(*self.center(layer), button=3)

    def offset(self, layer, distance):
        self.bot.key(pygame.K_3)
        start = self.center(layer)
        dx = int(round(distance * self.game._work_scale()))
        self.bot.drag(start, (start[0] + dx, start[1]))
        self.bot.require(not self.game.pie.layers[layer].fallen,
                         f"{self.mission.id}: offset made layer fall")

    def color(self, variant):
        count = unlocked_colors(self.game.campaign)
        self.bot.require(0 <= variant < count, f"Color {variant} unavailable")
        for _ in range((variant - self.game.color_variant) % count):
            self.bot.key(pygame.K_c)

    def place(self, kind, layer=None, nx=None, ny=None):
        if kind not in self.alphabet:
            raise AssertionError(f"{self.mission.id}: disallowed ingredient {kind}")
        if layer is None:
            layer = self.added % len(self.game.pie.layers)
        if nx is None:
            nx = (-.72, .03, .72)[self.added % 3]
        if ny is None:
            ny = (.23, .72)[(self.added // 3) % 2]
        target = self.pos(layer, nx, ny)
        old = len(self.game.pie.decorations)
        source = (65, 406 + 46 * (DECORATIONS.index(kind) + 1))
        self.bot.drag(source, target)
        added = len(self.game.pie.decorations) - old
        self.bot.require(added in (1, 2),
                         f"{self.mission.id}: {kind} at {target} did not land on tier {layer}")
        self.added += 1
        return old

    def shape_decoration(self, index):
        deco = self.game.pie.decorations[index]
        anchor = decoration_anchor(self.game.pie, deco, 660, 584, self.game._work_scale())
        start = tuple(int(round(v)) for v in anchor)
        self.bot.key(pygame.K_2)
        self.bot.drag(start, (start[0] + 44, start[1]))
        self.bot.require(abs(self.game.pie.decorations[index].stretch_x - 1) >= .22,
                         f"{self.mission.id}: placed {deco.kind} didn't shape through mouse")

    def paired(self, kind, number):
        if number <= 0:
            return
        self.color(0)
        enabled = self.game.campaign["next_story"] >= 6
        if enabled:
            if not self.game.mirror_mode:
                self.bot.key(pygame.K_m)
            for j in range(number):
                self.place(kind, layer=j % len(self.game.pie.layers),
                           nx=-.64, ny=.32 + (j % 3) * .17)
            self.bot.key(pygame.K_m)
        else:
            for j in range(number):
                layer = j % len(self.game.pie.layers)
                y = .32 + (j % 3) * .17
                self.place(kind, layer=layer, nx=-.64, ny=y)
                self.place(kind, layer=layer, nx=.64, ny=y)

    def build_geometry(self):
        cap = int(self.target("tiers_max", 7))
        minimum = max(
            2,
            int(self.target("tiers_min", 0)),
            int(self.target("shapes_min", 0)),
            int(self.target("workability_min", 0)),
            int(self.target("layer_pattern_min", 0)),
            math.ceil(self.target("height_min", 0) / 46),
        )
        n = min(cap, minimum)
        self.bot.require(n <= 7 and n >= minimum,
                         f"{self.mission.id}: impossible mud tier specification")
        for _ in range(n):
            self.add_mud()
        # Shape silhouettes before placing decorations (right-click would
        # otherwise remove a decoration under the cursor).
        for i in range(1, min(n, int(self.target("shapes_min", 0)))):
            self.shape_type(i, i % 3)
        taper = self.target("taper_min", 0)
        widen = self.target("width_min", 0)
        if taper or widen:
            desired = max(190, widen + 3, 190 + taper + 9)
            self.shape_width(0, min(300, desired))
        for i in range(int(self.target("workability_min", 0))):
            self.knead(i)
        if self.target("offset_min", 0):
            self.offset(n - 1, self.target("offset_min") + 6)

    def build_decorations(self):
        p = self.game.pie
        top = len(p.layers) - 1

        # Shape/flatten real placed objects with tool-2 mouse drags.
        for goal in self.goals("shaped_decos_min"):
            for j in range(int(goal.target)):
                idx = self.place(goal.kind, layer=top,
                                 nx=(-.73, .73)[j % 2],
                                 ny=.28 if j < 2 else .73)
                self.shape_decoration(idx)

        # Satisfy requested material counts by actual inventory drags.
        for goal in self.goals("kind_min"):
            while sum(d.kind == goal.kind for d in p.decorations) < goal.target:
                self.place(goal.kind)

        for goal in self.goals("kinds_min"):
            for kind in self.alphabet:
                if len({d.kind for d in p.decorations}) >= goal.target:
                    break
                if not any(d.kind == kind for d in p.decorations):
                    self.place(kind)

        # Color count is based on *placed decorations*, not palette selection.
        for goal in self.goals("colors_min"):
            for variant in range(int(goal.target)):
                if variant not in {d.color for d in p.decorations}:
                    self.color(variant)
                    self.place(self.alphabet[variant % len(self.alphabet)])
        self.color(0)

        for goal in self.goals("angle_variants_min"):
            while len({int(d.angle // 45) for d in p.decorations}) < goal.target:
                before = len({int(d.angle // 45) for d in p.decorations})
                self.place(self.alphabet[0], layer=top, nx=.66, ny=.52)
                for _ in range(before * 2):
                    self.bot.key(pygame.K_r)

        for goal in self.goals("layer_pattern_min"):
            for layer in range(int(goal.target)):
                if layer not in {d.layer for d in p.decorations}:
                    self.place(self.alphabet[0], layer=layer)

        for goal in self.goals("zones_min"):
            candidates = [(layer, x, y)
                          for layer in range(len(p.layers))
                          for x in (-.72, -.02, .72)
                          for y in (.20, .76)]
            for layer, x, y in candidates:
                if goal_progress(p, goal, self.mission.weather)[1]:
                    break
                self.place(self.alphabet[0], layer=layer, nx=x, ny=y)

        for goal in self.goals("top_decos_min"):
            while sum(d.layer == top for d in p.decorations) < goal.target:
                self.place(self.alphabet[0], layer=top)

        for goal in self.goals("decos_min"):
            while len(p.decorations) < goal.target:
                self.place(self.alphabet[0])

        # Mirrored placement is a real chapter-unlocked keyboard technique.
        for goal in self.goals("pair_min"):
            while not goal_progress(p, goal, self.mission.weather)[1]:
                self.paired(self.alphabet[0], 1)

        for goal in self.goals("feature_min"):
            if goal.kind == "Symmetry":
                for _ in range(24):
                    if goal_progress(p, goal, self.mission.weather)[1]:
                        break
                    self.paired(self.alphabet[0], 1)
            elif goal.kind == "Integrity":
                for layer in range(len(p.layers)):
                    if goal_progress(p, goal, self.mission.weather)[1]:
                        break
                    if not p.layers[layer].workable:
                        self.knead(layer)

    def construct(self):
        self.build_geometry()
        self.build_decorations()
        self.bot.require(not self.game.fall_animations,
                         f"{self.mission.id}: unfinished falling mud")
        failures = self.unmet()
        self.bot.require(not failures, f"{self.mission.id}: unmet physical goals {failures}")


def execute(output: Path, limit: int = 48) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    bot = LegalMouse(output)
    successes = []
    active = None
    try:
        g = bot.game
        selected = missions_in_order()[:limit]
        for number, mission in enumerate(selected, 1):
            active = mission.id
            before = g.campaign["next_story"]
            # Mission setup is the only direct game call: crafting and
            # progression use the same SDL events as normal play.
            g.begin_round(mission.id)
            g.draw()
            if g.overlay == "chapter":
                bot.click(390, 582)
            bot.require(g.scene == "clearing" and g.overlay is None,
                        f"{active}: chapter/clearing could not open")
            bot.click(1015, 665)
            bot.require(g.scene == "craft", f"{active}: could not enter workbench")
            if g.overlay == "tutorial":
                bot.click(625, 566)
            bot.require(g.overlay is None, f"{active}: tutorial still blocks controls")
            planner = CraftPlanner(bot, mission)
            planner.construct()
            if number in (1, 8, 16, 24, 32, 40, 48):
                bot.capture(f"legal_mouse_{number:02d}_{active}_workbench")
            bot.click(1142, 43)
            bot.require(g.scene == "presentation",
                        f"{active}: actual submit click failed")
            for _ in range(3):
                bot.click(1060, 665)
            bot.require(g.scene == "results",
                        f"{active}: presentation did not reach results")
            bot.require(g.mission_medals >= 2,
                        f"{active}: UI-crafted pie missed medal requirements")
            expected = before + (not mission.side)
            bot.require(g.campaign["next_story"] == expected,
                        f"{active}: actual story progression blocked")
            saved = load_game()
            bot.require(saved["campaign"]["next_story"] == expected,
                        f"{active}: progression not persisted")
            successes.append({
                "mission": active,
                "medals": g.mission_medals,
                "score": g.judgments[0].total,
                "input_events_so_far": bot.input_events,
                "actions_so_far": len(bot.actions),
                "goal_proofs": [
                    {"rule": goal.rule, "kind": goal.kind,
                     "value": goal_progress(g.pie, goal, mission.weather)[0],
                     "target": goal.target}
                    for goal in mission.goals
                ],
            })
        return {
            "passed": True, "method": "SDL mouse/keyboard gameplay construction (no pie injection)",
            "mission_selection": "Game.begin_round fixture API, not map-button navigation",
            "rounds": len(successes), "events": bot.input_events,
            "actions": len(bot.actions), "scores": successes,
            "limitations": [
                "Scripted bot, not independent human play or subjective fun testing",
                "Headless SDL video/audio, no physical Windows mouse or speakers",
                "Challenge selected with internal fixture API; construction and submission SDL-driven",
                "Live model goal feedback is read-only, not inferred from a human-facing image",
                "Does not establish 120 minutes of active meaningful play",
            ],
        }
    except Exception as exc:
        try:
            bot.capture("legal_mouse_FAILURE")
        except Exception:
            pass
        (output / "legal_mouse_FAILURE.json").write_text(json.dumps({
            "error": repr(exc), "active_mission": active,
            "completed": len(successes),
            "last_actions": bot.actions[-30:],
            "goals": [
                {"rule": goal.rule, "kind": goal.kind, "target": goal.target,
                 "value": goal_progress(bot.game.pie, goal, bot.game.mission.weather)[0]}
                for goal in bot.game.mission.goals
            ] if bot.game.mission else [],
        }, indent=2), encoding="utf-8")
        raise
    finally:
        bot.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("qa-artifacts/legal-mouse"))
    parser.add_argument("--limit", type=int, default=48)
    args = parser.parse_args()
    if not 1 <= args.limit <= 48:
        parser.error("--limit must be from 1 to 48")
    report = execute(args.output, limit=args.limit)
    (args.output / "legal_mouse_campaign.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {report['rounds']} SDL-input-constructed contest pies; "
          f"{report['events']} SDL events, no model-injected pies.")
    print("NOT human play, full menu navigation or two-hour gameplay certification.")


if __name__ == "__main__":
    main()
