#!/usr/bin/env python3
"""Integration test against the pinned local MAME checkout (commit 59e7c0b).
Run: python3 tools/assess/tests/test_controls_extract.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import controls_extract as ce

def test_real_file():
    path = ce.default_mame_path()
    assert os.path.isfile(path), f"pinned MAME source missing: {path}"
    rows = ce.extract(open(path, encoding="utf-8", errors="replace").read())
    assert "naomi" not in rows                      # BIOS roots excluded
    assert "Taito" in rows["cleoftp"]["maker"]        # real credit is "Altron / Taito"
    assert rows["cleoftp"]["parent"] is None        # parent set
    assert rows["ikaruga"]["maker"] == "Treasure"
    assert rows["cvs2mf"]["parent"] == "cvs2"       # clone linkage
    assert len(rows) >= 140                          # the Naomi library
    assert all("device_class_hint" in r for r in rows.values())
    # card/medal/hopper cabinets sharing input_ports="naomi" must not inherit "stick"
    assert rows["wccf116"]["device_class_hint"] == "review"     # WCCF trading-card scanner
    assert rows["cleoftp"]["device_class_hint"] != "review"     # plain sets unaffected
    assert rows["ikaruga"]["device_class_hint"] != "review"

if __name__ == "__main__":
    test_real_file(); print("test_real_file OK"); print("ALL OK")
