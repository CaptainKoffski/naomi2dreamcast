# Kurukuru Chameleon (Japan) (GDL-0034) (`kurucham`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **85.2 (S)** |
| Bottom line | With the v7 ARAM-content and v8 VRAM FB-mask fields actually populated (the prior v6 sidecar predated both and scored through conservative peak-keyed fallbacks), all three regions land under or near their DC caps — main content 0.16×, VRAM FB-masked fit 0.76×, ARAM content 0.90× (now the binding region, near-fit not overflow) — a very different memory picture from the old address-peak read, which had VRAM's 14.77 MB write-truth peak (1.76×) binding the axis at 19.6. |
| Assessed | capture 2026-08-09 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `kurucham` (covers: no clones — `parent: null` in controls.json) |
| Maker / year | Able (arcade publisher; developer Starfish SD — `@2006 STARFISH-SD` in `guts.sdk_strings`), 2006 |
| Genre / format | Puzzle ★, GD-ROM (GDL-0034) |
| Official DC port | No — platform history is PSP/DS (2006), Switch (2019), PS4/Windows (2020) as *Chameleon: To Dye For!* / *Kameleon*; no Dreamcast release ([Wikipedia](https://en.wikipedia.org/wiki/Chameleon:_To_Dye_For!), accessed 2026-08-02) |
| Community ports | None found — not in the Dreamcast Junkyard Naomi-conversion list ([link](https://www.thedreamcastjunkyard.co.uk/2016/01/guest-article-expanding-dreamcast.html)), no dreamcast-talk/Reddit conversion threads surfaced (searched 2026-08-02). Zophar's "Sega Dreamcast (DSF)" music rip ([link](https://www.zophar.net/music/sega-dreamcast-dsf/kuru-kuru-chameleon)) is almost certainly a mislabeled Naomi AICA rip, not a conversion. |
| Representative choice | Only member of its family (MAME parent, no clones) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"` — GD DIMM ~1 MB bootstrap) · run 600 s · rom: `naomi/kurucham.zip`
Attract/demo reached: **demo** — full attract-mode gameplay confirmed across the
capture: `shot-243s.png`/`shot-426s.png`/`shot-548s.png` show live two-player hex-match
demo rounds (turn counters, %-fill bars, cycling AI opponent portraits) well past the
title card seen at `shot-060s.png`, ending on a demo win screen at `shot-609s.png`;
sidecar `capture.coverage = "demo"` (battery writes `null` — set explicitly in this
pass after reviewing the shots).
Screenshots: `evidence/kurucham/shot-060s.png` · `shot-243s.png` · `shot-426s.png` ·
`shot-548s.png` · `shot-609s.png`.
Also in evidence (v2-era raw-VRAM decodes, durable): `vram-assets-c00000.png` — the
above-8-MB region decoded as dense structured asset data — and
`vram-fb-76a000-black.png`.
Anomalies: none.

## 4. Memory fit (axis: 92.2)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 2,703,775 | 16,777,216 | 0.161 | 100.0 | unchanged byte-for-byte from v6 · address peak 32,505,920 (`0x1F00040`, u 1.94, informational — kb §6 item 3 shared-structure signature) · `nz_above_cap` 1,352,471 · `dma_high_water` 27,449,344 — all byte-identical v6→v9 |
| VRAM (v8 FB-masked content: `content_total` + 2×`fb_bytes`) | 5,116,323 + 2×614,400 = 6,345,123 | 8,388,608 | 0.756 | 100.0 | **first real v8 measurement** — v6 had no `content_total`/`fb_bytes` and fell back to raw peak (14,770,864, u 1.761, sub-score 19.6, the old axis-binding region); `nz_total` 5,623,486 and `nz_above_cap` 5,612,252 byte-identical v6→v9 (address extent of the high-parked asset store, `vram-assets-c00000.png`, now known relocatable rather than binding) |
| ARAM (v7 content volume, `content_total`) | 1,896,338 | 2,097,152 | 0.904 | 92.2 | **first real v7 measurement, now binding** — v6 had no `content_total` and fell back to raw peak (2,395,328, u 1.142, sub-score 59.4); `peak` 2,395,328 and `nz_above_cap` 282,380 byte-identical v6→v9 — near-fit, not overflow |

Memory axis = min(100.0, 100.0, 92.2) = **92.2** — binding region moved from VRAM
(peak-keyed 1.76× overflow fallback) to ARAM (content-keyed 0.90× near-fit
measurement); VRAM's fallback→measured move alone would have cleared the axis to
100.0, same pattern as tetkiwam.

Watermarks (informational, content-scan — stale-data prone): main 32,505,920 ·
vram 14,770,864 · aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 74.3)

DMA events 2,615 · total 88,363,008 B (84.3 MB) · unique 28,819,456 B (27.5 MB) ·
re-read ratio 0.6739 · steady-state 7.162 MB/min (`short_window: false`) ·
PIO 1,049,920 B
(v6: 2,621 events, 88,897,536 B total, reread 0.6758, 7.226 MB/min — a fresh
capture's normal run-to-run noise, not a fallback effect; `unique_bytes` and
`pio_bytes` byte-identical v6→v9; axis moves 74.1→74.3, immaterial)

## 6. Guts (axis: 85.0)

Code 1,048,576 B (carve `base 0x8c020000`, entry `0x8c020fe0`, header title
"KURU KURU CHAMELEON") · functions 2,634 · MMIO refs: scif 2, rtc 3, g2ext 58 ·
BIOS vector refs: none · penalties applied: `eeprom_bios`, `serial`, `rtc` → 85.0

`guts.sdk_strings` shows a heavily DC-adjacent stack: Kunoichi2 Library for NAOMI 2.07,
Ninja2 2.01, `sd2 for DC`, `SEGAKATANA` RMC, CRI ADX/Sofdec, NEC KAMUI2 — plus the
internal build id `KAMELEON 2005 VER 1.00`.

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi stick + buttons, 2 players. MAME input ports: `naomi`.
The game's own INPUT TEST menu (in-binary, `guts.sdk_strings`) lists exactly
UP/DOWN/LEFT/RIGHT + SELECT/CANCEL/SPECIAL + START per player — one 8-way stick and
three game buttons. Proposed DC mapping: d-pad/stick + A (select), B (cancel),
X or Y (special), Start — 1:1 on a stock pad.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=kurucham)
(8-way joystick + 6-button JVS standard declaration, 2P);
[Wikipedia](https://en.wikipedia.org/wiki/Chameleon:_To_Dye_For!) ("simple controls"
competitive colour-matching puzzle); in-binary INPUT TEST strings
(`assessments/kurucham.metrics.json` → `guts.sdk_strings`).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 92.2^.40 · 74.3^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **85.2 (S)**
Similarity inputs: developer no (Starfish SD/Able ≠ reference), SDK overlap partial
(Kunoichi2/Ninja2/CRI — see §6), loader match yes.

## 9. Risks & notes

- **Port-planning takeaway: ARAM is now the binding region, and it's a near-fit, not
  overflow.** Content volume is 1,896,338 B against the 2,097,152 B cap (u 0.904) —
  204,814 B of headroom. A port needs modest compaction/streaming discipline on
  audio data, not a redesign.
- **Main RAM is address-sparse:** content volume is only 2.7 MB (0.16×) but the
  touched address peak is the 32,505,920 B `0x1F00040` shared-structure signature
  (1.94×, kb §6 item 3) with 1.35 MB of nonzero bytes above the 16 MB line — layout/
  relocation attention needed, though it no longer binds the axis.
- **VRAM's old address-peak overflow (1.76×) was a fallback artifact, not real
  pressure.** FB-masked content fit is 6,345,123 B (u 0.756) — the 14.77 MB peak was
  mostly the same high-parked, relocatable asset store noted at v6
  (`vram-assets-c00000.png`); the v8 measurement confirms that read.
- **Rendering must be verified on real DC hardware** (working-style rule). The v2
  display-blind run was a tooling artifact (kb §4.l/§4.m); v4+ builds render the
  attract demo, confirmed again in this capture (§3).

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-03 | 45.8 (B) | First score, headless zeroing-era build (`title` coverage was an artifact). Superseded the same-day `G1 broken: no-handoff-120s` park (commit `d7500a1`), retracted after kb §4.l/§4.m — false parks were a below-8MB-only boot heuristic plus launch flakes (fixes `61350c8`, `4ea17fc`, `e5f5649`) |
| v4 | 2026-08-04 | 45.8 (B) | Re-captured on a rendering build with demo coverage; same final (kb §7) |
| v6 | 2026-08-07 | 38.3 (C) | Main re-keyed to the write-truth address peak — 32,505,920 B `0x1F00040` shared-structure signature (kb §6 item 3); `dma_high_water` reproduced byte-for-byte |
| v9 | 2026-08-08 | 45.8 (B) | Scoring-only re-key (no re-capture): main scored on content volume `nz_total` (spec `2026-08-08-main-content-rekey-design.md`); memory 19.6, binding region moved to VRAM |
| v9 | 2026-08-09 | 85.2 S | ranking-groom chunk 4: fresh v9 capture, provenance v6→v9 — first real v7 ARAM-content + v8 VRAM FB-mask measurements replace conservative fallbacks (memory 19.6→92.2, binding region VRAM→ARAM; streaming 74.1→74.3 noise-level; final 45.8 B→85.2 S); every shared raw counter (main peak/nz_total/nz_above_cap/dma_high_water, vram peak/nz_total/nz_above_cap/regs_last, aram peak/nz_above_cap, streaming unique_bytes/pio_bytes, guts code_bytes/functions/mmio_refs/carve_meta/flags) reproduced byte-identically v6→v9 — the move is pure fallback-replacement, not re-capture drift |
