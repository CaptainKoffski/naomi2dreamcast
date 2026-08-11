# Crackin' DJ Part 2 (Japan) (`crakndj2`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **67.0 (A)** |
| Bottom line | Same story as its predecessor `crackndj` (67.6 A): the bytes fit — VRAM 0.65×, ARAM 0.61×, featherweight 1.5 MB/min streaming — and only main-RAM content overshoots (u 1.073); but the cabinet is the identical twin-motorized-turntable + cross-fader rig on the 837-13938 rotary JVS board, scratching is the game, no DC turntable peripheral exists → `awkward` (25) caps the score. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `crakndj2` (single member — `parent: null` in controls.json; one `ROM_START( crakndj2 )` in naomi.cpp @59e7c0b line 4767). Predecessor "Crackin' DJ" (`crackndj`, 840-0043) is its own family, assessed separately (`assessments/crackndj.md`) |
| Maker / year | Sega, 2001 (GAME line 10999) — developed with Hitmaker ("Created in cooperation with Hitmaker" splash + "© SEGA/Hitmaker. 2000 2001" on title, `evidence/crakndj2/shot-243s.png`) |
| Genre / format | Rhythm (DJ/scratch simulation), **cart** — M2-type 840-0068, `epr-23674` + 20×64 Mb maskroms, key 317-0311-COM (naomi.cpp game list line 284; ROM_START line 4767) |
| Official DC port | No — Guardiana lists the NAOMI arcade release only, no home conversion ([guardiana.net](https://www.guardiana.net/MDG-Database/NAOMI/Crackin'+DJ+Part+2/)); the DC was already end-of-life in 2001 |
| Community ports | None found (searched 2026-08-11: web search for DC port/conversion — Naomi cart title, outside the Atomiswave conversion pipeline). Emulator support only: the Flycast fork's `jvs_837_13938_crackindj` board covers both titles (see §7) |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/crakndj2.zip`
Attract/demo reached: **demo reached** — the attract loop cycles live gameplay demos with
SCORE/GROOVE HUD, twin platters, cross-fader hands and judgment popups (`shot-182s.png`
182 s, "PERFECT!!" visible; `shot-426s.png` 426 s, "PERFECT!!"/"GOOD" over both decks),
"PART 2" title card with copyright line (`shot-243s.png`), low-poly dancer scenes
(`shot-304s.png`) and the Hitmaker splash (121/365/609 s); sidecar
`capture.coverage = "demo"`. No static pre-game screen. "FREE PLAY" overlay = default
EEPROM (fork ships a set-up `crakndj2_eeprom_dump`, §7/§9).
Screenshots: `evidence/crakndj2/shot-060s.png` · `shot-182s.png` · `shot-243s.png` · `shot-304s.png` · `shot-426s.png`
Anomalies: none — single clean leg (battery log: `leg 1: crakndj2.zip attempt 1 -> ran full window`).

## 4. Memory fit (axis: 71.9)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 17,999,858 | 16,777,216 | 1.073 | 71.9 | address peak 31,604,384 (u 1.88, informational) · `dma_high_water` 26,738,688 · `nz_above_cap` 6,720,207 (37% of content sits above the DC 16 MB line) — grep `CARTDMA` in raw log |
| VRAM (FB-masked content volume + 2×framebuffer, `content_total + 2*fb_bytes`) | 5,469,202 | 8,388,608 | 0.652 | 100.0 | `content_total` 4,245,522 + 2×`fb_bytes` 611,840 · `nz_total` 4,835,630 of which `nz_above_cap` 3,218,970 — write FB at `fb_w_sof2=0xc00000` (sidecar `regs_last`) above the DC 8 MB space; volume fits, layout must come down — grep `VRAMPROFILE` |
| ARAM (content volume, fill-excluded, `content_total`) | 1,287,162 | 2,097,152 | 0.614 | 100.0 | address peak 8,257,552 (u 3.94, informational — streaming-buffer placement, see §9) · `nz_above_cap` 108,355 — grep `ARAMPROFILE` |

Watermarks (informational, content-scan — stale-data prone): main 31,604,384 ·
vram 12,824,580 · aram 8,388,608 (the boot-time DIMM "DMPD" fill, kb §7 — not content).
Risk flag: main watermark ≫ content volume — see §9.

## 5. Cart streaming (axis: 97.1)

DMA events 11,207 · total 40.9 MB (42,859,520 B) · unique 34.4 MB (36,072,960 B) ·
re-read ratio 0.1583 · steady-state 1.482 MB/min (`short_window: false`) ·
PIO 12,493,056 B

## 6. Guts (axis: 85.0)

Code 2,490,368 B · functions 1,337 · MMIO refs: scif 2, rtc 4, g2ext 140 ·
BIOS vector refs: none · penalties applied: flags `eeprom_bios`, `serial`, `rtc` (−15).
Cart boot blob carved at base `0x0c020000`, entry `0x0c021000`, header title
`CRACKIN'DJ PART2  ver JAPAN` (sidecar `carve_meta`).
SDK strings: the same in-house streaming-audio DJ engine as `crackndj` —
`[SoundDriver info]` / `[StreamHeader Info]` / `[StreamBuffer Info]` AICA stream
plumbing (`aicasmpl`, `bptrL/R`, per-port cache pointers), `[Rotate info]` (turntable
pos/dir/vel/**rpm**), `[RotarBuffer Info]` / `[FaderBuffer Info]` raw input buffers, a
"Scrach Test" menu — plus a new-for-Part-2 `S3AS_*` song bank (`S3AS_outrun`,
`S3AS_in_chaos`, …) alongside the `S3AM_*`/`S3LM_*` sample banks. Custom I/O handshake
present: `I/O BD IS NOT CONNECTED TO NAOMI BD.` / `R/E CHANNELS %d` spec table /
**"SET-UP THE TURNTABLE AND FADER. WITHOUT SET-UP, THE GAME WILL NOT OPERATE."** —
see §7/§9.

## 7. Controls (axis: 25.0 — `awkward`)

Cabinet: **two motorized vinyl turntables + a cross-fader** (+ start) — the identical
rig as `crackndj`, ruled `awkward` (25) there; the full argument lives in
`assessments/crackndj.md` §7 and applies verbatim. Hardware match verified for Part 2
on both primary sources:
- **MAME** naomi.cpp @59e7c0b: the `crakndj2` game-list entry (line 284, 840-0068C)
  carries the same requirement string as `crackndj` — "requires regular 837-13551 and
  837-13938 rotary JVS boards, **and turntable simulation**" — and the GAME line
  (10999) binds `crakndj2` to the shared `INPUT_PORTS( crackndj )` (lines 1887–1903:
  START1 + `AD_STICK_X` "Fader" on A0; turntables not in MAME's port map).
- **Flycast fork** (ground truth for how the device presents):
  `core/hw/maple/maple_jvs.cpp:527` class `jvs_837_13938_crackindj` is dispatched on
  gameId prefix `CRACKIN'DJ` (lines 1478–1488) — crakndj2's cart header title is
  `CRACKIN'DJ PART2  ver JAPAN` (sidecar `carve_meta`), so both titles hit the same
  branch: left/right platters = encoder ch0/ch2 from mouse relX/relY, motor-driven
  platter spin simulated on output bit 0x10, `mouseGame = true`. The fork also ships a
  Part-2-specific set-up EEPROM (`crakndj2_eeprom_dump`, `naomi_roms_eeprom.h:313`,
  wired at `naomi_roms.cpp:1196,1232`).
- **The binary agrees** (sidecar `sdk_strings`): "SET-UP THE TURNTABLE AND FADER.
  WITHOUT SET-UP, THE GAME WILL NOT OPERATE.", `[Rotate info] rpm`,
  `[FaderBuffer Info]`, `R/E CHANNELS %d` I/O spec check.
Why `awkward` (25), not G2/`pad_adaptable`/`dc_peripheral`: unchanged from `crackndj`
§7 — the signal side is honestly mappable (two relative encoder channels + one analog
axis, driven today by a mouse in the fork), so not G2; but scratching two platters
against motor feedback while cross-fading is continuous two-handed performance the DC
accessory line has no device for. The attract demos are literally hands on decks
(`shot-182s.png`, `shot-426s.png`). Proposed DC mapping (degraded): mouse or analog
stick X/Y = platter L/R scratch, triggers or second axis = cross-fader, Start = start.
Sources (all mirrored in sidecar `controls.sources`): MAME naomi.cpp @59e7c0b
(INPUT_PORTS line 1887; game-list line 284; GAME line 10999); Flycast fork
`maple_jvs.cpp:527,1478–1488` + `naomi_roms_eeprom.h:313`; `assessments/crackndj.md`
§7 (shared ruling); crakndj2 binary strings (sidecar); guardiana.net (no home port).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 71.9^.40 · 97.1^.20 · 85.0^.20 · 25.0^.10 · 40.0^.10 = **67.0 (A)**
Similarity inputs: developer no, SDK overlap partial, loader match no.

## 9. Risks & notes

- **Main RAM is the only real memory work: −1.2 MB.** Content volume 17,999,858 B is
  1.073× the DC's 16 MB (slightly worse than `crackndj`'s 1.046×) — asset trim or
  on-demand loading of the 6.7 MB currently DMA'd above the 16 MB line clears it;
  layout relocation is needed regardless (`nz_above_cap` 6,720,207 B, §4).
- **Same engine as `crackndj` — measurably.** Carved code blob is byte-identical in
  size (2,490,368 B, same base `0x0c020000` / entry `0x0c021000` in both sidecars;
  1,337 vs 1,265 functions, g2ext 140 vs 106), same guts flags, handoff at the same
  20.0 s via PIO, same VRAM `fb_w_sof2=0xc00000` layout. Part 2 is a content refresh
  on the Part-1 engine: memory/ARAM/VRAM numbers land within a few percent
  (main 18.0 vs 17.6 MB; VRAM content 4.25 vs 4.36 MB; ARAM 1.287 vs 1.290 MB).
  Porting work done for one title transfers nearly wholesale to the other.
- **Part 2 streams lighter than Part 1:** 1.48 vs 2.30 MB/min steady-state, re-read
  ratio 0.158 vs 0.310, half the DMA events — despite a bigger 20×64 Mb cart. Even
  less streaming pressure to solve.
- **ARAM address peak 8.26 MB vs content 1.29 MB.** The DJ engine's audio ring
  buffers sit high in the 8 MB Naomi ARAM (§6 `[StreamBuffer Info]` plumbing);
  content fits 0.61× but the buffers must be re-based into 2 MB — placement, not
  volume (OSB position-independence precedent, kb).
- **VRAM write-FB at 0xc00000.** Flip pair partially above the DC 8 MB space
  (`regs_last`); fit is 0.65× — relayout only.
- **The game refuses to run without turntable set-up** — same §6 guard as `crackndj`.
  Our capture ran because the fork emulates the 837-13938 board and ships a set-up
  EEPROM (`crakndj2_eeprom_dump`); a DC port must stub the JVS rotary-board handshake
  and set-up state first, or it sits on the error screen. Verify this path first.
- **Controls are the port's ceiling, not its blocker** — identical verdict to
  `crackndj` §9: all technical work is ordinary; the cabinet cannot be shipped.
- Rendering and EEPROM save must be verified on real DC hardware (working-style
  rule) — all evidence here is Flycast-fork capture.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | 67.0 (A) | First assessment. Hardware verified identical to `crackndj` (MAME line 284 + fork gameId dispatch) → shared `awkward` (25) ruling |
