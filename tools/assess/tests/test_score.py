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

def test_score_sidecar_none_streaming():
    # FIX 2: short run with no post-handoff streaming data (steady_mb_per_min=None)
    # Should not raise; drops streaming axis, renormalizes weights
    import math
    sc = {
        "set": "shortrun",
        "boot": {"ok": True},
        "memory": {"main": {"dma_high_water": 11761888}, "vram": {"peak": 8181717, "nz_above_cap": 0},
                   "aram": {"peak": 2097152, "nz_above_cap": 0}},
        "streaming": {"steady_mb_per_min": None, "reread_ratio": 0},
        "guts": {"dat_available": True, "flags": ["serial", "eeprom_bios"], "extra_bios_classes": 0},
        "controls": {"device_class": "stick"},
        "similarity": {"developer_match": True, "sdk_overlap": "full", "cart_loader_match": True},
    }
    out = score.score_sidecar(sc)
    assert out["gate"] is None
    assert out["scores"]["streaming"] is None
    # Final = geom mean of memory(85), guts(90), controls(100), similarity(100) with renormalized weights
    exp = math.exp(0.5 * math.log(85) + 0.25 * math.log(90) + 0.125 * math.log(100) + 0.125 * math.log(100))
    assert out["scores"]["final"] == round(exp, 1)

def test_main_unmeasured_never_100():
    # gwing2 shape (kb §4.v): PIO loader — dma_high_water 0 with real DMA
    # events means the main axis is BLIND, not "u=0 -> 100". The region drops
    # from the memory min() (spec §4.3 renormalize precedent) and a flag
    # records it in the sidecar.
    sc = {
        "set": "synth-pio",
        "boot": {"ok": True},
        "memory": {"main": {"dma_high_water": 0},
                   "vram": {"peak": 8066048, "nz_above_cap": 0},   # u=0.96
                   "aram": {"peak": 2097152, "nz_above_cap": 0}},  # u=1.0 -> 85
        "streaming": {"steady_mb_per_min": 1.155, "reread_ratio": 0.72,
                      "dma_events": 1344},
        "guts": {"dat_available": False},
        "controls": {"device_class": "stick"},
        "similarity": {"developer_match": False, "sdk_overlap": "none",
                       "cart_loader_match": False},
    }
    score.score_sidecar(sc)
    assert sc["gate"] is None
    assert sc["scores"]["main_unmeasured"] is True
    assert sc["scores"]["memory"] == 85.0, sc["scores"]   # min(vram, aram)

def test_main_write_truth_preferred():
    # v6 sidecar: memory.main.peak (write-truth) is the scored figure even
    # when dma_high_water is 0 (PIO loader, now measured) — no flag.
    sc = {
        "set": "synth-v6",
        "boot": {"ok": True},
        "memory": {"main": {"peak": 5 * MB, "nz_total": 4 * MB,
                            "nz_above_cap": 0, "dma_high_water": 0},
                   "vram": {"peak": 6 * MB, "nz_above_cap": 0},
                   "aram": {"peak": 1 * MB, "nz_above_cap": 0}},
        "streaming": {"steady_mb_per_min": 2.0, "reread_ratio": 0.05},
        "guts": {"dat_available": False},
        "controls": {"device_class": "stick"},
        "similarity": {"developer_match": False, "sdk_overlap": "none",
                       "cart_loader_match": False},
    }
    score.score_sidecar(sc)
    assert sc["gate"] is None
    assert "main_unmeasured" not in sc["scores"], sc["scores"]
    assert sc["scores"]["memory"] == 100.0, sc["scores"]  # all three regions fit

def _volume_sc(aram):
    # main/vram comfortably fit so the memory axis == the aram sub-score path
    return {
        "set": "synth-volume", "boot": {"ok": True},
        "memory": {"main": {"peak": 5 * MB, "nz_total": 4 * MB, "nz_above_cap": 0,
                            "dma_high_water": 0},
                   "vram": {"peak": 6 * MB, "nz_above_cap": 0},
                   "aram": aram},
        "streaming": {"steady_mb_per_min": 2.0, "reread_ratio": 0.05},
        "guts": {"dat_available": False},
        "controls": {"device_class": "stick"},
        "similarity": {"developer_match": False, "sdk_overlap": "none",
                       "cart_loader_match": False},
    }

def test_aram_small_blob_high_address_scores():
    # gwing2 shape (spec: the divergent case): 47.5 KB blob at the top of an
    # 8 MiB bank — address-u 3.99 parked it; volume-u 1.023 must score ~80.8.
    sc = _volume_sc({"peak": 8372160, "nz_above_cap": 48674,
                     "content_total": 2097152 + 48674})
    score.score_sidecar(sc)
    assert sc["gate"] is None, sc["gate"]
    assert sc["scores"]["memory"] == 80.8, sc["scores"]

def test_aram_volume_overflow_parks_with_content_message():
    # 4.4 MB of real compacted content (takoron class): u > 2 -> park, and the
    # message says "content" because the gate keyed on measured volume.
    sc = _volume_sc({"peak": 8257552, "nz_above_cap": 2302848,
                     "content_total": 4400000})
    score.score_sidecar(sc)
    assert sc["gate"] == "G3 memory: aram content > 2x DC capacity", sc["gate"]

def test_aram_no_content_total_falls_back_to_address():
    # Pre-v7 sidecar: no content_total -> the address keeps gating (legacy
    # message says "peak"). Volume <= address, so this only under-scores.
    sc = _volume_sc({"peak": 8257552, "nz_above_cap": 1000})
    score.score_sidecar(sc)
    assert sc["gate"] == "G3 memory: aram peak > 2x DC capacity", sc["gate"]

def test_aram_zero_volume_is_a_measurement_not_missing():
    # content_total == 0 must key the axis (u=0 -> 100), NOT fall back to the
    # 8 MiB address — the `is not None` check, not truthiness.
    sc = _volume_sc({"peak": 8 * MB, "nz_above_cap": 0, "content_total": 0})
    score.score_sidecar(sc)
    assert sc["gate"] is None, sc["gate"]
    assert sc["scores"]["memory"] == 100.0, sc["scores"]

def _vram_sc(vram):
    # aram comfortably fits so the memory axis == the vram sub-score path
    sc = _volume_sc({"peak": 1 * MB, "nz_above_cap": 0})
    sc["set"] = "synth-vram"
    sc["memory"]["vram"] = vram
    return sc

def test_vram_fb_masked_volume_scores():
    # chocomk shape (spec motivating case): raw peak 13.5 MB (address-u 1.61,
    # sub 25.6) but only ~2 MB of non-FB content. Volume keying: fit =
    # 2,000,000 + 2*614,400 = 3,228,800 -> u 0.38 -> sub 100.
    sc = _vram_sc({"peak": 13496860, "nz_above_cap": 3156395,
                   "content_total": 2000000, "fb_bytes": 614400})
    score.score_sidecar(sc)
    assert sc["gate"] is None, sc["gate"]
    assert sc["scores"]["memory"] == 100.0, sc["scores"]

def test_vram_fb_budget_is_double():
    # Pins the flat 2x multiplier (§6 ruling 2): content 5,800,000 + 2*614,400
    # = 7,028,800 -> u 0.8379 -> 97.2. A 1x budget would give u 0.7647 -> 100.
    sc = _vram_sc({"peak": 8 * MB, "nz_above_cap": 0,
                   "content_total": 5800000, "fb_bytes": 614400})
    score.score_sidecar(sc)
    assert sc["scores"]["memory"] == 97.2, sc["scores"]

def test_vram_volume_overflow_parks_with_content_message():
    # Genuinely unfittable texture volume: 16 MiB + 1.2 MB FB budget -> u 2.07
    # -> park, and the message says "content" (the gate keyed on volume).
    sc = _vram_sc({"peak": 16 * MB, "nz_above_cap": 8 * MB,
                   "content_total": 16 * MB, "fb_bytes": 614400})
    score.score_sidecar(sc)
    assert sc["gate"] == "G3 memory: vram content > 2x DC capacity", sc["gate"]

def test_vram_no_content_falls_back_to_address():
    # Pre-v8 sidecar (chocomk's committed shape): no content keys -> raw peak
    # keys the axis exactly as today (sub 25.6). Fallback under-scores.
    sc = _vram_sc({"peak": 13496860, "nz_above_cap": 3156395})
    score.score_sidecar(sc)
    assert sc["gate"] is None, sc["gate"]
    assert sc["scores"]["memory"] == 25.6, sc["scores"]

def test_vram_zero_volume_is_a_measurement_not_missing():
    # content_total == 0 with fb_bytes == 0 must key the axis (u=0 -> 100),
    # NOT fall back to the 13.5 MB address — `is not None`, not truthiness.
    sc = _vram_sc({"peak": 13496860, "nz_above_cap": 3156395,
                   "content_total": 0, "fb_bytes": 0})
    score.score_sidecar(sc)
    assert sc["gate"] is None, sc["gate"]
    assert sc["scores"]["memory"] == 100.0, sc["scores"]

if __name__ == "__main__":
    for n, f in sorted(globals().items()):
        if n.startswith("test_") and callable(f):
            f(); print(f"{n} OK")
    print("ALL OK")
