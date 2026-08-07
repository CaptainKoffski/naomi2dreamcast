#!/usr/bin/env python3
"""Guards against the REQUIREMENTS.md "BIOS noise scored as game usage" mistake.
run_battery refuses to start unless this prints ALL OK — these invariants are the
strict prohibition, not advice. Never weaken a test here to make a run pass:
a failure means the instrumentation regressed (kb §7), not that the test is old."""
import copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import score  # noqa: E402

ASSESS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "assessments"))


def base_sc(**over):
    sc = {
        "set": "synth",
        "boot": {"ok": True, "failure_class": None},
        "memory": {"main": {"dma_high_water": 8 << 20},
                   "vram": {"peak": 6 << 20, "nz_above_cap": 0},
                   "aram": {"peak": 1 << 20, "nz_above_cap": 0}},
        "streaming": {"steady_mb_per_min": 5.0, "reread_ratio": 0.05},
        "guts": {"dat_available": False},
        "controls": {"device_class": "stick"},
        "similarity": {"developer_match": False, "sdk_overlap": "none",
                       "cart_loader_match": False},
    }
    sc.update(over)
    return sc


def test_gd_bios_logo_signature_refuses_to_score():
    """v8 (spec 2026-08-07-vram-fb-masking-design.md ruling 4): post-v5
    handoff gating, the exact 9.4 MB Naomi-logo signature on a BOOTED title
    can only mean pre-VRAMHANDOFF samples leaked into the profile again —
    refuse, same posture as the DMPD canary (was: clamp to cap and score)."""
    sc = base_sc()
    sc["memory"]["vram"] = {"peak": 0x943000, "nz_above_cap": 57048}
    try:
        score.score_sidecar(sc)
    except score.MetricRegression:
        return
    raise AssertionError("BIOS-logo signature was scored instead of refused")


def test_gd_bios_logo_values_on_g1_park_do_not_raise():
    """dragntr3 shape: a G1-parked (never-booted) sidecar legitimately carries
    the logo values — the boot gate precedes the canary, no raise."""
    sc = base_sc()
    sc["boot"] = {"ok": False, "failure_class": "no-render-after-handoff"}
    sc["memory"]["vram"] = {"peak": 0x943000, "nz_above_cap": 57048}
    score.score_sidecar(sc)
    assert sc["gate"] == "G1 broken: no-render-after-handoff", sc["gate"]


def test_signature_requires_exact_match():
    """One byte off the signature = real game content -> normal (penalized)
    scoring through the address fallback, no refusal, no clamp key."""
    sc = base_sc()
    sc["memory"]["vram"] = {"peak": 0x943000, "nz_above_cap": 57049}
    score.score_sidecar(sc)
    assert sc["gate"] is None
    assert sc["scores"]["memory"] < 60.0, sc["scores"]
    assert "vram_bios_noise_excluded" not in sc["scores"]


def test_dmpd_signature_refuses_to_score():
    """aram nz_above_cap == 0x600000 exactly = the DIMM fill counted as usage."""
    sc = base_sc()
    sc["memory"]["aram"] = {"peak": 8 << 20, "nz_above_cap": 0x600000}
    try:
        score.score_sidecar(sc)
    except score.MetricRegression:
        return
    raise AssertionError("DMPD signature was scored instead of refused")


def test_anchor_title_must_never_park():
    """cleoftp/ikaruga run on real DC hardware; a park on them = broken tooling."""
    for anchor, bad in (("cleoftp", {"memory": {"main": {"dma_high_water": 8 << 20},
                                                "vram": {"peak": 6 << 20, "nz_above_cap": 0},
                                                "aram": {"peak": 5 << 20, "nz_above_cap": 3 << 20}}}),
                        ("ikaruga", {"boot": {"ok": False, "failure_class": "no-render-after-handoff"}})):
        sc = base_sc(set=anchor, **bad)
        try:
            score.score_sidecar(sc)
        except score.MetricRegression:
            continue
        raise AssertionError(f"anchor {anchor} parked without raising")


def test_committed_anchor_sidecars_score_clean():
    """The real committed sidecars must stay unparked with sane memory axes."""
    # ikaruga floor recalibrated 20.0 -> 12.5 (2026-08-07): the battery v6 main
    # write-truth metric scores its main axis 12.5 (address-keyed u=1.938 from a
    # high-placed 1.5 MB band; see assessments/ikaruga.md v6 banner). User ruling:
    # keep the address-keyed method for the whole v6 wave; the address-vs-volume
    # question is kb §6-checkpoint scope. The un-parked invariant is unchanged.
    for s, min_mem in (("cleoftp", 80.0), ("ikaruga", 12.5)):
        p = os.path.join(ASSESS, s + ".metrics.json")
        sc = copy.deepcopy(json.load(open(p)))
        score.score_sidecar(sc)
        assert sc["gate"] is None, (s, sc["gate"])
        assert sc["scores"]["memory"] >= min_mem, (s, sc["scores"])


def test_blind_main_shape_never_scores_100():
    """kb §4.v: dma_high_water == 0 with dma_events > 0 = main axis BLIND
    (PIO loader). score.py must drop+flag the region — a fabricated
    main u=0 -> 100 is the gwing2 100-from-nothing hazard."""
    sc = base_sc()
    sc["memory"]["main"] = {"dma_high_water": 0}
    sc["memory"]["vram"] = {"peak": 7 << 20, "nz_above_cap": 0}   # u=0.875
    sc["streaming"]["dma_events"] = 1344
    score.score_sidecar(sc)
    assert sc["scores"]["main_unmeasured"] is True
    assert sc["scores"]["memory"] < 100.0, sc["scores"]


def test_sgtetris_pio_face_stays_measured():
    """kb §4.v RESOLVED regression control: the PIO-loading cart must stay
    measurable. If this committed sidecar's shape degrades (handoff lost,
    trigger wrong, main blind), the PIO handoff trigger has regressed."""
    sc = json.load(open(os.path.join(ASSESS, "sgtetris.metrics.json")))
    assert sc["capture"]["handoff"]["seen"] is True
    assert sc["capture"]["handoff"]["trigger"] == "pio"
    assert sc["memory"]["main"]["peak"] > 0


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(name, "OK")
    print("ALL OK")
