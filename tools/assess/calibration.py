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
