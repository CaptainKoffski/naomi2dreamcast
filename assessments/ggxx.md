# Guilty Gear XX (GDL-0011) (`ggxx`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **55.4 (B)** |
| Bottom line | VRAM is the binding constraint — FB-masked content fit 12,845,936 B against the 8 MB cap (u 1.53) drags the memory axis down to 28.7 even though main RAM and ARAM each sit barely over their own 1x line (u ≈ 1.01); streaming (89.2) and guts (85.0) are clean and controls is a perfect 1:1 stick+6-button fit (100.0), but memory's 40% weight caps the geometric mean at B — no DC port, official or fan, exists for this title to validate against. |
| Assessed | capture 2026-08-10 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `ggxx` (no clones — `parent: null` in controls.json; the other GGXX revisions — `ggxxrl`/`ggxxrlo`, `ggxxsla`, `ggxxac` — are separate MAME parents/families in `GAME_FORMATS.md`, not clones of this set) |
| Maker / year | Arc System Works, 2002 (sidecar `maker`/`year`) |
| Genre / format | Fighting ★ (2D versus fighter), **GD-ROM** GDL-0011, machine `naomigd` (controls.json) |
| Official DC port | **No.** GGXX itself never reached Dreamcast — arcade (NAOMI, May 2002) went straight to **PlayStation 2** as *Guilty Gear X2* (JP Dec 2002, NA Feb 2003); later revisions (#Reload, Slash, Accent Core) spread to Xbox/PC/PSP/PS3/Wii/Vita/Steam, never DC ([Wikipedia: Guilty Gear X2](https://en.wikipedia.org/wiki/Guilty_Gear_X2), accessed 2026-08-10; [sega-naomi.eu Naomi→home-console port list](https://www.sega-naomi.eu/forum/viewtopic.php?t=2185) lists "Guilty Gear XX (PC,PS2,Psp)" with no DC entry, while the prequel is listed as "Guilty Gear X (Dreamcast,PC,PS2)") |
| Community ports | None found for GGXX itself (searched 2026-08-10). The **prequel** *Guilty Gear X* did get an official DC port (2000) and its Atomiswave-hardware *Ver.1.5* revision got a 2020 fan homebrew DC conversion by megavolt85 — but that is different hardware (Atomiswave, not Naomi) and a different game, not this title |
| Representative choice | Only member of its family (MAME parent, no clones) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/ggxx.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`; the full loop is visible
across the 10 battery shots: settings prompt → title screen → VS intro → ranking table →
live attract gameplay.
Screenshots (5 kept of 10):
- `evidence/ggxx/shot-060s.png` — settings/EEPROM prompt: "EEPROM ID or Version Err /
  Please Execute GameTestMode / Press Start Button key To Start Default Setting"
- `evidence/ggxx/shot-182s.png` — title screen: "THE MIDNIGHT CARNIVAL", FREE PLAY
- `evidence/ggxx/shot-243s.png` — attract VS intro: "MAY VERSUS FAUST", PUSH START 1P OR 2P
- `evidence/ggxx/shot-304s.png` — attract ranking table (NORMAL MODE, AXL/CHIPP/POTEMKIN/EDDIE)
- `evidence/ggxx/shot-609s.png` — live attract-demo gameplay: two characters mid-match on a
  stage background, HUD visible — the frame that sets coverage to `demo`

Anomalies: on first boot the game showed the EEPROM/settings prompt above (`shot-060s.png`,
`shot-121s.png` — identical frames, both pre-default-accept); the human operator pressed
Start to accept the default EEPROM settings during the 2026-08-10 capture, after which the
game booted into its normal title/attract cycle (title at `shot-182s.png` onward). This is a
legitimate operator assist — input via the normal Start control, not a metrics or harness
edit — the same evidence class as `gwing2`'s operator observation
(`assessments/gwing2.md` §3). The early capture window (through ~121 s) therefore includes
the static settings screen, and it is the attract loop afterward — VS intros, ranking
tables, and the live demo match at `shot-609s.png` — that set the per-sample memory/streaming
maxima the scores below are keyed on.

## 4. Memory fit (axis: 28.7)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 16,955,636 | 16,777,216 | 1.0106 | 83.1 | address peak 33,548,416 (u 2.00, informational) · `nz_above_cap` 3,355,344 (content bytes found above the cap address, informational) · `dma_high_water` 33,226,752 (informational-only from v6 on) |
| VRAM (FB-masked content + 2×FB) | 12,845,936 (content_total 11,617,136 + 2×fb_bytes 614,400) | 8,388,608 | 1.5314 | 28.7 | raw address peak 16,746,496 (u 1.996) is the extent artifact, not content · `nz_total` 12,119,626 · `nz_above_cap` 5,778,914 |
| ARAM (content volume, fill-excluded, `content_total`) | 2,142,107 | 2,097,152 | 1.0214 | 81.1 | address peak 8,355,712 (u 3.98, informational — near a full 8 MiB bank write, not scored) · `nz_above_cap` 131,583 |

Watermarks (informational, content-scan — stale-data prone): main 33,548,416 ·
vram 16,746,496 · aram 8,388,608 (the aram watermark exactly matches the classic
boot-time "DMPD" full-bank fill value seen elsewhere in the campaign, not content —
`content_total` above is what's scored). Main watermark (33,548,416) tracks
`dma_high_water` (33,226,752) closely (1.01×) — no divergence flag.

VRAM is the binding region: its sub-score (28.7) equals the memory axis, since
`region_score()`'s `min()` makes regions non-tradeable — main RAM and ARAM both clear
80+ even though each also sits just over its own 1x line.

## 5. Cart streaming (axis: 89.2)

DMA events 1,005 · total 78,281,632 B (74.7 MB) · unique 56,772,512 B (54.1 MB) ·
re-read ratio 0.2748 · steady-state 7.562 MB/min (`short_window: false`) ·
PIO bootstrap `pio_bytes` 1,050,496 B (GD DIMM PIO boot-load, handoff `trigger=pio`).
Light re-read on a large (54.1 MB) unique working set — a clean, cache-friendly streaming
profile, the best-scoring axis of the five.

## 6. Guts (axis: 85.0)

Code 1,048,576 B (carve `base 0x0c020000`, entry `0x0c021000`, header title
"GUILTY GEAR XX VERSION 1.0") · functions 1,922 · MMIO refs: scif 1, rtc 2, g2ext 121 ·
BIOS vector refs: {} · penalties: `eeprom_bios`+`serial`+`rtc` → −15.
SDK strings show the classic Sega Naomi AM R&D stack: NAOMI LIBRARY Ver 0.8 AM R&D,
syHw Ver 1.08am, syG2 Ver 1.02.02, KM1Naomi Ver 1.33.0.0, syCache/syChain/syInt/syTmr/syMmu/
syExtChk, libsnd Ver.1.05a, nlajamma Ver 1.01, NLOBJPUT Ver 0.99, NLSPRITE Ver 0.2 —
the same SDK family noted in other assessed GD-ROM titles (partial overlap, not a
DC-specific toolchain).

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 2P panel, 8-way joystick + 6 buttons, up to 2 concurrent players,
2 coin chutes. `controls.device_class = stick`. MAME input ports: `naomi`
(INPUT_PORTS_START at naomi.cpp @59e7c0b line 1506 — the same shared digital-stick + 6-button
block cited for `trgheart`, since both sets declare `input_ports="naomi"` in their `GAME()` row).
Proposed DC mapping: d-pad for the 8-way stick + DC pad's 4 face buttons (A/B/X/Y) for
Punch/Kick/Slash/Hard Slash, L/R analog triggers used digitally for Dust/Taunt — precedented
by the official PS2 port's own control scheme, which maps the same 6 arcade inputs onto
□/△/×/○ + L1/R1/L2/R2 ([Dustloop Wiki, GGI/Controls](https://dustloop.com/w/GGI/Controls)).
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia MAME machine DB](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=ggxx)
("Joystick 8 ways", "6" buttons, "Up to 2 players (solo, 2 concurrents)", "2" coin slots).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 28.7^.40 · 89.2^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **55.4 (B)**
Similarity inputs: developer match no, SDK overlap **partial**, cart loader match **yes**
→ 70.0.

## 9. Risks & notes

- VRAM's gap is the real work item: u 1.53 on FB-masked content is the largest overage of
  the three regions by a wide margin — a port needs meaningful texture/asset-store trims to
  clear the 8 MB cap, not just a placement fix.
- Main RAM and ARAM both sit just barely over their 1x line (u ≈ 1.01 each) — real but
  small overages; either would likely clear with a modest trim, unlike VRAM's larger gap.
- Main-RAM write-truth includes CPU writes (v6+); `dma_high_water` is informational-only,
  not scored.
- No official or fan DC port exists for this exact title (unlike `gwing2`/`trgheart`), so
  there is no shipped downport to validate memory/control choices against — this assessment
  is first-principles, not reference-checked.
- Rendering must be verified on real DC hardware per working-style rule — this is an
  emulator-only (Flycast) measurement.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-10 | 55.4 B | initial assessment — fighter cohort, fresh v9 capture |
