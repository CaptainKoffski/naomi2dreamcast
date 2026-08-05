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

if __name__ == "__main__":
    test_parse(); print("test_parse OK")
    test_pre_handoff_vram_noise(); print("test_pre_handoff_vram_noise OK")
    test_no_timeline_no_boot(); print("test_no_timeline_no_boot OK")
    print("ALL OK")
