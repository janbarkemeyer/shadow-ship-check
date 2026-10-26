import json

from shadow_ship_check.gfw import identities_from_entries


def test_eagle_s_identities(fixtures_dir):
    fx = json.loads((fixtures_dir / "eagle_s.json").read_text())
    ids = identities_from_entries(fx["identities"])
    names = [i.name for i in ids]
    assert names == ["NORSTAR INTREPID", "EAGLE-S"]
    assert ids[0].registry_confirmed and ids[0].flag == "MHL"
    assert not ids[1].registry_confirmed and ids[1].flag == "COK"


def test_registry_duplicate_is_not_a_new_identity(fixtures_dir):
    # GFW lists BALTICFULMAR in the registry with flag DEU - same hull, same MMSI
    fx = json.loads((fixtures_dir / "newnew_polar_bear.json").read_text())
    ids = identities_from_entries(fx["identities"])
    assert sum(1 for i in ids if i.key[0] == "BALTICFULMAR") == 1


def test_registry_only_identity_is_kept(fixtures_dir):
    # DONGSHUN3 only exists as a registry record (AIS name was JIN LONG 389)
    fx = json.loads((fixtures_dir / "hong_tai_58.json").read_text())
    names = {i.name for i in identities_from_entries(fx["identities"])}
    assert {"DONGSHUN3", "JIN LONG 389", "HONGTAI58", "HONGTA 8"} <= names


def test_no_dedupe_keeps_imo_less_copy(fixtures_dir):
    fx = json.loads((fixtures_dir / "hong_tai_58.json").read_text())
    raw = identities_from_entries(fx["mmsi_lookups"]["671756000"], dedupe=False)
    hongtai = [i for i in raw if i.name == "HONGTAI58"]
    assert {i.imo for i in hongtai} == {None, "8357069"}


def test_parse_ts_fractional_seconds():
    from datetime import datetime, timezone

    from shadow_ship_check.models import parse_ts

    assert parse_ts("2022-09-30T08:50:27.02Z") == datetime(2022, 9, 30, 8, 50, 27, 20000, tzinfo=timezone.utc)
    assert parse_ts("2023-07-22T10:15:56Z") == datetime(2023, 7, 22, 10, 15, 56, tzinfo=timezone.utc)
    assert parse_ts("2024-01-01T00:00:00.1234567Z").microsecond == 123456
    assert parse_ts(None) is None
