# World Kicks (`wldkicks`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **42.6 (B)** |
| Bottom line | Namco's kick-pendulum soccer game is honestly pad-adaptable — the kick sensor is one analog scalar per player, which Namco itself shipped as an "analog button" in the upright PCB version and the Flycast fork already maps to the DC pad's analog trigger (`pad_adaptable`, 50) — but VRAM is the real work: 11.9 MB of FB-masked texture/FB content vs the DC's 8 MB (u 1.42) drags the memory axis to 33.1, and main RAM content sits at 0.99× with 57% of it above the 16 MB line. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `wldkicks` (World, WK2 Ver.A — MAME parent; clones `wldkicksj` WK1 Japan, `wldkicksu` WK3 US, plus upright "PCB" versions `wldkickspj`/`wldkickspw` WKC1/WKC2, naomi.cpp @59e7c0b game list lines 11132–11141; QUEUE family = `wldkicks` alone) |
| Maker / year | Namco, 2000 (naomi.cpp line 11133) |
| Genre / format | Sports (4-player arcade soccer with physical kick sensor), **cart** — M2-type board 25209801, key 317-5040-COM `052e2901` (naomi.cpp ROM_START line 7085), 74.3 MB (GAME_FORMATS.md) |
| Official DC port | No — on the **cancelled-but-unreleased DC ports** list (GAME_FORMATS.md § Partial DC-port notes, line 198: `dygolf / spkrbtl / toyfight / sl2007 / wrungp / wldkicks / …`) |
| Community ports | None found (searched 2026-08-11; Naomi cart title, outside the Atomiswave-conversion pipeline). Emulator support only: the Flycast fork carries a dedicated `jvs_namco_v226` board (§7) |
| Representative choice | MAME parent, newest World revision (WK2 Ver.A) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/wldkicks.zip`
Attract/demo reached: **demo reached** — the attract loop cycles live gameplay demos
("Press button" over a goal-mouth scramble, `shot-060s.png` 60 s), "How to control"
tutorial screens that draw the stick and a foot kicking the physical ball
(`shot-121s.png` "Your character will tackle when you kick the ball on defence";
`shot-548s.png` "Shoot!"), an interactive "Kick the ball at your feet." attract prompt
(`shot-304s.png`), a TOP STRIKERS ranking table (182 s), the Namco splash (365/487 s)
and a stadium ball-juggling intro (`shot-609s.png`); sidecar `capture.coverage = "demo"`.
No static pre-game screen. "Free play" overlay = the fork's shipped free-play flash
(`resources/flash/wldkicks.nvmem.zip`, resources.cmake:9).
Screenshots: `evidence/wldkicks/shot-060s.png` · `shot-121s.png` · `shot-304s.png` · `shot-548s.png` · `shot-609s.png`
Anomalies: none — single clean leg (battery log: `leg 1: wldkicks.zip attempt 1 -> ran full window`).

## 4. Memory fit (axis: 33.1)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 16,645,321 | 16,777,216 | 0.992 | 85.6 | address peak 33,423,328 (u 1.99, informational) · `dma_high_water` 26,226,304 · `nz_above_cap` 9,440,884 (57% of content sits above the DC 16 MB line) — grep `CARTDMA` in raw log |
| VRAM (FB-masked content volume + 2×framebuffer, `content_total + 2*fb_bytes`) | 11,922,343 | 8,388,608 | 1.421 | 33.1 | `content_total` 10,693,543 + 2×`fb_bytes` 614,400 · `nz_total` 11,305,588 of which `nz_above_cap` 6,448,614 — write FB pair at `fb_w_sof1/2=0xc00000` (sidecar `regs_last`) above the DC 8 MB space — grep `VRAMPROFILE` |
| ARAM (content volume, fill-excluded, `content_total`) | 887,589 | 2,097,152 | 0.423 | 100.0 | address peak 3,605,737 (u 1.72, informational) · `nz_above_cap` 884,373 — grep `ARAMPROFILE` |

Watermarks (informational, content-scan — stale-data prone): main 33,423,328 ·
vram 16,451,584 · aram 8,388,608 (the boot-time DIMM "DMPD" fill, kb §7 — not content).
Risk flag: main watermark ≫ content volume — see §9.

## 5. Cart streaming (axis: 47.7)

DMA events 1,188 · total 270.2 MB (283,309,312 B) · unique 68.5 MB (71,851,424 B) ·
re-read ratio 0.7464 · steady-state 27.641 MB/min (`short_window: false`) ·
PIO 1,613,686 B

## 6. Guts (axis: 85.0)

Code 1,572,864 B · functions 3,515 · MMIO refs: scif 1, rtc 2, g2ext 203 ·
BIOS vector refs: none · penalties applied: flags `eeprom_bios`, `serial`, `rtc` (−15).
Cart boot blob carved at base `0x0c020000`, entry `0x0c020000`, header title
`WORLD KICKS` (sidecar `carve_meta`).
SDK strings: Namco in-house stack (`namco ltd.;N'paca`, `<< V226 ROOT MENU >>` dev
menu with per-developer DVLP pages), a full cabinet-link layer (`LINK TRYING:` /
`NODE_SIZE:` / `MASTER NODE DUPLICATION` / `COMM ESTABLISHED AS:` — the 2-cabinet
8-player link, §9), an AICA sound driver with its own error set (`SND:AICA RAM FULL`
etc.), and a very large soccer-physics tuning table — `KICK_POW_BASE/LMT`,
`KICK_WEAK/STRONG BORDER`, `LEVER_DGTL_ON/OFF_LEVEL`, `PAD_ANLG_SW` — direct evidence
the kick is processed as an analog power value with digital thresholds (§7).

## 7. Controls (axis: 50.0 — `pad_adaptable`)

Cabinet: **per-player analog joystick + physical kick sensor** — each of the 4
players has "a soccer ball, mounted to the bottom of the cabinet ... which reacts to
the strength of the player's kick"; stick steers/aims, kicking the ball pad shoots,
passes and tackles ([Highway Games: World Kicks SD](https://www.highwaygames.com/arcade-machines/world-kicks-6168/);
the game's own attract "How to control" screens draw exactly stick + foot-on-ball,
`shot-121s.png` / `shot-548s.png`). 4 players per cabinet, "Link 2 cabinets together
for 8 players" (same source; link strings in §6).
Electrically the kick is **one analog channel per player**: MAME @59e7c0b has no
dedicated wldkicks port map (generic `naomi` INPUT_PORTS, game list lines 11132–11141)
— the Namco JYU I/O board in naomi.cpp belongs to Ninja Assault (line 804), not this
game — but the driver comment on the upright versions is decisive: *"'PCB' means
upright version, **uses analog button on control panel to kick the ball**"* (lines
11140–11141). Namco itself shipped the kick reduced to an analog button.
Flycast fork is the ground truth for how the device presents:
`naomi_roms_input.h:577–613` (`wldkicks_inputs`: STICK L/R + U/D on analog axes 0–7,
one BUTTON, per-player analog **KICK** on axes 8–11; `wldkickspcb_inputs`: CHANGE
button + "BALL" Half axis) and `maple_jvs.cpp` class `jvs_namco_v226` (line 1092,
12 analog channels, dispatched on gameId `"WORLD KICKS"` line 1569): KICK axes 8–11
read `mapleInputState[p].halfAxes[PJTI_R]` — **the DC pad's analog right trigger** —
with `settings.input.fourPlayerGames = true`; the upright board (line 1170) derives
its 6 "Ball button" bits from the same trigger value.
Why `pad_adaptable` (50), not `awkward` (25) like crackndj: the kick is a
low-dimensional scalar (strength), not a continuous two-handed performance — the
vendor's own upright cabinet swapped the pendulum for an analog button, the game
tunes it as `KICK_POW_*` thresholds (§6), and the standard DC controller already has
the matching input (analog trigger). Not `stick` (100): losing the physical kick is
still losing the cabinet's defining novelty and the capture ran on this adapted
mapping, not the pendulum. Proposed DC mapping (per the fork, already proven in
capture): analog stick = player movement/aim, R trigger squeeze = kick with strength,
A = button, 4 pads = 4 players natively.
Sources (all mirrored in sidecar `controls.sources`): MAME naomi.cpp @59e7c0b
(generic INPUT_PORTS + game-list comment lines 11132–11141); Flycast fork
`naomi_roms_input.h:577–613` and `maple_jvs.cpp:1092,1170,1569`;
[Highway Games World Kicks SD](https://www.highwaygames.com/arcade-machines/world-kicks-6168/);
attract "How to control" screenshots `shot-121s.png`/`shot-548s.png`.

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 33.1^.40 · 47.7^.20 · 85.0^.20 · 50.0^.10 · 20.0^.10 = **42.6 (B)**
Similarity inputs: developer no, SDK overlap none, loader match no.

## 9. Risks & notes

- **VRAM is the gating axis: −3.5 MB of content needed.** FB-masked content + double
  framebuffer is 11,922,343 B = 1.42× the DC's 8 MB — this is volume, not placement:
  texture data must actually shrink (compression/down-res/on-demand), on top of the
  mandatory relayout (6.4 MB of writes above the 8 MB line, write-FB pair parked at
  `0xc00000`, §4).
- **Main RAM fits by 132 KB.** Content volume 16,645,321 B = 0.992× — but 9.4 MB of
  it (57%) currently loads above the DC 16 MB line and the write-address peak is
  33.4 MB, so the port needs a full relayout with near-zero headroom; any DC-side
  runtime overhead tips it over. (v1 limitation: CPU-written data above DMA assets
  may be under-captured; here `nz_total` is snapshot-diff write truth.)
- **Heavy cart re-streaming.** 270 MB total over 68.5 MB unique in 600 s (re-read
  0.746, steady 27.6 MB/min, §5): the game re-reads cart assets constantly (likely
  per-team/stadium swaps). A GD-ROM port needs a caching/prefetch plan inside the
  already-full 16 MB, or accepts seek-bound loads.
- **ARAM is trivial but misplaced.** 0.87 MB content (0.42×) placed up to 3.6 MB —
  rebase the banks (OSB position-independence precedent, kb).
- **Cabinet link layer must be stubbed.** `serial` guts flag + the full LINK/NODE/COMM
  string set (§6) is the 2-cabinet 8-player link; a DC port stubs the link handshake
  or it may hang in COMMUNICATION SETUP paths.
- **Kick calibration is a real knob.** The pendulum sensor became a DC analog trigger
  (§7); verify the game's `KICK_POW_BASE/LMT` / `KICK_WEAK/STRONG BORDER` tuning
  against the trigger's 8-bit range and squeeze speed — expect to retune thresholds,
  as the fork's FIXME on the KICK axis hints (`naomi_roms_input.h:594`).
- 4 simultaneous players map natively to the DC's 4 controller ports
  (`fourPlayerGames` in the fork, §7) — no compromise there.
- Rendering, EEPROM save and trigger feel must be verified on real DC hardware
  (working-style rule) — all evidence here is Flycast-fork capture.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | 42.6 (B) | First assessment. Controls researched: kick pendulum = one analog channel per player, vendor-reduced to an analog button in the PCB version, fork maps it to the DC trigger → `pad_adaptable` (50); battery's provisional auto-class `stick` had printed 45.7 |
