"""
A collection of regular expressions for use in different contexts.
Each one is available in two formats
- REGEX_RAW: raw string only, for sharing, and combining with other regexes
- REGEX: compiled, readable, annotated version
Based on Unicode database v11.0.0
"""
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


QUESTION_RAW = (r'(?i)(?:(?<={})(?:{}*)\s+|^)(¿?{}+?{}+)'
                .format(SENTENCE_END, QUOTE,
                        QUESTION_MARK_NEG_RAW,
                        QUESTION_MARK_RAW.replace('¿', '')))

QUESTION = re.compile(r"""
    (?i)           # case insensitive
    (?:(?<={s})    # beginning of string, or assert current position
                   #   preceded by a SENTENCE_END character
    (?:{q}*)       # optional quote character(s)
    \s+|^)         # one or more spaces
    (¿?{neg}+?     # optional Spanish question mark, then one or more
                   #   non-SENTENCE_END characters
     {raw}+)       # one or more question mark characters excluding "¿"
    """.format(s=SENTENCE_END,
               q=QUOTE,
               neg=SENTENCE_END.replace('[', '[^'),
               raw=QUESTION_MARK_RAW.replace('¿', '')),
    re.VERBOSE)
