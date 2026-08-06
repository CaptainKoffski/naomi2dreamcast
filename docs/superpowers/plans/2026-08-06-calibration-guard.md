# Calibration Guard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A golden-hash regression guard that carves three known-good sets end-to-end before every battery and refuses to run on any drift.

**Architecture:** New `tools/assess/calibration.py` with a pure `compare()` core, a check mode (default) and a `--bless` regen mode; committed hash table `tools/assess/calibration-goldens.json`; one new step in `run_battery.selftest()`. Spec: `docs/superpowers/specs/2026-08-06-calibration-guard-design.md`.

**Tech Stack:** Python 3 stdlib only (hashlib, subprocess, tempfile). Reuses `carve_boot.carve()`, `tools/dat-extract/cart2dat.py`, `tools/dat-extract/chd2dat.sh`.

## Global Constraints

- **Never commit or persist ROM-derived bytes** — hashes and metadata only; every produced `.dat` is deleted immediately after hashing; carved blobs stay in memory.
- Golden sets: `inunoos` (M2), `ausfache` (M4), `ikaruga` (GD) — one per pipeline flavor.
- Every failure path **refuses loudly** (nonzero exit / `sys.exit`); no degrade-to-warning anywhere.
- Tests are plain-assert `__main__` scripts printing `ALL OK` (repo convention, see `tools/assess/tests/test_metric_guards.py`).
- Batteries run serially; the guard adds ~15 s to battery start (measured 2026-08-06: cart2dat ≈ 1.1 s each, chd2dat ≈ 13 s).
- Expected hashes (observed 2026-08-06, the bless run must reproduce these prefixes): inunoos `.dat` `1ccddea101f9e38e…` boot `cc89bbbaab47fd7e…`; ausfache `.dat` `42bc1292b2e19e42…` boot `cfd8460ec1ba24c7…`; ikaruga `.dat` `d435938becdeb794…` boot `bcab6911ab9f8318…`.
- Local ROMs live under `naomi/` (`NAOMI_DIR` env override, same as `run_battery.py`); producers live in `tools/dat-extract/` and are invoked with `cwd` set there.
- The user's shell wraps `cd` (zoxide) — in Bash tool calls use absolute paths or `cd` only at the start of a command line with an absolute path.

---

### Task 1: `compare()` core + mismatch-path tests

**Files:**
- Create: `tools/assess/calibration.py` (module skeleton + `compare()` only)
- Test: `tools/assess/tests/test_calibration.py`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: `calibration.compare(goldens: dict, results: list[dict]) -> list[str]`. `goldens` is the parsed golden table `{"sets": [entry, …]}`; each entry and each result dict has keys `set` (str), `flavor` (str), `dat_sha256` (str), `boot_sha256` (str), `base` (hex str like `"0x0c020000"`), `entry` (hex str), `size` (int). Returns human-readable failure strings, empty list = clean. Also `calibration.SETS = (("inunoos", "M2"), ("ausfache", "M4"), ("ikaruga", "GD"))`. Task 2 fills in the rest of the module; keep it import-safe (no side effects at import).

- [ ] **Step 1: Write the failing test**

Create `tools/assess/tests/test_calibration.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/assess/tests/test_calibration.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'calibration'`

- [ ] **Step 3: Write the minimal module with `compare()`**

Create `tools/assess/calibration.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tools/assess/tests/test_calibration.py`
Expected: each check line `… OK`, then `ALL OK`

- [ ] **Step 5: Commit**

```bash
cd /Users/captainkoffski/AntigravityProjects/naomi2dreamcast && git add tools/assess/calibration.py tools/assess/tests/test_calibration.py && git commit -m "assess: calibration guard compare() core + mismatch-path tests

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: pipeline runner, check/bless modes, bless the goldens

**Files:**
- Modify: `tools/assess/calibration.py` (append below `compare()`)
- Create (generated by `--bless`, then committed): `tools/assess/calibration-goldens.json`

**Interfaces:**
- Consumes: `compare()`, `SETS`, module constants from Task 1; `carve_boot.carve(data: bytes) -> (bytes, dict)` where the dict has `base`/`entry` as hex strings and `size` as int; producers `python3 cart2dat.py <set> <outdir>` and `./chd2dat.sh <set> <outdir>` (both write `<outdir>/<set>.dat`, exit nonzero on failure, must run with `cwd=DAT_EXTRACT`).
- Produces: `calibration.py` runnable as a script — exit 0 = calibrated, nonzero = refuse (Task 3 wires this into `selftest()`); `calibration-goldens.json` with keys `blessed`, `repo_commit`, `chdman`, `regen`, `sets` (list of the result dicts from Task 1's interface plus a `cmd` string).

- [ ] **Step 1: Append the runner and main to `calibration.py`**

Append below `compare()`:

```python
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
```

- [ ] **Step 2: Re-run the unit test (module must stay import-safe)**

Run: `python3 tools/assess/tests/test_calibration.py`
Expected: `ALL OK`

- [ ] **Step 3: Bless the goldens**

Run: `python3 tools/assess/calibration.py --bless`
Expected: `BLESSED 3 sets -> tools/assess/calibration-goldens.json` in ~15 s.

- [ ] **Step 4: Verify the blessed hashes against the spec's cross-check values**

Run: `python3 -c "import json; [print(s['set'], s['dat_sha256'][:16], s['boot_sha256'][:16], s['base'], s['entry']) for s in json.load(open('tools/assess/calibration-goldens.json'))['sets']]"`
Expected output exactly:
```
inunoos 1ccddea101f9e38e cc89bbbaab47fd7e 0x0c020000 0x0c021000
ausfache 42bc1292b2e19e42 cfd8460ec1ba24c7 0x8c020000 0x8c021000
ikaruga d435938becdeb794 bcab6911ab9f8318 0x8c020000 0x8c021000
```
Any deviation = STOP, the pipeline drifted between brainstorm and implementation; investigate before committing anything.

- [ ] **Step 5: Run check mode end-to-end (clean pass)**

Run: `python3 tools/assess/calibration.py`
Expected: `calibration OK (3 sets)` in ~15 s.

- [ ] **Step 6: Tamper test — check mode must refuse and name the stage**

```bash
python3 - <<'EOF'
import json
p = "tools/assess/calibration-goldens.json"
t = json.load(open(p))
t["sets"][2]["boot_sha256"] = "0" * 64
json.dump(t, open(p, "w"), indent=2)
EOF
python3 tools/assess/calibration.py; echo "exit=$?"
git -C /Users/captainkoffski/AntigravityProjects/naomi2dreamcast checkout -- tools/assess/calibration-goldens.json 2>/dev/null || git checkout -- tools/assess/calibration-goldens.json
```
Expected: `CALIBRATION GUARD FAILED` mentioning `ikaruga` and `CARVE stage`, `exit=1`. (The `git checkout` restore only works after the JSON is committed — on this first pass, re-run `--bless` instead and re-verify Step 4.)

- [ ] **Step 7: Verify no decrypted artifacts persist**

Run: `ls /tmp/calibration-* /var/folders/*/*/T/calibration-* 2>/dev/null; ls tools/dat-extract/out/*.dat 2>/dev/null; echo clean`
Expected: only `clean` (temp dirs removed, no stray `.dat`).

- [ ] **Step 8: Commit**

```bash
cd /Users/captainkoffski/AntigravityProjects/naomi2dreamcast && git add tools/assess/calibration.py tools/assess/calibration-goldens.json && git commit -m "assess: calibration guard — bless golden hashes (inunoos/ausfache/ikaruga)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: wire the guard into `run_battery.selftest()`

**Files:**
- Modify: `tools/assess/run_battery.py:188-198` (the `selftest()` function)

**Interfaces:**
- Consumes: `calibration.py` as a script (Task 2): exit 0 = calibrated, nonzero = drift/refusal with the reason on stdout/stderr.
- Produces: a battery that cannot start with a drifted pipeline.

- [ ] **Step 1: Add the guard step to `selftest()`**

In `tools/assess/run_battery.py`, `selftest()` currently ends with the test loop. Append a third step so the function reads:

```python
def selftest():
    # Strict prohibition (REQUIREMENTS.md: BIOS noise must never be scored as game
    # usage; kb §7): the battery refuses to run at all unless the metric
    # invariants hold. Never bypass this to "just get a run" — a red test means
    # the measurements would be untrustworthy.
    for t in ("test_score.py", "test_metric_guards.py"):
        r = subprocess.run([sys.executable, os.path.join(HERE, "tests", t)],
                           capture_output=True, text=True)
        if r.returncode != 0 or "ALL OK" not in r.stdout:
            sys.exit(f"SELF-TEST FAILED ({t}) — battery refuses to run:\n"
                     f"{r.stdout}{r.stderr}")
    # Same posture for the carve pipeline: golden-hash calibration (kb §10)
    # catches silent producer/carve drift the per-title guards can't see.
    # ~15 s (chd2dat dominates) against a 10+ minute battery.
    r = subprocess.run([sys.executable, os.path.join(HERE, "calibration.py")],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("SELF-TEST FAILED (calibration guard) — battery refuses to run:\n"
                 f"{r.stdout}{r.stderr}")
```

- [ ] **Step 2: Verify selftest passes clean**

Run: `cd /Users/captainkoffski/AntigravityProjects/naomi2dreamcast/tools/assess && python3 -c "import run_battery; run_battery.selftest(); print('SELFTEST PASSED')"`
Expected: `SELFTEST PASSED` (takes ~20 s: two test scripts + the 15 s guard).

- [ ] **Step 3: Verify selftest refuses on tampered goldens**

```bash
cd /Users/captainkoffski/AntigravityProjects/naomi2dreamcast && python3 - <<'EOF'
import json
p = "tools/assess/calibration-goldens.json"
t = json.load(open(p))
t["sets"][0]["dat_sha256"] = "0" * 64
json.dump(t, open(p, "w"), indent=2)
EOF
cd tools/assess && python3 -c "import run_battery; run_battery.selftest()" ; echo "exit=$?"
cd /Users/captainkoffski/AntigravityProjects/naomi2dreamcast && git checkout -- tools/assess/calibration-goldens.json
```
Expected: `SELF-TEST FAILED (calibration guard)` with `inunoos … PRODUCER stage` in the output, `exit=1`, then a clean restore (`git status` shows the JSON unmodified).

- [ ] **Step 4: Commit**

```bash
cd /Users/captainkoffski/AntigravityProjects/naomi2dreamcast && git add tools/assess/run_battery.py && git commit -m "assess: selftest runs the calibration guard before every battery

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: docs — stale comment, kb §10, brief status

**Files:**
- Modify: `tools/assess/carve_boot.py:46-48` (comment only, no code change)
- Modify: `docs/kb/assessment-tooling.md` (append §10 after §9)
- Modify: `docs/superpowers/specs/backlog-calibration-guard.md:3-5` (status line)

**Interfaces:**
- Consumes: everything shipped in Tasks 1-3 (docs describe it).
- Produces: nothing consumed by code.

- [ ] **Step 1: Replace the stale "planned Task 9" comment in `carve_boot.py`**

The comment at lines 46-48 currently reads:

```python
        # GD-ROM .dat entries may use small hdr-relative offsets; try hdr-relative for small values.
        # hdr-relative rom that is accidentally in-bounds under absolute read is undetectable here;
        # calibration byte-compares against known-good boot.bin (planned Task 9) is the real guard.
```

Replace the third line so it reads:

```python
        # GD-ROM .dat entries may use small hdr-relative offsets; try hdr-relative for small values.
        # hdr-relative rom that is accidentally in-bounds under absolute read is undetectable here;
        # calibration.py's golden-hash guard (runs in selftest; kb §10) is the pipeline-level backstop.
```

- [ ] **Step 2: Sanity-run carve tests (comment-only change, but prove it)**

Run: `python3 tools/assess/tests/test_carve_boot.py`
Expected: `ALL OK` (or the file's existing pass output — no behavior change).

- [ ] **Step 3: Append kb §10**

Append to `docs/kb/assessment-tooling.md` (after the end of §9):

```markdown
## 10. Calibration guard (2026-08-06): golden-hash backstop for silent carve drift

The bit-30 mask (32e99e3) plus carve_boot's two cheap guards (illegal flag
bits, entrypoint-in-range, 22d765f) leave one undetectable window: garbage
within the legal bits that lands in-file carves plausible-but-wrong bytes.
Per-title that is unfixable at carve time — the backstop is pipeline-level:
`tools/assess/calibration.py` carves three golden sets end-to-end
(cart2dat/chd2dat → carve_boot) and compares sha256 + carve meta against the
committed `tools/assess/calibration-goldens.json`.

- Goldens: inunoos (M2), ausfache (M4), ikaruga (GD) — one per producer
  flavor; ikaruga doubles as a `DC_SHIPPED_ANCHOR` control. Full pass ~15 s
  (chd2dat ≈ 13 s dominates; measured 2026-08-06).
- Runs unconditionally in `run_battery.selftest()`: any mismatch refuses the
  battery — the §7/§8 refuse-to-score posture, applied to the carve pipeline.
  Environment drift (chdman upgrade, recompiled extract_dat) is covered
  precisely because the check runs every battery, not only on repo changes.
- Failure output names the stage: `.dat` sha256 drift = producer
  (cart2dat/m4dec/chd2dat); boot-hash or base/entry/size drift = carver.
- Only hashes and carve metadata are committed — never ROM-derived bytes.
- Regen after an INTENTIONAL pipeline change:
  `python3 tools/assess/calibration.py --bless`, then review the JSON diff
  (every changed hash must be explained by the change) and commit.
- Design + decisions: `docs/superpowers/specs/2026-08-06-calibration-guard-design.md`.
```

- [ ] **Step 4: Flip the brief's status line**

In `docs/superpowers/specs/backlog-calibration-guard.md`, replace lines 3-5:

```markdown
**Status:** not started. Written 2026-08-06 as the session brief for a future
session — start that session with:
`Implement the calibration guard per docs/superpowers/specs/backlog-calibration-guard.md`
```

with:

```markdown
**Status:** implemented 2026-08-06 — see
`2026-08-06-calibration-guard-design.md` (design) and kb §10 (regen
procedure). Kept as the motivating brief.
```

- [ ] **Step 5: Commit**

```bash
cd /Users/captainkoffski/AntigravityProjects/naomi2dreamcast && git add tools/assess/carve_boot.py docs/kb/assessment-tooling.md docs/superpowers/specs/backlog-calibration-guard.md && git commit -m "kb: §10 calibration guard; carve_boot comment + backlog brief status

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```
