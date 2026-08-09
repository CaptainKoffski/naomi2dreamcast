# Guilty Gear XX Accent Core (Japan) (GDL-0041) (`ggxxac`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **65.4 (A)** |
| Bottom line | ARAM is the binding constraint this run — content-volume fit of 2,583,214 B against the 2 MB cap (u 1.2318) drags the memory axis to 43.3, worse than main RAM (u 1.0564) and VRAM (u 1.0427, both just past their own 1x line); streaming (89.5) and guts (85.0) are clean and controls is a perfect 1:1 stick+6-button fit (100.0) — the geometric mean lands in tier A despite memory's 40% weight. This is a reversal from sibling `ggxx` (55.4 B, `assessments/ggxx.md`), whose binding region was VRAM (u 1.53), not ARAM — no DC port, official or fan, exists for this exact title to validate against. |
| Assessed | capture 2026-08-10 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `ggxxac` (no clones — `parent: null` in controls.json / "parent" in `GAME_FORMATS.md`; the other GGXX revisions — `ggxx`, `ggxxrl`/`ggxxrlo`, `ggxxsla` — are separate MAME parents/families, not clones of this set) |
| Maker / year | Arc System Works, 2006 (sidecar `maker`/`year`) |
| Genre / format | Fighting ★ (2D versus fighter), **GD-ROM** GDL-0041, machine `naomigd` (controls.json) |
| Official DC port | **No.** Accent Core (arcade NAOMI, Dec 2006 Japan) went straight to **PlayStation 2** and **Wii** (2006–2007); later revisions (Plus, Plus R) spread to PSP/Xbox 360/PS3/Vita/Switch/Steam — Dreamcast never appears in any revision's port list ([Wikipedia: Guilty Gear XX Accent Core](https://en.wikipedia.org/wiki/Guilty_Gear_XX_Accent_Core), accessed 2026-08-10; [arcade-history.com machine record, model GDL-0041](https://www.arcade-history.com/?n=guilty-gear-xx-accent-core-model-gdl-0041&page=detail&id=10267) confirms the arcade platform is "Sega NAOMI GD-ROM by SEGA Corp.", not Dreamcast — some search-engine summaries conflate the NAOMI GD-ROM release date with a Dreamcast release, which the primary port-list and hardware-catalog sources above do not support) |
| Community ports | None found for Accent Core itself (searched 2026-08-10). As with `ggxx` (`assessments/ggxx.md` §2), the prequel *Guilty Gear X* got an official DC port (2000) and its Atomiswave *Ver.1.5* revision got a 2020 fan homebrew DC conversion — different hardware (Atomiswave, not Naomi) and a different game, not this title |
| Representative choice | Only member of its family (MAME parent, no clones) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/ggxxac.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`; the game is already on its
title screen at the very first shot and cycles through character/VS intros, a ranking table, a
video-tech credit splash, and a live attract battle across the 10 battery shots.
Screenshots (5 kept of 10):
- `evidence/ggxxac/shot-060s.png` — title screen: character art (Testament), "PRESS START BUTTON",
  FREE PLAY — already past any settings prompt at the first capture
- `evidence/ggxxac/shot-182s.png` — attract ranking table (reset/blank "RANKING TABLE … ARCADE MODE")
- `evidence/ggxxac/shot-365s.png` — live attract-demo battle: two characters (a broom-riding fairy
  familiar and a scythe-wielding fighter) mid-action over a forest "Fairy Planet" stage — the frame
  that sets coverage to `demo`
- `evidence/ggxxac/shot-487s.png` — "Technology by CRIWARE" / Sofdec middleware credit splash
  (video-playback tech, attract-mode FMV segment)
- `evidence/ggxxac/shot-609s.png` — attract VS stance: two characters facing off on a cherry-blossom
  shrine stage, PRESS START BUTTON

Anomalies: no settings/EEPROM prompt was observed anywhere in this capture — contrast sibling
`ggxx`, whose first two shots showed a blank-EEPROM "Press Start Button key To Start Default
Setting" prompt that required operator assist before the game proceeded to its title screen
(`assessments/ggxx.md` §3). Here `shot-060s.png` (t=60 s) already shows the title screen, so
either the EEPROM was already primed ahead of this capture or this build/region clears the prompt
without requiring a Start press inside the first minute; no operator intervention was needed or
recorded for this run.

## 4. Memory fit (axis: 43.3)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 17,723,850 | 16,777,216 | 1.0564 | 74.8 | address peak 33,538,136 (u 1.999, informational) · `nz_above_cap` 3,659,089 (content bytes found above the cap address, informational) · `dma_high_water` 33,169,408 (informational-only from v6 on) |
| VRAM (FB-masked content + 2×FB) | 8,746,460 (content_total 7,517,660 + 2×fb_bytes 614,400) | 8,388,608 | 1.0427 | 77.3 | raw address peak 14,624,195 (u 1.743) is the extent artifact, not content · `nz_total` 7,903,184 · `nz_above_cap` 3,620,153 |
| ARAM (content volume, fill-excluded, `content_total`) | 2,583,214 | 2,097,152 | 1.2318 | 43.3 | address peak 8,355,712 (u 3.984, informational — near a full 8 MiB bank write, not scored) · `nz_above_cap` 574,850 |

Watermarks (informational, content-scan — stale-data prone): main 33,538,136 · vram 14,624,195 ·
aram 8,388,608 (the aram watermark matches the classic boot-time full-bank fill pattern seen
elsewhere in the campaign, not content — `content_total` above is what's scored). Main watermark
(33,538,136) tracks `dma_high_water` (33,169,408) closely (1.011×) — no divergence flag.

ARAM is the binding region: its sub-score (43.3) equals the memory axis, since `region_score()`'s
`min()` makes regions non-tradeable — main RAM and VRAM both clear 74+ even though each also sits
just over its own 1x line. This is a reversal from `ggxx`, where VRAM (u 1.5314, sub-score 28.7)
was the binding region and ARAM sat barely over 1.0x (u 1.0214) — see §9 for the cross-title
comparison.

## 5. Cart streaming (axis: 89.5)

DMA events 1,175 · total 87,127,552 B (83.1 MB) · unique 60,107,776 B (57.3 MB) · re-read ratio
0.3101 · steady-state 5.793 MB/min (`short_window: false`) · PIO bootstrap `pio_bytes` 1,574,784 B
(1.5 MB, GD DIMM PIO boot-load, handoff `trigger=pio`).
Light re-read on a large (57.3 MB) unique working set — a clean, cache-friendly streaming profile,
the best-scoring axis of the five (edging out `ggxx`'s 89.2).

## 6. Guts (axis: 85.0)

Code 1,572,864 B (carve `base 0x0c020000`, entry `0x0c021000`, header title "GUILTY GEAR XX ACCENT
CORE") · functions 2,203 · MMIO refs: scif 1, rtc 2, g2ext 197 · BIOS vector refs: {} ·
penalties: `eeprom_bios`+`serial`+`rtc` → −15.
SDK strings show the same Sega Naomi AM R&D stack noted for `ggxx`: NAOMI LIBRARY Ver 0.8 AM R&D,
syHw Ver 1.08am, syG2 Ver 1.02.02, KM1Naomi Ver 1.33.0.0, syCache/syChain/syInt/syTmr/syMmu/
syExtChk, nlajamma Ver 1.01, NLOBJPUT Ver 0.99, NLSPRITE Ver 0.2 — plus a CRI Sofdec/CRIWARE
video-playback middleware credit visible on screen (`shot-487s.png`) that `ggxx`'s SDK strings and
shots did not show, consistent with Accent Core adding FMV attract content over its predecessor.
Same SDK family overlap classification as `ggxx` (partial, not DC-specific).

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 2P panel, 8-way joystick + 6 buttons, up to 2 concurrent players, 2 coin
chutes. `controls.device_class = stick`. MAME input ports: `naomi` (`INPUT_PORTS_START(naomi)` at
naomi.cpp @59e7c0b line 1506 — the same shared digital-stick + 6-button block `ggxx` cites, since
`ggxxac`'s `GAME()` row at naomi.cpp line 11289 also declares `input_ports="naomi"`).
Proposed DC mapping: d-pad for the 8-way stick + DC pad's 4 face buttons (A/B/X/Y) for
Punch/Kick/Slash/Hard Slash, L/R analog triggers used digitally for Dust/Taunt — precedented by
the official PS2/console port's own control scheme, which maps the same P/K/S/H/D/Taunt inputs
used across the GGXX series ([Dustloop Wiki, GGACR/Controls](https://www.dustloop.com/w/GGACR/Controls)).
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia MAME machine DB](https://adb.arcadeitalia.net/?mame=ggxxac) ("Joystick 8 ways", "6"
buttons, "Up to 2 players (solo, 2 concurrents)", "2" coin slots).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 43.3^.40 · 89.5^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **65.4 (A)**
Similarity inputs: developer match no, SDK overlap **partial**, cart loader match **yes** → 70.0.

## 9. Risks & notes

- ARAM is the real work item here, a reversal from `ggxx`: u 1.2318 vs `ggxx`'s aram u 1.0214 —
  Accent Core's ARAM content grew to 2,583,214 B (vs `ggxx`'s 2,142,107 B, `assessments/ggxx.md`
  §4), while its VRAM content fit dropped to near the cap (u 1.0427, 8,746,460 B vs `ggxx`'s
  u 1.5314, 12,845,936 B). This looks like an asset-placement shift between the two engine builds
  (more sound/video buffering in ARAM, a trimmed VRAM texture footprint) rather than Accent Core
  being a straightforward superset of `ggxx`'s assets — a port project should verify ARAM usage
  first, not assume `ggxx`'s VRAM-bound profile carries over.
- Main RAM sits just over its 1x line (u 1.0564) — a real but modest overage, likely to clear with
  a modest trim, similar in kind (if larger in degree) to `ggxx`'s main-RAM overage (u 1.0106).
- Main-RAM write-truth includes CPU writes (v6+); `dma_high_water` is informational-only, not
  scored.
- No official or fan DC port exists for this exact title (Accent Core went PS2/Wii, later
  Plus/Plus R spread further, never DC) — this assessment is first-principles, not
  reference-checked, the same caveat noted for `ggxx`.
- Rendering must be verified on real DC hardware per working-style rule — this is an emulator-only
  (Flycast) measurement.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-10 | 65.4 A | initial assessment — fighter cohort, fresh v9 capture |
