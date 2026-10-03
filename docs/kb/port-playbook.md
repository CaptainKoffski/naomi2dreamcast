# Port playbook — Naomi/Atomiswave → Dreamcast

The reusable *method* for a static binary conversion, distilled from the
*Cleopatra Fortune Plus* port (cfp2dreamcast, local checkout `cleopatra/`)
and the *Senko no Ronde Special* port (senkosp2dreamcast). Each port's own
`docs/kb/` is the chronological, game-specific *record*; this file is the
ordered, reusable method, maintained here in the umbrella repo (moved from
cfp2dreamcast 2026-10-03). Port repos are sibling checkouts; paths below
are written `cfp/docs/kb/...` and `senkosp/docs/kb/...`.

Deeper references, cited throughout: `cfp/docs/kb/atomiswave-method.md`
(technique catalog), `cfp/docs/kb/naomi-vs-dreamcast.md` (hardware deltas),
each port's `tooling.md` (install recipes) and `boot-binary.md` (RE
findings). The hardware checklist every finished port is tested against:
`GENERAL_CHECKLIST.md` at this repo's root.

## Definition of done — what every port ships (standing, 2026-10-03)

Four requirements that are part of the deliverable, not polish. Each has a
shipped, hardware-verified implementation in senkosp2dreamcast to copy.

### 1. Three boot paths, all PASS on the release candidate

| Destination | Role | Fed by |
|---|---|---|
| **Flycast** (DC profile) | dev tool — never the verdict | `build/disc.gdi` |
| **Real console from a GDEMU-class ODE** | primary target | release zip via GDMENUCardManager |
| **Real console over the serial port via DreamShell** (isoldr serial-SD) | required path for testers without an ODE | GDI + the `DS/` per-game preset shipped in the release zip |

Both VGA and composite, per `GENERAL_CHECKLIST.md`. DreamShell is the path
that reshapes the design, so decide it in phase 4, not after release:

- **isoldr virtualizes the GD at the BIOS-syscall layer only.** A raw-ATA
  cart stream can never be served by it — senkosp's phase-6 control test
  died exactly there (`RAW-ATA READ FAIL`, `senkosp/docs/kb/phase6-release.md`
  §DreamShell). The fix that shipped: a **dual-backend GD driver** — raw
  ATA on real-BIOS boots, GD syscalls under isoldr, picked by a raw-first
  probe in the loader (`senkosp/docs/superpowers/specs/2026-09-03-phase7-t1-dreamshell-design.md`,
  `senkosp/docs/kb/phase7-polishing.md` §T1, `senkosp/shims/src/gd_sys.c`).
- **isoldr needs resident RAM you must carve.** Low RAM is unsound: the
  Naomi kernel slice's RTOS keeps a live TCB table at `0x8c004000`, and bare
  isoldr defaults (`memory = 0x8c004000`) reboot the console at the first
  3D scene. senkosp carves 64 KB off the top of the game's relocated heap
  (`memory = 0x8cff0000`, `heap = 0x8cff7a00`, pinned — never
  `HEAP_MODE_AUTO`) and ships that preset so testers touch nothing
  (`senkosp/scripts/make_preset.py` → `DS/` tree in the release zip).
- **Serial-debug TX corrupts SD reads mid-boot** under DreamShell
  (`cfp/docs/kb/00-status.md` §DreamShell serial-SD boot, round 1) —
  release builds compile the serial path out. DreamShell's own sound driver
  is still running at handoff (same section) — audit what you inherit.
- Expect serial-speed loads (~150 KB/s). It is a boot path, not a
  performance target.

### 2. Two disc formats: GDI and CDI

`make release` emits both `[GDI] <game>.zip` and `[CDI] <game>.zip`
(`senkosp/Makefile`; recipe and installs in `senkosp/docs/kb/tooling.md`
§CDI mastering; mastering script `senkosp/scripts/make_cdi.py`).

- **Generic GDI→CDI converters cannot work** on these ports: the shim
  streams the cart from a baked absolute FAD, and the cart is raw sectors
  past the filesystem, not a file. Master the CDI fresh.
- **Layout that works: audio/data MIL-CD** — session 1 a silent audio track
  (cdi4dc generates it), session 2 one mode-2 data track at LBA 11702
  (`mkisofs -C 0,11702`), a fixed 1792-sector boot region, cart at FAD
  13644. cdi4dc's data/data mode is beta: it booted in Flycast and died on
  GDEMU.
- **1ST_READ.BIN must be scrambled on CD media** — the BIOS descramble is
  keyed to media type, not layout (control-tested A/B legs in
  `senkosp/captures/cdi/`). The raw cart region stays plain.
- **The donor GD-ROM IP.BIN kills every real CD boot** (license → black →
  reboot, 100% on GDEMU; Flycast's drive model lets it through). Generate
  a CD-native IP.BIN per master with mkdcdisc, branded like the GDI's.
  Found by a hello-payload A/B bisect on hardware — the definitive
  emulator≠hardware case: **Flycast PASS ≠ GDEMU PASS ≠ burned-disc PASS**
  for CDI variants.
- **The CD FAD is a compile-line knob invisible to make.** Bracket
  `make cdi` with objclean and keep a FAD attestation marker in the shim so
  a stale object can't splice into the wrong image.
- *Gate:* GDI boots on GDEMU; CDI boots on GDEMU **and** from a burned CD-R
  on a stock console — the CDI's true target (senkosp's CD-R verdict is
  still owed; GDEMU leg PASS 2026-09-26).

### 3. Buttons-based games: pad AND arcade stick, both first-class

If the game reads buttons (CFP, senkosp — anything on a standard Naomi
panel), it must be fully playable from a standard DC pad **and** from an
HKT-7300-class arcade stick, every gameplay function reachable on both.
senkosp's first shipped mapping put OverDrive on the triggers only; a stick
has no triggers, so stick players had no OverDrive at all — an EVO player
caught it (`senkosp/CONTROLS_TASK.MD`). The shape that shipped
(`senkosp/docs/superpowers/specs/2026-09-27-controls-layouts-design.md`,
`senkosp/docs/kb/input-map.md` §Three-layout controls; hardware PASS
2026-09-30):

- **Classify the device per port, per poll, from the latched DEVINFO
  capability word**: no analog triggers and no analog stick ⇒ arcade stick;
  anything else ⇒ pad. Capability bits, not product-name strings. Re-probe
  after a dead stretch so hot-plug and mid-session swaps follow the device.
- **Sticks always get the cabinet layout** — not a setting, the buttons are
  already in arcade positions. **Pads get presets selectable per port** on
  the menu's Controls page, never "who sits where".
- **Never put a gameplay function only on L/R or an analog axis.** And gate
  axis reads on the capability word: a device without an axis fills that
  byte with a filler of its choosing (Ascii Stick: `0x80`), which read as
  "stuck held" until fixed (`senkosp/docs/kb/input-map.md` §Non-standard
  controllers).
- **One source of truth for layouts** (`senkosp/scripts/menu_def.py`)
  generating both the shim's button→JVS tables and the Controls page.
- *Gate:* hardware matrix on a real TV — pad default, alternate preset,
  stick, mixed ports, mid-session hot-swap, empty-port hot-plug.

### 4. The game's arcade settings reachable from a pre-game menu

The Naomi test-mode GAME ASSIGNMENTS (difficulty, round time, points per
match, modes…) must be settable from the port's own menu, the way senkosp
does it: a loader-side menu at every boot — START GAME (pre-selected) /
SETTINGS / CONTROLS — that writes the chosen bytes into the EEPROM game
record before handoff. Zero game-side code: the shim already serves the
EEPROM from a RAM copy (`senkosp/docs/kb/phase7-polishing.md` §T9; spec
`senkosp/docs/superpowers/specs/2026-09-11-phase7-t9-pregame-menu-design.md`).
Recipe:

1. **Recon the byte map** in stock Naomi-profile Flycast: flip one test-menu
   item per save-quit cycle and diff the `.eeprom`
   (`senkosp/scripts/eeprom_game_diff.py`). Every item → one record byte;
   record labels, values, and defaults (senkosp §T9 RECON table).
2. **Naomi CRC + game-area builder**, host-tested against BIOS-written
   vectors (`senkosp/loader/naomi_crc.c`).
3. **Menu definition as single source of truth** (`scripts/menu_def.py`)
   → generated sprite sheet + layout header; no runtime font, label words
   baked offline.
4. **Poke the record pre-handoff** with a CRC self-check and a pristine
   fallback on mismatch.
5. **A `MENU=0` build knob** for unattended emulator legs — a menu waits
   for input forever and never reaches attract on its own.

Stateless (defaults every power-on); VMU persistence is deferred and the
VMU-untouched tripwire still applies. *Gate:* each item verified to change
in-game behavior on hardware.

## The method — do it in this order

Each phase produces something the next one spends, and has a go/no-go gate.
Don't start a phase until the previous gate is green.

1. **Foundation.** Repo, KB skeleton, toolchain installed and *recorded*
   (`tooling.md`), and a plain unmodified boot verified in-emulator.
   *Gate:* the untouched game runs in the emulator's arcade profile.
2. **Instrumented analysis.** Build an instrumented emulator (see
   `tooling.md` → Flycast source build) and capture ground truth: the
   cart-streaming map, RAM/serial measurements, the input map. Measure before
   you reverse — dynamic truth beats static guessing.
   *Gate:* you know how the game streams data and reads inputs, from real
   traces, not inference.
3. **Reverse engineering.** Ghidra headless + interpreter-mode dynamic
   analysis. Find the touchpoints: entry chain, cart-read fn, input fn,
   EEPROM fn, and the SP/BIOS verdicts (`boot-binary.md`).
   *Gate:* every hardware touchpoint has an exact address and a patch plan.
4. **Conversion.** Loader + freestanding shim + patch table → a bootable GDI.
   Patch the arcade touchpoints to DC equivalents (see next section). Design
   in the dual-backend GD driver, the pad/stick input layer, and the
   pre-game settings menu now (Definition of done §1, §3, §4) — bolting them
   on later cost senkosp a phase.
   *Gate:* boots in the emulator's *Dreamcast* profile, attract runs,
   playable from the menu.
5. **Hardware test & fit.** Run on real hardware via a GDEMU-class ODE and
   via DreamShell serial-SD, on VGA and composite. This is where the
   emulator's lies surface (see gotchas). Budget real debugging rounds here —
   it is not a formality.
   *Gate:* boots and plays on real hardware on every path in Definition of
   done §1, controls matrix §3 PASS.
6. **Safety tripwires, then release.** An arcade game has no VMU concept, so
   the port must never write one (worst case: corrupting a user's saves).
   Run all three before packaging: `make test` (static maple-literal baseline
   scan over every executable surface — full cart, BIOS slices, loader
   objects), `make test-vmu` (unattended emulator canary run: seeded VMU
   images must survive byte-identical, an all-zero control file must get
   auto-formatted, proving the harness is wired), and a `make test-vmu-play`
   session covering settings, 2P, game over, and high-score screens. Method
   + baselines: `cfp/docs/superpowers/specs/2026-07-26-vmu-safety-design.md`,
   `cfp/scripts/test_maple_literals.py`, `cfp/scripts/test_vmu_untouched.sh` —
   reusable for the next port (start from an empty baseline, classify every
   hit). Then `make release`: GDI zip + CDI zip + DreamShell preset
   (Definition of done §2).
   *Gate:* all three tripwires PASS on the release candidate; both images
   boot on hardware.

## Core mechanism

Patch the Naomi/AW-specific touchpoints in the game binary and boot it from a
GDI via a custom loader:

- **Cart reads → GD-ROM loads.** Mirror the cart DMA registers to a
  shim-owned block; the streaming trigger becomes a shim call. No need to
  decode the game's DMA-descriptor struct — the parameters are the values the
  game was about to poke into the registers. Behind the call, two backends:
  raw ATA (+ G1 DMA) on real-BIOS boots, GD syscalls under DreamShell.
- **JVS input → controllers.** Map the game's input read to maple/controller:
  pad presets and a fixed cabinet layout for sticks, device-classified per
  poll (Definition of done §3).
- **EEPROM/coin logic → shims.** Return the game's own "nothing changed"
  native path; bake free-play into the image; let the pre-game menu write the
  GAME ASSIGNMENTS record before handoff (Definition of done §4).

Project-level decisions that generalize:

- **Real hardware is the goal; the emulator is a dev tool, not the target.**
- **A trap-based generic "arcade runtime" does not work** — the Naomi cart
  registers and the DC GD-ROM ATA registers share hardware addresses, so a
  trap cannot tell them apart on real hardware. Patch specific touchpoints.

## Gotchas — the traps that actually cost us

The highest-value transferable content. Each of these burned real time.

- **The emulator masks real hardware.** Emulator-green is not a boot. Benign
  reads and HLE boot paths hide real-HW spins (a settings write-back spun
  forever on G1 drive status on a real DC; the emulator's reads were benign)
  and skip init ladders the real machine runs (the MIE reset/firmware-upload
  ladder never executes under HLE boot). Flycast's drive model also boots a
  CD image whose IP.BIN a real console rejects (Definition of done §2).
  **Verify on the target.**
- **Control-test with a known-good disc.** When stuck on "does it boot at
  all," run a proven-bootable disc (for us, Dolphin Blue) through the *same*
  pipeline and ODE before theorizing about your own artifact. It isolates
  "your bytes" from "the process" in one step. For CDI, the control is a
  hello-payload image through your own mastering chain.
- **macOS AppleDouble sidecars poison disc/data folders.** `._*` files (e.g.
  `._disc.gdi`) made GDEMU pick up junk and refuse to boot. Run `dot_clean`,
  or master on Linux. This one masqueraded as a deep boot bug for a while.
- **Boot binary placement matters.** The boot binary must live in the last
  data track. Max-clone a proven-bootable donor's low tracks + structure
  verbatim and keep *your* delta to a single track — it minimizes the surface
  that can be wrong.
- **IP.BIN / bootstrap traps.** `makeip` hardcoded CD-ROM device-info and a
  CD-R bootstrap; use a donor IP.BIN for the GDI — and a mkdcdisc-generated
  one for the CDI, where the donor's is the thing that fails.
- **Sector size is 2048, not 2352.** Don't guess 2352; it cost a round.
- **Unpatched register literals hide in vendor-BIOS thunks.** The stall we
  chased longest was hardware-register literals (`0x5f7xxx`) reached
  *indirectly* through Naomi BIOS library calls, not in the game's own code.
  Grep every touchpoint address across the whole image, including code reached
  through BIOS thunks.
- **Build on-screen observability early.** With no debugger on real hardware,
  the breakthrough tool was an on-screen shim HUD: breadcrumb blocks,
  heartbeats, a PC sampler painting the stalled main-thread address, and hex
  dumps of live descriptor lists read off the TV. Invest in this before you
  need it, not after five blind boots.

## What mattered vs. red herrings

For a **"does it boot at all"** problem, exhaust the structural and
disc-mastering explanations *first* — a control test is one command — before
deep-diving the game binary. Our costly red herrings lived in the binary (the
2352 sector guess, the uncached-descriptor-walk "fix" that was correct but not
the bug); the real blockers were structural (disc mastering, the AppleDouble
sidecars, the donor IP.BIN on CD media) and one deep (the BIOS EEPROM
bit-bang). The debugging model itself was wrong more than once — hold
hypotheses loosely and let the HUD, not the theory, decide.

## Working cadence

The backbone that kept this from flailing was the superpowers loop, run **per
phase**: `brainstorming` → spec, `writing-plans` → plan, then
`executing-plans` / `subagent-driven-development`. Every phase in both ports
has a spec and a plan under `docs/superpowers/`. Two more that earned their
keep: `systematic-debugging` for the on-hardware bug hunts, and
`verification-before-completion` before any "it boots / it works" claim —
which is the same discipline as gotcha #1.

Followed for both ports. Not automated — a port skill that mandates this was
considered and deferred (see the reuse spec).

## Pointers

- Technique catalog & what transfers to Naomi: `cfp/docs/kb/atomiswave-method.md`
- Hardware deltas: `cfp/docs/kb/naomi-vs-dreamcast.md`
- Can a game damage the ODE / real GD-ROM drive? `cfp/docs/kb/drive-safety.md`
- Toolchain install recipes: `cfp/docs/kb/tooling.md`, `senkosp/docs/kb/tooling.md`
  (incl. §CDI mastering, §Decoupling from ../cleopatra)
- Each port's narrative index: `cfp/docs/kb/00-status.md`, `senkosp/docs/kb/00-status.md`
- Hardware checklist for finished ports: `GENERAL_CHECKLIST.md` (this repo)
- Deferred tooling handoff (kit repo, instrumented-Flycast fork) and the full
  reuse plan: `cfp/docs/superpowers/specs/2026-07-26-experience-reuse-design.md`
