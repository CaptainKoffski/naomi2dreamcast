# Alien Front (Rev T) (`alienfnt`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 7,763,615 B → utilization **3.702** — second-highest of the parked ARAM cohort, just under `vonot`'s 3.746 max. Same-game precedent for the gate (kb §6 item 1): **the game received an official Dreamcast port — *Alien Front Online* (Wow Entertainment/Sega, NA 2001-08-07) — that shipped inside the DC's 2 MiB ARAM** while *adding* online play and real-time voice chat. Unlike `vonot`/`ausfache`, ARAM is not the sole over-budget region: main content u ≈ 1.221 and VRAM content+2×fb u ≈ 1.224 both exceed 1× (low score band, no gate). Controls on-ladder: `pad_adaptable` — the arcade cab is wheel + pedals, but the official DC port shipped pad-native. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `alienfnt` (covers clone `alienfnta` Rev A — MAME src/mame/sega/naomi.cpp @59e7c0b `GAME()` lines 10991–10992, both `/* 0048 */`) |
| Maker / year | Sega (developer: Wow Entertainment), 2001 (MAME `GAME()` row; [Wikipedia](https://en.wikipedia.org/wiki/Alien_Front_Online): arcade NA January 2001, JP September 2001) |
| Genre / format | Tank-vs-alien 3D action shooter, **cart**, 45.9 MB (`GAME_FORMATS.md`) |
| Official DC port | **Partial — retooled, not a straight port.** *Alien Front Online* (Dreamcast, NA-only 2001-08-07, Sega/Wow Entertainment): same game rebuilt online-centric — 4v4 online battles with real-time voice chat via the bundled DC Microphone, the first console game with online voice chat ([Wikipedia](https://en.wikipedia.org/wiki/Alien_Front_Online), [Dreamcast Live](https://dreamcastlive.net/alien-front-online/); `GAME_FORMATS.md` note already records the "retooled" nuance) |
| Community ports | Not needed — an official DC version exists; no community DC port of the arcade revision found (searched 2026-08-11) |
| Representative choice | Parent set (Rev T, latest revision); clone `alienfnta` is Rev A of the same cart |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/alienfnt.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). The first ~3 min post-handoff sit on a static **optical-link slave-sync countdown**
("Optical Link card found! … Type: Slave, State: NLCB_ILM_INIT … sec TO TIMEOUT" — `shot-060s.png`,
143 s remaining; `shot-182s.png`, 22 s remaining), i.e. the linked-cabinet handshake timing out with no
second machine — so attract began at t ≈ 204 s and ran ~400 s: `shot-243s.png` story screen ("THE
INVADERS HAVE LANDED…"), `shot-304s.png` alien-POV attract segment with FREE PLAY overlay,
`shot-365s.png` live tank gameplay demo (操作説明 tutorial), `shot-487s.png` "BATTLE ON-LINE!" demo
combat. The park is unambiguously the game running its attract cycle, not tooling.
Screenshots: `evidence/alienfnt/shot-060s.png` · `shot-243s.png` · `shot-304s.png` · `shot-365s.png` ·
`shot-487s.png`
Anomalies: none operationally — the link-sync countdown consumed ~34% of the capture but demo coverage
is ample. The cab's online nature is visible everywhere: `guts.sdk_strings` is full of modem/PPP/
NaomiNetwork CGI strings (`/cgi-bin/Server2/NaomiNetwork/CGI/RankingSys/ranking.cgi`, "No modem has
been detected", PPP negotiation) and `serial_pokes` = 38,405. `shot-121s.png`, `shot-182s.png`,
`shot-426s.png`, `shot-548s.png`, `shot-609s.png` curated out (duplicate link-countdown ×2 / duplicate
story ×2 / duplicate tutorial).

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 7,763,615 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.702** — past `region_score()`'s `u > 2.0` gate and **second-highest of the
parked ARAM cohort**: `toyfight` 2.035, `tduno2` 2.615, `takoron` 2.997, `inunoos` 3.206,
`ninjaslt` 3.341, `pokasuka` 3.368, `mazan` 3.483, `mok` 3.558, `ringout` 3.684, `sstrkfgt`
3.687, `alienfnt` **3.702**, `vonot` 3.746 (max). `nz_above_cap` = 5,773,699 B (address-keyed
placement figure, informational). Address peak 8,257,552 B (u 3.938, pre-volume-keying read).

The other two regions, quoted from the sidecar (ARAM gates first in `score.py`'s region walk
regardless) — **both also exceed 1× here**, unlike the sole-blocker profiles (`vonot`,
`ausfache`):

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 20,487,795 | 16,777,216 | **1.221** | `nz_total` — over the 1× cap, under the 2× gate (would score ≈45); `nz_above_cap` (address-placement) 7,252,180 B · `dma_high_water` 28,729,344 B (u 1.712) · watermark 29,818,496 B (u 1.777) |
| VRAM (content volume + 2×fb) | 10,268,627 | 8,388,608 | **1.224** | `content_total` 9,039,827 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2) — over the 1× cap, under the gate (would score ≈45); raw `nz_total` 9,550,996 (u 1.139) · address peak 15,295,427 (u 1.823) |
| ARAM (content volume) | 7,763,615 | 2,097,152 | **3.702** | the gate — see above |

Streaming context: 29,665 DMA events · 83,482,656 B total · 31,429,472 B unique · re-read ratio
0.6235 · steady-state 9.12 MB/min (`short_window: false`) · `pio_bytes` 4,446,062 B.
Guts: carve 1,966,080 B (`carve_meta.title = "ALIEN FRONT"`) · 2,722 functions · MMIO refs
rtc 0 / g2ext 77 / scif 20 · flags `eeprom_bios`/`serial`.
Similarity: `developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: false`.

**Controls (on-ladder, does not gate — `pad_adaptable`):** the arcade cabinet is a sit-down
driving-style cab — **steering wheel + two pedals**, with turret buttons — not a twin-lever tank
rig. Primary source: Flycast carries a dedicated descriptor `alienfnt_inputs`
(core/hw/naomi/naomi_roms_input.h:115): analog `WHEEL` (Full) + `RIGHT PEDAL`/`LEFT PEDAL` (Half),
buttons `LEFT SHOT` / `RIGHT SHOT` / `ROTATION L` / `ROTATION R`. MAME assigns the generic `naomi`
input port set (`GAME( 2001, alienfnt, naomi, naomim2, naomi, … )`, src/mame/sega/naomi.cpp
@59e7c0b line 10991). Corroboration: [Wikipedia](https://en.wikipedia.org/wiki/Alien_Front_Online)
records designer Makoto Uchida chose wheel-and-pedal controls for the cab, and that the DC port
used the standard controller. The pad adaptation is *proven, not proposed*: **the official DC
port shipped pad-native** ([Wikipedia](https://en.wikipedia.org/wiki/Alien_Front_Online),
[Dreamcast Live](https://dreamcastlive.net/alien-front-online/)). `controls.device_class =
pad_adaptable` — on-ladder, so controls do not gate and would not gate G2 if ARAM cleared.
Proposed DC mapping: the shipped 2001 one — analog stick steer, triggers for pedals, face
buttons for shots/turret.
Sources (full parity in sidecar `controls.sources`): MAME naomi.cpp GAME() row · Flycast
`alienfnt_inputs` · [Wikipedia](https://en.wikipedia.org/wiki/Alien_Front_Online) ·
[Dreamcast Live](https://dreamcastlive.net/alien-front-online/).

**What would unblock it — same-game precedent for kb §6 item 1:** the G3-ARAM softening argument
gets another *same-title* data point here, alongside `vonot`: Sega shipped an official Dreamcast
version of this very game — ***Alien Front Online*, NA 2001-08-07 — running inside the DC's real
2 MiB AICA RAM**, and it did so while *adding* the most audio-hungry feature imaginable for the
era: real-time online voice chat through the bundled DC Microphone
([Wikipedia](https://en.wikipedia.org/wiki/Alien_Front_Online),
[Dreamcast Live](https://dreamcastlive.net/alien-front-online/)). A released product proves the
3.7× sound trim for this game is achievable. Two honest nuances: (1) *Alien Front Online* is a
**retooled online-centric version**, not a byte-for-byte port of this arcade build
(`GAME_FORMATS.md` note) — the precedent proves the sound budget, not a straight conversion;
(2) unlike `vonot` (main 0.809 / VRAM 0.740 both fit), `alienfnt`'s main (1.221) and VRAM (1.224)
also exceed capacity, so under any softer ARAM rule (kb §6 item 1's candidate fixes) it unparks
into the **low score band (memory axis ≈ 45)**, not into a comfortable fit — a real port would
still need the main/VRAM trims the official DC version evidently made. Unpark priority therefore
sits behind the sole-blocker candidates (`ausfache`, `radirgyn`, `vonot`).

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM u 3.702 second-highest in cohort; main 1.221/VRAM 1.224 also over 1× (no gate); same-game official DC port *Alien Front Online* (NA 2001) is the kb §6 item-1 precedent; controls pad_adaptable (wheel+pedal cab, pad-native DC port) |
