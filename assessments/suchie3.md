# Idol Janshi Suchie-Pai 3 (`suchie3`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **53.8 (B)** |
| Bottom line | Second mahjong-⚠ family, and again the ⚠ dissolves: same `naomi_mp` key-matrix cabinet as shangril, ruled `pad_adaptable` (50) with title-specific console precedent — this exact game shipped button-played on PSP/DS (*Suchie-Pai III Remix*, 2007) and its own attract loop advertises the 1999 Dreamcast adaptation on screen. What keeps it in B is VRAM: FB-masked texture content alone is 8.63 MB > the 8 MB cap, and with the double framebuffer the fit value lands at u 1.248 — a hair under the 40-point knee — dragging the memory axis to 40.3, which the ^.40 weight makes decisive. Main RAM (0.79× cap) and ARAM (0.67× cap) are green; streaming is moderate bandwidth with a high re-read ratio. A port lives or dies on cutting ~2 MB of texture content. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `suchie3` (no clones — sole `suchie3` set in naomi.cpp: ROM_START line 4996, GAME line 11091) |
| Maker / year | Jaleco, 1999 (`/* 0002 */ GAME( 1999, suchie3, naomi, naomim2, suchie3, naomi_state, init_naomi_mp, ROT0, "Jaleco", "Idol Janshi Suchie-Pai 3 (Japan)", GAME_FLAGS )` — naomi.cpp @59e7c0b line 11091; title screen concurs, `shot-182s.png` "©1999 JALECO LTD.") |
| Genre / format | Mahjong ⚠ (strip-mahjong vs. idol characters, story attract), **cart, Naomi M2** (`naomim2` machine, 102.3 MB; carve strings name Jaleco's `JV-98351 P.C.B.`) |
| Official DC port | **Partial** — *Idol Janshi wo Tsukucchaou* (アイドル雀士をつくっちゃおう), DC T-5703M (Shokai Genteiban T-5702M), Jaleco, Japan 1999: a retitled adaptation of Suchie-Pai III (adult content removed, "Making Mode" added) ([Satakore](https://www.satakore.com/sega-dreamcast-video-game-store,,38,,592,,Idol-Janshi-wo-Tsukucchaou-JP.html); [changev's world](https://www.changevworld.com/suchie/Pai_DCLE.htm); [Wikipedia series list](https://en.wikipedia.org/wiki/Idol_Janshi_Suchie-Pai)). The arcade attract loop itself advertises it — Dreamcast-swirl "つくっちゃおう" announce banner in `shot-060s.png`, and `ADREAMCAST ANNOUNCE` is a `<GAME CONFIG>` toggle in the carve strings. GAME_FORMATS.md's existing `Partial` cell verified correct. The straight port of this exact game came later on PSP/DS: *Idol Janshi Suchie-Pai III Remix*, 2007 ([StrategyWiki](https://strategywiki.org/wiki/Idol_Janshi_Suchie-Pai_III)). |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | MAME parent, sole member of the family; second of the three mahjong-⚠ families in the queue |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/suchie3.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). Attract cycles: Dreamcast-announce banner over story/character art
(`shot-060s.png`, `shot-121s.png`), title card (`shot-182s.png`), a full in-engine 3D mahjong
demo hand with helper popups (`shot-304s.png`), and a demo scoring frame — 倍満/baiman —
under the same DC banner (`shot-487s.png`) — all under FREE PLAY.
Screenshots: `evidence/suchie3/shot-060s.png` · `shot-121s.png` · `shot-182s.png` · `shot-304s.png` · `shot-487s.png`
Anomalies: none — clean first-attempt full-window leg; battery-printed provisional 53.8 B stands
unchanged (the battery's `pad_adaptable` hint survived research).

## 4. Memory fit (axis: 40.3)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 13,263,453 | 16,777,216 | 0.791 | 100.0 | Address peak 26,087,424 (u 1.56, placement artifact) · `nz_above_cap` 3,788,231 B of content above the 16 MB line (see Risks) · `dma_high_water` 24,432,448 (informational) |
| VRAM (FB-masked content volume + 2×framebuffer, `content_total + 2*fb_bytes`) | 10,471,660 | 8,388,608 | 1.248 | 40.3 | **The binding region.** `content_total` 8,628,460 + 2×`fb_bytes` 921,600 — texture content alone exceeds the cap before framebuffers. Address peak 16,746,495 (u 1.996, just under the G3 2× line) is the FB flip pair parked at 0x800000/0xc00000 (`regs_last`), the chocomk precedent the v8 FB-masking rekey exists for |
| ARAM (content volume, fill-excluded, `content_total`) | 1,406,734 | 2,097,152 | 0.671 | 100.0 | Address peak 4,670,845 · `nz_above_cap` 4 |

Watermarks (informational, content-scan — stale-data prone): main 26,087,424 ·
vram 16,746,495 · aram 8,388,608 (the boot-time "DMPD" fill, not content).
Axis = min(regions) = VRAM's 40.3.

## 5. Cart streaming (axis: 69.2)

DMA events 825 · total 112.5 MB (117,925,504 B) · unique 35.2 MB (36,897,472 B) ·
re-read ratio 0.6871 · steady-state 10.736 MB/min (`short_window: false`) ·
PIO 14,361,920 B. Bandwidth is comfortable (sub-score 89.5); the 0.69 re-read
ratio (sub-score 38.8) drags the axis to 69.2.

## 6. Guts (axis: 90.0)

Code 1,048,576 B · functions 1,472 · MMIO refs: scif 0, rtc 2, g2ext 249 ·
BIOS vector refs: `0x8c0000bc`×10 · penalties: `eeprom_bios` −5, `rtc` −5 → 90.0.
Carve clean (`hdr_at` 0, title "IDOL JANSHI SUCHIE-PAI 3", base 0x0c020000). SDK strings
show the stock Sega Naomi stack (syG2/syHw/syTmr/syCache/sySq/syChain/syInt, libintr 1.03,
libam 1.232810) plus CRI ADX 5.55 movie/audio streaming → `sdk_overlap: partial`.

## 7. Controls (axis: 50.0 — `pad_adaptable`)

Cabinet: the Sega Naomi **mahjong keyboard-matrix panel** — the same physical hardware
ruled `pad_adaptable` for `shangril` tonight. MAME gives `suchie3` its own INPUT_PORTS
(naomi.cpp @59e7c0b lines 2073–2077) but it is just `PORT_INCLUDE( naomi_mp )` with the
P1 reader swapped to `suchie3_mp_r` (lines 2051–2071 — "KEY1 and KEY5 are swapped", a
column-order quirk, not different hardware). The matrix itself (lines 1994–2049): five
strobed columns, keys **A–N** plus **Kan/Pon/Chi/Reach/Ron/Bet/Flip-Flop/Last-Chance/Start**;
wiring diagram at lines 1172–1190 ("mahjong panel uses ext. I/O 4-8", rows on JAMMA 17–22).
Our fork emulates no such matrix — `suchie3`'s ROM entry carries no per-game input struct
(`core/hw/naomi/naomi_roms.cpp:3671` @f014a410c) and `maple_jvs.cpp` has no mahjong
handling — yet the game attracts fine on the standard JVS digital path.

**Why `pad_adaptable`, not `awkward`:** the shangril precedent (same panel, same night)
plus two title-specific console precedents. (1) This exact game shipped button-played:
*Idol Janshi Suchie-Pai III Remix* (PSP + Nintendo DS, Jaleco 2007) — handhelds have no
mahjong panel by construction. (2) Jaleco's own 1999 DC adaptation (*Idol Janshi wo
Tsukucchaou*, T-5703M) was pad-played — and the arcade ROM knows it: the attract loop
renders a Dreamcast announce banner (`shot-060s.png`) and test mode has an
`ADREAMCAST ANNOUNCE` config toggle. Mahjong is turn-based with no timing pressure, so
cursor-over-tiles plus call buttons loses nothing mechanical. Not `stick` (100): the
panel's ~20 discrete keys cannot map 1:1 onto a pad; the tile-cursor UI layer is real
(if already-solved) work.

Proposed DC mapping: D-pad/stick = tile cursor, A = discard/confirm, B = cancel,
X/Y/triggers = Pon/Chi/Kan/Reach/Ron prompts (context-sensitive call prompts, the DC
mahjong idiom), Start = start.
Sources: all eight citations are in sidecar `controls.sources` (MAME GAME row + input
ports + wiring, Flycast fork input path, StrategyWiki PSP/DS Remix, Satakore +
changev's world DC T-5703M/T-5702M, Wikipedia series list, in-ROM DC-announce evidence).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 40.3^.40 · 69.2^.20 · 90.0^.20 · 50.0^.10 · 40.0^.10 = **53.8 (B)**
Similarity inputs: developer no, SDK overlap partial (stock Sega Naomi libs + CRI ADX, §6), loader match no.

## 9. Risks & notes

- **VRAM is the whole story**: FB-masked texture content is 8,628,460 B — over the 8 MB
  cap before a single framebuffer is placed — and the scored fit (content + 2×FB) is
  10.47 MB, u 1.248, sitting one thousandth under the 40-point knee at 1.25. A port must
  cut or recompress ~2.1 MB of texture content (or drop to a single 640×480 FB /
  smaller FB format) before anything else matters. First thing to map.
- Raw VRAM address peak 16,746,495 (u 1.996) grazes the G3 2× gate line — it is the FB
  flip pair parked at 0x800000/0xc00000 (`regs_last`), exactly the placement artifact
  the v8 FB-masking rekey discounts; the content-keyed number above is the real fit.
- **Main RAM content fits comfortably** (13.26 MB, u 0.79) but 3,788,231 B of it sits
  above the 16 MB line (`nz_above_cap`; DMA high-water 24.4 MB) — relocation work, not
  capacity work.
- **High streaming re-read ratio (0.69)** — the cart re-fetches a 35 MB working set to
  the tune of 112 MB over 10 minutes; flags asset-reload-per-scene design (each attract
  scene/character reloads its `pm_*.tlz` art). Bandwidth itself (10.7 MB/min) is fine.
- **Link/network code is present but optional**: NLCB + "NO COMMUNICATION BOARD."
  strings in the carve; no `network` guts flag assessed (standard cabinet has no comm
  board) — a port drops versus-link. Likewise "THIS GAME NEEDS ONE I/O BOARD" refers to
  the mahjong-panel ext. I/O, replaced wholesale by the pad mapping (§7).
- **CRI ADX movie/audio streaming** (ADXT 5.55, `movie/vlc.tbl`, `.tmv` files) — the
  attract's anime cutscenes stream from cart; a DC port streams the same ADX from
  GD-ROM (native CRI platform), low risk but worth budgeting.
- The official DC adaptation (T-5703M) is a ready-made reference for control scheme and
  content cuts, but unlike shangril's case it is *not* the same game (roster and content
  differ) — a faithful port of the arcade original still has an audience.
- Rendering must be verified on real DC hardware (working-style rule); evidence here is
  fork-rendered attract only.
- MAME status is the blanket naomi.cpp `GAME_FLAGS` (no per-title signal, kb §4.r).

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | 53.8 (B) | Initial assessment — second mahjong-⚠ family. Clean full-window first-attempt leg, demo reached; controls research confirmed the battery's `pad_adaptable` hint (same naomi_mp matrix as shangril; title-specific precedent: PSP/DS *III Remix* 2007 + Jaleco's own 1999 DC adaptation T-5703M, advertised in the ROM's attract), so the provisional 53.8 stood. GAME_FORMATS DC-port `Partial` cell verified correct |
