"""
.. _serp:

Import Search Engine Results Pages (SERPs) for Google and YouTube
=================================================================
Analyzing a single SERP is like getting one person to fill out a questionnaire
and calling it a survey.

Just like surveys, SERPs need to be collected in large-enough numbers that are
representative of the industry/market you want to understand. This is the main
feature of the ``serp_`` functions. They allow you to get the SERPs for a list
of queries, across several dimensions (like country, search type, start
position, and so on).

There are many parameters that can be used, and you can supply a list for each.
The function will get the SERPs for the *product* of all those lists. For
example, let's say you you provide the following arguments to the
:func:`serp_goog` function:

* `q`: ['serp tools', 'best serp tools', 'serp tool reviews']
* `gl`: ['us', 'ca', 'uk', 'au', 'nz']
* `start`: [1, 11, 21]

The function will produce:
3 (queries) x 5 (countries) x 3 (start positions) = 45 requests

You typically get ten results each, so in this case you would get 450 rows of
data.

All this is done in with one line of code. The result is a single DataFrame
with a row for each result, and columns for each attribute (title, snippet,
etc.), as well as meta data columns, like `queryTime` and the parameters you
selected (`q`, `gl`, and `start` in this case).


Before being able to run queries using :func:`serp_goog`, you will need to set
up some credentials as follows (you don't need a custom search engine for
:func:`serp_youtube`):

* `Create a custom search engine <https://cse.google.com/>`_: At first, you might be
  asked to enter a site to search. Enter any domain, then go to the control panel and
  remove it. Make sure you enable "Search the entire web" and image search. You will
  also need to get your search engine ID, which you can find on the control panel page.

* `Enable the custom search API <https://console.cloud.google.com/apis/library/customsearch.googleapis.com?pli=1>`_:
  The service will allow you to retrieve and display search results from your custom
  search engine programmatically. You will need to create a project for this first.

* `Create credentials for this project <https://console.developers.google.com/apis/api/customsearch.googleapis.com/credentials>`_:
  so you can get your key.

* `Enable billing for your project <https://console.cloud.google.com/billing/projects>`_
  if you want to run more than 100 queries per day. The first 100 queries are free; then
  for each additional 1,000 queries, you pay $5.


"""

__all__ = [
    "SERP_GOOG_VALID_VALS",
    "YOUTUBE_TOPIC_IDS",
    "YOUTUBE_VID_CATEGORY_IDS",
    "serp_goog",
    "serp_youtube",
    "set_logging_level",
    "youtube_channel_details",
    "youtube_video_details",
]

import datetime
import logging
from itertools import product

import pandas as pd

if int(pd.__version__[0]) >= 1:
    from pandas import json_normalize
else:
    from pandas.io.json import json_normalize

import requests

SERP_GOOG_LOG_FMT = (
    "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d "
    "| %(funcName)s | %(message)s"
)
logging.basicConfig(format=SERP_GOOG_LOG_FMT)


##############################################################################
# Google variables
##############################################################################


SERP_GOOG_VALID_VALS = dict(
    fileType={
        "bas",
        "c",
        "cc",
        "cpp",
        "cs",
        "cxx",
        "doc",
        "docx",
        "dwf",
        "gpx",
        "h",
        "hpp",
        "htm",
        "html",
        "hwp",
        "java",
        "kml",
        "kmz",
        "odp",
        "ods",
        "odt",
        "pdf",
        "pl",
        "ppt",
        "pptx",
        "ps",
        "py",
        "rtf",
        "svg",
        "swf",
        "tex",
        "text",
        "txt",
        "wap",
        "wml",
        "xls",
        "xlsx",
        "xml",
    },
    c2coff={0, 1},
    cr={
        "countryAF",
        "countryAL",
        "countryDZ",
        "countryAS",
        "countryAD",
        "countryAO",
        "countryAI",
        "countryAQ",
        "countryAG",
        "countryAR",
        "countryAM",
        "countryAW",
        "countryAU",
        "countryAT",
        "countryAZ",
        "countryBS",
        "countryBH",
        "countryBD",
        "countryBB",
        "countryBY",
        "countryBE",
        "countryBZ",
        "countryBJ",
        "countryBM",
        "countryBT",
        "countryBO",
        "countryBA",
        "countryBW",
        "countryBV",
        "countryBR",
        "countryIO",
        "countryBN",
        "countryBG",
        "countryBF",
        "countryBI",
        "countryKH",
        "countryCM",
        "countryCA",
        "countryCV",
        "countryKY",
        "countryCF",
        "countryTD",
        "countryCL",
        "countryCN",
        "countryCX",
        "countryCC",
        "countryCO",
        "countryKM",
        "countryCG",
        "countryCD",
        "countryCK",
        "countryCR",
        "countryCI",
        "countryHR",
        "countryCU",
        "countryCY",
        "countryCZ",
        "countryDK",
        "countryDJ",
        "countryDM",
        "countryDO",
        "countryTP",
        "countryEC",
        "countryEG",
        "countrySV",
        "countryGQ",
        "countryER",
        "countryEE",
        "countryET",
        "countryEU",
        "countryFK",
        "countryFO",
        "countryFJ",
        "countryFI",
        "countryFR",
        "countryFX",
        "countryGF",
        "countryPF",
        "countryTF",
        "countryGA",
        "countryGM",
        "countryGE",
        "countryDE",
        "countryGH",
        "countryGI",
        "countryGR",
        "countryGL",
        "countryGD",
        "countryGP",
        "countryGU",
        "countryGT",
        "countryGN",
        "countryGW",
        "countryGY",
        "countryHT",
        "countryHM",
        "countryVA",
        "countryHN",
        "countryHK",
        "countryHU",
        "countryIS",
        "countryIN",
        "countryID",
        "countryIR",
        "countryIQ",
        "countryIE",
        "countryIL",
        "countryIT",
        "countryJM",
        "countryJP",
        "countryJO",
        "countryKZ",
        "countryKE",
        "countryKI",
        "countryKP",
        "countryKR",
        "countryKW",
        "countryKG",
        "countryLA",
        "countryLV",
        "countryLB",
        "countryLS",
        "countryLR",
        "countryLY",
        "countryLI",
        "countryLT",
        "countryLU",
        "countryMO",
        "countryMK",
        "countryMG",
        "countryMW",
        "countryMY",
        "countryMV",
        "countryML",
        "countryMT",
        "countryMH",
        "countryMQ",
        "countryMR",
        "countryMU",
        "countryYT",
        "countryMX",
        "countryFM",
        "countryMD",
        "countryMC",
        "countryMN",
        "countryMS",
        "countryMA",
        "countryMZ",
        "countryMM",
        "countryNA",
        "countryNR",
        "countryNP",
        "countryNL",
        "countryAN",
        "countryNC",
        "countryNZ",
        "countryNI",
        "countryNE",
        "countryNG",
        "countryNU",
        "countryNF",
        "countryMP",
        "countryNO",
        "countryOM",
        "countryPK",
        "countryPW",
        "countryPS",
        "countryPA",
        "countryPG",
        "countryPY",
        "countryPE",
        "countryPH",
        "countryPN",
        "countryPL",
        "countryPT",
        "countryPR",
        "countryQA",
        "countryRE",
        "countryRO",
        "countryRU",
        "countryRW",
        "countrySH",
        "countryKN",
        "countryLC",
        "countryPM",
        "countryVC",
        "countryWS",
        "countrySM",
        "countryST",
        "countrySA",
        "countrySN",
        "countryCS",
        "countrySC",
        "countrySL",
        "countrySG",
        "countrySK",
        "countrySI",
        "countrySB",
        "countrySO",
        "countryZA",
        "countryGS",
        "countryES",
        "countryLK",
        "countrySD",
        "countrySR",
        "countrySJ",
        "countrySZ",
        "countrySE",
        "countryCH",
        "countrySY",
        "countryTW",
        "countryTJ",
        "countryTZ",
        "countryTH",
        "countryTG",
        "countryTK",
        "countryTO",
        "countryTT",
        "countryTN",
        "countryTR",
        "countryTM",
        "countryTC",
        "countryTV",
        "countryUG",
        "countryUA",
        "countryAE",
        "countryUK",
        "countryUS",
        "countryUM",
        "countryUY",
        "countryUZ",
        "countryVU",
        "countryVE",
        "countryVN",
        "countryVG",
        "countryVI",
        "countryWF",
        "countryEH",
        "countryYE",
        "countryYU",
        "countryZM",
        "countryZW",
    },
    gl={
        "ad",
        "ae",
        "af",
        "ag",
        "ai",
        "al",
        "am",
        "an",
        "ao",
        "aq",
        "ar",
        "as",
        "at",
        "au",
        "aw",
        "az",
        "ba",
        "bb",
        "bd",
        "be",
        "bf",
        "bg",
        "bh",
        "bi",
        "bj",
        "bm",
        "bn",
        "bo",
        "br",
        "bs",
        "bt",
        "bv",
        "bw",
        "by",
        "bz",
        "ca",
        "cc",
        "cd",
        "cf",
        "cg",
        "ch",
        "ci",
        "ck",
        "cl",
        "cm",
        "cn",
        "co",
        "cr",
        "cs",
        "cu",
        "cv",
        "cx",
        "cy",
        "cz",
        "de",
        "dj",
        "dk",
        "dm",
        "do",
        "dz",
        "ec",
        "ee",
        "eg",
        "eh",
        "er",
        "es",
        "et",
        "fi",
        "fj",
        "fk",
        "fm",
        "fo",
        "fr",
        "ga",
        "gd",
        "ge",
        "gf",
        "gh",
        "gi",
        "gl",
        "gm",
        "gn",
        "gp",
        "gq",
        "gr",
        "gs",
        "gt",
        "gu",
        "gw",
        "gy",
        "hk",
        "hm",
        "hn",
        "hr",
        "ht",
        "hu",
        "id",
        "ie",
        "il",
        "in",
        "io",
        "iq",
        "ir",
        "is",
        "it",
        "jm",
        "jo",
        "jp",
        "ke",
        "kg",
        "kh",
        "ki",
        "km",
        "kn",
        "kp",
        "kr",
        "kw",
        "ky",
        "kz",
        "la",
        "lb",
        "lc",
        "li",
        "lk",
        "lr",
        "ls",
        "lt",
        "lu",
        "lv",
        "ly",
        "ma",
        "mc",
        "md",
        "mg",
        "mh",
        "mk",
        "ml",
        "mm",
        "mn",
        "mo",
        "mp",
        "mq",
        "mr",
        "ms",
        "mt",
        "mu",
        "mv",
        "mw",
        "mx",
        "my",
        "mz",
        "na",
        "nc",
        "ne",
        "nf",
        "ng",
        "ni",
        "nl",
        "no",
        "np",
        "nr",
        "nu",
        "nz",
        "om",
        "pa",
        "pe",
        "pf",
        "pg",
        "ph",
        "pk",
        "pl",
        "pm",
        "pn",
        "pr",
        "ps",
        "pt",
        "pw",
        "py",
        "qa",
        "re",
        "ro",
        "ru",
        "rw",
        "sa",
        "sb",
        "sc",
        "sd",
        "se",
        "sg",
        "sh",
        "si",
        "sj",
        "sk",
        "sl",
        "sm",
        "sn",
        "so",
        "sr",
        "st",
        "sv",
        "sy",
        "sz",
        "tc",
        "td",
        "tf",
        "tg",
        "th",
        "tj",
        "tk",
        "tl",
        "tm",
        "tn",
        "to",
        "tr",
        "tt",
        "tv",
        "tw",
        "tz",
        "ua",
        "ug",
        "uk",
        "um",
        "us",
        "uy",
        "uz",
        "va",
        "vc",
        "ve",
        "vg",
        "vi",
        "vn",
        "vu",
        "wf",
        "ws",
        "ye",
        "yt",
        "za",
        "zm",
        "zw",
    },
    filter={0, 1},
    hl={
        "af",
        "sq",
        "sm",
        "ar",
        "az",
        "eu",
        "be",
        "bn",
        "bh",
        "bs",
        "bg",
        "ca",
        "zh-CN",
        "zh-TW",
        "hr",
        "cs",
        "da",
        "nl",
        "en",
        "eo",
        "et",
        "fo",
        "fi",
        "fr",
        "fy",
        "gl",
        "ka",
        "de",
        "el",
        "gu",
        "iw",
        "hi",
        "hu",
        "is",
        "id",
        "ia",
        "ga",
        "it",
        "ja",
        "jw",
        "kn",
        "ko",
        "la",
        "lv",
        "lt",
        "mk",
        "ms",
        "ml",
        "mt",
        "mr",
        "ne",
        "no",
        "nn",
        "oc",
        "fa",
        "pl",
        "pt-BR",
        "pt-PT",
        "pa",
        "ro",
        "ru",
        "gd",
        "sr",
        "si",
        "sk",
        "sl",
        "es",
        "su",
        "sw",
        "sv",
        "tl",
        "ta",
        "te",
        "th",
        "ti",
        "tr",
        "uk",
        "ur",
        "uz",
        "vi",
        "cy",
        "xh",
        "zu",
    },
    imgColorType={"color", "gray", "mono", "trans"},
    imgDominantColor={
        "black",
        "blue",
        "brown",
        "gray",
        "green",
        "orange",
        "pink",
        "purple",
        "red",
        "teal",
        "white",
        "yellow",
    },
    imgSize={
        "huge",
        "icon",
        "large",
        "medium",
        "small",
        "xlarge",
        "xxlarge",
    },
    imgType={"clipart", "face", "lineart", "stock", "photo", "animated"},
    lr={
        "lang_ar",
        "lang_bg",
        "lang_ca",
        "lang_zh-CN",
        "lang_zh-TW",
        "lang_hr",
        "lang_cs",
        "lang_da",
        "lang_nl",
        "lang_en",
        "lang_et",
        "lang_fi",
        "lang_fr",
        "lang_de",
        "lang_el",
        "lang_iw",
        "lang_hu",
        "lang_is",
        "lang_id",
        "lang_it",
        "lang_ja",
        "lang_ko",
        "lang_lv",
        "lang_lt",
        "lang_no",
        "lang_pl",
        "lang_pt",
        "lang_ro",
        "lang_ru",
        "lang_sr",
        "lang_sk",
        "lang_sl",
        "lang_es",
        "lang_sv",
        "lang_tr",
    },
    num={1, 2, 3, 4, 5, 6, 7, 8, 9, 10},
    rights={
        "cc_publicdomain",
        "cc_attribute",
        "cc_sharealike",
        "cc_noncommercial",
        "cc_nonderived",
    },
    safe={"active", "off"},
    searchType={None, "image"},
    siteSearchFilter={"e", "i"},
    start=range(1, 92),
)


##############################################################################
# YouTube variables
##############################################################################


YOUTUBE_TOPIC_IDS = {
    "Entertainment topics": {
        "Entertainment (parent topic)": "/m/02jjt",
        "Humor": "/m/09kqc",
        "Movies": "/m/02vxn",
        "Performing arts": "/m/05qjc",
        "Professional wrestling": "/m/066wd",
        "TV shows": "/m/0f2f9",
    },
    "Gaming topics": {
        "Action game": "/m/025zzc",
        "Action-adventure game": "/m/02ntfj",
        "Casual game": "/m/0b1vjn",
        "Gaming (parent topic)": "/m/0bzvm2",
        "Music video game": "/m/02hygl",
        "Puzzle video game": "/m/04q1x3q",
        "Racing video game": "/m/01sjng",
        "Role-playing video game": "/m/0403l3g",
        "Simulation video game": "/m/021bp2",
        "Sports game": "/m/022dc6",
        "Strategy video game": "/m/03hf_rm",
    },
    "Lifestyle topics": {
        "Fashion": "/m/032tl",
        "Fitness": "/m/027x7n",
        "Food": "/m/02wbm",
        "Hobby": "/m/03glg",
        "Lifestyle (parent topic)": "/m/019_rr",
        "Pets": "/m/068hy",
        "Physical attractiveness [Beauty]": "/m/041xxh",
        "Technology": "/m/07c1v",
        "Tourism": "/m/07bxq",
        "Vehicles": "/m/07yv9",
    },
    "Music topics": {
        "Christian music": "/m/02mscn",
        "Classical music": "/m/0ggq0m",
        "Country": "/m/01lyv",
        "Electronic music": "/m/02lkt",
        "Hip hop music": "/m/0glt670",
        "Independent music": "/m/05rwpb",
        "Jazz": "/m/03_d0",
        "Music (parent topic)": "/m/04rlf",
        "Music of Asia": "/m/028sqc",
        "Music of Latin America": "/m/0g293",
        "Pop music": "/m/064t9",
        "Reggae": "/m/06cqb",
        "Rhythm and blues": "/m/06j6l",
        "Rock music": "/m/06by7",
        "Soul music": "/m/0gywn",
    },
    "Other topics": {"Knowledge": "/m/01k8wb"},
    "Society topics": {
        "Business": "/m/09s1f",
        "Health": "/m/0kt51",
        "Military": "/m/01h6rj",
        "Politics": "/m/05qt0",
        "Religion": "/m/06bvp",
        "Society (parent topic)": "/m/098wr",
    },
    "Sports topics": {
        "American football": "/m/0jm_",
        "Baseball": "/m/018jz",
        "Basketball": "/m/018w8",
        "Boxing": "/m/01cgz",
        "Cricket": "/m/09xp_",
        "Football": "/m/02vx4",
        "Golf": "/m/037hz",
        "Ice hockey": "/m/03tmr",
        "Mixed martial arts": "/m/01h7lh",
        "Motorsport": "/m/0410tth",
        "Sports (parent topic)": "/m/06ntj",
        "Tennis": "/m/07bs0",
        "Volleyball": "/m/07_53",
    },
}

YOUTUBE_VID_CATEGORY_IDS = {
    "Action/Adventure": "32",
    "Anime/Animation": "31",
    "Autos & Vehicles": "2",
    "Classics": "33",
    "Comedy": "34",
    "Documentary": "35",
    "Drama": "36",
    "Education": "27",
    "Entertainment": "24",
    "Family": "37",
    "Film & Animation": "1",
    "Foreign": "38",
    "Gaming": "20",
    "Horror": "39",
    "Howto & Style": "26",
    "Movies": "30",
    "Music": "10",
    "News & Politics": "25",
    "Nonprofits & Activism": "29",
    "People & Blogs": "22",
    "Pets & Animals": "15",
    "Sci-Fi/Fantasy": "40",
    "Science & Technology": "28",
    "Short Movies": "18",
    "Shorts": "42",
    "Shows": "43",
    "Sports": "17",
    "Thriller": "41",
    "Trailers": "44",
    "Travel & Events": "19",
    "Videoblogging": "21",
}

SERP_YTUBE_VALID_VALS = dict(
    channelType={"any", "show"},
    eventType={"completed", "live", "upcoming"},
    forContentOwner={True, False, "true", "false"},
    forDeveloper={True, False, "true", "false"},
    forMine={True, False, "true", "false"},
    maxResults=range(51),
    order={"date", "rating", "relevance", "title", "videoCount", "viewCount"},
    regionCode={
        "ad",
        "ae",
        "af",
        "ag",
        "ai",
        "al",
        "am",
        "an",
        "ao",
        "aq",
        "ar",
        "as",
        "at",
        "au",
        "aw",
        "az",
        "ba",
        "bb",
        "bd",
        "be",
        "bf",
        "bg",
        "bh",
        "bi",
        "bj",
        "bm",
        "bn",
        "bo",
        "br",
        "bs",
        "bt",
        "bv",
        "bw",
        "by",
        "bz",
        "ca",
        "cc",
        "cd",
        "cf",
        "cg",
        "ch",
        "ci",
        "ck",
        "cl",
        "cm",
        "cn",
        "co",
        "cr",
        "cs",
        "cu",
        "cv",
        "cx",
        "cy",
        "cz",
        "de",
        "dj",
        "dk",
        "dm",
        "do",
        "dz",
        "ec",
        "ee",
        "eg",
        "eh",
        "er",
        "es",
        "et",
        "fi",
        "fj",
        "fk",
        "fm",
        "fo",
        "fr",
        "ga",
        "gd",
        "ge",
        "gf",
        "gh",
        "gi",
        "gl",
        "gm",
        "gn",
        "gp",
        "gq",
        "gr",
        "gs",
        "gt",
        "gu",
        "gw",
        "gy",
        "hk",
        "hm",
        "hn",
        "hr",
        "ht",
        "hu",
        "id",
        "ie",
        "il",
        "in",
        "io",
        "iq",
        "ir",
        "is",
        "it",
        "jm",
        "jo",
        "jp",
        "ke",
        "kg",
        "kh",
        "ki",
        "km",
        "kn",
        "kp",
        "kr",
        "kw",
        "ky",
        "kz",
        "la",
        "lb",
        "lc",
        "li",
        "lk",
        "lr",
        "ls",
        "lt",
        "lu",
        "lv",
        "ly",
        "ma",
        "mc",
        "md",
        "mg",
        "mh",
        "mk",
        "ml",
        "mm",
        "mn",
        "mo",
        "mp",
        "mq",
        "mr",
        "ms",
        "mt",
        "mu",
        "mv",
        "mw",
        "mx",
        "my",
        "mz",
        "na",
        "nc",
        "ne",
        "nf",
        "ng",
        "ni",
        "nl",
        "no",
        "np",
        "nr",
        "nu",
        "nz",
        "om",
        "pa",
        "pe",
        "pf",
        "pg",
        "ph",
        "pk",
        "pl",
        "pm",
        "pn",
        "pr",
        "ps",
        "pt",
        "pw",
        "py",
        "qa",
        "re",
        "ro",
        "ru",
        "rw",
        "sa",
        "sb",
        "sc",
        "sd",
        "se",
        "sg",
        "sh",
        "si",
        "sj",
        "sk",
        "sl",
        "sm",
        "sn",
        "so",
        "sr",
        "st",
        "sv",
        "sy",
        "sz",
        "tc",
        "td",
        "tf",
        "tg",
        "th",
        "tj",
        "tk",
        "tl",
        "tm",
        "tn",
        "to",
        "tr",
        "tt",
        "tv",
        "tw",
        "tz",
        "ua",
        "ug",
        "uk",
        "um",
        "us",
        "uy",
        "uz",
        "va",
        "vc",
        "ve",
        "vg",
        "vi",
        "vn",
        "vu",
        "wf",
        "ws",
        "ye",
        "yt",
        "za",
        "zm",
        "zw",
    },
    relevanceLanguage={
        "af",
        "sq",
        "sm",
        "ar",
        "az",
        "eu",
        "be",
        "bn",
        "bh",
        "bs",
        "bg",
        "ca",
        "zh-CN",
        "zh-TW",
        "zh-Hans",
        "zh-Hant",
        "hr",
        "cs",
        "da",
        "nl",
        "en",
        "eo",
        "et",
        "fo",
        "fi",
        "fr",
        "fy",
        "gl",
        "ka",
        "de",
        "el",
        "gu",
        "iw",
        "hi",
        "hu",
        "is",
        "id",
        "ia",
        "ga",
        "it",
        "ja",
        "jw",
        "kn",
        "ko",
        "la",
        "lv",
        "lt",
        "mk",
        "ms",
        "ml",
        "mt",
        "mr",
        "ne",
        "no",
        "nn",
        "oc",
        "fa",
        "pl",
        "pt-BR",
        "pt-PT",
        "pa",
        "ro",
        "ru",
        "gd",
        "sr",
        "si",
        "sk",
        "sl",
        "es",
        "su",
        "sw",
        "sv",
        "tl",
        "ta",
        "te",
        "th",
        "ti",
        "tr",
        "uk",
        "ur",
        "uz",
        "vi",
        "cy",
        "xh",
        "zu",
    },
    safeSearch={"moderate", "none", "strict"},
    topicId={
        "/m/04rlf",
        "/m/02mscn",
        "/m/0ggq0m",
        "/m/01lyv",
        "/m/02lkt",
        "/m/0glt670",
        "/m/05rwpb",
        "/m/03_d0",
        "/m/028sqc",
        "/m/0g293",
        "/m/064t9",
        "/m/06cqb",
        "/m/06j6l",
        "/m/06by7",
        "/m/0gywn",
        "/m/0bzvm2",
        "/m/025zzc",
        "/m/02ntfj",
        "/m/0b1vjn",
        "/m/02hygl",
        "/m/04q1x3q",
        "/m/01sjng",
        "/m/0403l3g",
        "/m/021bp2",
        "/m/022dc6",
        "/m/03hf_rm",
        "/m/06ntj",
        "/m/0jm_",
        "/m/018jz",
        "/m/018w8",
        "/m/01cgz",
        "/m/09xp_",
        "/m/02vx4",
        "/m/037hz",
        "/m/03tmr",
        "/m/01h7lh",
        "/m/0410tth",
        "/m/07bs0",
        "/m/07_53",
        "/m/02jjt",
        "/m/09kqc",
        "/m/02vxn",
        "/m/05qjc",
        "/m/066wd",
        "/m/0f2f9",
        "/m/019_rr",
        "/m/032tl",
        "/m/027x7n",
        "/m/02wbm",
        "/m/03glg",
        "/m/068hy",
        "/m/041xxh",
        "/m/07c1v",
        "/m/07bxq",
        "/m/07yv9",
        "/m/098wr",
        "/m/09s1f",
        "/m/0kt51",
        "/m/01h6rj",
        "/m/05qt0",
        "/m/06bvp",
        "/m/01k8wb",
    },
    type={"channel", "playlist", "video"},
    videoCaption={"any", "closedCaption", "none"},
    videoCategoryId={
        "1",
        "2",
        "10",
        "15",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
        "31",
        "32",
        "33",
        "34",
        "35",
        "36",
        "37",
        "38",
        "39",
        "40",
        "41",
        "42",
        "43",
        "44",
    },
    videoDefinition={"any", "high", "standard"},
    videoDimension={"2d", "3d", "any"},
    videoDuration={"any", "long", "medium", "short"},
    videoEmbeddable={"any", True, "true"},
    videoLicense={"any", "creativeCommon", "youtube"},
    videoSyndicated={"any", True, "true"},
    videoType={"any", "episode", "movie"},
)


def _split_by_comma(s, length=50):
    """Group a comma-separated string into a list of at-most
    ``length``-length words each."""
    str_split = s.split(",")
    str_list = []
    for i in range(0, len(str_split) + length, length):
        temp_str = ",".join(str_split[i : i + length])
        if temp_str:
            str_list.append(temp_str)
    return str_list


def youtube_video_details(key, vid_ids):
    """Return details of videos for which the ids are given.
    Assumes ``ids`` is a comma-separated list of video ids with
    no spaces.

    Parameters
    ----------
    key : str
      Your Google Developer key.
    vid_ids : str
      A comma-separated list of video ID's, with no spaces.

    Returns
    -------
    video_df : pandas.DataFrame
    """
    base_url = (
        "https://www.googleapis.com/youtube/v3/videos?part="
        "contentDetails,id,liveStreamingDetails,localizations,player,"
        "recordingDetails,snippet,statistics,status,topicDetails"
    )
    vid_ids = _split_by_comma(vid_ids, length=50)
    final_df = pd.DataFrame()
    for vid_id in vid_ids:
        params = {"id": vid_id, "key": key}
        logging.info(msg="Requesting: " + "video details")
        video_resp = requests.get(base_url, params=params)
        if video_resp.status_code >= 400:
            raise Exception(video_resp.json())
        items_df = pd.DataFrame(video_resp.json()["items"])
        details = ["snippet", "topicDetails", "statistics", "status", "contentDetails"]
        detail_df = pd.DataFrame()
        for detail in details:
            try:
                detail_df = pd.concat(
                    [
                        detail_df,
                        pd.DataFrame([x[detail] for x in video_resp.json()["items"]]),
                    ],
                    axis=1,
                )
            except KeyError:
                continue
        temp_df = pd.concat([items_df, detail_df], axis=1)
        final_df = pd.concat([final_df, temp_df], sort=False, ignore_index=True)
    return final_df


def youtube_channel_details(key, channel_ids):
    """Return details of channels for which the ids are given.
    Assumes ``ids`` is a comma-separated list of channel ids with
    no spaces.

    Parameters
    ----------
    key : str
      Your Google Developer key.
    channel_ids : str
      A comma-separated list of channel ID's, with no spaces.

    Returns
    -------
    channel_df : pandas.DataFrame
    """
    base_url = (
        "https://www.googleapis.com/youtube/v3/channels?part="
        "snippet,contentDetails,statistics"
    )
    channel_ids = _split_by_comma(channel_ids, length=50)
    final_df = pd.DataFrame()
    for channel_id in channel_ids:
        params = {"id": channel_id, "key": key}
        logging.info(msg="Requesting: " + "channel details")
        channel_resp = requests.get(base_url, params=params)
        if channel_resp.status_code >= 400:
            raise Exception(channel_resp.json())
        items_df = pd.DataFrame(channel_resp.json()["items"])
        details = ["snippet", "statistics", "contentDetails"]
        detail_df = pd.DataFrame()
        for detail in details:
            try:
                detail_df = pd.concat(
                    [
                        detail_df,
                        pd.DataFrame([x[detail] for x in channel_resp.json()["items"]]),
                    ],
                    axis=1,
                )
            except KeyError:
                continue
        temp_df = pd.concat([items_df, detail_df], axis=1)
        final_df = pd.concat([final_df, temp_df], sort=False, ignore_index=True)
    return final_df


def _dict_product(d):
    """Return the product of all values of a dict, while
    coupling each value with its key.
    This is used to generate multiple queries out of
        possibly multiple arguments in serp_goog.

    >>> d = {"a": [1], "b": [2, 3, 4], "c": [5, 6]}
    >>> _dict_product(d)
    >>> [{'a': 1, 'b': 2, 'c': 5},
         {'a': 1, 'b': 2, 'c': 6},
         {'a': 1, 'b': 3, 'c': 5},
         {'a': 1, 'b': 3, 'c': 6},
         {'a': 1, 'b': 4, 'c': 5},
         {'a': 1, 'b': 4, 'c': 6}]
    """
    items = list(d.items())
    keys = [x[0] for x in items]
    values = [x[1] for x in items]
    dicts = []
    for prod in product(*values):
        tempdict = dict(zip(keys, prod))
        dicts.append(tempdict)
    return dicts


def serp_goog(
    q,
    cx,
    key,
    c2coff=None,
    cr=None,
    dateRestrict=None,
    exactTerms=None,
    excludeTerms=None,
    fileType=None,
    filter=None,
    gl=None,
    highRange=None,
    hl=None,
    hq=None,
    imgColorType=None,
    imgDominantColor=None,
    imgSize=None,
    imgType=None,
    linkSite=None,
    lowRange=None,
    lr=None,
    num=None,
    orTerms=None,
    rights=None,
    safe=None,
    searchType=None,
    siteSearch=None,
    siteSearchFilter=None,
    sort=None,
    start=None,
):
    """Query Google's search API and get search results in a DataFrame.

    For each parameter, you can supply single or multiple values / arguments.
        If you pass multiple arguments, all the possible combinations of
        arguments (the product) will be requested, and you will get one
        DataFrame combining all queries. See examples below.

    Parameters
    ----------
    q : str
      The search expression.
    cx : str
      The custom search engine ID to use for this request.
    key : str
      The API key of your custom search engine.
    c2coff : str
      Enables or disables Simplified and Traditional Chinese Search. The default value
      for this parameter is 0 (zero), meaning that the feature is enabled. Supported
      values are:1: Disabled0: Enabled (default)
    cr : str
      Restricts search results to documents originating in a particular country. You may
      use Boolean operators in the cr parameter's value.Google Search determines the
      country of a document by analyzing:the top- level domain (TLD) of the document's
      URLthe geographic location of the Web server's IP addressSee the Country Parameter
      Values page for a list of valid values for this parameter.
    dateRestrict : str
      Restricts results to URLs based on date.

      Supported values include:
        - d[number]: requests results from the specified number of past days.
        - w[number]: requests results from the specified number of past weeks.
        - m[number]: requests results from the specified number of past months.
        - y[number]: requests results from the specified number of past years.
    exactTerms : str
      Identifies a phrase that all documents in the search results must contain.
    excludeTerms : str
      Identifies a word or phrase that should not appear in any documents in the search
      results.
    fileType : str
      Restricts results to files of a specified extension. A list of file types
      indexable by Google can be found in Search Console Help Center.
    filter : str
      Controls turning on or off the duplicate content filter.See Automatic Filtering
      for more information about Google's search results filters. Note that host
      crowding filtering applies only to multi-site searches.By default, Google applies
      filtering to all search results to improve the quality of those results.
      Acceptable values are:  "0": Turns off duplicate content filter.  "1": Turns on
      duplicate content filter.
    gl : str
      Geolocation of end user. The gl parameter value is a two-letter country code. The
      gl parameter boosts search results whose country of origin matches the parameter
      value. See the Country Codes page for a list of valid values.Specifying a gl
      parameter value should lead to more relevant results. This is particularly true
      for international customers and, even more specifically, for customers in
      English- speaking countries other than the United States.
    highRange : str
      Specifies the ending value for a search range.Use lowRange and highRange to append
      an inclusive search range of lowRange...highRange to the query.
    hl : str
      Sets the user interface language. Explicitly setting this parameter improves the
      performance and the quality of your search results.See the Interface Languages
      section of Internationalizing Queries and Results Presentation for more
      information, and Supported Interface Languages for a list of supported languages.
    hq : str
      Appends the specified query terms to the query, as if they were combined with a
      logical AND operator.
    imgColorType : str
      Returns black and white, grayscale, or color images: mono, gray, and color.
      Acceptable values are:  "color": color  "gray": gray  "mono": mono
    imgDominantColor : str
      Returns images of a specific dominant color.  Acceptable values are:
      "black": black "blue": blue  "brown": brown  "gray": gray  "green": green
      "orange": orange  "pink": pink  "purple": purple  "red": red "teal": teal
      "white": white  "yellow": yellow
    imgSize : str
      Returns images of a specified size. Acceptable values are:  "huge": huge
      "icon": icon  "large": large  "medium": medium  "small": small  "xlarge": xlarge
      "xxlarge": xxlarge
    imgType : str
      Returns images of a type.  Acceptable values are:  "clipart": clipart
      "face": face  "lineart": lineart  "news": news  "photo": photo
    linkSite : str
      Specifies that all search results should contain a link to a particular URL
    lowRange : str
      Specifies the starting value for a search range. Use lowRange and highRange to
      append an inclusive search range of lowRange...highRange to the query.
    lr : str
      Restricts the search to documents written in a particular language
      (e.g., lr=lang_ja).  Acceptable values are:  "lang_ar": Arabic
      "lang_bg": Bulgarian  "lang_ca": Catalan  "lang_cs": Czech  "lang_da": Danish
      "lang_de": German  "lang_el": Greek  "lang_en": English  "lang_es": Spanish
      "lang_et": Estonian  "lang_fi": Finnish  "lang_fr": French  "lang_hr": Croatian
      "lang_hu": Hungarian "lang_id": Indonesian  "lang_is": Icelandic
      "lang_it": Italian  "lang_iw": Hebrew  "lang_ja": Japanese  "lang_ko": Korean
      "lang_lt": Lithuanian  "lang_lv": Latvian "lang_nl": Dutch  "lang_no": Norwegian
      "lang_pl": Polish "lang_pt": Portuguese  "lang_ro": Romanian  "lang_ru": Russian
      "lang_sk": Slovak  "lang_sl": Slovenian  "lang_sr": Serbian  "lang_sv": Swedish
      "lang_tr": Turkish  "lang_zh- CN": Chinese (Simplified)  "lang_zh-TW":
      Chinese (Traditional)
    num : int
      Number of search results to return.Valid values are integers between 1 and 10,
      inclusive.
    orTerms : str
      Provides additional search terms to check for in a document, where each document
      in the search results must contain at least one of the additional search terms.
    rights : str
      Filters based on licensing. Supported values include: cc_publicdomain,
      cc_attribute, cc_sharealike, cc_noncommercial, cc_nonderived, and combinations of
      these.
    safe : str
      Search safety level.  Acceptable values are:  "active": Enables SafeSearch
      filtering.  "off":Disables SafeSearch filtering.  (default)
    searchType : str
      Specifies the search type: image. If unspecified, results are limited to webpages.
      Acceptable values are:  "image": custom image search.
    siteSearch : str
      Specifies all search results should be pages from a given site.
    siteSearchFilter : str
      Controls whether to include or exclude results from the site named in the
      siteSearch parameter.  Acceptable values are:  "e": exclude  "i": include
    sort : str
      The sort expression to apply to the results.
    start : int
      The index of the first result to return.Valid value are integers starting 1
      (default) and the second result is 2 and so forth. For example &start=11 gives the
      second page of results with the default "num" value of 10 results per page.Note:
      No more than 100 results will ever be returned for any query with JSON API, even
      if more than 100 documents match the query, so setting (start + num) to more than
      100 will produce an error. Note that the maximum value for num is 10.

    Returns
    -------
    serp_df : pandas.DataFrame

    Examples
    --------
    The following function call will produce two queries:
    "hotel" in the USA, and "hotel" in France

    >>> serp_goog(q="hotel", gl=["us", "fr"], cx="YOUR_CX", key="YOUR_KEY")

    The below function call will prouce four queries and make four requests:

    * "fligts" in UK
    * "fligts" in Australia
    * "tickets" in UK
    * "tickets" in Australia

    'cr' here refers to 'country restrict', which focuses on content
    originating from the specified country.

    >>> serp_goog(q=['flights', 'tickets'], cr=['countryUK', 'countryAU'],
                  cx='YOUR_CX', key='YOUR_KEY')
    """
    params = locals()
    supplied_params = {k: v for k, v in params.items() if params[k] is not None}

    for p in supplied_params:
        if isinstance(supplied_params[p], (str, int)):
            supplied_params[p] = [supplied_params[p]]

    for p in supplied_params:
        if p in SERP_GOOG_VALID_VALS:
            if not set(supplied_params[p]).issubset(SERP_GOOG_VALID_VALS[p]):
                raise ValueError(
                    "Please make sure you provide a"
                    ' valid value for "{}", valid values:\n'
                    "{}".format(p, sorted(SERP_GOOG_VALID_VALS[p]))
                )
    params_list = _dict_product(supplied_params)
    base_url = "https://www.googleapis.com/customsearch/v1?"
    specified_cols = [
        "searchTerms",
        "rank",
        "title",
        "snippet",
        "displayLink",
        "link",
        "queryTime",
        "totalResults",
    ]
    responses = []
    for param in params_list:
        param_log = ", ".join([k + "=" + str(v) for k, v in param.items()])
        logging.info(msg="Requesting: " + param_log)
        resp = requests.get(base_url, params=param)
        if resp.status_code >= 400:
            raise Exception(resp.json())
        responses.append(resp)
    result_df = pd.DataFrame()
    for i, resp in enumerate(responses):
        request_metadata = resp.json()["queries"]["request"][0]
        del request_metadata["title"]
        search_info = resp.json()["searchInformation"]
        if int(search_info["totalResults"]) == 0:
            df = pd.DataFrame(columns=specified_cols, index=range(1))
            df["searchTerms"] = request_metadata["searchTerms"]
            # These keys don't appear in the response so they have to be
            # added manually
            for missing in ["lr", "num", "start", "c2coff"]:
                if missing in params_list[i]:
                    df[missing] = params_list[i][missing]
        else:
            df = pd.DataFrame(resp.json()["items"])
            df["cseName"] = resp.json()["context"]["title"]
            start_idx = request_metadata["startIndex"]
            df["rank"] = range(start_idx, start_idx + len(df))
            for missing in ["lr", "num", "start", "c2coff"]:
                if missing in params_list[i]:
                    df[missing] = params_list[i][missing]
        meta_columns = {**request_metadata, **search_info}
        df = df.assign(**meta_columns)
        df["queryTime"] = datetime.datetime.now(tz=datetime.timezone.utc)
        df["queryTime"] = pd.to_datetime(df["queryTime"])
        if "image" in df:
            img_df = json_normalize(df["image"])
            img_df.columns = ["image." + c for c in img_df.columns]
            df = pd.concat([df, img_df], axis=1)
        result_df = pd.concat([result_df, df], sort=False, ignore_index=True)
    ordered_cols = (
        list(set(params_list[i]).difference({"q", "key", "cx"})) + specified_cols
    )
    non_ordered = result_df.columns.difference(set(ordered_cols))
    final_df = result_df[ordered_cols + list(non_ordered)]
    if "pagemap" in final_df:
        pagemap_df = pd.DataFrame()
        for p in final_df["pagemap"]:
            try:
                temp_pagemap_df = json_normalize(p)
                pagemap_df = pd.concat([pagemap_df, temp_pagemap_df], sort=False)
            except Exception:
                temp_pagemap_df = pd.DataFrame({"delete_me": None}, index=range(1))
                pagemap_df = pd.concat([pagemap_df, temp_pagemap_df], sort=False)
        pagemap_df = pagemap_df.reset_index(drop=True)
        if "delete_me" in pagemap_df:
            del pagemap_df["delete_me"]
        for col in pagemap_df:
            if col in final_df:
                pagemap_df = pagemap_df.rename(columns={col: "pagemap_" + col})
        final_df = pd.concat([final_df, pagemap_df], axis=1)

        if "metatags" in pagemap_df:
            metatag_df = pd.DataFrame()
            for m in pagemap_df["metatags"]:
                try:
                    temp_metatags_df = json_normalize(m)
                    metatag_df = pd.concat([metatag_df, temp_metatags_df], sort=False)
                except Exception:
                    temp_metatags_df = pd.DataFrame({"delete_me": None}, index=range(1))
                    metatag_df = pd.concat([metatag_df, temp_metatags_df], sort=False)
            metatag_df = metatag_df.reset_index(drop=True)
            if "delete_me" in metatag_df:
                del metatag_df["delete_me"]
            for col in metatag_df:
                if col in final_df:
                    metatag_df = metatag_df.rename(columns={col: "metatag_" + col})

            final_df = pd.concat([final_df, metatag_df], axis=1)
    return final_df


def serp_youtube(
    key,
    q=None,
    channelId=None,
    channelType=None,
    eventType=None,
    forContentOwner=None,
    forDeveloper=None,
    forMine=None,
    location=None,
    locationRadius=None,
    maxResults=None,
    onBehalfOfContentOwner=None,
    order=None,
    pageToken=None,
    publishedAfter=None,
    publishedBefore=None,
    regionCode=None,
    relatedToVideoId=None,
    relevanceLanguage=None,
    safeSearch=None,
    topicId=None,
    type=None,
    videoCaption=None,
    videoCategoryId=None,
    videoDefinition=None,
    videoDimension=None,
    videoDuration=None,
    videoEmbeddable=None,
    videoLicense=None,
    videoSyndicated=None,
    videoType=None,
):
    """Query the YouTube API and get search results in a DataFrame.

    For each parameter you can supply a single or multiple value(s).
    Looping and merging results is handled automatically in case of multiple
    values.

    Parameters
    ----------
    q : str
      The ``q`` parameter specifies the query term to search for. Your request can also
      use the Boolean NOT (-) and OR (|) operators to exclude videos or to find videos
      that are associated with one of several search terms. For example, to search for
      videos matching either "boating" or "sailing", set the ``q`` parameter value to
      boating|sailing. Similarly, to search for videos matching either "boating" or
      "sailing" but not "fishing", set the q parameter value to
      boating|sailing -fishing. Note that the pipe character must be URL- escaped when
      it is sent in your API request. The URL-escaped value for the pipe character is
      %7C.
    channelId : str
      The ``channelId`` parameter indicates that the API response should only contain
      resources created by the channel. Note: Search results are constrained to a
      maximum of 500 videos if your request specifies a value for the ``channelId``
      parameter and sets the ``type`` parameter value to video, but it does not also set
      one of the ``forContentOwner``, ``forDeveloper``, or ``forMine`` filters.
    channelType : str
      The ``channelType`` parameter lets you restrict a search to a particular type of
      channel. Acceptable values are:

        any - Return all channels.

        show - Only retrieve shows.
    eventType : str
      The ``eventType`` parameter restricts a search to broadcast events. If you specify
      a value for this parameter, you must also set the type parameter's value to video.
      Acceptable values are:

        completed - Only include completed broadcasts.

        live - Only include active broadcasts.

        upcoming - Only include upcoming broadcasts.

    forContentOwner : bool
      This parameter can only be used in a properly authorized request, and it is
      intended exclusively for YouTube content partners. The ``forContentOwner``
      parameter restricts the search to only retrieve videos owned by the content owner
      identified by the ``onBehalfOfContentOwner`` parameter. If ``forContentOwner`` is
      set to true, the request must also meet these requirements: The
      ``onBehalfOfContentOwner`` parameter is required.The user authorizing the request
      must be using an account linked to the specified content owner. The ``type``
      parameter value must be set to video.None of the following other parameters can be
      set: ``videoDefinition``, ``videoDimension``, ``videoDuration``, ``videoLicense``,
      ``videoEmbeddable``, ``videoSyndicated``, ``videoType``.
    forDeveloper : bool
      This parameter can only be used in a properly authorized request. The
      ``forDeveloper`` parameter restricts the search to only retrieve videos uploaded
      via the developer's application or website. The API server uses the request's
      authorization credentials to identify the developer. The ``forDeveloper``
      parameter can be used in conjunction with optional search parameters like the
      ``q`` parameter. For this feature, each uploaded video is automatically tagged
      with the project number that is associated with the developer's application in the
      Google Developers Console. When a search request subsequently sets the
      ``forDeveloper`` parameter to ``true`` the API server uses the request's
      authorization credentials to identify the developer. Therefore, a developer can
      restrict results to videos uploaded through the developer's own app or website but
      not to videos uploaded through other apps or sites.
    forMine : bool
      This parameter can only be used in a properly authorized request. The ``forMine``
      parameter restricts the search to only retrieve videos owned by the authenticated
      user. If you set this parameter to ``true``, then the ``type`` parameter's value
      must also be set to ``video``. In addition, none of the following other parameters
      can be set in the same request: ``videoDefinition``, ``videoDimension``,
      ``videoDuration``, ``videoLicense``, ``videoEmbeddable``, ``videoSyndicated``,
      ``videoType``.
    relatedToVideoId: str
      The ``relatedToVideoId`` parameter retrieves a list of videos that are related to
      the video that the parameter ``value`` identifies. The parameter ``value`` must be
      set to a YouTube video ID and, if you are using this parameter, the ``type``
      parameter must be set to video.Note that if the ``relatedToVideoId`` parameter is
      set, the only other supported parameters are ``part``, ``maxResults``,
      ``pageToken``, ``regionCode``, ``relevanceLanguage``, ``safeSearch``, ``type``
      (which must be set to video), and ``fields``.
    location : str
      The ``location`` parameter, in conjunction with the ``locationRadius`` parameter,
      defines a circular geographic area and also restricts a search to videos that
      specify, in their metadata, a geographic location that falls within that area. The
      parameter value is a string that specifies latitude/longitude coordinates e.g.
      (37.42307,-122.08427).The location parameter value identifies the point at the
      center of the area. The ``locationRadius`` parameter specifies the maximum
      distance that the location associated with a video can be from that point for the
      video to still be included in the search results. The API returns an error if your
      request specifies a value for the ``location`` parameter but does not also specify
      a value for the ``locationRadius`` parameter.
    locationRadius : str
      The ``locationRadius`` parameter, in conjunction with the ``location`` parameter,
      defines a circular geographic area. The parameter value must be a floating point
      number followed by a measurement unit. Valid measurement units are m, km, ft, and
      mi. For example, valid parameter values include 1500m, 5km, 10000ft, and 0.75mi.
      The API does not support ``locationRadius`` parameter values larger than 1000
      kilometers. Note: See the definition of the ``location`` parameter for more
      information.
    maxResults : int
      The ``maxResults`` parameter specifies the maximum number of items that should be
      returned in the result set. Acceptable values are 0 to 50, inclusive. The default
      value is 5.
    onBehalfOfContentOwner : str
      This parameter can only be used in a properly authorized request. Note: This
      parameter is intended exclusively for YouTube content partners.The
      ``onBehalfOfContentOwner`` parameter indicates that the request's authorization
      credentials identify a YouTube CMS user who is acting on behalf of the content
      owner specified in the parameter value. This parameter is intended for YouTube
      content partners that own and manage many different YouTube channels. It allows
      content owners to authenticate once and get access to all their video and channel
      data, without having to provide authentication credentials for each individual
      channel. The CMS account that the user authenticates with must be linked to the
      specified YouTube content owner.
    order : str
      The order parameter specifies the method that will be used to order resources in
      the API response. The default value is relevance. Acceptable values are:

        date - Resources are sorted in reverse chronological order based on the
        date they were created.

        rating - Resources are sorted from highest to lowest rating.

        relevance - Resources are sorted based on their relevance to the search
        query. This is the default value for this parameter.

        title - Resources are sorted alphabetically by title.

        videoCount - Channels are sorted in descending order of their number of
        uploaded videos.

        viewCount - Resources sorted from highest to lowest number of views.

        For live broadcasts, videos are sorted by number of concurrent viewers
        while the broadcasts are ongoing.
    pageToken : str
      The ``pageToken`` parameter identifies a specific page in the result set that
      should be returned. In an API response, the ``nextPageToken`` and
      ``prevPageToken`` properties identify other pages that could be retrieved.
    publishedAfter : datetime
      The ``publishedAfter`` parameter indicates that the API response should only
      contain resources created at or after the specified time. The value is an RFC 3339
      formatted date-time value (1970-01-01T00:00:00Z).
    publishedBefore : datetime
      The ``publishedBefore`` parameter indicates that the API response should only
      contain resources created before or at the specified time. The value is an RFC
      3339 formatted date-time value (1970-01-01T00:00:00Z).
    regionCode : str
      The ``regionCode`` parameter instructs the API to return search results for videos
      that can be viewed in the specified country. The parameter value is an ISO 3166-1
      alpha-2 country code.
    relevanceLanguage : str
      The ``relevanceLanguage`` parameter instructs the API to return search results
      that are most relevant to the specified language. The parameter value is typically
      an ISO 639-1 two-letter language code. However, you should use the values zh-Hans
      for simplified Chinese and zh-Hant for traditional Chinese. Please note that
      results in other languages will still be returned if they are highly relevant to
      the search query term.
    safeSearch : str
      The ``safeSearch`` parameter indicates whether the search results should include
      restricted content as well as standard content. Acceptable values are:

        moderate - YouTube will filter some content from search results and,
        at the least, will filter content that is restricted in your locale.
        Based on their content, search results could be removed from search
        results or demoted in search results. This is the default parameter
        value.

        none - YouTube will not filter the search result set.

        strict - YouTube will try to exclude all restricted content from the
        search result set.

        Based on their content, search results
        could be removed from search results or demoted in search
        results.
    topicId : str
      The ``topicId`` parameter indicates that the API response should only contain
      resources associated with the specified topic. The value identifies a Freebase
      topic ID.
    type : str
      The ``type`` parameter restricts a search query to only retrieve a particular type
      of resource. The value is a comma-separated list of resource types. The default
      value is video,channel,playlist. Acceptable values are: channel, playlist, and
      video.
    videoCaption : str
      The ``videoCaption`` parameter indicates whether the API should filter video
      search results based on whether they have captions. If you specify a value for
      this parameter, you must also set the ``type`` parameter's value to video.
      Acceptable values are:

        any - Do not filter results based on caption availability.

        closedCaption - Only include videos that have captions.

        none - Only include videos that do not have captions.
    videoCategoryId : str
      The ``videoCategoryId`` parameter filters video search results based on their
      category. If you specify a value for this parameter, you must also set the
      ``type`` parameter's value to video.
    videoDefinition : str
      The ``videoDefinition`` parameter lets you restrict a search to only include
      either high definition (HD) or standard definition (SD) videos. HD videos are
      available for playback in at least 720p, though higher resolutions, like 1080p,
      might also be available. If you specify a value for this parameter, you must also
      set the ``type`` parameter's value to video. Acceptable values are:

        any - Return all videos, regardless of their resolution.

        high - Only retrieve HD videos.

        standard - Only retrieve videos in standard definition.
    videoDimension : str
      The ``videoDimension`` parameter lets you restrict a search to only retrieve 2D or
      3D videos. If you specify a value for this parameter, you must also set the
      ``type`` parameter's value to video. Acceptable values are:

        2d - Restrict search results to exclude 3D videos.

        3d - Restrict search results to only include 3D videos.

        any - Include both 3D and non-3D videos in returned results. This is the default
        value.
    videoDuration : str
      The ``videoDuration`` parameter filters video search results based on their
      duration. If you specify a value for this parameter, you must also set the
      ``type`` parameter's value to video. Acceptable values are:

        any - Do not filter video search results based on their duration.
        This is the default value.

        long - Only include videos longer than 20 minutes.

        medium - Only include videos that are between four and 20 minutes
        long (inclusive).

        short - Only include videos that are less than four minutes long.
    videoEmbeddable : str
      The ``videoEmbeddable`` parameter lets you to restrict a search to only videos
      that can be embedded into a webpage. If you specify a value for this parameter,
      you must also set the ``type`` parameter's value to video. Acceptable values are:

        any - Return all videos, embeddable or not.

        true - Only retrieve embeddable videos.
    videoLicense : str
      The ``videoLicense`` parameter filters search results to only include videos with
      a particular license. YouTube lets video uploaders choose to attach either the
      Creative Commons license or the standard YouTube license to each of their videos.
      If you specify a value for this parameter, you must also set the ``type``
      parameter's value to video. Acceptable values are:

        any - Return all videos, regardless of which license they have,
        that match the query parameters.

        creativeCommon - Only return videos that have a Creative Commons
        license.
        Users can reuse videos with this license in other videos that they
        create.

        youtube - Only return videos that have the standard YouTube license.
    videoSyndicated : str
      The ``videoSyndicated`` parameter lets you to restrict a search to only videos
      that can be played outside youtube.com. If you specify a value for this parameter,
      you must also set the ``type`` parameter's value to video. Acceptable values are:

        any - Return all videos, syndicated or not.

        true - Only retrieve syndicated videos.
    videoType : str
      The ``videoType`` parameter lets you restrict a search to a particular type of
      videos. If you specify a value for this parameter, you must also set the ``type``
      parameter's value to video. Acceptable values are:

        any - Return all videos.

        episode - Only retrieve episodes of shows.

        movie - Only retrieve movies.
    Returns
    -------
    serp_df : pandas.DataFrame
    """
    params = locals()
    supplied_params = {k: v for k, v in params.items() if params[k]}

    type_vid_params = {
        "eventType",
        "relatedToVideoId",
        "videoCaption",
        "videoCategoryId",
        "videoDefinition",
        "videoDimension",
        "videoDuration",
        "videoEmbeddable",
        "videoLicense",
        "videoSyndicated",
        "videoType",
        "forMine",
        "forContentOwner",
    }

    if supplied_params.get("type") != "video" and type_vid_params.intersection(
        set(supplied_params.keys())
    ):
        raise ValueError(
            'You need to set type="video" if you want to set'
            " any of the following:" + str(type_vid_params)
        )

    for p in supplied_params:
        if isinstance(supplied_params[p], (str, int)):
            supplied_params[p] = [supplied_params[p]]

    for p in supplied_params:
        if p in SERP_YTUBE_VALID_VALS:
            if not set(supplied_params[p]).issubset(SERP_YTUBE_VALID_VALS[p]):
                raise ValueError(
                    "Please make sure you provide a"
                    ' valid value for "{}", valid values:\n{}'.format(
                        p, sorted([str(x) for x in SERP_YTUBE_VALID_VALS[p]])
                    )
                )

    params_list = _dict_product(supplied_params)
    base_url = "https://www.googleapis.com/youtube/v3/search?part=snippet"

    responses = []
    for param in params_list:
        param_log = ", ".join([k + "=" + str(v) for k, v in param.items()])
        logging.info(msg="Requesting: " + param_log)
        resp = requests.get(base_url, params=param)
        if resp.status_code >= 400:
            raise Exception(resp.json())
        responses.append(resp)

    result_df = pd.DataFrame()
    for i, resp in enumerate(responses):
        snippet_df = pd.DataFrame([x["snippet"] for x in resp.json()["items"]])
        id_df = pd.DataFrame([x["id"] for x in resp.json()["items"]])
        if "channelId" in id_df:
            id_df = id_df.drop("channelId", axis=1)

        if "thumbnails" in snippet_df:
            thumb_df = json_normalize(snippet_df["thumbnails"])
        else:
            thumb_df = pd.DataFrame()
        page_info = resp.json()["pageInfo"]
        temp_df = pd.concat([snippet_df, id_df, thumb_df], axis=1).assign(**page_info)
        temp_df["rank"] = range(1, len(temp_df) + 1)

        if len(temp_df) == 0:
            empty_df_cols = [
                "title",
                "description",
                "publishedAt",
                "channelTitle",
                "kind",
                "videoId",
                "channelId",
            ]
            temp_df = temp_df.assign(q=[params_list[i]["q"]])
            temp_df = temp_df.assign(**dict.fromkeys(empty_df_cols))

            temp_df = temp_df.assign(**page_info)
        del params_list[i]["key"]
        temp_df = temp_df.assign(**params_list[i])
        temp_df["nextPageToken"] = resp.json().get("nextPageToken")
        result_df = pd.concat([result_df, temp_df], sort=False, ignore_index=True)

    result_df["queryTime"] = datetime.datetime.now(tz=datetime.timezone.utc)
    result_df["queryTime"] = pd.to_datetime(result_df["queryTime"])

    specified_cols = [
        "queryTime",
        "rank",
        "title",
        "description",
        "publishedAt",
        "channelTitle",
        "totalResults",
        "kind",
    ]
    ordered_cols = list(params_list[i].keys()) + specified_cols
    non_ordered = result_df.columns.difference(set(ordered_cols))
    final_df = result_df[ordered_cols + list(non_ordered)]

    vid_ids = ",".join(final_df["videoId"].dropna())
    if vid_ids:
        vid_details_df = youtube_video_details(vid_ids=vid_ids, key=key)
        vid_details_df.columns = ["video." + x for x in vid_details_df.columns]
        final_df = pd.merge(
            final_df, vid_details_df, how="left", left_on="videoId", right_on="video.id"
        )

    channel_ids = ",".join(final_df["channelId"].dropna())
    if channel_ids:
        channel_details_df = youtube_channel_details(channel_ids=channel_ids, key=key)
        channel_details_df.columns = [
            "channel." + x for x in channel_details_df.columns
        ]

        final_df = pd.merge(
            final_df,
            channel_details_df,
            how="left",
            left_on="channelId",
            right_on="channel.id",
        )
    final_df = final_df.drop_duplicates(subset=["videoId"])
    return final_df.reset_index(drop=True)


def set_logging_level(level_or_name):
    """Change the logging level during the session.
    Acceptable values are [0, 10, 20, 30, 40, 50,
    'NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR',
    'CRITICAL']
    """
    lvl_names_values = [
        0,
        10,
        20,
        30,
        40,
        50,
        "NOTSET",
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ]
    if level_or_name not in lvl_names_values:
        raise ValueError(
            "Please make sure you supply" " a value from: {}".format(lvl_names_values)
        )
    logging.getLogger().setLevel(level_or_name)


logging.getLogger().setLevel("INFO")
