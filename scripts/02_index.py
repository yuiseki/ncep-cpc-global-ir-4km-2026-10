#!/usr/bin/env python3
"""Write a small index of the downloaded files: hour, bytes, sha256, Last-Modified, decoded size and checksum.

    uv run python scripts/02_index.py     # writes data/index.tsv

The .Z files are published as they are (compress format). The index is read from them with gzip -dc.
"""

import hashlib
import json
import subprocess
from pathlib import Path

import cpcir

ROOT = Path(__file__).parents[1]
COLUMNS = [
    "file",
    "hour_utc",
    "bytes",
    "sha256",
    "last_modified",
    "decoded_bytes",
    "decoded_sha256",
]


def main() -> int:
    run = sorted((ROOT / "data" / "raw").glob("*/MANIFEST.json"))[-1].parent
    manifest = json.loads((run / "MANIFEST.json").read_text())
    lines = ["\t".join(COLUMNS)]
    for name, m in manifest["files"].items():
        raw = subprocess.run(
            ["gzip", "-dc", str(run / name)], capture_output=True, check=True
        ).stdout
        row = [name, cpcir.hour_of(name).isoformat(sep=" "), m["size"], m["sha256"],
               m["last_modified_header"], len(raw), hashlib.sha256(raw).hexdigest()]  # fmt: skip
        lines.append("\t".join(str(x) for x in row))
    (ROOT / "data" / "index.tsv").write_text("\n".join(lines) + "\n")
    print(f"{len(lines) - 1} files indexed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
