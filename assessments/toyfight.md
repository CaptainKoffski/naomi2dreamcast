# Toy Fighter (`toyfight`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 4,262,853 B → utilization **2.033**, just 3.3% of one DC AICA-RAM capacity past the `u > 2.0` gate line — the **first title ever measured strictly inside** the previously-empty band between the campaign's scored max (`zerogu2` 1.962) and parked min (`takoron` 2.997), where until now no possible threshold changed any title's fate (kb §6 item 9, checkpoint re-run 2026-08-10). Main RAM (`nz_total` u ≈ 0.424) and VRAM (`content_total`+2×`fb_bytes` u ≈ 0.867) both clear their caps with room; ARAM alone gates. Controls are clean: a standard 8-way stick + 6 buttons (MAME generic `naomi` input ports, corroborated), `controls.device_class = stick` — full marks, no penalty. |
| Assessed | capture 2026-08-10 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `toyfight` (no clones; sole family member, self-keyed MAME parent) |
| Maker / year | Sega / Anchor Inc., 1999 (GAME line: `/* 0011 */`; ROM_START comment `840-0011 1999 317-0257-COM Naomi`) |
| Genre / format | Fighting — 3D toy-themed versus fighter (queue genre label is accurate here, confirmed by attract-demo combat HUD footage, §3), **cart** — 840-0011, boot ROM + 10×64 Mb, 46.0 MB |
| Official DC port | No (GAME_FORMATS.md: "No"). Note: a Dreamcast port was reportedly in development but never released — listed among GAME_FORMATS.md's "cancelled-but-unreleased DC ports" and corroborated by Wikipedia's [List of cancelled Dreamcast games](https://en.wikipedia.org/wiki/List_of_cancelled_Dreamcast_games) ("A Dreamcast port of Sega's arcade fighting game *Toy Fighter* (1999) was reported to be in development but never materialized") — no consumer DC release exists either way |
| Community ports | None found (searched 2026-08-10) |
| Representative choice | Sole family member, MAME parent (`toyfight`) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/toyfight.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set
here after screenshot review). The attract loop cycles through character-posing/title-prompt
shots (`shot-121s.png`, "PRESS 1P OR 2P START BUTTON"), win-ranking result boards (`shot-243s.png`
"1st ... 8 WINS", a full 5-place standings screen), **live in-match combat footage with a working
HUD** — a "REVERSE" special-move callout, P+K button-combo prompt, and health bars over two
fighting toy characters (`shot-426s.png`), the "TOY FIGHTER" title logo (`shot-548s.png`), and a
character close-up cutscene (`shot-609s.png`) — genuine attract-demo gameplay including an actual
in-match combat HUD, not a frozen frame or idle EEPROM prompt.
Screenshots: `evidence/toyfight/shot-121s.png` · `shot-243s.png` · `shot-426s.png` ·
`shot-548s.png` · `shot-609s.png`
Anomalies: none. `shot-182s.png` (a near-blank, blurry ground-texture camera-pan frame) and
`shot-060s.png`/`shot-304s.png` (redundant character-posing shots) were curated out for
readability, same class as the fade-transition frames trimmed from `inunoos`/`pokasuka`/`sstrkfgt`.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 4,262,853 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **2.033** — past `region_score()`'s `u > 2.0` gate.

This is the **first title ever measured strictly inside** the kb §6 item-9 empty band: the
checkpoint re-run at 32 assessed families (2026-08-10, all-fresh v9 capture provenance) re-affirmed
that band as empty — max scored volume-u 1.962 (`zerogu2`), min parked 2.997 (`takoron`) — and
noted that *any threshold placed in (1.962, 2.997) changes no title's fate*. toyfight's 2.033 is
the first counterexample: it lands 0.071 above the scored max and 0.964 below the parked min,
squarely inside that gap. The excess over the gate line itself is small — `u − 2.0 = 0.033`, i.e.
only **3.3%** of one DC AICA-RAM capacity past the line — so a gate placed at, say, 2.1 would score
this title outright rather than park it.

Fragility angle: the same checkpoint recorded run-to-run ARAM content drift of up to **+1.89%**
(`inunoos`, v7→v9 captures) and −0.77% (`takoron`) on this exact gate class (kb §6 item 9).
toyfight's 3.3%-of-cap margin over the line sits within roughly 1.6× that observed drift envelope
— close enough that a second capture could plausibly land on either side of `u = 2.0`. A
reproduction re-run is queued as a controller follow-up to test measurement stability. The park
stands as scored under the current rule: no mid-wave `score.py` re-keying — scoring-semantics
changes (including any G3 multiple change) are user-ruled checkpoint decisions (RUNBOOK "Campaign
checkpoint"; kb §6). This makes toyfight the strongest unpark candidate in the campaign if the
checkpoint ever revisits the 2.0 multiple.

`nz_above_cap` = 2,267,732 B (address-keyed placement figure, informational). Address peak is
8,257,552 B (u 3.938, pre-volume-keying read).

The other two regions clear comfortably, quoted from the sidecar for context (ARAM gates first in
`score.py`'s region walk regardless):

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 7,121,855 | 16,777,216 | **0.424** | `nz_total` — clears the 1x cap with wide margin; `nz_above_cap` (address-placement) 5,491,198 B · `dma_high_water` 30,694,656 B (u 1.829, old address-peak read) |
| VRAM (content volume + 2×fb) | 7,269,948 | 8,388,608 | **0.867** | `content_total` 6,041,148 + 2×`fb_bytes` (2×614,400, the standard double-buffered 640×480×2 constant, per `score.py`'s `vram_ct + 2*vram_fb` formula) — clears the 1x cap with room; raw peak (address) 14,639,104 (u 1.745) · `nz_above_cap` 3,960,911 B (address-keyed) |
| ARAM (content volume) | 4,262,853 | 2,097,152 | **2.033** | the gate — see above |

Streaming context: 260 DMA events · 112,657,664 B (107.5 MB) total · 41,521,152 B (39.6 MB) unique
· re-read ratio 0.6314 · steady-state 10.464 MB/min (`short_window: false`) · `pio_bytes`
1,078,648 B.
Guts: code 1,048,576 B (1.0 MiB, well under the 4 MiB `code_over_4mb` threshold) · 1,184
functions · MMIO refs rtc 4 / g2ext 193 / scif 0 · flags `eeprom_bios`/`rtc`.
Similarity: `developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: false`.

Evidence: `assessments/toyfight.metrics.json` → `memory.aram`; `guts.sdk_strings` shows a full
NAOMI AM-library credits/build-string dump (`libam/Version 1.232810`, `Mioz/Version 1.102000`
"NAOMI ARCADE CONTROLLER") plus complete development-staff and voice-actor credits, consistent
with a sizeable character-voice/SFX bank behind the toy-fighter combat and win-ranking screens
visible in the attract demo.

**Controls would not gate or meaningfully penalize, if ARAM were ever solved.** Researched (2
sources): toyfight carries no `PORT_INCLUDE`/`PORT_MODIFY` override in MAME — its `GAME()` line
(src/mame/sega/naomi.cpp @59e7c0b, line 10950) uses the generic `INPUT_PORTS_START( naomi )`
directly, which defines an 8-way digital joystick + 6 buttons per player (`IPT_JOYSTICK_*` ·
`PORT_8WAY`, `IPT_BUTTON1`–`IPT_BUTTON6`); corroborated by
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=toyfight) (8-way joystick,
6 buttons, up to 2 players). That is the canonical arcade-fighter control scheme and maps directly
onto a DC pad's D-pad/stick + face buttons — `controls.device_class = stick` (100.0 on the
`score.py:108` ladder, the ladder's top rung), not a gate and not a penalty.

What would unblock it: ARAM content would need to drop below the 2× cap — by far the smallest cut
needed among the campaign's parked ARAM titles so far (`takoron` 2.997×, `inunoos` 3.206×,
`pokasuka` 3.368×, `sstrkfgt` 3.687×), realistically a modest trim to the character-voice/SFX
bank. Whether the current 2.033 reading is real margin or capture noise is exactly what the queued
reproduction re-run will settle.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-10 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — fighter cohort, fresh v9 capture; u 2.033 = first in-band park, 3.3% over the line (checkpoint-flagged) |
