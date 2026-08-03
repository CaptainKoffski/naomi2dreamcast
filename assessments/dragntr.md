# Dragon Treasure (Rev B) (GDS-0030B) (`dragntr`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — G2 controls: `medal_hopper` (satellite medal machine)** (not a numeric tier) |
| Bottom line | Dragon Treasure is not a video game with mappable controls — it is a **satellite terminal of a networked Sega medal (coin-pusher) machine**: medal/hopper mechanics + SAXA HW210 IC card reader + mandatory multi-cabinet NetDIMM link to a main unit, with a dedicated satellite security PIC (317-0364-COM) baked into the ROM set. Every one of RUNBOOK's three off-ladder hardware categories applies at once; no conceivable DC mapping exists. The sidecar's **formal** gate reads `G1 broken: no-handoff-120s` because gate precedence runs the boot check first and the fork cannot boot the title at all (zip legs die on the gdcartridge netpic quirk, §Gate) — but even a booting build would park G2. This verdict transfers wholesale to `dragntr2` and `dragntr3`. |
| Assessed | 2026-08-03 · battery v2 · flycast `9e882cbd2` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `dragntr` (Rev B, representative) covers `dragntra` (Rev A, GDS-0030A). Identical security PIC pair in both revs (main `317-0363-COM` + satellite `317-0364-COM`); they differ only in GD image SHA1 (`gds-0030b` a49e1ae2… vs `gds-0030a` fa7fb0ff…) — MAME src/mame/sega/naomi.cpp @59e7c0b ROM_START blocks lines 9397–9433, GAME lines 11201–11202. No public A→B changelog found. The original GDS-0030 (no rev) is **not** in MAME — the GAME table jumps from 0029A straight to 0030A — i.e. undumped |
| Maker / year | Sega (developed by Overworks), 2003 ([Wikipedia](https://en.wikipedia.org/wiki/Dragon_Treasure)) |
| Genre / format | Queue genre "?" resolved: **Medal Game / Adventure** ([arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=dragntr)) — a coin-pusher medal game combined with an RPG (start with 100 medals, battles/chest openings/roulette/slots to level a character; progress on IC card usable across machines, a first for JP medal games — [Wikipedia](https://en.wikipedia.org/wiki/Dragon_Treasure)). **GD-ROM** GDS-0030B, 142.3 MB, machine `naomigd` |
| Official DC port | No — "released only in Japanese arcades and received no port of any kind" ([Wikipedia](https://en.wikipedia.org/wiki/Dragon_Treasure)) |
| Community ports | None found (searched 2026-08-03) — as expected for a medal-machine satellite |
| Representative choice | Rev B is the MAME parent set; `dragntra` is its clone |

## 3. Boot & run evidence

Boots: **no** — sidecar `boot.ok = false`, `failure_class = "no-handoff-120s"`, all **6 legs failed**
(`assessments/dragntr.metrics.json`; rom recorded: `naomi/dragntr/gds-0030b.chd`, the final leg).

- **Zip legs 1–2:** deterministic `emulator-exited` — both logs show
  `ui/gui.cpp:1358 E[BOOT]: Naomi GDROM: Could not find the file to decrypt.`
  (`raw/stdout-leg1.log` line 11, `raw/stdout-leg2.log` line 11). The DIMM loader never finds
  the boot binary — exactly the fork's own TODO at
  `../cleopatra/tools/flycast-src/core/hw/naomi/gdcartridge.cpp:487`:
  `netpic = picdata[0x6ee]; // TODO dragntr[2] seem to prefer a 0 here` — the netpic byte read
  from the real PIC misdirects the DIMM firmware read frame. First observed instance of this
  TODO biting in the campaign (kb §4.s).
- **Chd-direct legs 3–6:** `no-handoff-120s` ×4 — the known dead-end path for GD sets (kb §4);
  logs show only DC BIOS activity (`CLEO-SPG write SPG_LOAD` from BIOS pc `8c00b87c`), and the
  kept screenshot is the DC BIOS main menu.

Attract/demo reached: the `calibration | title | demo` taxonomy does not apply — the game never
executed; sidecar `capture.coverage = null` stands.
Screenshot kept: `assessments/evidence/dragntr/shot-060s.png` (DC BIOS menu, boot-failure
evidence from the chd legs; the second shot was the same menu one minute later — deleted).
All measurement fields in the sidecar are zeros/non-measurements; guts skipped
(`"skipped (--skip-static or no boot)"`).

## Gate

Score run after setting `controls.device_class = "medal_hopper"`:

```
dragntr PARKED G1 broken: no-handoff-120s
```

The boot check runs first, so the formal gate stays G1; the off-ladder `medal_hopper` value
means G2 fires the moment any build boots. Both gates documented:

**G2 controls: `medal_hopper` — physically unmappable, permanent.** The cabinet hits all three
off-ladder categories of RUNBOOK step 2 simultaneously:

1. **Medal/hopper:** coin-pusher medal game — players bet and receive physical medals
   ([Wikipedia](https://en.wikipedia.org/wiki/Dragon_Treasure); catalogued as a "Medal Machine"
   by [Highway Games (DT2)](https://www.highwaygames.com/arcade-machines/dragon-treasure-medal-machine-9042/),
   [Highway Games (DT3)](https://www.highwaygames.com/arcade-machines/dragon-treasure-iii-medal-machine-9187/);
   category "Medal Game / Adventure" on [arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=dragntr)).
2. **Card reader:** requires the SAXA HW210 IC card reader — MAME naomi.cpp @59e7c0b line ~9396:
   `// requires 837-14381 "G2 EXPANSION BD" I/O board, NetDIMM, IC Card reader SAXA HW210 and coin mechanics`.
3. **Mandatory multi-cabinet:** the dumped board is `837-14389 SATL BD NAOMI DGT` — a
   **satellite** board — and the ROM set carries a second, satellite-specific security PIC
   region (`satl_pic`, 317-0364-COM) alongside the main-unit PIC (naomi.cpp lines 9397–9433).
   The sequels make the dependence explicit: "data starting from 0x1000000 uploaded via network
   to satellite units and later decrypted using keys from satellite security PICs"
   (naomi.cpp comment above `dragntr2`, lines 9483–9487).

Note: arcadeitalia's "8-way joystick / 6 buttons" is MAME's generic `naomi` INPUT_PORTS
placeholder (the real medal I/O is unemulated — GAME line 11202), not cabinet evidence.

**G1 broken: no-handoff-120s (sidecar formal gate).** Verified it is the game+fork, not
tooling: deterministic identical decrypt error across both zip legs (log lines quoted in §3),
matching the fork's documented dragntr-specific netpic TODO (gdcartridge.cpp:487);
`boot.mame_not_working = false` carries no per-title signal (kb §4.r) and MAME's own status is
preliminary with blanket NOT_WORKING flags.

**What would unblock:** nothing realistic. G2 is permanent — a coin-pusher RPG satellite has no
DC-mappable input surface. G1 is additionally an emulator gap (the netpic TODO), but fixing it
would only surface the G2 park.

## Risks & notes

- **This verdict transfers wholesale to `dragntr2` (GDS-0037A) and `dragntr3` (GDS-0041A).**
  Same "requires 837-14381 G2 EXPANSION BD, NetDIMM, IC Card reader SAXA HW210 and coin
  mechanics" comment on both ROM_STARTs; both share satellite PIC 317-0390-COM. They are
  **more** main-unit-dependent than DT1: the bulk of their binaries is network-uploaded from
  the main unit and decrypted with the satellite key (naomi.cpp lines 9483–9487). The
  netpic TODO names `dragntr[2]` — expect the same zip-leg decrypt failure.
- **Boot-ID quirk (color):** all three Dragon Treasures boot with the SDK placeholder title
  `SAMPLE GAME MAX LONG NAME-`; Flycast special-cases them by rom name to substitute
  "DRAGON TREASURE [2/3]" (`../cleopatra/tools/flycast-src/core/hw/naomi/naomi_cart.cpp:653–662`).
- `dragntra` (Rev A) needs no separate assessment: same PIC pair, GD image differs, no
  changelog; the original GDS-0030 is undumped (absent from MAME @59e7c0b).
- Every numeric field in the sidecar is a non-measurement (no boot); do not quote any of them
  as game figures.
