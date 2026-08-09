# Illvelo (Illmatic Envelope) (Japan) (841-0059C) (`illvelo`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **79.8 (A)** |
| Bottom line | Milestone vertical shmup whose content fits DC budgets everywhere under current keying (main content 0.49× cap, VRAM fit 0.67×, ARAM 0.36×) — held below S only by the campaign's heaviest streaming — with in-family DC portability proven by Milestone's own Radirgy/Karous Dreamcast ports. |
| Assessed | capture 2026-08-08 · battery v8 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — scored under battery v9 keying (scoring-only re-score 2026-08-08, see History) |

## 2. Identity

| | |
|---|---|
| Set / family | `illvelo` (no clones — `parent: null` in controls.json; single GAME line, MAME src/mame/sega/naomi.cpp @59e7c0b line 11117) |
| Maker / year | Milestone, 2008 (JP arcade June 11, 2008 per [Shmups Wiki](https://www.shmups.wiki/library/Illmatic_Envelope_(Illvelo))). "Illvelo" is a contraction of "Illmatic Envelope" ([arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=illvelo)) |
| Genre / format | Shmup ★ (vertical, ROT270), **M4 cartridge** 841-0059C — 3× 512 Mb flash (`fpr-24437/24438/24439`, IC11 populated-but-empty) + PIC `317-5131-JPN`, rom_board id 5504, machine `naomim4` (MAME naomi.cpp @59e7c0b cart table ~line 668 + `ROM_START(illvelo)`). 88.4 MB zip. Note: arcadeitalia's "840-0059C" and "BAD DUMP" claims are both contradicted by the MAME source (841- third-party prefix; no `BAD_DUMP` macro anywhere in `ROM_START(illvelo)`) — primary source wins |
| Official DC port | No — widely expected as the next "last Dreamcast game ever" after Radirgy/Karous, but Milestone went Wii instead ([Engadget, Sep 2008](https://www.engadget.com/2008-09-10-illvelo-wii-is-real-velo.html)): standalone *Illvelo Wii* (JP 2008-11-13, [Shmups Wiki](https://www.shmups.wiki/library/Illmatic_Envelope_(Illvelo))), then *Milestone Shooting Collection 2* (Wii JP 2010-12-30, [MobyGames](https://www.mobygames.com/game/56616/milestone-shooting-collection-2/)), later *Sakura Flamingo Archives* (X360 2014, Shmups Wiki). `GAME_FORMATS.md` files it under "cancelled-but-unreleased DC ports", but no cancellation evidence was found — [Wikipedia's List of cancelled Dreamcast games](https://en.wikipedia.org/wiki/List_of_cancelled_Dreamcast_games) does not include it; "expected but never announced" is the accurate framing |
| Community ports | None found (searched 2026-08-03) — only generic Naomi-conversion threads on dreamcast-talk ([NAOMI Rom in GDI](https://www.dreamcast-talk.com/forum/viewtopic.php?t=15366), [Naomi and Naomi 2 conversion](https://dreamcast-talk.com/forum/viewtopic.php?t=14103)); the conversion scene targets GD-ROM sets, and an M4 cart needs a decrypted dump |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/illvelo.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`; full attract cycle observed (story text card, MADOWS "98se" ranking-window fake-desktop, live ILLMATIC ENVELOPE gameplay, MILESTONE INC. logo).
Screenshots: `evidence/illvelo/shot-060s.png` · `shot-121s.png` · `shot-304s.png` · `shot-548s.png` · `shot-609s.png` (black story-text card, MADOWS ranking-window desktop, live gameplay ×2, MILESTONE INC. logo card)
Anomalies: none — single clean leg.

## 4. Memory fit (axis: 100.0)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 8,294,066 | 16,777,216 | 0.494 | 100.0 | address peak 32,505,920 (`0x1F00040`, u 1.938, informational) — **first cart instance of the kb §6 item 3 shared-structure signature** (byte-identical to ikaruga/kurucham/ss2005, all GD-ROM) · nz_above_cap 5,526,495 · `dma_high_water` 27,289,280 (informational) |
| VRAM (FB-masked content + 2×FB) | 5,619,014 (content_total 4,390,214 + 2×`fb_bytes` 614,400) | 8,388,608 | 0.670 | 100.0 | rotated 480×640 panel (kb §3) — 480×640×2 is the same byte count as 640×480×2, sanity check unchanged · raw address peak 14,172,160 (u 1.690) is extent; nz_total 4,753,553 |
| ARAM (content volume, fill-excluded, `content_total`) | 762,858 | 2,097,152 | 0.364 | 100.0 | address peak 2,097,136 — 16 B under the cap (the Milestone engine's just-under-2-MiB sound budget, cf. karous) |

Watermarks (informational, content-scan — stale-data prone): main 32,505,920 ·
vram 14,172,160 · aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 60.1)

DMA events 3,244 · total 163.3 MB · unique 37.3 MB · re-read ratio 0.7715 ·
steady-state 16.063 MB/min (`short_window: false`) · PIO 2,099,776 B

## 6. Guts (axis: 85.0)

Code 2,097,152 B · functions 3,419 · MMIO refs: scif 2, rtc 3, g2ext 237 ·
BIOS vector refs: none · flags: `eeprom_bios`, `serial`, `rtc` → −15.
M4 boot blob carved at base `0x8c020000`, entry `0x8c021000` (header title
"ILLVELO JAPAN VERSION") — needs the `carve_boot.py` bit-30 mask (M4 encrypted-read
flag, MAME `src/mame/sega/naomim4.cpp:124-125` @59e7c0b, Flycast
`m4cartridge.cpp:115,132`; kb §4.q).
SDK strings: Kunoichi2 Library for NAOMI 2.07, Ninja2 2.01.011, `sd2 for DC` 2.50.17,
CRI ADX/Sofdec, NEC KAMUI2 (Sega libraries, Mar 2001 builds).

## 7. Controls (axis: 100.0)

Cabinet: 8-way stick + 3 buttons (A shot — hold to fire, B DOLL module control,
C MEGALOPHAZ bomb; auto-shield when not firing), 2P. `controls.device_class = stick`.
Proposed DC mapping: 1:1 on a stock DC pad; the Wii port shipped on standard pads,
confirming pad-friendliness.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi` (GAME line ROT270);
[Shmups Wiki](https://www.shmups.wiki/library/Illmatic_Envelope_(Illvelo));
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=illvelo)
(8-way joystick, JVS standard 6-button declaration, 2P);
[shmups forum ST thread](https://shmups.system11.org/viewtopic.php?f=5&t=67562).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 100.0^.40 · 60.1^.20 · 85.0^.20 · 100.0^.10 · 40.0^.10 = **79.8 (A)**
Similarity inputs: developer no (reference-list artifact — the reference `makers` list
contains only `Altron / Taito`, despite Milestone's directly relevant DC porting
pedigree), SDK overlap partial, loader match no.

## 9. Risks & notes

- **Port-planning takeaway: everything fits under content keying.** VRAM is the
  tightest region at 0.670×; main content is under half the DC's 16 MB; ARAM content
  is 0.364×.
- **Main RAM is address-sparse:** content volume is 8.3 MB but the touched address
  peak reaches 32,505,920 B (`0x1F00040`, 1.94× cap — the kb §6 item 3 shared-structure
  signature, first seen on a cart here, which weakened the GD-stream-cache-placement
  hypothesis) with 5.5 MB of nonzero bytes above the 16 MB line — a port needs
  layout/relocation attention.
- **Heaviest streaming in the campaign**: 163.3 MB total at 16.06 MB/min steady,
  re-read ratio 0.77 — cart re-reads on Naomi. A DC port streams from GD-ROM instead;
  the 37.3 MB unique working set is the number that matters for GD feasibility, and the
  re-read-heavy pattern is the small-working-set loop kb §6 item 2 flags as
  cache-friendly rather than disqualifying.
- **ROT270 vertical screen.** A DC port must handle tate/yoko presentation — solved
  in-family: Karous DC shipped with proper TATE support, Radirgy DC likewise
  ([Wikipedia Karous](https://en.wikipedia.org/wiki/Karous),
  [Radirgy](https://en.wikipedia.org/wiki/Radirgy)).
- MAME emulation status is the blanket naomi.cpp `GAME_FLAGS` (no per-title signal,
  kb §4.r) — the title runs and renders fully under our fork.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-03 | PARKED G3-ARAM | Full 8 MiB ARAM bank at boot read as 4.00× cap — the DIMM "DMPD" fill artifact; fifth full-bank park in the kb §6 tally, first on a cartridge. M4 static scan also failed (kb §4.q, §7) |
| v4 | 2026-08-04 | 43.9 (B) | Unparked by the v4 fill-excluded ARAM content metric (kb §7); 2026-08-06 `carve_boot.py` bit-30 fix unlocked M4 guts (85.0) + similarity (40.0) via `rescore_static.py` (kb §4.q) |
| v8 | 2026-08-08 | 34.7 (C) | Re-capture. VRAM re-keyed to FB-masked content + 2×FB → sub 100.0 (spec `2026-08-07-vram-fb-masking-design.md`); main write-truth first measured — address peak 32,505,920 `0x1F00040`, first cart instance of the kb §6 item 3 signature, sub 12.5 binding |
| v9 | 2026-08-08 | 79.8 (A) | Scoring-only re-key (no re-capture): main scored on content volume `nz_total` (spec `2026-08-08-main-content-rekey-design.md`); memory 100.0, tightest region moved to VRAM |
