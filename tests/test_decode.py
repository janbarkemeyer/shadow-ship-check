from datetime import datetime, timezone

from shadow_ship_check.gfw import decode_value_array, decode_varints


def _varint(n: int) -> bytes:
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def _encode(values):
    payload = b"".join(_varint((v << 1) ^ (v >> 63)) for v in values)
    return bytes([0x0A]) + _varint(len(payload)) + payload  # field 1, wire type 2


def test_varint_roundtrip():
    vals = [-2147483648, 2, 0, 8, 121736000, 25233000, 1735905600, 1300000, -5, 0]
    assert decode_varints(_encode(vals)) == vals


def test_value_array_two_segments():
    ts = int(datetime(2025, 1, 3, 12, tzinfo=timezone.utc).timestamp())
    seg1 = [121736000, 25233000, ts, 1300000, 121734000, 25230000, ts + 480, 2400000]
    seg2 = [121700000, 25300000, ts + 7200, 4500000]
    vals = [-2147483648, 2, 0, len(seg1)] + seg1 + seg2
    pts = decode_value_array(_encode(vals))
    assert len(pts) == 3
    assert pts[0].lat == 25.233 and pts[0].lon == 121.736
    assert pts[1].speed == 2.4
    assert [p.segment for p in pts] == [0, 0, 1]
    assert pts[2].t == datetime(2025, 1, 3, 14, tzinfo=timezone.utc)


def test_empty_response():
    assert decode_value_array(b"") == []


def test_real_gfw_response():
    """Binary response captured from the GFW API (Xingshun 39, 3-4 Jan 2025)."""
    from pathlib import Path

    buf = (Path(__file__).parent / "data" / "xingshun39_2025-01-03.pbf").read_bytes()
    pts = decode_value_array(buf)
    assert len(pts) == 59
    assert (pts[0].lat, pts[0].lon) == (25.335045, 121.707316)
    assert pts[0].t == datetime(2025, 1, 3, 8, 52, 21, tzinfo=timezone.utc)
    assert all(a.t <= b.t for a, b in zip(pts, pts[1:]))
