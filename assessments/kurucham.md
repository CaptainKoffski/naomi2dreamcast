# Kurukuru Chameleon (Japan) (GDL-0034) (`kurucham`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **45.8 (B)** |
| Bottom line | Content is genuinely DC-sized (main content 0.16× cap, 5.6 MB of actual VRAM assets, ARAM 1.14× near-fit) but the VRAM sub-score binds at 19.6 on the 14.77 MB write-truth address peak — the v6 sidecar predates FB-masked VRAM keying, and nearly all of that peak is a relocatable high-parked asset store, so the real pressure is milder than the score implies. |
| Assessed | capture 2026-08-07 · battery v6 · flycast `65f9f7857` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — scored under battery v9 keying (scoring-only re-score 2026-08-08, see History) |

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
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (the v2 run's
`title`-only label was a headless zeroing-era artifact, see History).
Screenshots: `evidence/kurucham/shot-060s.png` · `shot-365s.png` · `shot-609s.png`.
Also in evidence (v2-era raw-VRAM decodes, durable): `vram-assets-c00000.png` — the
above-8-MB region decoded as dense structured asset data — and
`vram-fb-76a000-black.png`.
Anomalies: none at v6.

## 4. Memory fit (axis: 19.6)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 2,703,775 | 16,777,216 | 0.161 | 100.0 | address peak 32,505,920 (`0x1F00040`, u 1.94, informational — kb §6 item 3 shared-structure signature) · nz_above_cap 1,352,471 · `dma_high_water` 27,449,344 (byte-identical to v4) |
| VRAM (write-truth address peak — v6 sidecar has no FB-masked `content_total`/`fb_bytes`) | 14,770,864 | 8,388,608 | 1.761 | 19.6 | **binding** — nz_total 5,623,486 with 5,612,252 above the 8 MB line: address extent of a high-parked asset store (decoded at `0xc00000`, `vram-assets-c00000.png`), relocatable in a port |
| ARAM (write-truth address peak — v6 sidecar has no `content_total`) | 2,395,328 | 2,097,152 | 1.142 | 59.4 | nz_above_cap 282,380 — near-fit |

Watermarks (informational, content-scan — stale-data prone): main 32,505,920 ·
vram 14,770,864 · aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 74.1)

DMA events 2,621 · total 88.9 MB · unique 28.8 MB · re-read ratio 0.6758 ·
steady-state 7.226 MB/min (`short_window: false`) · PIO 1,049,920 B

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
      = 19.6^.40 · 74.1^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **45.8 (B)**
Similarity inputs: developer no (Starfish SD/Able ≠ reference), SDK overlap partial
(Kunoichi2/Ninja2/CRI — see §6), loader match yes.

## 9. Risks & notes

- **VRAM binds on pre-v8 keying.** The v6 sidecar predates FB-masked VRAM keying (no
  `content_total`/`fb_bytes` fields), so the sub-score keys on the 14.77 MB address
  peak; actual nonzero content is 5.6 MB, nearly all of it parked above the 8 MB line
  (`vram-assets-c00000.png`) — relocatable extent, so the real VRAM pressure is far
  milder than sub 19.6 implies.
- **Main RAM is address-sparse:** content volume is only 2.7 MB (0.16×) but the
  touched address peak is the 32,505,920 B `0x1F00040` shared-structure signature
  (1.94×, kb §6 item 3) with 1.35 MB of nonzero bytes above the 16 MB line — layout/
  relocation attention needed.
- **ARAM is address-keyed** (no `content_total` in the v6 sidecar): 1.14× near-fit
  with 282,380 B above cap.
- **Rendering must be verified on real DC hardware** (working-style rule). The v2
  display-blind run was a tooling artifact (kb §4.l/§4.m); v4+ builds render the
  attract demo.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-03 | 45.8 (B) | First score, headless zeroing-era build (`title` coverage was an artifact). Superseded the same-day `G1 broken: no-handoff-120s` park (commit `d7500a1`), retracted after kb §4.l/§4.m — false parks were a below-8MB-only boot heuristic plus launch flakes (fixes `61350c8`, `4ea17fc`, `e5f5649`) |
| v4 | 2026-08-04 | 45.8 (B) | Re-captured on a rendering build with demo coverage; same final (kb §7) |
| v6 | 2026-08-07 | 38.3 (C) | Main re-keyed to the write-truth address peak — 32,505,920 B `0x1F00040` shared-structure signature (kb §6 item 3); `dma_high_water` reproduced byte-for-byte |
| v9 | 2026-08-08 | 45.8 (B) | Scoring-only re-key (no re-capture): main scored on content volume `nz_total` (spec `2026-08-08-main-content-rekey-design.md`); memory 19.6, binding region moved to VRAM |
