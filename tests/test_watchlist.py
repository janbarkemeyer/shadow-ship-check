from datetime import datetime, timezone

from shadow_ship_check import watchlist
from shadow_ship_check.models import Identity


def _ids(imo):
    return [Identity("X", "PAN", "352000000", imo, None, None, None, False, "ais")]


def test_bundled_list_loads():
    listing = watchlist.load()
    assert len(listing) > 500
    assert listing["9329760"]["name"] == "EAGLE S"


def test_designation_only_counts_before_reference_date():
    listing = watchlist.load()
    before = datetime(2025, 1, 1, tzinfo=timezone.utc)
    after = datetime(2026, 1, 1, tzinfo=timezone.utc)
    early = watchlist.sanctions(_ids("9329760"), before, listing)
    assert [s.points for s in early] == [0]  # designated July 2025: context only
    assert [s.points for s in watchlist.sanctions(_ids("9329760"), after, listing)] == [20]
    assert watchlist.sanctions(_ids("1234567"), after, listing) == []
