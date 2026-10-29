#!/usr/bin/env python3
"""Write data/README.md (the dataset card), data/LICENSE and data/provenance.yaml.

uv run python scripts/04_card.py     # needs 01_collect, 02_index and 03_verify first
"""

import json
from pathlib import Path

import cpcir

ROOT = Path(__file__).parents[1]
DATA = ROOT / "data"
GITHUB = f"https://github.com/yuiseki/{cpcir.REPO}"
JANOWIAK = (
    "Janowiak, J. E., R. J. Joyce, and Y. Yarosh, 2001: A Real-Time Global Half-hourly Pixel-Resolution Infrared "
    "Dataset and Its Applications. Bull. Amer. Meteor. Soc., 82(2), 205-217."
)
NWS = (
    "The information on National Weather Service (NWS) Web pages are in the public domain, unless specifically "
    "noted otherwise, and may be used without charge for any lawful purpose so long as you do not: 1) claim it is "
    "your own (e.g., by claiming copyright for NWS information -- see below), 2) use it in a manner that implies an "
    "endorsement or affiliation with NOAA/NWS, or 3) modify its content and then present it as official government "
    "material. You also cannot present information of your own in a way that makes it appear to be official "
    "government information."
)

CARD = """---
license: other
license_name: noaa-nws-public-domain-with-conditions
license_link: LICENSE
language:
- en
tags:
- remote-sensing
- infrared
- brightness-temperature
- geostationary
- clouds
- noaa
- ncep
pretty_name: NCEP/CPC 4 km global merged IR, hourly files of 2026-10-20 to 2026-10-26 (UTC)
viewer: false
---

# NCEP/CPC 4 km global merged IR: one week of hourly files, 2026-10-20 to 2026-10-26 (UTC)

NOAA/CPC が配布する、静止気象衛星の赤外画像を全球(60N から 60S)で合成した 4 km 格子の輝度温度の、
2026-10-20 から 2026-10-26(UTC)までの 1 週間分(1 時間ごとのファイル 168 個、各ファイルに :00 と :30 の 2 枚)です。
配布されたままの圧縮ファイルで、何も変えていません。元のサーバーは新しい時間帯から順に古いものを消す方式なので、
このコピーは凍結した窓です。後から同じものは取れません。

A frozen window of the files `merg_YYYYMMDDHH_4km-pixel.Z` served by the NOAA/NWS Climate Prediction Center
(CPC), acquired on {run_date}. Each file holds two images, the half hours :00 and :30 of its hour. The files are
byte for byte what the provider serves ({size_gb:.2f} GB, {n} files). The upstream server keeps only a rolling window of
recent months (when acquired, {listing_first} to {listing_last}), so this repository is a frozen window and the
same files cannot be fetched again later; the file list and sha256 are in `MANIFEST.json` and `index.tsv`.

## Source

- Provider: NOAA/NWS/NCEP Climate Prediction Center. Data page: <{page}>. Files: <{base}>.
- Format documentation: the CPC README, saved as `docs/cpc_README.txt` (source <{readme}>).
- Anonymous HTTPS only. No login or workaround was used. The NASA GES DISC copy of this product (GPM_MERGIR,
  Earthdata login) was not used.
- The files are served without a version number. The newest Last-Modified in the window is {last_modified}, hence
  {vintage} in the name.

## Contents

| path | what it is |
| --- | --- |
| `data/merg_YYYYMMDDHH_4km-pixel.Z` | the {n} hourly files of the window (compress format, about 26 MB each) |
| `index.tsv` | per file: hour, bytes, sha256, Last-Modified, decoded bytes, decoded sha256 |
| `MANIFEST.json` | per file: URL, size, sha256, the Last-Modified header and the listing time, as fetched |
| `docs/` | the provider's listing, data page, README and the NWS disclaimer as saved; `verify_local.json` |
| `LICENSE`, `provenance.yaml` | the terms and the provenance |

## Data format (from the CPC README, `docs/cpc_README.txt`)

- Decompress with `gzip -dc file.Z` or `uncompress`. The decoded file is {decoded:,} bytes: two records of
  9896 x 3298 unsigned bytes, the first for the image on the hour (:00), the second for the half hour (:30).
- Brightness temperature in kelvin = stored value + 75. The value 255 (330 K after adding 75) is the undefined
  value (UNDEF 330 in the README's GrADS control file).
- Grid: longitude from 0.0182 E eastward in steps of 0.036378335 degrees, latitude from 59.982 N southward in steps
  of 0.036383683 degrees (60 N to 60 S), north to south rows.
- Source: the ~11 micron IR channels of the geostationary satellites, corrected for zenith angle dependence
  (CPC data page).
- Read with numpy: `np.frombuffer(gzip.decompress(open(f, "rb").read()), np.uint8).reshape(2, 3298, 9896)`.

## Terms and acknowledgement

The files carry no licence text. The CPC data page links the NWS disclaimer (saved as `docs/nws_disclaimer.html`),
which says (quoted):

> {nws}

Please do the same: do not claim the data as your own, do not imply an endorsement by NOAA/NWS, and do not present
modified data as official government material. This repository is not endorsed by NOAA/NWS. The data are provided as
published, without warranty, and the timely delivery and accuracy of the NWS server data are not guaranteed.
The maintainer treats the disclaimer's conditions, together with the citation below, as equivalent to CC BY style
attribution; this is the maintainer's reading, not a statement by NOAA. The disclaimer is written for NWS web
pages and servers; it is not a statement made for these files in particular, which is why the card says `license: other`.

Please acknowledge the source as: "NOAA/NWS/NCEP Climate Prediction Center, global merged IR (4 km), https://www.cpc.ncep.noaa.gov",
and cite the reference that the CPC data page gives:

> {janowiak}

Caveat: the CPC README says the data were held back for a few days under data exchange agreements between NOAA and
EUMETSAT (the Meteosat data provider). The files of this window were already published on the CPC server when
they were acquired. This repository does not assess those agreements.

## Verification

`scripts/03_verify.py` re-reads every file: size and sha256 against the manifest, size and Last-Modified against a
new request to the provider, `gzip -dc` against `uncompress -c` (the same bytes), the decoded size of two 9896 x 3298
records, consecutive hours over the whole window, and per record the undefined pixels and the brightness range:
{n} files, brightness {min_k} to {max_k} K where defined, {undef:,} undefined pixels in all, {problems} problems.
The provider publishes no checksums, so the sha256 values are ours.

## Reproduce

Scripts, tests and logs: <{github}>. `scripts/01_collect.py` fetches the window (it works only while the files are
still on the server), `02_index.py` indexes, `03_verify.py` checks, `04_card.py` writes this card.
"""

LICENSE = """Terms for the files of the NCEP/CPC 4 km global merged IR (merg_YYYYMMDDHH_4km-pixel.Z).

The Climate Prediction Center data page (https://www.cpc.ncep.noaa.gov/products/global_precip/html/wpage.full_res.html)
links the NWS disclaimer (https://www.weather.gov/disclaimer), which says, copied on {run_date}:

  {nws}

Reference given on the CPC data page:
  {janowiak}

The files themselves carry no licence text, and the disclaimer is written for NWS web pages and servers. The maintainer
of this repository (yuiseki) treats these conditions, together with the citation, as equivalent to CC BY style
attribution; that is the maintainer's reading, not a statement by NOAA. No endorsement by NOAA/NWS is implied. The data
are provided as published, without warranty.
"""

PROVENANCE = """dataset: {repo}
source:
  provider: NOAA/NWS/NCEP Climate Prediction Center
  data_page: {page}
  files: {base}
  documentation: {readme}
  product: global (60N-60S) merged IR brightness temperature, 4 km, half-hourly records in hourly files
window_utc: [{w0}, {w1}]
acquired_utc: {retrieved}
vintage_month: "{vintage}"
files: {n}
bytes: {size}
checksums: MANIFEST.json (sha256 computed by us; the provider publishes none)
changes: none to the .Z files; index.tsv, docs/ and MANIFEST.json are added
terms: LICENSE (NWS disclaimer conditions; maintainer treats them with the citation as CC BY equivalent attribution)
scripts: {github}
"""


def main() -> int:
    run = sorted((DATA / "raw").glob("*/MANIFEST.json"))[-1].parent
    m = json.loads((run / "MANIFEST.json").read_text())
    ver = json.loads((ROOT / "docs" / "verify_local.json").read_text())
    if ver["problems"]:
        raise SystemExit("the local verification found problems; no card")
    listing = cpcir.parse_listing(
        (DATA / "docs" / "cpc_ftp_listing.html").read_text("utf-8", "replace")
    )
    lm = max(m["files"].values(), key=lambda f: f["listing_modified"])
    kw = {
        "n": len(m["files"]), "run_date": run.name[:4] + "-" + run.name[4:6] + "-" + run.name[6:],
        "size_gb": sum(f["size"] for f in m["files"].values()) / 1e9, "page": cpcir.PAGE_URL,
        "base": cpcir.BASE, "readme": cpcir.README_URL, "github": GITHUB, "vintage": m["vintage_month"],
        "last_modified": lm["listing_modified"], "decoded": cpcir.DECODED_BYTES, "nws": NWS, "janowiak": JANOWIAK,
        "listing_first": min(cpcir.hour_of(r["name"]) for r in listing).strftime("%Y-%m-%d"),
        "listing_last": max(cpcir.hour_of(r["name"]) for r in listing).strftime("%Y-%m-%d"),
        "min_k": ver["min_K_overall"], "max_k": ver["max_K_overall"], "undef": ver["undefined_pixels_total"],
        "problems": len(ver["problems"]), "repo": cpcir.REPO, "retrieved": m["retrieved_utc"],
        "size": sum(f["size"] for f in m["files"].values()), "w0": m["window"][0], "w1": m["window"][1],
    }  # fmt: skip
    (DATA / "README.md").write_text(CARD.format(**kw), encoding="utf-8")
    (DATA / "LICENSE").write_text(LICENSE.format(**kw), encoding="utf-8")
    (DATA / "provenance.yaml").write_text(PROVENANCE.format(**kw), encoding="utf-8")
    print("wrote README.md, LICENSE, provenance.yaml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
