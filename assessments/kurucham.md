# Kurukuru Chameleon (Japan) (GDL-0034) (`kurucham`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G1 broken: no-handoff-120s`** (not a numeric tier) |
| Bottom line | The game never reaches its own code under our instrumented Flycast fork: the zip candidate hangs forever on the NAOMI GD-ROM SYSTEM splash (DIMM firmware boot hang, despite a real ARAM handoff), and the chd-direct candidate falls to the stock Dreamcast BIOS home menu. The dump itself is verified good against MAME's reference SHA1, and upstream Flycast builds are reported to boot it — this is a title-specific incompatibility of our fork's base (`9e882cbd2`), not a bad dump and not a broken game. |
| Assessed | 2026-08-03 · battery v2 · flycast `9e882cbd2` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `kurucham` (covers: no clones — `parent: null` in controls.json) |
| Maker / year | Able (arcade publisher; developer Starfish SD), 2006 |
| Genre / format | Puzzle ★, GD-ROM (GDL-0034) |
| Official DC port | No — platform history is PSP/DS (2006), Switch (2019), PS4/Windows (2020) as *Chameleon: To Dye For!* / *Kameleon*; no Dreamcast release ([Wikipedia](https://en.wikipedia.org/wiki/Chameleon:_To_Dye_For!), accessed 2026-08-02) |
| Community ports | None found — not in the Dreamcast Junkyard Naomi-conversion list ([link](https://www.thedreamcastjunkyard.co.uk/2016/01/guest-article-expanding-dreamcast.html)), no dreamcast-talk/Reddit conversion threads surfaced (searched 2026-08-02). Zophar's Domain hosts a "Sega Dreamcast (DSF)" music rip ([link](https://www.zophar.net/music/sega-dreamcast-dsf/kuru-kuru-chameleon)) — almost certainly a mislabeled Naomi AICA rip (same sound hardware), not evidence of a DC conversion. |
| Representative choice | Only member of its family (MAME parent, no clones) |

## 3. Boot & run evidence

Boots: **no** · handoff: never seen · run 600 s window · rom: `naomi/kurucham/gdl-0034.chd`
Attract/demo reached: n/a — `capture.coverage` left `null`; the three-state taxonomy
(calibration/title/demo) does not apply because the game's own code never executed.
Screenshots (both show the **stock DC BIOS home menu** — Play/File/Music/Settings,
Dreamcast swirl, RTC clock — the kb §4.a fall-to-BIOS signature, not game content):
- `assessments/evidence/kurucham/shot-060s.png` — DC BIOS home menu at t=60 s
- `assessments/evidence/kurucham/shot-121s.png` — DC BIOS home menu at t=121 s, unchanged
Anomalies: the two candidate legs fail *differently* (splash hang vs. fall-to-BIOS) — see Gate.

## Gate

**G1 broken: no-handoff-120s** (`boot.ok = false`, `boot.mame_not_working = false` in the
sidecar — MAME marks the set runnable, so this is not a known-broken title).

Two candidate legs, diagnosed in the main session (2026-08-03):

- **Zip candidate (`naomi/kurucham.zip`):** deterministically hangs on the NAOMI GD-ROM
  SYSTEM splash for the full 600 s window *with* a real ARAM handoff (`ARAMHANDOFF zeroed
  size=800000` in cartlog) and live framebuffer flips — observed on 2 independent runs.
  Battery v2's candidate loop detects this class (`no-render-after-handoff`, fixed in
  commit `61350c8`, kb §4.k) and falls through to the chd.
- **Chd-direct candidate (`naomi/kurucham/gdl-0034.chd`):** falls to the stock DC BIOS
  home menu (kb §4.a signature; screenshots above), **no CARTDMA/ARAMHANDOFF at all**,
  twice (auto-retry included). The sidecar's final failure class comes from this leg.
- **The dump is not the problem:** `chdman verify` passes, and the chd SHA1
  `48a7d20811a6658d749c495db8aa802d1172a8db` exactly matches MAME's `DISK_IMAGE_READONLY`
  reference for gdl-0034 (`../cleopatra/tools/mame/src/mame/sega/naomi.cpp:8851`, pinned
  @59e7c0b). The security PIC `317-5115-jpn.pic` CRC `e5435e85` matches Flycast's
  expectation (`naomi_roms.cpp:5398` in our fork checkout `../cleopatra/tools/flycast-src`).
- **Tooling is not the problem:** the layout (zip + `naomi/kurucham/gdl-0034.chd`) is
  identical to `azumanga`, which reached demo on the same battery. Flycast's
  `gdcartridge.cpp:506-527` shows a failed chd-open would THROW ("Naomi GDROM: Cannot
  open") rather than hang — so on the zip path the disc opened and the DIMM firmware boot
  itself hung. `gdcartridge.cpp:487` carries a TODO on the `netpic` byte that selects the
  DIMM firmware's start sector — a plausible hang mechanism, unconfirmed.
- **Upstream data point:** the libretro Flycast NAOMI compatibility list marks `kurucham`
  OK ([libretro/flycast#136](https://github.com/libretro/flycast/issues/136)) — the game
  has booted on other Flycast builds.

What would unblock it: retest when the instrumented fork rebases onto a newer upstream
Flycast; no per-title work is warranted before that.

## Risks & notes

- **All measurement fields in the sidecar are non-measurements.** Memory peaks,
  streaming counters, and watermarks are all `0` because the game never ran — they are
  not small values, they are absent values. Guts static analysis was skipped
  (`"skipped (--skip-static or no boot)"`). Do not compare this sidecar's numbers with
  scored titles.
- **Controls would be the easy axis if unparked:** `controls.device_class = stick`,
  standard `naomi` INPUT_PORTS (MAME src/mame/sega/naomi.cpp @59e7c0b);
  [arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=kurucham)
  mirrors the 8-way joystick + 6-button JVS standard declaration, 2 players;
  [Wikipedia](https://en.wikipedia.org/wiki/Chameleon:_To_Dye_For!) describes a
  "simple controls" competitive colour-matching puzzle. Maps 1:1 to a DC pad.
- MAME emulates the title as runnable but with "imperfect graphics and sound" flags
  ([arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=kurucham);
  [minimaws](https://arcade.vastheman.com/minimaws/machine/kurucham)) — consistent with
  a quirky title that trips emulator edge cases.
- The console ports (PSP/DS/Switch/PS4/PC) mean the game content itself is well within
  handheld-class budgets — if the fork boot issue clears, this 41.6 MB puzzle title is a
  plausible easy candidate, not a lost cause.
