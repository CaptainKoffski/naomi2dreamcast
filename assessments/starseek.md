# Doki Doki Idol Star Seeker (GDL-0005) (`starseek`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **79.0** (A) |
| Bottom line | VRAM narrowly binds the memory axis at u=1.106 (FB-masked content fit, ~11% over the 8 MB cap), with main RAM close behind at u=1.086 — both modest overflows, not the severe multiples that gate other titles; zero cart-DMA streaming after a one-shot PIO load (streaming 100.0) plus clean guts/controls/similarity axes carry a small, lean puzzle title to a solid A. |
| Assessed | 2026-08-12 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `starseek` (covers: no clones — sole member of its family) |
| Maker / year | G.Rev, 2001 |
| Genre / format | Puzzle ★, GD-ROM (GDL-0005) |
| Official DC port | Partial — *Doki Doki Idol Star Seeker Remix* (G.Rev, Japan, Jan 31 2002) adds an original "Doki Doki Idol" story mode, voice acting, an art gallery and a sound test on top of a "Star Seeker" mode "closely based on the arcade game" — not a straight DIMM-image conversion ([GAME_FORMATS.md](../GAME_FORMATS.md) note; [lunaticobscurity blog](https://lunaticobscurity.blogspot.com/2023/01/doki-doki-idol-star-seeker-remix.html); [video-games-museum.com](https://www.video-games-museum.com/en/game/Doki-Doki-Idol-Star-Seeker-Remix/68/2/27665)) |
| Community ports | None found — searched the dreamcast-talk.com and forums.sega-mag.com Naomi-conversion tracking threads (both HTTP 403 to direct fetch; search-snippet only, no `starseek`-specific hits) and generic web search for "starseek dreamcast port" / "dokidoki idol star seeker dreamcast conversion"; no GitHub or homebrew repo surfaced. Moot in practice — an official Remix already exists (above). |
| Representative choice | Only member of its family (no clones) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/starseek.zip`
Attract/demo reached: **demo** — full attract-mode gameplay reached and looped through
multiple stages, well past a static title card: title screen at `shot-243s.png`; live
hex-panel gameplay demos with in-game rules-tutorial overlays across Stage 1-1 through
Stage 4 at `shot-060s.png`/`shot-121s.png`/`shot-365s.png`/`shot-487s.png`/`shot-548s.png`;
ending on a full high-score ranking screen ("ハイスコア☆ランキング DOKIDOKI IDOL",
FREE PLAY) at `shot-609s.png`. Sidecar `capture.coverage = "demo"` (battery writes `null`
— set explicitly in this pass after reviewing the shots).
Screenshots: `evidence/starseek/shot-060s.png` · `shot-243s.png` · `shot-365s.png` ·
`shot-548s.png` · `shot-609s.png` (curated to 5; battery originally captured 10 —
`assessments/starseek.metrics.json` → `capture.screenshots` lists all of them).
Anomalies: none — single clean leg, ran the full 600 s capture window.

## 4. Memory fit (axis: 65.9)

| Region | Scored value | DC cap | u | Sub-score | Evidence |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 18,221,631 | 16,777,216 | 1.086 | 69.5 | `nz_above_cap` 8,238,047 informational under content-keying (placement, not volume, kb §6 item 8); write-truth address peak 33,554,404 (informational); `dma_high_water` 0 — expected for a PIO-only load (§5), `nz_total` still measured and used |
| VRAM (FB-masked content: `content_total` + 2×`fb_bytes`) | 8,050,897 + 2×614,400 = 9,279,697 | 8,388,608 | 1.106 | 65.9 | **binding region** — `nz_above_cap` 5,552,543 informational; address peak 16,336,896; `regs_last` shows a second framebuffer surface parked at `fb_w_sof2=0xc00000` |
| ARAM (content volume, `content_total`) | 1,542,037 | 2,097,152 | 0.735 | 100.0 | `peak` 8,257,552 is the boot-time "DMPD" ARAM-sweep fill, not content (kb §7 canary check cleared — `gate: null`); `nz_above_cap` 8, negligible |

Memory axis = min(69.5, 65.9, 100.0) = **65.9** — VRAM binds by a narrow margin ahead of
main RAM (u 1.106 vs 1.086); both regions sit modestly over cap (roughly +9–11%), not the
severe multi-× overflows that gate other titles in the campaign.

Watermarks (informational, content-scan — stale-data prone): main 33,554,404 ·
vram 16,336,896 · aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 100.0)

DMA events 0 · total 0 B · unique 0 B · re-read ratio 0.0 · steady-state 0.0 MB/min
(`short_window: false`) · PIO 13,311,414 B (12.7 MB)

Zero cart-DMA activity across the full 600 s capture — the entire ~12.7 MB working set
loads once via PIO during the boot/handoff window and the game never issues a cart DMA
read afterward. The scorer's formula (bandwidth 0 MB/min, re-read 0.0) yields a clean
100.0, and `short_window: false` confirms this is a genuine zero, not a data-insufficiency
artifact — consistent with a small, single-load puzzle title with no per-stage asset
streaming.

## 6. Guts (axis: 85.0)

Code 1,179,648 B (1.13 MB) · functions 732 · MMIO refs: scif 2, rtc 2, g2ext 60 ·
BIOS vector refs: none (`extra_bios_classes: 0`) · penalties applied: `eeprom_bios` (5),
`serial` (5), `rtc` (5) → 100 − 15 = 85.0
Carve: base `0x0c020000`, entry `0x0c020500`, header title `------- STAR SEEKER ------`.

`guts.sdk_strings` shows a NAOMI-era library stack that predates DC-specific naming:
NLOBJPUT/NLSPRITE/libspr (Ver 0.2, 1999), `KM1Naomi Ver 1.31` (Sep 1999), `NAOMI LIBRARY
Ver 0.9 AM R&D` (Aug 2000), AM2/AICAsoundDrv, Sequencer 1.33, nlajamma, libintr, libsnd,
the Katana-derived `sy*` system modules (syHw/syCache/sySq/syChain/syInt/syTmr/syMmu/syG2
— also seen in kurucham/tetkiwam), and NEC's KAMUI2/KAMUI-Darkness. No explicit
"for DREAMCAST"/"for DC" strings appear (unlike tetkiwam's `sd2 for DC Ver 2.50.18` or
kurucham's `sd2 for DC`) — consistent with a 2001 Naomi-only build and with
`similarity.sdk_overlap = "partial"` rather than `"full"`.

## 7. Controls (axis: 100.0)

Cabinet: MAME's generic `naomi` input port (2P, 8-way stick, 6 buttons) is the NAOMI I/O
board's electrical ceiling — `starseek` has no game-specific `INPUT_PORTS` override in
`naomi.cpp`, so this is not confirmed cabinet-panel documentation by itself. The strongest
evidence is primary: the game's own captured attract-mode rules-tutorial screens read
"Aボタンで赤いカーソル部分のパネルをめくることができます" ("Press the A button to flip
the panel at the red cursor", `shot-060s.png`) and "Bボタンはマーキングをします" ("The B
button marks/flags", `shot-548s.png`) — directly from the arcade binary. This confirms a
minesweeper-style scheme: directional cursor movement + 2 action buttons per player
(A = reveal, B = flag), well inside the NAOMI ceiling. The official DC *Remix* release
plays the same "Star Seeker" mode on a stock DC control pad, corroborating a clean 1:1
mapping.
Proposed DC mapping: d-pad/analog stick for cursor, A = reveal, B = flag, Start.
Sources: in-game rules-tutorial screenshots `assessments/evidence/starseek/shot-060s.png`
+ `shot-548s.png` (primary, arcade binary); MAME src/mame/sega/naomi.cpp @59e7c0b
INPUT_PORTS `naomi`; [arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=starseek)
(8-way joystick + 6-button JVS standard declaration, 2P — MAME-derived capability ceiling,
not an independently verified cabinet panel); [lunaticobscurity blog](https://lunaticobscurity.blogspot.com/2023/01/doki-doki-idol-star-seeker-remix.html)
(Remix DC gameplay: directional cursor + A=clear flagged hexagons, B=place flag; "closely
based on the arcade game"); [video-games-museum.com](https://www.video-games-museum.com/en/game/Doki-Doki-Idol-Star-Seeker-Remix/68/2/27665)
(confirms official DC release, G.Rev, 2002, 1-2 players).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 65.9^.40 · 100.0^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **79.0** (A)
Similarity inputs: developer no (G.Rev ≠ reference), SDK overlap partial (§6), loader
match yes.

## 9. Risks & notes

- **Memory axis binds narrowly, not catastrophically.** VRAM (u 1.106) and main RAM
  (u 1.086) are both modest overflows (+9–11%), unlike the 2–4× multiples that gate other
  titles in this campaign — a port likely needs light asset/texture trimming or
  double-buffer budget tightening, not a redesign.
- VRAM's second framebuffer surface parks at `fb_w_sof2=0xc00000` (12 MB address) — the
  same high-address pattern noted elsewhere as a relocatable, position-independent asset
  placement (kurucham's `vram-assets-c00000.png`, OSB-bank compaction precedent);
  informational, not necessarily a hard placement constraint.
- **Zero cart-DMA streaming (§5) means the entire working set loads once via PIO at boot.**
  The capture loops the same demo stages (1-1 through 4) repeatedly across 600 s, so this
  is likely a complete picture, but a port should still verify there's no late-game/extra-
  stage asset streaming outside what attract mode exercises.
- Rendering and actual gameplay must be verified on real DC hardware per the working-style
  rule — this assessment is Flycast-emulated only.
- An official DC port already exists (*Remix*, 2002, §2) — any new port project should
  treat it as reference material / prior art, though it is not a byte-identical conversion
  of this GD-ROM.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-12 | 79.0 (A) | First assessment: single clean 600 s capture, demo coverage; VRAM binds narrowly (u=1.106) just ahead of main (u=1.086); controls set to `stick` (100.0) from primary in-game tutorial screenshots + MAME `naomi` generic port; zero cart-DMA streaming (PIO-only load) scores streaming 100.0 |
