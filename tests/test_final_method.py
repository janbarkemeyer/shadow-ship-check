"""Counterexamples for dated registry matches and alternative track coverage."""

import random
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from itertools import permutations

from shadow_ship_check import signals
from shadow_ship_check.models import Identity, TrackPoint

T = datetime(2025, 1, 1, tzinfo=timezone.utc)


def identity(name, start, end, confirmed=False):
    return Identity(name, "DEU", "211000001", "9000001", None, start, end, confirmed, "ais")


def point(hours, lon=0):
    return TrackPoint(T + timedelta(hours=hours), 0, lon, 2)


def gap_score(hours, alternative=(), window=None):
    window = window or (T + timedelta(hours=1), T + timedelta(hours=hours - 1))
    found = signals.ais_gaps([point(0), point(hours)], window, cover={"linked": list(alternative)})
    return sum(s.points for s in found)


def test_registry_latest_dated_observation_is_order_independent():
    first_only = identity("A", T - timedelta(days=365), None, True)
    ended = identity("B", T - timedelta(days=500), first_only.start, True)
    current = identity("CURRENT", T - timedelta(days=1), T)
    observed = set()
    for rows in permutations([first_only, ended, current]):
        s = signals.registry_confirmation(rows, T)[0]
        observed.add((s.points, tuple(s.evidence), s.caveat))
    assert len(observed) == 1
    assert next(iter(observed))[0] == 15


def test_registry_known_start_is_recent_evidence_when_end_is_unknown():
    recent = identity("OLD", T - timedelta(days=1), None, True)
    current = identity("CURRENT", T, T)
    s = signals.registry_confirmation([recent, current], T)[0]
    assert s.points == 15
    assert "ended more than" not in s.caveat
    old = replace(recent, start=T - timedelta(days=6 * 365))
    s = signals.registry_confirmation([old, current], T)[0]
    assert s.points == 5
    assert "last dated match" in s.caveat


def test_undated_registry_match_is_not_described_as_absent():
    known = identity("KNOWN", None, None, True)
    current = identity("CURRENT", T, T)
    s = signals.registry_confirmation([known, current], T)[0]
    assert s.code == "NO_REGISTRY"
    assert "dated registry match" in s.title
    assert "undated" in s.caveat


def test_identity_title_counts_combinations_separately_from_episodes():
    rows = [
        identity("A", T - timedelta(days=100), T - timedelta(days=90)),
        identity("A", T - timedelta(days=10), T),
        identity("B", T - timedelta(days=10), T),
    ]
    s = signals.multiple_identities(rows, T)[0]
    assert s.points == 10
    assert "2 distinct name/flag combinations" in s.title
    assert "3 linked records" in s.title


def test_one_distant_linked_point_does_not_hide_an_ais_gap():
    assert gap_score(8, [point(4, 150)]) == 15


def test_one_local_point_cannot_hide_two_fifty_hour_gaps():
    assert gap_score(100, [point(50)]) == gap_score(100) == 20


def test_plausible_linked_observations_can_fill_short_gaps():
    assert gap_score(8, [point(4)]) == 0
    assert gap_score(24, [point(h) for h in range(1, 24)]) == 0


def test_coverage_outside_window_does_not_imply_observations_inside():
    window = (T + timedelta(hours=3), T + timedelta(hours=5))
    assert gap_score(8, [point(h) for h in (1, 2, 6, 7)], window) == 15
    assert gap_score(8, [point(h) for h in (1, 2, 4, 6, 7)], window) == 0


def test_conflicting_additional_points_do_not_remove_existing_coverage():
    local = [point(4)]
    conflicting = [point(3.99, 1)]
    assert gap_score(8, local) == gap_score(8, local + conflicting) == 0
    assert gap_score(8, local + local) == 0


def test_alternative_coverage_never_increases_gap_points():
    rnd = random.Random(49)
    for _ in range(100):
        hours = rnd.choice([8, 12, 24, 50, 100])
        added = [point(rnd.uniform(0.1, hours - 0.1), rnd.choice([0, 0.1, 150])) for _ in range(5)]
        scores = [gap_score(hours, added[:n]) for n in range(len(added) + 1)]
        assert all(after <= before for before, after in zip(scores, scores[1:]))


def test_registry_last_seen_date_is_evidence_without_first_seen_date():
    known = identity("KNOWN", None, T - timedelta(days=1), True)
    current = identity("CURRENT", T, T)
    found = signals.registry_confirmation([known, current], T)
    assert [(s.code, s.points) for s in found] == [("REGISTRY_LOST", 15)]


def test_end_only_identity_is_a_dated_observation():
    last_seen = identity("LAST_SEEN", None, T)
    old = identity("OLD", T - timedelta(days=100), T - timedelta(days=50), True)
    for rows in permutations([last_seen, old]):
        assert signals.active_at(rows, T).name == "LAST_SEEN"
        assert [(s.code, s.points) for s in signals.registry_confirmation(rows, T)] == [("REGISTRY_LOST", 15)]


def test_end_after_reference_does_not_date_unknown_start_identity():
    future = identity("FUTURE", None, T + timedelta(days=1))
    undated = identity("UNDATED", None, None)
    assert signals.active_at([future, undated], T) is None


def test_past_end_only_identity_does_not_imply_presence_at_reference():
    unknown_start = identity("LAST_SEEN", None, T - timedelta(days=1))
    covering = identity("COVERING", T - timedelta(days=50), T + timedelta(days=1), True)
    assert signals.active_at([unknown_start, covering], T).name == "COVERING"


def test_linked_observation_can_remove_only_the_extra_absence_points():
    own = [point(-10), point(-2, 0.1)]
    window = (T, T + timedelta(hours=8))
    base = signals.ais_gaps(own, window)
    covered = signals.ais_gaps(own, window, cover={"linked": [point(4, 0.1)]})
    assert base[0].points == 20
    assert covered[0].points == 5
    assert any("does not establish continuous coverage" in e for e in covered[0].evidence)


def test_distant_linked_point_does_not_remove_absence_points():
    found = signals.ais_gaps([point(-1)], (T, T + timedelta(hours=8)), cover={"linked": [point(4, 150)]})
    assert found[0].points == 15


def test_later_identity_can_remove_absence_points_with_plausible_prior_observation():
    found = signals.ais_gaps([point(10)], (T, T + timedelta(hours=8)), cover={"linked": [point(4)]})
    assert found[0].points == 0


def test_alternative_observation_outside_window_does_not_remove_absence_points():
    found = signals.ais_gaps([point(-1)], (T, T + timedelta(hours=8)), cover={"linked": [point(9)]})
    assert found[0].points == 15
