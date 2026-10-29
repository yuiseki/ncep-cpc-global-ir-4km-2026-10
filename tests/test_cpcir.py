from datetime import datetime

import cpcir


def row(name, modified, size):
    return (
        f'<tr><td class="indexcolname"><a href="{name}">{name}</a></td>'
        f'<td class="indexcollastmod">{modified}  </td><td class="indexcolsize"> {size}</td></tr>\n'
    )


LISTING = (
    row("merg_2026102700_4km-pixel.Z", "27-Oct-2026 02:06", "25M")
    + row("merg_2026102701_4km-pixel.Z", "27-Oct-2026 03:06", "25M")
    + row("geomerg_satid_202610.Z", "01-Oct-2026 00:00", "3.0M")
    + row("IRTBB_current.gif", "29-Oct-2026 02:14", "76K")
)


def test_parse_listing_keeps_only_hourly_files():
    rows = cpcir.parse_listing(LISTING)
    assert [r["name"] for r in rows] == [
        "merg_2026102700_4km-pixel.Z",
        "merg_2026102701_4km-pixel.Z",
    ]
    assert rows[0]["modified"] == datetime(2026, 10, 27, 2, 6)


def test_hour_of_name():
    assert cpcir.hour_of("merg_2026102623_4km-pixel.Z") == datetime(2026, 10, 26, 23)


def test_window_names_are_consecutive_hours():
    names = cpcir.window_names(datetime(2026, 10, 20), datetime(2026, 10, 26, 23))
    assert len(names) == 168
    assert names[0] == "merg_2026102000_4km-pixel.Z"
    assert names[-1] == "merg_2026102623_4km-pixel.Z"


def test_decoded_size_is_two_records_of_the_grid():
    assert cpcir.DECODED_BYTES == 2 * 9896 * 3298


def test_vintage_is_the_last_modified_month():
    rows = cpcir.parse_listing(LISTING)
    assert cpcir.vintage_month(rows) == "2026-10"
