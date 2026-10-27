"""Keep malformed sample data separate from valid scores and missing history."""

import copy
import gzip
import json

import pytest

from shadow_ship_check import cli, evaluate


def record(label="sanctioned", imo="9000001", *, future=False):
    return {
        "label": label,
        "imo": imo,
        "as_of": "2025-06-01",
        "identities": [
            {
                "selfReportedInfo": [
                    {
                        "shipname": "SHIP",
                        "flag": "DEU",
                        "ssvid": "211000001",
                        "imo": imo,
                        "transmissionDateFrom": "2026-01-01" if future else "2024-01-01",
                        "transmissionDateTo": "2026-06-01",
                    }
                ]
            }
        ],
    }


def sample():
    return {"records": [record(), record("control", "9000002")]}


@pytest.mark.parametrize("imo", [9000001, "900001", "9000001 ", "٩٠٠٠٠٠١"])
def test_imo_is_an_exact_seven_digit_string(imo):
    row = record()
    row["imo"] = imo
    with pytest.raises(ValueError, match="IMO"):
        evaluate.score_record(row)


def test_numeric_duplicate_cannot_be_scored_as_a_second_vessel():
    data = sample()
    data["records"].append({**record("control"), "imo": 9000001})
    with pytest.raises(ValueError, match="IMO"):
        evaluate.evaluate(data)


@pytest.mark.parametrize("as_of", [20250601, None, []])
def test_invalid_reference_type_is_an_input_error(as_of):
    with pytest.raises(ValueError, match="as_of"):
        evaluate.score_record({**record(), "as_of": as_of})


@pytest.mark.parametrize("field", ["mmsi_lookups", "name_lookups"])
@pytest.mark.parametrize("value", [[1], 0])
def test_lookup_mapping_type_is_checked_even_when_falsey(field, value):
    with pytest.raises(ValueError, match=field):
        evaluate.score_record({**record(), field: value})


@pytest.mark.parametrize("data", [[], {"records": {}}, {"records": [None]}, {"records": [], "meta": []}])
def test_invalid_file_structure_is_an_input_error(data):
    with pytest.raises(ValueError):
        evaluate.evaluate(data)


@pytest.mark.parametrize(
    "entries",
    [[{}], [{"selfReportedInfo": []}], [{"selfReportedInfo": [{}]}]],
)
def test_nonempty_unrecognized_primary_response_is_not_an_ordinary_zero(entries):
    with pytest.raises(ValueError, match="recogni.ed identity"):
        evaluate.score_record({**record(), "identities": entries})


def test_foreign_only_primary_response_is_rejected():
    row = record()
    row["identities"] = record(imo="9000002")["identities"]
    with pytest.raises(ValueError, match="compatible"):
        evaluate.score_record(row)


def test_empty_raw_response_remains_distinct_from_filtered_missing_history():
    data = sample()
    data["records"][1] = record("control", "9000002", future=True)
    data["records"].append({**record("control", "9000003"), "identities": []})
    result = evaluate.evaluate(data)
    assert result["missing"] == 1
    assert result["n"] == {"sanctioned": 1, "control": 1}
    assert result["unavailable_at_reference"] == {"sanctioned": 0, "control": 1}
    assert evaluate.score_record(data["records"][1]) == (0, {})
    assert "data gap, not an ordinary-history finding" in evaluate.to_text(result, {})


def test_custom_sample_gets_shared_interpretation_without_a_holdout_claim():
    data = sample()
    data["meta"] = {"title": "UK-sanctioned shadow-fleet vessels vs. random ships"}
    result = evaluate.evaluate(data)
    text = evaluate.to_text(result, data["meta"])
    assert result["interpretation"] in text
    assert "does not predict cable incidents" in text
    assert "does not reconstruct past knowledge" in text
    assert "selection bias" in text and "dependence between related vessels" in text
    assert "untouched holdout" not in result["interpretation"]
    reviewed = evaluate.evaluate(data, reviewed_sample=True)
    assert "not an untouched holdout" in reviewed["interpretation"]
    for key in result.keys() - {"interpretation"}:
        assert reviewed[key] == result[key]


def test_cli_invalid_evaluation_types_are_reported_without_traceback(tmp_path, capsys):
    path = tmp_path / "sample.json.gz"
    data = sample()
    data["records"][0]["as_of"] = 20250601
    with gzip.open(path, "wt", encoding="utf-8") as f:
        json.dump(data, f)
    assert cli.main(["eval", "--data", str(path)]) == 2
    error = capsys.readouterr().err
    assert "as_of" in error and "Traceback" not in error


def test_bundled_metrics_keep_reviewed_scores_and_expose_the_reference_data_gap():
    data = evaluate.load()
    original = copy.deepcopy(data)
    result = evaluate.evaluate(data, reviewed_sample=True)
    assert result["n"] == {"sanctioned": 300, "control": 300}
    assert result["auc"] == 0.8325777777777777
    assert result["unavailable_at_reference"] == {"sanctioned": 0, "control": 1}
    assert data == original


def test_source_context_survives_export_as_unverified_input_metadata():
    data = sample()
    data["meta"] = {
        "title": "Sample",
        "collected": "2025-06-01",
        "source": "Global Fishing Watch",
        "licence": "CC BY-NC 4.0",
        "private_note": "not an exported source field",
    }
    result = evaluate.evaluate(data)
    context = result["dataset_context"]
    assert "not independently verified" in context["description"]
    assert context["source"] == "Global Fishing Watch" and context["licence"] == "CC BY-NC 4.0"
    assert "private_note" not in context
    text = evaluate.to_text(result, data["meta"])
    assert context["description"] in text and context["licence"] in text


def test_wrong_source_metadata_type_is_an_input_error():
    data = sample()
    data["meta"] = {"source": ["not a source string"]}
    with pytest.raises(ValueError, match="meta"):
        evaluate.evaluate(data)
