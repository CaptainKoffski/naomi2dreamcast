#!/usr/bin/env python3
"""Run: python3 tools/assess/tests/test_parse_capture.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import parse_capture

# Synthetic capture: handoff at first CARTDMA; one re-read; one DMA outside main RAM.
LOG = (
    "WATERMARK region=main used=1fff60b size=2000000\n"      # stale-content scan: informational only
    "CARTDMA src=00010000 dest=0c020000 len=100000\n"        # handoff DMA, 1 MiB to main
    "ARAMHANDOFF zeroed size=800000\n"
    "VRAMHANDOFF zeroed size=1000000\n"
    "CARTDMA src=00200000 dest=0cb00000 len=80000\n"         # high-water: 0xb80000 above base
    "CARTDMA src=00200000 dest=0cb00000 len=80000\n"         # exact re-read (0x80000 re-bytes)
    "CARTDMA src=00300000 dest=10000000 len=1000\n"          # not main RAM: streams, no high-water
    "ARAMPROFILE high=200000 nz=1e0000 nz_below2m=1e0000 nz_above2m=0 size=800000\n"
    "VRAMPROFILE high=7cd7d5 nz=400000 nz_below8m=400000 nz_above8m=0 size=1000000\n"
    "VRAMREGS isp_base=0 isp_limit=0 ol_base=0 ol_limit=0 fb_w_sof1=0 fb_w_sof2=0 fb_r_sof1=0\n"
    "SERIALPOKE addr=ffe80000 data=00000041\n"
)
# Timeline: line offsets — first CARTDMA line ends within the first 10s sample.
def offsets():
    total, offs = 0, []
    for i, line in enumerate(LOG.splitlines(keepends=True)):
        total += len(line)
        offs.append(total)
    return offs

def test_parse():
    offs = offsets()
    # samples at t=10 (through line 2: handoff seen), t=200, t=360 (all bytes)
    timeline = [[10.0, offs[1]], [200.0, offs[6]], [360.0, offs[-1]]]
    m = parse_capture.parse(LOG, timeline=timeline)
    assert m["handoff"]["seen"] and m["handoff"]["aram_zeroed"] and m["handoff"]["vram_zeroed"]
    assert m["handoff"]["t"] == 10.0
    assert m["main"]["dma_high_water"] == 0x0cb80000 - 0x0c000000
    assert m["main"]["watermark_max"] == 0x1fff60b
    assert m["vram"]["peak"] == 0x7cd7d5 and m["vram"]["nz_above_cap"] == 0
    assert m["aram"]["peak"] == 0x200000 and m["aram"]["nz_above_cap"] == 0
    st = m["streaming"]
    assert st["dma_events"] == 4 and st["total_bytes"] == 0x100000 + 0x80000 + 0x80000 + 0x1000
    assert st["unique_bytes"] == 0x100000 + 0x80000 + 0x1000
    assert round(st["reread_ratio"], 4) == round(0x80000 / st["total_bytes"], 4)
    # steady window = t >= 10+120=130; only DMAs sampled after that fall in it. Events at
    # offsets <= offs[6] have t<=200... the window exists (360-130=230s >= 60) so not short.
    assert st["short_window"] is False and st["steady_mb_per_min"] is not None
    assert m["serial_pokes"] == 1
    assert m["boot_ok"] is True     # handoff seen + vram nz_below8m >= 0x10000

def test_pre_handoff_vram_noise():
    # v4 hole (ausfache 2026-08-05): an ARM-reset pre-DMA enables profile ticks
    # before the first CARTDMA, and cartlog_vram_profile with a null baseline
    # diffs raw BIOS VRAM vs zero — the cart-BIOS boot frame above 8 MB
    # (high=93e738, nz_above8m=9ed8) then max-merges into the game's peak.
    # Pre-VRAMHANDOFF profile lines are a different measurement: drop them.
    log = (
        "ARAMREBASE armrst size=800000\n"
        "VRAMPROFILE high=93e738 nz=d264 nz_below8m=338c nz_above8m=9ed8 size=1000000\n"
        "CARTDMA src=00010000 dest=0c020000 len=100000\n"
        "ARAMHANDOFF baselined size=800000\n"
        "VRAMHANDOFF baselined size=1000000\n"
        "VRAMPROFILE high=726180 nz=306790 nz_below8m=306790 nz_above8m=0 size=1000000\n"
    )
    m = parse_capture.parse(log)
    assert m["vram"]["peak"] == 0x726180, hex(m["vram"]["peak"])
    assert m["vram"]["nz_above_cap"] == 0

def test_no_timeline_no_boot():
    m = parse_capture.parse("WATERMARK region=main used=5 size=2000000\n")
    assert m["handoff"]["seen"] is False and m["boot_ok"] is False
    assert m["streaming"]["steady_mb_per_min"] is None and m["streaming"]["short_window"] is True

def test_pio_handoff_and_main_profile():
    # v6 PIO face (sgtetris, kb §4.v): no CARTDMA line ever — handoff.seen
    # must latch on the marker lines themselves. Pre-MAINHANDOFF MAINPROFILE
    # samples diff vs a null baseline (a different measurement, kb §9) and
    # must be dropped — the exact pre-VRAMHANDOFF rule, applied to main.
    log = (
        "CARTPIO offset=00000000\n"
        "MAINPROFILE high=1d00000 nz=400000 nz_below16m=300000 nz_above16m=100000 size=2000000\n"
        "ARAMHANDOFF baselined size=800000 trigger=pio\n"
        "VRAMHANDOFF baselined size=1000000 trigger=pio\n"
        "MAINHANDOFF baselined size=2000000 trigger=pio\n"
        "MAINPROFILE high=4c0000 nz=3c0000 nz_below16m=3c0000 nz_above16m=0 size=2000000\n"
        "MAINPROFILE high=980000 nz=700000 nz_below16m=700000 nz_above16m=0 size=2000000\n"
        "VRAMPROFILE high=300000 nz=200000 nz_below8m=200000 nz_above8m=0 size=1000000\n"
        "CARTPIOCNT bytes=2f0000\n"
    )
    m = parse_capture.parse(log)
    assert m["handoff"]["seen"] is True and m["handoff"]["trigger"] == "pio"
    assert m["handoff"]["main_baselined"] is True
    assert m["main"]["peak"] == 0x980000, hex(m["main"]["peak"])
    assert m["main"]["nz_total"] == 0x700000 and m["main"]["nz_above_cap"] == 0
    assert m["main"]["dma_high_water"] == 0
    assert m["streaming"]["pio_bytes"] == 0x2f0000
    assert m["streaming"]["dma_events"] == 0
    assert m["boot_ok"] is True     # vram nz_total 0x200000 >= 0x80000

def test_dma_trigger_and_main_above_cap():
    log = (
        "CARTDMA src=00010000 dest=0c020000 len=100000\n"
        "ARAMHANDOFF baselined size=800000 trigger=dma\n"
        "VRAMHANDOFF baselined size=1000000 trigger=dma\n"
        "MAINHANDOFF baselined size=2000000 trigger=dma\n"
        "MAINPROFILE high=1100000 nz=e00000 nz_below16m=d00000 nz_above16m=100000 size=2000000\n"
    )
    m = parse_capture.parse(log)
    assert m["handoff"]["trigger"] == "dma"
    assert m["main"]["peak"] == 0x1100000 and m["main"]["nz_above_cap"] == 0x100000

def test_aram_content_total_per_sample_max():
    # §6 ruling (spec 2026-08-07-aram-gate-volume-design.md): content_total is
    # the max of PER-SAMPLE below+above totals. max(below)+max(above) across
    # different samples (here 0x1f0000+0x80000=0x270000) is a volume that never
    # existed at once and must NOT be the answer.
    log = (
        "CARTDMA src=00010000 dest=0c020000 len=100000\n"
        "ARAMHANDOFF baselined size=800000 trigger=dma\n"
        "ARAMPROFILE high=400000 nz=200000 nz_below2m=1f0000 nz_above2m=10000"
        " content_high=400000 content_below2m=1f0000 content_above2m=10000 size=800000\n"
        "ARAMPROFILE high=400000 nz=180000 nz_below2m=100000 nz_above2m=80000"
        " content_high=400000 content_below2m=100000 content_above2m=80000 size=800000\n"
    )
    m = parse_capture.parse(log)
    assert m["aram"]["content_total"] == 0x200000, hex(m["aram"]["content_total"])
    assert m["aram"]["peak"] == 0x400000 and m["aram"]["nz_above_cap"] == 0x80000

def test_aram_content_total_legacy_and_rebase():
    # Legacy line (no content_* fields): content_total must stay None, and
    # peak/nz_above_cap keep their raw-diff fallback semantics.
    m = parse_capture.parse(
        "ARAMPROFILE high=200000 nz=1e0000 nz_below2m=1e0000 nz_above2m=0 size=800000\n")
    assert m["aram"]["content_total"] is None
    assert m["aram"]["peak"] == 0x200000
    # ARAMREBASE restarts every running max — content_total included (samples
    # before the last rebase measured BIOS sound-RAM-test residue).
    log = (
        "ARAMPROFILE high=700000 nz=600000 nz_below2m=200000 nz_above2m=400000"
        " content_high=700000 content_below2m=200000 content_above2m=400000 size=800000\n"
        "ARAMREBASE armrst size=800000\n"
        "ARAMPROFILE high=180000 nz=150000 nz_below2m=150000 nz_above2m=0"
        " content_high=180000 content_below2m=150000 content_above2m=0 size=800000\n"
    )
    m = parse_capture.parse(log)
    assert m["aram"]["content_total"] == 0x150000, hex(m["aram"]["content_total"])

def test_vram_content_total_per_sample_max_and_handoff_gate():
    # §6 ruling 2 (spec 2026-08-07-vram-fb-masking-design.md): content_total is
    # the max of PER-SAMPLE below+above totals. max(below)+max(above) across
    # different samples (0x280000+0x200000=0x480000) is a volume that never
    # existed at once and must NOT be the answer. The pre-VRAMHANDOFF sample
    # (vs-null baseline, kb §9) must be ignored — new fields included.
    log = (
        "VRAMPROFILE high=f00000 nz=e00000 nz_below8m=100000 nz_above8m=d00000"
        " content_high=f00000 content_below8m=100000 content_above8m=d00000"
        " fb_bytes=96000 fb_masked_nz=0 size=1000000\n"
        "CARTDMA src=00010000 dest=0c020000 len=100000\n"
        "VRAMHANDOFF baselined size=1000000 trigger=dma\n"
        "VRAMPROFILE high=c00000 nz=400000 nz_below8m=100000 nz_above8m=300000"
        " content_high=7f0000 content_below8m=100000 content_above8m=200000"
        " fb_bytes=96000 fb_masked_nz=100000 size=1000000\n"
        "VRAMPROFILE high=c00000 nz=380000 nz_below8m=280000 nz_above8m=100000"
        " content_high=280000 content_below8m=280000 content_above8m=0"
        " fb_bytes=96000 fb_masked_nz=100000 size=1000000\n"
    )
    m = parse_capture.parse(log)
    assert m["vram"]["content_total"] == 0x300000, hex(m["vram"]["content_total"])
    assert m["vram"]["fb_bytes"] == 0x96000, m["vram"]["fb_bytes"]
    # raw fields keep their independent-max semantics, post-handoff only
    assert m["vram"]["peak"] == 0xc00000 and m["vram"]["nz_above_cap"] == 0x300000

def test_vram_legacy_line_leaves_content_none():
    # v7-format line (no content_* fields): keys stay None so the sidecar
    # omits them (no zero-fill) and the scorer falls back to the address.
    log = (
        "VRAMHANDOFF baselined size=1000000 trigger=dma\n"
        "VRAMPROFILE high=7b0000 nz=200000 nz_below8m=200000 nz_above8m=0 size=1000000\n"
    )
    m = parse_capture.parse(log)
    assert m["vram"]["content_total"] is None and m["vram"]["fb_bytes"] is None
    assert m["vram"]["peak"] == 0x7b0000

if __name__ == "__main__":
    test_parse(); print("test_parse OK")
    test_pre_handoff_vram_noise(); print("test_pre_handoff_vram_noise OK")
    test_no_timeline_no_boot(); print("test_no_timeline_no_boot OK")
    test_pio_handoff_and_main_profile(); print("test_pio_handoff_and_main_profile OK")
    test_dma_trigger_and_main_above_cap(); print("test_dma_trigger_and_main_above_cap OK")
    test_aram_content_total_per_sample_max(); print("test_aram_content_total_per_sample_max OK")
    test_aram_content_total_legacy_and_rebase(); print("test_aram_content_total_legacy_and_rebase OK")
    test_vram_content_total_per_sample_max_and_handoff_gate(); print("test_vram_content_total_per_sample_max_and_handoff_gate OK")
    test_vram_legacy_line_leaves_content_none(); print("test_vram_legacy_line_leaves_content_none OK")
    print("ALL OK")
