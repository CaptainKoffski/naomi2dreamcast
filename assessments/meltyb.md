# Melty Blood Act Cadenza Version B2 (Japan) (GDL-0039A) (`meltyb`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **52.4 (B)** |
| Bottom line | VRAM is the binding constraint — FB-masked content fit 9,978,034 B (`content_total` 8,749,234 + 2×`fb_bytes` 1,228,800) against the 8 MB cap (u 1.1895) drags the memory axis to 50.9, even though main RAM (u 0.9203, 91.0) sits just under its cap and ARAM (u 1.0248, 80.5) also lands just past its own 1x line without binding — `region_score()`'s `min()` makes VRAM's 50.9 the memory axis. Streaming is mid-low (65.3), driven by a re-read ratio of 0.5595 that runs far heavier than the sibling GD-ROM fighters `ggxx`/`ggxxac`/`ggxxsla` (0.27–0.31) and is close to the cart title `mbaa`'s 0.5811 despite `meltyb` itself being GD-ROM. Controls is a perfect 1:1 stick+6-button fit (100.0). Guts could not be measured — the static-scan carve failed (`entrypoint 0x8c021000 outside carved image 0xc020000..0xc1a0000`) — so that axis drops and weights renormalize to .50/.25/.125/.125 (spec §4.3); the same carve failure also forces `cart_loader_match` to `false` (it requires `guts.dat_available`) despite `meltyb` being GD-ROM format like the anchor titles, and `sdk_overlap` to `none` (no `sdk_strings` extracted), pulling similarity to 20.0 — well below the ~70 a healthy GD-ROM carve scores elsewhere in this campaign. This is the fourth Naomi fighter this session to land VRAM-bound in the 1.0–1.6x overage band, alongside `ggxx` (55.4 B), `ggxxac` (65.4 A), and `mbaa` (55.9 B); no DC port, official or fan, exists for any Melty Blood Act Cadenza revision to validate against. |
| Assessed | 2026-08-10 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `meltyb` (covers: `meltybo` — clone in MAME `naomi.cpp` @59e7c0b line 11286: `GAME( 2006, meltybo, meltyb, naomigd, naomi, ... )`, parent `meltyb`; `GAME_FORMATS.md` lists `meltybo` "Melty Blood Act Cadenza Version B (Japan) (GDL-0039)" as "clone of `meltyb`") |
| Maker / year | Ecole Software, 2006 (sidecar `maker`/`year`) |
| Genre / format | Fighting ★ (2D versus fighter), **GD-ROM**, machine `naomigd` (`tools/assess/out/controls.json`) — `rom_used` `naomi/meltyb.zip` is a GD-ROM DIMM-firmware bootstrap (BIOS zip + `.chd` pair), not a single cart image; contrast with sibling `mbaa` (naomim4 cart, `assessments/mbaa.md` §2) |
| Official DC port | **No.** `GAME_FORMATS.md` marks "No" for `meltyb`. The Act Cadenza arcade original released on Naomi in March 2005 ([Wikipedia: Melty Blood](https://en.wikipedia.org/wiki/Melty_Blood), accessed 2026-08-10); a PS2 console port followed Aug 10, 2006, and that PS2 build was then used as the base for an arcade "Ver. B" update (GDL-0039, Dec 23 2006) which added a fifth button and made White Len playable — this set's Version B2 (GDL-0039A) is a further revision of that same Ver. B line. Dreamcast never appears in any Act Cadenza port history; the earlier Act Cadenza Ver. A family (`meltybld` GDL-0028C, `meltyblo` GDL-0028, also QUEUE.md families) are themselves other NAOMI GD-ROM arcade cabinets, not DC releases — no member of the Melty Blood family assessed in this campaign (including `mbaa`, `assessments/mbaa.md` §2) has shipped on retail DC |
| Community ports | None found for `meltyb`/Act Cadenza on Dreamcast (searched 2026-08-10) — no fan/homebrew NAOMI→DC conversion of this title exists, matching the same-family finding for `mbaa` (`assessments/mbaa.md` §2). A Steam community thread about the later *Actress Again Current Code* references an in-fiction "Dreamcast" text string as a joke/easter egg tied to Naomi hardware sharing the DC's architecture, not an actual playable DC build ([Steam Community discussion](https://steamcommunity.com/app/411370/discussions/0/357284131803757255/), accessed 2026-08-10) — noted only to rule it out, it is unrelated to Act Cadenza specifically |
| Representative choice | Newest revision (Version B2, GDL-0039A) of the Act Cadenza GD-ROM family tracked in `GAME_FORMATS.md`; covers clone `meltybo` (Version B, GDL-0039) per the `naomi.cpp` parent link above. The earlier Act Cadenza Ver. A family (`meltybld`/`meltyblo`) is a separate `QUEUE.md` row, still pending |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/meltyb.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`; by t=121 s the run already shows a
live "DEMONSTRATION"-tagged attract battle, and the loop keeps alternating between the title
card and fresh attract battles through t=609 s (the last capture).
Screenshots (5 kept of 10):
- `evidence/meltyb/shot-121s.png` — live attract-demo battle: Tohno Akiha vs. Warachia in a
  red-tinted pillared hall, "MELTY BLOOD Act Cadenza DEMONSTRATION" HUD banner, "PRESS START
  BUTTON" — the frame that sets coverage to `demo`
- `evidence/meltyb/shot-182s.png` — title screen: "MELTY BLOOD Act Cadenza Version B2" over a
  dark textured backdrop, subtitle "Through the Looking-Glass, Northern Light transparently",
  "©TYPE-MOON/ECOLE, 1999-2007", "FREE PLAY" HUD
- `evidence/meltyb/shot-365s.png` — live attract-demo battle: Mech-Hisui vs. Kohaku, a
  15-hit/2040-damage combo mid-flight, "MELTY BLOOD Act Cadenza DEMONSTRATION" HUD banner
- `evidence/meltyb/shot-548s.png` — alternate title-sequence frame: "MELTY BLOOD Act Cadenza"
  logo over a moonlit night sky (no Version B2 label/subtitle on this frame), "PRESS START
  BUTTON" — a different beat of the same attract title sequence as `shot-182s.png`
- `evidence/meltyb/shot-609s.png` — live attract-demo battle: a blonde character (Warakia's
  opponent) in a ruined-building night alley, "MELTY BLOOD Act Cadenza DEMONSTRATION" HUD
  banner — confirms the attract loop is still cycling at the end of the 600 s capture

Anomalies: `shot-060s.png` (t=60 s, dropped from the curated set) is a solid near-black frame —
consistent with a fade transition inside the attract sequence (between the EEPROM handoff at
t=20 s and the first title/demo card), not a stuck/static screen, since the very next capture
at t=121 s already shows a live attract-demo battle. No settings/EEPROM prompt (the
"press Start for defaults" cohort class) was observed in any of the 10 captures, the same
no-prompt pattern `mbaa` showed (`assessments/mbaa.md` §3) — either the EEPROM was already
primed ahead of this capture or this build clears the prompt without an operator Start press
inside the first minute; no operator intervention was needed or recorded for this run.

## 4. Memory fit (axis: 50.9)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 15,439,831 | 16,777,216 | 0.9203 | 91.0 | address peak 33,514,496 (u 1.9976, informational) · `nz_above_cap` 10,855,533 (content bytes found above the cap address, informational) · `dma_high_water` 33,312,544 (informational-only from v6 on) |
| VRAM (FB-masked content + 2×FB) | 9,978,034 (content_total 8,749,234 + 2×fb_bytes 1,228,800) | 8,388,608 | 1.1895 | 50.9 | raw address peak 16,760,448 (u 1.9980) is the extent artifact, not content · `nz_total` 9,672,898 · `nz_above_cap` 5,712,282 |
| ARAM (content volume, fill-excluded, `content_total`) | 2,149,151 | 2,097,152 | 1.0248 | 80.5 | address peak 3,535,472 (u 1.6858, informational) · `nz_above_cap` 943,203 |

Watermarks (informational, content-scan — stale-data prone): main 33,514,496 · vram
16,760,448 · aram 8,388,608 (the aram watermark hits the classic boot-time full-bank fill
value seen elsewhere in the campaign — including `mbaa`, `assessments/mbaa.md` §4 — not
content; `content_total` above is what's scored). Main watermark (33,514,496) tracks
`dma_high_water` (33,312,544) closely (1.0061×) — no divergence flag.

VRAM is the binding region: its sub-score (50.9) equals the memory axis, since
`region_score()`'s `min()` makes regions non-tradeable — main RAM clears 91.0 and ARAM clears
80.5 even though ARAM also sits just past its own 1x line. Across the fighter cohort measured
this campaign, VRAM/ARAM overage keeps recurring as the soft spot, and `meltyb`'s VRAM u
(1.1895) is the mildest of the four VRAM-bound fighters so far: `ggxx`'s VRAM u 1.5314
(sub-score 28.7, `assessments/ggxx.md` §4), `mbaa`'s VRAM u 1.2605 (sub-score 39.6,
`assessments/mbaa.md` §4), `meltyb`'s VRAM u 1.1895 here (sub-score 50.9), and `ggxxac`'s ARAM
u 1.2318 is its binding region instead (sub-score 43.3, VRAM only barely over at u 1.0427,
`assessments/ggxxac.md` §4) — all four Naomi fighters land in the same 1.0–1.6x memory-overage
band on their binding region.

## 5. Cart streaming (axis: 65.3)

DMA events 2,906 · total 168,390,656 B (160.6 MiB) · unique 74,180,608 B (70.7 MiB) · re-read
ratio 0.5595 · steady-state 15.974 MB/min (`short_window: false`) · PIO bootstrap `pio_bytes`
1,574,208 B (1.5 MB, GD-ROM DIMM firmware boot-load into DIMM RAM, handoff `trigger=pio`).
`meltyb` is GD-ROM format, so this PIO block is the DIMM firmware's own bootstrap ahead of
G1-bus DMA streaming, structurally the same path the other GD-ROM fighters use.

Despite being GD-ROM, `meltyb`'s re-read ratio (0.5595) sits far above its own GD-ROM fighter
siblings — `ggxx` 0.2748, `ggxxac` 0.3101, `ggxxsla` 0.2975 (`*.metrics.json` `streaming.reread_ratio`)
— and lands close to the cart title `mbaa`'s 0.5811 (`assessments/mbaa.md` §5) on a similarly
sized unique working set (70.7 MB vs. `mbaa`'s 73.2 MB, vs. 56.8–60.1 MB for the other GD-ROM
fighters). This is a genuine measured anomaly, not a format artifact: a GD-ROM fighter
re-reading roughly twice the fraction of its unique data that its own GD-ROM siblings do is
worth understanding before assuming the fighter cohort's GD-ROM streaming behavior is uniform
(§9).

## 6. Guts (axis: n/a — no .dat)

No `.dat` available — the static-scan carve failed: `entrypoint 0x8c021000 outside carved
image 0xc020000..0xc1a0000` (`guts.error`, `carve_boot.py`'s entrypoint-bounds check;
degrade-to-no-guts per spec §4.3 — a produced-but-odd `.dat` must not crash the battery or
lose the capture). Code bytes / functions / MMIO refs / BIOS vector refs: unavailable (carve
never reached Ghidra). Flags recorded but **unscored** since `guts_axis()` only runs when
`dat_available` is true: `eeprom_bios` (`extra_bios_classes` 0). `sdk_strings` empty — no
SDK-overlap evidence could be extracted, which also drives similarity's `sdk_overlap: none`
and `cart_loader_match: false` in §8 below (`run_battery.py` `similarity()` requires
`guts.get("dat_available")` truthy for `cart_loader_match`, and non-empty `sdk_strings` for any
overlap beyond `none`).

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 2P panel, 8-way joystick + 6 buttons (digital), up to 2 concurrent
players, 2 coin chutes. `controls.device_class = stick`. MAME input ports: `naomi`
(`INPUT_PORTS_START(naomi)` at `naomi.cpp` @59e7c0b line 1506 — the same shared digital-stick +
6-button block `ggxx`/`ggxxac`/`mbaa` cite; `meltyb`'s own `GAME()` row at line 11287 declares
`machine=naomigd`, `input_ports=naomi`).
The game itself uses 5 of those 6 cabinet buttons: A (weak), B (medium), C (strong), D
(Shield), plus a macro/shortcut button ("Q") for canned combined inputs — Melty Blood's
signature parry mechanic on D, same as `mbaa` (`assessments/mbaa.md` §7), plus the extra
shortcut button that Wikipedia records as added starting with the Ver. B arcade update
(Dec 23 2006) this Version B2 revision continues from ([Wikipedia: Melty Blood](https://en.wikipedia.org/wiki/Melty_Blood),
accessed 2026-08-10; button-function detail per community arcade move-list FAQs —
[GameFAQs: Melty Blood Act Cadenza arcade FAQ (Servbot001)](https://gamefaqs.gamespot.com/arcade/921913-melty-blood-act-cadenza/faqs/47975)
and [GameFAQs: Melty Blood Act Cadenza arcade FAQ (kalciane)](https://gamefaqs.gamespot.com/arcade/921913-melty-blood-act-cadenza/faqs/35471),
accessed 2026-08-10 — forum/community sources, lower authority than the MAME/hardware-DB
citations below, cited only for the button-function detail).
Proposed DC mapping: d-pad for the 8-way stick + DC pad's 4 face buttons (A/B/X/Y) for
weak/medium/strong/Shield, plus a shoulder button (L or R) for the macro/shortcut input —
precedented by the official PS2 port's own convention of collapsing macro inputs onto shoulder
buttons (L1=ABC, R1=AD, R2=AB) rather than adding face buttons
([GameFAQs: Melty Blood Act Cadenza PS2 move list (jygting)](https://gamefaqs.gamespot.com/ps2/932171-melty-blood-act-cadenza/faqs/45171),
accessed 2026-08-10 — forum source, cited only for the shoulder-button mapping detail).
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi` (line 1506; `GAME()` row
for `meltyb` at line 11287 declares `machine=naomigd`, `input_ports=naomi`; `meltybo` clone row
at line 11286);
[arcadeitalia MAME machine DB](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=meltyb)
("Joystick 8 ways", "6" buttons, "Up to 2 players (solo, 2 concurrents)", "2" coin slots).

## 8. Score computation

final = memory^.50 · streaming^.25 · controls^.125 · similarity^.125 (guts dropped — no `.dat`
— weights renormalized per spec §4.3, nominal .40/.20/.20/.10/.10 → .50/.25/·/.125/.125)
      = 50.9^.50 · 65.3^.25 · 100.0^.125 · 20.0^.125 = **52.4 (B)**
Similarity inputs: developer match no, SDK overlap **none**, loader match **no** → 20.0.
Developer match is false on its own merits — Ecole Software is not in
`assessments/reference/similarity-reference.json`'s `makers` list (Altron / Taito) —
independent of the carve failure. SDK overlap and loader match, by contrast, are **both**
downstream of the same carve failure (§6): `sdk_overlap` can only be `none` with an empty
`sdk_strings` list, and `cart_loader_match` requires `guts.dat_available` truthy regardless of
format match, so `meltyb` being GD-ROM (matching the reference's GD-ROM format) does not save
it the way it does for `ggxx`/`ggxxac`/`ggxxsla` (similarity 70.0 each) — this pulls `meltyb`
down to `mbaa`'s cart-format similarity band (40.0) and below, at 20.0, purely on the missing
carve, not a title-specific SDK difference.

## 9. Risks & notes

- The carve failure is the single biggest lever on this score: recovering a `.dat` (different
  Ghidra pass, or an addressing fix to `carve_boot.py`'s load-entry handling for this title)
  would both restore the guts axis and very likely lift `cart_loader_match` to true (this is a
  GD-ROM title, format-matching the reference), pushing similarity from 20.0 toward the
  GD-ROM-fighter norm of 70.0 — a substantially higher final score is plausible without any
  change to the game itself. This is a measurement gap, not a porting-difficulty finding.
- VRAM is a real work item: u 1.1895 on FB-masked content needs a texture/asset-store trim to
  clear the 8 MB cap — the mildest overage of the four VRAM-bound fighters measured this
  campaign (`ggxx` u 1.5314, `mbaa` u 1.2605, `ggxxac`'s ARAM u 1.2318), but still binding.
- ARAM sits just past its own cap (u 1.0248, sub-score 80.5) — not binding, but not much
  headroom either; worth re-checking after any VRAM-driven asset rework.
- Main RAM is comfortably under cap (u 0.9203, sub-score 91.0) — the highest main-RAM
  utilization of the fighter cohort measured so far, though still non-binding.
- Streaming's re-read ratio (0.5595) is anomalously high for a GD-ROM title in this cohort —
  roughly double `ggxx`/`ggxxac`/`ggxxsla`'s 0.27–0.31 and close to the cart title `mbaa`'s
  0.5811 (§5) — worth confirming this isn't itself a carve/measurement artifact before taking
  it as a genuine asset-streaming characteristic of this title.
- Main-RAM write-truth includes CPU writes (v6+); `dma_high_water` is informational-only, not
  scored.
- No official or fan DC port exists for any Act Cadenza revision (PS2 got the 2006 console
  port; the Actress Again lineage's later PC/Steam release is a different title, `mbaa`
  §2) — this assessment is first-principles, not reference-checked.
- Rendering must be verified on real DC hardware per working-style rule — this is an
  emulator-only (Flycast) measurement.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-10 | 52.4 B | initial assessment — fighter cohort, fresh v9 capture |
