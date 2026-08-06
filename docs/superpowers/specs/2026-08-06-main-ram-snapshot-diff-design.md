# Design: main-RAM write-truth via snapshot+diff (battery v6)

**Date:** 2026-08-06. **Supersedes:** the open decisions in
`backlog-main-ram-snapshot-diff.md` (which stays as the motivating brief).

## Goal

Replace the main-RAM footprint metric (`CARTDMA` dest high-water) with a
snapshot+diff write-truth high-water over Naomi's **32 MB** main RAM — the
same mechanism `VRAMPROFILE`/`ARAMPROFILE` already use. (The brief said
"16 MB main window"; that is the DC cap, which stays the scoring divisor.
The scan covers the full Naomi window: `ram_size = 32_MB`,
fork `core/emulator.cpp:462` @ebae3b513.)

Two birds, per the brief:

1. **PIO-loading carts un-blind.** `sgtetris` loads with zero
   `CARTDMA`/`ARAMHANDOFF` tags and parks G1 despite visibly running
   (kb §4.v); `gwing2` fires handoff but `dma_high_water = 0` with 1,344
   DMA events, and only its ARAM gate stopped `score.py` from scoring the
   main axis 100.0 from nothing.
2. **The spec-v1 limitation retires for everyone.** DMA high-water measures
   where assets land, not the working set, and misses CPU-written data —
   the suspicious 27–30 MB main clustering across GD titles (kb §6 item 3)
   gets the cleaner metric plus a histogram to resolve it.

## Decisions (settled 2026-08-06, brainstorm session)

- **Handoff generalizes to "first bulk cart→RAM transfer":** first
  `CARTDMA` **or** cumulative PIO `ROM_DATA` reads crossing **32 KB**,
  whichever fires first. Evidence from the surviving chocomk cartlog:
  BIOS-era `CARTPIO offset=00000000` header pokes are bytes-to-KB and fire
  thousands of lines before handoff, while a PIO image load is MBs — any
  threshold in that gap works; 32 KB is the documented choice. The trigger
  runs the existing one-shot baseline block, so PIO titles emit the same
  `ARAMHANDOFF`/`VRAMHANDOFF` markers and the battery's `handoff_seen()`
  needs **zero changes**; VRAM/ARAM un-blind for PIO titles along with
  main.
- **Rejected anchors** (the brief's candidates, killed by evidence):
  - *PC-leaves-BIOS:* the Naomi BIOS relocates itself into low main RAM
    and runs from there — `pc=0c03184c` at chocomk cartlog line 1 — so
    "PC in RAM" fires long before game handoff.
  - *First `CARTPIO`:* fires in the BIOS era on every title (header
    reads); only the cumulative threshold separates header pokes from a
    load.
  - *Per-write intercept hooks:* the arm64 dynarec fast path stores
    directly into host-mapped RAM, bypassing every C-level write function
    (the `cartlog_shimwatch` comment in fork naomi.cpp documents this).
    Cart reads are MMIO and always route through C code, so the PIO
    counter has no such blind spot.
- **Main baseline lands at the handoff trigger, never earlier** (kb §9:
  a diff is only as meaningful as its baseline). chocomk's pre-handoff
  main watermark already reads 12.58 MB of BIOS-era content; sgtetris's
  29.1 MB watermark is presumed mostly BIOS/test residue — the write-truth
  number will tell.
- **Raw diff counters only for main — no ARAM-style content dedup.** No
  fill artifact is known for main RAM, and §8 discipline adds signatures
  only when a control run proves one.
- **Cadence unchanged:** every 64th cart DMA + every 600 vblanks (~10 s),
  the existing `cartlog_sample()` sites. +32 MB scan atop the existing
  24 MB, instrumented runs only; measure once during implementation, and
  the 600-vblank constant is the knob if a frame hitch shows.
- **`CARTPIO` byte counter bundled** (the brief's open question → yes):
  it doubles as the trigger's own accumulator and gives PIO streaming
  lower bounds for gwing2-class titles.
- **Blind main = unmeasured, renormalize-and-flag, never 100** — and the
  scorer guard lands as **Task 1**, before any fork work, killing the
  100-from-nothing hazard immediately.
- **Re-run wave: anchors + faces + cluster** (user decision): cleoftp,
  ikaruga, then sgtetris, gwing2, then kurucham/ss2005/takoron/tetkiwam.
  The rest of the assessed queue re-runs lazily per the re-assessment
  rule.

## Components

### Fork (`../cleopatra/tools/flycast-src`, one commit)

- **`cartlog_handoff(const char *trigger)`** (naomi.cpp, declared in
  cartlog.h): the one-shot block extracted from `Naomi_DmaStart`
  (naomi.cpp:377–387). Latches once; allocates and snapshots three
  host-side baselines — `cartlog_aram_base` (8 MB), `cartlog_vram_base`
  (16 MB), new `cartlog_main_base` (32 MB from `mem_b`) — and emits
  `ARAMHANDOFF`/`VRAMHANDOFF`/`MAINHANDOFF baselined size=%x trigger=%s`.
  Appending `trigger=` to the existing lines is safe: the parser matches
  prefixes, the battery greps substrings. Call sites: `Naomi_DmaStart`
  (`"dma"`, where the block sits today) and the PIO threshold (`"pio"`).
- **PIO trigger + counter** (naomi_cart.cpp, `NaomiCartridge::ReadMem`
  case `NAOMI_ROM_DATA_addr`): accumulate `cartlog_pio_bytes += 2` per
  read; on crossing 32 KB with no handoff latched, call
  `cartlog_handoff("pio")`. Reads only — PIO writes to cart are not a
  loading path.
- **`cartlog_main_profile()`** (naomi.cpp): clone of
  `cartlog_vram_profile()` over `mem_b[0..32 MB)`. Emits
  `MAINPROFILE high= nz= nz_below16m= nz_above16m= size=` plus `MAINHIST`
  (128 × 256 KB buckets — the data kb §6 item 3 needs). **Skips entirely
  while `cartlog_main_base == nullptr`** — no vs-zero line ever exists
  (fork-side prevention of the §9 hole); the parser gates anyway (defense
  in depth). Wired into `cartlog_sample()`.
- **`CARTPIOCNT bytes=%llx`** (cumulative) emitted in `cartlog_sample()`.
- Memory rule honored: snapshot+diff, host-side only; instrumentation
  never mutates the guest.

### `parse_capture.py` (edit)

- `_MPROF` regex mirroring `_VPROF`; main samples **ignored until
  `MAINHANDOFF`** (the exact v5 pre-`VRAMHANDOFF` pattern).
- `main` output: `{"dma_high_water"` (kept, informational)`, "peak",
  "nz_total", "nz_above_cap"}` — `nz_above_cap` counts changed bytes
  above 16 MB.
- `handoff` gains `"trigger"` (`dma`/`pio`/`None`) parsed from the marker
  lines.
- `CARTPIOCNT` → `streaming.pio_bytes` (cumulative max; documented as a
  lower bound for PIO streaming — it counts cart→CPU reads, not
  re-reads-with-locality).
- `boot_ok` unchanged.

### `score.py` (edit — Task 1 lands the guard before fork work)

- Effective main peak = `memory.main["peak"]` when present (v6 sidecars),
  else `dma_high_water` (legacy sidecars).
- **If the effective peak is 0 on a booted title, main is unmeasured**:
  dropped from `memory_axis`'s min() and recorded as
  `scores["main_unmeasured"] = true`. One rule subsumes the gwing2 blind
  shape (`dma_high_water == 0`, `dma_events > 0`) and any future
  regression; renormalize-and-flag follows the spec-§4.3 axis-drop
  precedent. Never a fabricated u=0 → 100.

### `run_battery.py` (edit)

- `BATTERY_VERSION = "6"` with changelog comment.
- Sidecar `memory.main` becomes `{"peak", "nz_total", "nz_above_cap",
  "dma_high_water"}` (same shape as vram); `capture.handoff.trigger`
  recorded.
- `HANDOFF_TAGS` and `handoff_seen()` unchanged.

## Data flow

Fork cartlog (`MAINHANDOFF`, `MAINPROFILE`/`MAINHIST`, `CARTPIOCNT`,
`trigger=` fields) → `parse_capture.py` (gated running max) → sidecar
`memory.main.peak` / `streaming.pio_bytes` / `capture.handoff.trigger` →
`score.py` memory axis. `dma_high_water` still computed and carried,
informational only.

## Error handling

- **Old-binary/new-parser skew:** no `MAINHANDOFF` in the cartlog → main
  peak stays 0 → scorer's unmeasured path (honest, not wrong).
- **Neither DMA nor 32 KB of PIO reads:** no handoff → parks
  `no-handoff-120s` exactly as today (exotic loaders — multiboard/m3comm —
  are parked classes regardless).
- **Baseline alloc:** same `new u8[]` pattern as the existing baselines;
  instrumented runs only.
- **Pre-handoff `MAINPROFILE` line in a hand-edited/corrupt log:** parser
  gate drops it (test-pinned).

## Testing

- `test_parse_capture.py`: pre-`MAINHANDOFF` samples ignored (mirror of
  `test_pre_handoff_vram_noise`); `trigger=` parse; `CARTPIOCNT` →
  `pio_bytes`; main peak/nz_above_cap running max.
- `test_score.py`: peak preferred over `dma_high_water`; unmeasured-main
  drop renormalizes and flags; blind shape never scores 100.
- `test_metric_guards.py`: blind-main-shape guard as a standing
  invariant; committed cleoftp/ikaruga v5 sidecars still re-score green
  (legacy fallback exercised); after sgtetris's v6 re-run lands, its
  sidecar shape (`handoff.seen`, `trigger=pio`, `main.peak > 0`) is
  pinned as the PIO regression control.
- Scan-cost measurement: one-off timing of the 32 MB diff during
  implementation, recorded in the kb.

## Validation ladder (each step gates the next)

Rebuild per the recorded recipe (USE_VULKAN=ON, MoltenVK bundled from the
vanilla app); new fork commit recorded in `versions.flycast`.

1. **cleoftp** — must not park; main write-truth expected
   ≥ 11,761,888 B (CPU writes now count); VRAM/ARAM must reproduce v5
   (untouched paths). If main crosses 16 MB, investigate `MAINHIST`
   provenance (stream-cache hypothesis) before accepting any number —
   guards are never weakened to pass.
2. **ikaruga** — stays un-parked; main now measured.
3. **sgtetris** — expect `trigger=pio`, full metrics; scores or parks for
   a *real* reason; shape goldened per Testing above.
4. **gwing2** — main measured, doc tension 2 resolved; ARAM G3 stands
   (checkpoint's problem, out of scope).
5. **kurucham / ss2005 / takoron / tetkiwam** — write-truth + `MAINHIST`
   vs the old 27–30 MB clustering; findings recorded against kb §6
   item 3. No scoring-rule change here.

## Doc updates

- kb §4.v gets a RESOLVED note; new kb § for battery v6 (what changed,
  why, scan cost, threshold choice).
- `backlog-main-ram-snapshot-diff.md` status flipped to implemented,
  pointing here.
- Re-run docs/tables per RUNBOOK for every wave title.

## Out of scope

G3-ARAM address-vs-volume re-keying (`backlog-aram-gate-volume.md`), VRAM
FB masking (`backlog-vram-fb-masking.md`), any §6 checkpoint scoring
changes, scripted START-press injection (kb §4.e).

## Done means

- Fork emits `MAINHANDOFF`/`MAINPROFILE`/`MAINHIST`/`CARTPIOCNT` with the
  unified dma|pio trigger; `memory.main` scored from write-truth peak.
- sgtetris assessable end-to-end (un-parks or parks for a real reason);
  gwing2 main axis measured.
- Blind-main sidecar shape can never score 100 (guard test standing).
- `BATTERY_VERSION = "6"`; anchors re-validated first; the agreed re-run
  wave recorded; kb updated.
