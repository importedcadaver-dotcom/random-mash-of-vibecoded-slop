"""A saved pie must lead to the same Daisy response across Python processes.

The RNG seed alone did not guarantee determinism: iterating an unordered set
of borrowed ingredients depended on PYTHONHASHSEED.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


CHILD = r"""
import json
from mudpie.models import Pie
from mudpie.rivals import make_entry, make_rivals

previous = Pie()
previous.add_layer()
for kind in ("leaves", "berries", "petals", "sticks", "pebbles"):
    previous.add_deco(kind, 0, .15, .5)
daisy = next(r for r in make_rivals() if r.name == "Daisy")
# Round 3 deterministically takes the 'borrow previous decoration idea' path.
pie = make_entry(daisy, 3, 7393, previous)
assert any("borrowed" in m for m in daisy.memories), daisy.memories
print(json.dumps({
    "kinds": [d.kind for d in pie.decorations],
    "signature": pie.signature,
    "memory": daisy.memories
}, sort_keys=True))
"""


def test_daisy_borrowed_ingredients_reproducible_across_hash_seeds():
    root = Path(__file__).resolve().parents[1]
    observed = []
    for seed in ("1", "2", "17", "187"):
        env = os.environ.copy()
        env["PYTHONHASHSEED"] = seed
        result = subprocess.run(
            [sys.executable, "-c", CHILD],
            cwd=root, env=env, capture_output=True, text=True, timeout=15,
            check=True,
        )
        observed.append(result.stdout.strip())
    assert len(set(observed)) == 1, "Equal input/seed changed Daisy between processes"
