=======================
Change Log - advertools
=======================

0.9.0 (2020-04-03)
------------------

* Added
    - New function ``sitemap_to_df`` imports an XML sitemap into a
      ``DataFrame``

0.8.1 (2020-02-08)
------------------

* Changed
    - Column :attr:`query_time` is now named :attr:`queryTime` in the :ref:`youtube <youtube>` module for consistency with :ref:`serp_ <serp>` functions
    - Handle json_normalize import from pandas based on pandas version

0.8.0 (2020-02-02)
------------------

* Added
    - New module :ref:`youtube <youtube>` connecting to all GET requests in API
    - :ref:`extract_numbers <extract>` new function
    - :ref:`emoji_search <emoji>` new function
    - :ref:`emoji_df <emoji>` new variable containing all emoji as a DataFrame

* Changed
    - Emoji database updated to v13.0
    - :ref:`serp_goog <serp>` with expanded :attr:`pagemap` and metadata

* Fixed
    - :ref:`serp_goog <serp>` errors, some parameters not appearing in result
      df
    - :ref:`extract_numbers <extract>` issue when providing dash as a separator
      in the middle

0.7.3 (2019-04-17)
------------------

* Added
    - New function :ref:`extract_exclamations <extract>` very similar to
      :ref:`extract_questions <extract>`
    - New function :ref:`extract_urls <extract>`, also counts top domains and
      top TLDs
    - New keys to :ref:`extract_emoji <extract>`; :attr:`top_emoji_categories`
      & :attr:`top_emoji_sub_categories`
    - Groups and sub-groups to :ref:`emoji db <emoji>`

0.7.2 (2019-03-29)
------------------

* Changed
    - :ref:`Emoji regex <emoji>` updated
    - Simpler extraction of Spanish :ref:`questions <extract>`

0.7.1 (2019-03-26)
------------------

* Fixed
    - Missing __init__ imports.

0.7.0 (2019-03-26)
------------------

* Added
    - New :ref:`extract_ <extract>` functions:

      * Generic :ref:`extract <extract>` used by all others, and takes
        arbitrary regex to extract text.
      * :ref:`extract_questions <extract>` to get question mark statistics, as
        well as the text of questions asked.
      * :ref:`extract_currency <extract>` shows text that has currency symbols in it, as
        well as surrounding text.
      * :ref:`extract_intense_words <extract>` gets statistics about, and extract words with
        any character repeated three or more times, indicating an intense
        feeling (+ve or -ve).

    - New function :ref:`word_tokenize <word_tokenize>`:
      
      * Used by :ref:`word_frequency <word_frequency>` to get tokens of
        1,2,3-word phrases (or more).
      * Split a list of text into tokens of a specified number of words each.

    - New stop-words from the ``spaCy`` package:

      **current:** Arabic, Azerbaijani, Danish, Dutch, English, Finnish,
      French, German, Greek, Hungarian, Italian, Kazakh, Nepali, Norwegian,
      Portuguese, Romanian, Russian, Spanish, Swedish, Turkish.

      **new:** Bengali, Catalan, Chinese, Croatian, Hebrew, Hindi, Indonesian,
      Irish, Japanese, Persian, Polish, Sinhala, Tagalog, Tamil, Tatar, Telugu,
      Thai, Ukrainian, Urdu, Vietnamese

* Changed
    - :ref:`word_frequency <word_frequency>` takes new parameters:
        * :attr:`regex` defaults to words, but can be changed to anything '\S+'
          to split words and keep punctuation for example.

        * :attr:`sep` not longer used as an option, the above :ref:`regex` can
          be used instead

        * :attr:`num_list` now optional, and defaults to counts of 1 each if not
          provided. Useful for counting :attr:`abs_freq` only if data not
          available.

        * :attr:`phrase_len` the number of words in each split token. Defaults
          to 1 and can be set to 2 or higher. This helps in analyzing phrases
          as opposed to words.

    - Parameters supplied to :ref:`serp_goog <serp>` appear at the beginning
      of the result df
    - :ref:`serp_youtube <serp>` now contains :attr:`nextPageToken` to make
      paginating requests easier

0.6.0 (2019-02-11)
------------------

* New function
    - :ref:`extract_words <extract>` to extract an arbitrary set of words
* Minor updates
    - :ref:`ad_from_string <ad_from_string>` slots argument reflects new text
      ad lenghts
    - :attr:`hashtag` regex improved

0.5.3 (2019-01-31)
------------------

* Fix minor bugs
    - Handle Twitter search queries with 0 results in final request

0.5.2 (2018-12-01)
------------------

* Fix minor bugs
    - Properly handle requests for >50 items (:ref:`serp_youtube <serp>`)
    - Rewrite test for _dict_product
    - Fix issue with string printing error msg

0.5.1 (2018-11-06)
------------------

* Fix minor bugs
    - _dict_product implemented with lists
    - Missing keys in some YouTube responses

0.5.0 (2018-11-04)
------------------

* New function :ref:`serp_youtube <serp>`
    - Query YouTube API for videos, channels, or playlists
    - Multiple queries (product of parameters) in one function call
    - Reponse looping and merging handled, one DataFrame 
* :ref:`serp_goog <serp>` return Google's original error messages
* twitter responses with entities, get the entities extracted, each in a
  separate column


0.4.1 (2018-10-13)
------------------

* New function :ref:`serp_goog <serp>` (based on Google CSE)
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
