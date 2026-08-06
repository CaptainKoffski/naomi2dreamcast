#!/usr/bin/env python3
"""compare() invariants for the calibration guard (kb §10): a drifted pipeline
must be reported per set with the drifted STAGE named — .dat drift is the
producer (cart2dat/m4dec/chd2dat), boot/meta drift is the carver. Never weaken
these to make a battery start: a red guard means verdicts would be untrustworthy."""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import calibration

GOLD = {"sets": [{"set": "a", "flavor": "M2", "dat_sha256": "d1", "boot_sha256": "b1",
                  "base": "0x0c020000", "entry": "0x0c021000", "size": 100}]}


def res(**kw):
    d = {"set": "a", "flavor": "M2", "dat_sha256": "d1", "boot_sha256": "b1",
         "base": "0x0c020000", "entry": "0x0c021000", "size": 100}
    d.update(kw)
    return d


checks = []


def check(name):
    def deco(fn):
        checks.append((name, fn))
        return fn
    return deco


@check("clean pass returns no failures")
def _():
    assert calibration.compare(GOLD, [res()]) == []


@check("dat hash drift names the PRODUCER stage")
def _():
    f = calibration.compare(GOLD, [res(dat_sha256="XX")])
    assert len(f) == 1 and "a" in f[0] and "PRODUCER" in f[0], f


@check("dat drift suppresses carve-stage noise for that set")
def _():
    f = calibration.compare(GOLD, [res(dat_sha256="XX", boot_sha256="YY")])
    assert len(f) == 1 and "PRODUCER" in f[0], f


@check("boot hash drift names the CARVE stage")
def _():
    f = calibration.compare(GOLD, [res(boot_sha256="XX")])
    assert len(f) == 1 and "CARVE" in f[0], f


@check("meta drift (size) names the CARVE stage")
def _():
    f = calibration.compare(GOLD, [res(size=999)])
    assert len(f) == 1 and "CARVE" in f[0] and "size" in f[0], f


@check("golden set with no result is reported")
def _():
    f = calibration.compare(GOLD, [])
    assert len(f) == 1 and "not checked" in f[0], f


@check("result with no golden entry is reported")
def _():
    f = calibration.compare(GOLD, [res(), res(set="b")])
    assert any("no golden entry" in x for x in f), f


if __name__ == "__main__":
    for name, fn in checks:
        fn()
        print(name, "OK")
    print("ALL OK")
