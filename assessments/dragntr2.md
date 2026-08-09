# Dragon Treasure 2 (Rev A) (GDS-0037A) (`dragntr2`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final** | **PARKED — `G1 broken: emulator-exited`** (G2 `medal_hopper` latent, permanent) |
| Bottom line | Satellite terminal (`837-14457 SATL BD NAOMI DGS`) of a networked Sega medal machine: no build boots under the fork (netpic decrypt failure), a lone satellite literally lacks the game — only the first 16 MB of the binary is locally encrypted, everything from 0x1000000 is uploaded via network from the main unit — and the `medal_hopper` control class parks G2 the moment anything boots. |
| Assessed | 2026-08-04 · battery v4 · flycast `4b59eceff` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `dragntr2` (covers: no clones — `parent: null`, no children in controls.json). Rev A, GDS-0037A, is the only dumped revision; the original GDS-0037 is absent from MAME @59e7c0b (GAME table line 11218 comment only). Main-unit PIC `317-0389-COM` + satellite PIC `317-0390-COM` (ROM_START lines 9491–9505) |
| Maker / year | Sega, 2004 ([Highway Games](https://www.highwaygames.com/arcade-machines/dragon-treasure-medal-machine-9042/)) |
| Genre / format | **Medal Game** — sequel to the Dragon Treasure coin-pusher/RPG medal machine ([Highway Games "Dragon Treasure 2 Medal Machine"](https://www.highwaygames.com/arcade-machines/dragon-treasure-medal-machine-9042/): crystal-roulette bonus rounds, gold-eater chance, three hunting modes; series mechanics per [Wikipedia](https://en.wikipedia.org/wiki/Dragon_Treasure)). **GD-ROM** GDS-0037A, 231.6 MB, machine `naomigd` |
| Official DC port | No — the series "received no port of any kind" ([Wikipedia](https://en.wikipedia.org/wiki/Dragon_Treasure)) |
| Community ports | None found (searched 2026-08-03) |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: **no** — v4 sidecar `boot.ok = false`, `failure_class = "emulator-exited"` ·
handoff never seen · run 600 s · rom `naomi/dragntr2.zip`. Same signature as `dragntr`:
`Naomi GDROM: Could not find the file to decrypt.` (`gdcartridge.cpp:611`) — no bootable
payload.
Attract/demo reached: taxonomy does not apply — the game never executed
(`capture.coverage = null`). All sidecar measurement fields are zeros/non-measurements;
guts skipped.
Screenshots: none (no boot; `evidence/dragntr2/` is empty).

The battery v2 4-leg evidence (durable diagnosis):

- **Zip leg 2:** `emulator-exited` with the `dragntr` signature —
  `ui/gui.cpp:1358 E[BOOT]: Naomi GDROM: Could not find the file to decrypt.`
  (`raw/stdout-leg2.log` line 11) — second confirmed instance of the fork's
  `gdcartridge.cpp:487` netpic TODO (kb §4.s), which names `dragntr[2]` explicitly.
- **Zip leg 1:** died earlier and differently — a 4-line log ending in a dynarec init
  assert, `ui/gui.cpp:1596 E[COMMON]: Verify Failed : &mem_b[0] == ((u8*)getContext()->sq_buffer + …)`
  at `core/hw/sh4/dyna/driver.cpp:349` (`raw/stdout-leg1.log` line 3), with a DC-profile
  memory map (RAM 16 MB) — an init crash before content load, not the decrypt error.
  Leg 2's deterministic signature plus dragntr's 2/2 identical zip legs carry the diagnosis.
- **Chd-direct legs 3–4:** `no-handoff-120s` ×2 — known dead-end path for GD sets (kb §4);
  logs show only DC BIOS activity (`CLEO-SPG write SPG_LOAD` from BIOS pc `8c00b87c`), and
  the kept screenshot was the DC BIOS main menu.

## Gate

Current score run:

```
dragntr2 PARKED G1 broken: emulator-exited
```

Boot check precedence keeps the formal gate at G1 (v4 class `emulator-exited`; the v2 run
classed as `no-handoff-120s`); the off-ladder `medal_hopper` value means G2 fires the
moment any build boots. Both gates:

**G2 controls: `medal_hopper` — physically unmappable, permanent.** All three off-ladder
categories at once, same analysis as [`dragntr`](dragntr.md) §Gate:
medal/hopper ([Highway Games medal-machine catalog entry](https://www.highwaygames.com/arcade-machines/dragon-treasure-medal-machine-9042/),
[Wikipedia](https://en.wikipedia.org/wiki/Dragon_Treasure)), card reader + coin mechanics
(MAME naomi.cpp @59e7c0b line 9490: `// requires 837-14381 "G2 EXPANSION BD" I/O board,
NetDIMM, IC Card reader SAXA HW210 and coin mechanics`), and mandatory multi-cabinet
(satellite board `837-14457 SATL BD NAOMI DGS`, line 9489; satellite PIC 317-0390-COM,
lines 9500–9504). DT2 hardens the third category beyond DT1: naomi.cpp lines 9483–9487 —
"Dragon Treasure 2 and 3 game binaries have only first 16MB encrypted using key from main
unit security PIC. data starting from 0x1000000 uploaded via network to satellite units and
later decrypted using keys from satellite security PICs." **The satellite does not hold the
game; the main unit serves it over the network.**

**G1 broken (formal gate).** The netpic decrypt failure is **doubly moot** here: even with
the netpic byte fixed, the local image only contains the first 16 MB of playable binary —
the rest arrives from an emulated main unit that does not exist.
(`boot.mame_not_working` carries no per-title signal for Naomi sets, kb §4.r.)

**What would unblock:** nothing realistic. G2 is permanent; G1 would additionally require
emulating the main-unit-to-satellite network upload, only to surface the G2 park.

## Risks & notes

- **`dragntr3` (GDS-0041A) inherits this verdict wholesale** — same requires-comment
  (naomi.cpp line 9507), same satellite PIC 317-0390-COM, same network-upload scheme
  (comment covers "2 and 3").
- Zip leg 1's `Verify Failed` dynarec init crash is a one-off launch flake distinct from
  the netpic signature — recorded here so the "deterministic ×2" claim isn't overstated
  for this set; determinism rests on leg 2 plus dragntr's two identical legs.
- DT2's binary also contains "DIMM firmware updater ver 3.13 at 0x19000000" (naomi.cpp
  line 9486) — color for anyone poking the image, not assessment-relevant.
- Boot-ID quirk as siblings: boots with SDK placeholder `SAMPLE GAME MAX LONG NAME-`;
  Flycast renames by set (`naomi_cart.cpp:653–662`).
- Every numeric sidecar field is a non-measurement (no boot); quote none of them.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-03 | PARKED `G1 broken: no-handoff-120s` | All 4 legs failed (zip: netpic decrypt error + one dynarec-init flake; chd-direct: known dead-end, kb §4); `medal_hopper` researched and set — G2 latent behind boot-check precedence (kb §4.s) |
| v4 | 2026-08-04 | PARKED `G1 broken: emulator-exited` | Re-run reclassified the same netpic failure ("Could not find the file to decrypt.", `gdcartridge.cpp:611`) — no bootable payload, same as `dragntr` (kb §4.s; instrumentation root-causes kb §7) |
