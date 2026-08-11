# Virtua Golf / Dynamic Golf (Rev A) (GDS-0009A) (`dygolf`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM parks it: `content_total` = 6,125,377 B of fill-excluded ARAM content, **2.921×** the DC's 2 MiB AICA RAM — inside the formerly empty (1.962, 2.997) scored/parked band tracked for the kb §6 item-1 threshold checkpoint, slotting between asndynmt 2.782 and alpilot 2.958 (4th-lowest parked ARAM u: toyfight 2.035 < tduno2 2.615 < asndynmt 2.782 < **dygolf 2.921** < alpilot 2.958 < takoron 2.997). It is a **near-sole-blocker**: main content u ≈ 1.0012 (20,048 B over the 16 MiB budget) and VRAM fit u ≈ 1.044 — both marginally over their 1× caps but comfortably scoreable, so an ARAM-gate softening would score this title respectably, not poorly. Controls are `dc_peripheral`: the real cab is a **trackball + buttons** panel (2.25" trackball on a dedicated panel I/O PCB), and the official Sega DC mouse reproduces relative ball-roll input directly. Strong unpark pedigree: **Sega itself announced a Dreamcast port of Dynamic Golf and cancelled it** in the DC wind-down ([GameSpot](https://www.gamespot.com/articles/sega-cancels-two-dreamcast-games-in-japan/1100-2781615/)). |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `dygolf` (covers: `dygolfp` "Virtua Golf / Dynamic Golf (prototype)", cart on `naomim2`, MAME GAME line 11064 — parent `dygolf`) |
| Maker / year | Sega, 2001 (GAME line 11160; staff-roll strings in `guts.sdk_strings`: produce Rikiya Nakagawa, direction Kenichi Imaeda) |
| Genre / format | Golf (Sports), **GD-ROM** GDS-0009A, 70.6 MB |
| Official DC port | No — **announced, then cancelled**: Sega cancelled the Dreamcast releases of Alien Front Online (JP) and Dynamic Golf during the DC wind-down ([GameSpot](https://www.gamespot.com/articles/sega-cancels-two-dreamcast-games-in-japan/1100-2781615/); GAME_FORMATS.md cancelled-but-unreleased list) |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | MAME parent, the GD-ROM Rev A release; the only other set is the unreleased cart prototype `dygolfp` |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/dygolf.zip`

Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote
`null`; set here after screenshot review). The attract loop is full 3D gameplay demo
from second one of the window: a player-character demo on a seaside course
(`shot-060s.png`), stroke-play demo holes with the swing/aim UI — on-screen colored
button prompts "ショット方向調整" (shot direction adjust) and CAM markers mirroring the
cab panel (`shot-182s.png`) — a "SCORE RANKING — Stroke Play Mode" leaderboard
(`shot-304s.png`), a club-car cutaway under the DYNAMIC GOLF logo (`shot-426s.png`),
and a 4-player hole-overview (14H, 398 yd, par 4) with per-player score panels
(`shot-609s.png`). FREE PLAY watermark visible throughout — genuine attract gameplay,
not a static pre-game screen.
Screenshots: `evidence/dygolf/shot-060s.png` · `shot-182s.png` · `shot-304s.png` ·
`shot-426s.png` · `shot-609s.png`
Anomalies: none.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 6,125,377 B`
(fill-excluded content volume, kb §6 volume keying) against the DC's 2,097,152 B AICA
RAM → utilization **2.921** — past `region_score()`'s `u > 2.0` gate. Cohort position:
4th-lowest parked ARAM u in the campaign (toyfight 2.035 < tduno2 2.615 < asndynmt
2.782 < **dygolf 2.921** < alpilot 2.958 < takoron 2.997), i.e. another title inside
the formerly empty (1.962, 2.997) scored/parked band tracked for the kb §6 item-1
threshold checkpoint. `nz_above_cap` = 4,263,925 B of content above the cap
(address-keyed placement figure, informational). Address peak is 8,257,552 B (u 3.938)
and the informational content-scan watermark is 8,388,608 B — the full 8 MiB ARAM
touched (stale-data prone; the write-truth content figure above is the scoring one).
`guts.sdk_strings` corroborates a sound-pack loader ("PACKLOAD !!",
"SoundPackFlag : %08X") consistent with large voice/SFX banks.

The other two regions, quoted from the sidecar for context:

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 16,797,264 | 16,777,216 | **1.0012** | `nz_total` — 20,048 B over the 1× cap (would score ≈ 84.8, not gate); `nz_above_cap` (address-placement) 9,895,850 B · `dma_high_water` 29,360,128 B (u 1.750) · write peak 29,326,752 B (u 1.748) |
| VRAM (content volume + 2×fb) | 8,758,363 | 8,388,608 | **1.0441** | `content_total` 7,534,683 + 2×`fb_bytes` (2×611,840, per `score.py`'s `vram_ct + 2*vram_fb` formula) — would score ≈ 77; raw `nz_total` 8,306,726 (u 0.990) · `nz_above_cap` 6,632,053 (address-keyed) |
| ARAM (content volume) | 6,125,377 | 2,097,152 | **2.921** | the gate — see above |

**Near-sole-blocker:** unlike alpilot (main 1.389 / VRAM 1.196), dygolf's main overage
is 0.12% and its VRAM overage 4.4% — an ARAM-gate softening per the kb §6 item-1
checkpoint (the ikaruga official-port 4× sound-trim precedent comfortably covers
2.921×) would move it to a mid-tier score, and the cancelled official DC SKU (§2)
is direct evidence Sega judged the content DC-feasible.

Streaming context: 20,612 DMA events · 103.7 MB total · 36.8 MB unique · re-read ratio
0.6454 · steady-state 7.635 MB/min (`short_window: false`) · `pio_bytes` 1,967,424 B.
Guts: code 1,966,080 B (1.88 MiB) · 1,572 functions · MMIO refs rtc 4 / g2ext 234 /
scif 2 · flags `eeprom_bios`/`serial`/`rtc` · carve title "DYNAMIC GOLF".
Similarity: `developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: true`.

**Controls (on-ladder, does not gate — `dc_peripheral`).** The real cabinet is a
**trackball + buttons** panel, not a stick panel: a 2.25" trackball sits on the control
panel with its own trackball I/O PCB that connects to the JVS I/O
([Worthpoint sold-panel listing "SEGA VIRTUA GOLF CONTROL PANEL W/TRACKBALL & I/O
BOARD BUTTONS & WIRE HARNESS"](https://www.worthpoint.com/worthopedia/sega-virtua-golf-control-panel-306666182);
[Arcade Museum forum](https://forums.arcade-museum.com/threads/sega-naomi-virtua-golf-question.320288/):
the Golf panel "has the trackball and another PCB on it, that connects to the IO board";
[Arcade Otaku forum](https://forum.arcadeotaku.com/viewtopic.php?t=26782): NAOMI →
JVS-JAMMA I/O → VG panel I/O chain). MAME input ports: `naomi` (generic digital set —
the trackball board is unemulated there; GAME line 11160); the Flycast fork likewise
maps only DPAD/START/base buttons (`dygolf_inputs`,
`core/hw/naomi/naomi_roms_input.h:615`, wired at `naomi_roms.cpp:4531,5205`) — so
neither emulator table describes the real device; the physical-panel sources above do.
Why `dc_peripheral` (75): the input surface reduces to relative ball-roll deltas
(direction + velocity = swing aim + power) plus a few buttons, and the official Sega
DC mouse is the same ball-sensor geometry inverted — relative-to-relative, with no
absolute-position caveat (cleaner than the zunou touchscreen→mouse precedent); PC golf
established mouse-swing decades ago (Links "TrueSwing"). Pad fallback: analog-stick
flick swing + face buttons, the standard console-golf layer. Sources mirrored in
sidecar `controls.sources`.

What would unblock it: an ARAM-gate softening per the kb §6 item-1 checkpoint. On
unpark it would score with main ≈ 84.8 / VRAM ≈ 77 region sub-scores and 75-class
controls — a genuine port candidate, backed by Sega's own cancelled DC SKU.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM u 2.921 joins the (1.962, 2.997) band (4th-lowest parked); main 1.0012 / VRAM 1.044 near-fit; cab is trackball+buttons → `dc_peripheral`; official DC port announced then cancelled (GameSpot) |
