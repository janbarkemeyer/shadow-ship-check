"""Counterexamples at the input and output boundaries of the CLI."""

import gzip
import json
import os
from datetime import datetime, timezone
from itertools import permutations

import pytest

from shadow_ship_check import cli, signals
from shadow_ship_check.gfw import identities_from_entries
from shadow_ship_check.models import TrackPoint

T = datetime(2025, 1, 1, tzinfo=timezone.utc)


def _row(**changes):
    return {
        "shipname": "OLD",
        "flag": "DEU",
        "ssvid": "211000001",
        "imo": "9000001",
        "transmissionDateFrom": "2024-01-01T00:00:00Z",
        "transmissionDateTo": "2024-12-01T00:00:00Z",
        **changes,
    }


def test_disjoint_registry_episodes_survive_both_input_orders():
    old = _row(transmissionDateFrom="2010-01-01T00:00:00Z", transmissionDateTo="2011-01-01T00:00:00Z")
    recent = _row()
    current = _row(
        shipname="CURRENT",
        ssvid="211000002",
        transmissionDateFrom="2024-12-15T00:00:00Z",
        transmissionDateTo="2025-01-01T00:00:00Z",
    )
    for rows in permutations([old, recent]):
        entries = [{"registryInfo": list(rows), "selfReportedInfo": [current]}]
        records = identities_from_entries(entries)
        assert len([i for i in records if i.source == "registry"]) == 2
        assert [(s.code, s.points) for s in signals.registry_confirmation(records, T)] == [("REGISTRY_LOST", 15)]
        assert len(identities_from_entries(entries, dedupe=False)) == 3


def test_repeated_registry_rows_still_merge_after_preserving_raw_episodes():
    records = identities_from_entries([{"registryInfo": [_row(), _row()]}])
    assert len(records) == 1


@pytest.mark.parametrize("field", ["selfReportedInfo", "registryInfo"])
def test_inverted_identity_period_is_rejected(field):
    row = _row(transmissionDateFrom="2025-02-01T00:00:00Z", transmissionDateTo="2025-01-01T00:00:00Z")
    with pytest.raises(ValueError, match="start|begin|period"):
        identities_from_entries([{field: [row]}])


@pytest.mark.parametrize("value", [True, -1, 1.2, "100", {}])
def test_message_counter_requires_a_nonnegative_integer(value):
    with pytest.raises(ValueError, match="messagesCounter"):
        identities_from_entries([{"selfReportedInfo": [_row(messagesCounter=value)]}])


@pytest.mark.parametrize(
    "field,value",
    [
        (0, True),
        (0, float("nan")),
        (0, float("inf")),
        (0, "1735689600"),
        (1, True),
        (1, "0"),
        (2, False),
        (2, None),
        (3, True),
        (3, "2"),
        (4, False),
        (4, "0"),
        (4, -1),
        (4, 0.0),
    ],
)
def test_fixture_track_rows_do_not_coerce_invalid_value_types(field, value):
    row = [T.timestamp(), 0, 0, 2, 0]
    row[field] = value
    with pytest.raises(ValueError):
        TrackPoint.from_row(row)


def test_extra_track_columns_are_not_silently_ignored():
    with pytest.raises(ValueError, match="row|values|columns"):
        TrackPoint.from_row([T.timestamp(), 0, 0, 2, 0, 99])


def test_zero_values_optional_segment_and_partial_dates_remain_valid():
    assert TrackPoint.from_row([0, 0, 0.0, 0]).segment == 0
    assert TrackPoint.from_row([T.timestamp(), 0, 0, 2.0, 1]).segment == 1
    records = identities_from_entries(
        [
            {
                "selfReportedInfo": [
                    _row(transmissionDateTo=None, messagesCounter=0),
                    _row(transmissionDateFrom=None, messagesCounter=None),
                ]
            }
        ]
    )
    assert len(records) == 2


@pytest.mark.parametrize("entry", [{}, {"renamedInfo": []}])
def test_unknown_identity_entry_schema_is_not_an_empty_result(entry):
    with pytest.raises(ValueError, match="identity|schema"):
        identities_from_entries([entry])


def test_known_empty_identity_fields_remain_an_empty_result():
    assert identities_from_entries([{"selfReportedInfo": [], "registryInfo": None, "extraMetadata": 1}]) == []
    assert identities_from_entries([]) == []


def _never_network(monkeypatch):
    class Client:
        def __init__(self):
            raise AssertionError("invalid output paths must fail before network access")

    monkeypatch.setattr(cli, "GFWClient", Client)


@pytest.mark.parametrize("kind", ["same", "symlink", "hardlink"])
def test_live_output_aliases_are_rejected_before_network(monkeypatch, tmp_path, kind):
    first = tmp_path / "result.json"
    first.write_text("keep existing result")
    other = tmp_path / "other.md"
    if kind == "same":
        other = first
    elif kind == "symlink":
        other.symlink_to(first)
    else:
        os.link(first, other)
    _never_network(monkeypatch)
    assert cli.main(["check", "9000001", "--json", str(first), "--md", str(other)]) == 2
    assert first.read_text() == "keep existing result"


@pytest.mark.parametrize("hardlink", [False, True])
def test_single_case_output_does_not_overwrite_its_fixture(tmp_path, fixtures_dir, hardlink):
    source = tmp_path / "eagle_s.json"
    before = (fixtures_dir / "eagle_s.json").read_bytes()
    source.write_bytes(before)
    output = tmp_path / "out.json" if hardlink else source
    if hardlink:
        os.link(source, output)
    assert cli.main(["case", "eagle_s", "--fixtures", str(tmp_path), "--json", str(output)]) == 2
    assert source.read_bytes() == before


def test_all_cases_preflight_rejects_report_alias_before_any_write(tmp_path, fixtures_dir):
    for name in cli.ALL:
        (tmp_path / f"{name}.json").write_bytes((fixtures_dir / f"{name}.json").read_bytes())
    output = tmp_path / "reports"
    output.mkdir()
    source = tmp_path / "yi_peng_3.json"
    before = source.read_bytes()
    (output / "yi_peng_3.md").symlink_to(source)
    assert cli.main(["case", "all", "--fixtures", str(tmp_path), "--md", str(output)]) == 2
    assert source.read_bytes() == before
    assert not (output / "eagle_s.md").exists()


def test_evaluation_output_does_not_overwrite_its_data(tmp_path):
    source = tmp_path / "sample.json.gz"
    with gzip.open(source, "wt") as fh:
        json.dump(
            {
                "records": [
                    {
                        "imo": "9000001",
                        "label": "sanctioned",
                        "as_of": "2025-01-01",
                        "identities": [{"selfReportedInfo": [_row()]}],
                    },
                    {
                        "imo": "9000002",
                        "label": "control",
                        "as_of": "2025-01-01",
                        "identities": [{"selfReportedInfo": [_row(imo="9000002")]}],
                    },
                ]
            },
            fh,
        )
    before = source.read_bytes()
    assert cli.main(["eval", "--data", str(source), "--json", str(source)]) == 2
    assert source.read_bytes() == before


@pytest.mark.parametrize("directory", [False, True])
def test_live_output_does_not_overwrite_cable_inputs(monkeypatch, tmp_path, directory):
    source = tmp_path / "cables.geojson"
    source.write_text('{"type": "FeatureCollection", "features": []}')
    before = source.read_bytes()
    _never_network(monkeypatch)
    assert (
        cli.main(
            [
                "check",
                "9000001",
                "--cables",
                str(tmp_path if directory else source),
                "--json",
                str(source),
            ]
        )
        == 2
    )
    assert source.read_bytes() == before


@pytest.mark.parametrize("queries", [["MISSING"], ["FOUND", "MISSING"]])
def test_unmatched_manual_link_is_an_error_without_partial_output(monkeypatch, tmp_path, queries):
    class Client:
        def search_raw(self, query):
            if query == "MISSING":
                return [{"selfReportedInfo": [_row(shipname="NEARBY BUT DIFFERENT")]}]
            return [{"selfReportedInfo": [_row(shipname="FOUND" if query == "FOUND" else "OWN")]}]

        def track(self, *args):
            raise AssertionError("a failed manual query must stop before loading tracks")

    monkeypatch.setattr(cli, "GFWClient", Client)
    output = tmp_path / "report.json"
    assert (
        cli.main(
            [
                "check",
                "9000001",
                "--no-mmsi-lookup",
                "--no-cables",
                "--no-sanctions",
                "--json",
                str(output),
                *[arg for query in queries for arg in ("--also", query)],
            ]
        )
        == 2
    )
    assert not output.exists()


def test_ambiguous_mmsi_error_lists_the_candidate_imos():
    rows = identities_from_entries([{"selfReportedInfo": [_row(imo=imo) for imo in ("9000002", "9000001")]}])
    with pytest.raises(ValueError, match="9000001, 9000002"):
        cli._same_hull(rows, "211000001")


@pytest.mark.parametrize("symlink_directory", [False, True])
def test_nested_case_export_links_to_the_actual_local_source(monkeypatch, tmp_path, symlink_directory):
    from urllib.parse import unquote

    checkout = tmp_path / "code space"
    (checkout / "cases").mkdir(parents=True)
    source = checkout / "cases" / "eagle_s.md"
    source.write_text("# Eagle S source")
    monkeypatch.setattr(cli, "data_path", lambda: checkout / "data")
    destination = tmp_path / "exports" / "deep"
    if symlink_directory:
        actual = tmp_path / "actual"
        actual.mkdir()
        destination.parent.mkdir()
        destination.symlink_to(actual, target_is_directory=True)
    assert cli.main(["case", "all", "--no-cables", "--no-sanctions", "--md", str(destination)]) == 0
    line = next(
        line
        for line in (destination / "eagle_s.md").read_text().splitlines()
        if line.startswith("Case file with context")
    )
    target = line.split("](", 1)[1].removesuffix(")")
    assert "%20" in target
    assert (destination / unquote(target)).resolve() == source.resolve()


def test_case_export_without_local_sources_uses_versioned_github_link(monkeypatch, tmp_path):
    from shadow_ship_check import __version__

    monkeypatch.setattr(cli, "data_path", lambda: tmp_path / "no-local-cases" / "data")
    assert cli.main(["case", "all", "--no-cables", "--no-sanctions", "--md", str(tmp_path)]) == 0
    assert (
        f"https://github.com/janbarkemeyer/shadow-ship-check/blob/v{__version__}/cases/eagle_s.md"
        in (tmp_path / "eagle_s.md").read_text()
    )
