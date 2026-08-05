#!/usr/bin/env python3
"""Verify Sega SOSB sound-bank structure in a live ARAM dump.

Usage: parse_osb.py <aram-dump>   (dump via FLYCAST_ARAMDUMP=<path>, fork >= 4b59eceff)

Layout, established empirically against an azumanga dump (2026-08-04) — see
assessments/azumanga.md "ARAM bank-structure verification":
  SOSB bank:  'SOSB' u32 version  u32 size  u32 tone_count
              u32 tone_off[tone_count]          <- relative to bank start
  tone rec:   'SOSP' u16 ?  u32 sample_off      <- relative to bank start
              ... 0x40 bytes, ends 'ENDP'
Verdict criteria per bank: tone offsets strictly increasing, all < size,
each landing on 'SOSP'; sample offsets all < size, first sample_off == end
of tone-record area; bank ends 'ENDB' at declared size; sample bytes
non-uniform. Note: raw .p16 BGM is headerless and sits between banks —
magic-scan cannot find it. Dumps are copyrighted game data: never commit.
"""
import struct, sys

data = open(sys.argv[1], "rb").read()
u32 = lambda o: struct.unpack_from("<I", data, o)[0]
u16 = lambda o: struct.unpack_from("<H", data, o)[0]


def uniform(buf):
    return len(set(buf[i:i+16] for i in range(0, len(buf) - 16, 16))) <= 1


pos, banks = 0, []
while True:
    pos = data.find(b"SOSB", pos)
    if pos < 0:
        break
    ver, size, count = u32(pos + 4), u32(pos + 8), u32(pos + 12)
    # driver code embeds the magics as literals; a real bank has sane fields
    if ver == 2 and 0x20 < size < len(data) and 0 < count < 1024:
        banks.append((pos, size, count))
    pos += 4

total_sample_bytes = 0
for base, size, count in banks:
    offs = [u32(base + 0x10 + 4 * i) for i in range(count)]
    mono = all(b > a for a, b in zip(offs, offs[1:]))
    inside = all(o < size for o in offs)
    magics_ok = all(data[base + o: base + o + 4] == b"SOSP" for o in offs)
    rec_end = offs[-1] + 0x40  # records are 0x40 bytes each
    samples = [u32(base + o + 6) for o in offs]
    s_inside = all(0 < s < size for s in samples)
    first_adjacent = samples[0] == rec_end
    ends_endb = data[base + size - 4: base + size] == b"ENDB"
    # sample regions: sort offsets (storage order != tone order), region i
    # runs to the next-higher offset
    bounds = sorted(set(samples)) + [size]
    nonuni = sum(1 for i in range(len(bounds) - 1)
                 if not uniform(data[base + bounds[i]: base + bounds[i + 1]]))
    total_sample_bytes += size - samples[0]
    print(f"bank @ {base:#08x}  size={size:#x} ({size/1024:.0f} KiB)  tones={count}")
    print(f"  tone table: monotonic={mono} in-bank={inside} all-SOSP={magics_ok}")
    print(f"  sample offs: in-bank={s_inside} "
          f"first==rec_end={first_adjacent} (rec_end={rec_end:#x}, s0={samples[0]:#x})")
    print(f"  bank ends with ENDB: {ends_endb}  "
          f"non-uniform sample regions: {nonuni}/{len(bounds) - 1}")

covered = sum(s for _, s, _ in banks)
print(f"\n{len(banks)} real SOSB banks, {covered:,} bytes total "
      f"({covered/1048576:.2f} MiB), sample payload {total_sample_bytes:,} bytes")
