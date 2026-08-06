#!/usr/bin/env python3
"""Carve-pipeline calibration guard (kb §10). Carves the three golden sets
end-to-end (cart2dat/chd2dat -> carve_boot) and compares sha256 + carve meta
against the committed golden table. Hashes only, NEVER ROM-derived bytes.
Any drift refuses loudly — a drifted pipeline must never write a verdict.
Usage: calibration.py            check against calibration-goldens.json (selftest runs this)
       calibration.py --bless    regenerate the table after an INTENTIONAL change,
                                 then review the diff and commit.
Design: docs/superpowers/specs/2026-08-06-calibration-guard-design.md"""
import glob, hashlib, json, os, shutil, struct, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import carve_boot  # noqa: E402

NAOMI = os.environ.get("NAOMI_DIR", os.path.join(REPO, "naomi"))
DAT_EXTRACT = os.path.join(REPO, "tools", "dat-extract")
GOLDENS_PATH = os.path.join(HERE, "calibration-goldens.json")
# One golden per pipeline flavor (design decision 2026-08-06); ikaruga doubles
# as a DC_SHIPPED_ANCHOR control.
SETS = (("inunoos", "M2"), ("ausfache", "M4"), ("ikaruga", "GD"))
META_KEYS = ("boot_sha256", "base", "entry", "size")


def compare(goldens, results):
    """Pure comparison core (unit-tested without ROMs). Returns failure strings."""
    failures = []
    gold = {g["set"]: g for g in goldens["sets"]}
    seen = set()
    for r in results:
        seen.add(r["set"])
        g = gold.get(r["set"])
        if g is None:
            failures.append(f"{r['set']}: no golden entry — re-bless required")
            continue
        if r["dat_sha256"] != g["dat_sha256"]:
            # Carve output of a drifted .dat is meaningless — report the producer
            # stage only, don't bury it under derived carve mismatches.
            failures.append(f"{r['set']}: .dat sha256 drift (PRODUCER stage — "
                            f"cart2dat/m4dec/chd2dat): expected {g['dat_sha256']} "
                            f"got {r['dat_sha256']}")
            continue
        for k in META_KEYS:
            if r[k] != g[k]:
                failures.append(f"{r['set']}: {k} drift (CARVE stage): "
                                f"expected {g[k]} got {r[k]}")
    for s in gold:
        if s not in seen:
            failures.append(f"{s}: golden set not checked")
    return failures


def rom_path(setname, flavor):
    """Path of the local ROM artifact the producer needs, or None if absent."""
    if flavor == "GD":
        hits = glob.glob(os.path.join(NAOMI, setname, "*.chd"))
        return hits[0] if hits else None
    z = os.path.join(NAOMI, setname + ".zip")
    return z if os.path.isfile(z) else None


def produce(setname, flavor, outdir):
    """Run the .dat producer + carve; return the hash/meta result dict.
    The decrypted .dat is deleted before this returns; the carved blob is
    hashed in memory and never written."""
    cmd = (["./chd2dat.sh", setname, outdir] if flavor == "GD"
           else ["python3", "cart2dat.py", setname, outdir])
    r = subprocess.run(cmd, cwd=DAT_EXTRACT, capture_output=True, text=True)
    dat = os.path.join(outdir, setname + ".dat")
    if r.returncode != 0 or not os.path.isfile(dat):
        raise RuntimeError(f"{setname}: producer failed:\n"
                           f"{(r.stdout + r.stderr)[-2000:]}")
    with open(dat, "rb") as fh:
        data = fh.read()
    os.remove(dat)                       # decrypted dump never persists
    blob, meta = carve_boot.carve(data)
    return {"set": setname, "flavor": flavor, "cmd": " ".join(cmd[:2]),
            "dat_sha256": hashlib.sha256(data).hexdigest(),
            "boot_sha256": hashlib.sha256(blob).hexdigest(),
            "base": meta["base"], "entry": meta["entry"], "size": meta["size"]}


def _line(cmd):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True).stdout
        return out.splitlines()[0].strip() if out.strip() else "unknown"
    except OSError:
        return "unknown"


def main():
    bless = "--bless" in sys.argv
    missing = [s for s, f in SETS if rom_path(s, f) is None]
    if missing:
        sys.exit("CALIBRATION GUARD: golden ROM(s) missing under "
                 f"{NAOMI}: {', '.join(missing)} — cannot establish pipeline "
                 "health, refusing (this machine is the designated runner).")
    if not bless and not os.path.isfile(GOLDENS_PATH):
        sys.exit(f"CALIBRATION GUARD: no golden table at {GOLDENS_PATH} — "
                 "run calibration.py --bless, review, commit.")
    tmp = tempfile.mkdtemp(prefix="calibration-")
    try:
        results = [produce(s, f, tmp) for s, f in SETS]
    except (RuntimeError, ValueError, struct.error, OSError) as e:
        # carve_boot.carve raises ValueError; struct.error on a short file.
        sys.exit(f"CALIBRATION GUARD: pipeline run failed — {e}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if bless:
        table = {"blessed": time.strftime("%Y-%m-%d"),
                 "repo_commit": _line(["git", "-C", REPO, "rev-parse", "--short", "HEAD"]),
                 "chdman": _line(["chdman", "--version"]),
                 "regen": "python3 tools/assess/calibration.py --bless   "
                          "# then review the diff (every changed hash must be "
                          "explained by your change) and commit",
                 "sets": results}
        with open(GOLDENS_PATH, "w") as fh:
            json.dump(table, fh, indent=2)
        print(f"BLESSED {len(results)} sets -> {os.path.relpath(GOLDENS_PATH, REPO)}")
        return
    with open(GOLDENS_PATH) as fh:
        goldens = json.load(fh)
    failures = compare(goldens, results)
    if failures:
        sys.exit("CALIBRATION GUARD FAILED — carve-pipeline drift, a drifted "
                 "pipeline must never write a verdict:\n  "
                 + "\n  ".join(failures)
                 + "\nIf this change is INTENTIONAL: python3 tools/assess/"
                   "calibration.py --bless, review the diff, commit (kb §10).")
    print(f"calibration OK ({len(results)} sets)")


if __name__ == "__main__":
    main()
