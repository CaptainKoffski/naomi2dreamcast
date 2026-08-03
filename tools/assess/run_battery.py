#!/usr/bin/env python3
"""One-family assessment battery (spec §2). SERIAL ONLY — never run two at once.
Usage: run_battery.py <set> [--secs 600] [--skip-static] [--keep-dat] [--rom PATH]
Env overrides: FLYCAST_BIN, NAOMI_DIR, MAME_NAOMI."""
import glob, json, os, shutil, signal, struct, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import carve_boot, parse_capture, score  # noqa: E402

NAOMI = os.environ.get("NAOMI_DIR", os.path.join(REPO, "naomi"))
CLEO = os.path.normpath(os.path.join(REPO, "..", "cleopatra"))
BIN = os.environ.get("FLYCAST_BIN", os.path.join(
    CLEO, "tools/flycast-src/build/Flycast.app/Contents/MacOS/Flycast"))
ASSESS = os.path.join(REPO, "assessments")
OUT = os.path.join(HERE, "out")
BATTERY_VERSION = "4"  # v4: ARAM rebaseline at ARM reset (BIOS 8MB sound-RAM-test sweep polluted first-DMA baselines: exact-0x600000 cohort) + periodic vblank profile sampling (cart-DMA-only sampling missed post-load steady state: ikaruga false no-render). v3: snapshot-diff instead of guest zeroing + Vulkan build. v2 and v3 sidecars are stale.
HANDOFF_TAGS = (b"ARAMHANDOFF", b"CARTDMA")
# Sets whose disc/feature set is network-bound (netpic/WCCF/satellite — GAME_FORMATS.md
# Completeness section). Drives the guts 'network' penalty (spec §4.3).
# wccf2chk/wccf400j/wccf420e added to match controls_extract.py's HINT_OVERRIDES WCCF list
# (all 12 WCCF sets are network-bound card-reader cabinets, not just the first 9).
NETWORK_SETS = {"wccf116", "wccf1dup", "wccf212e", "wccf234j", "wccf310j", "wccf322e",
                "wccf341j", "wccf331e", "wccf331j", "wccf2chk", "wccf400j", "wccf420e",
                "dragntr", "dragntra", "dragntr2", "dragntr3", "quizqgd"}


def rom_candidates(setname):
    cands = []
    z = os.path.join(NAOMI, setname + ".zip")
    if os.path.isfile(z):
        cands.append(z)
    cands += sorted(glob.glob(os.path.join(NAOMI, setname, "*.chd")))
    return cands


def flycast_commit():
    try:
        return subprocess.run(["git", "-C", os.path.join(CLEO, "tools/flycast-src"),
                               "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
    except OSError:
        return "unknown"


def handoff_seen(logpath):
    try:
        with open(logpath, "rb") as fh:
            data = fh.read()
        return any(t in data for t in HANDOFF_TAGS)
    except OSError:
        return False


# (no-eeprom-180s abort removed 2026-08-03: stdout EEPROM markers proved per-title
# unreliable — three gaps in three weeks of titles (ss2005 saved-eeprom, gunsur2
# Namco header, moeru silent default-MIE path, kb §4.n) and every abort it fired on
# a real game was a false kill. Flake faces burn a full window harmlessly; FIX 3
# no-render + the mandatory representativeness check catch dead runs.)


def capture(setname, rom, secs):
    ev = os.path.join(ASSESS, "evidence", setname)
    raw = os.path.join(ev, "raw")
    os.makedirs(raw, exist_ok=True)
    log = os.path.join(raw, "cartlog.txt")
    shot = os.path.join(raw, "shot.png")
    for p in (log, shot):
        if os.path.exists(p):
            os.remove(p)
    # FIX 3: clean up stale shot-*.png from previous candidate runs
    for stale in glob.glob(os.path.join(ev, "shot-*.png")):
        os.remove(stale)
    # macOS: suppress the "reopen windows?" modal that blocks boot after a killed run
    # (root-caused in ../cleopatra/scripts/capture.sh)
    for k, v in (("ApplePersistenceIgnoreState", "YES"), ("NSQuitAlwaysKeepsWindows", "false")):
        subprocess.run(["defaults", "write", "com.flyinghead.Flycast", k, "-bool", v],
                       check=False, capture_output=True)
    env = dict(os.environ, FLYCAST_CARTLOG=log, FLYCAST_SHOT=shot, FLYCAST_SHOT_EVERY="300")
    so_path = os.path.join(raw, "stdout.log")
    with open(so_path, "wb") as so:
        # vsync off so the emu thread doesn't deadlock unfocused (capture.sh finding)
        p = subprocess.Popen([BIN, "-config", "config:rend.vsync=no", rom],
                             env=env, stdout=so, stderr=subprocess.STDOUT)
    t0 = time.time()
    timeline, next_shot, shots, aborted = [], 60, [], None
    while True:
        time.sleep(10)
        t = round(time.time() - t0, 1)
        size = os.path.getsize(log) if os.path.exists(log) else 0
        timeline.append([t, size])
        if t >= next_shot and p.poll() is None:
            os.kill(p.pid, signal.SIGUSR1)
            time.sleep(1)                       # copy-then-open: fwrite isn't atomic
            if os.path.exists(shot):
                dst = os.path.join(ev, f"shot-{int(t):03d}s.png")
                shutil.copyfile(shot, dst)
                shots.append(os.path.relpath(dst, REPO))
            next_shot += 60
        if p.poll() is not None:
            aborted = "emulator-exited"
            break
        if t >= 120 and not handoff_seen(log):
            aborted = "no-handoff-120s"          # spec §2 early abort
            break
        if t >= secs:
            break
    if p.poll() is None:
        p.terminate()
        try:
            p.wait(5)
        except subprocess.TimeoutExpired:
            p.kill()
    with open(os.path.join(raw, "timeline.json"), "w") as fh:
        json.dump(timeline, fh)
    return log, timeline, shots, aborted


def static_scan(setname, keep_dat):
    de = os.path.join(REPO, "tools", "dat-extract")
    is_gd = bool(glob.glob(os.path.join(NAOMI, setname, "*.chd")) or
                 glob.glob(os.path.join(NAOMI, "*", setname + "*.chd")))
    cmd = ["./chd2dat.sh", setname] if is_gd else ["python3", "cart2dat.py", setname]
    r = subprocess.run(cmd, cwd=de, capture_output=True, text=True)
    dat = os.path.join(de, "out", setname + ".dat")
    if r.returncode != 0 or not os.path.isfile(dat):
        return {"dat_available": False, "error": (r.stdout + r.stderr)[-500:]}
    try:
        stem = os.path.join(OUT, setname)
        os.makedirs(OUT, exist_ok=True)
        with open(dat, "rb") as fh:
            blob, meta = carve_boot.carve(fh.read())
        with open(stem + ".boot.bin", "wb") as fh:
            fh.write(blob)
        guts_json = stem + ".guts.json"
        g = subprocess.run(["sh", os.path.join(HERE, "ghidra", "run_guts.sh"),
                            stem + ".boot.bin", meta["base"], guts_json],
                           capture_output=True, text=True)
        if g.returncode != 0 or not os.path.isfile(guts_json):
            return {"dat_available": False, "error": "ghidra: " + (g.stdout + g.stderr)[-500:]}
        with open(guts_json) as fh:
            guts = json.load(fh)
        guts["dat_available"] = True
        guts["carve_meta"] = meta
        return guts
    except (ValueError, struct.error, OSError, json.JSONDecodeError) as e:
        # degrade-to-no-guts (spec §4.3): a produced-but-odd .dat must not crash the battery
        # and lose the capture (carve_boot.carve raises ValueError; struct.error on a short
        # file; json.JSONDecodeError on a bad guts.json).
        return {"dat_available": False, "error": f"static scan: {e}"}
    finally:
        if not keep_dat:
            for p in (dat, os.path.join(OUT, setname + ".boot.bin")):
                if os.path.exists(p):
                    os.remove(p)                 # SSD hygiene + never keep decrypted dumps


def guts_flags(setname, guts, serial_pokes):
    flags = ["eeprom_bios"]                      # every Naomi game reads settings via BIOS
    if serial_pokes > 0 or guts.get("mmio_refs", {}).get("scif", 0) > 0:
        flags.append("serial")
    if guts.get("mmio_refs", {}).get("rtc", 0) > 0:
        flags.append("rtc")
    if setname in NETWORK_SETS:
        flags.append("network")
    if guts.get("code_bytes", 0) > 4 << 20:
        flags.append("code_over_4mb")
    extra = max(0, sum(1 for v in guts.get("bios_refs", {}).values() if v) - 2)
    return flags, extra


def similarity(row, fmt, guts):
    ref_path = os.path.join(ASSESS, "reference", "similarity-reference.json")
    if not os.path.isfile(ref_path):
        return {"developer_match": False, "sdk_overlap": "none", "cart_loader_match": False,
                "note": "no reference yet (pre-calibration)"}
    with open(ref_path) as fh:
        ref = json.load(fh)
    ours = set(guts.get("sdk_strings", []))
    theirs = set(ref["sdk_strings"])
    overlap = "full" if theirs and theirs <= ours else ("partial" if ours & theirs else "none")
    return {"developer_match": row["maker"] in ref["makers"],
            "sdk_overlap": overlap,
            "cart_loader_match": fmt == ref["format"] and guts.get("dat_available", False)}


def main():
    args = sys.argv[1:]
    setname = args[0]
    secs = int(args[args.index("--secs") + 1]) if "--secs" in args else 600
    skip_static = "--skip-static" in args
    keep_dat = "--keep-dat" in args
    rom = args[args.index("--rom") + 1] if "--rom" in args else None

    with open(os.path.join(OUT, "controls.json")) as fh:
        controls = json.load(fh)
    row = controls[setname]
    cands = [rom] if rom else rom_candidates(setname)
    if not cands:
        sys.exit(f"no rom for {setname} under {NAOMI}")
    if not rom:
        # A bare GD .chd boots as a Dreamcast disc (DC BIOS menu, never Naomi) —
        # flycast needs the companion zip (PIC key + BIOS) and finds the chd itself.
        cands = [c for c in cands if c.endswith(".zip")] or cands
    fmt = "GD-ROM" if any(c.endswith(".chd") for c in rom_candidates(setname)) else "cart"

    log = timeline = shots = None
    aborted, rom_used, best = "no-candidates", None, None
    raw = os.path.join(ASSESS, "evidence", setname, "raw")
    # SSD hygiene: prior families' raw captures are regenerable scratch and grew past
    # 10 GB by family 18 (mamonoro's run died ENOSPC mid-screenshot) — drop every
    # other set's raw dir before capturing
    for other in glob.glob(os.path.join(ASSESS, "evidence", "*", "raw")):
        if other != raw:
            shutil.rmtree(other, ignore_errors=True)
    for stale in glob.glob(os.path.join(raw, "stdout-leg*.log")):
        os.remove(stale)
    leg = 0
    for cand in cands:
        # launch flake faces retried once per candidate: DC BIOS menu (no handoff),
        # GD splash (handoff but no EEPROM init), dynarec-init assert exit
        # (vmem layout luck, driver.cpp:349)
        for attempt in (1, 2):
            leg += 1
            log, timeline, shots, aborted = capture(setname, cand, secs)
            rom_used = cand
            src = os.path.join(raw, "stdout.log")
            if os.path.exists(src):
                shutil.copyfile(src, os.path.join(raw, f"stdout-leg{leg}.log"))
            print(f"leg {leg}: {os.path.basename(cand)} attempt {attempt} -> "
                  f"{aborted or 'ran full window'}", flush=True)
            if aborted not in ("no-handoff-120s", "no-eeprom-180s", "emulator-exited"):
                break
        # FIX 1: guard against missing cartlog (game dies before first probe hit)
        try:
            with open(log) as fh:
                cap = parse_capture.parse(fh.read(), timeline=timeline)
        except FileNotFoundError:
            cap = parse_capture.parse("", timeline=timeline)
            if aborted is None:
                aborted = "no-cartlog"
        # FIX 3: a full-window run whose game never renders (vram write-truth < 64 KiB)
        # is not a boot — kurucham 2026-08-03 runs its whole loop headless (EEPROM init,
        # per-frame FB flips, empty framebuffers; MAME flags it imperfect-gfx). Label it
        # and fall through to the next launch file in case that one renders.
        if aborted is None and not cap["boot_ok"]:
            aborted = "no-render-after-handoff"
        # FIX 4: keep the most informative failed leg for the sidecar — a full-window
        # no-render capture (real measurements, real timeline) must not be overwritten
        # by a later candidate's 120 s launch-flake leg.
        if aborted == "no-render-after-handoff" and best is None:
            for s in shots:      # later legs delete shot-*.png — keep copies in raw/
                p = os.path.join(REPO, s)
                if os.path.exists(p):
                    shutil.copyfile(p, os.path.join(raw, "best-" + os.path.basename(p)))
            best = (log, timeline, shots, aborted, rom_used, cap)
        if aborted is None:
            break
    else:
        if best is not None:
            log, timeline, shots, aborted, rom_used, cap = best
            for s in shots:
                src = os.path.join(raw, "best-" + os.path.basename(s))
                dst = os.path.join(REPO, s)
                if os.path.exists(src) and not os.path.exists(dst):
                    shutil.copyfile(src, dst)

    boot_ok = cap["boot_ok"] and aborted is None
    guts = {"dat_available": False, "error": "skipped (--skip-static or no boot)"}
    if boot_ok and not skip_static:
        guts = static_scan(setname, keep_dat)
    flags, extra = guts_flags(setname, guts, cap["serial_pokes"])

    sc = {
        "set": setname, "title": row["title"], "maker": row["maker"], "year": row["year"],
        "format": fmt, "assessed": time.strftime("%Y-%m-%d"),
        "versions": {"flycast": flycast_commit(), "battery": BATTERY_VERSION,
                     "ghidra": "12.1.2_PUBLIC", "mame_src": "59e7c0b"},
        "params": {"capture_s": secs, "steady_after_s": 120, "shot_interval_s": 60,
                   "boot_timeout_s": 120, "rom_used": os.path.relpath(rom_used, REPO)},
        "boot": {"ok": boot_ok,
                 "failure_class": aborted if not boot_ok else None,
                 "mame_not_working": row["not_working"]},
        "capture": {"handoff": cap["handoff"], "screenshots": shots,
                    # set by the assessing agent from the screenshots (RUNBOOK
                    # representativeness check): "demo" | "title" | "calibration"
                    "coverage": None,
                    "watermarks_info": {r: cap[r]["watermark_max"] for r in ("main", "vram", "aram")}},
        "memory": {"main": {"dma_high_water": cap["main"]["dma_high_water"]},
                   "vram": {"peak": cap["vram"]["peak"], "nz_total": cap["vram"].get("nz_total"),
                            "nz_above_cap": cap["vram"]["nz_above_cap"],
                            "regs_last": cap["vram"]["regs_last"]},
                   "aram": {"peak": cap["aram"]["peak"], "nz_above_cap": cap["aram"]["nz_above_cap"]}},
        "streaming": dict(cap["streaming"]),
        "guts": {**{k: v for k, v in guts.items() if k != "sdk_strings"},
                 "flags": flags, "extra_bios_classes": extra,
                 "sdk_strings": guts.get("sdk_strings", [])},
        "serial_pokes": cap["serial_pokes"],
        "controls": {"device_class": row["device_class_hint"], "input_ports": row["input_ports"],
                     "sources": [f"MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS "
                                 f"'{row['input_ports']}'"]},
        "similarity": similarity(row, fmt, guts),
    }
    if sc["controls"]["device_class"] == "review":
        sc["gate"] = None
        sc["scores"] = None
        verdict = "UNSCORED (controls research required — set device_class, rerun score.py)"
    else:
        score.score_sidecar(sc)
        verdict = (f"PARKED {sc['gate']}" if sc["gate"]
                   else f"{sc['scores']['final']} {sc['scores']['tier']}")
    path = os.path.join(ASSESS, setname + ".metrics.json")
    with open(path, "w") as fh:
        json.dump(sc, fh, indent=2)
    print(f"{setname}: {verdict}  -> {os.path.relpath(path, REPO)}")


if __name__ == "__main__":
    main()
