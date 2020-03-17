"""
.. _regex:

Regular Expressions for Extracting Structured Entities
======================================================

A collection of regular expressions for use in different contexts.
Each one is available in two formats:

* REGEX_RAW: (HASHTAG_RAW, MENTION_RAW, etc.) raw string only, for sharing
             and combining with other regexes
* REGEX: (HASHTAG, MENTION, etc.) compiled regex, readable, and annotated

Based on Unicode database v11.0.0

URL regex from Regular Expressions Cookbook 2nd Ed. O'Reilly
"""

__all__ = ['APOSTROPHE', 'BRACKET', 'COLON', 'COMMA', 'CURRENCY',
           'CURRENCY_RAW', 'EXCLAMATION', 'EXCLAMATION_MARK', 'FULL_STOP',
           'HASHTAG', 'HASHTAG_RAW', 'MENTION', 'MENTION_RAW', 'PAREN',
           'QUESTION', 'QUESTION_MARK', 'QUESTION_MARK_NEG_RAW',
           'QUESTION_MARK_RAW', 'QUESTION_RAW', 'QUOTE',
           'SENTENCE_END', 'WORD_DELIM', 'URL', 'URL_RAW']

import re


# word delimiters used to extract words
QUOTE = r'["«»‘’‚‛“”„‟‹›❮❯⹂〝〞〟＂]'

EXCLAMATION = r'[!¡՜߹᥄‼⁈⁉︕﹗！𖺚𞥞]'

FULL_STOP = r'[.։۔܁܂።᙮᠃᠉⳹⳾⸼。꓿꘎꛳︒﹒．｡𖫵𖺘𛲟𝪈]'

COMMA = r'[,՝،߸፣᠂᠈⸲⸴⹁⹉⹌、꓾꘍꛵︐︑﹐﹑，､𑑍𖺗𝪇]'

BRACKET = (r'[[]{}⁅⁆〈〉❬❭❰❱❲❳❴❵⟦⟧⟨⟩⟪⟫⟬⟭⦃⦄⦇⦈⦉⦊⦋⦌⦍⦎⦏⦐⦑⦒⦓⦔⦕⦖⦗⦘⧼⧽⸂⸃⸄⸅⸉⸊⸌⸍⸜⸝⸢⸣⸤⸥⸦⸧〈〉'
           r'《》「」『』【】〔〕〖〗〘〙〚〛︗︷︸︹︺︻︼︽︾︿﹀﹁﹂﹃﹄﹇﹈'
           r'﹛﹜﹝﹞［］｛｝｢｣]')

COLON = r'[:;؛܃܄܅܆܇܈܉፤፥፦᠄⁏⁝⸵꛴꛶︓︔﹔﹕：；𒑱𒑲𒑳𒑴𝪉𝪊]'

PAREN = r'[()⁽⁾₍₎❨❩❪❫⟮⟯⦅⦆⸨⸩﴾﴿︵︶﹙﹚（）｟｠𝪋]'

APOSTROPHE = r'["\'ʼˮ՚ߴߵ＇"]'

EXCLAMATION_MARK_RAW = r'[!¡՜߹᥄‼⁈⁉︕﹗！𖺚𞥞]'

EXCLAMATION_MARK = re.compile(
    r"""[!¡՜߹᥄‼⁈⁉︕﹗！𖺚𞥞]
        # Unicode characters named exclamation mark
    """, re.VERBOSE)

EXCLAMATION_MARK_NEG_RAW = r'[^!¡՜߹᥄‼⁈⁉︕﹗！𖺚𞥞]'

QUESTION_MARK_RAW = r'[?¿;՞؟፧᥅⁇⁈⁉⳺⳻⸮꘏꛷︖﹖？𑅃𞥟' + r'ʔ‽' + r']'

QUESTION_MARK = re.compile(
    r"""[?¿;՞؟፧᥅⁇⁈⁉⳺⳻⸮꘏꛷︖﹖？𑅃𞥟ʔ‽]
         # Unicode characters named question mark
    """, re.VERBOSE)

QUESTION_MARK_NEG_RAW = r'[^?;՞؟፧᥅⁇⁈⁉⳺⳻⸮꘏꛷︖﹖？𑅃𞥟ʔ‽]'

WORD_DELIM = r'[' + r''.join([x.strip('[]')
                              for x in [QUOTE, EXCLAMATION, QUESTION_MARK_RAW,
                                        FULL_STOP, COMMA, BRACKET, COLON,
                                        APOSTROPHE + PAREN]]) + r']'

SENTENCE_END = r'[' + r''.join([x.strip('[]')
                                for x in [EXCLAMATION, FULL_STOP,
                                          QUESTION_MARK_RAW]]) + r']'

HASHTAG_RAW = r'(?i)(?<!\w)([＃#]\w+)'

HASHTAG = re.compile(
    r"""
    (?i)        # case-insensitive mode
    (?<!\w)     # hashtag not preceded by word character
    ([＃#]\w+)  # one of two hashtag characters
    """, re.VERBOSE)

MENTION_RAW = r'(?ix)(?<!\w)([@＠][a-z0-9_]+)\b'

MENTION = re.compile(
    r"""(?i)     # case-insensitive
    (?<!\w)      # word character doesn't precede mention
    ([@＠]       # either of two @ signs
    [a-z0-9_]+)  # A to Z, numbers and underscores only
    \b           # end with a word boundary
    """, re.VERBOSE)

CURRENCY_RAW = r'[$¢£¤¥֏؋৲৳৻૱௹฿៛₠₡₢₣₤₥₦₧₨₩₪₫€₭₮₯₰₱₲₳₴₵₶₷₸₹₺₻₼₽₾₿﷼﹩＄￠￡￥￦]'

CURRENCY = re.compile(
    r"""[$¢£¤¥֏؋৲৳৻૱௹฿៛₠₡₢₣₤₥₦₧₨₩₪₫€₭₮₯₰₱₲₳₴₵₶₷₸₹₺₻₼₽₾₿﷼﹩＄￠￡￥￦]
         # Unicode characters under the category is "Sc"
    """, re.VERBOSE)


EXCLAMATION_RAW = (r'(?i)(?:(?:(?<={})(?:{}*)\s+|^)|(?=¡))(¡?{}+?{}+)'
                   .format(SENTENCE_END, QUOTE,
                           EXCLAMATION_MARK_NEG_RAW,
                           EXCLAMATION_MARK_RAW.replace('¡', '')))


EXCLAMATION = re.compile(r"""
    (?i)           # case insensitive
    (?:
    (?:(?<={s})    # beginning of string, or assert current position
                   #   preceded by a SENTENCE_END character
    (?:{q}*)       # optional quote character(s)
    \s+|^)         # one or more spaces
    |(?=¡))        # or assert current position is "¡" 
    (¡?{neg}+?     # optional Spanish exclamation mark, then one or more
                   #   non-SENTENCE_END characters
     {raw}+)       # one or more exclamation mark characters excluding "¡"
    """.format(s=SENTENCE_END,
               q=QUOTE,
               neg=SENTENCE_END.replace('[', '[^'),
               raw=EXCLAMATION_MARK_RAW.replace('¡', '')),
    re.VERBOSE)


QUESTION_RAW = (r'(?i)(?:(?:(?<={})(?:{}*)\s+|^)|(?=¿))(¿?{}+?{}+)'
                .format(SENTENCE_END, QUOTE,
                        QUESTION_MARK_NEG_RAW,
                        QUESTION_MARK_RAW.replace('¿', '')))

QUESTION = re.compile(r"""
    (?i)           # case insensitive
    (?:
    (?:(?<={s})    # beginning of string, or assert current position
                   #   preceded by a SENTENCE_END character
    (?:{q}*)       # optional quote character(s)
    \s+|^)         # one or more spaces
    |(?=¿))        # or assert current position is "¿" 
    (¿?{neg}+?     # optional Spanish question mark, then one or more
                   #   non-SENTENCE_END characters
     {raw}+)       # one or more question mark characters excluding "¿"
    """.format(s=SENTENCE_END,
               q=QUOTE,
               neg=SENTENCE_END.replace('[', '[^'),
               raw=QUESTION_MARK_RAW.replace('¿', '')),
    re.VERBOSE)

URL_RAW = (r'(?xi)\b(?:(?:https?|ftp|file)://|www\.|ftp\.)'
           r'(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|'
           r'[-A-Z0-9+&@#/%=~_|$?!:,.])*'
           r'(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|'
           r'[A-Z0-9+&@#/%=~_|$])')

URL = re.compile(r"""
    (?xi)                                     # case-insensitive / verbose
    \b(?:(?:https?|ftp|file)://|www\.|ftp\.)  # starts w/ http(s), ftp or www
      (?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|      # acceptable url chars in parens
       [-A-Z0-9+&@#/%=~_|$?!:,.])*            # acceptable url chars
       (?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|     # acceptable url chars in parens
       [A-Z0-9+&@#/%=~_|$])                   # acceptable url chars  
    """, re.VERBOSE)
