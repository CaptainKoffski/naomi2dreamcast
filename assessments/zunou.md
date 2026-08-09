# Touch De Zunou (Japan, Rev A) (840-0166C) (`zunou`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G1 broken: frozen-splash-bad-dump`** (agent override; not a numeric tier) |
| Bottom line | The game boots its own code as far as a static attract card (the "探求力" touch-prompt panel — not the NAOMI splash) and freezes there deterministically: shots 121–609 s are byte-identical (md5 `79dd7b8c`), reproducing the 2026-08-04 run exactly. Prime suspect: the M4 cart's decryption key `317-0435-JPN` is a **BAD_DUMP** in both MAME and Flycast. The touchscreen path is verified innocent (§Gate). Cabinet-controls research (the family's critical question) is recorded below for when a good key lands: the cabinet is a **touchscreen** (837-14672 SH4 sensor board), honest class `dc_peripheral`. |
| Assessed | capture 2026-08-09 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `zunou` (covers: no clones — `parent: null` in controls.json; Rev A, 840-0166C, is the only dumped revision in MAME/Flycast) |
| Maker / year | Sega, 2006. Full JP title: *Zunou Nouryoku Koujou Machine: Touch de Zunou — Tanoshiku check? Soretomo Battle!?* ("Brain-ability improvement machine", [LaunchBox](https://gamesdb.launchbox-app.com/games/details/102498-touch-de-zunou)) |
| Genre / format | Puzzle ★ (touchscreen brain-training minigames), **cart** — M4-type 840-0166C, 2×512 Mb FPRs (`fpr-24338/24339`), board id 5502 (MAME naomi.cpp @59e7c0b lines 697, 6660–6674). NOT GD-ROM — arcadeitalia's "NAOMI GD-ROM System" label is wrong; `GAME_FORMATS.md` correctly says cart |
| Official DC port | No — the official port is Nintendo DS: *Zunou Nouryoku Koujou Machine: Touch de Zunou! DS* (Sega, 2008-01-17; [retrogames.cc](https://www.retrogames.cc/nds-games/zunou-nouryoku-koujou-machine-touch-de-zunoo-ds-japan.html), [romsfun](https://romsfun.com/roms/nintendo-ds/zunou-nouryoku-koujou-machine-touch-de-zunoo-ds.html), [Sega Retro soundtrack page](https://segaretro.org/Touch_de_Zuno_Original_Soundtrack)) |
| Community ports | None found (searched 2026-08-03) — absent from the [Dreamcast Junkyard Naomi-conversion article](https://www.thedreamcastjunkyard.co.uk/2016/01/guest-article-expanding-dreamcast.html); no dreamcast-talk conversion threads surfaced |
| Representative choice | Only member of its family (MAME parent, no clones) |

## 3. Boot & run evidence

Boots: **no** — sidecar `boot.ok = false`, gate `G1 broken: frozen-splash-bad-dump`
(agent override, re-applied after the battery's `boot_ok` heuristic passed it) ·
BIOS handoff at 20.0 s (`trigger=pio`) · run 600 s · rom: `naomi/zunou.zip`
Attract/demo reached: the `calibration | title | demo` taxonomy **does not apply** —
sidecar `capture.coverage = null`. The game executes its own code as far as a static
attract card, then freezes: shots 121–609 s are byte-identical (md5 `79dd7b8c`), the
*same md5 as the 2026-08-04 run* — a fully deterministic freeze.
Screenshots: `evidence/zunou/shot-060s.png` · `evidence/zunou/shot-121s.png` ·
`evidence/zunou/shot-609s.png` (the latter two identical frozen attract card).
Anomalies: the v9 battery scored the title **85.8 S before the screenshot check** — the
kb §4.p `boot_ok` false-positive reproduced; the G1 override was re-applied per the
RUNBOOK representativeness check (kb §8 addendum).

## Gate

**G1 broken: frozen-splash-bad-dump.** Sidecar `assessments/zunou.metrics.json` →
`boot.ok = false`; gate re-applied by agent override on the v9 control re-run
(2026-08-09): the frozen screen is the game's own static attract card ("探求力"
touch-prompt panel), not the NAOMI splash — zunou boots game code and then freezes
deterministically (shots 121–609 s byte-identical, md5 `79dd7b8c`, reproducing the
2026-08-04 run exactly).

**Not the touchscreen's fault.** The fork logs `NAOMI GAME ID [TOUCH DE ZUNO (JAPAN)]`,
which exactly matches the `touchscreen::init()` trigger in Flycast
`core/hw/naomi/naomi_cart.cpp:691` (fork checkout `../cleopatra/tools/flycast-src`) —
the 837-14672 board emulation initializes correctly.

**Prime suspect: bad M4 decryption key.** The security PIC `317-0435-jpn.ic3` (key CRC
`b553d900`) is marked **BAD_DUMP** in both MAME (`src/mame/sega/naomi.cpp:6672`
@59e7c0b) and Flycast (`core/hw/naomi/naomi_roms.cpp:4939`, entry comment
"Touch De Zunou (Rev A) *** BAD DUMP ***"). A wrong M4 key decrypts the game code to
garbage — consistent with booting to a static card and freezing. Corroboration that the
game logic itself is fine: a
[Demul WIP video](https://www.youtube.com/watch?v=OPh_X0JUGC4) shows the game playing —
Demul's key tables/handling differ — which strengthens "bad key in our MAME/Flycast
emulator family" over "undumped or broken game logic".

**What would unblock it:** a good `317-0435-JPN` dump reaching MAME/Flycast, then re-run
the battery.

## Controls (researched — recorded for the unpark)

**The cabinet is a touchscreen; the controls.json `stick` hint is the kb §4.g trap.**
Sidecar `controls.device_class` set to **`dc_peripheral`** (the G1 gate fires first, so
scores stay null either way).

- MAME `src/mame/sega/naomi.cpp` @59e7c0b line 697: `Touch De Zunou (Rev A) 840-0166C …
  requires 837-14672 sensor board (SH4 based)`; lines 6834/6855 identify that board's
  firmware as `// touch screen I/O board, program disassembles as little-endian SH-4`.
  The GAME macro (line 11039) declares generic `naomi` INPUT_PORTS — MAME does not
  emulate zunou's touch board at all (zunou's ROM_START has no ioboard region), which is
  exactly how the generic hint hides real cabinet hardware (kb §4.g).
- Flycast `core/hw/naomi/touchscreen.cpp` @9e882cbd2 lines 35–44: "837-14672
  touchscreen sensor board / used by Manic Panic Ghosts and Touch De Zunou" — a **SCIF
  serial** pipe whose 60 Hz protocol carries two touch points (10-bit x/y + hit/drag
  bits each), sourced from `mapleInputState[i].absPos` + button A (lines 117–146).
- Web: [citylan MAME mirror](https://www.citylan.it/index.php/Touch_De_Zunou_(Japan,_Rev_A))
  quotes the sensor-board requirement;
  [arcadeitalia](http://adb.arcadeitalia.net/?mame=zunou) lists only the generic
  8-way/6-button declaration (mirrors MAME's generic ports — illustrates the trap, not
  evidence of a stick).

**Why `dc_peripheral`, not a G2 `touchscreen` gate:** the entire input surface reduces
to per-player absolute pointer + one press — Flycast's own working emulation performs
precisely this reduction. No unmappable physical transaction exists (no card, printer,
hopper). The official Sega DC mouse (HKT-9700) covers point/press/drag via an on-screen
cursor; 2-player simultaneous play = two mice on two maple ports; the 2008 DS port
proves the design survives on a small pointer device. Caveat: mouse is relative where
the panel is absolute — a port draws a cursor (as mouse-driven emulator play already
does); a pad-driven cursor is the `pad_adaptable` fallback, so the class is comfortably
on-ladder.

## Risks & notes

- **Every measured number in the sidecar is a splash/static-attract artifact, not a game
  measurement** — the v9 run wrote `nz_total` 11,422,679 B / `nz_above_cap` 9,082,662 B
  of main content **on a static screen**: a broken-boot title can out-write real games,
  so the G1-before-scoring discipline matters under v9 content keying too (kb §8
  addendum). None of the sidecar figures may be quoted as game figures.
- **The §6 item 8 firmware question was answered by a sidecar-derived bound instead**:
  zunou boots its own game code (static attract card, not the NAOMI splash), so it is
  NOT a firmware-only control (v9 control re-run finding, kb §8 addendum).
- **SCIF will be load-bearing on the re-run.** The touch board talks over the SH4 SCIF
  serial port, so `score.py`'s `serial` guts penalty will fire on input code that is the
  game's core input path, not netboot/debug residue — a scoring-semantics data point for
  the kb §6 checkpoint when the title unparks.
- Sibling control if the unpark misbehaves: Manic Panic Ghosts / Pokasuka Ghost (2007)
  share the same 837-14672 board and Flycast touchscreen path.
- Rev A is the only dumped revision; there is no original-rev dump to control-test
  against, and the family is a single set.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-03 | PARKED G1 no-render-after-handoff | First park: all shots read as a frozen splash, BAD_DUMP `317-0435-JPN` key identified as prime suspect; same-day fix of the 64 KiB render-threshold false score (37.7 C, never committed to a table; commit `fd5863b`) — kb §4.p |
| v4 | 2026-08-04 | PARKED G1 frozen-splash-bad-dump | Deliberate cart-splash control run for the BIOS-VRAM-signature work: no ausfache cart-logo exclusion exists; the `boot_ok` threshold mis-parked it G3-ARAM, reclassified by the representativeness check (shots 304–609 s md5-identical `79dd7b8c`) — kb §8 |
| v9 | 2026-08-09 | PARKED G1 frozen-splash-bad-dump | §6 item 8 control re-run: `boot_ok` false-positive reproduced (battery scored 85.8 S pre-screenshot-check, same md5 as v4 — deterministic); frozen screen identified as the game's own static attract card, so the firmware bound was derived from sidecars instead; first write-truth main data on a static screen — kb §8 addendum, spec `2026-08-08-main-content-rekey-design.md` |
