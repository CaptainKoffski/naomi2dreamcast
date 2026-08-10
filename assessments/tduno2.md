# Touch de Uno! 2 (Japan) (`tduno2`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 5,484,670 B → utilization **2.615**, past `region_score()`'s `u > 2.0` gate — the **second** title measured inside the former kb §6 item-9 "empty band" (scored max `zerogu2` 1.962, parked min `takoron` 2.997), joining `toyfight` (2.035) there: the band now holds two parks (`toyfight` 2.035 · `tduno2` 2.615) below the old parked cluster (`takoron` 2.997 → `sstrkfgt` 3.687). Main RAM (content-u **0.711**) and VRAM (fit-u **0.912**) both clear their caps — ARAM is the **sole blocker**, and controls are on-ladder (`pad_adaptable`: single-point ELO AccuTouch panel the fork already drives as one absolute pointer), so this is a clean unpark-payoff candidate if the ARAM 2× multiple ever softens (kb §6 item 1; ikaruga's official DC port proved a real 4× sound trim). |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `tduno2` (no clones — MAME src/mame/sega/naomi.cpp @59e7c0b GAME row line 10965, self-keyed parent). Predecessor `tduno` "Touch de Uno! / Unou Nouryoku Check Machine (Japan)" (1999, 840-0008C, GAME row line 10947) is a separate game, not in the library. |
| Maker / year | Sega, 2000 (MAME cart-PCB notes @59e7c0b line 544: `840-0022C`, boot ROM 23071, key `317-0276-JPN`) |
| Genre / format | Touch-panel **right-brain ability-check** mini-game/quiz machine — *not* the UNO card game: the name is a 右脳 ("unou" = right brain) pun; the attract loop is all 右脳能力 ("right-brain ability") course cards over a "RIGHT BRAIN" motif (§3 shots), the official Sega history page describes answer-by-touch-panel brain-check courses ([sega.jp product 8967](https://www.sega.jp/history/arcade/product/8967/)), and the carve's own strings are per-minigame banks + nurse-hostess motion tables (`sdk_strings`: `SHINDAN 2P`, `[Nurse_RYOKO]`…, `MOT_NURSE2_*`). The Saturn/PS1 card game *Uno DX* (MediaQuest 1998, [MobyGames](https://www.mobygames.com/game/221959/uno-dx/)) is unrelated and never reached the Dreamcast. **Cart**, 840-0022C — EPR-23071 boot + 6×64 Mb mask ROMs, 49.9 MB (GAME_FORMATS.md). |
| Official DC port | No (GAME_FORMATS.md: "No"; no DC release of any Touch de Uno! entry found, searched 2026-08-11) |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | MAME parent and sole family member; the 1999 predecessor is a distinct set (different game code/cart) outside the library |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/tduno2.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set here
after screenshot review). The attract loop cycles animated course-explanation cards with "TOUCH to
START" / "FREE PLAY" overlays: touch-operation intro over the 3D TV mascot (`shot-060s.png`, "画面は
タッチするだけの簡単操作" — "controls are just touching the screen"), the 右脳カップル度チェックコース
couple-compatibility course card (`shot-121s.png`), the check-course card "4つのステージで右脳能力を
チェック。結果がプリントアウトされる" — "4 stages check your right-brain ability; results are printed
out" (`shot-304s.png`, the cabinet-printer evidence), a 3D cabinet scene with two silhouetted players
demonstrating the 2P alternating check stages (`shot-365s.png` — the cabinet's own mini-screen
renders its preview correctly), and two nurse characters over right-brain trivia copy
(`shot-548s.png`). Ten distinct animated frames across 060–609 s — the game running its attract
demo, not the DC BIOS and not a frozen splash.
Screenshots: `evidence/tduno2/shot-060s.png` · `shot-121s.png` · `shot-304s.png` · `shot-365s.png` ·
`shot-548s.png`
Anomalies: the inset "TV screen" viewport (where the attract loop should show mini-game preview
footage) renders black with garbled debris rows along its top edge in most scenes
(`shot-060s.png`/`shot-121s.png`/`shot-304s.png`), while the 3D cabinet's screen in `shot-365s.png`
renders fine — a render-to-texture presentation artifact, cosmetic only; the write-truth memory
counters are capture-side and unaffected. `shot-182s.png`, `shot-243s.png`, `shot-426s.png`,
`shot-487s.png`, `shot-609s.png` curated out as redundant course-card/nurse variants of the kept
frames.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 5,484,670 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **2.615** — past `region_score()`'s `u > 2.0` gate. Placement is the notable part:
this is the **second title measured inside the former kb §6 item-9 "empty band"** (1.962…2.997)
after `toyfight` (2.035) falsified it on 2026-08-10 — the full parked ARAM ladder now reads
`toyfight` 2.035 · **`tduno2` 2.615** · `takoron` 2.997 · `inunoos` 3.206 · `ninjaslt` 3.341 ·
`pokasuka` 3.368 · `mazan` 3.483 · `mok` 3.558 · `ringout` 3.684 · `sstrkfgt` 3.687.
`nz_above_cap` = 3,482,744 B of content above the cap (address-keyed placement figure,
informational). Address peak is 8,323,024 B (u 3.969) — the near-full-8-MiB-bank address-keyed
ceiling artifact this campaign has seen throughout (kb "ARAM write-truth vs content"), not a
tduno2-specific anomaly.

The other two regions, quoted from the sidecar — both **clear**, ARAM is the sole blocker:

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 11,931,248 | 16,777,216 | **0.711** | `nz_total` — clears comfortably; `nz_above_cap` (address-placement) 10,140,411 B · `dma_high_water` 23,646,784 B (u 1.410, address-peak read) · peak 31,288,336 B |
| VRAM (content volume + 2×fb) | 7,649,372 | 8,388,608 | **0.912** | `content_total` 6,420,572 + 2×`fb_bytes` (2×614,400, per `score.py`'s `vram_ct + 2*vram_fb`) — clears; raw `nz_total` 6,830,428 (u 0.814) · peak 15,437,824 (u 1.840) · `nz_above_cap` 3,475,369 B (address-keyed) |
| ARAM (content volume) | 5,484,670 | 2,097,152 | **2.615** | the gate — see above |

Streaming context: 188 DMA events · 16,869,400 B (16.1 MB) total · 15,191,416 B (14.5 MB) unique ·
re-read ratio 0.0995 · steady-state 0.419 MB/min (`short_window: false`) · `pio_bytes` 1,575,680 B —
a very light streamer.
Guts: code 1,572,864 B (1.5 MiB) · 1,735 functions · MMIO refs rtc 2 / g2ext 233 / scif 1 · flags
`eeprom_bios`/`serial`/`rtc`.
Similarity: `developer_match: false`, `sdk_overlap: "none"`, `cart_loader_match: false`.

Evidence: `assessments/tduno2.metrics.json` → `memory.aram`; `guts.sdk_strings` shows the ARAM
load's shape — per-minigame SE banks (`SND_SEB_KYOTU_*` common set incl. crowd/scream/applause
foley, plus `PARA`/`MATI`/`MARU`/`HEX`/`STEND`/`GOSEI`/`NUMBER`/`SIRO` minigame sets and per-course
`*CHECK`/`*COMBI`/`*OTHER` jingle families), ~30 `SND_SNG_*` BGM bank entries, and a SOUND TEST
menu listing SE/BGM/**VOICE**/**STREAM** categories — a large layered voice+BGM bank behind the
nurse-hosted quiz flow.

**Controls (researched; does not gate — on-ladder):** the cabinet is the standard **837-13844 JVS
I/O with DIPSW 5 On, an ELO AccuTouch-compatible touch-screen controller on top, and a "special
printer"** (MAME src/mame/sega/naomi.cpp @59e7c0b cart-PCB notes line 544 — the GAME row's generic
`naomi` INPUT_PORTS at line 10965 is the kb §4.g trap, not cabinet evidence; consistent with kb
§4.t: 837-13844 is the standard encoder board, only the device wired on top matters). The fork
already drives exactly this: gameId `" TOUCH DE UNOH 2 -----------"` selects `jvs_837_13844_touch`
— a **single lightgun-style absolute pointer** (`light_gun_count = 1`; maple_jvs.cpp @f014a410c
lines 602–623 with the line-617 calibration note "any >= 0x1000 value works after calibration
(tduno, tduno2)", wiring at lines 1561–1567 with `settings.input.lightgunGame = true`) — and
emulates the printer (`printer::init()`, naomi_cart.cpp lines 709–714; JVS custom cmd `0x74` pipes
board serial to `printer::print`, maple_jvs.cpp line 2450). Single-point touch on an untimed
touch-the-answer quiz reduces to one absolute pointer, so a pad-driven cursor covers it (DC mouse
or light gun as natural upgrades) → `controls.device_class = pad_adaptable` — unlike `pokasuka`'s
frantic multi-touch panel (off-ladder `touchscreen`). The **printer is output-only**: the
results-sheet printout (attract card "結果がプリントアウトされる", `shot-304s.png`) has no
DC equivalent — a feature cut (or VMU-screen substitute) for a port, not a control blocker.
Sources (all mirrored in sidecar `controls.sources`): MAME naomi.cpp @59e7c0b line 544; Flycast
fork maple_jvs.cpp / naomi_cart.cpp @f014a410c as cited;
[sega.jp arcade history](https://www.sega.jp/history/arcade/product/8967/) (Touch de Uno! =
right-brain check variety game, touch-panel answers);
[Game Watch on Touch de Zunou](https://game.watch.impress.co.jp/docs/20060720/zuno.htm) (third in
the "Touch" series — same lineage, later 837-14672 hardware);
[MobyGames Uno DX](https://www.mobygames.com/game/221959/uno-dx/) (name disambiguation).

What would unblock it: **(a) ARAM gate softening at a future §6 checkpoint** (kb §6 item 1 — the
2× multiple is the open ruling, with ikaruga's official DC port's real 4× sound trim as the outer
bound): at 2.615× with main and VRAM both clear and `pad_adaptable` controls, `tduno2` joins
`toyfight` as the in-band unpark payoff — any threshold above ≈2.62 scores it. **(b) A real
sound-trim argument:** the over-cap bytes are voice/SE/BGM banks (SOUND TEST's VOICE/STREAM
categories + the per-minigame bank tables above); 2.615× is inside the 4× trim ikaruga's shipped
DC port achieved by downsampling/ADPCM, so a port-side trim case is plausible on its face — it
just needs someone to make it with numbers.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — second in-band ARAM park (u 2.615 inside the former item-9 (1.962, 2.997) band, after toyfight); main/VRAM clear, ARAM sole blocker; cabinet = 837-13844 + ELO AccuTouch panel + printer, fork drives it as one absolute pointer → `pad_adaptable`; game is the right-brain-check machine, not the UNO card game |
