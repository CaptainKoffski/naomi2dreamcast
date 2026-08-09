# Pokasuka Ghost! (Japan) (`pokasuka`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** — reproduced 2026-08-10 (battery v9) on a fresh capture, the same volume-keyed message as v7 |
| Bottom line | Boots and runs its full whack-the-ghost attract demo, but carries `content_total` = 7,064,212 B (u = 3.368, §6 volume-keyed) of real sound content against the DC's 2 MiB ARAM cap — a real G3, not the DMPD artifact, essentially byte-identical to the v7/v4 reads (three straight captures agree). Main RAM and VRAM, both measured under content-volume keying on this title for the first time this pass, actually clear their own caps (main u ≈ 0.944 via `nz_total`; VRAM u ≈ 0.561 via `content_total`+2×`fb_bytes`) — reversing the old address-peak reads that made main look exactly at 2× and VRAM 1.25× — but it's moot: ARAM gates first regardless. Also a touchscreen cabinet besides. |
| Assessed | capture 2026-08-10 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — fresh v9 capture (parked-list groom), superseding the v7 capture (see History) |

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

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s ·
rom: `naomi/pokasuka.zip` (byte-identical handoff fields to v7: `aram_zeroed`,
`vram_zeroed`, `main_baselined` all true)
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote
`null`; set here after screenshot review, reproducing v7). Live score/quota-counter
tutorial-attract gameplay across three distinct mechanics: "叩け!" whack-with-the-wand
at `evidence/pokasuka/shot-060s.png`, "ひっぱれ!" pull-the-ghost at
`evidence/pokasuka/shot-182s.png`, "打ち返せ!" knock-back at
`evidence/pokasuka/shot-548s.png`, plus the title/logo loop at `shot-304s.png` and
`shot-487s.png` — same conclusion as v7.
Screenshots: `evidence/pokasuka/shot-060s.png` · `shot-182s.png` · `shot-304s.png` ·
`shot-487s.png` · `shot-548s.png`
Anomalies: none. One mid-run shot (`shot-609s.png`, the old v7-curated close) landed on
a fade-to-black attract transition this capture and was curated out for readability
(same class as `inunoos`'s fade-to-white transition shots) — not a capture fault, just
which frame the fixed 60 s interval happened to land on this run.

An earlier uncommitted v2 sidecar parked it G3 with `aram nz_above_cap =
5,130,927` under the artifact-prone write-truth metric; the v4 content metric
(fill runs excluded) independently confirmed 5,068,309 B above cap — this park is
real, unlike the ten v2 fill-artifact parks (`docs/kb/assessment-tooling.md` §7). v9's
fresh capture reproduces that figure exactly: `nz_above_cap` = 5,068,306 B, byte-identical
to v7 and within 3 B of the v4 read.

## Gate

**G3 `aram content > 2x DC capacity` — reproduced 2026-08-10 (battery v9) on a fresh
capture; the §6 checkpoint's volume keying still doesn't change the outcome, this
content is genuinely heavy across three straight captures (v4/v7/v9).**

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 15,837,112 | 16,777,216 | 0.944 | `nz_total`, first measured as the scoring key this pass (v9 main-content rekey, spec `2026-08-08-main-content-rekey-design.md`) — **clears** the 1x cap, reversing the old address-peak read (peak 33,554,432, exactly `0x2000000`, u=2.000 — a suspiciously round placement artifact, kb §6 stream-cache-placement family); above cap (address) 7,270,360 · `dma_high_water` 33,030,144 (u=1.97) — byte-identical to v7 on every raw field; moot either way, ARAM gates first |
| VRAM (content volume + 2×fb) | 4,706,832 | 8,388,608 | 0.561 | `content_total` 2,871,312 + 2×`fb_bytes` 917,760 (both first measured on this title this pass, v8 FB-masking keying, spec `2026-08-07-vram-fb-masking-design.md`) — clears the cap even more comfortably than the old address-peak read (peak 10,465,280, u=1.248, itself never gating); raw nz_total 3,626,053 · above cap 1,866,630 — byte-identical to v7 |
| ARAM (content volume, fill-excluded) | 7,064,212 | 2,097,152 | **3.368** | `content_total` (§6 volume-keyed) — well past the u>2.0 gate; reproduces v7's 7,064,300 B within 88 B (−0.0012%, noise); `nz_above_cap` 5,068,306 B — byte-identical to v7, and within 3 B of the v4 figure (5,068,309 B) |

Streaming (all deltas ≤0.3%, ordinary run-to-run jitter, not a regression): 11,104 DMA
events (v7: 11,140) · total 133.0 MB (v7: 133.3 MB) · unique 34.9 MB (byte-identical) ·
re-read 0.7378 (v7: 0.7383) · steady 12.15 MB/min (v7: 12.18) · `pio_bytes` 3,149,632
(byte-identical). `guts` (code 3,145,728 B · 5,337 functions · mmio_refs
rtc 3/g2ext 257/scif 48 · flags `eeprom_bios`/`serial`/`rtc`) and `similarity`
(`developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: false`) are
all byte-identical to v7.

Evidence: `assessments/pokasuka.metrics.json` → `memory.aram`; v4/v7/v9 ARAM content
fields agree the sound bank genuinely cannot fit even after repacking (above-cap
content alone is 2.4× the whole DC ARAM).

What would unblock it: a per-title audio trim (voice/SFX bank reduction of ~3.5×) —
nothing the battery can measure further. Main RAM and VRAM, now both measured under
content-volume keying for the first time on this title, already clear their caps — the
ARAM sound bank is the sole remaining memory blocker.

Secondary blocker (does not currently gate — G3 fires first, and would not change even
if the ARAM figure ever cleared): the cabinet is a **touchscreen**
(`controls.device_class = touchscreen`, off-ladder → would gate G2 per RUNBOOK's
off-ladder rule regardless of any memory fix). Controls research carried forward from
v7, not re-run this pass. Sources: MAME INPUT_PORTS cite in sidecar; the attract demo
itself instructs 画面をタッチしてね ("touch the screen") — visible on every curated
shot's top-right corner this run, e.g. `evidence/pokasuka/shot-060s.png`. A DC
mouse/light-gun mapping is conceivable but is redesign territory.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v4 | 2026-08-04 | PARKED G3-ARAM | First assessment: ARAM over 2× cap on the address-keyed rule, `nz_above_cap` 5,068,309 B of real content |
| v7 | 2026-08-07 | PARKED G3-ARAM | Reconfirmed on the §6 volume keying — `content_total` 7,064,300 B (u 3.369), re-keying changes nothing (spec `2026-08-07-aram-gate-volume-design.md`) |
| v9 | 2026-08-10 | PARKED G3 memory: aram content > 2x DC capacity | parked-list groom: fresh v9 capture (was v7) — gate reproduced (`content_total` 7,064,300→7,064,212 B, u 3.369→3.368, −0.0012%); all other shared raw counters (main peak/nz_total/nz_above_cap/dma_high_water, vram peak/nz_total/nz_above_cap, aram nz_above_cap, streaming dma_events/total_bytes/unique_bytes/reread_ratio/steady_mb_per_min/pio_bytes, handoff trigger/t) byte-identical or within ≤0.3% jitter; main and vram now measured under first-time content-volume keying on this title (main `nz_total`, vram `content_total`+2×`fb_bytes`) and both clear their caps (main u≈0.94, vram u≈0.56, reversing the v7 address-peak reads) — ARAM sound bank is the sole memory blocker; touchscreen controls carried forward unresearched |
