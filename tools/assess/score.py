#!/usr/bin/env python3
"""Deterministic Naomi->DC portability scoring — the ONLY implementation of spec §4
(docs/superpowers/specs/2026-08-02-portability-assessment-design.md).
CLI: score.py <sidecar.json>  — rewrites the sidecar in place with scores/gate."""
import json, math, sys

CAPS = {"main": 16 << 20, "vram": 8 << 20, "aram": 2 << 20}
WEIGHTS = {"memory": 0.40, "streaming": 0.20, "guts": 0.20, "controls": 0.10, "similarity": 0.10}
AXIS_FLOOR = 10.0   # spec §4: axes live in [10,100]; a 0 would annihilate the geometric mean


def _lerp(x, x0, x1, y0, y1):
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def region_score(peak, cap):
    """Spec §4.1 piecewise map. None => gate G3 (u > 2)."""
    u = peak / cap
    if u > 2.0:
        return None
    if u <= 0.80:
        return 100.0
    if u <= 1.00:
        return _lerp(u, 0.80, 1.00, 100.0, 85.0)
    if u <= 1.25:
        return _lerp(u, 1.00, 1.25, 85.0, 40.0)
    return _lerp(u, 1.25, 2.00, 40.0, 10.0)


def memory_axis(peaks):
    """peaks: {'main'|'vram'|'aram': bytes}. Returns (axis, None) or (None, gated_region)."""
    scores = {}
    for region, peak in peaks.items():
        s = region_score(peak, CAPS[region])
        if s is None:
            return None, region
        scores[region] = s
    return max(AXIS_FLOOR, min(scores.values())), None   # min: regions aren't tradeable


def bandwidth_score(mb_per_min):
    b = mb_per_min
    if b <= 6:
        return 100.0
    if b <= 24:
        return _lerp(b, 6, 24, 100.0, 60.0)
    if b <= 60:
        return _lerp(b, 24, 60, 60.0, 20.0)
    return 10.0


def reread_score(r):
    if r <= 0.1:
        return 100.0
    if r <= 0.5:
        return _lerp(r, 0.1, 0.5, 100.0, 50.0)
    return _lerp(min(r, 1.0), 0.5, 1.0, 50.0, 20.0)


def streaming_axis(steady_mb_per_min, reread_ratio):
    return max(AXIS_FLOOR, 0.6 * bandwidth_score(steady_mb_per_min) + 0.4 * reread_score(reread_ratio))


PENALTIES = {"serial": 5, "eeprom_bios": 5, "eeprom_direct": 10, "rtc": 5,
             "network": 25, "code_over_4mb": 5}


def guts_axis(flags, extra_bios_classes=0):
    p = sum(PENALTIES[f] for f in flags)
    p += min(10, 2 * extra_bios_classes)
    return max(AXIS_FLOOR, 100.0 - p)


CONTROLS = {"stick": 100.0, "dc_peripheral": 75.0, "pad_adaptable": 50.0, "awkward": 25.0}


def controls_axis(device_class):
    """None => gate G2 (class not on the ladder = physically unmappable)."""
    return CONTROLS.get(device_class)


def similarity_axis(dev_match, sdk_overlap, cart_loader_match):
    pts = 20 + (30 if dev_match else 0) \
             + {"full": 40, "partial": 20, "none": 0}[sdk_overlap] \
             + (30 if cart_loader_match else 0)
    return float(min(100, pts))


TIERS = [(80, "S"), (60, "A"), (40, "B"), (20, "C")]


def tier(score):
    for lo, t in TIERS:
        if score >= lo:
            return t
    return "D"


def final_score(axes):
    """axes: {name: value | None}; None drops the axis and renormalizes weights (spec §4.3)."""
    used = {k: v for k, v in axes.items() if v is not None}
    wsum = sum(WEIGHTS[k] for k in used)
    s = math.exp(sum(WEIGHTS[k] / wsum * math.log(v) for k, v in used.items()))
    return round(s, 1)


def score_sidecar(sc):
    """Fill sc['scores'] / sc['gate'] from a spec-§5.2 sidecar. Mutates and returns sc."""
    sc["gate"] = None
    sc["scores"] = None
    if not sc["boot"]["ok"]:
        sc["gate"] = "G1 broken: " + (sc["boot"].get("failure_class") or "no boot")
        return sc
    mem, gated = memory_axis({"main": sc["memory"]["main"]["dma_high_water"],
                              "vram": sc["memory"]["vram"]["peak"],
                              "aram": sc["memory"]["aram"]["peak"]})
    if mem is None:
        sc["gate"] = f"G3 memory: {gated} peak > 2x DC capacity"
        return sc
    ctrl = controls_axis(sc["controls"]["device_class"])
    if ctrl is None:
        sc["gate"] = "G2 controls: " + str(sc["controls"]["device_class"])
        return sc
    guts = None
    if sc["guts"]["dat_available"]:
        guts = guts_axis(set(sc["guts"]["flags"]), sc["guts"]["extra_bios_classes"])
    # FIX 2: no post-handoff streaming data (short run) — drop axis, renormalize; short_window flag in sidecar records why
    stream = None if sc["streaming"]["steady_mb_per_min"] is None else \
             streaming_axis(sc["streaming"]["steady_mb_per_min"],
                            sc["streaming"]["reread_ratio"])
    axes = {"memory": mem,
            "streaming": stream,
            "guts": guts,
            "controls": ctrl,
            "similarity": similarity_axis(sc["similarity"]["developer_match"],
                                          sc["similarity"]["sdk_overlap"],
                                          sc["similarity"]["cart_loader_match"])}
    f = final_score(axes)
    sc["scores"] = {k: (round(v, 1) if v is not None else None) for k, v in axes.items()}
    sc["scores"]["final"] = f
    sc["scores"]["tier"] = tier(f)
    return sc


if __name__ == "__main__":
    path = sys.argv[1]
    with open(path) as fh:
        sc = json.load(fh)
    if sc.get("controls", {}).get("device_class") in (None, "review"):
        sys.exit(f"{sc.get('set')}: controls research required — set controls.device_class first")
    sc = score_sidecar(sc)
    with open(path, "w") as fh:
        json.dump(sc, fh, indent=2)
    if sc["gate"]:
        print(sc["set"], "PARKED", sc["gate"])
    else:
        print(sc["set"], sc["scores"]["final"], sc["scores"]["tier"])
