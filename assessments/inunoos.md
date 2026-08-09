# Inu no Osanpo / Dog Walking (Japan, Export, Rev A) (840-0073) (`inunoos`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | Real above-cap sound content parks it even under the v7 volume keying — ARAM content is 6,597,975 B, 3.15× the DC's 2 MiB AICA RAM — main write-truth is independently close to its own gate boundary (1.97×), and even unparked the treadmill + leash cabinet caps the ceiling at `awkward` (25.0, the ladder's bottom rung). |
| Assessed | capture 2026-08-07 · battery v7 · flycast `65f9f7857` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `inunoos` (covers: no clones — `parent: null` in controls.json; arcadeitalia "Clone of: –"). Only Rev A (`epr-22294a.ic22`) is dumped; no original-rev set exists in MAME @59e7c0b. Cart 840-0073, M2 crypt key `294bc3e3` (317-0316-JPN) — naomi.cpp ROM_START lines 7533–7558, GAME line 11000. arcadeitalia's "BAD DUMP" label is spurious — no `BAD_DUMP` flag appears anywhere in the ROM_START block (verified @59e7c0b) |
| Maker / year | Wow Entertainment / Sega (MAME GAME line); [Wikipedia](https://en.wikipedia.org/wiki/Inu_no_Osanpo) additionally credits **Cave** as co-developer — both noted. 2001 |
| Genre / format | Simulation (dog-walking simulation — [Wikipedia](https://en.wikipedia.org/wiki/Inu_no_Osanpo)), **cart** — M2-type 840-0073, boot ROM + 16×64 Mb, 79.7 MB |
| Official DC port | No — Japan-only arcade release, no home version of any kind ([Wikipedia](https://en.wikipedia.org/wiki/Inu_no_Osanpo), [IGDB](https://www.igdb.com/games/inu-no-osanpo), [arcade-history](https://www.arcade-history.com/?n=inu-no-osanpo&page=detail&id=4909)). The title's "Japan, Export" label notwithstanding, the binary itself carries the "THIS GAME IS TO BE USED ONLY IN JAPAN" warning block (`guts.sdk_strings`) and all sources say Japan-only |
| Community ports | None found (searched 2026-08-03) — as expected for a treadmill novelty cabinet |
| Representative choice | Only member of its family (MAME parent, no clones, single dumped revision) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/inunoos.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`. The v2-era
display blindness (all shots one identical frozen NAOMI splash, kb §4.m class) did not
recur at v7: this run's shots show distinct "おさんぽランキング" (Walk Ranking) result
screens with different scores/routes across frames (500/KOR/route-C at `shot-365s.png`,
400/INU/route-B at `shot-609s.png`) — genuine live attract-demo content.
Screenshots: `evidence/inunoos/shot-060s.png` · `shot-365s.png` · `shot-609s.png`
Anomalies: none at v7.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total =
6,597,975 B` (fill-excluded content volume, §6 checkpoint keying) against the DC's
2,097,152 B AICA RAM → utilization **3.146**, still well past `region_score()`'s
`u > 2.0` gate even after the volume re-keying; address peak 8,257,552 B (u 3.94,
pre-v7 keying), `nz_above_cap = 4,610,037 B`. Boot-time full-bank load — **tenth** in
the kb §6 tally and the **earliest** title in it: at 2001 on an M2 cart, it pushes the
full-bank practice back from "late-Naomi-era norm" to common practice across the
platform's life. The bank-loading sound stack is visible in `guts.sdk_strings`: a
bank-based AICA loader ("LoadAICA ERROR", "AICA ERROR -4(AICA RAM FULL)") shipping
per-breed voice/SE banks and `SND_SNGA_SNG_BNK9_*` music.

Not the only memory problem: main-RAM write-truth peak `33,030,208 B` (u 1.969 —
independently close to its own u>2.0 boundary, though ARAM gates first; `nz_total`
9,675,761 B · `nz_above_cap` 5,268,098 B · `dma_high_water` 29,180,960 B, u 1.74, the
old v4 scoring input, reproduced bit-identically). VRAM peak `12,845,578 B` (u 1.53),
backed by real content — `nz_total = 7,080,366 B` drawn.

Context values quoted from the sidecar (no axis scores exist — the pipeline stops at
the gate): streaming 2,822 DMA events, 126.5 MB total / 27.2 MB unique, re-read ratio
0.7848, steady-state 12.15 MB/min (`short_window: false`); guts **works** (M2 cart,
`dat_available: true`): 2,097,152 B code, 1,429 functions, MMIO refs scif 1 / rtc 7 /
g2ext 137, flags `eeprom_bios`/`serial`/`rtc`; similarity inputs
`developer_match: false`, `sdk_overlap: "none"`, `cart_loader_match: false`.

What would unblock it: a per-title audio trim (downsample/ADPCM the banks) — standard
porting work with released-port precedent (Ikaruga DC, kb §4.d) — but main RAM near 2×
needs real reduction too, and the controls class below caps the ceiling regardless.

## Controls (researched — recorded for the record)

Sidecar `controls.device_class` set to **`awkward`** (the G3 gate fires before controls
in `score.py`, so the class is recorded, not scored).

**The cabinet is a treadmill + leash controller** — confirmed, ≥2 independent sources:

- [Wikipedia](https://en.wikipedia.org/wiki/Inu_no_Osanpo): players "walk" the dog on a
  **treadmill** and steer with a **leash attached to a plastic dog** in front of the
  player; pace-matching is the core mechanic (too fast drags the dog, too slow
  frustrates it).
- [Siliconera first-hand account](https://www.siliconera.com/walking-sega%E2%80%99s-virtual-dog/):
  "you literally begin walking on the treadmill, but it doesn't move automatically. You
  have to push it with the force of your feet"; "you hold the handle and guide the dog
  by moving it left or right"; hazards avoided "by quickly yanking on the leash".
- Corroborating: [gamesdatabase.org](https://www.gamesdatabase.org/game/arcade/inu-no-osanpo-dog-walking),
  [arcade-history](https://www.arcade-history.com/?n=inu-no-osanpo&page=detail&id=4909),
  [HandWiki](https://handwiki.org/wiki/Software:Inu_no_Osanpo).

**Electrically, though, it is not exotic I/O.** MAME naomi.cpp @59e7c0b line 291:
"requires **837-13844 JVS IO with DIPSW 1 ON**" — the same standard "I/O CNTL BD2" used
by Sega Marine Fishing, Touch de Uno and Tokyo Bus Guide (DIPSW-selected modes, board
firmware `EPR-21868`, naomi.cpp:1028); no extra I/O firmware region and no second PIC in
the game's ROM set. Upstream Flycast explicitly supports the title:
`core/hw/maple/maple_jvs.cpp:1556–1560` — `gameId == "INU NO OSANPO"` →
`jvs_837_13844_encoders` (837-13844 with 8 digital ins + **4 rotary-encoder channels**,
class at line 591), the encoders fed from **mouse relative movement** (lines 2388–2409:
ch0 = relX, ch1 = relY ×3). At the JVS level the treadmill belt and leash are rotary
encoders — already emulated and playable with a mouse in stock Flycast. (No per-title
entry in `naomi_roms_input.h`; the special-casing is by boot game ID.)

**Why `awkward`, not a G2 `treadmill` gate — argued both ways:**

- *For G2:* the defining input is a physical exercise device; no DC peripheral is a
  treadmill; pace-matching-by-walking is the whole game.
- *For on-ladder:* RUNBOOK step 2's off-ladder criterion is **physically unmappable**
  hardware (card reader/printer, medal/hopper, mandatory multi-cabinet). Unlike all
  three exemplars (`dragntr` produced/consumed physical objects and machines), the
  treadmill + leash is pure input signal: 4 relative-encoder channels + buttons,
  *demonstrably mapped today* — upstream Flycast plays it with a mouse. The input
  honestly reduces to walk pace (encoder tick rate) + leash steer (second axis) + leash
  yank (tick burst), and the DC even has a native relative-encoder peripheral (the
  mouse, HKT-9700) matching Flycast's mapping 1:1. Per the `gunsur2` precedent (3-axis
  gun → `pad_adaptable` because the signal reduces), the consistent rung is one lower:
  mappable, but the physical experience (exercise) is unreproducible → **`awkward`**
  (25.0 on the `score.py:74` ladder). A `treadmill` G2 call is defensible if
  experience-fidelity outweighs signal mappability, but by the stated "physically
  unmappable" criterion it does not qualify.

## Risks & notes

- **Double-blocked even if the ARAM rule softens:** the sound bank parks it today
  (real content, not an artifact), and the `awkward` controls class (25.0, the
  ladder's bottom) caps any future score — a port is both trim-the-audio work *and* a
  fundamentally degraded-experience title.
- **Display blindness resolved at v7** (v2's frozen-splash capture was the kb §4.m
  stale-TA-frame class); per the working-style rule, rendering must still be verified
  on real DC hardware.
- **Heavy streaming for a cart title:** 12.15 MB/min steady-state, re-read 0.7848,
  126.5 MB total over 600 s — GD-ROM seek behavior on a real DC would need attention
  even though the source is a cart.
- MAME status is the blanket `GAME_FLAGS` macro (naomi.cpp:10914) — carries no per-title
  signal either way (kb §4.r); arcadeitalia's "8-way joystick / 6 buttons" is the
  generic `naomi` INPUT_PORTS placeholder, not cabinet evidence, and its "BAD DUMP"
  label is spurious (§2).

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-03 | PARKED G3-ARAM (peak 4.00×) | Boot-time full 8 MiB bank; tenth full-bank park in the kb §6 tally, earliest title in it; capture display-blind (frozen splash, kb §4.m) |
| v4 | 2026-08-04 | PARKED G3-ARAM | Park **confirmed** under the v4 fill-excluded content metric — 4.41 MiB of genuine sound content above the DC cap, not the DMPD fill artifact (kb §7); `awkward` controls research recorded |
| v7 | 2026-08-07 | PARKED G3-ARAM (content 3.146×) | §6 checkpoint volume re-keying doesn't change the outcome (spec `2026-08-07-aram-gate-volume-design.md`); main write-truth first measured (u 1.969); display blindness resolved, coverage `demo` |
