# Data

## Source

All vessel data comes from [Global Fishing Watch](https://globalfishingwatch.org) (GFW). The bundled
snapshots contain AIS-derived identities and simplified tracks collected on 26 Oct 2026.

| What | Endpoint | Access |
|---|---|---|
| Vessel identities | `GET /v3/vessels/search?query=…&datasets[0]=public-global-vessel-identity:v5.0` | snapshot collected without a token |
| Tracks | `GET /v3/vessels/{id}/tracks?dataset=public-global-all-tracks:v4.0&format=VALUE_ARRAY&binary=true&…` | simplified map tracks; snapshot collected without a token |

Base URL: `https://gateway.api.globalfishingwatch.org`. The track endpoint is not part of GFW's
documented public API and may change without notice. Access to these map requests is not guaranteed.
The client supports `GFW_API_TOKEN`; a token does not guarantee higher-resolution tracks or access
to every dataset. For supported access and current conditions, see the
[GFW API documentation](https://api-doc.globalfishingwatch.org/our-apis/documentation/).

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
treated as registry-confirmed when the same GFW entry holds a registry record with the same
non-empty MMSI and no conflicting known IMO number. This is a match in the available data, not an independent verification of the hull,
flag or legal registration. GFW documents uneven registry coverage by flag and vessel size in its
[vessel identity caveats](https://globalfishingwatch.org/datasets-and-code-vessel-identity/).
`NO_REGISTRY` and `REGISTRY_LOST` can therefore reflect coverage rather than a change in legal status.
At a reference date, the latest-starting covering identity is selected; if none covers it, the
latest-ended dated identity is used, including a record with an end but no start when that end is
at or before the reference date. An unknown start and a later end do not establish an earlier
observation. Equal dates have a deterministic tie-break, not an independent
resolution of conflicting records. The age of an earlier registry match uses its last dated
observation (end, or start when no end is known); an undated match does not establish confirmation
before the reference date.

The decoder rejects truncated messages, invalid segment offsets, invalid coordinates and unavailable
AIS speeds. The CLI reports these as input errors rather than scoring a partial track. Separate GFW
track IDs remain separate even when their displayed name, flag and MMSI are identical. Movement
calculations and figures do not connect segments or gaps longer than three hours. The local planar
cable intersection check rejects tracks or routes spanning the date line. A crossing at an internal
cable vertex counts when the route passes from one side of the track to the other; a tangent touch,
collinear overlap or contact only at a track endpoint does not count as a proper crossing.

## Known limitations

* Simplified tracks. On open water the public track often has one point every 60–90 minutes;
  near the coast it is denser. Short manoeuvres disappear, and gaps of an hour or two mean little.
* Coverage gaps are not AIS switch-offs. GFW has no Eagle S positions from 11 Dec 2024 to 7 Mar
  2025, although other providers recorded the ship crossing Estlink 2. Treat `AIS_GAP` as "this
  source has no data", then check a second source.
* Identity linking is GFW's. GFW decides which AIS identities belong to an IMO. Identities that
  broadcast no IMO (e.g. SHUNXING39) are only found by searching names and MMSIs; the CLI searches
  the hull's MMSIs and recent names automatically, and `--also` links others by hand.
* First/last message dates of an identity overstate how long it was really in use.
* Historical timestamp filtering retains current identity links, registry matches and manually
  associated identities. The fixed Paris MoU 2025 list was published in July 2026, after the case
  incidents. These snapshots do not reconstruct the information available before an incident.
* Cable routes are approximate. OpenStreetMap routes are drawn from nautical charts and
  notices, often simplified, and many cables are missing (the Taiwan layer has no named
  trans-Pacific cables; TPKM-3 is not mapped). A slow crossing of a *mapped* route is evidence
  worth checking; the absence of one means little.

## Cable and pipeline routes

`data/cables/baltic.geojson` and `data/cables/taiwan.geojson` hold submarine telecom and power
cables and gas/oil pipelines from [OpenStreetMap](https://www.openstreetmap.org), extracted on
26 Oct 2026 with the Overpass API: ways tagged `location=underwater|submarine` or
`seamark:type=cable_submarine|pipeline_submarine` within the two regions; water and sewage pipes
dropped; lines simplified with Douglas-Peucker (≈ 50 m) and pieces shorter than 0.3 nm removed.
Each feature keeps its OSM way id, so it can be traced back. © OpenStreetMap contributors,
[ODbL 1.0](https://www.openstreetmap.org/copyright) - a derived database; changes to it must be shared
under the same licence.

The incident cables that are mapped: C-Lion 1, BCS East-West Interlink, Balticconnector, Estlink 1 and 2
and the Finland-Estonia telecom cables (Baltic); an unnamed telecom cable off Taiwan's north coast,
passing about 14 nm north of Keelung (Taiwan). Use `--cables FILE_OR_DIR` for other routes, `--no-cables` to skip.

## Sanctions list

`data/sanctions/uk_vessels.csv` contains 683 vessel records designated under UK sanctions regimes
(645 under the Russia regime), in the bundled 26 Oct 2026 snapshot. Of these, 682 have an IMO number;
the remaining record cannot match this tool's IMO-based check. Names, flags, types and designation
dates are included where available.
Sources: the [UK Sanctions List](https://www.gov.uk/government/publications/the-uk-sanctions-list)
(FCDO, Open Government Licence v3.0), via the OpenSanctions dataset `gb_fcdo_sanctions`
([CC BY-NC 4.0](https://www.opensanctions.org/docs/commercial/exemption/)). The `SANCTIONED` check only
scores designations dated on or before the reference date. Date-only records are treated as 00:00
UTC. The file is a snapshot and does not automatically reflect later listings or delistings.

## Evaluation set

`data/eval/uk_sanctions_vs_random.json.gz` holds the GFW identity search results (plus MMSI and name
look-ups) for the sanctioned and control vessels used in [evaluation.md](evaluation.md). Collected on
26 Oct 2026 the same way as the fixtures. Licence: CC BY-NC 4.0 (GFW).

## Fixtures

`data/fixtures/*.json` hold snapshots of the GFW data used in the case files and tests (identities,
MMSI look-ups and tracks for fixed time windows). They were collected on 26 Oct 2026 through the GFW
web map's endpoints without logging in. `python scripts/refresh_fixtures.py` requests the configured
tracks again and overwrites the fixture files. It does not reproduce the original data state or
automatically discover all relevant identities; queries and track identifiers are fixed in the script.

## Licence

GFW data is published under CC BY-NC 4.0: credit Global Fishing Watch and do not use it
commercially without an agreement with GFW. The project code is MIT-licensed; the fixtures inherit
GFW's licence; the cable layer is ODbL.
