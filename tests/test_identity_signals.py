from datetime import datetime, timedelta, timezone

from shadow_ship_check.models import Identity, TrackPoint
from shadow_ship_check.signals import (
    concurrent_identities,
    flag_changes,
    identity_handover,
    multiple_identities,
    name_on_other_mmsi,
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


def test_recent_flag_change_scores_by_paris_mou_tier_and_old_history_does_not():
    ids = [
        ident("OLD", "GRC", "240000000", -3000, -2500),
        ident("MID", "LBR", "636000000", -2500, -100),
        ident("NEW", "COK", "518000000", -100, 10),
    ]
    sig = flag_changes(ids, ref=T0)[0]
    assert sig.points == 10  # only LBR -> COK (Paris MoU grey) is recent; GRC -> LBR is > 3 years old
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


def test_flag_tiers():
    to = lambda flag: [ident("A", "GRC", "240000000", -400, -200), ident("B", flag, "1", -200, 10)]  # noqa: E731
    assert flag_changes(to("TGO"), ref=T0)[0].points == 15  # black
    assert flag_changes(to("COK"), ref=T0)[0].points == 10  # grey
    assert flag_changes(to("LBR"), ref=T0)[0].points == 5  # white
    assert flag_changes(to("GAB"), ref=T0)[0].points == 10  # unlisted, ITF flag of convenience
    assert flag_changes(to("GUY"), ref=T0)[0].points == 5  # unlisted, not on the ITF list


def test_ordinary_sale_to_open_registry_stays_low():
    """A Greek ship sold and reflagged to Liberia, registry-confirmed both times."""
    from shadow_ship_check.analyze import analyze

    ids = [ident("ATHINA", "GRC", "240000001", -3000, -400, confirmed=True),
           ident("OCEAN STAR", "LBR", "636000001", -400, 30, confirmed=True)]  # fmt: skip
    r = analyze("test", ids, [], window=(T0 - timedelta(days=3), T0))
    assert r.level == "LOW", [(s.code, s.points) for s in r.signals]


def test_name_on_other_mmsi_ignores_namesakes():
    from dataclasses import replace

    hull = [ident("RAGNAR", "PLW", "511100983", 0, 400)]
    borrowed = replace(ident("RAGNAR", "PLW", "511999999", 100, 105), imo=None)  # no IMO, same flag, in use
    other_ship = replace(ident("RAGNAR", "PLW", "511888888", 100, 300), imo="9621522")  # its own IMO
    other_flag = replace(ident("RAGNAR", "FRA", "227957250", 100, 300), imo=None)  # French boat
    before = replace(ident("RAGNAR", "PLW", "511777777", -900, -800), imo=None)  # before the hull used the name
    lookups = {i.mmsi: [i] for i in (borrowed, other_ship, other_flag, before)}
    sigs = name_on_other_mmsi(hull, lookups)
    assert len(sigs) == 1 and len(sigs[0].evidence) == 1 and "511999999" in sigs[0].evidence[0]


def test_name_on_other_mmsi_does_not_fill_gaps_between_uses():
    from dataclasses import replace

    hull = [
        ident("A", "PLW", "511000001", 0, 10),
        ident("B", "PLW", "511000001", 11, 99),
        ident("A", "PLW", "511000001", 100, 110),
    ]
    namesake = replace(ident("A", "PLW", "511000002", 40, 50), imo=None)
    assert name_on_other_mmsi(hull, {namesake.mmsi: [namesake]}) == []


def test_name_on_other_mmsi_matches_flag_and_time_in_the_same_period():
    from dataclasses import replace

    hull = [ident("A", "PLW", "511000001", 0, 10), ident("A", "TGO", "671000001", 100, 110)]
    namesake = replace(ident("A", "PLW", "511000002", 100, 110), imo=None)
    assert name_on_other_mmsi(hull, {namesake.mmsi: [namesake]}) == []


def test_concurrency_after_reference_date_does_not_score():
    ids = [ident("A", "PLW", "511000001", 10, 100), ident("B", "TGO", "671000001", 20, 100)]
    assert concurrent_identities(ids, ref=T0)[0].points == 0


def test_concurrency_needs_thirty_observed_days_before_reference():
    ids = [ident("A", "PLW", "511000001", -10, 100), ident("B", "TGO", "671000001", -5, 100)]
    assert concurrent_identities(ids, ref=T0)[0].points == 0


def test_concurrency_scores_at_the_thirty_day_boundary():
    ids = [ident("A", "PLW", "511000001", -40, 10), ident("B", "TGO", "671000001", -30, 20)]
    assert concurrent_identities(ids, ref=T0)[0].points == 20


def test_concurrency_with_less_than_thirty_days_in_lookback_does_not_score():
    ids = [ident("A", "PLW", "511000001", -2200, -1820), ident("B", "TGO", "671000001", -2100, -1820)]
    assert concurrent_identities(ids, ref=T0)[0].points == 0
