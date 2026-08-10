# Shootout Pool (`shootopl`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **79.0 (A)** |
| Bottom line | Billiards sim whose content volumes all fit DC caps (main 0.30×, VRAM 0.82×, ARAM 0.38×) with light cart streaming — but the main RAM layout spans nearly the full 32 MB Naomi bank (address u 2.000) so wholesale relocation is required, and the cabinet's dedicated miniature pool-cue controller costs it the controls axis (`pad_adaptable`, 50): the auto `stick` value was wrong, dropping the score from 84.7 S to 79.0 A. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `shootopl` (single member — `parent: null` in controls.json; one `ROM_START( shootopl )` in naomi.cpp @59e7c0b line 6052, no clones. The Prize/Medal sets `shootpl`/`shootplm`/`shootplmp` are a separate redemption-cabinet family, force-hinted `review` — kb §4.g) |
| Maker / year | Sega, 2002 (developed by HI Corp 2nd Development Dept. "team NIGHT FOX", binary `[APPINFO]`, `Build:Apr 20 2002`) |
| Genre / format | Billiards (Sports), **cart** — MAME GAME line 11012: `naomim1` M1 rom board, 840-0098, key `a0f37ca7` (317-0336-COM), `epr-23844.ic11` + 4 MTP maskroms. Arcade DBs ([arcade-history](https://arcade-history.com/?id=4087&n=shootout-pool&page=detail), [Highway Games](https://www.highwaygames.com/arcade-machines/shootout-pool-8742/)) call it "NAOMI GD-ROM" — the MAME ROM definition (primary source) shows a cart; primary outranks (working-style rule 3) |
| Official DC port | No |
| Community ports | None found (searched 2026-08-11: dreamcast-talk, arcade-projects). Only emulator support exists — Flycast carries a dedicated `shootout_inputs` mapping ([GameBrew Flycast Switch page](https://www.gamebrew.org/wiki/Flycast_Switch) lists it among supported exotic-input titles); that is emulation, not a port |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/shootopl.zip`
Attract/demo reached: **demo reached** — the attract loop is live in-engine from the first
shot: how-to-play cue demo with animated aim/spin HUD (`shot-060s.png`, 60 s), VS Computer
ranking boards (`shot-121s.png`), stage-variant demos (`shot-304s.png` disco bar), and a
full attract match with "BREAK SHOT" callout and player portraits (`shot-548s.png`);
sidecar `capture.coverage = "demo"`. No static pre-game screen — all 10 shots have unique
md5s, not the byte-identical EEPROM-prompt class (kb §4.vi). "FREE PLAY" overlay = default
EEPROM.
Screenshots: `evidence/shootopl/shot-060s.png` · `shot-121s.png` · `shot-304s.png` · `shot-548s.png`
Anomalies: none — single clean leg (battery log: `leg 1: shootopl.zip attempt 1 -> ran full window`).

## 4. Memory fit (axis: 98.2)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 5,029,563 | 16,777,216 | 0.300 | 100.0 | address peak 33,550,016 (u **2.000**, informational — nearly the full 32 MB Naomi bank) · `dma_high_water` 30,993,024 · **`nz_above_cap` 3,624,304** (72% of content sits above the DC 16 MB line) — grep `CARTDMA` in raw log |
| VRAM (FB-masked content volume + 2×framebuffer, `content_total + 2*fb_bytes`) | 6,909,166 | 8,388,608 | 0.824 | 98.2 | `content_total` 4,451,566 + 2×`fb_bytes` 1,228,800 · `nz_total` 5,195,746 of which `nz_above_cap` 3,666,207 — framebuffers at `fb_w_sof1=0x800000` / `fb_w_sof2=0xc00000` (sidecar `regs_last`), above the DC 8 MB space; volume fits, layout must be relocated — grep `VRAMPROFILE` |
| ARAM (content volume, fill-excluded, `content_total`) | 805,356 | 2,097,152 | 0.384 | 100.0 | address peak 915,728 (u 0.437) · 0 bytes above cap — grep `ARAMPROFILE` |

Watermarks (informational, content-scan — stale-data prone): main 33,550,016 ·
vram 15,708,160 · aram 8,388,608 (the boot-time DIMM "DMPD" fill, kb §7 — not content).
Risk flag: main watermark ≫ content volume — see §9.

## 5. Cart streaming (axis: 84.0)

DMA events 408 · total 24.7 MB (25,856,000 B) · unique 14.3 MB (14,995,456 B) ·
re-read ratio 0.42 · steady-state 1.896 MB/min (`short_window: false`) ·
PIO 1,049,920 B

## 6. Guts (axis: 85.0)

Code 1,048,576 B · functions 1,945 · MMIO refs: scif 2, rtc 3, g2ext 101 ·
BIOS vector refs: none · penalties applied: flags `eeprom_bios`, `serial`, `rtc` (−15).
Cart boot blob carved at base `0x8c020000`, entry `0x8c021000`, header title
`SHOOTOUT POOL` (sidecar `carve_meta`).
SDK strings: stock Sega Naomi stack — `\sound\Manatee.drv` sound driver + `.mlt`
multi-unit banks, Ninja `.NJ` models / `.pvr` textures, `GDD_*` GD/DIMM library
status tables, SRAM save strings; extensive in-house billiards physics debug
(`pgCalcShotWhiteBall`, ball/cushion energy-conservation errors). Custom I/O board
handshake strings present: `I/O BD IS NOT CONNECTED TO NAOMI BD` /
`COM. ERROR OCCURED BETWEEN NAOMI BD AND I/O BD` — see §7.

## 7. Controls (axis: 50.0 — `pad_adaptable`)

Cabinet: **dedicated miniature physical pool-cue controller on an ergonomic control
unit** — the player strokes a real mini cue to shoot, with spin/masse/jump techniques
set via the unit ("a miniature pool cue and an ergonomically designed control unit",
[Highway Games](https://www.highwaygames.com/arcade-machines/shootout-pool-8742/);
"realistic miniature cue-controller",
[Arcade Database](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=shootopl) and
[arcade-history](https://arcade-history.com/?id=4087&n=shootout-pool&page=detail)).
Dedicated upright, 76×97×203 cm / 124 kg (Highway Games). Binary corroboration: custom
I/O board handshake strings (§6), `Analog:%d, %d, %d`, and MECHANICAL ENGINEER /
ELECTRICAL ENGINEER credits — an electromechanical controller, not a stick panel.
MAME input ports: `naomi` (generic — the cue device is unemulated there; GAME line 11012).
Flycast is the ground truth for how the device presents: `shootout_inputs`
(`core/hw/naomi/naomi_roms_input.h:483`, wired to `shootopl` at `naomi_roms.cpp:449`)
maps it as **two Full analog axes** ("CUE TIP U/D" ch1, "CUE TIP L/R" ch0, both
inverted) plus START/MODE, TOP/VIEW, ZOOM IN/OUT buttons and an emulator-only
"CUE ROLLER" toggle — i.e. the cue reaches the game as plain JVS analog channels, and
the game is already played today on stick/pad mappings under emulation.

Why `pad_adaptable` (50), not `stick` (auto value — wrong: the cabinet has no joystick
panel), not `dc_peripheral` (75 — no DC peripheral reproduces a cue thrust), not
`awkward` (25 — unlike the inunoos treadmill, the physical action is not the game's
content: shot state is low-dimensional aim/spin/power, exactly what every console pool
game drives from a pad; precedent: gunsur2's 3-axis gun → `pad_adaptable`).
Proposed DC mapping: analog stick = cue tip aim/spin point, pull-back-push-forward
stick gesture or analog trigger = cue power, d-pad = zoom, A/Start = mode — the
standard console pool-game control layer. The cue *feel* is unreproducible; that loss
is what 50 encodes.
Sources (all mirrored in sidecar `controls.sources`): MAME naomi.cpp @59e7c0b;
Highway Games; Arcade Database (arcadeitalia); arcade-history.com; Flycast fork
`naomi_roms_input.h:483`.

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 98.2^.40 · 84.0^.20 · 85.0^.20 · 50.0^.10 · 40.0^.10 = **79.0 (A)**
Similarity inputs: developer no, SDK overlap partial, loader match no.

## 9. Risks & notes

- **Main-RAM relocation is the port's core work.** Content is only 5.0 MB (u 0.30)
  but the write-truth address peak is 33,550,016 — u 1.9997 by address, a hair under
  the 2× gate — and 3,624,304 B (72%) of the content sits above the DC's 16 MB line
  (§4). This title is exactly the shikgam2-class case the v9 content re-key exists
  for (score.py comment, spec 2026-08-08-main-content-rekey-design.md): viable by
  volume, address-sparse by layout. Everything above 16 MB must move.
- **VRAM framebuffers above 8 MB.** Flip pair at 0x800000/0xc00000; content+2×FB =
  6.9 MB fits at 0.82× but the FB/texture layout must come down below 8 MB.
- **Custom I/O board handshake.** The binary carries connect/error paths for its
  dedicated I/O BD (§6). Our capture ran the full window under generic JVS emulation,
  so a no-I/O-BD path exists, but a port must verify which path the game takes and
  stub the handshake accordingly.
- **Controls layer is a redesign, not a remap.** The cue device is two analog
  channels (§7), so inputs are technically trivial — but shot-feel tuning (power from
  stick gesture/trigger) decides whether the port is playable. Prototype this first.
- Rendering and the SRAM save path must be verified on real DC hardware
  (working-style rule) — all evidence here is Flycast-fork capture.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | 79.0 (A) | First assessment. Auto controls class `stick` (84.7 S) corrected to `pad_adaptable` after cabinet research — dedicated miniature cue controller |
