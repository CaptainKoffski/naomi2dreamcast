# Touch De Zunou (Japan, Rev A) (840-0166C) (`zunou`) — portability assessment

> **Battery v4 control run (2026-08-04): still parked — `G1 broken: frozen-splash-bad-dump`.**
> Run deliberately as the cart-splash control for the BIOS-VRAM-signature work
> (kb §8). Two findings: (1) it did NOT reproduce ausfache's small above-cap VRAM
> remainder, so no cart-logo exclusion exists — ausfache's score stands on its own
> bytes. (2) The frozen splash writes 1.07 MB of VRAM (more than ikaruga's real
> title screen), so the automatic `boot_ok` threshold passed it and mis-parked it
> G3-ARAM; reclassified by the RUNBOOK representativeness check with evidence:
> shots 304s–609s are byte-identical (`md5 79dd7b8c…`, `evidence/zunou/shot-304s.png`
> = `shot-609s.png`) and the 317-0435-JPN key PIC is a BAD_DUMP — the game cannot
> decrypt and freezes. Lesson recorded in kb §8: `vram nz_total` cannot separate a
> frozen splash from a static title; the screenshot-based representativeness check
> is the real gate.

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G1 broken: no-render-after-handoff`** (not a numeric tier) |
| Bottom line | The game's own code never executes under our fork: all 10 battery screenshots are the frozen NAOMI cart splash (first/last MD5-identical), ARAM peak is 49,402 B of dead silence across 600 s, and VRAM nonzero content (242,798 B) is exactly the splash's own footprint. Prime suspect: the M4 cart's decryption key `317-0435-JPN` is a **BAD_DUMP** in both MAME and Flycast — a wrong key decrypts the game code to garbage and the BIOS never leaves the splash. The touchscreen path is verified innocent (§Gate). Cabinet-controls research (the family's critical question) is recorded below for when a good key lands: the cabinet is a **touchscreen** (837-14672 SH4 sensor board), honest class `dc_peripheral`. |
| Assessed | 2026-08-03 · battery v2 · flycast `9e882cbd2` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

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

Boots: **no** — sidecar `boot.ok = false`, `failure_class = "no-render-after-handoff"` ·
BIOS handoff seen at 40.0 s · run 600 s · rom: `naomi/zunou.zip` (single zip leg, full window)
Attract/demo reached: the `calibration | title | demo` taxonomy **does not apply** — the
game never executed; sidecar `capture.coverage = null` stands.
Evidence the game code never ran:
- All 10 screenshots are the same frozen NAOMI cart splash — first and last are
  MD5-identical (`ebaaf1ee5ee46dc98eba39d863749c87`, verified on
  `shot-060s.png` / `shot-606s.png`).
- `memory.aram.peak = 49,402 B` — audio dead silence for 600 s.
- `memory.vram.nz_total = 242,798 B` — exactly the splash's own footprint.
- `streaming.dma_events = 316` (9,425,568 B, zero re-read) — the cart upload, then nothing.
- No game strings anywhere in the capture.
Screenshots kept: `assessments/evidence/zunou/shot-060s.png`,
`assessments/evidence/zunou/shot-606s.png` (identical splash at t=60 s and t=606 s).
Anomalies: an initial battery run **falsely scored this title 37.7 C** — the splash's
~237 KiB of VRAM content passed the old 64 KiB render-threshold in the boot heuristic.
Fixed same day (threshold now 1 MiB, commit `fd5863b`, kb §4.p); the false score was
never committed to any table, so no retraction entry is needed.

## Gate

**G1 broken: no-render-after-handoff.** Sidecar `assessments/zunou.metrics.json` →
`boot.ok = false`, `gate = "G1 broken: no-render-after-handoff"`; evidence in §3.

**Not the touchscreen's fault.** The fork logs `NAOMI GAME ID [TOUCH DE ZUNO (JAPAN)]`,
which exactly matches the `touchscreen::init()` trigger in Flycast
`core/hw/naomi/naomi_cart.cpp:691` (fork checkout `../cleopatra/tools/flycast-src`) —
the 837-14672 board emulation initializes correctly.

**Prime suspect: bad M4 decryption key.** The security PIC `317-0435-jpn.ic3` (key CRC
`b553d900`) is marked **BAD_DUMP** in both MAME (`src/mame/sega/naomi.cpp:6672`
@59e7c0b) and Flycast (`core/hw/naomi/naomi_roms.cpp:4939`, entry comment
"Touch De Zunou (Rev A) *** BAD DUMP ***"). A wrong M4 key decrypts the game code to
garbage, so the BIOS hands off into nothing and the splash stays up — matching every
observation in §3. Corroboration that the game logic itself is fine: a
[Demul WIP video](https://www.youtube.com/watch?v=OPh_X0JUGC4) shows the game playing —
Demul's key tables/handling differ — which strengthens "bad key in our MAME/Flycast
emulator family" over "undumped or broken game logic".

Also informational (kb §4.q, commit `fd5863b`): the M4 cart broke the cart2dat static
scan (`load entry out of file: rom=0x40000000 len=0x380000`) → `guts.dat_available =
false`. For a parked title this is informational only.

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

- **Every measured number in the sidecar is a BIOS/splash artifact, not a game
  measurement** — main DMA high-water 26,723,680 B, VRAM peak 14,423,814 B, etc. must
  not be quoted as game figures; the game code never ran (§3).
- **SCIF will be load-bearing on the re-run.** The touch board talks over the SH4 SCIF
  serial port, so `score.py`'s `serial` guts penalty will fire on input code that is the
  game's core input path, not netboot/debug residue — a scoring-semantics data point for
  the kb §6 checkpoint when the title unparks.
- Sibling control if the unpark misbehaves: Manic Panic Ghosts / Pokasuka Ghost (2007)
  share the same 837-14672 board and Flycast touchscreen path.
- Rev A is the only dumped revision; there is no original-rev dump to control-test
  against, and the family is a single set.
