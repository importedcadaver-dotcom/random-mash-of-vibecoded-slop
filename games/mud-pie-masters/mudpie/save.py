"""Safe JSON saves with bounded history and atomic writes."""
from __future__ import annotations
import json
import os
from dataclasses import asdict
from pathlib import Path
from .rivals import Rival, make_rivals
from .campaign import initial_campaign, normalized_campaign

VERSION = 1


def default_path() -> Path:
    override = os.getenv("MUDPIE_SAVE_DIR")
    return Path(override) / "save.json" if override else Path.home() / ".mud_pie_masters" / "save.json"


def save_game(round_number: int, rivals: list[Rival], gallery: list[dict],
              history: list[dict], settings: dict, path: Path | None = None,
              campaign: dict | None = None) -> None:
    path = path or default_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {"version": VERSION, "round": round_number,
            "rivals": [asdict(r) for r in rivals], "gallery": gallery[-60:],
            "history": history[-100:], "settings": settings,
            "campaign": normalized_campaign(campaign)}
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    temp.replace(path)


def load_game(path: Path | None = None) -> dict:
    path = path or default_path()
    defaults = {"round": 1, "rivals": make_rivals(), "gallery": [],
                "history": [], "campaign": initial_campaign(), "settings": {"sound": True, "music": True,
                                           "reduced_motion": False, "fullscreen": False,
                                           "sound_volume": 0.55, "music_volume": 0.28,
                                           "tutorial_seen": False}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        # Valid JSON need not be an object. Ignore malformed root values
        # instead of raising AttributeError before the version check.
        if not isinstance(data, dict):
            return defaults
        if data.get("version") != VERSION:
            return defaults
        # A damaged optional rival record must not discard otherwise valid
        # campaign, scrapbook or history. Preserve only complete, typed pairs.
        saved_rivals = []
        raw_rivals = data.get("rivals", [])
        if isinstance(raw_rivals, list):
            for raw in raw_rivals:
                if not isinstance(raw, dict):
                    continue
                try:
                    rival = Rival(**raw)
                except (TypeError, ValueError):
                    continue
                numeric = ("affection", "victories", "defeats", "embarrassment",
                           "confidence", "rivalry")
                textual = ("name", "personality", "last_signature",
                           "last_interaction")
                if (all(type(getattr(rival, key)) is int for key in numeric)
                        and all(isinstance(getattr(rival, key), str) for key in textual)
                        and isinstance(rival.memories, list)
                        and all(isinstance(item, str) for item in rival.memories)):
                    saved_rivals.append(rival)
        if len(saved_rivals) == 2 and {r.name for r in saved_rivals} == {"Bruno", "Daisy"}:
            defaults["rivals"] = [next(r for r in saved_rivals if r.name == name)
                                   for name in ("Bruno", "Daisy")]
        try:
            defaults["round"] = max(1, min(100000, int(data.get("round", 1))))
        except (ValueError, TypeError, OverflowError):
            pass
        defaults["gallery"] = [entry for entry in data.get("gallery", []) if isinstance(entry, dict)][-60:] if isinstance(data.get("gallery"), list) else []
        defaults["history"] = [entry for entry in data.get("history", []) if isinstance(entry, dict)][-100:] if isinstance(data.get("history"), list) else []
        defaults["campaign"] = normalized_campaign(data.get("campaign"))
        if isinstance(data.get("settings"), dict):
            for key, value in data["settings"].items():
                if key not in defaults["settings"]:
                    continue
                if key.endswith("_volume"):
                    try:
                        defaults["settings"][key] = max(0.0, min(1.0, float(value)))
                    except (TypeError, ValueError):
                        pass
                else:
                    defaults["settings"][key] = bool(value)
    except (OSError, ValueError, TypeError, KeyError):
        pass
    return defaults
