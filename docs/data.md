# Data

## Source

All vessel data comes from [Global Fishing Watch](https://globalfishingwatch.org) (GFW), which publishes
AIS-derived vessel identities and tracks for free.

| What | Endpoint | Access |
|---|---|---|
| Vessel identities | `GET /v3/vessels/search?query=…&datasets[0]=public-global-vessel-identity:v5.0` | public |
| Tracks | `GET /v3/vessels/{id}/tracks?dataset=public-global-all-tracks:v4.0&format=VALUE_ARRAY&binary=true&…` | public, simplified; the same request the GFW map makes |

Base URL: `https://gateway.api.globalfishingwatch.org`. The track endpoint is not part of GFW's
documented public API and may change without notice. Tracks in other formats (JSON, GeoJSON) require
download permissions. An API token (`GFW_API_TOKEN`) is optional; GFW issues them free of charge for
non-commercial use.

### Binary track format

`VALUE_ARRAY` with `binary=true` is a protobuf message with one packed `sint32` field. Decoded:

```
[ sentinel, n_segments, offset_1 … offset_n, lon*1e6, lat*1e6, unix_seconds, speed_kn*1e6, … ]
```

The offsets are indices into the value list where each track segment starts. The decoder in
`src/shadow_ship_check/gfw.py` is tested against a response captured from the API
(`tests/data/xingshun39_2025-01-03.pbf`).

## Identities: what "registry-confirmed" means

A GFW search result can carry `selfReportedInfo` (what the ship broadcasts in AIS) and `registryInfo`
(matching records from public registries such as IMO or regional fishery bodies). An AIS identity is
treated as registry-confirmed when the same GFW entry holds a registry record with the same MMSI.
Logged-out users see fewer registry sources than logged-in users (GFW: "11 sources won't appear
unless you log in"), so `NO_REGISTRY` may be a coverage artefact.

## Known limitations

* **Simplified tracks.** On open water the public track often has one point every 60–90 minutes;
  near the coast it is denser. Short manoeuvres disappear, and gaps of an hour or two mean little.
* **Coverage gaps are not AIS switch-offs.** GFW has no Eagle S positions from 11 Dec 2024 to 7 Mar
  2025, although other providers recorded the ship crossing Estlink 2. Treat `AIS_GAP` as "this
  source has no data", then check a second source.
* **Identity linking is GFW's.** GFW decides which AIS identities belong to an IMO. Identities that
  broadcast no IMO (e.g. SHUNXING39) are only found by searching names and MMSIs; the CLI searches
  the hull's MMSIs and recent names automatically, and `--also` links others by hand.
* **First/last message dates** of an identity overstate how long it was really in use.
* **No cable geometry** is bundled. Public cable maps are rarely openly licensed. Bring your own
  GeoJSON (`--cables`); `examples/demo_cables.geojson` is a synthetic line for testing only.

## Fixtures

`data/fixtures/*.json` hold snapshots of the GFW data used in the case files and tests (identities,
MMSI look-ups and tracks for fixed time windows). They were collected on 26 Oct 2026 through the GFW
web map's public API without logging in. `python scripts/refresh_fixtures.py` downloads them again.

## Licence

GFW data is published under **CC BY-NC 4.0**: credit Global Fishing Watch and do not use it
commercially without an agreement with GFW. The project code is MIT-licensed; the fixtures inherit
GFW's licence.
