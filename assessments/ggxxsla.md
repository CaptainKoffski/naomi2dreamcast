# Guilty Gear XX Slash (Japan, Rev A) (GDL-0033A) (`ggxxsla`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **58.6 (B)** |
| Bottom line | VRAM is again the binding constraint — FB-masked content fit 11,994,021 B (content_total 10,765,221 + 2×fb_bytes 614,400) against the 8 MB cap (u 1.4298) drags the memory axis down to 32.8, even though main RAM sits just over its own 1x line (u 1.0157, sub-score 82.2) and ARAM lands right at — fractionally *under* — its cap for the first time in the family (u 0.9989, sub-score 85.1); streaming (90.1) and guts (85.0) are clean and controls is a perfect 1:1 stick+6-button fit (100.0), but memory's 40% weight caps the geometric mean at B. This continues the VRAM-bound pattern seen in sibling `ggxx` (55.4 B, u 1.5314) rather than the ARAM-bound reversal seen in `ggxxac` (65.4 A, u 1.2318) — two of the three assessed GGXX revisions are VRAM-bound, one is ARAM-bound. No DC port, official or fan, exists for this title to validate against. |
| Assessed | capture 2026-08-10 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `ggxxsla` (no clones — `parent: null` in controls.json / "parent" in `GAME_FORMATS.md`; the other GGXX revisions — `ggxx`, `ggxxrl`/`ggxxrlo`, `ggxxac` — are separate MAME parents/families, not clones of this set) |
| Maker / year | Arc System Works, 2005 (sidecar `maker`/`year`) |
| Genre / format | Fighting ★ (2D versus fighter), **GD-ROM** GDL-0033A, machine `naomigd` (controls.json) |
| Official DC port | **No.** Slash (arcade NAOMI, Japan, September 28, 2005) went straight to **PlayStation 2**, Japan-exclusive, April 13, 2006 (re-released March 15, 2007 under Sega's "Sega the Best" budget line); Dreamcast never appears in its port history ([Wikipedia: Guilty Gear X2 updated versions](https://en.wikipedia.org/wiki/Guilty_Gear_X2_updated_versions), accessed 2026-08-10: "It was first released on September 28, 2005 for the arcades in Japan. In December 2005, it was reported that it would be ported for PS2, which occurred on April 13, 2006"). Consistent with siblings `ggxx`/`ggxxac` (`assessments/ggxx.md` / `ggxxac.md` §2), no GGXX revision reached Dreamcast. |
| Community ports | None found for Slash itself (searched 2026-08-10). As with `ggxx`/`ggxxac`, the prequel *Guilty Gear X* got an official DC port (2000) and its Atomiswave *Ver.1.5* revision got a 2020 fan homebrew DC conversion by megavolt85 — different hardware (Atomiswave, not Naomi) and a different game, not this title. |
| Representative choice | Only member of its family (MAME parent, no clones) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/ggxxsla.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`; the 10 battery shots show the
attract loop cycling title/VS-intro art, M.O.M./Normal-mode ranking tables, story-mode stills, and
two frames of live in-engine attract combat.
Screenshots (5 kept of 10):
- `evidence/ggxxsla/shot-060s.png` — title/VS-intro art (witch-hat character with a guitar-neck
  visible — visually consistent with I-No, a character new to this revision), "PRESS START
  BUTTON", FREE PLAY — already past any settings prompt at the first capture
- `evidence/ggxxsla/shot-121s.png` — live attract-demo gameplay: two characters mid-combo on a
  stage, HUD visible (Sol mid-combo, per operator/controller confirmation) — the frame that sets
  coverage to `demo`
- `evidence/ggxxsla/shot-182s.png` — M.O.M. MODE attract ranking table (Anji/Venom/Johnny/Dizzy)
- `evidence/ggxxsla/shot-243s.png` — attract VS-intro art, same witch-hat character, FREE PLAY
- `evidence/ggxxsla/shot-304s.png` — live attract-demo gameplay: two characters mid-battle on an
  airship/industrial stage (one in a dark coat, one in red wielding a rifle-like weapon)

Anomalies: none. No EEPROM/settings prompt was observed anywhere in this capture — contrast
sibling `ggxx`, whose first two shots showed a blank-EEPROM "Press Start Button key To Start
Default Setting" prompt that required operator assist (`assessments/ggxx.md` §3). Here
`shot-060s.png` (t=60 s) already shows title/VS-intro art, matching `ggxxac`'s clean-boot pattern
(`assessments/ggxxac.md` §3) rather than `ggxx`'s first-boot EEPROM class. Two shots not kept
(`shot-426s.png`, `shot-548s.png` — a rain/silhouette VS-intro screen and a second ranking table)
and one blank transition frame (`shot-609s.png`, solid black) were reviewed and confirmed
consistent with normal attract cycling, not anomalies.

## 4. Memory fit (axis: 32.8)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 17,040,264 | 16,777,216 | 1.0157 | 82.2 | address peak 33,548,416 (u 2.00, informational) · `nz_above_cap` 3,255,213 (content bytes found above the cap address, informational) · `dma_high_water` 33,226,752 (informational-only from v6 on) |
| VRAM (FB-masked content + 2×FB) | 11,994,021 (content_total 10,765,221 + 2×fb_bytes 614,400) | 8,388,608 | 1.4298 | 32.8 | raw address peak 16,736,256 (u 1.995) is the extent artifact, not content · `nz_total` 11,010,169 · `nz_above_cap` 5,190,510 |
| ARAM (content volume, fill-excluded, `content_total`) | 2,094,912 | 2,097,152 | 0.9989 | 85.1 | address peak 8,355,712 (u 3.984, informational — near a full 8 MiB bank write, not scored) · `nz_above_cap` 87,714 |

Watermarks (informational, content-scan — stale-data prone): main 33,548,416 · vram 16,736,256 ·
aram 8,388,608 (the aram watermark matches the classic boot-time full-bank fill pattern seen
elsewhere in the campaign, not content — `content_total` above is what's scored). Main watermark
(33,548,416) tracks `dma_high_water` (33,226,752) closely (1.01×) — no divergence flag.

VRAM is the binding region: its sub-score (32.8) equals the memory axis, since `region_score()`'s
`min()` makes regions non-tradeable — main RAM clears 82+ and ARAM clears 85+ even though main RAM
also sits just over its own 1x line. ARAM itself lands fractionally *under* its 1x line
(u 0.9989) — the tightest, cleanest ARAM fit of the three GGXX titles assessed so far (`ggxx` u
1.0214, `ggxxac` u 1.2318) — see §9 for the cross-title comparison.

## 5. Cart streaming (axis: 90.1)

DMA events 951 · total 84,951,584 B (81.0 MB) · unique 59,674,944 B (56.9 MB) · re-read ratio
0.2975 · steady-state 5.715 MB/min (`short_window: false`) · PIO bootstrap `pio_bytes` 1,247,104 B
(1.2 MB, GD DIMM PIO boot-load, handoff `trigger=pio`).
Light re-read on a large (56.9 MB) unique working set — a clean, cache-friendly streaming profile,
the best-scoring axis of the five, in line with siblings `ggxx` (89.2) and `ggxxac` (89.5).

## 6. Guts (axis: 85.0)

Code 1,245,184 B (carve `base 0x0c020000`, entry `0x0c021000`, header title "GUILTY GEAR XX
SLASH") · functions 2,004 · MMIO refs: scif 1, rtc 2, g2ext 152 · BIOS vector refs: {} ·
penalties: `eeprom_bios`+`serial`+`rtc` → −15.
SDK strings show the same Sega Naomi AM R&D stack noted for `ggxx`/`ggxxac`: NAOMI LIBRARY Ver 0.8
AM R&D, syHw Ver 1.08am, syG2 Ver 1.02.02, KM1Naomi Ver 1.33.0.0, syCache/syChain/syInt/syTmr/syMmu/
syExtChk, libsnd Ver.1.05, nlajamma Ver 1.01, NLOBJPUT Ver 0.99, NLSPRITE Ver 0.2 — no CRIWARE/Sofdec
video-middleware string is present here (unlike `ggxxac`'s FMV credit splash,
`assessments/ggxxac.md` §6), consistent with no such splash appearing in this capture's screenshots.
Same SDK family overlap classification as `ggxx`/`ggxxac` (partial, not DC-specific).

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 2P panel, 8-way joystick + 6 buttons, up to 2 concurrent players, 2 coin
chutes. `controls.device_class = stick`. MAME input ports: `naomi` (`INPUT_PORTS_START(naomi)` at
naomi.cpp @59e7c0b line 1506 — the same shared digital-stick + 6-button block `ggxx`/`ggxxac` cite,
since `ggxxsla`'s `GAME()` row also declares `input_ports="naomi"`).
Proposed DC mapping: d-pad for the 8-way stick + DC pad's 4 face buttons (A/B/X/Y) for
Punch/Kick/Slash/Hard Slash, L/R analog triggers used digitally for Dust/Taunt — the same P/K/S/HS/D
six-button command set carried across every GGXX revision, precedented by the official PS2 port's
own control scheme for this era of the series ([Dustloop Wiki, GGACR/Controls](https://www.dustloop.com/w/GGACR/Controls),
the closest dedicated Dustloop controls reference — no Slash-specific controls subpage was found).
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia MAME machine DB](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=ggxxsla)
("Joystick 8 ways", "6" buttons, "Up to 2 players (solo, 2 concurrents)", "2" coin slots).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 32.8^.40 · 90.1^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **58.6 (B)**
Similarity inputs: developer match no, SDK overlap **partial**, cart loader match **yes** → 70.0.

## 9. Risks & notes

- VRAM's gap is the real work item, continuing the pattern from `ggxx`: u 1.4298 here vs `ggxx`'s
  u 1.5314 (`assessments/ggxx.md` §4) — both meaningfully over the 8 MB line, unlike `ggxxac`'s
  near-cap VRAM fit (u 1.0427, `assessments/ggxxac.md` §4). A port needs meaningful texture/asset
  trims to clear the cap, not just a placement fix — same conclusion as `ggxx`.
- ARAM is the cleanest fit of the three GGXX titles assessed: u 0.9989 (fractionally under cap),
  vs `ggxx`'s u 1.0214 and `ggxxac`'s u 1.2318 — no ARAM work needed here, a reversal of the
  concern flagged in `ggxxac`'s §9.
- Main RAM sits just over its 1x line (u 1.0157) — a real but modest overage, similar in kind to
  both siblings (`ggxx` u 1.0106, `ggxxac` u 1.0564).
- Main-RAM write-truth includes CPU writes (v6+); `dma_high_water` is informational-only, not
  scored.
- No official or fan DC port exists for this exact title (Slash went PS2-only, Japan-exclusive) —
  this assessment is first-principles, not reference-checked, the same caveat noted for
  `ggxx`/`ggxxac`.
- Rendering must be verified on real DC hardware per working-style rule — this is an emulator-only
  (Flycast) measurement.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-10 | 58.6 B | initial assessment — fighter cohort, fresh v9 capture |
