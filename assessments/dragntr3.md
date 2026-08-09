# Dragon Treasure 3 (Rev A) (GDS-0041A) (`dragntr3`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final** | **PARKED — `G1 broken: no-render-after-handoff`** (G2 `medal_hopper` latent, permanent) |
| Bottom line | Satellite terminal of a networked Sega medal machine that says so itself: it boots to the NAOMI GD-ROM splash then stalls polling the network for its main unit (`Network command received cmd 1. Need full NetDIMM?`, fork `gdcartridge.cpp:761`) — vanilla Flycast reproduces the identical stall, the bytes above 0x1000000 are network-served and don't exist locally in any emulator, and the `medal_hopper` control class parks G2 regardless. |
| Assessed | 2026-08-04 · battery v4 · flycast `4b59eceff` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` · vanilla control run 2026-08-05 (Flycast v2.6 `392a429e8`) |

## 2. Identity

| | |
|---|---|
| Set / family | `dragntr3` (covers: no clones — `parent: null`, no children in controls.json). Rev A, GDS-0041A, is the only dumped revision; the original GDS-0041 is absent from MAME @59e7c0b (GAME table line 11225 comment only). Main-unit PIC `317-0426-JPN` (PIC16F628A) + satellite PIC `317-0390-COM` — the same satellite PIC as `dragntr2` (ROM_START lines 9508–9523) |
| Maker / year | Sega, 2005 ([Highway Games](https://www.highwaygames.com/arcade-machines/dragon-treasure-iii-medal-machine-9187/); GAME line 11226) |
| Genre / format | **Medal Game** — third entry in the Dragon Treasure coin-pusher/RPG medal-machine series ([Highway Games "Dragon Treasure 3 Medal Machine"](https://www.highwaygames.com/arcade-machines/dragon-treasure-iii-medal-machine-9187/); series mechanics per [Wikipedia](https://en.wikipedia.org/wiki/Dragon_Treasure)). **GD-ROM** GDS-0041A, 290.1 MB, machine `naomigd` |
| Official DC port | No — the series "received no port of any kind" ([Wikipedia](https://en.wikipedia.org/wiki/Dragon_Treasure)) |
| Community ports | None found (searched 2026-08-03) |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: **no** — v4 sidecar `boot.ok = false`, `failure_class = "no-render-after-handoff"` ·
handoff at 20.0 s · run 600 s · rom `naomi/dragntr3.zip`. Boots to the NAOMI GD-ROM
splash then stalls polling the network: `Network command received cmd 1. Need full
NetDIMM?` (fork `gdcartridge.cpp:761`).
Attract/demo reached: taxonomy does not apply — the game proper never executes
(`capture.coverage = null`).
Screenshots: `evidence/dragntr3/shot-060s.png` · `shot-365s.png` · `shot-609s.png`
(GD-ROM splash throughout; shot-609s is still the splash at end of window) ·
`evidence/dragntr3/vanilla-control-2026-08-05.log` (control-run log).

The battery v2 leg evidence (durable diagnosis):

- **Zip legs 1–2: `no-eeprom-180s`, deterministic** — both logs are 1732 lines, line-for-line
  identical in signature. **No decrypt error** (the `gdcartridge.cpp:487` netpic TODO names
  only `dragntr[2]`, and indeed did not fire here). The image loads —
  `NAOMI GAME ID [DRAGON TREASURE 3] region ff players 0 vertical 0` (`raw/stdout-leg1.log`
  line 8; the placeholder header live: line 10 reads
  `Initializing Naomi EEPROM for game SAMPLE GAME MAX LONG NAME-`) — runs ~31 s of GD-splash
  face activity, then each log ends with
  `hw/naomi/gdcartridge.cpp:761 W[NAOMI]: Network command received cmd 1. Need full NetDIMM?`
  ×2 (`raw/stdout-leg1.log` lines 1731–1732, `raw/stdout-leg2.log` lines 1731–1732;
  fork source: `WARN_LOG(NAOMI, "Network command received cmd %x. Need full NetDIMM?", cmd)`).
  The battery aborted the stalled face at 180 s per the kb §4 no-eeprom rule.
- **Chd-direct legs 3–4:** `no-handoff-120s` ×2 — known dead-end path for GD sets (kb §4);
  logs show only DC BIOS activity, and the kept screenshot was the DC BIOS main menu.

## Gate

Current score run:

```
dragntr3 PARKED G1 broken: no-render-after-handoff
```

Boot check precedence keeps the formal gate at G1; the off-ladder `medal_hopper` value
means G2 fires the moment any build boots. Both gates:

**G2 controls: `medal_hopper` — physically unmappable, permanent.** All three off-ladder
categories at once, same analysis as [`dragntr`](dragntr.md) §Gate: medal/hopper
([Highway Games medal-machine catalog entry](https://www.highwaygames.com/arcade-machines/dragon-treasure-iii-medal-machine-9187/),
[Wikipedia](https://en.wikipedia.org/wiki/Dragon_Treasure)), card reader + coin mechanics
(MAME naomi.cpp @59e7c0b line 9507: `// requires 837-14381 "G2 EXPANSION BD" I/O board,
NetDIMM, IC Card reader SAXA HW210 and coin mechanics`), and mandatory multi-cabinet
(satellite PIC 317-0390-COM shared with `dragntr2`; network-upload scheme, lines 9483–9487:
"data starting from 0x1000000 uploaded via network to satellite units and later decrypted
using keys from satellite security PICs" — the comment covers "Dragon Treasure 2 and 3").
Uniquely in the trio, the dependency is **observed at runtime**: the runs stall asking
`Need full NetDIMM?` — the satellite requesting its main unit (§3).

**G1 broken (formal gate).** A network-stall, not the siblings' netpic decrypt failure —
and moot for the same reason: the local image lacks the network-served payload, and no
emulated main unit exists. (`boot.mame_not_working` carries no per-title signal for Naomi
sets, kb §4.r.)

**Vanilla control run (2026-08-05): identical stall — not a fork bug.** Vanilla
Flycast v2.6 (build `392a429e8`, `/Applications/Flycast.app`, shared `emu.cfg`)
reproduces the exact signature: boots to GAME ID `[DRAGON TREASURE 3]`, then
`Network command received cmd 1. Need full NetDIMM?` ×2 (vanilla
`gdcartridge.cpp:758`) ~12 s in, then silence (`evidence/dragntr3/vanilla-control-2026-08-05.log`).
The fork's naomi-side diff vs its base `4126f1464` is additive logging only
(`git diff` — cartlog + `GetDmaSrcOffset`); the stalling code is byte-identical
upstream code: `GDCartridge::process()` rejects the whole network command group,
and the `NetDimm` class (selected only for vf4*/mj1/wccf*, `naomi_cart.cpp:283`)
stubs `accept`/`bind` anyway. Satellite payload above 0x1000000 is served over
the network by the main unit (MAME naomi.cpp @59e7c0b lines 9483–9487), so the
bytes to run don't exist locally in any emulator.

**What would unblock:** nothing realistic. G2 is permanent; G1 would require emulating the
main-unit network upload protocol, only to surface the G2 park.

## Risks & notes

- **Leg-pattern is not uniform across the trio** — three sets, three zip-leg outcomes:
  `dragntr` 2× netpic decrypt error, `dragntr2` 1× decrypt error + 1× unrelated dynarec-init
  flake, `dragntr3` 2× network-stall (no decrypt error). All three converge on the same
  dual-gate park; kb §4.s tracks the per-set signatures.
- dragntr3 got the **furthest** of the three under the fork — GAME ID handoff and ~31 s of
  execution before the NetDIMM stall — which is why its failure is the best dynamic evidence
  of the satellite architecture.
- Boot-ID quirk visible live in the logs: `Initializing Naomi EEPROM for game SAMPLE GAME
  MAX LONG NAME-` while Flycast's rename special-case reports `DRAGON TREASURE 3`
  (`naomi_cart.cpp:653–662`).
- The v4 sidecar's numeric fields are splash-only, not game usage: its VRAM
  (peak, nz_above_cap) pair is literally `score.py`'s `BIOS_VRAM_SIGNATURES` control
  entry ("control: dragntr3 splash-only run"), and the 8 MiB ARAM watermark is the DIMM
  "DMPD" fill. Quote none of them as measurements.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-03 | PARKED `G1 broken: no-handoff-120s` | Zip legs deterministic `no-eeprom-180s`: GAME ID handoff, ~31 s of GD-splash, then `Need full NetDIMM?` stall ×2 — best dynamic evidence of the satellite architecture; `medal_hopper` set, G2 latent (kb §4.s) |
| v4 | 2026-08-04 | PARKED `G1 broken: no-render-after-handoff` | Re-run boots to the GD-ROM splash and stalls polling the network — park correct, class corrected (kb §4.s; instrumentation root-causes kb §7) |
| — (control) | 2026-08-05 | PARKED (unchanged) | Vanilla Flycast v2.6 `392a429e8` reproduces the identical stall — not a fork bug; stalling code is byte-identical upstream (`evidence/dragntr3/vanilla-control-2026-08-05.log`) |
