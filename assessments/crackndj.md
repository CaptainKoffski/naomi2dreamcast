# Crackin' DJ (`crackndj`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **67.6 (A)** |
| Bottom line | The bytes fit the DC easily (VRAM 0.67×, ARAM 0.61×, light 2.3 MB/min streaming) and only main RAM content slightly overshoots (u 1.046) — but the cabinet is two motorized turntables + a cross-fader driven through a dedicated 837-13938 rotary-encoder JVS board, and the scratching IS the game: no DC turntable peripheral ever existed, so controls land on the ladder's bottom rung (`awkward`, 25) and cap the score. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `crackndj` (single member — `parent: null` in controls.json; one `ROM_START( crackndj )` in naomi.cpp @59e7c0b line 4746). "Crackin' DJ Part 2" (`crakndj2`, 2001, 840-0068) is its own MAME parent and its own QUEUE family — not covered here |
| Maker / year | Sega, 2000 (GAME line 10986) — developed by Hitmaker ("Created in cooperation with Hitmaker" splash, `evidence/crackndj/shot-060s.png` header URL hitmaker.co.jp; Hitmaker splash seen at 304 s during capture) |
| Genre / format | Rhythm (DJ/scratch simulation), **cart** — M2-type 840-0043, `epr-23450` + 10×128 Mb maskroms, key 317-0288-COM (naomi.cpp game list line 593; ROM_START line 4746) |
| Official DC port | No — EGM Nov 2000 suggested a home release was coming ([GemuBaka](https://gemubaka.com/2025/08/31/popn-music-on-my-vmu-this-is-doko-demo-popn-music/), citing EGM), but DC support ended first; [sega-naomi.eu](https://www.sega-naomi.eu/software/crackin-dj/) lists home conversions "N/A" |
| Community ports | None found (searched 2026-08-11: dreamcast-talk Atomiswave-conversion scene, retrorgb port list — Naomi cart title, outside the AW conversion pipeline). Emulator support only: the Flycast fork carries a dedicated `jvs_837_13938_crackindj` board (see §7) |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/crackndj.zip`
Attract/demo reached: **demo reached** — the attract loop cycles live gameplay demos with
SCORE/GROOVE HUD and judgment popups (`shot-121s.png` 121 s, score 00102116;
`shot-548s.png` "perfect!!" 22200), a how-to-play tutorial explicitly instructing the
player to spin the turntable ("ターンテーブルを反対に回しきってから" + rotating-vinyl
icon, `shot-426s.png`), title/character scenes (`shot-060s.png`, `shot-609s.png`) and
the Hitmaker splash (304 s); sidecar `capture.coverage = "demo"`. No static pre-game
screen. "FREE PLAY" overlay = default EEPROM.
Screenshots: `evidence/crackndj/shot-060s.png` · `shot-121s.png` · `shot-426s.png` · `shot-548s.png` · `shot-609s.png`
Anomalies: none — single clean leg (battery log: `leg 1: crackndj.zip attempt 1 -> ran full window`).
One mid-run demo (365 s, curated out) renders with a full-screen horizontal-line video
effect; it is scene styling in that song's backdrop, not a capture fault — adjacent
shots are clean.

## 4. Memory fit (axis: 76.7)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 17,551,843 | 16,777,216 | 1.046 | 76.7 | address peak 31,588,060 (u 1.88, informational) · `dma_high_water` 25,165,824 · `nz_above_cap` 5,743,925 (33% of content sits above the DC 16 MB line) — grep `CARTDMA` in raw log |
| VRAM (FB-masked content volume + 2×framebuffer, `content_total + 2*fb_bytes`) | 5,592,730 | 8,388,608 | 0.667 | 100.0 | `content_total` 4,363,930 + 2×`fb_bytes` 614,400 · `nz_total` 4,606,079 of which `nz_above_cap` 3,076,251 — write FB at `fb_w_sof2=0xc00000` (sidecar `regs_last`) above the DC 8 MB space; volume fits, layout must come down — grep `VRAMPROFILE` |
| ARAM (content volume, fill-excluded, `content_total`) | 1,289,724 | 2,097,152 | 0.615 | 100.0 | address peak 8,259,728 (u 3.94, informational — streaming-buffer placement, see §9) · `nz_above_cap` 111,256 — grep `ARAMPROFILE` |

Watermarks (informational, content-scan — stale-data prone): main 31,588,060 ·
vram 13,068,288 · aram 8,388,608 (the boot-time DIMM "DMPD" fill, kb §7 — not content).
Risk flag: main watermark ≫ content volume — see §9.

## 5. Cart streaming (axis: 89.5)

DMA events 22,719 · total 48.0 MB (50,322,176 B) · unique 33.1 MB (34,715,904 B) ·
re-read ratio 0.3101 · steady-state 2.297 MB/min (`short_window: false`) ·
PIO 7,340,224 B

## 6. Guts (axis: 85.0)

Code 2,490,368 B · functions 1,265 · MMIO refs: scif 2, rtc 4, g2ext 106 ·
BIOS vector refs: none · penalties applied: flags `eeprom_bios`, `serial`, `rtc` (−15).
Cart boot blob carved at base `0x0c020000`, entry `0x0c021000`, header title
`CRACKIN'DJ  ver JAPAN` (sidecar `carve_meta`).
SDK strings: an elaborate in-house streaming-audio DJ engine — `[SoundDriver info]` /
`[StreamHeader Info]` / `[StreamBuffer Info]` AICA stream plumbing (`aicasmpl`,
`bptrL/R`, per-port cache pointers), `[Rotate info]` (turntable pos/dir/vel/**rpm**),
`[RotarBuffer Info]` and `[FaderBuffer Info]` raw input buffers, a "Scrach Test" menu
and per-song `S3AS_*`/`S3AM_*`/`S3LM_*` sample banks. Custom I/O handshake present:
`I/O BD IS NOT CONNECTED TO NAOMI BD.` / `R/E CHANNELS %d` spec table / **"SET-UP THE
TURNTABLE AND FADER. WITHOUT SET-UP, THE GAME WILL NOT OPERATE."** — see §7/§9.

## 7. Controls (axis: 25.0 — `awkward`)

Cabinet: **two motorized vinyl turntables + a cross-fader** (+ start). The player
scratches two real platters and cross-fades between them — that action is the entire
game ([sega-naomi.eu](https://www.sega-naomi.eu/software/crackin-dj/): "2 Turntables
and 1 fader"; the game's own attract tutorial orders a platter spin, `shot-426s.png`;
binary `[Rotate info] rpm` / `[FaderBuffer Info]` / "SET-UP THE TURNTABLE AND FADER",
§6).
Electrically: the turntables are rotary-encoder channels on a dedicated **837-13938
"ENCORDER BD"** JVS expansion (MIE 315-6146, daisy-chained via USB cable to the
standard 837-13551 I/O — naomi.cpp @59e7c0b lines 1090–1105: "trackballs and other
rotary type game controls"); game list line 593: "requires regular 837-13551 and
837-13938 rotary JVS boards, **and turntable simulation**". The fader is a plain A/D
channel: MAME's INPUT_PORTS `crackndj` (line 1887) models only START1 + `AD_STICK_X`
"Fader" on A0 — the turntables aren't in MAME's port map at all.
Flycast fork is the ground truth for how the device presents:
`core/hw/maple/maple_jvs.cpp` class `jvs_837_13938_crackindj` (line 527), dispatched
on gameId prefix `CRACKIN'DJ` (lines 1478–1489) — left/right platters = encoder ch0/ch2
fed from **mouse relX/relY**, with the cabinet's motor-driven platter spin simulated
when the game asserts output bit 0x10 (`motorRotation[] -= 10`/read), and
`settings.input.mouseGame = true`. The old libretro core simply couldn't play it
([libretro/flycast#524](https://github.com/libretro/flycast/issues/524): "exotic
analog controls"; notes Demul players used an Xbox 360 pad).

Why `awkward` (25), not off-ladder G2, not `pad_adaptable` (50), not `dc_peripheral`
(75): the signal side is honestly mappable — two relative encoder channels + one
analog axis, demonstrably driven today by a mouse (Flycast) or a pad (Demul) — so the
RUNBOOK's "physically unmappable" G2 criterion (card readers, hoppers) does not apply.
But unlike `shootopl`'s cue (low-dimensional aim/power state → `pad_adaptable`), DJ
scratching is continuous two-handed performance: both platters and the fader are
worked simultaneously, velocity-sensitive, against motor feedback — and the DC has
nothing to map it to: the official accessory line (keyboard, mouse, fishing rod, twin
sticks, light guns, Dreameye…) contains no turntable/DJ controller
([Wikipedia: Dreamcast](https://en.wikipedia.org/wiki/Dreamcast)), and the home
version EGM hinted at died with the platform
([GemuBaka](https://gemubaka.com/2025/08/31/popn-music-on-my-vmu-this-is-doko-demo-popn-music/)).
This is the inunoos rung: the physical action IS the game content, a pad/mouse drives
it only badly. Proposed DC mapping (degraded): mouse or analog stick X/Y = platter
L/R scratch, triggers or second axis = cross-fader, Start = start — playable, not
Crackin' DJ.
Sources (all mirrored in sidecar `controls.sources`): MAME naomi.cpp @59e7c0b
(INPUT_PORTS line 1887; comments lines 593, 1090–1105); Flycast fork
`maple_jvs.cpp:527,1478–1489`; sega-naomi.eu; libretro/flycast#524; Wikipedia
(Dreamcast accessories); GemuBaka/EGM Nov 2000.

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 76.7^.40 · 89.5^.20 · 85.0^.20 · 25.0^.10 · 40.0^.10 = **67.6 (A)**
Similarity inputs: developer no, SDK overlap partial, loader match no.

## 9. Risks & notes

- **Main RAM is the only real memory work: −0.8 MB.** Content volume 17,551,843 B is
  1.046× the DC's 16 MB — a small trim (asset compression or on-demand loading of the
  5.7 MB currently DMA'd above the 16 MB line) clears it; layout relocation is needed
  regardless (`nz_above_cap` 5,743,925 B, §4).
- **ARAM address peak 8.26 MB vs content 1.29 MB.** The DJ engine streams audio through
  ring buffers placed high in the 8 MB Naomi ARAM (§6 `[StreamBuffer Info]` plumbing);
  content fits 0.61× but the streaming buffers must be re-based into 2 MB — buffer
  placement, not volume (OSB position-independence precedent, kb).
- **VRAM write-FB at 0xc00000.** Flip pair partially above the DC 8 MB space
  (`regs_last`); fit is 0.67× — relayout only.
- **The game refuses to run without its turntable hardware set-up** — "SET-UP THE
  TURNTABLE AND FADER. WITHOUT SET-UP, THE GAME WILL NOT OPERATE." (§6) plus the
  I/O-board spec check (`R/E CHANNELS`). Our capture ran the full window because the
  Flycast fork emulates the 837-13938 board and its EEPROM ships set-up
  (`naomi_roms_eeprom.h:301` `crackndj_eeprom_dump`); a DC port must stub the JVS
  rotary-board handshake and the set-up state, or the game will sit in the §6 error
  screen. Verify this path first.
- **Controls are the port's ceiling, not its blocker.** Everything technical is
  ordinary porting work; what cannot be ported is the cabinet. Budget the controls
  layer as a redesign (see §7 mapping) and expect a fundamentally degraded experience.
- Rendering and EEPROM save must be verified on real DC hardware (working-style
  rule) — all evidence here is Flycast-fork capture.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | 67.6 (A) | First assessment. Controls researched: twin motorized turntables + cross-fader via 837-13938 rotary JVS board → `awkward` (25) |
