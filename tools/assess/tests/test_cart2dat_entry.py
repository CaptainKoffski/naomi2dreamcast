#!/usr/bin/env python3
"""Plain-assert test for cart2dat.py Games[] lookup.
Run: python3 tools/assess/tests/test_cart2dat_entry.py

Regression: the lookup must anchor on an entry's own name field, not a clone's
parent_name reference. `cart2dat.py mushik2e` used to resolve to `mushikc` (whose
parent_name "mushik2e" appears first in naomi_roms.cpp), assemble a foreign
ic8.bin, and die "no NAOMI header" -> guts axis silently dropped.
"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "dat-extract"))
import cart2dat


def test_entry_lookup_ignores_parent_name_refs():
    if not os.path.exists(cart2dat.ROMS):
        print("SKIP  naomi_roms.cpp not available"); return
    e = cart2dat.entry_text(open(cart2dat.ROMS).read(), "mushik2e")
    assert re.match(r'\{\s*"mushik2e"\s*,', e), e[:80]
    assert "epr-24357.ic7" in e, "wrong entry: EPR-mode overlay blob missing"
    assert "ic8.bin" not in e, "resolved to mushikc"


if __name__ == "__main__":
    test_entry_lookup_ignores_parent_name_refs()
    print("OK  test_cart2dat_entry")
