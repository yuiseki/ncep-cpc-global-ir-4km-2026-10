---
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
(CPC), acquired on 2026-10-29. Each file holds two images, the half hours :00 and :30 of its hour. The files are
byte for byte what the provider serves (4.55 GB, 168 files). The upstream server keeps only a rolling window of
recent months (when acquired, 2026-03-30 to 2026-10-27), so this repository is a frozen window and the
same files cannot be fetched again later; the file list and sha256 are in `MANIFEST.json` and `index.tsv`.

## Source

- Provider: NOAA/NWS/NCEP Climate Prediction Center. Data page: <https://www.cpc.ncep.noaa.gov/products/global_precip/html/wpage.full_res.html>. Files: <https://ftp.cpc.ncep.noaa.gov/precip/global_full_res_IR/>.
- Format documentation: the CPC README, saved as `docs/cpc_README.txt` (source <https://www.cpc.ncep.noaa.gov/products/global_precip/html/README>).
- Anonymous HTTPS only. No login or workaround was used. The NASA GES DISC copy of this product (GPM_MERGIR,
  Earthdata login) was not used.
- The files are served without a version number. The newest Last-Modified in the window is 2026-10-28 00:06:00, hence
  2026-10 in the name.

## Contents

| path | what it is |
| --- | --- |
| `data/merg_YYYYMMDDHH_4km-pixel.Z` | the 168 hourly files of the window (compress format, about 26 MB each) |
| `index.tsv` | per file: hour, bytes, sha256, Last-Modified, decoded bytes, decoded sha256 |
| `MANIFEST.json` | per file: URL, size, sha256, the Last-Modified header and the listing time, as fetched |
| `docs/` | the provider's listing, data page, README and the NWS disclaimer as saved; `verify_local.json` |
| `LICENSE`, `provenance.yaml` | the terms and the provenance |

## Data format (from the CPC README, `docs/cpc_README.txt`)

- Decompress with `gzip -dc file.Z` or `uncompress`. The decoded file is 65,274,016 bytes: two records of
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

> The information on National Weather Service (NWS) Web pages are in the public domain, unless specifically noted otherwise, and may be used without charge for any lawful purpose so long as you do not: 1) claim it is your own (e.g., by claiming copyright for NWS information -- see below), 2) use it in a manner that implies an endorsement or affiliation with NOAA/NWS, or 3) modify its content and then present it as official government material. You also cannot present information of your own in a way that makes it appear to be official government information.

Please do the same: do not claim the data as your own, do not imply an endorsement by NOAA/NWS, and do not present
modified data as official government material. This repository is not endorsed by NOAA/NWS. The data are provided as
published, without warranty, and the timely delivery and accuracy of the NWS server data are not guaranteed.
The maintainer treats the disclaimer's conditions, together with the citation below, as equivalent to CC BY style
attribution; this is the maintainer's reading, not a statement by NOAA. The disclaimer is written for NWS web
pages and servers; it is not a statement made for these files in particular, which is why the card says `license: other`.

Please acknowledge the source as: "NOAA/NWS/NCEP Climate Prediction Center, global merged IR (4 km), https://www.cpc.ncep.noaa.gov",
and cite the reference that the CPC data page gives:

> Janowiak, J. E., R. J. Joyce, and Y. Yarosh, 2001: A Real-Time Global Half-hourly Pixel-Resolution Infrared Dataset and Its Applications. Bull. Amer. Meteor. Soc., 82(2), 205-217.

Caveat: the CPC README says the data were held back for a few days under data exchange agreements between NOAA and
EUMETSAT (the Meteosat data provider). The files of this window were already published on the CPC server when
they were acquired. This repository does not assess those agreements.

## Verification

`scripts/03_verify.py` re-reads every file: size and sha256 against the manifest, size and Last-Modified against a
new request to the provider, `gzip -dc` against `uncompress -c` (the same bytes), the decoded size of two 9896 x 3298
records, consecutive hours over the whole window, and per record the undefined pixels and the brightness range:
168 files, brightness 168 to 329 K where defined, 232,116,042 undefined pixels in all, 0 problems.
The provider publishes no checksums, so the sha256 values are ours.

## Reproduce

Scripts, tests and logs: <https://github.com/yuiseki/ncep-cpc-global-ir-4km-2026-10>. `scripts/01_collect.py` fetches the window (it works only while the files are
still on the server), `02_index.py` indexes, `03_verify.py` checks, `04_card.py` writes this card.
