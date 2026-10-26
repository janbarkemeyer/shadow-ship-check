from datetime import datetime, timedelta, timezone

from shadow_ship_check.models import Identity, TrackPoint
from shadow_ship_check.signals import (
    concurrent_identities,
    flag_changes,
    identity_handover,
    multiple_identities,
    registry_confirmation,
)

T0 = datetime(2024, 1, 1, tzinfo=timezone.utc)


def ident(name, flag, mmsi, start_days, end_days, confirmed=False, source="ais"):
    return Identity(
        name,
        flag,
        mmsi,
        "1234567",
        None,
        T0 + timedelta(days=start_days),
        T0 + timedelta(days=end_days),
        confirmed,
        source,
    )


def test_flag_change_into_foc_scores_and_old_history_does_not():
    ids = [
        ident("OLD", "GRC", "240000000", -3000, -2500),
        ident("MID", "LBR", "636000000", -2500, -100),
        ident("NEW", "COK", "518000000", -100, 10),
    ]
    sig = flag_changes(ids, ref=T0)[0]
    assert sig.points == 15  # only LBR -> COK is recent; GRC -> LBR is > 3 years old
    assert any("(recent)" in e for e in sig.evidence)


def test_change_after_reference_date_scores_little():
    ids = [ident("A", "HKG", "477000000", -300, 50), ident("B", "PAN", "352000000", 50, 300)]
    assert flag_changes(ids, ref=T0)[0].points == 5


def test_concurrent_identities_and_no_flag_change_for_them():
    ids = [ident("A", "TZA", "677000000", -200, 10), ident("B", "CMR", "613000000", -100, 10)]
    assert concurrent_identities(ids)[0].code == "CONCURRENT_IDENTITIES"
    assert flag_changes(ids, ref=T0) == []


def test_registry_lost_uses_identity_active_at_reference():
    ids = [ident("A", "MHL", "538000000", -1000, -100, confirmed=True), ident("B", "COK", "518000000", -100, 400)]
    sig = registry_confirmation(ids, ref=T0)[0]
    assert sig.code == "REGISTRY_LOST" and sig.points == 15


def test_multi_identity_counts_lookback_only():
    ids = [ident("A", "GRC", "1", -4000, -3000), ident("B", "LBR", "2", -3000, 10)]
    assert multiple_identities(ids, ref=T0)[0].points == 0


def _track(lat, lon, start_h, n, step_min=30):
    return [TrackPoint(T0 + timedelta(hours=start_h, minutes=step_min * i), lat, lon, 0.5) for i in range(n)]


def test_identity_handover():
    a = _track(25.0, 121.0, 0, 10)  # stops after 4.5 h
    b = _track(25.001, 121.001, 5, 10)  # starts 30 min later, same place
    fetched = {k: (T0 - timedelta(days=1), T0 + timedelta(days=1)) for k in "ab"}
    sig = identity_handover({"a": a, "b": b}, fetched)[0]
    assert sig.code == "IDENTITY_HANDOVER" and "a stops" in sig.evidence[0]


def test_no_handover_at_edge_of_requested_range():
    a = _track(25.0, 121.0, 0, 10)
    b = _track(25.0, 121.0, 5, 10)
    fetched = {"a": (T0, T0 + timedelta(hours=4.5)), "b": (T0 + timedelta(hours=5), T0 + timedelta(days=1))}
    assert identity_handover({"a": a, "b": b}, fetched) == []
