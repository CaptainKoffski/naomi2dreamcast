#!/usr/bin/env python3
"""Carve a Naomi .dat's main load image into one Ghidra-loadable blob.
Header layout per ../cleopatra/scripts/parse_header.py (netboot rom.py cross-check):
magic@hdr+0, Japan title@hdr+0x30, main load entries@hdr+0x360, entrypoints@hdr+0x420.
ROM offsets are absolute file offsets; if an entry runs past EOF we retry hdr-relative
(GD .dat images place the header at 0x800000).
Cart images decode load-entry offsets with the M4 mask (bit 30 = encrypted-read flag, naomim4.cpp:124-125 / m4cartridge.cpp:115,132).
Usage: carve_boot.py <dat> <outstem>   -> <outstem>.boot.bin + <outstem>.meta.json"""
import json, struct, sys


def _entries(data, hdr):
    out = []
    for i in range(8):
        rom, ram, n = struct.unpack_from("<III", data, hdr + 0x360 + 12 * i)
        if rom == 0xFFFFFFFF or (rom == 0 and n == 0):
            break
        out.append((rom, ram, n))
    return out


def carve(data):
    hdr = 0 if data[0:5] == b"NAOMI" else 0x800000
    if data[hdr:hdr + 5] != b"NAOMI":
        raise ValueError("no NAOMI header at 0 or 0x800000")
    title = data[hdr + 0x30:hdr + 0x50].decode("ascii", "replace").rstrip("\x00 ")
    entries = _entries(data, hdr)
    if not entries:
        raise ValueError("no main load entries")
    fixed = []
    for rom, ram, n in entries:
        if hdr == 0:
            # Bits 31/29 are never legitimate (29-bit address + bit-30 flag is
            # the whole legal space) — a set bit there is a corrupt/misdecrypted
            # table, not data the mask below may silently swallow.
            if rom & 0xa0000000:
                raise ValueError(f"load entry has illegal flag bits: rom=0x{rom:x}")
            # Cart images: bit 30 of a load-entry rom offset is the M4
            # encrypted-read flag, and cart addressing is 29-bit — apply the
            # hardware decode. MAME naomim4.cpp:124-125 @59e7c0b
            # (rom_cur_address = address & 0x1ffffffe; encryption =
            # rom_offset & 0x40000000), Flycast m4cartridge.cpp:115,132
            # @ebae3b513. cart2dat's m4dec already wrote plaintext, so the
            # masked value is a plain file offset.
            rom &= 0x1ffffffe
        # GD-ROM .dat entries may use small hdr-relative offsets; try hdr-relative for small values.
        # hdr-relative rom that is accidentally in-bounds under absolute read is undetectable here;
        # calibration.py's golden-hash guard (runs in selftest; kb §10) is the pipeline-level backstop.
        if hdr > 0 and rom < 0x100000:
            rom = hdr + rom                       # Small rom values are hdr-relative
        if rom + n > len(data):
            raise ValueError(f"load entry out of file: rom=0x{rom:x} len=0x{n:x}")
        fixed.append((rom, ram, n))
    base = min(ram for _, ram, _ in fixed)
    top = max(ram + n for _, ram, n in fixed)
    blob = bytearray(top - base)
    for rom, ram, n in fixed:
        blob[ram - base:ram - base + n] = data[rom:rom + n]
    entry, _test_ep = struct.unpack_from("<II", data, hdr + 0x420)
    # A mis-carve that survives the offset checks almost always leaves the
    # entrypoint outside the carved image — make that loud, not a Ghidra mystery.
    if not base <= entry < top:
        raise ValueError(f"entrypoint 0x{entry:x} outside carved image "
                         f"0x{base:x}..0x{top:x}")
    meta = {"base": f"0x{base:08x}", "entry": f"0x{entry:08x}", "size": len(blob),
            "entries": [[r, m, n] for r, m, n in fixed], "hdr_at": hdr, "title": title}
    return bytes(blob), meta


if __name__ == "__main__":
    dat, stem = sys.argv[1], sys.argv[2]
    with open(dat, "rb") as fh:
        blob, meta = carve(fh.read())
    with open(stem + ".boot.bin", "wb") as fh:
        fh.write(blob)
    with open(stem + ".meta.json", "w") as fh:
        json.dump(meta, fh, indent=2)
    print(f"OK {meta['title']} base={meta['base']} entry={meta['entry']} size=0x{meta['size']:x}")
