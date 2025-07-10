"""
Text partitioning with Python
=============================

The ``partition`` function in ``advertools`` provides a powerful way to partition a string
based on a regular expression. Unlike typical string splitting methods that only return
the text *between* delimiters, ``partition`` includes the delimiters themselves in the
result list. This is particularly useful for tasks where the delimiters are as important
as the content they separate.



What is partitioning?
---------------------

It is the process of converting a string of characters into a list, while preserving all
characters in the input string.
In other words, you should be able to do a "round trip" from string to partitioned
string, and back to the original string.

This function does this, although it strips whitespace so the round-trip is not 100%
but almost.


Partitioning using a regular expression
---------------------------------------

An important feature in this function is that it enables you to partition using a regex
pattern, and not just a fixed sequence of characters. You can partition a markdown
string into headings and regular text for example, and use only "#", "##", and "###" for
the partitioning.

It also provides a `flags` parameter, in case you want to utilize Python's various options
like ``re.IGNORECASE``, ``re.DOTALL``, or ``re.MULTILINE`` for example



Core Functionality
------------------

The function takes a ``text`` string, a ``regex`` pattern, and optional ``flags`` from
the ``re`` module. It returns a list of strings, alternating between the substrings and
the matches.

**Key Features:**

*   **Includes Delimiters:** The matched delimiters are part of the output list.
*   **Regex Powered:** Leverages the full power of regular expressions for defining separators.


Examples
--------

Let's explore some practical examples:

**1. Basic splitting by numbers:**

.. code-block:: python

   >>> import advertools as adv

   >>> text = "abc123def456ghi"
   >>> regex = r"\\d+"
   >>> adv.partition(text, regex)
   ['abc', '123', 'def', '456', 'ghi']

**2. No match found:**

If the regex pattern doesn't find any matches, the original string is returned as a single-element list.

.. code-block:: python

   >>> import advertools as adv

   >>> text = "test"
   >>> regex = r"X"
   >>> adv.partition(text, regex)
   ['test']

**3. Handling consecutive delimiters and edge matches:**

This example shows how ``partition`` handles cases where delimiters are at the start/end or appear consecutively.

.. code-block:: python

   >>> import advertools as adv

   >>> text = ",a,,b,"
   >>> regex = r","
   >>> adv.partition(text, regex)
   [',', 'a', ',', ',', 'b', ',']

**4. Case-insensitive partitioning:**

You can use regex flags, like ``re.IGNORECASE``, for more flexible matching.

.. code-block:: python

   >>> import advertools as adv
   >>> import re

   >>> text = "TestData"
   >>> regex = r"t"
   >>> adv.partition(text, regex, flags=re.IGNORECASE)
   ['T', 'es', 't', 'Da', 't', 'a']

Connecting to other use cases
-----------------------------

While ``partition`` is a general-purpose string manipulation tool, its ability to retain
delimiters makes it valuable in various contexts. For instance, if you were working with
a function that processes Markdown documents (using the ``adv.crawlytics.generate_markdown``
function),
``partition`` could be used to split a Markdown document by specific structural elements
(e.g., headings, code blocks, lists).


Imagine you want to break down a Markdown document into chunks based on heading levels
(e.g., ``##``, ``###`` ). The ``partition`` function could be used to identify these
headings and the content between them.

.. code-block:: python

   >>> import advertools as adv
   >>> import re

   >>> markdown_text = '''
   # Document Title

   Some introductory text.

   ## Section 1

   Content for section 1.

   ### Subsection 1.1

   Details for subsection 1.1.

   ## Section 2

   Content for section 2.
   '''

   >>> heading_regex = r"^#+ .*?$"

   # Partition the markdown text by headings
   # Note: This is a simplified example. A robust markdown parser would be more complex.
   >>> chunks = adv.partition(markdown_text, heading_regex, flags=re.MULTILINE)

   # The 'chunks' list would contain alternating text blocks and the matched headings,
   # allowing further processing of each part of the document.
   >>> print(*chunks, sep="\\n----\\n")
   # Document Title
   ----
   Some introductory text.
   ----
   ## Section 1
   ----
   Content for section 1.
   ----
   ### Subsection 1.1
   ----
   Details for subsection 1.1.
   ----
   ## Section 2
   ----
   Content for section 2.

"""

import re


def partition(text, regex, flags=0):
    """Partition a string based on a regex pattern.

    Splits the `text` by all occurrences of `regex`. The resulting list
    includes both the substrings between the matches and the matches
    themselves.

    Parameters
    ----------
    text : str
        The input string to partition.
    regex : str
        The regular expression string to find delimiter strings.
        This pattern defines the separators.
    flags : int, optional
        Regex flags from the `re` module (e.g., `re.IGNORECASE`).
        Defaults to 0 (no flags).

    Returns
    -------
    list[str] : A list of strings, where elements are alternating parts of the original
                string and the substrings matched by the regex.
    - If `regex` does not match, the list contains `text` as its
      only element.
    - If matches occur at the beginning/end of `text`, or are
      consecutive, empty strings may be included to represent zero-length parts.

    Examples
    --------
    >>> partition("abc123def456ghi", r"\\d+")
    ['abc', '123', 'def', '456', 'ghi']
    >>> partition("test", r"X")  # No match
    ['test']
    >>> partition(",a,,b,", r",")
    ['', ',', 'a', ',', '', ',', 'b', ',', '']
    >>> partition("startmiddleend", r"middle")
    ['start', 'middle', 'end']
    >>> partition("delimtextdelim", r"delim")
    ['delim', 'text', 'delim']
    >>> partition("TestData", r"t", flags=re.IGNORECASE)
    ['T', 'es', 't', 'Da', 't', 'a']
    """
    if text == "":
        return [""]

    capturing_regex = f"({regex})"

    parts = re.split(capturing_regex, text, flags=flags)

    return [part.strip() for part in parts if part.strip()]
