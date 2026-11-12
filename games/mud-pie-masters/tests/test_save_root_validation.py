"""Well-formed JSON with a malformed save root must not crash startup."""
import pytest

from mudpie.save import load_game


@pytest.mark.parametrize("payload", [
    "[]",
    "null",
    "42",
    '"text"',
    "true",
    '[{"version": 1}]',
])
def test_non_object_save_root_recovers_defaults(tmp_path, payload):
    path = tmp_path / "save.json"
    path.write_text(payload, encoding="utf-8")
    loaded = load_game(path)
    assert loaded["round"] == 1
    assert [r.name for r in loaded["rivals"]] == ["Bruno", "Daisy"]
    assert loaded["history"] == []
    assert loaded["gallery"] == []
    assert loaded["campaign"]["next_story"] == 0
