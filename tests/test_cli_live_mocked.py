"""End-to-end tests of `ssc check` with the HTTP layer mocked by fixture data."""

import io
import json
import urllib.error
from pathlib import Path

from shadow_ship_check import gfw
from shadow_ship_check.cli import main

DATA = Path(__file__).parent / "data"


class _Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _varint(n):
    out = bytearray()
    while True:
        b, n = n & 0x7F, n >> 7
        out.append(b | (0x80 if n else 0))
        if not n:
            return bytes(out)


def encode_track(points):
    """Inverse of gfw.decode_value_array for one segment (used to fake the API)."""
    vals = [-2147483648, 1, 0]
    for t, lat, lon, sp, *_ in points:
        vals += [round(lon * 1e6), round(lat * 1e6), int(t), round(sp * 1e6)]
    payload = b"".join(_varint((v << 1) ^ (v >> 63)) for v in vals)
    return b"\x0a" + _varint(len(payload)) + payload


def _fake_api(fx, calls):
    by_vessel = {v["vessel_id"]: v["points"] for v in fx["tracks"].values()}

    def fake_urlopen(req, timeout=0):
        url = req.full_url
        calls.append(url)
        if "/vessels/search" in url:
            q = url.split("query=")[1].split("&")[0]
            if q in fx.get("mmsi_lookups", {}):
                return _Resp(json.dumps({"entries": fx["mmsi_lookups"][q]}).encode())
            if q == "SHUNXING39":
                return _Resp(json.dumps({"entries": fx["mmsi_lookups"]["613003889"]}).encode())
            return _Resp(json.dumps({"entries": fx["identities"]}).encode())
        vid = url.split("/vessels/")[1].split("/tracks")[0]
        return _Resp(encode_track(by_vessel[vid]) if vid in by_vessel else b"")

    return fake_urlopen


def test_encoder_matches_real_response():
    real = (DATA / "xingshun39_2025-01-03.pbf").read_bytes()
    pts = gfw.decode_value_array(real)
    again = gfw.decode_value_array(encode_track([[p.t.timestamp(), p.lat, p.lon, p.speed] for p in pts]))
    assert [(p.t, p.lat, p.lon, p.speed) for p in pts] == [(p.t, p.lat, p.lon, p.speed) for p in again]


def test_check_finds_identity_swap_with_also(monkeypatch, tmp_path, fixtures_dir):
    fx = json.loads((fixtures_dir / "xingshun_39.json").read_text())
    calls = []
    monkeypatch.setattr(gfw.urllib.request, "urlopen", _fake_api(fx, calls))
    md = tmp_path / "report.md"
    rc = main(
        [
            "check",
            "8358427",
            "--start",
            "2025-01-02",
            "--end",
            "2025-01-04",
            "--also",
            "SHUNXING39",
            "--at",
            "2025-01-02T23:40",
            "--md",
            str(md),
        ]
    )
    assert rc == 0
    text = md.read_text()
    assert "IDENTITY_HANDOVER" in text and "CONCURRENT_IDENTITIES" in text
    assert "SHUNXING39/CMR/613003889 (no IMO)" in text
    assert any("/tracks?" in c for c in calls)


def test_check_without_also_still_reports_gap(monkeypatch, tmp_path, fixtures_dir):
    fx = json.loads((fixtures_dir / "xingshun_39.json").read_text())
    monkeypatch.setattr(gfw.urllib.request, "urlopen", _fake_api(fx, []))
    md = tmp_path / "report.md"
    assert main(["check", "8358427", "--start", "2025-01-02", "--end", "2025-01-04", "--md", str(md)]) == 0
    text = md.read_text()
    assert "AIS_GAP" in text and "XINGSHUN39" in text


def test_network_error_is_reported(monkeypatch, capsys):
    def boom(req, timeout=0):
        raise urllib.error.URLError("Tunnel connection failed: 403 Forbidden")

    monkeypatch.setattr(gfw.urllib.request, "urlopen", boom)
    assert main(["check", "8358427"]) == 2
    assert "Could not reach Global Fishing Watch" in capsys.readouterr().err
