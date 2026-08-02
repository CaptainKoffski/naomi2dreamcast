#!/usr/bin/env python3
"""Plain-assert tests for score.py (spec §4). Run: python3 tools/assess/tests/test_score.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import score

MB = 1 << 20

def test_region_bands():
    cap = 16 * MB
    assert score.region_score(int(0.5 * cap), cap) == 100.0
    assert score.region_score(int(0.80 * cap), cap) == 100.0
    assert round(score.region_score(cap, cap), 4) == 85.0            # u=1.00 exactly -> 85 (spec §4.1)
    assert round(score.region_score(int(1.25 * cap), cap), 4) == 40.0
    assert round(score.region_score(2 * cap, cap), 4) == 10.0
    assert score.region_score(2 * cap + 1, cap) is None              # gate G3

def test_memory_axis_min_and_gate():
    ax, gated = score.memory_axis({"main": 8 * MB, "vram": 2 * MB, "aram": 2 * MB})  # aram u=1.0
    assert round(ax, 4) == 85.0 and gated is None
    ax, gated = score.memory_axis({"main": 40 * MB, "vram": MB, "aram": MB})
    assert ax is None and gated == "main"

def test_streaming():
    assert score.streaming_axis(2.0, 0.05) == 100.0
    assert round(score.streaming_axis(24.0, 0.1), 4) == round(0.6 * 60 + 0.4 * 100, 4)

def test_guts():
    assert score.guts_axis({"serial", "eeprom_bios"}, 0) == 90.0     # the Cleopatra profile
    assert score.guts_axis({"network"}, 6) == 100 - 25 - 10          # bios-class penalty capped at 10
    assert score.guts_axis(set(PENALTY_ALL), 9) == 35.0              # 100 - 55 - 10 (all penalties + cap)

PENALTY_ALL = ("serial", "eeprom_bios", "eeprom_direct", "rtc", "network", "code_over_4mb")

def test_controls_similarity_tiers():
    assert score.controls_axis("stick") == 100.0
    assert score.controls_axis("card_reader") is None                # gate G2: not on the ladder
    assert score.similarity_axis(True, "full", True) == 100.0        # 20+30+40+30 capped
    assert score.similarity_axis(False, "none", False) == 20.0
    assert score.tier(80.0) == "S" and score.tier(79.9) == "A" and score.tier(19.9) == "D"

def test_final_anchor():
    # Cleopatra anchor (spec §4.6): mem 85, stream 100, guts 90, ctrl 100, sim 100 -> 91.8 S
    axes = {"memory": 85.0, "streaming": 100.0, "guts": 90.0, "controls": 100.0, "similarity": 100.0}
    assert score.final_score(axes) == 91.8
    # no-.dat renormalization (spec §4.3): drop guts -> weights x1.25
    axes2 = {"memory": 85.0, "streaming": 100.0, "guts": None, "controls": 100.0, "similarity": 100.0}
    import math
    exp = math.exp(0.5 * math.log(85) + 0.25 * math.log(100) + 0.125 * math.log(100) + 0.125 * math.log(100))
    assert score.final_score(axes2) == round(exp, 1)

def test_score_sidecar_anchor():
    sc = {
        "set": "cleoftp",
        "boot": {"ok": True},
        "memory": {"main": {"dma_high_water": 11761888}, "vram": {"peak": 8181717, "nz_above_cap": 0},
                   "aram": {"peak": 2097152, "nz_above_cap": 0}},
        "streaming": {"steady_mb_per_min": 2.0, "reread_ratio": 0.05},
        "guts": {"dat_available": True, "flags": ["serial", "eeprom_bios"], "extra_bios_classes": 0},
        "controls": {"device_class": "stick"},
        "similarity": {"developer_match": True, "sdk_overlap": "full", "cart_loader_match": True},
    }
    out = score.score_sidecar(sc)
    assert out["gate"] is None
    assert out["scores"]["final"] == 91.8 and out["scores"]["tier"] == "S"

def test_score_sidecar_gates():
    base = {"set": "x", "boot": {"ok": True},
            "memory": {"main": {"dma_high_water": 40 << 20}, "vram": {"peak": 1}, "aram": {"peak": 1}},
            "streaming": {"steady_mb_per_min": 1, "reread_ratio": 0}, "guts": {"dat_available": True, "flags": [], "extra_bios_classes": 0},
            "controls": {"device_class": "stick"}, "similarity": {"developer_match": False, "sdk_overlap": "none", "cart_loader_match": False}}
    assert score.score_sidecar(dict(base))["gate"].startswith("G3")
    b2 = dict(base); b2["boot"] = {"ok": False}
    assert score.score_sidecar(b2)["gate"].startswith("G1")
    b3 = dict(base); b3["memory"] = {"main": {"dma_high_water": 1}, "vram": {"peak": 1}, "aram": {"peak": 1}}
    b3["controls"] = {"device_class": "card_reader"}
    assert score.score_sidecar(b3)["gate"].startswith("G2")

if __name__ == "__main__":
    for n, f in sorted(globals().items()):
        if n.startswith("test_") and callable(f):
            f(); print(f"{n} OK")
    print("ALL OK")
