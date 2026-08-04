# Pokasuka Ghost! (Japan) (`pokasuka`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram peak > 2x DC capacity`** |
| Bottom line | Boots and runs its full whack-the-ghost attract demo, but carries 4.83 MiB of genuine (fill-excluded) sound content above the DC's 2 MiB ARAM cap — a real G3, not the DMPD artifact — and is a touchscreen cabinet besides. |
| Assessed | 2026-08-04 · battery v4 · flycast `4b59eceff` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

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

**G3 memory: aram peak > 2x DC capacity.** `memory.aram.peak = 8,339,264 B`
(content high-address) with `nz_above_cap = 5,068,309 B` of fill-excluded content
against the DC's 2,097,152 B AICA RAM → the sound bank genuinely cannot fit even
after repacking (above-cap content alone is 2.4× the whole DC ARAM).
Evidence: `assessments/pokasuka.metrics.json` → `memory.aram`; v4 `ARAMPROFILE`
content fields.

What would unblock it: a per-title audio trim (voice/SFX bank reduction of ~3.5×)
— nothing the battery can measure further.

Secondary blocker (does not currently gate — G3 fires first): the cabinet is a
**touchscreen** (`controls.device_class = touchscreen`, off-ladder → would gate
G2). Sources: MAME INPUT_PORTS cite in sidecar; the attract demo itself instructs
画面をタッチしてね ("touch the screen") — `evidence/pokasuka/shot-609s.png`. A DC
mouse/light-gun mapping is conceivable but is redesign territory.
