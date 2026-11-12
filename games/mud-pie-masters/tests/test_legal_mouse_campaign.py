"""A first chapter built using actual SDL mouse/keyboard gestures, not oracle Pie injection."""
from __future__ import annotations

import json

from tools.legal_mouse_campaign import execute


def test_all_six_first_chapter_contests_and_two_commissions_via_sdl_events(tmp_path):
    evidence = execute(tmp_path / "legal-mouse", limit=8)
    assert evidence["passed"]
    assert evidence["rounds"] == 8
    assert evidence["events"] > 60
    assert evidence["mission_selection"].startswith("Game.begin_round")
    assert all(goal["value"] >= goal["target"]
               for entry in evidence["scores"]
               for goal in entry["goal_proofs"]
               if not goal["rule"].endswith("_max"))
    assert not (tmp_path / "legal-mouse" / "legal_mouse_FAILURE.json").exists()
