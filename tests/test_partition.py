import re

from advertools.partition import partition


def test_partition_basic():
    assert partition("abc123def456ghi", r"\d+") == ["abc", "123", "def", "456", "ghi"]


def test_partition_no_match_strip():
    assert partition("test", r"X") == ["test"]
    assert partition("  test  ", r"X") == ["test"]


def test_partition_consecutive_delimiters():
    assert partition(",a,,b,", r",") == [",", "a", ",", ",", "b", ","]


def test_partition_delimiter_at_start_and_end():
    assert partition("delimtextdelim", r"delim") == ["delim", "text", "delim"]


def test_partition_delimiter_in_middle():
    assert partition("startmiddleend", r"middle") == ["start", "middle", "end"]


def test_partition_ignore_case():
    assert partition("TestData", r"t", flags=re.IGNORECASE) == [
        "T",
        "es",
        "t",
        "Da",
        "t",
        "a",
    ]


def test_partition_empty_string_input():
    assert partition("", r"\d+") == [""]


def test_partition_regex_is_capturing_group():
    # User regex: r"(--)". Function makes it r"((--))".
    # re.split(r"((--))", "abc--def") -> ['abc', '--', '--', 'def']
    # All parts are non-empty after strip, so all are kept by current code.
    assert partition("abc--def", r"(--)") == ["abc", "--", "--", "def"]


def test_partition_special_chars_in_regex():
    assert partition("abc.def", r"\.") == ["abc", ".", "def"]


def test_partition_special_chars_in_text():
    assert partition("a*b+c?d", r"\+|\*|\?") == ["a", "*", "b", "+", "c", "?", "d"]


def test_partition_unicode_chars():
    assert partition("你好世界123再见", r"\d+") == ["你好世界", "123", "再见"]


def test_partition_flags_combination():
    assert partition("abc123DEF", r"[a-z]+") == ["abc", "123DEF"]

    assert partition("abc123DEF", r"[a-z]+", flags=re.IGNORECASE) == [
        "abc",
        "123",
        "DEF",
    ]


def test_partition_stripping_behavior():
    assert partition("  abc  123  def  ", r"\d+") == ["abc", "123", "def"]
    assert partition(" leading space123trailing space ", r"\d+") == [
        "leading space",
        "123",
        "trailing space",
    ]


def test_partition_only_delimiters():
    assert partition(",,,", r",") == [",", ",", ","]


def test_partition_delimiters_with_surrounding_spaces():
    assert partition(" , a , , b , ", r",") == [",", "a", ",", ",", "b", ","]


def test_partition_regex_matches_whole_string():
    # with capturing group
    assert partition("abc", r"(^.*)") == ["abc", "abc"]
    # without capturing group
    assert partition("abc", r".*") == ["abc"]


def test_partition_regex_matches_empty_string_positions():
    assert partition("abc", r"()") == ["a", "b", "c"]


def test_partition_stripping_part_makes_it_empty():
    assert partition("  --abc", r"--") == ["--", "abc"]

    assert partition("abc--  ", r"--") == ["abc", "--"]

    assert partition("  --  abc  --  ", r"--") == ["--", "abc", "--"]
