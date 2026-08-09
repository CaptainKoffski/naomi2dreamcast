# Melty Blood Actress Again Version A (Japan, Rev A) (`mbaa`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **55.9 (B)** |
| Bottom line | VRAM is the binding constraint — FB-masked content fit 10,574,173 B against the 8 MB cap (u 1.2605) drags the memory axis to 39.6, even though main RAM (u 0.5187, 100.0) sits comfortably under its cap and ARAM (u 0.9804, 86.5) stays just inside its own 1x line; streaming (65.0) and guts (85.0) are mid/clean and controls is a perfect 1:1 stick+6-button fit (100.0), but similarity drops to 40.0 because `mbaa` is a **cart** (naomim4) title and so misses the cart-loader match every GD-ROM anchor gets — the geometric mean lands in tier B. This joins `ggxx` (55.4 B) and `ggxxac` (65.4 A) as the third fighter-cohort title where VRAM/ARAM sit past their 1x line; no DC port, official or fan, exists for this exact title to validate against. |
| Assessed | capture 2026-08-10 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `mbaa` (covers: no clones tracked in `GAME_FORMATS.md` — `parent: null` in `tools/assess/out/controls.json`; upstream MAME `naomi.cpp` @59e7c0b line 11119 also lists `mbaao` "Melty Blood Actress Again (Japan)" as a clone of this set, but that ROM isn't a separate row in this repo's catalog) |
| Maker / year | Type-Moon / Ecole, 2008 (sidecar `maker`/`year`) |
| Genre / format | Fighting ★ (2D versus fighter), **cart** (naomim4), machine `naomim4` (`tools/assess/out/controls.json`) — no GD-ROM disc/DIMM bootstrap; `rom_used` is a single cart image `naomi/mbaa.zip`, not a BIOS.zip + `.chd` pair |
| Official DC port | **No.** `GAME_FORMATS.md` marks "No" for `mbaa`. Arcade NAOMI release Sep 19 2008 (Japan) went to **PlayStation 2** (Aug 20, 2009, published by Ecole; new secret characters and an alternate PS2-exclusive Option Mode) — Dreamcast never appears in this title's port history ([Wikipedia: Melty Blood](https://en.wikipedia.org/wiki/Melty_Blood), accessed 2026-08-10). The earlier *Melty Blood Act Cadenza* entries (`meltybld` GDL-0028C, `meltyb` GDL-0039A) in this same queue are themselves other NAOMI **GD-ROM arcade** cabinets, not Dreamcast home-console ports — `GAME_FORMATS.md` marks "No" DC port for those too, so no member of the Melty Blood family assessed in this campaign has shipped on retail DC |
| Community ports | None found for `mbaa`/Actress Again on Dreamcast (searched 2026-08-10) — no fan/homebrew NAOMI→DC conversion of this title exists. Its gameplay lineage continued on **PC**, not DC: the arcade update *Melty Blood Actress Again Current Code* (MBAACC, arcade July 2010) was bundled on PC with *Carnival Phantasm* vol. 3 (Dec 31 2011); mirror moon's fan translation effort was superseded when Arc System Works published an official English Steam release (Apr 19 2016) ([RPG Site: "Branching Path: Melty Blood Actress Again Current Code's Steam Version"](https://www.rpgsite.net/feature/4802-branching-path-melty-blood-actress-again-current-codes-steam-version), accessed 2026-08-10) |
| Representative choice | Only member of its family tracked in `GAME_FORMATS.md` (no clones) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/mbaa.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`; the very first shot
(t=60 s) is already past any settings/EEPROM prompt, showing the Melty Blood logo splash, and
by t=304 s the run is cycling through live "DEMONSTRATION"-tagged attract battles between
different character pairs on different stages.
Screenshots (5 kept of 10):
- `evidence/mbaa/shot-060s.png` — logo splash: "MELTY BLOOD" title card over a glowing
  circle/hand motif — already past any settings prompt at the first capture
- `evidence/mbaa/shot-243s.png` — stylized attract-intro reel: a character rendered in a
  red/cyan multi-exposure glitch effect over scrolling text — part of the pre-gameplay
  attract sequence, not a calibration screen
- `evidence/mbaa/shot-304s.png` — live attract-demo battle: Tohno Akiha vs. Sion Tatari on a
  night-street stage, "MELTY BLOOD Actress Again DEMONSTRATION" HUD banner — the frame that
  sets coverage to `demo`
- `evidence/mbaa/shot-487s.png` — "TYPE-MOON" / "ECOLE" developer/publisher credit splash
  (attract-mode credits screen)
- `evidence/mbaa/shot-609s.png` — live attract-demo battle: Len vs. Akiha Vermilion on a
  ruined-city stage, "MELTY BLOOD Actress Again DEMONSTRATION" HUD banner, PRESS START BUTTON

Anomalies: no settings/EEPROM prompt (the "press Start for defaults" cohort class) was
observed anywhere in this capture — `shot-060s.png` (t=60 s) already shows the title/logo
splash, so either the EEPROM was already primed ahead of this capture or this build clears
the prompt without an operator Start press inside the first minute; no operator intervention
was needed or recorded for this run. `shot-121s.png` (dropped from the curated set) is a
near-blank black frame with only a "FREE PLAY" HUD string — a normal fade transition between
attract-loop segments, not a stuck/static screen.

## 4. Memory fit (axis: 39.6)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 8,702,591 | 16,777,216 | 0.5187 | 100.0 | address peak 33,499,296 (u 1.9967, informational) · `nz_above_cap` 4,515,711 (content bytes found above the cap address, informational) · `dma_high_water` 33,352,544 (informational-only from v6 on) |
| VRAM (FB-masked content + 2×FB) | 10,574,173 (content_total 9,345,373 + 2×fb_bytes 614,400) | 8,388,608 | 1.2605 | 39.6 | raw address peak 16,428,032 (u 1.9584) is the extent artifact, not content · `nz_total` 9,502,550 · `nz_above_cap` 5,192,901 |
| ARAM (content volume, fill-excluded, `content_total`) | 2,056,134 | 2,097,152 | 0.9804 | 86.5 | address peak 6,291,504 (u 3.000, informational — short of the full 8 MiB bank ceiling other campaign titles show, not scored) · `nz_above_cap` 552,412 |

Watermarks (informational, content-scan — stale-data prone): main 33,499,296 ·
vram 16,428,032 · aram 8,388,608 (the aram watermark hits the classic boot-time full-bank
fill value seen elsewhere in the campaign, not content — `content_total` above is what's
scored; note this diverges from the ARAMPROFILE address peak of 6,291,504, consistent with
the watermark's stale-data-prone caveat). Main watermark (33,499,296) tracks
`dma_high_water` (33,352,544) closely (1.0044×) — no divergence flag.

VRAM is the binding region: its sub-score (39.6) equals the memory axis, since
`region_score()`'s `min()` makes regions non-tradeable — main RAM clears 100 and ARAM clears
86.5 even though ARAM also sits just under its own 1x line. Across the fighter cohort so far,
VRAM/ARAM overage keeps recurring as the soft spot: `ggxx`'s VRAM u 1.5314 (sub-score 28.7,
`assessments/ggxx.md` §4), `mbaa`'s VRAM u 1.2605 here, and `ggxxac`'s ARAM u 1.2318
(sub-score 43.3, `assessments/ggxxac.md` §4) — all three Naomi fighters measured this session
land in the same 1.0–1.6x memory-overage band on their binding region.

## 5. Cart streaming (axis: 65.0)

DMA events 1,924 · total 174,675,968 B (166.6 MB) · unique 73,175,040 B (69.8 MB) · re-read
ratio 0.5811 · steady-state 15.758 MB/min (`short_window: false`) · PIO bootstrap
`pio_bytes` 2,212,390 B (2.1 MB, cart ROM board PIO boot-load into DIMM RAM, handoff
`trigger=pio`) — `mbaa` is a naomim4 **cart**, so this is the cart's own initial boot block
loaded via the G1-bus PIO path, not a GD-ROM DIMM firmware bootstrap (no disc/CD image is
mounted at all for this title).
Heavier re-read (0.58) than the GD-ROM fighters (`ggxx` 0.27, `ggxxac` 0.31) on a smaller
unique working set (69.8 MB vs. 54–57 MB) — a cart-streaming profile that re-reads roughly
double the fraction of its unique data, dragging the streaming axis down from the ~89 both GD
siblings score to 65.0.

## 6. Guts (axis: 85.0)

Code 1,572,864 B (carve `base 0x8c020000`, entry `0x8c021000`, header title "MELTY BLOOD
ACTRESS AGAIN") · functions 4,456 · MMIO refs: scif 25, rtc 3, g2ext 271 · BIOS vector refs:
{} · penalties: `eeprom_bios`+`serial`+`rtc` → −15 (same three flags/penalty as `ggxx` and
`ggxxac`).
SDK strings show the same Sega Naomi AM R&D library family as the GD-ROM fighters, plus a
much heavier CRI middleware footprint: Sega `syXxx` common libs (`syStartKn`, `syMalloc`,
`syRtc`, `syFbr`, `syFs`, `syCallback`, `syMng`, `syBtKn`, `syVideoKn`, `syHwKn`, `syCache`,
`syChain`, `syInt`, `syTmr`, `syMmu`, `syG2`), Sega 3D middleware (`Ninja2`, `Nindows2`,
`Kunoichi2 Library for NAOMI Version 2.07`), and CRI's ADX audio codec (`ADXT`/`ADXF`/`SFA`)
plus Sofdec video playback (`mwPly`/`mwSfd`/`CRI SFD`/`SFH`/`MPS`/`MPV`) — the same
Sofdec/CRIWARE family `ggxxac` shows for its FMV credit splash. One literal build string
reads `"Nindows2 for DREAMCAST version %s"` — direct textual evidence the windowing library
is shared code with Dreamcast, not a NAOMI-only build. SDK strings also include GD-ROM file
API calls (`gdCiGetFileSize`, `gdCiReqRd`, `gdRmc Ver 0.94`) despite `mbaa` being cart-format
with no disc mounted — almost certainly unused/dead code paths carried by the shared Naomi
SDK rather than evidence of actual GD-ROM access, consistent with `machine=naomim4` in
`tools/assess/out/controls.json`. Same SDK-family overlap classification as `ggxx`/`ggxxac`
(partial, not DC-specific).

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 2P panel, 8-way joystick + 6 buttons (digital), up to 2 concurrent
players, 2 coin chutes. `controls.device_class = stick`. MAME input ports: `naomi`
(`INPUT_PORTS_START(naomi)` at naomi.cpp @59e7c0b line 1506 — the same shared digital-stick +
6-button block `ggxx`/`ggxxac` cite, since `mbaa`'s own `GAME()` row at naomi.cpp line 11120
also declares `input_ports="naomi"`). The game itself only drives 4 of those 6 buttons: A
(weak), B (medium), C (heavy), D (Shield/guard) — Melty Blood's signature parry mechanic
([Wikipedia: Melty Blood](https://en.wikipedia.org/wiki/Melty_Blood), accessed 2026-08-10).
Proposed DC mapping: d-pad for the 8-way stick + DC pad's 4 face buttons (A/B/X/Y) for
weak/medium/heavy/Shield — an even cleaner 1:1 fit than the 6-button GGXX titles need, since
MBAA's 4 active inputs match the DC pad's 4 face buttons exactly with no spare-button
mapping required. Precedented by the official PS2 port's own layout — Square/Triangle/
Circle/X for weak/medium/heavy/Shield, i.e. the 4 attack inputs mapped straight onto the
console pad's 4 face buttons with no shoulder buttons used (per community report on
[GameFAQs: "I have such a hard time with the ps2 controller..."](https://gamefaqs.gamespot.com/boards/959354-melty-blood-actress-again/51131939),
accessed 2026-08-10 — a forum source, lower authority than the MAME/hardware-DB citations
below, cited only for the button-layout detail).
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi` (line 1506; `GAME()` row
for `mbaa` at line 11120 declares `machine=naomim4`, `input_ports=naomi`);
[arcadeitalia MAME machine DB](https://adb.arcadeitalia.net/?mame=mbaa) ("Joystick 8 ways",
"6" buttons, "Up to 2 players (solo, 2 concurrents)", "2" coin slots).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 39.6^.40 · 65.0^.20 · 85.0^.20 · 100.0^.10 · 40.0^.10 = **55.9 (B)**
Similarity inputs: developer match no, SDK overlap **partial**, cart loader match **no** → 40.0.
Cart loader match is false for structural reasons — `mbaa` is a naomim4 cart, and every
other cart-format title assessed in this campaign (`illvelo`, `gunsur2`, `marstv`) also
scores `cart_loader_match: false`; this is not a title-specific defect, it pulls similarity
down from the GD-ROM fighters' 70.0 to 40.0 purely because the loader-match check is keyed
against the GD-ROM anchor titles' DIMM firmware path.

## 9. Risks & notes

- VRAM is the real work item: u 1.2605 on FB-masked content is a genuine overage — a port
  needs a meaningful texture/asset-store trim to clear the 8 MB cap, more than a placement
  fix alone would buy. It sits between `ggxxac`'s VRAM u 1.0427 (barely over) and `ggxx`'s
  u 1.5314 (the largest of the three fighters measured this session).
- ARAM sits close under its cap (u 0.9804, sub-score 86.5) — not currently binding, but with
  little headroom; worth re-checking after any VRAM-driven asset rework in case sound-data
  placement shifts.
- Main RAM is comfortably under cap (u 0.5187, sub-score 100.0) — no work item here.
- Streaming's heavier re-read ratio (0.5811, vs. 0.27–0.31 for the GD-ROM fighters) on a
  smaller unique working set (69.8 MB) is a cart-specific profile worth understanding before
  assuming the GD-ROM siblings' streaming behavior carries over — the cart's PIO/DMA path
  differs structurally from GD-ROM DIMM streaming (§5).
- Similarity's 40.0 (vs. 70.0 for the GD-ROM fighters) is driven entirely by
  `cart_loader_match: false`, a structural cart-vs-GD-ROM attribute shared by every
  cart-format title in this campaign, not a `mbaa`-specific finding (§8).
- Main-RAM write-truth includes CPU writes (v6+); `dma_high_water` is informational-only,
  not scored.
- No official or fan DC port exists for this exact title (PS2 got the 2009 console port,
  MBAACC's later lineage went to PC/Steam, not DC) — this assessment is first-principles,
  not reference-checked.
- Rendering must be verified on real DC hardware per working-style rule — this is an
  emulator-only (Flycast) measurement.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-10 | 55.9 B | initial assessment — fighter cohort, fresh v9 capture |
