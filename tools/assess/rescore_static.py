#!/usr/bin/env python3
"""rescore_static.py <set> [<set> ...]

Re-run the static scan (cart2dat assemble+decrypt -> carve -> Ghidra guts)
for an already-captured family and re-score its sidecar in place. Capture
provenance (versions/assessed/params/boot/capture/memory/streaming/
serial_pokes/controls) is left untouched; guts, similarity, gate and scores
are recomputed. Written for the kb §4.q M4 cohort (ausfache/radirgyn/
mamonoro/illvelo) after the carve_boot bit-30 fix: guts is static-only, so
no 600 s capture re-run is needed. If the scan still fails, the sidecar is
left byte-identical (keeps the historical error string)."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run_battery, score  # noqa: E402


def rescore(setname):
    path = os.path.join(run_battery.ASSESS, setname + ".metrics.json")
    with open(path) as fh:
        sc = json.load(fh)
    guts = run_battery.static_scan(setname, False)
    if not guts.get("dat_available"):
        sys.exit(f"{setname}: static scan still failing, sidecar untouched: "
                 f"{guts.get('error')}")
    flags, extra = run_battery.guts_flags(setname, guts, sc["serial_pokes"])
    # same field shape run_battery.main() writes (sidecar guts block)
    sc["guts"] = {**{k: v for k, v in guts.items() if k != "sdk_strings"},
                  "flags": flags, "extra_bios_classes": extra,
                  "sdk_strings": guts.get("sdk_strings", [])}
    sc["similarity"] = run_battery.similarity({"maker": sc["maker"]},
                                              sc["format"], guts)
    score.score_sidecar(sc)
    with open(path, "w") as fh:
        json.dump(sc, fh, indent=2)
    v = (f"PARKED {sc['gate']}" if sc["gate"]
         else f"{sc['scores']['final']} {sc['scores']['tier']} "
              f"(guts {sc['scores']['guts']})")
    print(f"{setname}: {v}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__.splitlines()[0])
    for s in sys.argv[1:]:
        rescore(s)
