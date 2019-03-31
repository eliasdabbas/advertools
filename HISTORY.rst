=======
History
=======

Unreleased
----------

* Added
    - New function ``extract_exclamations`` very similar to ``extract_questions``

0.7.2 (2019-03-29)
------------------

* Changed
    - Emoji regex updated
    - Simpler extraction of Spanish questions

0.7.1 (2019-03-26)
------------------

* Fixed
    - Missing __init__ imports.

0.7.0 (2019-03-26)
------------------

* Added
    - New ``extract_`` functions:

      * Generic ``extract`` used by all others, and takes arbitrary regex to extract text.
      * ``extract_questions`` to get question mark statistics, as well as the text of questions asked. 
      * ``extract_currency`` shows text that has currency symbols in it, as well as surrounding text.
      * ``extract_intense_words`` gets statistics about, and extract words with any character repeated three or more times, indicating an intense feeling (+ve or -ve).

    - New function ``word_tokenize``: 
      
      * Used by ``word_frequency`` to get tokens of 1,2,3-word phrases (or more).
      * Split a list of text into tokens of a specified number of words each.

    - New stop-words from the ``spaCy`` package:

      current: Arabic, Azerbaijani, Danish, Dutch, English, Finnish, French, German, Greek, Hungarian, Italian, Kazakh, Nepali, Norwegian, Portuguese, Romanian, Russian, Spanish, Swedish, Turkish.

      new: Bengali, Catalan, Chinese, Croatian, Hebrew, Hindi, Indonesian, Irish, Japanese, Persian, Polish, Sinhala, Tagalog, Tamil, Tatar, Telugu, Thai, Ukrainian, Urdu, Vietnamese
* Changed
    - ``word_frequency`` takes new parameters:
        ``regex``: defaults to words, but can be changed to anything '\S+' to split words and keep punctuation for example.

        ``sep``: not longer used as an option, the above regex can be used instead

        ``num_list``: now optional, and defaults to counts of 1 each if not
        provided. Usefull for counting abs_freq only if data not available.

        ``phrase_len``: the number of words in each split token. Defaults to 1
        and can be set to 2 or higher. This helps in analyzing phrases as
        opposed to words.
    - Parameters supplied to ``serp_goog`` appear at the beginning of the result df
    - ``serp_youtube`` now contains ``nextPageToken`` to make paginating requests easier

0.6.0 (2019-02-11)
------------------

* New function
    - ``extract_words`` to extract an arbitrary set of words
* Minor updates
    - ``ad_from_string`` slots argument reflects new text ad lenghts 
    - hashtag regex improved

0.5.3 (2019-01-31)
------------------

* Fix minor bugs
    - Handle Twitter search queries with 0 results in final request

0.5.2 (2018-12-01)
------------------

* Fix minor bugs
    - Properly handle requests for >50 items (``serp_youtube``)
    - Rewrite test for _dict_product
    - Fix issue with string printing error msg

0.5.1 (2018-11-06)
------------------

* Fix minor bugs
    - _dict_product implemented with lists
    - Missing keys in some YouTube responses

0.5.0 (2018-11-04)
------------------

* New function serp_youtube
    - Query YouTube API for videos, channels, or playlists
    - Multiple queries (product of parameters) in one function call
    - Reponse looping and merging handled, one DataFrame 
* serp_goog return Google's original error messages
* twitter responses with entities, get the entities extracted, each in a separate column


0.4.1 (2018-10-13)
------------------

* New function serp_goog (based on Google CSE)
    - Query Google search and get the result in a DataFrame
    - Make multiple queries / requests in one function call
    - All responses merged in one DataFrame
* twitter.get_place_trends results are ranked by town and country

0.4.0 (2018-10-08)
------------------

* New Twitter module based on twython
    - Wraps 20+ functions for getting Twitter API data
    - Gets data in a pands DataFrame
    - Handles looping over requests higher than the defaults
* Tested on Python 3.7

0.3.0 (2018-08-14)
------------------

* Search engine marketing cheat sheet.
* New set of extract\_ functions with summary stats for each:
    * extract_hashtags
    * extract_mentions
    * extract_emoji
* Tests and bug fixes

0.2.0 (2018-07-06)
------------------

* New set of kw_<match-type> functions.
* Full testing and coverage. 

0.1.0 (2018-07-02)
------------------

* First release on PyPI.
* Functions available:
    - ad_create: create a text ad place words in placeholders
    - ad_from_string: split a long string to shorter string that fit into
        given slots
    - kw_generate: generate keywords from lists of products and words
    - url_utm_ga: generate a UTM-tagged URL for Google Analytics tracking
    - word_frequency: measure the absolute and weighted frequency of words in
        collection of documents
