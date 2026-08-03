# Kurukuru Chameleon (Japan) (GDL-0034) (`kurucham`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **45.8** (B) |
| Bottom line | Mid-tier B: the actual content volume is genuinely DC-sized (5.3 MiB of nonzero VRAM assets, 2.4 MB ARAM, 1 MiB code) — but main-RAM DMA high-water is 1.64× the DC's 16 MB and needs real reduction, and our Flycast fork renders no visible frames for this title (display-path gap, §3), so nothing can be visually validated in emulation today. |
| Assessed | 2026-08-03 · battery v2 · flycast `9e882cbd2` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

History: this doc supersedes the 2026-08-03 `G1 broken: no-handoff-120s` park (commit
`d7500a1`) — that diagnosis was retracted after the kb §4.l/§4.m investigation showed the
game boots and runs headless under the fork; two tooling bugs had masked it (see §3/§9).

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

Boots: yes · handoff at 30.0 s · run 600 s · rom: `naomi/kurucham.zip` (single clean zip leg)
Attract/demo reached: **title (conservative lower bound)** — sidecar
`capture.coverage = "title"`. The run cannot be classified visually (see Display
blindness below); the game verifiably runs its attract loop for the full window —
EEPROM init (`Initializing Naomi EEPROM for game KURU KURU CHAMELEON`, raw
stdout of earlier legs), ~2 framebuffer flips/frame for 600 s, 86.7 MB of GD streaming
across 2,597 DMA events, ARAM written to 2.4 MB, and 5,600,640 B of nonzero VRAM asset
uploads (`memory.vram.nz_total`) — but we cannot visually distinguish title-idle from
demo gameplay, so the conservative `title` label is used.

### Display blindness

The game runs with no visible output under our fork; three image classes prove the
metrics come from a running game, not a hang:

- `shot-060s.png` / `shot-609s.png` — all 10 battery screenshots show the same frozen
  NAOMI GD-ROM SYSTEM splash: a **stale TA frame** left in the GL display path, not a
  boot hang (the activity counters above run underneath it the whole time).
- `vram-fb-76a000-black.png` — raw VRAM framebuffer decode at the displayed FB address
  `0x76a000` (640×480 RGB565 per `FB_R_SIZE=0017753f`, from a CLEO-VRAMDUMP snapshot):
  pure black — the game never composes a frame the fork's display path can show.
- `vram-assets-c00000.png` — decode of the 5.34 MiB nonzero region above 8 MB at
  `0xc00000`: dense structured asset data, not a displayable frame.

MAME flags the title imperfect-graphics
([arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=kurucham),
[minimaws](https://arcade.vastheman.com/minimaws/machine/kurucham)) — consistent with an
emulator display-path gap for this title's 2D composition method, not a broken game: it
shipped in arcades and was ported to PSP/DS/Switch/PS4. The score remains valid because
memory/streaming/guts measure real game activity (DMA, VRAM/ARAM writes, static
analysis), none of which depends on rendering.

Screenshots kept: `shot-060s.png`, `shot-609s.png` (frozen splash, identical at t=60 s
and t=609 s), `vram-fb-76a000-black.png`, `vram-assets-c00000.png`.
Anomalies: the two earlier false G1 parks were tooling, not the game — (a) the boot
heuristic checked nonzero VRAM only below 8 MB, blind to this title's above-8-MB asset
store (fixed → total-nz, kb §4.m); (b) genuine launch flakes (kb §4.a DC-BIOS-menu and
dynarec-assert faces) hit the chd legs repeatedly (fixes: `61350c8`, `4ea17fc`,
`e5f5649`, plus the boot_ok fix).

## 4. Memory fit (axis: 19.6)

| Region | Peak | DC capacity | Utilization | Sub-score | Evidence |
|---|---|---|---|---|---|
| Main RAM (DMA high-water) | 27,449,344 B | 16 MB | 1.64× | 24.6 | grep `CARTDMA` in raw log |
| VRAM (write-truth) | 14,770,864 B | 8 MB | 1.76× | 19.6 | grep `VRAMPROFILE` |
| ARAM (write-truth) | 2,395,328 B | 2 MB | 1.14× | 59.4 | grep `ARAMPROFILE` |

Watermarks (informational, content-scan — stale-data prone): main 32,505,920 /
vram 14,770,864 / aram 2,395,328. Main watermark is 1.18× the DMA high-water — mild
flag; some content above the last DMA'd asset.

Note on VRAM: the 14.77 MB peak is **address-extent**, not content volume — actual
nonzero content is only 5,600,640 B (5.34 MiB, `nz_total`), most of it parked above the
8 MB line at `0xc00000` (`nz_above_cap = 5,599,740 B`); a port would relocate it, so the
real VRAM pressure is far milder than the sub-score implies. ARAM at 1.14× is near-fit.
Main RAM at 1.64× is the genuine weak point.

## 5. Cart streaming (axis: 74.4)

DMA events 2,597 · total 86.76 MB · unique 28.82 MB · re-read ratio 0.6678 ·
steady-state 7.171 MB/min (full window, `short_window: false`)

## 6. Guts (axis: 85.0)

Code 1,048,576 B · functions 2,634 · MMIO refs: scif 2, rtc 3, g2ext 58 ·
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
      = 19.6^.40 · 74.4^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **45.8** (tier B)
Similarity inputs: developer no (Starfish SD/Able ≠ reference), SDK overlap partial
(Kunoichi2/Ninja2/CRI — see §6), loader match yes.

## 9. Risks & notes

- **Display path is an unknown-class risk.** Under our fork the game produces zero
  visible frames (§3); whatever 2D composition method Flycast doesn't emulate for this
  title, a port must implement or replace it — and per the working-style rule, rendering
  must be verified on real DC hardware, since no emulator check is currently possible.
  Fork base `9e882cbd2` is effectively current (upstream `d4fc07741` is only 2
  non-emulation commits ahead, kb §4.l) — a rebase will not fix this today.
- **Main RAM is the weak axis regardless of the display issue**: 1.64× DC's 16 MB DMA
  high-water (and a 1.18×-higher content watermark) needs real data reduction, unlike
  VRAM (5.34 MiB actual content, relocatable) and ARAM (1.14×, near-fit).
- Coverage is `title` as a conservative lower bound — activity data proves the attract
  loop ran, but visual confirmation of demo gameplay is impossible (§3), so peaks could
  be understated relative to played gameplay.
- Supersedes the 2026-08-03 G1 park (`d7500a1`): "GD-DIMM boot hang" retracted; the
  false parks were a below-8MB-only boot heuristic (kb §4.m) plus launch flakes on the
  chd legs (kb §4.a) — both fixed (`61350c8`, `4ea17fc`, `e5f5649`).
- Main-RAM v1 limitation carried from the spec: DMA high-water misses CPU-written data
  above the last DMA'd asset (the watermark gap above is consistent with some).
