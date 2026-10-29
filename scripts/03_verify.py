#!/usr/bin/env python3
"""Check the downloaded files with two decompressors, the manifest and the provider.

    uv run python scripts/03_verify.py     # writes docs/verify_local.json, exits 1 on any difference

Per file: size and sha256 against the manifest; the size and Last-Modified of a new HEAD against the
frozen values; gzip -dc against uncompress -c (ncompress) must give the same bytes; the decoded size must be
two records of 9896 x 3298; the hours must be consecutive over the window; per record the undefined pixels and
the brightness range (plausible K) are counted, and the :00 and :30 records must differ.
"""

import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path

import cpcir

ROOT = Path(__file__).parents[1]


def head(url: str) -> tuple[int, str | None]:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": cpcir.UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return int(r.headers["Content-Length"]), r.headers.get("Last-Modified")


def main() -> int:
    run = sorted((ROOT / "data" / "raw").glob("*/MANIFEST.json"))[-1].parent
    manifest = json.loads((run / "MANIFEST.json").read_text())
    expected = cpcir.window_names(cpcir.WINDOW_START, cpcir.WINDOW_END)
    problems = []
    if list(manifest["files"]) != expected:
        problems.append("the manifest is not the full consecutive window")
    idx = {
        ln.split("\t")[0]: ln.split("\t")
        for ln in (ROOT / "data" / "index.tsv").read_text().splitlines()[1:]
    }
    per_file, undef, lo, hi = {}, 0, 10_000, 0
    for name, m in manifest["files"].items():
        p = run / name
        if p.stat().st_size != m["size"] or cpcir.sha256(p) != m["sha256"]:
            problems.append(f"{name}: size or sha256 differs from the manifest")
        size, lm = head(m["url"])
        if size != m["size"] or lm != m["last_modified_header"]:
            problems.append(f"{name}: the provider now says {size} bytes, {lm}")
        a = subprocess.run(["gzip", "-dc", str(p)], capture_output=True, check=True).stdout
        b = subprocess.run(["uncompress", "-c", str(p)], capture_output=True, check=True).stdout
        if a != b:
            problems.append(f"{name}: gzip and uncompress decode differently")
        try:
            st = cpcir.decode_stats(a)
        except ValueError as e:
            problems.append(f"{name}: {e}")
            continue
        if not st["records_differ"]:
            problems.append(f"{name}: the :00 and :30 records are identical")
        if idx[name][6] != hashlib.sha256(a).hexdigest() or int(idx[name][5]) != len(a):
            problems.append(f"{name}: index.tsv differs from the decoded bytes")
        for r in st["records"]:
            undef += r["undefined_pixels"]
            lo, hi = min(lo, r["min_K"]), max(hi, r["max_K"])
            if r["min_K"] < 150 or r["max_K"] > 340:
                problems.append(f"{name}: brightness range {r['min_K']} to {r['max_K']} K")
        per_file[name] = st
    res = {
        "files": len(manifest["files"]), "problems": problems, "undefined_pixels_total": undef,
        "min_K_overall": lo, "max_K_overall": hi, "per_file": per_file,
    }  # fmt: skip
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "verify_local.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "per_file"}, indent=1))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
