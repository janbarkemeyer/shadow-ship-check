"""Check that each output preserves the context needed to read the findings."""

import json
from datetime import datetime, timezone

import pytest

from shadow_ship_check.models import Report, TrackPoint
from shadow_ship_check.report import DISCLAIMER, to_json, to_markdown, to_markdown_case, to_text


def _utc(day, hour=0):
    return datetime(2025, 1, day, hour, tzinfo=timezone.utc)


def _report(excerpt=True):
    point = TrackPoint(_utc(2, 12), 25.1234, 121.5678, 4.5)
    return Report(
        query="test vessel",
        identities=[],
        signals=[],
        window=(_utc(1), _utc(3)),
        incident_time=_utc(2, 12),
        excerpt=[("known identity", point)] if excerpt else [],
        excerpt_hours=3,
    )


def test_terminal_shows_window_and_requested_incident_excerpt():
    text = to_text(_report())
    assert "Analysis window: 2025-01-01 00:00 - 2025-01-03 00:00 UTC" in text
    assert "reported incident time (approximate): 2025-01-02 12:00 UTC" in text
    assert "Positions within +/- 3 h:" in text
    assert "2025-01-02 12:00 UTC  known identity  25.1234, 121.5678  4.5 kn" in text


def test_terminal_distinguishes_empty_excerpt_from_no_requested_excerpt():
    assert "No loaded AIS positions in this interval." in to_text(_report(excerpt=False))
    no_request = Report(query="test vessel", identities=[], signals=[])
    assert "reported incident time" not in to_text(no_request)


def test_score_interpretation_is_preserved_in_every_output():
    report = _report()
    assert json.loads(to_json(report))["interpretation"] == DISCLAIMER
    assert DISCLAIMER in to_text(report)
    assert DISCLAIMER in to_markdown(report)
    assert "capped at 100" in DISCLAIMER and "group totals are uncapped" in DISCLAIMER


@pytest.mark.parametrize("incident", [True, False])
def test_combined_report_distinguishes_incident_from_control_cutoff(incident):
    full = _report()
    if not incident:
        full.incident_time = None
    before = Report(query="test vessel", identities=[], signals=[], as_of=_utc(2))
    text = to_markdown_case(full, before, "comparison")
    if incident:
        assert "| Before the incident |" in text
    else:
        assert "| Window-end cut-off |" in text
        assert "This control has no incident time." in text
        assert "Before the incident" not in text


def test_combined_report_keeps_missing_data_notes_in_the_cutoff_section():
    full = _report()
    before = Report(
        query="test vessel",
        identities=[],
        signals=[],
        as_of=_utc(2),
        notes=["No positions inside the analysis window: movement findings are limited by missing data."],
    )
    text = to_markdown_case(full, before, "comparison")
    cutoff_section, full_section = text.split("## Full data", 1)
    assert "No positions inside the analysis window" in cutoff_section
    assert "No positions inside the analysis window" not in full_section
