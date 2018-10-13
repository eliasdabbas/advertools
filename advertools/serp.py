import datetime
import logging
from itertools import product

import pandas as pd
from pandas.io.json import json_normalize
import requests

LOG_FMT = '%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s'
logging.basicConfig(format=LOG_FMT)


VALID_VALUES = dict(
    fileType={
        'bas', 'c', 'cc', 'cpp', 'cs', 'cxx', 'doc', 'docx', 'dwf', 'gpx',
        'h', 'hpp', 'htm', 'html', 'hwp', 'java', 'kml', 'kmz', 'odp', 'ods',
        'odt', 'pdf', 'pl', 'ppt', 'pptx', 'ps', 'py', 'rtf', 'svg', 'swf',
        'tex', 'text', 'txt', 'wap', 'wml', 'xls', 'xlsx', 'xml',
    },

    c2coff={0, 1},

    cr={
        'countryAF', 'countryAL', 'countryDZ', 'countryAS', 'countryAD',
        'countryAO', 'countryAI', 'countryAQ', 'countryAG', 'countryAR',
        'countryAM', 'countryAW', 'countryAU', 'countryAT', 'countryAZ',
        'countryBS', 'countryBH', 'countryBD', 'countryBB', 'countryBY',
        'countryBE', 'countryBZ', 'countryBJ', 'countryBM', 'countryBT',
        'countryBO', 'countryBA', 'countryBW', 'countryBV', 'countryBR',
        'countryIO', 'countryBN', 'countryBG', 'countryBF', 'countryBI',
        'countryKH', 'countryCM', 'countryCA', 'countryCV', 'countryKY',
        'countryCF', 'countryTD', 'countryCL', 'countryCN', 'countryCX',
        'countryCC', 'countryCO', 'countryKM', 'countryCG', 'countryCD',
        'countryCK', 'countryCR', 'countryCI', 'countryHR', 'countryCU',
        'countryCY', 'countryCZ', 'countryDK', 'countryDJ', 'countryDM',
        'countryDO', 'countryTP', 'countryEC', 'countryEG', 'countrySV',
        'countryGQ', 'countryER', 'countryEE', 'countryET', 'countryEU',
        'countryFK', 'countryFO', 'countryFJ', 'countryFI', 'countryFR',
        'countryFX', 'countryGF', 'countryPF', 'countryTF', 'countryGA',
        'countryGM', 'countryGE', 'countryDE', 'countryGH', 'countryGI',
        'countryGR', 'countryGL', 'countryGD', 'countryGP', 'countryGU',
        'countryGT', 'countryGN', 'countryGW', 'countryGY', 'countryHT',
        'countryHM', 'countryVA', 'countryHN', 'countryHK', 'countryHU',
        'countryIS', 'countryIN', 'countryID', 'countryIR', 'countryIQ',
        'countryIE', 'countryIL', 'countryIT', 'countryJM', 'countryJP',
        'countryJO', 'countryKZ', 'countryKE', 'countryKI', 'countryKP',
        'countryKR', 'countryKW', 'countryKG', 'countryLA', 'countryLV',
        'countryLB', 'countryLS', 'countryLR', 'countryLY', 'countryLI',
        'countryLT', 'countryLU', 'countryMO', 'countryMK', 'countryMG',
        'countryMW', 'countryMY', 'countryMV', 'countryML', 'countryMT',
        'countryMH', 'countryMQ', 'countryMR', 'countryMU', 'countryYT',
        'countryMX', 'countryFM', 'countryMD', 'countryMC', 'countryMN',
        'countryMS', 'countryMA', 'countryMZ', 'countryMM', 'countryNA',
        'countryNR', 'countryNP', 'countryNL', 'countryAN', 'countryNC',
        'countryNZ', 'countryNI', 'countryNE', 'countryNG', 'countryNU',
        'countryNF', 'countryMP', 'countryNO', 'countryOM', 'countryPK',
        'countryPW', 'countryPS', 'countryPA', 'countryPG', 'countryPY',
        'countryPE', 'countryPH', 'countryPN', 'countryPL', 'countryPT',
        'countryPR', 'countryQA', 'countryRE', 'countryRO', 'countryRU',
        'countryRW', 'countrySH', 'countryKN', 'countryLC', 'countryPM',
        'countryVC', 'countryWS', 'countrySM', 'countryST', 'countrySA',
        'countrySN', 'countryCS', 'countrySC', 'countrySL', 'countrySG',
        'countrySK', 'countrySI', 'countrySB', 'countrySO', 'countryZA',
        'countryGS', 'countryES', 'countryLK', 'countrySD', 'countrySR',
        'countrySJ', 'countrySZ', 'countrySE', 'countryCH', 'countrySY',
        'countryTW', 'countryTJ', 'countryTZ', 'countryTH', 'countryTG',
        'countryTK', 'countryTO', 'countryTT', 'countryTN', 'countryTR',
        'countryTM', 'countryTC', 'countryTV', 'countryUG', 'countryUA',
        'countryAE', 'countryUK', 'countryUS', 'countryUM', 'countryUY',
        'countryUZ', 'countryVU', 'countryVE', 'countryVN', 'countryVG',
        'countryVI', 'countryWF', 'countryEH', 'countryYE', 'countryYU',
        'countryZM', 'countryZW'
    },

    gl={
        'ad', 'ae', 'af', 'ag', 'ai', 'al', 'am', 'an', 'ao', 'aq', 'ar',
        'as', 'at', 'au', 'aw', 'az', 'ba', 'bb', 'bd', 'be', 'bf', 'bg',
        'bh', 'bi', 'bj', 'bm', 'bn', 'bo', 'br', 'bs', 'bt', 'bv', 'bw',
        'by', 'bz', 'ca', 'cc', 'cd', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl',
        'cm', 'cn', 'co', 'cr', 'cs', 'cu', 'cv', 'cx', 'cy', 'cz', 'de',
        'dj', 'dk', 'dm', 'do', 'dz', 'ec', 'ee', 'eg', 'eh', 'er', 'es',
        'et', 'fi', 'fj', 'fk', 'fm', 'fo', 'fr', 'ga', 'gd', 'ge', 'gf',
        'gh', 'gi', 'gl', 'gm', 'gn', 'gp', 'gq', 'gr', 'gs', 'gt', 'gu',
        'gw', 'gy', 'hk', 'hm', 'hn', 'hr', 'ht', 'hu', 'id', 'ie', 'il',
        'in', 'io', 'iq', 'ir', 'is', 'it', 'jm', 'jo', 'jp', 'ke', 'kg',
        'kh', 'ki', 'km', 'kn', 'kp', 'kr', 'kw', 'ky', 'kz', 'la', 'lb',
        'lc', 'li', 'lk', 'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc',
        'md', 'mg', 'mh', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', 'mr',
        'ms', 'mt', 'mu', 'mv', 'mw', 'mx', 'my', 'mz', 'na', 'nc', 'ne',
        'nf', 'ng', 'ni', 'nl', 'no', 'np', 'nr', 'nu', 'nz', 'om', 'pa',
        'pe', 'pf', 'pg', 'ph', 'pk', 'pl', 'pm', 'pn', 'pr', 'ps', 'pt',
        'pw', 'py', 'qa', 're', 'ro', 'ru', 'rw', 'sa', 'sb', 'sc', 'sd',
        'se', 'sg', 'sh', 'si', 'sj', 'sk', 'sl', 'sm', 'sn', 'so', 'sr',
        'st', 'sv', 'sy', 'sz', 'tc', 'td', 'tf', 'tg', 'th', 'tj', 'tk',
        'tl', 'tm', 'tn', 'to', 'tr', 'tt', 'tv', 'tw', 'tz', 'ua', 'ug',
        'uk', 'um', 'us', 'uy', 'uz', 'va', 'vc', 've', 'vg', 'vi', 'vn',
        'vu', 'wf', 'ws', 'ye', 'yt', 'za', 'zm', 'zw',
    },

    filter={0, 1},

    hl={
        'af', 'sq', 'sm', 'ar', 'az', 'eu', 'be', 'bn', 'bh', 'bs', 'bg',
        'ca', 'zh-CN', 'zh-TW', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et',
        'fo', 'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu', 'iw', 'hi',
        'hu', 'is', 'id', 'ia', 'ga', 'it', 'ja', 'jw', 'kn', 'ko', 'la',
        'lv', 'lt', 'mk', 'ms', 'ml', 'mt', 'mr', 'ne', 'no', 'nn', 'oc',
        'fa', 'pl', 'pt-BR', 'pt-PT', 'pa', 'ro', 'ru', 'gd', 'sr', 'si',
        'sk', 'sl', 'es', 'su', 'sw', 'sv', 'tl', 'ta', 'te', 'th', 'ti',
        'tr', 'uk', 'ur', 'uz', 'vi', 'cy', 'xh', 'zu'
    },

    imgColorType={
        'color', 'gray', 'mono'
    },

    imgDominantColor={
        'black',
        'blue',
        'brown',
        'gray',
        'green',
        'orange',
        'pink',
        'purple',
        'red',
        'teal',
        'white',
        'yellow',
    },

    imgSize={
        'huge',
        'icon',
        'large',
        'medium',
        'small',
        'xlarge',
        'xxlarge',
    },

    imgType={
        'clipart',
        'face',
        'lineart',
        'news',
        'photo',
    },

    lr={
        'lang_ar', 'lang_bg', 'lang_ca', 'lang_zh-CN', 'lang_zh-TW',
        'lang_hr', 'lang_cs', 'lang_da', 'lang_nl', 'lang_en', 'lang_et',
        'lang_fi', 'lang_fr', 'lang_de', 'lang_el', 'lang_iw', 'lang_hu',
        'lang_is', 'lang_id', 'lang_it', 'lang_ja', 'lang_ko', 'lang_lv',
        'lang_lt', 'lang_no', 'lang_pl', 'lang_pt', 'lang_ro', 'lang_ru',
        'lang_sr', 'lang_sk', 'lang_sl', 'lang_es', 'lang_sv', 'lang_tr',
    },

    num={1, 2, 3, 4, 5, 6, 7, 8, 9, 10},

    rights={
        'cc_publicdomain', 'cc_attribute', 'cc_sharealike',
        'cc_noncommercial', 'cc_nonderived'
    },

    safe={'active', 'off'},

    searchType={None, 'image'},

    siteSearchFilter={'e', 'i'},

    start=range(1, 92)
)


def _dict_product(d):
    """Return the product of all values of a dict, while
    coupling each value with its key.
    This is used to generate multiple queries out of
        possibly multiple arguments in serp_goog.

    >>> d = {'a': [1], 'b': [2, 3, 4], 'c': [5, 6]}
    >>> _dict_product(d)
    >>> [{'a': 1, 'b': 2, 'c': 5},
         {'a': 1, 'b': 2, 'c': 6},
         {'a': 1, 'b': 3, 'c': 5},
         {'a': 1, 'b': 3, 'c': 6},
         {'a': 1, 'b': 4, 'c': 5},
         {'a': 1, 'b': 4, 'c': 6}]
    """
    dicts = []
    for prod in product(*d.values()):
        tempdict = dict(zip(d.keys(), prod))
        dicts.append(tempdict)
    return dicts


def serp_goog(q, cx, key, c2coff=None, cr=None,
              dateRestrict=None, exactTerms=None, excludeTerms=None,
              fileType=None, filter=None, gl=None, highRange=None,
              hl=None, hq=None, imgColorType=None, imgDominantColor=None,
              imgSize=None, imgType=None, linkSite=None, lowRange=None,
              lr=None, num=None, orTerms=None, relatedSite=None,
              rights=None, safe=None, searchType=None, siteSearch=None,
              siteSearchFilter=None, sort=None, start=None):
    """Query Google and get search results in a DataFrame.

    For each parameter, you can supply single or multiple values / arguments.
        If you pass multiple arguments, all the possible combinations of
        arguments (the product) will be requested, and you will get one
        DataFrame combining all queries. See examples below.

    :param q: The search expression.
    :param cx: The custom search engine ID to use for this
        request.
    :param key: The API key of your custom search engine.
    :param c2coff: Enables or disables Simplified and
        Traditional Chinese Search. The default value for this
        parameter is 0 (zero), meaning that the feature is enabled.
        Supported values are:1: Disabled0: Enabled (default)
    :param cr: Restricts search results to documents
        originating in a particular country. You may use Boolean
        operators in the cr parameter's value.Google Search
        determines the country of a document by analyzing:the top-
        level domain (TLD) of the document's URLthe geographic
        location of the Web server's IP addressSee the Country
        Parameter Values page for a list of valid values for this
        parameter.
    :param dateRestrict: Restricts results to URLs based on
        date. Supported values include:d[number]: requests results
        from the specified number of past days.
            w[number]: requests results from the specified number
                of past weeks.
            m[number]: requests results from the specified number
                of past months.
            y[number]: requests results from the specified number
                of past years.
    :param exactTerms: Identifies a phrase that all
        documents in the search results must contain.
    :param excludeTerms: Identifies a word or phrase that
        should not appear in any documents in the search results.
    :param fileType: Restricts results to files of a
        specified extension. A list of file types indexable by
        Google can be found in Search Console Help Center.
    :param filter: Controls turning on or off the duplicate
        content filter.See Automatic Filtering for more information
        about Google's search results filters. Note that host
        crowding filtering applies only to multi-site searches.By
        default, Google applies filtering to all search results to
        improve the quality of those results.  Acceptable values
        are:  "0": Turns off duplicate content filter.  "1": Turns
        on duplicate content filter.
    :param gl: Geolocation of end user. The gl parameter
        value is a two-letter country code. The gl parameter boosts
        search results whose country of origin matches the parameter
        value. See the Country Codes page for a list of valid
        values.Specifying a gl parameter value should lead to more
        relevant results. This is particularly true for
        international customers and, even more specifically, for
        customers in English- speaking countries other than the
        United States.
    :param highRange: Specifies the ending value for a
        search range.Use lowRange and highRange to append an
        inclusive search range of lowRange...highRange to the query.
    :param hl: Sets the user interface language. Explicitly
        setting this parameter improves the performance and the
        quality of your search results.See the Interface
        Languages section of Internationalizing Queries and Results
        Presentation for more information, and Supported Interface
        Languages for a list of supported languages.
    :param hq: Appends the specified query terms to the
        query, as if they were combined with a logical AND operator.
    :param imgColorType: Returns black and white, grayscale,
        or color images: mono, gray, and color.  Acceptable values
        are:  "color": color  "gray": gray  "mono": mono
    :param imgDominantColor: Returns images of a specific
        dominant color.  Acceptable values are:  "black": black
        "blue": blue  "brown": brown  "gray": gray  "green": green
        "orange": orange  "pink": pink  "purple": purple  "red": red
        "teal": teal  "white": white  "yellow": yellow
    :param imgSize: Returns images of a specified size.
        Acceptable values are:  "huge": huge  "icon": icon  "large":
        large  "medium": medium  "small": small  "xlarge": xlarge
        "xxlarge": xxlarge
    :param imgType: Returns images of a type.  Acceptable
        values are:  "clipart": clipart  "face": face  "lineart":
        lineart  "news": news  "photo": photo
    :param linkSite: Specifies that all search results
        should contain a link to a particular URL
    :param lowRange: Specifies the starting value for a
        search range. Use lowRange and highRange to append an
        inclusive search range of lowRange...highRange to the query.
    :param lr: Restricts the search to documents written in
        a particular language (e.g., lr=lang_ja).  Acceptable values
        are:  "lang_ar": Arabic  "lang_bg": Bulgarian  "lang_ca":
        Catalan  "lang_cs": Czech  "lang_da": Danish  "lang_de":
        German  "lang_el": Greek  "lang_en": English  "lang_es":
        Spanish  "lang_et": Estonian  "lang_fi": Finnish  "lang_fr":
        French  "lang_hr": Croatian  "lang_hu": Hungarian
        "lang_id": Indonesian  "lang_is": Icelandic  "lang_it":
        Italian  "lang_iw": Hebrew  "lang_ja": Japanese  "lang_ko":
        Korean  "lang_lt": Lithuanian  "lang_lv": Latvian
        "lang_nl": Dutch  "lang_no": Norwegian  "lang_pl": Polish
        "lang_pt": Portuguese  "lang_ro": Romanian  "lang_ru":
        Russian  "lang_sk": Slovak  "lang_sl": Slovenian  "lang_sr":
        Serbian  "lang_sv": Swedish  "lang_tr": Turkish  "lang_zh-
        CN": Chinese (Simplified)  "lang_zh-TW": Chinese
        (Traditional)
    :param num: Number of search results to return.Valid
        values are integers between 1 and 10, inclusive.
    :param orTerms: Provides additional search terms to
        check for in a document, where each document in the search
        results must contain at least one of the additional search
        terms.
    :param relatedSite: Specifies that all search results
        should be pages that are related to the specified URL.
    :param rights: Filters based on licensing. Supported
        values include: cc_publicdomain, cc_attribute,
        cc_sharealike, cc_noncommercial, cc_nonderived, and
        combinations of these.
    :param safe: Search safety level.  Acceptable values
        are:  "active": Enables SafeSearch filtering.  "off":
        Disables SafeSearch filtering.  (default)
    :param searchType: Specifies the search type: image. If
        unspecified, results are limited to webpages.  Acceptable
        values are:  "image": custom image search.
    :param siteSearch: Specifies all search results should
        be pages from a given site.
    :param siteSearchFilter: Controls whether to include or
        exclude results from the site named in the siteSearch
        parameter.  Acceptable values are:  "e": exclude  "i":
        include
    :param sort: The sort expression to apply to the
        results.
    :param start: The index of the first result to
        return.Valid value are integers starting 1 (default) and the
        second result is 2 and so forth. For example &start=11 gives
        the second page of results with the default "num" value of
        10 results per page.Note: No more than 100 results will ever
        be returned for any query with JSON API, even if more than
        100 documents match the query, so setting (start + num) to
        more than 100 will produce an error. Note that the maximum
        value for num is 10.

    The following function call will produce two queries:
    "hotel" in English, and "hotel"
    >>> serp_goog(q='hotel', gl=['en', 'fr'])

    The below function call will prouce four queries and make four
        requests:
    "fligts" in UK
    "fligts" in Australia
    "tickets" in UK
    "tickets" in Australia
    >>> serp_goog(q=['flights', 'tickets'], cr=['uk', 'au'])
    """
    params = locals()
    supplied_params = {k: v for k, v in params.items() if params[k]}

    for p in supplied_params:
        if isinstance(supplied_params[p], (str, int)):
            supplied_params[p] = [supplied_params[p]]

    for p in supplied_params:
        if p in VALID_VALUES:
            if not set(supplied_params[p]).issubset(VALID_VALUES[p]):
                raise ValueError('Please make sure you provide a'
                                 ' valid value for "{}", valid values:\n'
                                 '{}'.format(p, sorted(VALID_VALUES[p])))
    params_list = _dict_product(supplied_params)
    base_url = 'https://www.googleapis.com/customsearch/v1?'
    ordered_cols = ['searchTerms', 'rank', 'title', 'snippet',
                    'displayLink', 'link', 'queryTime', 'totalResults']
    responses = []
    for param in params_list:
        param_log = ', '.join([k + '=' + str(v) for k, v in param.items()])
        logging.info(msg='Requesting: ' + param_log)
        resp = requests.get(base_url, params=param)
        resp.raise_for_status()
        responses.append(resp)

    result_df = pd.DataFrame()
    for resp in responses:
        request_metadata = resp.json()['queries']['request'][0]
        del request_metadata['title']
        search_info = resp.json()['searchInformation']
        if int(search_info['totalResults']) == 0:
            df = pd.DataFrame(columns=ordered_cols, index=range(1))
            df['searchTerms'] = request_metadata['searchTerms']
        else:
            df = pd.DataFrame(resp.json()['items'])
            df['cseName'] = resp.json()['context']['title']
            start_idx = request_metadata['startIndex']
            df['rank'] = range(start_idx, start_idx + len(df))

        meta_columns = {**request_metadata, **search_info}
        df = df.assign(**meta_columns)
        df['queryTime'] = datetime.datetime.now(tz=datetime.timezone.utc)
        df['queryTime'] = pd.to_datetime(df['queryTime'])
        if 'image' in df:
            img_df = json_normalize(df['image'])
            img_df.columns = ['image.' + c for c in img_df.columns]
            df = pd.concat([df, img_df], axis=1)
        result_df = result_df.append(df, sort=False, ignore_index=True)
    non_ordered = [c for c in result_df.columns if c not in ordered_cols]
    result_df = result_df[ordered_cols + non_ordered]
    return result_df


def set_logging_level(level_or_name):
    """Change the logging level during the session.
    Acceptable values are [0, 10, 20, 30, 40, 50,
        'NOTSET', 'DEBUG', 'INFO', 'WARNING',
        'ERROR', 'CRITICAL']
    """
    lvl_names_values = [0, 10, 20, 30, 40, 50,
                        'NOTSET', 'DEBUG', 'INFO',
                        'WARNING', 'ERROR', 'CRITICAL']
    if level_or_name not in lvl_names_values:
        raise ValueError('Please make sure you supply'
                         ' a value from: {}'.format(lvl_names_values))
    logging.getLogger().setLevel(level_or_name)


logging.getLogger().setLevel('INFO')
