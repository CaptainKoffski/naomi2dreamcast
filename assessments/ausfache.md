# Akatsuki Blitzkampf Ausf. Achse (Japan) (841-0058C) (`ausfache`) — portability assessment

> **Battery v9 main-content re-score (2026-08-08): 80.7 (S), was 79.8 (A)** — scoring-only blanket re-score, no re-capture: every measurement
> below is still the battery v7 run. §6 item 8 ruling (spec `2026-08-08-main-content-rekey-design.md`,
> adopted to main 2026-08-09): main now keys on write-truth content VOLUME instead of
> the address peak — `nz_total` 8,000,910 B (content-u 0.477) replaces peak 16,349,952 B (u 0.975).
> Memory axis 89.4, binding region now **vram** (was memory 86.9). Verdict section below is the capture-time (v≤8) record.

> **Battery v7 aram-volume + main-write-truth re-run (2026-08-07): 79.8 (A)** — up from
> v5's 79.1, tier unchanged. This title skipped v6 entirely (last real run was v5), so
> two independent instrumentation changes land in the same run: (1) the §6 checkpoint
> re-keys G3-ARAM on content **volume** — `content_total` = 1,561,912 B (u = 0.745, well
> under the 2 MiB cap, sub-score 100.0 — ARAM is no longer close to binding); (2) main
> RAM gets write-truth-measured for the first time (battery v6's MAINPROFILE
> snapshot+diff, landed between v5 and v7) and reveals genuine near-cap usage invisible
> to the old DMA-high-water accounting — write-truth peak **16,349,952 B (u = 0.9745,
> sub-score 86.9)**, now the *binding* region, vs. the v5 doc's DMA high-water of only
> 5,065,888 B (u = 0.30, still reproduced below as an informational floor). VRAM
> (7,892,608 B, u = 0.9409) reproduces bit-identically to v5. Net effect: memory axis
> rises 85.0 → 86.9, final 79.1 → **79.8 (A)**. The v5/v2 sections' "everything fits but
> sound" framing is now dated for main RAM specifically: that was a DMA-high-water blind
> spot (kb §4.v family), not evidence main was lightly used — the write-truth figure
> sits at 97.45% of the DC cap, the tightest fit in this doc.

## v7 verdict & measurements

| | |
|---|---|
| **Final** | **79.8 (A)** |
| Coverage | demo (live attract gameplay in `shot-609s.png`, same evidence frame as v5) |
| Assessed | 2026-08-06 · battery v5 · flycast `ebae3b513` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b`; aram-volume re-run 2026-08-07 · battery v7 · flycast `65f9f7857` |
| Boot | ok=True · handoff 20.0 s (`trigger = "pio"`) · run 600 s · rom `naomi/ausfache.zip` |

| Region | v7 peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (write-truth) | 16,349,952 | 16,777,216 | **0.9745** | nz_total 8,000,910 · above cap 0 · `dma_high_water` 5,065,888 (u=0.30, the old v5 scoring input — informational floor now the DMA counter never saw the rest) — **new binding region** |
| VRAM (write-truth diff, post-handoff) | 7,892,608 | 8,388,608 | 0.9409 | nz_total 3,699,405 · 0 above cap (bit-identical to v5) |
| ARAM (content volume, fill-excluded) | 1,561,912 | 2,097,152 | **0.745** | `content_total` (§6 volume-keyed, battery v7) — sub-score 100.0, no longer close to binding; old write-truth address peak 2,097,136 (u≈1.00, pre-v7 keying) unchanged |

Streaming: 458 DMA events · total 50.2 MB · unique 24.7 MB · re-read 0.507 · steady 5.055 MB/min (matches v5 within run-to-run noise)
Axes: memory 86.9 · streaming 79.8 · guts 85.0 · controls 100.0 · similarity 40.0 → **final 79.8 (A)**
Screenshots: `evidence/ausfache/shot-060s.png` · `evidence/ausfache/shot-365s.png` · `evidence/ausfache/shot-609s.png`

## Historical: battery v5 measurements (superseded by v7 above)

> **Battery v5 re-assessment (2026-08-06): **79.1 (A)**.**
> v4's 58.4 (B) charged the game for 40,664 B of VRAM above the DC cap at
> `0x93e738` — proven to be the Naomi BIOS boot-screen texture sheet (fonts +
> NAOMI logo), uploaded **pre-handoff** and captured by a v4 sampling hole
> (profile tick armed before the VRAM baseline exists → diff vs zero →
> max-merged into the game peak). A dump-instrumented control run reproduced
> the artifact byte-exactly pre-handoff and showed **zero** game writes above
> 8 MB across the whole window. Root-cause + proof:
> `docs/kb/assessment-tooling.md` §9. The v2-era section at the bottom keeps
> the identity/controls/similarity research; its measured figures are
> superseded (kb §7) — note its VRAM figure 7,892,608 matches v5 exactly.

## v5 verdict & measurements

| | |
|---|---|
| **Final** | **79.1 (A)** |
| Coverage | demo (live attract gameplay in `shot-609s.png`) |
| Assessed | 2026-08-06 · battery v5 · flycast `ebae3b513` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |
| Boot | ok=True · handoff 20.0 s · run 600 s · rom `naomi/ausfache.zip` |

| Region | v5 peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (DMA high-water) | 5,065,888 | 16,777,216 | 0.30 |  |
| VRAM (write-truth diff, post-handoff) | 7,892,608 | 8,388,608 | 0.94 | nz_total 3,691,629 · **0 above cap** |
| ARAM (content, fill-excluded) | 2,097,136 | 2,097,152 | 1.00 | content above cap 0 |

Streaming: 459 DMA events · total 47.9 MB · unique 23.6 MB · re-read 0.5066 · steady 5.062 MB/min
Axes: memory 85.0 · streaming 79.8 · guts 85.0 · controls 100.0 · similarity 40.0 → **final 79.1 (A)**
Every metric except the corrected VRAM peak is byte-identical to the v4 run (459
DMA events, same watermarks) — the fork binary is unchanged; only the parser
stopped counting the pre-handoff BIOS sample. ARAM sits 16 B under the DC cap
(u ≈ 1.00, the binding memory region): a port still wants the standard audio
trim margin, but nothing is over budget anywhere.
Screenshots: `evidence/ausfache/shot-060s.png` · `evidence/ausfache/shot-365s.png` · `evidence/ausfache/shot-609s.png`

## Historical: battery v4 measurements (superseded by v5, kb §9)

v4 (2026-08-04, flycast `4b59eceff`): final **58.4 (B)** — memory 57.0 with
VRAM "peak" 9,692,984 / 40,664 B above cap. Both figures were the pre-handoff
BIOS boot-frame artifact; all other v4 numbers match v5 above.

---

# Historical: battery v2 assessment (measurements superseded)

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram peak > 2x DC capacity`** (not a numeric tier) |
| Bottom line | The campaign's most extreme "only sound blocks it" case. The full 8 MiB Naomi ARAM bank is written at boot (4.00× the DC's 2 MiB AICA RAM) — the **ninth** boot-time full-bank G3-aram park — and it is the **only** number over budget in the entire sidecar: main-RAM DMA high-water is 4,777,120 B = **0.28×** (fits the DC's 16 MB with ~11 MB to spare, the campaign's lightest by far) and VRAM peak 7,892,608 B = **0.94×** (fits the 8 MB cap outright, nz_total 3,600,148 B, nothing above cap). The doujin-PC-origins prior is confirmed by measurement: 2003–2007-era PC assets fit DC hardware. If the kb §6 checkpoint softens the ARAM rule, ausfache leapfrogs `radirgyn` as THE unpark candidate — and since Ausf. Achse never left the arcade (no port on any platform), a 3-button fighter port would also be the most *valuable* target on the board. |
| Assessed | 2026-08-03 · battery v2 · flycast `9e882cbd2` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `ausfache` (single member — `parent: null` in controls.json, no clones in naomi.cpp) |
| Maker / year | Subtle Style, 2008 (arcade debut 2008-02-20). Doujin circle founded April 2000; Ausf. Achse is its only Naomi title ([Wikipedia](https://en.wikipedia.org/wiki/Akatsuki_Blitzkampf)) |
| Genre / format | 2D fighter (queue genre "?" resolved), **cart, Naomi M4** 841-0058C, rom_board id `5504`, ROT0 — MAME src/mame/sega/naomi.cpp @59e7c0b GAME line 11116 (`naomim4`), ROM_START lines 6808–6822: 2× 64 MiB flash (ic8/ic9, IC10/IC11 populated-empty). **Clean PIC key** `317-05130-jpn.ic3` (CRC `eccdcd59`, no BAD_DUMP — contrast zunou's BAD_DUMP key at naomi.cpp:6669 that caused its G1; Flycast fork agrees, naomi_roms.cpp:4583). Arcadeitalia's "BAD DUMP" badge is stale metadata refuted by the primary source |
| Official DC port | No — and no port of Ausf. Achse exists **anywhere**. Lineage: doujin PC *Akatsuki Shisei Ichigō* (2003) → *Akatsuki Blitzkampf* (PC, 2007-04-30) → *Ausf. Achse* (Naomi, 2008); sequels are the EN-Eins line (System Board Y2 2010, NESiCAxLive 2012/2023). A Windows port of Ausf. Achse announced 2019-03-29 was never released (COVID-delayed) ([Wikipedia](https://en.wikipedia.org/wiki/Akatsuki_Blitzkampf), [Akatsuki/En-Eins wiki](https://akatsuki-en1.fandom.com/wiki/Akatsuki_Blitzkampf)); no PS4 or Steam release |
| Community ports | None found (searched 2026-08-02) — only generic "can Naomi run on DC" threads ([dreamcast-talk](https://www.dreamcast-talk.com/forum/viewtopic.php?t=2001), [GameFAQs](https://gamefaqs.gamespot.com/boards/916412-dreamcast/73913493)); YouTube "Dreamcast/Naomi" videos are emulator captures. An active Fightcade/Flycast netplay scene runs the Naomi version ([RetroAchievements](https://retroachievements.org/game/17891), [mainline Flycast video](https://www.youtube.com/watch?v=gBJtj_P6HJE)) |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: yes · handoff at 30.0 s · run 600 s · rom: `naomi/ausfache.zip` (single clean zip leg)
Attract/demo reached: **title (conservative)** — sidecar `capture.coverage = "title"`;
visual classification is impossible (see Display blindness), so the lower-bound label is
used even though activity metrics show the game running for the full window.

### Display blindness

All 10 battery screenshots share a single MD5 — the same frozen NAOMI cart splash. That
is a **stale TA frame** left in the GL display path (kb §4.m class, same as `kurucham` /
`ss2005`), not a hang: underneath it the game verifiably runs — BIOS handoff at 30.0 s,
3,600,148 B of nonzero VRAM drawn (vs the bare splash's ~237 KiB, kb §4.p), the full
8 MiB ARAM bank loaded, and 415 cart-DMA events / 43,786,240 B streamed across the
window. Note the contrast with §2's mainline-Flycast videos: mainline renders the game
fine; under OUR fork the capture is display-blind — no contradiction, it is the kb §4.m
stale-TA-frame mechanism in the fork's screenshot path.

Screenshots kept (first + last, identical splash, proving the freeze):
- `assessments/evidence/ausfache/shot-060s.png` — frozen NAOMI cart splash at t=60 s
- `assessments/evidence/ausfache/shot-600s.png` — same splash at t=600 s, unchanged
Anomalies: display blindness as above; none otherwise — single clean leg.

## Gate

**G3 memory: aram peak > 2x DC capacity.** `memory.aram.peak = 8,388,608 B` (exactly
8 MiB, the full Naomi ARAM bank) against the DC's 2,097,152 B AICA RAM → utilization
4.00×, past `region_score()`'s `u > 2.0` gate; `nz_above_cap = 6,291,456 B` nonzero
above the cap at scan. Boot-time full-bank load — **ninth** in the kb §6 tally.

**The sound bank is the only over-budget number in the sidecar.** Main-RAM DMA
high-water `4,777,120 B` = 0.28× the DC's 16 MB — the campaign's lightest main figure —
and VRAM peak `7,892,608 B` = 0.94× the 8 MB cap (nz_total `3,600,148 B`,
`nz_above_cap = 0`). Every prior full-bank park carried at least one other over-cap
region; ausfache carries none. The measurement confirms the research prior: this is a
2D sprite fighter whose content was authored for a 2003–2007 low-spec doujin PC, and it
fits DC budgets everywhere except the luxury full-bank sound load.

What would unblock it: a per-title audio trim (downsample PCM/ADPCM — the standard
full-bank remedy with released-port precedent, kb §4.d Ikaruga 4× trim) — and nothing
else. If the kb §6 checkpoint softens the ARAM rule, this is the strongest unpark
candidate in the campaign, ahead of `radirgyn` (which still carried main 1.17× /
VRAM 1.33×).

Context values quoted from the sidecar (no axis scores exist — the pipeline stops at
the gate): streaming 415 DMA events, `43,786,240 B` total / `24,932,352 B` unique,
re-read ratio 0.4306, steady-state 4.487 MB/min (`short_window: false`). Guts were
**unavailable at v2 time**: the M4 cart broke the `cart2dat.py` static scan (kb §4.q
fourth instance, `rom=0x40000000 len=0x100000`) → `guts.dat_available = false`, no
sdk_strings, and `similarity.sdk_overlap = "none"` was an artifact of that gap, not
evidence. **Re-scanned 2026-08-06** after the `carve_boot.py` bit-30 fix: the M4
load-entry rom offset carries bit 30 as an encrypted-read flag, not a file offset
(MAME `src/mame/sega/naomim4.cpp:124-125` @59e7c0b, Flycast `m4cartridge.cpp:115,132`
@ebae3b513); masking it (`& 0x1ffffffe`) lets the scan carve and Ghidra-analyze the
1 MiB boot blob → `guts.dat_available = true`, guts axis **85.0**,
`similarity.sdk_overlap = "partial"`, similarity axis **40.0** (v5 axes above;
capture itself was not re-run).

## Risks & notes

- **Port-planning takeaway, stated plainly: everything fits but sound.** Main 0.28×,
  VRAM 0.94× (all nonzero content below cap), streaming light at 4.487 MB/min — the
  8 MiB boot-time sound bank is the single blocker, and it is the blocker class with
  the best released-port precedent (Ikaruga DC's 4× trim). No port of Ausf. Achse
  exists on any platform, so a DC port would be uniquely valuable, not redundant.
- **Display-path gap blocks emulator validation under our fork** — a stale TA frame
  masks a running game (kb §4.m). Mainline Flycast demonstrably renders the title
  (§2 links), so the gap is fork/capture-side; per the working-style rule, rendering
  of any ported build must be verified on real DC hardware.
- **M4 guts gap: closed 2026-08-06.** `carve_boot.py` now masks bit 30 (the M4
  encrypted-read flag) on cart load-entry offsets, so the static scan carves and
  Ghidra-analyzes the boot blob. Re-scored via `tools/assess/rescore_static.py`
  (guts 85.0, similarity 40.0, final 79.1 A above); capture was not re-run.
- **Controls are the easy axis**: `controls.device_class = stick` — 8-way stick +
  3 attack buttons (A/B/C = Weak/Medium/Strong; throw and Reflector parry are
  mechanics on the same buttons), 2P. 1:1 on a stock DC pad (A/B/X + Start) and
  native on the DC Arcade Stick. Sources: MAME src/mame/sega/naomi.cpp @59e7c0b
  INPUT_PORTS `naomi` (line 11116); Flycast per-title descriptor
  `naomi_roms_input.h:195` `INPUT_3_BUTTONS("Weak Attack", "Medium Attack", "Strong
  Attack")` (strongest citation);
  [Mizuumi Controls](https://mizuumi.wiki/w/Akatsuki_Blitzkampf/Controls);
  [arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=ausfache)
  (the "6 buttons" there is the generic JVS standard declaration).
- Main watermark `16,371,936 B` (informational, stale-data-prone) vs DMA high-water
  4,777,120 B — a 3.4× gap; per the v1 limitation some CPU-written data above the
  last DMA'd asset is likely, but even the full watermark still fits under 16 MB.
- MAME status is the blanket naomi.cpp `GAME_FLAGS` (no per-title signal, kb §4.r);
  the game runs under our fork and renders under mainline Flycast regardless.
