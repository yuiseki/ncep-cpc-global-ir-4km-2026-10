#!/usr/bin/env python3
"""Fetch the frozen window (cpcir.WINDOW_START to WINDOW_END, hourly) of the CPC 4 km global merged IR.

    uv run python scripts/01_collect.py          # resumable; writes data/raw/<run>/MANIFEST.json

The upstream keeps a rolling window of recent months, so what is frozen here cannot be fetched again
later: the file list, sizes and sha256 are in the manifest. Polite fetch: two connections per file, one
file at a time, two seconds between files. No checksums are published by CPC; the sha256 is ours.
"""

import json
import subprocess
import time
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

import cpcir

ROOT = Path(__file__).parents[1]


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": cpcir.UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def head(url: str) -> dict:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": cpcir.UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return dict(r.headers)


def main() -> int:
    run = datetime.now(UTC).strftime("%Y%m%d")
    out = ROOT / "data" / "raw" / run
    out.mkdir(parents=True, exist_ok=True)
    docs = ROOT / "data" / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    saved = {
        "cpc_ftp_listing.html": cpcir.BASE, "cpc_full_res_ir_page.html": cpcir.PAGE_URL,
        "cpc_README.txt": cpcir.README_URL, "nws_disclaimer.html": cpcir.DISCLAIMER_URL,
    }  # fmt: skip
    for name, url in saved.items():
        (docs / name).write_bytes(get(url))
    rows = cpcir.parse_listing((docs / "cpc_ftp_listing.html").read_text("utf-8", "replace"))
    by_name = {r["name"]: r for r in rows}
    want = cpcir.window_names(cpcir.WINDOW_START, cpcir.WINDOW_END)
    absent = [n for n in want if n not in by_name]
    if absent:
        raise SystemExit(
            f"{len(absent)} files of the window are no longer on the server, first {absent[0]}"
        )
    files = {}
    for i, name in enumerate(want):
        url = cpcir.BASE + name
        h = head(url)
        size = int(h["Content-Length"])
        dest = out / name
        if not dest.exists() or dest.stat().st_size != size:
            subprocess.run(
                ["aria2c", "-q", "-x2", "-s2", "-c", "--user-agent", cpcir.UA, "-d", str(out), "-o", name, url],
                check=True,
            )  # fmt: skip
            time.sleep(2)
        if dest.stat().st_size != size:
            raise SystemExit(f"{name}: {dest.stat().st_size} bytes, the server said {size}")
        files[name] = {
            "url": url, "size": size, "sha256": cpcir.sha256(dest),
            "last_modified_header": h.get("Last-Modified"),
            "listing_modified": by_name[name]["modified"].isoformat(sep=" "),
        }  # fmt: skip
        print(f"{i + 1}/{len(want)} {name} {size:,}", flush=True)
    window_rows = [by_name[n] for n in want]
    manifest = {
        "source": cpcir.BASE, "page": cpcir.PAGE_URL, "retrieved_utc": datetime.now(UTC).isoformat(),
        "window": [cpcir.WINDOW_START.isoformat(), cpcir.WINDOW_END.isoformat()],
        "docs_sha256": {n: cpcir.sha256(docs / n) for n in saved},
        "vintage_month": cpcir.vintage_month(window_rows), "files": files,
    }  # fmt: skip
    (out / "MANIFEST.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    print(
        f"done: {len(files)} files, {sum(f['size'] for f in files.values()):,} bytes, vintage {manifest['vintage_month']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
