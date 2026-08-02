# {{Title}} (`{{set}}`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **{{final}}** ({{tier}}) |
| Bottom line | {{one sentence: why this rank}} |
| Assessed | {{date}} · battery v{{battery}} · flycast `{{flycast_commit}}` · Ghidra {{ghidra}} · MAME `{{mame_src}}` |

## 2. Identity

| | |
|---|---|
| Set / family | `{{set}}` (covers: {{clone list or "no clones"}}) |
| Maker / year | {{maker}}, {{year}} |
| Genre / format | {{genre}}, {{cart or GD-ROM}} |
| Official DC port | {{No / Partial + note}} |
| Community ports | {{none found / links}} |
| Representative choice | {{why this set represents the family}} |

## 3. Boot & run evidence

Boots: {{yes/no}} · handoff at {{t}} s · run {{secs}} s · rom: `{{rom_used}}`
Screenshots: {{links to evidence/<set>/shot-*.png}}
Anomalies: {{none / description}}

## 4. Memory fit (axis: {{memory score}})

| Region | Peak | DC capacity | Utilization | Sub-score | Evidence |
|---|---|---|---|---|---|
| Main RAM (DMA high-water) | {{bytes}} | 16 MB | {{u}} | {{s}} | grep `CARTDMA` in raw log |
| VRAM (write-truth) | {{bytes}} | 8 MB | {{u}} | {{s}} | grep `VRAMPROFILE` |
| ARAM (write-truth) | {{bytes}} | 2 MB | {{u}} | {{s}} | grep `ARAMPROFILE` |

Watermarks (informational, content-scan — stale-data prone): {{main/vram/aram}}.
{{Risk flag if main watermark ≫ high-water.}}

## 5. Cart streaming (axis: {{streaming score}})

DMA events {{n}} · total {{MB}} · unique {{MB}} · re-read ratio {{r}} ·
steady-state {{MB/min}} {{(short-window flag?)}}

## 6. Guts (axis: {{guts score or "n/a — no .dat"}})

Code {{bytes}} · functions {{n}} · MMIO refs: scif {{n}}, rtc {{n}}, g2ext {{n}} ·
BIOS vector refs: {{map}} · penalties applied: {{flags → numbers}}

## 7. Controls (axis: {{controls score or gate}})

Cabinet: {{description}}. MAME input ports: `{{input_ports}}`.
Proposed DC mapping: {{pad/peripheral proposal}}.
Sources: {{≥2 citations, URLs}}

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = {{m}}^.40 · {{st}}^.20 · {{g}}^.20 · {{c}}^.10 · {{si}}^.10 = **{{final}}**
{{If guts dropped: note renormalized weights .50/.25/.125/.125.}}
Similarity inputs: developer {{y/n}}, SDK overlap {{full/partial/none}}, loader match {{y/n}}.

## 9. Risks & notes

- {{main-RAM v1 limitation: CPU-written data above DMA assets not captured}}
- {{anything odd; what a port project should verify first}}
