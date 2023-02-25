#!/usr/bin/env python

countries = (
    "Ar",
    "Am",
    "Au",
    "At",
    "Az",
    "Bh",
    "Bd",
    "By",
    "Belgium",
    "Brazil",
    "Bulgaria",
    "Canada",
    "Chile",
    "Colombia",
    "Costa Rica",
    "Croatia",
    "Cyprus",
    "Czech",
    "Denmark",
    "Ecuador",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hong Kong",
    "Hungary",
    "India",
    "Indonesia",
    "Iran",
    "Iraq",
    "Ireland",
    "Israel",
    "Italy",
    "Japan",
    "Kazakhstan",
    "Kenya",
    "Korea",
    "Kyrgyzstan",
    "Latvia",
    "Lebanon",
    "Lithuania",
    "Malaysia",
    "Mexico",
    "Moldova",
    "Morocco",
    "Netherlands",
    "Nigeria",
    "Norway",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Romania",
    "Russian Federation",
    "Serbia",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "South Africa",
    "Spain",
    "Sweden",
    "Switzerland",
    "Taiwan",
    "Tajikistan",
    "Thailand",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "Uruguay",
    "Uzbekistan",
    "Vietnam",
)
# missing: Kyrgyzystan, Tajikistan
abbreviatures = (
    "ar",
    "am",
    "au",
    "at",
    "az",
    "bh",
    "bd",
    "by",
    "be",
    "br",
    "bg",
    "ca",
    "cl",
    "co",
    "cr",
    "hr",
    "cy",
    "cz",
    "dk",
    "ec",
    "ee",
    "fi",
    "fr",
    "de",
    "gr",
    "hk",
    "hu",
    "in",
    "id",
    "ir",
    "iq",
    "ie",
    "il",
    "it",
    "jp",
    "kz",
    "ke",
    "kr",
    "lv",
    "lb",
    "lt",
    "my",
    "mx",
    "md",
    "ma",
    "nl",
    "ng",
    "no",
    "pe",
    "ph",
    "pl",
    "pt",
    "ro",
    "ru",
    "rs",
    "sg",
    "sk",
    "si",
    "za",
    "es",
    "se",
    "ch",
    "tw",
    "th",
    "tn",
    "tr",
    "tm",
    "ua",
    "ae",
    "gb",
    "uy",
    "uz",
    "vn",
)

ports = {
    10_000: ["ar", "br", "hk", "in", "id", "kr", "nl", "sg", "es"],
    11_000: ["md"],
    13_000: ["no", "ro"],
    14_000: ["rs"],
    15_000: ["sk", "uy"],
    16_000: ["si"],
    20_000: ["ca", "ec", "de", "it", "lt", "mx", "pl", "pt", "se", "ch", "tw", "ae"],
    22_000: ["lv"],
    24_000: ["ie"],
    26_000: ["cz"],
    27_000: ["dk", "lb"],
    28_000: ["ee"],
    30_000: ["au", "co", "cl", "gr", "ir", "il", "jp", "my", "th", "gb"],
    31_000: ["cr"],
    35_000: ["at"],
    37_000: ["az", "bh"],
    38_000: ["bg"],
    39_000: ["by"],
    40_000: ["be", "fr", "kz", "ma", "pe", "ph", "ru", "za", "tr", "ua"],
    41_000: ["fi"],
    42_000: ["am", "hr", "ng"],
    43_000: ["hu"],
    44_000: ["iq"],
    45_000: ["ke"],
    46_000: ["vn"],
    47_000: ["tm"],
    48_000: ["cy", "uz"],
}


def choose_port(country) -> int:
    """
    This func chooses a port for a given country
    :param country: str
    :return: int
    """
    for port in ports:
        if country in ports[port]:
            return port
        if port == 48000:
            return 7000


previous_choice = ""


def get_domain() -> str:
    """
    Starts from the last position it was called, returns the next one
    :return: str, returns "stop" if list of countries is over
    """
    global previous_choice
    if previous_choice not in abbreviatures:
        previous_choice = abbreviatures[0]
        return abbreviatures[0]
    else:
        try:
            pointer = abbreviatures.index(previous_choice) + 1
            previous_choice = abbreviatures[pointer]
            return abbreviatures[pointer]
        except IndexError:
            previous_choice = abbreviatures[0]
            return abbreviatures[0]
