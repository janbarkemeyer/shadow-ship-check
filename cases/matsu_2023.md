# Case file: Matsu cables TPKM-2 and TPKM-3, February 2023 (no ship identified)

| | |
|---|---|
| Incident | Both cables linking Taiwan with the Matsu islands failed: TPKM-2 on the evening of 2 Feb 2023, TPKM-3 around noon on 8 Feb 2023 |
| Suspected cause | According to Taiwan's National Communications Commission, a Chinese fishing vessel (TPKM-2) and a Chinese freighter (TPKM-3) |
| Status | **Suspected.** No intent established; the NCC said there was no evidence of deliberate damage. Matsu relied on microwave backup until repairs in April 2023. |
| Tool result | not run – **no ship names, MMSIs or IMO numbers were published** |

## Why this case is still in the project

It is the template for the hard case: the authorities knew roughly what kind of ship was involved,
but the public never got an identifier. Without a name, MMSI or IMO there is nothing to look up in
GFW, and a fishing vessel without AIS would be invisible anyway.

What would be needed to work on it:

1. The cable routes between Taiwan and Matsu (TPKM-2: Tamsui – Dongyin; TPKM-3: Taoyuan – Nangan).
2. An area search ("which AIS vessels were slow within x nm of the route on 2 Feb evening / 8 Feb
   noon?"). GFW offers this as area reports for logged-in users; this tool does not implement it yet
   (see roadmap in the README).
3. A list of the candidate ships, then `ssc check <MMSI>` on each.

## Sources

* [New Bloom, 17 Feb 2023](https://newbloommag.net/2023/02/17/matsu-submarine-cable-cut/) – the two cables, fishing vessel and freighter, NCC statement
* [TechNews, 17 Feb 2023](https://cdn.technews.tw/2023/02/17/the-submarine-cable-was-damaged-suspected-to-be-caused-by-chinese-ship/) – times, MMSI pointing to China, no names
