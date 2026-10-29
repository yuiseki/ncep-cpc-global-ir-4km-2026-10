"""Constants and helpers shared by the scripts of ncep-cpc-global-ir-4km-2026-10."""

import hashlib
import re
from datetime import datetime, timedelta
from pathlib import Path

BASE = "https://ftp.cpc.ncep.noaa.gov/precip/global_full_res_IR/"
README_URL = "https://www.cpc.ncep.noaa.gov/products/global_precip/html/README"
PAGE_URL = "https://www.cpc.ncep.noaa.gov/products/global_precip/html/wpage.full_res.html"
DISCLAIMER_URL = "https://www.weather.gov/disclaimer"
UA = "Mozilla/5.0 (research; yuiseki)"
REPO = "ncep-cpc-global-ir-4km-2026-10"
WINDOW_START = datetime(2026, 10, 20, 0)
WINDOW_END = datetime(2026, 10, 26, 23)
NX, NY, RECORDS = (
    9896,
    3298,
    2,
)  # each file: the :00 and the :30 image, 1 byte per pixel, value + 75 = K
DECODED_BYTES = RECORDS * NX * NY
_ROW = re.compile(
    r'<a href="(merg_\d{10}_4km-pixel\.Z)">[^<]*</a>(?:</td>\s*<td[^>]*>)?\s*'
    r"(\d{2}-[A-Za-z]{3}-\d{4} \d{2}:\d{2})\s*(?:</td>\s*<td[^>]*>)?\s*(\S+?)\s*(?:<|$)"
)


def parse_listing(html: str) -> list[dict]:
    return [
        {"name": n, "modified": datetime.strptime(m, "%d-%b-%Y %H:%M"), "size_printed": s}
        for n, m, s in _ROW.findall(html)
    ]


def hour_of(name: str) -> datetime:
    return datetime.strptime(name[5:15], "%Y%m%d%H")


def window_names(start: datetime, end: datetime) -> list[str]:
    n = int((end - start).total_seconds() // 3600) + 1
    return [f"merg_{(start + timedelta(hours=i)):%Y%m%d%H}_4km-pixel.Z" for i in range(n)]


def vintage_month(rows: list[dict]) -> str:
    return max(r["modified"] for r in rows).strftime("%Y-%m")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()
