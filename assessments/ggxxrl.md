# Guilty Gear XX #Reload (Japan, Rev A) (GDL-0019A) (`ggxxrl`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **55.4 (B)** |
| Bottom line | VRAM is again the binding constraint — FB-masked content fit 12,821,369 B (content_total 11,592,569 + 2×fb_bytes 1,228,800) against the 8 MB cap (u 1.5284) drags the memory axis down to 28.9, even though ARAM sits just over its own 1x line (u 1.0105, sub-score 83.1) and main RAM lands — for the first time in the family — fractionally *under* its cap (u 0.9955, sub-score 85.3); streaming (87.8) and guts (85.0) are clean and controls is a perfect 1:1 stick+6-button fit (100.0), but memory's 40% weight caps the geometric mean at B. This continues the VRAM-bound pattern seen in sibling `ggxx` (55.4 B, u 1.5314) and `ggxxsla` (58.6 B, u 1.4298), in contrast to `ggxxac`'s ARAM-bound reversal (65.4 A, u 1.2318) — three of the four assessed GGXX revisions are VRAM-bound, one is ARAM-bound. No DC port, official or fan, exists for this title to validate against. |
| Assessed | capture 2026-08-10 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `ggxxrl` — MAME parent (GDL-0019A); clone `ggxxrlo` (GDL-0019, no Rev A) shares the family (`naomi.cpp` @59e7c0b `ROM_START` blocks lines 8573/8586, `GAME()` rows 11256–11257; `controls.json` confirms `ggxxrlo.parent = "ggxxrl"`). The other GGXX revisions — `ggxx`, `ggxxsla`, `ggxxac` — are separate MAME parents/families in `GAME_FORMATS.md`, not clones of this set |
| Maker / year | Arc System Works, 2003 (sidecar `maker`/`year`) |
| Genre / format | Fighting ★ (2D versus fighter), **GD-ROM** GDL-0019A, machine `naomigd` (`controls.json`) |
| Official DC port | **No.** #Reload (arcade NAOMI GD-ROM, March 26, 2003 Japan) went to **PlayStation 2** (July 31, 2003 Japan), **Xbox** (April 29, 2004 Japan; September 14, 2004 NA), **Windows** (August 12, 2005 Japan), **PSP** (September 29, 2005), and **Xbox 360** via Xbox Originals (June 16, 2008) — Dreamcast never appears in this port list ([Wikipedia: Guilty Gear X2 updated versions](https://en.wikipedia.org/wiki/Guilty_Gear_X2_updated_versions), accessed 2026-08-10). Consistent with siblings `ggxx`/`ggxxsla`/`ggxxac` (`assessments/ggxx.md` / `ggxxsla.md` / `ggxxac.md` §2) — no GGXX revision reached Dreamcast |
| Community ports | None found for #Reload itself (searched 2026-08-10). As with the other siblings, the prequel *Guilty Gear X* got an official DC port (2000) and its Atomiswave *Ver.1.5* revision got a 2020 fan homebrew DC conversion by megavolt85 — different hardware (Atomiswave, not Naomi) and a different game, not this title |
| Representative choice | MAME parent set (`ggxxrl` GDL-0019A, the newer revision) over clone `ggxxrlo` (GDL-0019) — consistent with the campaign's newest-revision-in-original-region preference (spec §1) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/ggxxrl.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`; `shot-487s.png` shows an explicit
"DEMO PLAY" caption over live in-engine combat, and `shot-304s.png` shows a second live attract-combat
frame — the 10 battery shots otherwise cycle title/VS-intro art and M.O.M./Normal-mode ranking tables.
Screenshots (5 kept of 10):
- `evidence/ggxxrl/shot-060s.png` — title/VS-intro art: Millia close-up (yellow palette), "PUSH START
  1P OR 2P", FREE PLAY — already at the attract cycle at the very first capture, confirming the
  persisted EEPROM setting (see Anomalies below) carried through to this run
- `evidence/ggxxrl/shot-182s.png` — M.O.M. MODE attract ranking table (Baiken/Testament/Faust/Jam)
- `evidence/ggxxrl/shot-304s.png` — live attract-demo gameplay: a character mid-jump-kick over a
  bridge/shrine stage, small HUD sprites visible in both top corners
- `evidence/ggxxrl/shot-487s.png` — live attract-demo gameplay with an explicit "DEMO PLAY" caption:
  May (guitar) vs. Potemkin on an industrial rail-yard stage — the frame that sets coverage to `demo`
- `evidence/ggxxrl/shot-609s.png` — Guilty Gear XX title-logo screen (starburst wordmark), "PUSH START
  1P OR 2P", FREE PLAY — loop restart

Anomalies: this title has an unusual two-run history. The **first** battery attempt on 2026-08-10
false-parked it `G1 broken: no-render-after-handoff` — all 10 screenshots were byte-identical
(md5 `c37dc6dd1e7790d214bf0d96574caa74` for every file), frozen the entire 600 s window on Naomi's
stock EEPROM-defaults prompt ("EEPROM ID or Version Err / Please Execute GameTestMode / Press Start
Button key To Start Default Setting") because no operator answered it. That sparse white-on-black
prompt text is real rendered content (`memory.vram.content_total` 32,334 B) but fell under the
battery's 64 KiB no-render heuristic (`tools/assess/run_battery.py` FIX 3), the same false-negative
class already noted for this family in `docs/kb/assessment-tooling.md` §4.n. Diagnosis (full report:
`/private/tmp/claude-501/-Users-captainkoffski-AntigravityProjects-naomi2dreamcast/b87713d0-79d2-452d-a47c-8fba381d0e2a/scratchpad/ggxxrl-report.md`)
proved the dump good — `gdl-0019a.chd` chdman SHA1 `95b017c2faedf19cabfd1e6cd99a67ac27d76422` is an
exact match to `naomi.cpp` @59e7c0b line 8578, and the sibling `gdl-0019.chd` (the `ggxxrlo` clone's
disc, line 8591 SHA1 `1915534f366934110e7cd6641bb817f47000150f`) sits unused in the same folder — a
normal shared-family layout, not a wrong-disc load. Nothing was committed from that run.

**Today's attended re-run** is the capture scored here: the operator pressed Start once at the EEPROM
prompt — a legitimate assist via the normal Start control, the same evidence class as `ggxx`'s own
first-boot EEPROM prompt (`assessments/ggxx.md` §3, kb §4.vi item 1) — after which the setting
persisted, so this run (and every future run) boots straight to the title/attract cycle with no
prompt at all. All 10 shots this time are unique (distinct file sizes/content, unlike the frozen
first attempt), the capture ran the full 600 s window, and there is no gate.

## 4. Memory fit (axis: 28.9)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 16,702,155 | 16,777,216 | 0.9955 | 85.3 | address peak 33,548,416 (u 2.00, informational) · `nz_above_cap` 3,121,605 (content bytes found above the cap address, informational) · `dma_high_water` 33,226,752 (informational-only from v6 on) |
| VRAM (FB-masked content + 2×FB) | 12,821,369 (content_total 11,592,569 + 2×fb_bytes 1,228,800) | 8,388,608 | 1.5284 | 28.9 | raw address peak 16,746,496 (u 1.996) is the extent artifact, not content · `nz_total` 11,990,172 · `nz_above_cap` 5,710,443 |
| ARAM (content volume, fill-excluded, `content_total`) | 2,119,118 | 2,097,152 | 1.0105 | 83.1 | address peak 8,355,712 (u 3.984, informational — near a full 8 MiB bank write, not scored) · `nz_above_cap` 115,492 |

Watermarks (informational, content-scan — stale-data prone): main 33,548,416 · vram 16,746,496 ·
aram 8,388,608 (the aram watermark matches the classic boot-time full-bank fill pattern seen
elsewhere in the campaign, not content — `content_total` above is what's scored). Main watermark
(33,548,416) tracks `dma_high_water` (33,226,752) closely (1.01×) — no divergence flag.

VRAM is the binding region: its sub-score (28.9) equals the memory axis, since `region_score()`'s
`min()` makes regions non-tradeable — ARAM clears 83+ and main RAM clears 85+ even though ARAM also
sits just over its own 1x line. Main RAM's u (0.9955) is the only sub-1.0 main-RAM fit seen across
the four assessed GGXX revisions so far (`ggxx` u 1.0106, `ggxxsla` u 1.0157, `ggxxac` u 1.0564) —
see §9 for the cross-title comparison.

## 5. Cart streaming (axis: 87.8)

DMA events 1,207 · total 88,462,432 B (84.4 MB) · unique 58,857,056 B (56.1 MB) · re-read ratio
0.3347 · steady-state 6.338 MB/min (`short_window: false`) · PIO bootstrap `pio_bytes` 1,116,096 B
(1.1 MB, GD DIMM PIO boot-load, handoff `trigger=pio`).
Light re-read on a large (56.1 MB) unique working set — a clean, cache-friendly streaming profile, in
line with siblings `ggxx` (89.2), `ggxxsla` (90.1), and `ggxxac` (89.5), though marginally lower here
on a somewhat higher re-read ratio (0.3347 vs. `ggxx`'s 0.2748).

## 6. Guts (axis: 85.0)

Code 1,114,112 B (carve `base 0x0c020000`, entry `0x0c021000`, header title
"GUILTYGEARXX#RELOAD1.0") · functions 1,943 · MMIO refs: scif 1, rtc 2, g2ext 122 · BIOS vector
refs: {} · penalties: `eeprom_bios`+`serial`+`rtc` → −15.
SDK strings show the same Sega Naomi AM R&D stack noted for `ggxx`/`ggxxsla`/`ggxxac`: NAOMI LIBRARY
Ver 0.8 AM R&D, syHw Ver 1.08am, syG2 Ver 1.02.02, KM1Naomi Ver 1.33.0.0, syCache/syChain/syInt/
syTmr/syMmu/syExtChk, libsnd Ver.1.05a, nlajamma Ver 1.01, NLOBJPUT Ver 0.99, NLSPRITE Ver 0.2 — no
CRIWARE/Sofdec video-middleware string is present here (unlike `ggxxac`'s FMV credit splash,
`assessments/ggxxac.md` §6), matching `ggxx`'s and `ggxxsla`'s SDK profile and this capture's
screenshots. The carved code also contains the exact EEPROM-prompt string set ("EEPROM ID or Version
ErrPelase Execute GameTestMode", "Press Start Button key To Start Default Setting") — the same text
that froze the first, unattended battery run described in §3. Same SDK family overlap classification
as the other siblings (partial, not DC-specific).

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 2P panel, 8-way joystick + 6 buttons, up to 2 concurrent players, 2 coin
chutes. `controls.device_class = stick`. MAME input ports: `naomi` (`INPUT_PORTS_START(naomi)` at
naomi.cpp @59e7c0b line 1506 — the same shared digital-stick + 6-button block `ggxx`/`ggxxsla`/
`ggxxac` cite, since `ggxxrl`'s `GAME()` row at naomi.cpp line 11257 also declares
`input_ports="naomi"`).
Proposed DC mapping: d-pad for the 8-way stick + DC pad's 4 face buttons (A/B/X/Y) for
Punch/Kick/Slash/Hard Slash, L/R analog triggers used digitally for Dust/Taunt — the same P/K/S/HS/D
six-button command set carried across every GGXX revision ([Dustloop Wiki, GGACR/Controls](https://www.dustloop.com/w/GGACR/Controls),
the closest dedicated Dustloop controls reference — no #Reload-specific controls subpage was
confirmed accessible).
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia MAME machine DB](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=ggxxrl)
("Joystick 8 ways", "6" buttons, "Up to 2 players (solo, 2 concurrents)", "2" coin slots).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 28.9^.40 · 87.8^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **55.4 (B)**
Similarity inputs: developer match no, SDK overlap **partial**, cart loader match **yes** → 70.0.

## 9. Risks & notes

- VRAM's gap is the real work item, matching the pattern from `ggxx`: u 1.5284 here vs `ggxx`'s
  u 1.5314 (`assessments/ggxx.md` §4) — the two GGXX parent revisions have nearly identical
  VRAM-bound profiles, both meaningfully over the 8 MB line, unlike `ggxxac`'s near-cap VRAM fit
  (u 1.0427, `assessments/ggxxac.md` §4) or `ggxxsla`'s milder overage (u 1.4298,
  `assessments/ggxxsla.md` §4). A port needs meaningful texture/asset trims to clear the cap, not
  just a placement fix — same conclusion as `ggxx`.
- Main RAM is the cleanest fit of the four GGXX titles assessed: u 0.9955, fractionally *under* the
  16 MB cap — the only GGXX revision so far that doesn't sit just over its own 1x line (`ggxx`
  u 1.0106, `ggxxsla` u 1.0157, `ggxxac` u 1.0564) — no main-RAM work needed here.
- ARAM sits just over its 1x line (u 1.0105) — a real but modest overage, close to `ggxx`'s
  u 1.0214, well under `ggxxac`'s u 1.2318 and just above `ggxxsla`'s near-perfect u 0.9989.
- Main-RAM write-truth includes CPU writes (v6+); `dma_high_water` is informational-only, not
  scored.
- No official or fan DC port exists for this exact title (#Reload went PS2/Xbox/Windows/PSP/Xbox
  360, never DC) — this assessment is first-principles, not reference-checked, the same caveat
  noted for `ggxx`/`ggxxsla`/`ggxxac`.
- This title's first battery run false-parked on an unattended EEPROM-defaults prompt (§3) — worth a
  kb note that GGXX-family EEPROM defaults are per-title/operator-gated and will misfire the
  no-render heuristic on any future first-boot capture of a title in this state (the removed
  `no-eeprom-180s` auto-abort was not a substitute — kb §4.n).
- Rendering must be verified on real DC hardware per working-style rule — this is an emulator-only
  (Flycast) measurement.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-10 | — (parked) | first attempt — unattended run froze on the EEPROM-defaults prompt for the full 600 s window (all 10 shots byte-identical); false-parked `G1 broken: no-render-after-handoff` by the 64 KiB no-render heuristic misreading sparse prompt text; diagnosed as a tooling/process gap, not a dump/game break (chd SHA1 verified against MAME, wrong-disc ruled out); nothing committed |
| v9 | 2026-08-10 | 55.4 B | attended re-run — operator pressed Start once at the EEPROM prompt (persisted for all future runs); full 600 s capture, all 10 shots unique, no gate — fighter cohort, this assessment |
