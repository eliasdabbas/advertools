import re
from unicodedata import name

APOSTROPHE = []
BRACKET = []
COLON = []
COMMA = []
CURRENCY = []
CURRENCY_RAW = []
EXCLAMATION_MARK_RAW = []
FULL_STOP = []
HASHTAG = []
HASHTAG_RAW = []
MENTION = []
MENTION_RAW = []
PAREN = []
QUESTION_MARK_RAW = []
QUOTE = []
SENTENCE_END = []
URL = []
URL_RAW = []
WORD_DELIM = []

for i in range(2_000_000):
    try:
        if "APOSTROPHE" in name(chr(i)) and (chr(i) not in ["ŉ", "\U000e0027"]):
            APOSTROPHE.append(chr(i))
        if (
            "BRACKET" in name(chr(i))
            and "IDEOGRAPH" not in name(chr(i))
            and "TORTOISE SHELL BRACKETED LATIN CAPITAL LETTER S" not in name(chr(i))
        ):
            BRACKET.append(chr(i))
        if "COLON" in name(chr(i)) and i != 8353:  # remove the colon currency sign (₡)
            COLON.append(chr(i))
        if (
            ("COMMA" in name(chr(i)))
            and not re.match("LATIN (SMALL|CAPITAL) LETTER", name(chr(i)))
            and not re.match("DIGIT", name(chr(i)))
        ):
            COMMA.append(chr(i))
        if "EXCLAMATION" in name(chr(i)):
            EXCLAMATION_MARK_RAW.append(chr(i))
        if (
            "FULL STOP" in name(chr(i))
            and (not name(chr(i)).startswith("DIGIT"))
            and (not name(chr(i)).startswith("NUMBER"))
        ):
            FULL_STOP.append(chr(i))
        if "QUOT" in name(chr(i)) and name(chr(i)) != "YI SYLLABLE QUOT":
            QUOTE.append(chr(i))
        if "CURRENC" in name(chr(i)):
            CURRENCY.append(chr(i))
        if ("PAREN" in name(chr(i))) and not re.match("PARENTHESIZED", name(chr(i))):
            PAREN.append(chr(i))
        if "QUESTION" in name(chr(i)) and "IDEOGRAPH" not in name(chr(i)):
            QUESTION_MARK_RAW.append(chr(i))
    except Exception:
        continue
