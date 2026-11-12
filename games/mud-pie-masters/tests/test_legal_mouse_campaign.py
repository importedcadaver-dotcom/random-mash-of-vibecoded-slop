"""All 48 Mud Pie Masters goals via production SDL mouse/keyboard gestures."""
from __future__ import annotations

from tools.legal_mouse_campaign import execute


def test_all_48_contests_and_commissions_are_constructible_using_sdl_input(tmp_path):
    evidence = execute(tmp_path / "legal-mouse", limit=48)
    assert evidence["passed"]
    assert evidence["rounds"] == 48
    assert evidence["events"] > 200
    assert evidence["mission_selection"].startswith("Game.begin_round")
    assert all(goal["value"] >= goal["target"]
               for entry in evidence["scores"]
               for goal in entry["goal_proofs"]
               if not goal["rule"].endswith("_max"))
    assert not (tmp_path / "legal-mouse" / "legal_mouse_FAILURE.json").exists()
