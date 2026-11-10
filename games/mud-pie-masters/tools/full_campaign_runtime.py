"""Exercise 48 actual Pygame scene/judging/save cycles with oracle-generated pies.

Each first scoop and each submit/presentation is delivered through the game's
real SDL event dispatcher. Exact challenge solutions come from challenge_bot
and are injected into the pie model; this is NOT 48 human-crafted pies.
A separate walkthrough validates physical tool gestures.
"""
from __future__ import annotations
import argparse
import json
import time
import sys
from pathlib import Path

# Works when invoked as python tools/full_campaign_runtime.py from game root.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mudpie.campaign import STORY, SIDES, campaign_statistics
from mudpie.save import load_game
from tools.challenge_bot import design_for
from tools.runtime_walkthrough import Walkthrough


def execute(output: Path) -> dict:
    start = time.monotonic()
    bot = Walkthrough(output)
    results = []
    try:
        game = bot.game
        missions = []
        for chapter in range(6):
            missions.extend(STORY[6*chapter:6*(chapter+1)])
            missions.extend(SIDES[2*chapter:2*(chapter+1)])
        assert len(missions) == 48
        for ordinal, mission in enumerate(missions, 1):
            before_story = game.campaign["next_story"]
            game.begin_round(mission.id)
            if game.overlay == "chapter":
                game.draw()
                game.choose_chapter(True)
            bot.require(game.scene == "clearing", f"{mission.id}: clearing unavailable")
            bot.require(game.mission.id == mission.id, f"{mission.id}: wrong mission selected")
            game.draw()
            bot.click(1015, 666)
            if game.overlay == "tutorial":
                game.close_overlay()
            bot.require(game.scene == "craft", f"{mission.id}: workbench unavailable")
            game.draw()
            bot.drag((65, 405), (654, 553))
            bot.require(len(game.pie.layers) == 1,
                        f"{mission.id}: mouse-placed mud tier was not created")
            # The oracle constructs feasible test geometry, not actual mouse art.
            game.pie = design_for(mission)
            game.draw()
            bot.click(1143, 41)
            bot.require(game.scene == "presentation", f"{mission.id}: submit broke")
            bot.require(len(game.judgments) == 3, f"{mission.id}: rivals not scored")
            if ordinal in (1, 8, 16, 24, 32, 40, 48):
                bot.capture(f"challenge_{ordinal:02d}_{mission.id}_presentation")
            for _ in range(3):
                game.draw()
                bot.click(1060, 665)
            bot.require(game.scene == "results", f"{mission.id}: results did not open")
            bot.require(game.mission_medals >= 2,
                        f"{mission.id}: oracle failed checks {[(g.rule,v,ok) for g,v,ok in game.mission_checks]}")
            expected_story = before_story + (0 if mission.side else 1)
            bot.require(game.campaign["next_story"] == expected_story,
                        f"{mission.id}: unexpected progression")
            bot.require(len(game.judgments) == 3 and len(game.history) == ordinal,
                        f"{mission.id}: history/judging corruption")
            bot.require(game.gallery[-1]["mission"] == mission.id,
                        f"{mission.id}: gallery stored wrong mission")
            if ordinal in (1, 8, 16, 24, 32, 40, 48):
                bot.capture(f"challenge_{ordinal:02d}_{mission.id}_results")
            game.save()
            saved = load_game()
            bot.require(saved["campaign"]["next_story"] == game.campaign["next_story"],
                        f"{mission.id}: save did not retain progression")
            medal_key = "side_medals" if mission.side else "story_medals"
            bot.require(saved["campaign"][medal_key].get(mission.id, 0) >= 2,
                        f"{mission.id}: medal lost on save")
            results.append({
                "mission": mission.id, "chapter": mission.chapter + 1, "side": mission.side,
                "medal": game.mission_medals, "score": game.judgments[0].total,
                "winner": game.last_winner,
                "rival_scores": [ev.total for ev in game.judgments[1:]],
                "collapsed": game.collapsed, "story_progress": game.campaign["next_story"],
            })
        bot.require(game.campaign["next_story"] == 36, "Final story contest did not complete")
        bot.require(len(game.campaign["story_medals"]) == 36, "Missing story medal")
        bot.require(len(game.campaign["side_medals"]) == 12, "Missing commission medal")
        bot.require(game.round_no == 49, "Round counter inconsistent after 48 contests")
        game.scene = "title"
        game.draw()
        bot.capture("post_campaign_title")
        game.begin_round()
        bot.require(game.scene == "campaign", "Post-campaign replay/map entry failed")
        game.draw()
        bot.capture("completed_campaign_map")
        stats = campaign_statistics(game.campaign)
        bot.require(stats["story_done"] == 36 and stats["side_done"] == 12,
                    "Completion statistics disagree with mission records")
        return {
            "passed": True,
            "duration_seconds_measured_for_bot": round(time.monotonic() - start, 3),
            "automated_rounds": len(results), "story_rounds": 36, "optional_commissions": 12,
            "rounds_with_2_or_3_medals": sum(x["medal"] >= 2 for x in results),
            "saves_reload_checked": len(results),
            "rival_wins": {name: sum(x["winner"] == name for x in results)
                           for name in ("You", "Bruno", "Daisy")},
            "screenshots": bot.snapshots,
            "input_events": bot.input_events,
            "round_results": results,
            "limitations": [
                "SDL dummy video and audio: no physical monitor or audio output",
                "Test pies generated in the model by challenge oracle, not constructed with the mouse",
                "Not a human playtest or two-hour enjoyment measurement",
                "Separate runtime_walkthrough.py exercises tactile tool gestures",
            ],
        }
    except Exception as exc:
        try:
            bot.capture("failure_frame")
        except Exception:
            pass
        (output / "full_campaign_FAILURE.json").write_text(json.dumps({
            "error": repr(exc), "last_mission": results[-1]["mission"] if results else None,
            "rounds_completed": len(results), "snapshots": bot.snapshots,
        }, indent=2), encoding="utf-8")
        raise
    finally:
        bot.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("qa-artifacts/full-campaign"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = execute(args.output)
    (args.output / "full_campaign.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"PASS: {report['automated_rounds']} Pygame scene/judging/save cycles, "
          f"{report['saves_reload_checked']} save reloads, "
          f"{len(report['screenshots'])} screenshots, oracle-generated test pies.")
    print("NOT a human playtest; not two-hour certification.")


if __name__ == "__main__":
    main()
