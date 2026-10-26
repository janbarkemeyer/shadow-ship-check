"""Reference lists: flags of convenience and MMSI country prefixes (MIDs).

The FOC list is compiled from ITF (International Transport Workers' Federation)
publications: the long-standing list plus the additions announced in May 2024
(Gabon, Eswatini) and November 2025 (Dominica, The Gambia, Niue). ITF counts
48 registries; second registries such as the German (GIS) or French (FIS)
international registers cannot be told apart from the national flag in AIS
and are therefore not included. Always verify against the current ITF list
before publishing claims: https://www.itfseafarers.org
"""

FLAGS_OF_CONVENIENCE = {
    "ATG": "Antigua and Barbuda",
    "BHS": "Bahamas",
    "BRB": "Barbados",
    "BLZ": "Belize",
    "BMU": "Bermuda",
    "BOL": "Bolivia",
    "KHM": "Cambodia",
    "CMR": "Cameroon",
    "CYM": "Cayman Islands",
    "COM": "Comoros",
    "COK": "Cook Islands",
    "CUW": "Curacao",
    "CYP": "Cyprus",
    "GNQ": "Equatorial Guinea",
    "FRO": "Faroe Islands",
    "GEO": "Georgia",
    "GIB": "Gibraltar",
    "HND": "Honduras",
    "JAM": "Jamaica",
    "LBN": "Lebanon",
    "LBR": "Liberia",
    "MLT": "Malta",
    "MHL": "Marshall Islands",
    "MUS": "Mauritius",
    "MDA": "Moldova",
    "MNG": "Mongolia",
    "MMR": "Myanmar",
    "PRK": "North Korea",
    "PLW": "Palau",
    "PAN": "Panama",
    "STP": "Sao Tome and Principe",
    "KNA": "St Kitts and Nevis",
    "VCT": "St Vincent and the Grenadines",
    "SLE": "Sierra Leone",
    "LKA": "Sri Lanka",
    "TZA": "Tanzania (Zanzibar)",
    "TGO": "Togo",
    "TON": "Tonga",
    "TUV": "Tuvalu",
    "VUT": "Vanuatu",
    "GAB": "Gabon",
    "SWZ": "Eswatini",
    "DMA": "Dominica",
    "GMB": "The Gambia",
    "NIU": "Niue",
}

# Maritime Identification Digits (first 3 digits of an MMSI) -> ISO3 flag.
# Subset covering the flags that matter for this project; extend as needed.
MID_TO_FLAG = {
    "205": "BEL",
    "209": "CYP",
    "210": "CYP",
    "211": "DEU",
    "212": "CYP",
    "213": "GEO",
    "214": "MDA",
    "215": "MLT",
    "218": "DEU",
    "219": "DNK",
    "220": "DNK",
    "229": "MLT",
    "230": "FIN",
    "231": "FRO",
    "236": "GIB",
    "237": "GRC",
    "239": "GRC",
    "240": "GRC",
    "241": "GRC",
    "244": "NLD",
    "245": "NLD",
    "246": "NLD",
    "248": "MLT",
    "249": "MLT",
    "256": "MLT",
    "257": "NOR",
    "258": "NOR",
    "259": "NOR",
    "265": "SWE",
    "266": "SWE",
    "273": "RUS",
    "275": "LVA",
    "276": "EST",
    "277": "LTU",
    "304": "ATG",
    "305": "ATG",
    "306": "CUW",
    "308": "BHS",
    "309": "BHS",
    "310": "BMU",
    "311": "BHS",
    "312": "BLZ",
    "314": "BRB",
    "319": "CYM",
    "325": "DMA",
    "334": "HND",
    "339": "JAM",
    "341": "KNA",
    "351": "PAN",
    "352": "PAN",
    "353": "PAN",
    "354": "PAN",
    "355": "PAN",
    "356": "PAN",
    "357": "PAN",
    "370": "PAN",
    "371": "PAN",
    "372": "PAN",
    "373": "PAN",
    "374": "PAN",
    "375": "VCT",
    "376": "VCT",
    "377": "VCT",
    "412": "CHN",
    "413": "CHN",
    "414": "CHN",
    "416": "TWN",
    "417": "LKA",
    "440": "KOR",
    "441": "KOR",
    "445": "PRK",
    "450": "LBN",
    "457": "MNG",
    "477": "HKG",
    "506": "MMR",
    "511": "PLW",
    "514": "KHM",
    "515": "KHM",
    "518": "COK",
    "538": "MHL",
    "555": "NIU",
    "570": "TON",
    "572": "TUV",
    "576": "VUT",
    "577": "VUT",
    "613": "CMR",
    "620": "COM",
    "626": "GAB",
    "629": "GMB",
    "631": "GNQ",
    "636": "LBR",
    "637": "LBR",
    "645": "MUS",
    "667": "SLE",
    "668": "STP",
    "669": "SWZ",
    "671": "TGO",
    "674": "TZA",
    "677": "TZA",
    "720": "BOL",
    "750": "GUY",
}


def is_foc(flag: str | None) -> bool:
    return bool(flag) and flag.upper() in FLAGS_OF_CONVENIENCE


def flag_from_mmsi(mmsi: str | None) -> str | None:
    if not mmsi or len(mmsi) != 9 or not mmsi.isascii() or not mmsi.isdigit():
        return None
    return MID_TO_FLAG.get(mmsi[:3])


# Paris MoU flag performance lists 2025 (published 1 July 2026), based on port
# state inspections and detentions 2023-2025. Black = high / very high risk.
# Flags with too few inspections in the Paris MoU region are not listed.
# Source: https://parismou.org (Paris MoU WGB Flag performance list 2025)
PARIS_MOU_BLACK = {"KNA", "PLW", "TGO", "GNB", "BLZ", "VUT", "VNM", "COM", "TZA", "CMR"}
PARIS_MOU_GREY = {
    "KOR", "LTU", "LVA", "IND", "MAR", "SMR", "DZA", "SLE", "THA", "RUS",
    "LBN", "PHL", "EGY", "VCT", "COK", "ALB", "BGD", "TUV", "TUN",
}  # fmt: skip
PARIS_MOU_WHITE = {
    "CYM", "SWE", "NOR", "DNK", "JPN", "SGP", "FRA", "FIN", "NLD", "LUX", "ITA", "HKG", "DEU", "PRT",
    "BHS", "MLT", "IMN", "BMU", "CHN", "USA", "MHL", "CYP", "ESP", "GBR", "GRC", "SAU", "IRL", "GIB",
    "LBR", "HRV", "BRB", "TUR", "EST", "JEY", "ATG", "PAN", "FRO", "BEL", "POL", "CAN",
}  # fmt: skip


def flag_tier(flag: str | None) -> str:
    """'black', 'grey', 'white' (Paris MoU 2025) or 'unlisted'."""
    f = (flag or "").upper()
    if f in PARIS_MOU_BLACK:
        return "black"
    if f in PARIS_MOU_GREY:
        return "grey"
    if f in PARIS_MOU_WHITE:
        return "white"
    return "unlisted"
