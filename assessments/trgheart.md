# Trigger Heart Exelica Ver.A (Japan) (GDL-0036A) (`trgheart`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **86.5 (S)** |
| Bottom line | Everything fits under content keying — memory axis 100.0 (main content 3.9 MB, FB-masked VRAM 4.7 MB, ARAM 1.3 MB; the first assessed title whose ARAM *address* peak already fits the DC cap) — leaving re-read-heavy GD streaming (0.84 on a 14 MB working set) as the lowest axis; Warashi shipped this exact game on DC in 2007, so the title is reference/validation material, not a porting target. |
| Assessed | capture 2026-08-08 · battery v8 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — scored under battery v9 keying (scoring-only re-score 2026-08-08, see History) |

## 2. Identity

| | |
|---|---|
| Set / family | `trgheart` (covers: `trghearto` — GDL-0036 base revision, same PIC `317-5121-JPN` and default EEPROM, MAME naomi.cpp @59e7c0b lines 11282–11283, ROM_START 8875/8891) |
| Maker / year | Warashi, 2006 |
| Genre / format | Shmup ★ (vertical, ROT270), **GD-ROM** GDL-0036A, machine `naomigd` |
| Official DC port | **Yes** — *Triggerheart Exelica*, JP 2007-02-22, developed/published by Warashi; the Dreamcast's penultimate licensed release (two weeks before Karous). Adds Story/Arrange modes, configurable controls, **TATE** ([Wikipedia](https://en.wikipedia.org/wiki/Triggerheart_Exelica), [1CC Log](http://1cclog.blogspot.com/2024/10/triggerheart-exelica-dreamcast.html)). Later: X360 XBLA 2008, PS2 *Enhanced* 2009, Switch 2023 |
| Community ports | No Naomi→DC conversion found (searched 2026-08-08) — moot given the official port. The scene targets the DC release instead: English translation patch v1.0 by Derek Pascarella (analog support, 50/60 Hz fix; [dreamcast-talk t=19162](https://www.dreamcast-talk.com/forum/viewtopic.php?t=19162), [GitHub](https://github.com/DerekPascarella/TriggerheartExelica-EnglishPatchDreamcast)) |
| Representative choice | Ver.A parent — newest revision in the original region (spec §1); `trghearto` differs only by disc revision |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger=pio`) · run 600 s · rom: `naomi/trgheart.zip` (single clean zip leg)
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`; full attract cycle observed across the 10 battery shots: boot logo → Warashi calligraphy logo → live demo gameplay (DEMONSTRATION overlay) → title → ship/bullet-pattern intro → score ranking.
Screenshots (5 kept of 10):
- `evidence/trgheart/shot-060s.png` — boot: TRIGGERHEART EXELICA logo over circuit-board motif
- `evidence/trgheart/shot-182s.png` — attract gameplay, DEMONSTRATION + PRESS START overlays, live score/multiplier HUD
- `evidence/trgheart/shot-243s.png` — title screen, PRESS START BUTTON, ©WARASHI 2006, Ver.A badge
- `evidence/trgheart/shot-548s.png` — SCORE RANKING table (EXELICA/CRUELTEAR entries)
- `evidence/trgheart/shot-609s.png` — attract gameplay, DEMONSTRATION overlay, boss structure

Anomalies: none.

## 4. Memory fit (axis: 100.0)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 3,897,601 | 16,777,216 | 0.2323 | 100.0 | address peak 31,643,808 (u 1.886, informational — NOT the `0x1F00040` shared-structure signature, it lands 862,112 B below it, kb §6 item 3) · `nz_above_cap` 2,296,697 · `dma_high_water` 30,078,176 (informational-only from v6 on) |
| VRAM (FB-masked content + 2×FB) | 4,736,359 (content_total 3,507,559 + 2×fb_bytes 614,400) | 8,388,608 | 0.5646 | 100.0 | raw address peak 13,277,695 (u 1.583) is the extent artifact, not content · nz_total 4,118,519 |
| ARAM (content volume, fill-excluded, `content_total`) | 1,346,112 | 2,097,152 | 0.6419 | 100.0 | address peak 1,635,440 — **first assessed title whose ARAM address peak already fits the cap** (no 8 MiB full-bank load; `nz_above_cap` 0) — kb §6 item 1 |

Watermarks (informational, content-scan — stale-data prone): main 31,643,808 ·
vram 13,277,695 · aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 68.2)

DMA events 3,984 · total 94,140,416 B (89.8 MB) · unique 14,888,960 B (14.2 MB) ·
re-read ratio 0.8418 · steady-state 8.724 MB/min (`short_window: false`) ·
PIO bootstrap `pio_bytes` 2,098,496 B (GD DIMM PIO boot-load, handoff `trigger=pio`).
High re-read on a small (14.2 MB) unique working set — the cache-friendly loop pattern kb
§6 item 2 already flags as over-penalized.

## 6. Guts (axis: 85.0)

Code 2,097,152 B (carve `base 0x8c020000`, entry `0x8c021000`, header title
"TRIGGERHEART EXELICA") · functions 2,558 · MMIO refs: scif 2, rtc 3, g2ext 835 ·
BIOS vector refs: {} · penalties: `eeprom_bios`+`serial`+`rtc` → −15.
SDK strings show the full Sega Katana-derived Naomi stack: Kunoichi2 2.07, Ninja2 2.01,
KAMUI2, sd2 for DC 2.50.17, CRI ADXT/ADXF/LSC, gdCi 1.03 GD filesystem — heavily
DC-adjacent tooling (`.nj`/`.pvr` asset names throughout).

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 2P panel, 8-way stick + 3 buttons — A = Shot (hold to pull an
anchored enemy in), B = Anchor, C = Bomb. `controls.device_class = stick`. MAME input
ports: `naomi` (INPUT_PORTS_START at naomi.cpp @59e7c0b line 1506 — digital stick +
6 buttons, no analog).
Proposed DC mapping: d-pad + 3 face buttons, 1:1 — proven by the official DC port's
configurable controls (and the fan patch even added analog-stick support).
Sources: MAME naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[Shmups Wiki](https://shmups.wiki/library/Triggerheart_Exelica);
[1CC Log DC review](http://1cclog.blogspot.com/2024/10/triggerheart-exelica-dreamcast.html).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 100.0^.40 · 68.2^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **86.5 (S)**
Similarity inputs: developer match no, SDK overlap **partial**, cart loader match **yes**
(gdCi/Kunoichi GD loader stack — same family as the cleoftp reference) → 70.0.

## 9. Risks & notes

- **The strongest A/B reference candidate after cleoftp**: Warashi's own 2007 DC build of
  this exact GD-ROM game exists — comparing the Naomi image against the retail DC disc
  would show precisely what a first-party downport changed (main-RAM layout above all,
  given the 31.6 MB address extent over 3.9 MB of actual content). High-value
  control-test material for the campaign.
- The 2,296,697 B of main content above the 16 MB address line is placement, not volume
  (kb §6 item 3 divergence class); the shipped DC port is proof the game fits 16 MB
  after a real downport.
- ROT270 vertical — solved in the official port (TATE mode).
- Official DC port's PAL mode shipped 50 Hz-broken (fan patch fixes it) — irrelevant to
  NTSC but worth knowing for PAL hardware testing.
- Main-RAM write-truth includes CPU writes (v6+); `dma_high_water` is informational-only.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v8 | 2026-08-08 | 40.0 (B) | First assessment (FB-masked VRAM keying); main address-keyed peak 31.6 MB bound at u 1.886 while changed content was only 3.9 MB — the address-vs-content divergence logged for the checkpoint — kb §6 item 3 |
| v9 | 2026-08-08 | 86.5 (S) | Scoring-only re-key (no re-capture): main keyed on content volume `nz_total` 3,897,601 B; memory axis 100.0 — spec `2026-08-08-main-content-rekey-design.md` |
