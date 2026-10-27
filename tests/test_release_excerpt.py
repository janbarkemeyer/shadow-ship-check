"""Keep requested evidence consistent with the timestamp cut-off."""

from datetime import datetime, timedelta, timezone

from shadow_ship_check.analyze import analyze
from shadow_ship_check.models import TrackPoint
from shadow_ship_check.report import to_text

T = datetime(2025, 1, 1, tzinfo=timezone.utc)


def point(hour):
    return TrackPoint(T + timedelta(hours=hour), 25, 121, 4)


def test_incident_excerpt_before_cutoff_is_preserved_and_clipped():
    report = analyze(
        "q",
        [],
        [point(9), point(10), point(11), point(12)],
        window=(T, T + timedelta(hours=24)),
        as_of=T + timedelta(hours=11),
        incident_time=T + timedelta(hours=10),
    )
    assert report.incident_time == T + timedelta(hours=10)
    assert [p.t.hour for _, p in report.excerpt] == [9, 10, 11]
    assert "2025-01-01 10:00 UTC" in to_text(report)
    assert all(p.t <= report.as_of for _, p in report.excerpt)


def test_incident_at_cutoff_remains_visible_without_later_positions():
    report = analyze(
        "q", [], [point(10), point(11)], as_of=T + timedelta(hours=10), incident_time=T + timedelta(hours=10)
    )
    assert report.incident_time == report.as_of
    assert [p.t.hour for _, p in report.excerpt] == [10]


def test_incident_after_effective_end_is_omitted_with_explanation():
    report = analyze(
        "q",
        [],
        [point(9), point(10), point(11)],
        window=(T, T + timedelta(hours=10)),
        as_of=T + timedelta(hours=12),
        incident_time=T + timedelta(hours=11),
    )
    assert report.as_of == T + timedelta(hours=10)
    assert report.incident_time is None
    assert not report.excerpt
    assert any("after the timestamp cut-off" in n for n in report.notes)


def test_cutoff_without_requested_incident_does_not_invent_an_excerpt():
    report = analyze("q", [], [point(10)], as_of=T + timedelta(hours=12))
    assert report.incident_time is None
    assert not report.excerpt
    assert not any("Incident excerpt omitted" in n for n in report.notes)
