#!/usr/bin/env python3
"""Carve a Naomi .dat's main load image into one Ghidra-loadable blob.
Header layout per ../cleopatra/scripts/parse_header.py (netboot rom.py cross-check):
magic@hdr+0, Japan title@hdr+0x30, main load entries@hdr+0x360, entrypoints@hdr+0x420.
ROM offsets are absolute file offsets; if an entry runs past EOF we retry hdr-relative
(GD .dat images place the header at 0x800000).
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
        if rom + n > len(data) and hdr + rom + n <= len(data):
            rom = hdr + rom                       # hdr-relative fallback
        if rom + n > len(data):
            raise ValueError(f"load entry out of file: rom=0x{rom:x} len=0x{n:x}")
        fixed.append((rom, ram, n))
    base = min(ram for _, ram, _ in fixed)
    top = max(ram + n for _, ram, n in fixed)
    blob = bytearray(top - base)
    for rom, ram, n in fixed:
        blob[ram - base:ram - base + n] = data[rom:rom + n]
    entry, _test_ep = struct.unpack_from("<II", data, hdr + 0x420)
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
