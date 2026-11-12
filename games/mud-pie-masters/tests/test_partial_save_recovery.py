"""Corrupted optional save fields should not erase healthy gameplay progress."""
from __future__ import annotations

import json
from dataclasses import asdict

import pytest

from mudpie.rivals import make_rivals
from mudpie.save import load_game, save_game


def _save_with_bad_field(tmp_path, *, rivals=None, round_value=8):
    path = tmp_path / "save.json"
    gallery = [{"round": 7, "pie": {"layers": [{"width": 190, "height": 49}]},
                "signature": "valid", "score": 61.0}]
    history = [{"round": 7, "winner": "Daisy", "scores": {"You": 61,
                "Daisy": 70, "Bruno": 55}}]
    save_game(8, make_rivals(), gallery, history, {"sound": True},
              path, campaign={"next_story": 4})
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["rivals"] = rivals
    payload["round"] = round_value
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path, gallery, history


@pytest.mark.parametrize("invalid_rivals", [
    None,
    {"Bruno": "not an array"},
    [None],
    [1, {"name": "Daisy"}],
    [asdict(make_rivals()[0]), {"name": "Daisy", "personality": "little sister",
                                 "affection": "broken"}],
])
def test_invalid_rivals_do_not_erase_healthy_campaign(tmp_path, invalid_rivals):
    path, gallery, history = _save_with_bad_field(tmp_path, rivals=invalid_rivals)
    state = load_game(path)
    assert state["round"] == 8
    assert state["campaign"]["next_story"] == 4
    assert state["gallery"] == gallery
    assert state["history"] == history
    assert [r.name for r in state["rivals"]] == ["Bruno", "Daisy"]
    assert all(isinstance(r.affection, int) for r in state["rivals"])


@pytest.mark.parametrize("invalid_round", [None, "broken", [], {}, "Infinity"])
def test_invalid_round_only_defaults_the_round(tmp_path, invalid_round):
    path, gallery, history = _save_with_bad_field(
        tmp_path, rivals=[asdict(r) for r in make_rivals()],
        round_value=invalid_round,
    )
    state = load_game(path)
    assert state["round"] == 1
    assert state["campaign"]["next_story"] == 4
    assert state["gallery"] == gallery
    assert state["history"] == history


def test_valid_rival_records_and_round_still_restore(tmp_path):
    rivals = make_rivals()
    rivals[0].affection = 87
    rivals[1].memories = ["I won!"]
    path = tmp_path / "save.json"
    save_game(11, rivals, [], [], {"sound": True}, path,
              campaign={"next_story": 7})
    loaded = load_game(path)
    assert loaded["round"] == 11
    assert loaded["campaign"]["next_story"] == 7
    assert loaded["rivals"][0].affection == 87
    assert loaded["rivals"][1].memories == ["I won!"]
