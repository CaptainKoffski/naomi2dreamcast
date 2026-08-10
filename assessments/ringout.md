# Ring Out 4x4 (Rev A) (`ringout`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | A heavy sound bank parks it on first assessment: `content_total` = 7,726,701 B of fill-excluded ARAM content, **3.684×** the DC's 2 MiB AICA RAM — second-highest ARAM utilization in the campaign's parked cohort, just 5,772 B under the record holder `sstrkfgt` (3.687). Main RAM is also over its own 1x line under content keying (`nz_total` u ≈ 1.180, no gate), while VRAM clears (u ≈ 0.808). Controls are clean: generic `naomi` 8-way stick + buttons (`controls.device_class = stick`, the ladder's top rung) — ARAM alone decides the park. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `ringout` (covers: MAME clone `ringouto`, the pre-Rev-A original — same 10 `mpr-21761`–`mpr-21770` mask ROMs, only the boot EPR differs (`epr-21779a` vs `epr-21779`); MAME src/mame/sega/naomi.cpp @59e7c0b GAME lines 10943–10944; QUEUE.md family column lists `ringout` alone) |
| Maker / year | Sega, 1999 (GAME line: `/* 0004 */`; ROM_START comment `840-0004 1999 317-0250-COM Naomi`) |
| Genre / format | Vehicle arena battle — "ring out" 4WD sumo: up to four toy-scale RC-style 4x4 trucks shove each other around a walled arena, bumper-punch attacks, 1P–4P (QUEUE genre "?" resolved by attract footage §3: `shot-121s.png` "1Pから4Pまで プレイ可能" / playable 1P to 4P, `shot-182s.png` HOW TO PLAY bumper-punch card; Japan-only release — `guts.carve_meta.title` "RINGOUT 4X4 JAPAN", "THIS GAME IS TO BE USED ONLY IN JAPAN" warning in `guts.sdk_strings`), **cart** — 840-0004, boot ROM + 10×64 Mb, 39.0 MB |
| Official DC port | No (GAME_FORMATS.md: "No") |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | MAME parent (Rev A); sole queue family member — clone `ringouto` is the original revision of the same ROM set, not a distinct release |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/ringout.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set
here after screenshot review). By the first shot the attract loop is already in live demo
gameplay: a four-truck AI match on the timber-floored arena, top-down camera, with FREE PLAY
overlays rotated onto **all four screen edges** — the 1P–4P around-the-screen presentation
(`shot-060s.png`); a match-start close-up with countdown and the "1Pから4Pまで プレイ可能"
4-player banner (`shot-121s.png`); a HOW TO PLAY demo card over live arena footage
("ハンドルを押すと バンパーパンチ!" — push the stick to bumper-punch, `shot-182s.png`); a further
in-arena demo battle (`shot-304s.png`); and the "RING OUT 4x4 — CRASH IN!!" rock-carved title
logo (`shot-609s.png`). Genuine attract-demo gameplay — no calibration screen, no idle EEPROM
prompt, no frozen frame.
Screenshots: `evidence/ringout/shot-060s.png` · `shot-121s.png` · `shot-182s.png` ·
`shot-304s.png` · `shot-609s.png`
Anomalies: none. `shot-365s.png` (a 9.6 kB near-black fade-transition frame) and
`shot-243s.png`/`shot-426s.png`/`shot-487s.png`/`shot-548s.png` (redundant stage-showcase and
demo-match frames) were curated out for readability, same class as the fade-transition frames
trimmed from `inunoos`/`pokasuka`/`sstrkfgt`/`toyfight`.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 7,726,701 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.684** — well past `region_score()`'s `u > 2.0` gate. This makes `ringout` the
**ninth currently-gated G3-aram family** and the second-highest ARAM figure in the parked
cohort, 5,772 B under the top: toyfight 2.035, takoron 2.997, inunoos 3.206, ninjaslt 3.341,
pokasuka 3.368, mazan 3.483, mok 3.558, **ringout 3.684**, sstrkfgt 3.687. Well above the kb §6
item-1 empty band (scored max ~1.96, parked min 2.997) — it lands inside the dense upper
cluster, another data point for the checkpoint that softening the 2× line marginally would
change nothing here. `nz_above_cap` = 5,767,137 B of content above the cap (address-keyed
placement figure, informational). Address peak is 8,088,219 B (u 3.857, pre-volume-keying read).

The other two regions, quoted from the sidecar for context (ARAM gates first in `score.py`'s
region walk regardless):

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 19,793,309 | 16,777,216 | **1.180** | `nz_total` — **over** the 1x cap (would land in the penalty band, not a gate); `nz_above_cap` (address-placement) 8,983,740 B · `dma_high_water` 21,407,328 B (u 1.276) · write-truth address peak 31,666,976 B (u 1.888) |
| VRAM (content volume + 2×fb) | 6,779,016 | 8,388,608 | **0.808** | `content_total` 5,550,216 + 2×`fb_bytes` (2×614,400, the standard double-buffered 640×480×2 constant, per `score.py`'s `vram_ct + 2*vram_fb` formula) — clears the 1x cap; raw `nz_total` 6,009,816 · `nz_above_cap` 5,289,275 (address-keyed) · address peak 16,533,504 (u 1.971) |
| ARAM (content volume) | 7,726,701 | 2,097,152 | **3.684** | the gate — see above |

Streaming context: 1 DMA event · 9,872,992 B total = unique (re-read ratio 0.0) · steady-state
0.0 MB/min (`short_window: false`) · `pio_bytes` 21,991,954 B — an M2-crypt cart loaded almost
entirely by PIO up front, everything resident, nothing streamed after handoff: the memory
figures are the whole story for this title.
Guts: code 2,097,152 B (2.0 MiB, under the 4 MiB `code_over_4mb` threshold) · 1,271 functions ·
MMIO refs rtc 4 / g2ext 91 / scif 0 · flags `eeprom_bios`/`rtc`.
Similarity: `developer_match: false`, `sdk_overlap: "none"`, `cart_loader_match: false`.

Evidence: `assessments/ringout.metrics.json` → `memory.aram`; `guts.sdk_strings` shows the
early-1999 Sega AM library stack (`NAOMI LIBRARY Ver 0.8 AM R&D`, `syG2 Ver 1.01.01`,
`libam/Version 1.232590`) and the dual-I/O requirement ("TWO JAMMA I/O BOARDS ARE REQUIRED FOR
THIS GAME") backing the 4-player build.

**Controls would not gate or penalize, if ARAM were ever solved.** Researched (2 sources):
`ringout` carries no `PORT_INCLUDE`/`PORT_MODIFY` override in MAME — its `GAME()` line
(src/mame/sega/naomi.cpp @59e7c0b, line 10944) uses the generic `INPUT_PORTS_START( naomi )`
directly: 8-way digital joystick + 6 buttons per player (`IPT_JOYSTICK_*` · `PORT_8WAY`,
`IPT_BUTTON1`–`IPT_BUTTON6`), all analog channels unused; corroborated by
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=ringout) (8-way
joystick, 6 buttons, 2 concurrent players / up to 4 via the second JAMMA I/O board). The
attract HOW TO PLAY card ("push the stick → bumper punch", `shot-182s.png`) matches a plain
stick-plus-buttons panel. That maps directly onto DC pads (up to 4, matching the 1P–4P design)
— `controls.device_class = stick`, the ladder's top rung, no penalty.

What would unblock it: ARAM content would need to shrink below the 2× cap — a **45.7% cut**
(3,532,397 B) to the voice/BGM bank, near the top of the range needed in the parked cohort.
Per-title audio trim has released-port precedent (the official Ikaruga DC port's 4× sound trim,
kb §4.d), so it is not implausible on its face, but at 3.684× it is a real porting project, not
a scoring artifact. Alternatively, an ARAM gate softening at the kb §6 item-1 checkpoint —
though any threshold below ~3.7× still parks this title, so only a "score heavy-ARAM overshoot
low instead of parking" rule change would move it. Main RAM's 1.180× content line would also
need attention for a full clear, though it does not gate on its own.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — fresh v9 capture; u 3.684, second-highest in parked cohort |
