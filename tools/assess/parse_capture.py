#!/usr/bin/env python3
"""Instrumented-Flycast cartlog -> metrics fragment (JSON on stdout).
Regexes adapted from ../cleopatra/scripts/parse_cart_log.py (the Phase 2/3 parser).
The cartlog has no timestamps; time comes from the orchestrator's timeline file
([[t_seconds, log_byte_size], ...] sampled every ~10 s) via byte-offset lookup.
Usage: parse_capture.py <cartlog> [--timeline timeline.json] [--handoff-window 120]"""
import bisect, json, re, sys

MAIN_LO, MAIN_HI = 0x0c000000, 0x0e000000    # Naomi main-RAM physical window
_DMA = re.compile(r"^CARTDMA src=([0-9a-f]+) dest=([0-9a-f]+) len=([0-9a-f]+)", re.I)
_WM = re.compile(r"^WATERMARK region=(\w+) used=([0-9a-f]+) size=([0-9a-f]+)", re.I)
_APROF = re.compile(r"^ARAMPROFILE high=([0-9a-f]+) nz=[0-9a-f]+ nz_below2m=[0-9a-f]+ nz_above2m=([0-9a-f]+)", re.I)
_VPROF = re.compile(r"^VRAMPROFILE high=([0-9a-f]+) nz=([0-9a-f]+) nz_below8m=([0-9a-f]+) nz_above8m=([0-9a-f]+)", re.I)
_VREGS = re.compile(r"^VRAMREGS (.+)$")


def parse(text, timeline=None, handoff_window=120):
    ts = [t for t, _ in timeline] if timeline else []
    offs = [o for _, o in timeline] if timeline else []

    def t_of(byte_off):
        if not offs:
            return None
        i = bisect.bisect_left(offs, byte_off)
        return ts[i] if i < len(ts) else ts[-1]

    pos = 0
    handoff = {"seen": False, "t": None, "aram_zeroed": False, "vram_zeroed": False}
    wm = {}
    vram = {"peak": 0, "nz_total": 0, "nz_above_cap": 0, "nz_below_max": 0, "regs_last": ""}
    aram = {"peak": 0, "nz_above_cap": 0}
    dmas = []           # (t, src, dest, length)
    serial = 0
    for line in text.splitlines(keepends=True):
        end = pos + len(line)
        s = line.rstrip("\n")
        m = _DMA.match(s)
        if m:
            src, dest, length = (int(g, 16) for g in m.groups())
            if not handoff["seen"]:
                handoff["seen"] = True
                handoff["t"] = t_of(end)
            dmas.append((t_of(end), src, dest, length))
        elif s.startswith("ARAMHANDOFF"):
            handoff["aram_zeroed"] = True
        elif s.startswith("VRAMHANDOFF"):
            handoff["vram_zeroed"] = True
        elif s.startswith("SERIALPOKE"):
            serial += 1
        else:
            m = _WM.match(s)
            if m:
                wm[m.group(1)] = max(wm.get(m.group(1), 0), int(m.group(2), 16))
            else:
                m = _APROF.match(s)
                if m:
                    aram["peak"] = max(aram["peak"], int(m.group(1), 16))
                    aram["nz_above_cap"] = max(aram["nz_above_cap"], int(m.group(2), 16))
                else:
                    m = _VPROF.match(s)
                    if m:
                        vram["peak"] = max(vram["peak"], int(m.group(1), 16))
                        vram["nz_total"] = max(vram["nz_total"], int(m.group(2), 16))
                        vram["nz_below_max"] = max(vram["nz_below_max"], int(m.group(3), 16))
                        vram["nz_above_cap"] = max(vram["nz_above_cap"], int(m.group(4), 16))
                    else:
                        m = _VREGS.match(s)
                        if m:
                            vram["regs_last"] = m.group(1)
        pos = end

    main_hw = max((dest + n - MAIN_LO for _, _, dest, n in dmas if MAIN_LO <= dest < MAIN_HI),
                  default=0)
    total = sum(n for _, _, _, n in dmas)
    seen, unique = set(), 0
    for _, src, _, n in dmas:
        if (src, n) not in seen:            # ponytail: overlap-blind unique sum; exact interval
            seen.add((src, n))              # union not needed at MB/min granularity
            unique += n
    reread = (total - unique) / total if total else 0.0

    steady, short_window = None, True
    if handoff["t"] is not None and ts:
        w0 = handoff["t"] + handoff_window
        dur = ts[-1] - w0
        if dur >= 60:
            in_w = sum(n for t, _, _, n in dmas if t is not None and t >= w0)
            steady = round(in_w / (1 << 20) / (dur / 60.0), 3)
            short_window = False
        elif ts[-1] > handoff["t"]:
            # run too short for a clean window: fall back to whole post-handoff rate, flagged
            dur = ts[-1] - handoff["t"]
            in_w = sum(n for t, _, _, n in dmas if t is not None and t >= handoff["t"])
            steady = round(in_w / (1 << 20) / (dur / 60.0), 3)

    return {
        "handoff": handoff,
        "main": {"dma_high_water": main_hw, "watermark_max": wm.get("main", 0)},
        "vram": {"peak": vram["peak"], "nz_total": vram["nz_total"],
                 "nz_above_cap": vram["nz_above_cap"],
                 "watermark_max": wm.get("vram", 0), "regs_last": vram["regs_last"]},
        "aram": {"peak": aram["peak"], "nz_above_cap": aram["nz_above_cap"],
                 "watermark_max": wm.get("aram", 0)},
        "streaming": {"dma_events": len(dmas), "total_bytes": total, "unique_bytes": unique,
                      "reread_ratio": round(reread, 4), "steady_mb_per_min": steady,
                      "short_window": short_window},
        "serial_pokes": serial,
        # total nz, not nz_below8m: CPU-framebuffer 2D titles (kurucham) draw above
        # the 8 MB line and are invisible to a below-8m check. Threshold 1 MiB: the
        # bare NAOMI cart splash writes ~237 KiB (zunou false-positive, kb §4.p);
        # every real boot observed writes >=2.29 MiB (tetkiwam, the smallest)
        "boot_ok": bool(handoff["seen"] and vram["nz_total"] >= 0x100000),
    }


if __name__ == "__main__":
    args = sys.argv[1:]
    tl = None
    if "--timeline" in args:
        i = args.index("--timeline")
        with open(args[i + 1]) as fh:
            tl = json.load(fh)
        del args[i:i + 2]
    with open(args[0]) as fh:
        print(json.dumps(parse(fh.read(), timeline=tl), indent=2))
