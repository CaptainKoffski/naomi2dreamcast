#!/usr/bin/env python3
"""Run: python3 tools/assess/tests/test_gen_tables.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import gen_tables as gt

FIXTURE = """| Some Game (GDL-1) | `aaa` | **GD-ROM** | parent | 10 MB | Puzzle ★ | No | not assessed |
| Some Game (Japan) (GDL-1J) | `aaaj` | **GD-ROM** | clone of `aaa` | 10 MB | Puzzle ★ | No | not assessed |
| Ported Game (GDL-2) | `bbb` | **GD-ROM** | parent | 20 MB | Fighting | Yes (2001) | not assessed |
| Ported Clone (GDL-2J) | `bbbj` | **GD-ROM** | clone of `bbb` | 20 MB | Fighting | No | not assessed |
| Cleopatra Fortune Plus (GDL-0012) | `cleoftp` | **GD-ROM** | parent | 65.8 MB | Puzzle ★ | No | not assessed |
"""

def test_parse_rows():
    rows = gt.parse_rows(FIXTURE)
    assert rows["aaa"]["parent"] is None and rows["aaaj"]["parent"] == "aaa"
    assert rows["bbb"]["dc_port"].startswith("Yes")

def test_families_scope():
    rows = gt.parse_rows(FIXTURE)
    fams = gt.families(rows)
    scope = gt.in_scope(fams, rows)
    assert "aaa" in scope                        # family all-No -> in scope
    assert "bbb" not in scope                    # any member Yes -> whole family out
    assert "cleoftp" not in scope                # EXCLUDE: already fan-ported reference

def test_orphan_clone():
    """Orphan clones (parent absent from table) self-key and don't crash queue()."""
    fixture_orphan = FIXTURE + "| Orphan Game (GDL-9) | `orph` | **GD-ROM** | clone of `missing` | 5 MB | Puzzle ★ | No | not assessed |\n"
    rows = gt.parse_rows(fixture_orphan)
    assert "orph" in rows and "missing" not in rows  # orphan exists, parent doesn't
    fams = gt.families(rows)
    assert "orph" in fams  # orphan self-keys, not parented to missing
    scope = gt.in_scope(fams, rows)
    assert "orph" in scope  # orphan family in scope
    # queue() regression test: sort key must not crash on orphan rep
    def key(rep):
        g = rows[rep]["genre"]
        return (0 if "★" in g else (2 if "⚠" in g else 1), g, rep)
    for rep in scope:
        _ = key(rep)  # no KeyError

def test_patch_cell():
    sidecars = {"aaa": {"scores": {"final": 72.5, "tier": "A"}, "gate": None}}
    out = gt.patch_text(FIXTURE, sidecars, clones={"aaaj": "aaa"})
    assert "| **72.5** A · [assessment](assessments/aaa.md) |" in out
    assert "| see [`aaa`](assessments/aaa.md) |" in out
    assert out.count("not assessed") == 3        # untouched rows stay untouched
    parked = {"aaa": {"scores": None, "gate": "G2 controls: card_reader"}}
    assert "| parked G2 · [notes](assessments/aaa.md) |" in gt.patch_text(FIXTURE, parked, clones={})

if __name__ == "__main__":
    test_parse_rows(); print("test_parse_rows OK")
    test_families_scope(); print("test_families_scope OK")
    test_orphan_clone(); print("test_orphan_clone OK")
    test_patch_cell(); print("test_patch_cell OK")
    print("ALL OK")
