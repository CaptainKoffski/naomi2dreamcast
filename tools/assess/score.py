#!/usr/bin/env python3
"""Deterministic Naomi->DC portability scoring — the ONLY implementation of spec §4
(docs/superpowers/specs/2026-08-02-portability-assessment-design.md).
CLI: score.py <sidecar.json>  — rewrites the sidecar in place with scores/gate."""
import json, math, sys

CAPS = {"main": 16 << 20, "vram": 8 << 20, "aram": 2 << 20}
WEIGHTS = {"memory": 0.40, "streaming": 0.20, "guts": 0.20, "controls": 0.10, "similarity": 0.10}
AXIS_FLOOR = 10.0   # spec §4: axes live in [10,100]; a 0 would annihilate the geometric mean


class MetricRegression(SystemExit):
    """A known instrumentation-artifact signature reappeared, or an anchor title
    parked. Scoring REFUSES to produce a verdict from poisoned measurements —
    REQUIREMENTS.md ('rendered by Naomi BIOS and not the game itself... just
    noise. We need to avoid it during data collection or data assessment phase')
    and docs/kb/assessment-tooling.md §7."""


# VRAM structures drawn by the Naomi BIOS, not the game — identified by an EXACT
# (peak, nz_above_cap) pair. Proof: dragntr3 never boots past the GD-ROM splash
# yet reports values byte-identical to booted GD titles (cleoftp/moeru/ikaruga/
# tetkiwam, 2026-08-04). This is REQUIREMENTS.md's "9.4 mb during the Naomi logo
# show time" caveat: 0x943000 == 9,711,616 == 9.4 MB. When a sidecar matches, the
# game's own VRAM content is proven <= cap (the entire above-cap diff IS the
# logo), so the scored peak clamps to the cap (conservative: u=1.0 floor 85).
BIOS_VRAM_SIGNATURES = {
    (0x943000, 57048): "GD-ROM BIOS logo (control: dragntr3 splash-only run, identical values)",
}

# The GD DIMM firmware's "DMPD" ARAM sweep counted as usage: every byte in
# [2 MB, 8 MB) differing. The v4 content metric excludes it; this exact value
# reappearing means the content metric regressed (kb §7 canary).
ARAM_DMPD_ABOVE_CAP = 0x600000

# Titles that verifiably ran on real DC hardware (cleoftp: the ../cleopatra fan
# port this whole project is calibrated against; ikaruga: official 2002 DC
# release). A park on one of these is impossible-by-evidence — it means the
# instrumentation or harness broke, never the game. Refuse to write the verdict.
DC_SHIPPED_ANCHORS = {"cleoftp", "ikaruga"}


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


def _check_anchor(sc):
    if sc["gate"] and sc["set"] in DC_SHIPPED_ANCHORS:
        raise MetricRegression(
            f"METRIC REGRESSION: anchor title '{sc['set']}' parked ({sc['gate']}) — "
            f"this game verifiably runs on real DC hardware, so the measurement or "
            f"harness is broken, not the game. No verdict written. Diagnose the "
            f"instrumentation first (kb §7).")


def score_sidecar(sc):
    """Fill sc['scores'] / sc['gate'] from a spec-§5.2 sidecar. Mutates and returns sc.
    Raises MetricRegression instead of writing a verdict from poisoned measurements."""
    sc["gate"] = None
    sc["scores"] = None
    if sc["memory"]["aram"].get("nz_above_cap") == ARAM_DMPD_ABOVE_CAP:
        raise MetricRegression(
            f"METRIC REGRESSION: '{sc['set']}' aram nz_above_cap == 0x600000 exactly — "
            f"the DIMM 'DMPD' fill signature. The ARAM content metric has regressed "
            f"(kb §7); refusing to score.")
    if not sc["boot"]["ok"]:
        sc["gate"] = "G1 broken: " + (sc["boot"].get("failure_class") or "no boot")
        _check_anchor(sc)
        return sc
    vram_peak = sc["memory"]["vram"]["peak"]
    bios_noise = BIOS_VRAM_SIGNATURES.get((vram_peak, sc["memory"]["vram"].get("nz_above_cap")))
    if bios_noise is not None:
        vram_peak = min(vram_peak, CAPS["vram"])
    # v6: prefer the write-truth peak (MAINPROFILE snapshot+diff); legacy
    # pre-v6 sidecars fall back to the CARTDMA-dest high-water. A booted title
    # with NEITHER measured is a blind metric (PIO loader — gwing2, kb §4.v),
    # not a zero-footprint game: drop the region from the min() (spec §4.3
    # renormalize precedent) and flag it — u=0 must never fabricate a 100.
    main_peak = sc["memory"]["main"].get("peak") or sc["memory"]["main"]["dma_high_water"]
    # §6 checkpoint ruling (2026-08-07, spec 2026-08-07-aram-gate-volume-design.md):
    # ARAM keys on compacted content VOLUME — OSB banks are position-independent
    # (azumanga live verification), so the high-water ADDRESS is a porting
    # artifact. content_total <= content_high + 1 always, so the address fallback
    # for pre-v7 sidecars can only under-score, never over-score.
    aram_ct = sc["memory"]["aram"].get("content_total")
    aram_fit = aram_ct if aram_ct is not None else sc["memory"]["aram"]["peak"]
    peaks = {"vram": vram_peak, "aram": aram_fit}
    if main_peak:
        peaks["main"] = main_peak
    mem, gated = memory_axis(peaks)
    if mem is None:
        metric = "content" if (gated == "aram" and aram_ct is not None) else "peak"
        sc["gate"] = f"G3 memory: {gated} {metric} > 2x DC capacity"
        _check_anchor(sc)
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
    if not main_peak:
        sc["scores"]["main_unmeasured"] = True
    if bios_noise is not None:
        sc["scores"]["vram_bios_noise_excluded"] = bios_noise
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
