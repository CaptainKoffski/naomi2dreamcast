# Pokasuka Ghost! (Japan) (`pokasuka`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** — reconfirmed 2026-08-07 (battery v7) on the volume-keyed message |
| Bottom line | Boots and runs its full whack-the-ghost attract demo, but carries `content_total` = 7,064,300 B (u = 3.369, §6 volume-keyed) of real sound content against the DC's 2 MiB ARAM cap — a real G3, not the DMPD artifact, and heavy enough that the §6 checkpoint's volume-vs-address re-keying doesn't change the outcome (5,068,306 B of that sits above the cap alone, essentially unchanged from the v4 figure). Also a touchscreen cabinet besides. |
| Assessed | 2026-08-04 · battery v4 · flycast `4b59eceff` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b`; aram-volume re-run 2026-08-07 · battery v7 · flycast `65f9f7857` |

## 2. Identity

| | |
|---|---|
| Set / family | `pokasuka` (no clones) |
| Maker / year | Sega, 2007 |
| Genre / format | Touchscreen action (whack-a-ghost), cart |
| Official DC port | None found |
| Community ports | None found |
| Representative choice | Only set in family |

## 3. Boot & run evidence

Boots: yes · run 600 s · rom: `naomi/pokasuka.zip`
Attract/demo reached: **demo** — tutorial-attract gameplay with live score/quota
counters: "ひっぱれ!" pull-the-ghost at `evidence/pokasuka/shot-365s.png`,
"叩け!" whack-with-the-wand at `evidence/pokasuka/shot-609s.png`.
Screenshots: `evidence/pokasuka/shot-060s.png` · `shot-365s.png` · `shot-609s.png`
Anomalies: none — clean single-leg full-window run.

An earlier uncommitted v2 sidecar parked it G3 with `aram nz_above_cap =
5,130,927` under the artifact-prone write-truth metric; the v4 content metric
(fill runs excluded) independently confirms 5,068,309 B above cap — this park is
real, unlike the ten v2 fill-artifact parks (`docs/kb/assessment-tooling.md` §7).

## Gate

**G3 `aram content > 2x DC capacity` — reconfirmed 2026-08-07 (battery v7) on the volume-keyed message; the §6 checkpoint's re-keying doesn't change the outcome, this content is genuinely heavy.**

| Region | Peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (write-truth) | 33,554,432 | 16,777,216 | **2.000** | exactly `0x2000000` — a suspiciously round number (kb §6 stream-cache-placement family, same class as takoron's exact `0x1C00000`); nz_total 15,837,112 · above cap 7,270,360 · `dma_high_water` 33,030,144 (u=1.97, close but not identical) — moot for gating, ARAM gates first |
| VRAM (write-truth diff) | 10,465,280 | 8,388,608 | 1.248 | nz_total 3,626,053 · above cap 1,866,630 |
| ARAM (content volume, fill-excluded) | 7,064,300 | 2,097,152 | **3.369** | `content_total` (§6 volume-keyed, battery v7) — well past the u>2.0 gate; `nz_above_cap` 5,068,306 B (essentially unchanged from v4's 5,068,309 B, a 3 B run-to-run delta) |

Streaming: 11,140 DMA events · total 133.3 MB · unique 34.9 MB · re-read 0.7383 ·
steady 12.18 MB/min.
Evidence: `assessments/pokasuka.metrics.json` → `memory.aram`; v4/v7 `ARAMPROFILE`
content fields agree the sound bank genuinely cannot fit even after repacking
(above-cap content alone is 2.4× the whole DC ARAM).

What would unblock it: a per-title audio trim (voice/SFX bank reduction of ~3.5×)
— nothing the battery can measure further.

Secondary blocker (does not currently gate — G3 fires first): the cabinet is a
**touchscreen** (`controls.device_class = touchscreen`, off-ladder → would gate
G2). Sources: MAME INPUT_PORTS cite in sidecar; the attract demo itself instructs
画面をタッチしてね ("touch the screen") — `evidence/pokasuka/shot-609s.png`. A DC
mouse/light-gun mapping is conceivable but is redesign territory.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v4 | 2026-08-04 | PARKED G3-ARAM | First assessment: ARAM over 2× cap on the address-keyed rule, `nz_above_cap` 5,068,309 B of real content |
| v7 | 2026-08-07 | PARKED G3-ARAM | Reconfirmed on the §6 volume keying — `content_total` 7,064,300 B (u 3.369), re-keying changes nothing (spec `2026-08-07-aram-gate-volume-design.md`) |
