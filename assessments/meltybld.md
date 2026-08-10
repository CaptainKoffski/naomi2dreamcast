# Melty Blood Act Cadenza Ver. A (Japan) (GDL-0028C) (`meltybld`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **59.6** (B) |
| Bottom line | ARAM is the binding constraint — compacted content volume `content_total` 2,758,787 B against the 2 MB cap (u 1.3155) drags the memory axis to 37.4, even though VRAM (FB-masked fit 7,874,493 B, u 0.9387, sub-score 89.6) and main RAM (`nz_total` 15,540,720 B, u 0.9263, sub-score 90.5) both clear their caps comfortably — `region_score()`'s `min()` makes ARAM's 37.4 the memory axis, a harder bind than sibling `meltyb`'s VRAM-bound 50.9. Streaming is mid (67.5), and its re-read ratio (0.5993) is the **highest** measured anywhere in the Melty Blood family so far — above `meltyb`'s own 0.5595 and `mbaa`'s 0.5811 — strengthening the case that this is a genuine Act Cadenza-engine streaming trait rather than a one-off. Controls is a perfect 1:1 stick fit (100.0); unlike `meltyb` (Version B2), this Ver. A revision predates the 5th "shortcut" button added in the December 2006 arcade "Ver. B" update, so the game itself only drives 4 of the cabinet's 6 buttons. Guts is clean (95.0): 1.5 MiB code, 597 functions, near-zero MMIO surface (`eeprom_bios` only) — measured after the 2026-08-10 carve mirror-mask fix recovered the `.dat` (the same mixed-view header signature as `meltyb`), lifting similarity to 70.0 (SDK overlap partial + GD-ROM loader match). No DC port, official or fan, exists for any Melty Blood Act Cadenza revision. |
| Assessed | capture 2026-08-10 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — guts/similarity re-scored 2026-08-10 after the carve mirror-mask fix (see History) |

## 2. Identity

| | |
|---|---|
| Set / family | `meltybld` (covers: `meltyblo` — clone in MAME `naomi.cpp` @59e7c0b line 11267: `GAME( 2005, meltyblo, meltybld, naomigd, naomi, ... )`, parent `meltybld`; `GAME_FORMATS.md` lists `meltyblo` "Melty Blood Act Cadenza (Japan) (GDL-0028)" as "clone of `meltybld`") |
| Maker / year | Ecole Software, 2005 (sidecar `maker`/`year`) |
| Genre / format | Fighting ★ (2D versus fighter), **GD-ROM**, machine `naomigd` (`naomi.cpp` @59e7c0b line 11270 `GAME()` row for `meltybld` declares `machine=naomigd`, `input_ports=naomi`) — `rom_used` `naomi/meltybld.zip` is a GD-ROM DIMM-firmware bootstrap (BIOS zip + `.chd` pair), same format class as sibling `meltyb` (`assessments/meltyb.md` §2) |
| Official DC port | **No.** `GAME_FORMATS.md` marks "No" for `meltybld`. This is the **original** Act Cadenza arcade release (March 2005, [Wikipedia: Melty Blood](https://en.wikipedia.org/wiki/Melty_Blood), accessed 2026-08-10) — GDL-0028C, "Ver. A", is the newest revision of that original release (following unreleased/internal GDL-0028A/0028B revision markers noted in `naomi.cpp`'s comments, both skipped in the ROM set list). The PS2 console port followed in August 2006, and that PS2 build was then used as the base for the arcade "Ver. B" update (GDL-0039, Dec 23 2006) assessed separately as `meltyb`/`meltybo`. Dreamcast never appears in any Act Cadenza port history for either revision line |
| Community ports | None found for `meltybld`/Act Cadenza Ver. A on Dreamcast (searched 2026-08-10) — no fan/homebrew NAOMI→DC conversion of this title exists, matching the same finding already recorded for the Ver. B2 sibling `meltyb` (`assessments/meltyb.md` §2); research not repeated in full since it is the same underlying game/engine and franchise |
| Representative choice | GDL-0028C ("Ver. A") is the newest revision of the original Act Cadenza GD-ROM release tracked in `GAME_FORMATS.md`, and covers clone `meltyblo` (GDL-0028) per the `naomi.cpp` parent link above. The later Act Cadenza "Ver. B" line (`meltyb`/`meltybo`, GDL-0039/0039A) is a separate, already-assessed `QUEUE.md` row (66.9 A after the carve-fix rescore) — the family is split across two representative sets because the Ver. B update is a materially different build (new 5th button, roster changes) layered on a PS2-derived base, not merely a revision stamp |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/meltybld.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`; by t=121 s the run already shows a
live "DEMONSTRATION"-tagged attract battle, and the loop cycles through further battles, a
ranking-records screen, and back to the pre-title movie-codec splash by t=609 s — a full
demo-loop cycle observed inside the capture window.
Screenshots (5 kept of 10):
- `evidence/meltybld/shot-121s.png` — live attract-demo battle: Tohno Akiha vs. Warachia in a
  red-tinted pillared hall, "4 HITS!"/"1448 Damage"/"Critical!!" combo HUD, "PRESS START
  BUTTON" and "MELTY BLOOD Act Cadenza DEMONSTRATION" banners — the frame that sets coverage
  to `demo`
- `evidence/meltybld/shot-243s.png` — live attract-demo battle: Umiduka Satsuki vs. Akiha
  Vermilion in a mansion/staircase interior with a fountain, "PLEASE WAIT" HUD, "MELTY BLOOD
  Act Cadenza DEMONSTRATION" banner — a different match-up than t=121 s, confirming the loop
  cycles through multiple bouts
- `evidence/meltybld/shot-365s.png` — "RANKING RECORDS" high-score table (FREE PLAY): Ciel
  8th, Tohno Akiha 9th, Hisui&Kohaku 10th — confirms attract mode's non-battle screens are
  also reached
- `evidence/meltybld/shot-548s.png` — title-sequence frame: "MELTY BLOOD Act Cadenza" logo in
  red/white text over a purple gradient backdrop
- `evidence/meltybld/shot-609s.png` — Sofdec/ADX movie-codec splash logos, the opening frame
  of the pre-title FMV sequence — confirms the attract/demo loop completed a full cycle and
  restarted within the 600 s+ capture window

Anomalies: `shot-304s.png` (t=304 s, dropped from the curated set) is a blown-out white
motion-blur frame — consistent with a scene-transition wipe inside the attract sequence
(it sits directly between the live battle at t=243 s and the "RANKING RECORDS" screen at
t=365 s), not a stuck/static or corrupted screen. `shot-060s.png` (also dropped) shows an
in-progress intro-movie fade frame ("原作『月姫』" / "original story: Tsukihime" over a moon
backdrop), the same fade-transition class noted for sibling `meltyb`'s equivalent early frame
(`assessments/meltyb.md` §3). No settings/EEPROM prompt (the "press Start for defaults"
cohort class) was observed in any of the 10 captures — the same no-prompt pattern `meltyb`
and `mbaa` showed (`assessments/meltyb.md` §3) — so no operator intervention was needed or
recorded for this run.

## 4. Memory fit (axis: 37.4)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 15,540,720 | 16,777,216 | 0.9263 | 90.5 | address peak 33,554,412 (u 1.99999, informational — sits right at the 2x gate boundary as an extent artifact only) · `nz_above_cap` 11,355,499 (content bytes found above the cap address, informational) · `dma_high_water` 33,554,432 (informational-only from v6 on, tracks peak within 20 B) |
| VRAM (FB-masked content + 2×FB) | 7,874,493 (content_total 6,645,693 + 2×fb_bytes 614,400) | 8,388,608 | 0.9387 | 89.6 | raw address peak 15,669,772 (u 1.8680) is the extent artifact, not content · `nz_total` 7,073,574 · `nz_above_cap` 3,548,795 |
| ARAM (content volume, fill-excluded, `content_total`) | 2,758,787 | 2,097,152 | 1.3155 | **37.4** | address peak 3,662,624 (u 1.7465, informational) · `nz_above_cap` 1,226,866 |

Watermarks (informational, content-scan — stale-data prone): main 33,554,412 · vram
15,669,772 · aram 8,388,608 (the aram watermark hits the classic boot-time full-bank fill
value seen elsewhere in the campaign — including `meltyb`, `assessments/meltyb.md` §4 — not
content; `content_total` above is what's scored). Main watermark (33,554,412) tracks
`dma_high_water` (33,554,432) within 20 B — no divergence flag.

ARAM is the binding region here: its sub-score (37.4) equals the memory axis, since
`region_score()`'s `min()` makes regions non-tradeable — main RAM clears 90.5 and VRAM clears
89.6 even though both also sit close to their own 1x lines. This is the opposite bind from
sibling `meltyb`, where VRAM was the binding region (u 1.1895, sub-score 50.9,
`assessments/meltyb.md` §4) and ARAM merely grazed its cap (u 1.0248, sub-score 80.5,
non-binding); here the two revisions swap which region binds, and `meltybld`'s ARAM overage
(u 1.3155) is considerably worse than `meltyb`'s (u 1.0248) — content volume needs to shrink
by roughly 0.6 MB (`content_total` 2,758,787 vs. 2,097,152 cap) to clear the line.

## 5. Cart streaming (axis: 67.5)

DMA events 1,398 · total 145,588,224 B (138.8 MiB) · unique 58,339,328 B (55.6 MiB) · re-read
ratio 0.5993 · steady-state 13.616 MB/min (`short_window: false`) · PIO bootstrap `pio_bytes`
1,574,208 B (1.5 MB, GD-ROM DIMM firmware boot-load into DIMM RAM, handoff `trigger=pio`).
`meltybld` is GD-ROM format, so this PIO block is the DIMM firmware's own bootstrap ahead of
G1-bus DMA streaming, structurally the same path sibling `meltyb` and the other GD-ROM
fighters use.

`meltybld`'s re-read ratio (0.5993) is the **highest** measured across the whole Melty Blood
family this campaign — above `meltyb`'s own 0.5595 (`assessments/meltyb.md` §5), above the
cart title `mbaa`'s 0.5811, and roughly double the other GD-ROM fighter siblings `ggxx`
0.2748, `ggxxac` 0.3101, `ggxxsla` 0.2975 (`*.metrics.json` `streaming.reread_ratio`) — on a
smaller unique working set (55.6 MB vs. `meltyb`'s 70.7 MB). With now two Act Cadenza
revisions (Ver. A here, Ver. B2 `meltyb`) both showing anomalously heavy re-read behavior
relative to the other GD-ROM fighters, this strengthens — but does not confirm — the
hypothesis raised in `meltyb.md` §9 that the elevated re-read ratio is a genuine Act Cadenza
engine streaming characteristic rather than a one-off carve/measurement artifact (§9).

## 6. Guts (axis: 95.0)

Code 1,572,864 B (1.5 MiB) · functions 597 · MMIO refs: scif 0, rtc 0, g2ext 1 ·
BIOS vector refs: none · penalties applied: `eeprom_bios` only (`extra_bios_classes` 0) → 95.0.
Carved at base `0x0c020000`, entry `0x8c021000`, header title `MELTY BLOOD ACT CADENZA`.
The original v9 scan failed with `guts.error` = `"static scan: entrypoint 0x8c021000 outside
carved image 0xc020000..0xc1a0000"` — **byte-identical** to sibling `meltyb`'s failure, and
the carve meta now shows why: the load table declares its RAM targets in the physical view
(`0x0c02xxxx`) while the entrypoint uses the SH-4 P1 cached mirror (`0x8c021000`) — the same
bytes on hardware (29-bit external address space, SH7750 HW manual §3.3). The 2026-08-10 fix
masks both sides of `carve_boot.py`'s entrypoint-bounds check to physical (`& 0x1FFFFFFF`);
calibration-guard golden hashes reproduced bit-for-bit across the fix (kb §10), so no battery
version bump. The mixed-view header is systematic to the Act Cadenza engine — both GD-ROM
revisions hit it identically.
SDK strings (sidecar `guts.sdk_strings`, 497 recovered) include the game's own debug-menu
text (`CHANGE DEBUG MODE`, `PLAY VS DEMO`, `PLAY OPENING MOVIE`) alongside shared-SDK entries
that feed similarity's `sdk_overlap: partial` (§8).

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 2P panel, 8-way joystick + 6 buttons (digital), up to 2 concurrent
players, 2 coin chutes. `controls.device_class = stick`. MAME input ports: `naomi`
(`INPUT_PORTS_START(naomi)` at `naomi.cpp` @59e7c0b line 1506 — the same shared digital-stick +
6-button block `meltyb`/`ggxx`/`ggxxac`/`mbaa` cite; `meltybld`'s own `GAME()` row at line
11270 declares `machine=naomigd`, `input_ports=naomi`; `meltyblo` clone row at line 11267).

Unlike sibling `meltyb` (Version B2), this Ver. A revision (GDL-0028C, March 2005) predates
the arcade "Ver. B" update (Dec 23 2006) that Wikipedia records as adding the 5th
"contextual"/shortcut button: *"It also introduced a fifth button that served as a contextual
action depending on the situation and the direction held on the joystick when pressed"*
([Wikipedia: Melty Blood](https://en.wikipedia.org/wiki/Melty_Blood), accessed 2026-08-10,
Ver. B section — text implies Ver. A did not have this button). So `meltybld` uses only 4 of
the cabinet's 6 physical buttons: A (weak), B (medium), C (strong), D (Shield) — Melty Blood's
signature parry mechanic — with no macro/shortcut button. Cabinet-level axis score is
unaffected (still `stick` class → 100.0); the game-side button count is a porting detail only.
Proposed DC mapping: d-pad for the 8-way stick + DC pad's 4 face buttons (A/B/X/Y) for
weak/medium/strong/Shield — a straight 1:1 fit with no macro-button trick needed (contrast
`meltyb`'s shoulder-button proposal for its extra 5th button, `assessments/meltyb.md` §7).
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi` (line 1506; `GAME()` row
for `meltybld` at line 11270 declares `machine=naomigd`, `input_ports=naomi`; `meltyblo` clone
row at line 11267);
[arcadeitalia MAME machine DB](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=meltybld)
("Joystick 8 ways", "6" buttons, "Up to 2 players (solo, 2 concurrents)", "2" coin slots);
[Wikipedia: Melty Blood](https://en.wikipedia.org/wiki/Melty_Blood) (accessed 2026-08-10, for
the Ver. A vs. Ver. B 5th-button distinction).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 37.4^.40 · 67.5^.20 · 95.0^.20 · 100.0^.10 · 70.0^.10 = **59.6 (B)**
Similarity inputs: developer match no, SDK overlap **partial**, loader match **yes** → 70.0.
Developer match is false on its own merits — Ecole Software is not in
`assessments/reference/similarity-reference.json`'s `makers` list (Altron / Taito), same as
`meltyb` (`assessments/meltyb.md` §8). SDK overlap and loader match were both recovered by
the carve fix (§6), landing `meltybld` in the same 70.0 similarity band as its GD-ROM fighter
siblings.

Command run: `python3 tools/assess/rescore_static.py meltybld` → output
`meltybld: 59.6 B (guts 95.0)`.

## 9. Risks & notes

- The initial 45.3 B score was a lower bound from a carve-tool measurement gap, since
  resolved: the 2026-08-10 mirror-mask fix (§6) restored the guts axis (95.0) and lifted
  similarity 20.0 → 70.0, moving the final to 59.6 B with no change to any captured metric.
- ARAM is the real work item here: u 1.3155 on compacted content volume needs roughly 0.6 MB
  trimmed (downsample/ADPCM/stream, per the v7 volume-is-work ruling) to clear the 2 MB cap —
  this is the binding region for `meltybld`, unlike `meltyb` where VRAM bound instead (§4).
- VRAM sits close to but under its cap (u 0.9387, sub-score 89.6, 0 MB of work) — comfortable
  headroom, contrast `meltyb`'s binding VRAM overage (u 1.1895, `assessments/meltyb.md` §9).
- Main RAM is comfortably under cap (u 0.9263, sub-score 90.5) — similar margin to `meltyb`'s
  main-RAM utilization (u 0.9203), non-binding in both revisions.
- Streaming's re-read ratio (0.5993) is now the highest measured anywhere in the Melty Blood
  family — above both `meltyb` (0.5595) and `mbaa` (0.5811) — worth treating as a candidate
  genuine Act Cadenza-engine trait rather than assuming it's a per-title measurement artifact,
  though that has not been independently confirmed (§5).
- Main-RAM write-truth includes CPU writes (v6+); `dma_high_water` is informational-only, not
  scored.
- Ver. A (this title) uses only 4 of the cabinet's 6 buttons — no 5th shortcut button, added
  only in the later Ver. B arcade update (§7) — a simpler DC control mapping than `meltyb`'s.
- No official or fan DC port exists for any Act Cadenza revision (PS2 got the 2006 console
  port that the later Ver. B arcade update was itself based on; no member of the Melty Blood
  family assessed this campaign, including `mbaa` and `meltyb`, has shipped on retail DC) —
  this assessment is first-principles, not reference-checked.
- Rendering must be verified on real DC hardware per working-style rule — this is an
  emulator-only (Flycast) measurement.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-10 | 45.3 B | initial assessment — fighter cohort, fresh v9 capture; guts carve failed (mirror-address gap, lower-bound score) |
| v9 | 2026-08-10 | 59.6 B | static-only rescore after the carve mirror-mask fix (`carve_boot.py` entrypoint bounds now compared in physical view, `& 0x1FFFFFFF`; calibration goldens reproduced bit-for-bit, no battery bump): guts measured for the first time (95.0 — 1.5 MiB code, 597 funcs, `eeprom_bios` only), similarity 20.0 → 70.0 (`sdk_overlap` partial, `cart_loader_match` true); capture metrics untouched |
