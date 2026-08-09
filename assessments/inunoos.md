# Inu no Osanpo / Dog Walking (Japan, Export, Rev A) (840-0073) (`inunoos`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | Real above-cap sound content parks it again on a fresh v9 capture — ARAM content is 6,722,778 B, 3.206× the DC's 2 MiB AICA RAM (v7: 3.146×) — but main RAM and VRAM, both keyed on content volume for the first time on this title, actually clear their caps (main u ≈ 0.577, vram u ≈ 0.966), reversing the v7 doc's address-peak reads; even if the sound bank is trimmed, the treadmill + leash cabinet still caps the ceiling at `awkward` (25.0, the ladder's bottom rung). |
| Assessed | capture 2026-08-10 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — fresh v9 capture (parked-list groom), superseding the v7 capture (see History) |

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
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote
`null`; set here after screenshot review, reproducing v7). This run's shots span the
full attract loop: a breed-select card ("Welsh Corgi Pembroke"), in-engine walking
footage, the title screen ("犬のおさんぽ"), and two distinct "おさんぽランキング"
(Walk Ranking) result screens with different scores/routes (300/HAV/route-A at
`shot-487s.png`, 400/INU/route-B at `shot-609s.png`) — genuine live attract-demo
content, not a frozen frame, same conclusion as v7.
Screenshots: `evidence/inunoos/shot-060s.png` · `shot-182s.png` · `shot-426s.png` ·
`shot-487s.png` · `shot-609s.png`
Anomalies: none. Several mid-run shots (`shot-243s.png`, `shot-304s.png`,
`shot-365s.png`) caught the attract loop's fade-to-white transition between
routes/rounds — expected demo behavior, curated out of the committed set for
readability, not evidence of a capture fault.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total =
6,722,778 B` (fill-excluded content volume, §6 checkpoint keying) against the DC's
2,097,152 B AICA RAM → utilization **3.206**, still well past `region_score()`'s
`u > 2.0` gate — the park **reproduces** the v7 result within run-to-run jitter
(6,597,975 B → 6,722,778 B, +1.89%; `nz_above_cap` 4,610,037 B → 4,734,702 B, +2.70%).
Address peak is byte-identical at 8,257,552 B (u 3.94, pre-v7 keying). Boot-time
full-bank load — still the **tenth** entry in the kb §6 tally and the **earliest**
title in it. The bank-loading sound stack is visible in `guts.sdk_strings`: a
bank-based AICA loader ("LoadAICA ERROR", "AICA ERROR -4(AICA RAM FULL)") shipping
per-breed voice/SE banks and `SND_SNGA_SNG_BNK9_*` music (unchanged from v7).

Not the only memory datum worth reading — and the picture improved on the other two
regions once keyed on content instead of address, first surfaced on this title under
v9 (does not change the gate: ARAM is checked first in `score.py`'s region walk):

- **Main RAM**: address peak `33,030,208 B` (byte-identical to v7; u 1.969 on the old
  address-peak read that the v7 doc quoted) — but the v9 main-content rekey (spec
  `2026-08-08-main-content-rekey-design.md`), now live in `score.py`, keys main on
  write-truth content VOLUME (`nz_total`) instead: `nz_total` 9,680,725 B (v7:
  9,675,761 B, +0.05%, noise) ⇒ u ≈ **0.577** — main actually clears the 16 MB cap
  comfortably, reversing the v7 doc's "independently close to its own gate boundary"
  read, which was an address-placement artifact (the same class of over-read ARAM's
  volume keying already corrected in §6). `nz_above_cap` 5,254,903 B (v7: 5,268,098 B,
  −0.25%, noise) · `dma_high_water` 29,180,960 B (byte-identical, u 1.74 on the old v4
  scoring input).
- **VRAM**: address peak `12,845,578 B` (byte-identical; u 1.53 on the old address-peak
  read) — the v8 FB-masked content fields are measured on this title for the first
  time this pass: `content_total` 6,874,244 B (no such field in the v7 sidecar) +
  `fb_bytes` 614,400 B (the standard 640×480×2 constant) ⇒ fit 8,103,044 B, u ≈
  **0.966** — likewise clears the 8 MB cap, reversing the prior "over 1×" read.
  `nz_total` 7,078,984 B (v7: 7,080,366 B, noise) · `nz_above_cap` 4,262,946 B (v7:
  4,264,328 B, noise).

Context values quoted from the sidecar (no axis scores exist — the pipeline stops at
the gate): streaming 2,822 DMA events (unchanged), 127.2 MB total (v7: 126.5 MB) /
27.6 MB unique (v7: 27.2 MB), re-read ratio 0.7825 (v7: 0.7848), steady-state
12.237 MB/min (v7: 12.15) (`short_window: false`), `pio_bytes` 101,422,154 B (v7:
101,287,928 B) — all within ordinary capture jitter (≤1.6%); guts **works** (M2 cart,
`dat_available: true`): 2,097,152 B code, 1,429 functions, MMIO refs scif 1 / rtc 7 /
g2ext 137, flags `eeprom_bios`/`serial`/`rtc` (all byte-identical to v7); similarity
inputs `developer_match: false`, `sdk_overlap: "none"`, `cart_loader_match: false`
(unchanged).

What would unblock it: a per-title audio trim (downsample/ADPCM the banks) — standard
porting work with released-port precedent (Ikaruga DC, kb §4.d). Main RAM and VRAM, now
both measured under content-volume keying for the first time on this title, already
clear their caps — the sound bank is the sole remaining memory blocker — but the
controls class below caps the ceiling regardless of any memory fix.

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
  (real content, not an artifact, reproduced across two fresh captures at v7 and v9),
  and — now that main RAM and VRAM are known to clear their own caps under
  content-volume keying — audio trim is genuinely the *only* memory fix needed; but
  the `awkward` controls class (25.0, the ladder's bottom) caps any future score
  regardless, so a port is still both trim-the-audio work *and* a
  fundamentally degraded-experience title.
- **Display blindness resolved at v7** (v2's frozen-splash capture was the kb §4.m
  stale-TA-frame class); reconfirmed clean at v9. Per the working-style rule,
  rendering must still be verified on real DC hardware.
- **Heavy streaming for a cart title:** 12.237 MB/min steady-state (v7: 12.15),
  re-read 0.7825 (v7: 0.7848), 127.2 MB total over 600 s (v7: 126.5 MB) — GD-ROM seek
  behavior on a real DC would need attention even though the source is a cart.
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
| v9 | 2026-08-10 | PARKED G3 memory: aram content > 2x DC capacity | parked-list groom: fresh v9 capture (was v7) — gate reproduced (`content_total` 6,597,975→6,722,778 B, u 3.146→3.206, +1.89%; all other shared raw counters byte-identical or within ≤2.7% jitter); main and vram now measured under first-time content-volume keying on this title (main `nz_total`, vram `content_total`+`fb_bytes`) and both clear their caps (main u≈0.58, vram u≈0.97, reversing the v7 address-peak reads) — ARAM sound bank is the sole memory blocker |
