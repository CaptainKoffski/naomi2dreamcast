# dat-extract — produce a Naomi `.dat` for a game

A `.dat` is the flat, decrypted Naomi image (`NAOMI` header at offset 0 or 0x800000)
that **Ghidra** loads for static analysis and that a port build consumes. This dir
converts a groomed romset (`../../naomi/<set>`) into that `.dat`.

Instrumented **Flycast runs the romset (`.chd`/`.zip`) directly** — it does NOT need the
`.dat`. Only the Ghidra/static step needs it. See `../../docs/producing-the-dat.md` for
the full format-by-format explanation.

## Which tool (dispatch rule)

Look at the set's folder `../../naomi/<set>`:

| The set has… | It is | Command |
|---|---|---|
| a `.chd` (in `<set>/` or a parent set's folder) | **GD-ROM** | `./chd2dat.sh <set>` |
| only a `.zip`, no `.chd` | **cartridge** (M1/M2/M4) | `python3 cart2dat.py <set>` |

You do NOT need to know the cart encryption type — `cart2dat.py` auto-detects M1/M2/M4,
auto-selects the security PIC, decrypts M4 via `m4dec`, and matches blobs by filename or CRC.
`chd2dat.sh` auto-selects the PIC and handles netpic discs.

Output: `out/<set>.dat`. Both tools print one `OK …` line on success (with the parsed
game title) or a diagnostic and non-zero exit on failure.

## Prerequisites (macOS, already installed this project)

- `chdman` (GD-ROM only): `brew install rom-tools`  (v0.289 used)
- `7zz`: `/opt/homebrew/bin/7zz` (Homebrew `p7zip`)
- `clang` (auto-builds `extract_dat` / `m4dec` on first run)
- Flycast's `naomi_roms.cpp` for cart blob tables — path in `cart2dat.py` `ROMS` (override
  with env `NAOMI_ROMS=`).

## Success & validation

- Success = an `OK` line and `out/<set>.dat` whose first bytes are `NAOMI`.
- Byte-exact proof exists only for GD-ROM (reproduces the known-good Cleopatra `.dat`,
  SHA1 `08c2666b…`). Carts have no reference dump, so validate by:
  `python3 ../../../cleopatra/scripts/parse_header.py out/<set>.dat`  (expect NAOMI magic,
  real title, sane load entries) and, for a candidate you'll port, a real **Flycast boot**.

## Coverage & the sets that WON'T convert

All GD-ROM (standard + netpic) and 72/74 carts convert. Skip these — they error by design:

| Set | Why | If Ghidra is ever needed |
|---|---|---|
| `hotd2` (M2) | early cart, header itself is 315-5881-encrypted | Flycast runtime RAM dump |
| `mushik2e` (M4) | ambiguous Flycast entry + library zip is an unclear revision | Flycast runtime RAM dump |
| WCCF `cdv-*` sets | not Naomi games — networked-system/update discs | n/a (no game image) |

## Notes for a batch/agent loop

- Deterministic: a `.dat` is fully regenerable from the romset, so deleting it loses nothing.
- Ghidra only needs the boot region (~1–3 MB, per the header load entries) — you can keep that
  slice and delete the full `.dat` (75–480 MB).
- Full one-shot conversion of the whole library is ~24–25 GB; convert per game on demand instead.
- `out/` and the built binaries are gitignored (copyrighted / derived).
