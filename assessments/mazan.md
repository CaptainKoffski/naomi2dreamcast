# Mazan: Flash of the Blade (World, MAZ2 Ver.A) (`mazan`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 7,303,511 B → utilization **3.483**, well past `region_score()`'s `u > 2.0` gate and squarely inside the parked cluster — between `pokasuka` (3.368) and `sstrkfgt` (3.687) in this campaign's ARAM distribution (`takoron` 2.997, `inunoos` 3.206, `pokasuka` 3.368, `mazan` **3.483**, `sstrkfgt` 3.687), clear of the kb §6 item-9 empty band that only `toyfight` (2.033) occupies. Main RAM clears its own cap under content-volume keying (`nz_total` u ≈ 0.925) but VRAM does not: `content_total` + 2×`fb_bytes` = 9,387,215 B, u ≈ 1.119 — over its 1x line, same as `sstrkfgt`, unlike `toyfight`/`pokasuka` which both cleared VRAM. Controls compound the block rather than help it: the cabinet is a dedicated motion-sword rig with no Dreamcast peripheral equivalent — `controls.device_class = motion_sword`, off-ladder — which would gate G2 on its own if ARAM ever cleared. |
| Assessed | capture 2026-08-10 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `mazan` (covers: clone `mazanj` "Mazan: Flash of the Blade (Japan, MAZ1 Ver.A)", clone `mazanu` "Mazan: Flash of the Blade (US, MAZ3 Ver.A)" — both `parent: "mazan"` in controls.json, region variants of the same ROM content; MAME src/mame/sega/naomi.cpp @59e7c0b GAME lines 11144–11146; `mazan` (World, MAZ2 Ver.A) is `parent: null`/self-keyed, the MAME parent) |
| Maker / year | Namco, 2002 (MAME cart-PCB notes table @59e7c0b ~line 801–802: `317-0266-COM` Naomi, cart code MAZ2) |
| Genre / format | Motion-sword hack-and-slash (samurai swordfighting — QUEUE.md/GAME_FORMATS.md's "Light-gun" queue label is a genre-taxonomy artifact, not accurate; the game is a sword-swinging melee combat title against skeleton/demon enemies with a "Parry & slash" advanced-technique tutorial, confirmed by attract-demo combat HUD footage, §3, and by the ROM's own `SWORD SENSOR`/`SWORD ADJUSTMENT` service-mode strings, Gate section), **cart** — 317-0266-COM, boot ROM + 8×128 Mb mask ROMs, 73.7 MB (GAME_FORMATS.md) |
| Official DC port | No (GAME_FORMATS.md: "No") |
| Community ports | None found (searched 2026-08-10) |
| Representative choice | MAME parent (`mazan`, World MAZ2 Ver.A); family also includes region variants `mazanj` (Japan) and `mazanu` (US) of the same ROM content |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/mazan.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set
here after screenshot review). The full attract loop cycles through narrative sword-lore
cutscenes (twin-blade close-ups with flavor text, `shot-060s.png` "Imbued with the power of
holy light... it counters the power of darkness" and `shot-487s.png` "Despite being forged in
the fires of hell, the blade is as cold as ice"), the "MAZAN Flash of the Blade" title logo
(`shot-121s.png`), **live in-combat HUD footage** — score/life-bar/kill-counter readouts over a
skeletal swordsman enemy (`shot-182s.png`) and clean sword-vs-demon melee footage
(`shot-548s.png`) — plus a "TOP 3 PLAYERS" online high-score leaderboard (`shot-243s.png`), a
story-continuation card (`shot-304s.png`, "the master of Lightbringer... destined to rid the
world of this malignant evil"), a Namco WonderPage online-ranking promo screen
(`shot-426s.png`), and a second combat frame with an "Advanced technique: Parry & slash"
tutorial callout (`shot-609s.png`) — genuine attract-demo gameplay including live combat HUD,
not a frozen frame or idle EEPROM prompt.
Screenshots: `evidence/mazan/shot-060s.png` · `shot-121s.png` · `shot-182s.png` ·
`shot-243s.png` · `shot-548s.png`
Anomalies: none. `shot-304s.png`, `shot-365s.png`, `shot-426s.png`, `shot-487s.png`, and
`shot-609s.png` were curated out as redundant with the kept narrative/title/HUD/leaderboard
shots, same class as the redundant frames trimmed from `sstrkfgt`/`toyfight`/`pokasuka`.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 7,303,511 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.483** — well past `region_score()`'s `u > 2.0` gate, and it slots directly
into the middle of this campaign's parked ARAM distribution: `takoron` 2.997, `inunoos` 3.206,
`pokasuka` 3.368, `mazan` **3.483**, `sstrkfgt` 3.687. This is *not* inside the kb §6 item-9
empty band (scored max `zerogu2` 1.962, parked min `takoron` 2.997 — `toyfight` at 2.033 is the
sole title measured strictly inside it) — `mazan` sits well above, adding another data point to
the already-parked cluster rather than the empty gap. `nz_above_cap` = 5,344,360 B of content
above the cap (address-keyed placement figure, informational). Address peak is 8,257,552 B
(u 3.938, pre-volume-keying read) — the same address-peak figure recorded for `sstrkfgt` and
`toyfight`, consistent with this campaign's known address-keyed ceiling artifact (kb "ARAM
write-truth vs content"), not a mazan-specific anomaly.

The other two regions, quoted from the sidecar for context (ARAM gates first in `score.py`'s
region walk regardless):

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 15,524,171 | 16,777,216 | **0.925** | `nz_total` — clears the 1x cap; `nz_above_cap` (address-placement) 11,335,802 B · `dma_high_water` 33,544,256 B (u 1.999, old address-peak read, just under a round 2× placement) — moot either way, ARAM gates first |
| VRAM (content volume + 2×fb) | 9,387,215 | 8,388,608 | **1.119** | `content_total` 8,158,415 + 2×`fb_bytes` (2×614,400, the standard double-buffered 640×480×2 constant, per `score.py`'s `vram_ct + 2*vram_fb` formula) — **over** the 1x cap, same as `sstrkfgt` (1.107), unlike `toyfight`/`pokasuka` which both cleared VRAM under this keying; raw `nz_total` 9,031,333 (u 1.077) · peak 16,207,872 (u 1.932) · `nz_above_cap` 6,781,681 B (address-keyed) |
| ARAM (content volume) | 7,303,511 | 2,097,152 | **3.483** | the gate — see above |

Streaming context: 3,047 DMA events · 108,889,536 B (103.8 MB) total · 68,565,888 B (65.4 MB)
unique · re-read ratio 0.3703 · steady-state 9.422 MB/min (`short_window: false`) · `pio_bytes`
5,082,352 B.
Guts: code 4,194,304 B (4.0 MiB, exactly at — not over — the 4 MiB `code_over_4mb` threshold;
flag absent from `guts.flags`) · 3,170 functions · MMIO refs rtc 4 / g2ext 196 / scif 8 · flags
`eeprom_bios`/`serial`/`rtc`.
Similarity: `developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: false`.

Evidence: `assessments/mazan.metrics.json` → `memory.aram`; `guts.sdk_strings` shows an
extensive `SND_SEB_*`/`SND_SNGA_*` sound-effect naming table (hundreds of foley/impact/footstep
cues — chop by wood/stone/rope/board/cloth/paper, footsteps on metal/stone/wood/sand/tatami ×4
variants each, blood-splash/drop, sword-sheath/crash/pick, guard impacts by material) consistent
with a large layered SFX bank behind the sword-combat sound design visible in the attract demo.

**Secondary blocker (does not currently gate — G3 fires first — but would gate G2 on its own if
ARAM ever cleared):** the cabinet is a dedicated **motion-sword rig** — a physical katana-shaped
controller tracked by dual sensors for 1:1 sword-swing input, with no Dreamcast peripheral
equivalent (`controls.device_class = motion_sword`, off-ladder → RUNBOOK's off-ladder rule
turns any value outside `{stick, dc_peripheral, pad_adaptable, awkward}` into gate G2,
`score.py:111-113`). Researched (3 sources, all in sidecar `controls.sources`): MAME's own
cart-PCB notes table (src/mame/sega/naomi.cpp @59e7c0b, ~line 801–802) documents the World MAZ2
cart as using "2x Namco FCB JVS I/O (not dumped)" — the driver's `GAME()` line falls back to the
generic digital `INPUT_PORTS_START('naomi')` joystick+buttons set only because the real
sword-sensor I/O boards were never dumped, not because the cabinet is actually a stick+buttons
cabinet; corroborated by [highwaygames.com](https://www.highwaygames.com/arcade-machines/mazan-flash-the-8721/)
(control type "Sword, Motion Sensors": "the machine detects the players movement of the blade
via sensors placed around the frame and relays this information to the game"); and by the
game's own service-mode strings carved from the ROM (`assessments/mazan.metrics.json` →
`guts.sdk_strings`): "SWORD ADJUSTMENT", "SWORD TEST", "SWORD SENSOR1"/"SWORD SENSOR2", "SWORD
HOLDER", "SWORD INITIALIZE MENU", "SENSOR 1: X%4d Y%4d W1=%3d W2=%3d N%1d", "POINT AT THE
YELLOW/RED/BLUE/GREEN MARK" — a dual-sensor sword-pointing calibration menu that only makes
sense for physical motion hardware, not a generic joystick. No DC peripheral (pad, light gun,
fishing-rod controller, maracas) tracks 3-axis sword-swing motion, so `motion_sword` is the
honest raw-hardware label — same off-ladder treatment as `pokasuka`'s touchscreen.

What would unblock it: ARAM content would need to shrink below the 2× cap — `mazan`'s 3.483×
sits mid-pack in the parked cohort (below `sstrkfgt` 3.687×, above `pokasuka` 3.368×),
realistically a large trim to the layered foley/impact SFX bank (hundreds of
`SND_SEB_*`/`SND_SNGA_*` cues per `sdk_strings`). VRAM would also need to come down from its
1.119× line for a full clear, though it does not gate on its own. Even if ARAM cleared, controls
would gate G2 independently (`motion_sword`, off-ladder) — a genuine second blocker, not merely
a penalty like `sstrkfgt`'s `pad_adaptable`.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-10 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — light-gun queue-label cohort (game is actually motion-sword hack-and-slash), fresh v9 capture; controls off-ladder too (`motion_sword`, would gate G2 if ARAM ever cleared) |
