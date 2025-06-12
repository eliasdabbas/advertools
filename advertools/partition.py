"""
Introduction to partitioning text
===================================

The ``partition`` function in ``advertools`` provides a powerful way to split a string
based on a regular expression. Unlike typical string splitting methods that only return the text *between* delimiters, ``partition`` includes the delimiters themselves in the result list. This is particularly useful for tasks where the delimiters are as important as the content they separate.

Core Functionality
------------------

The function takes a ``text`` string, a ``regex`` pattern, and optional ``flags`` from the ``re`` module. It returns a list of strings, alternating between the substrings and the matches.

**Key Features:**

*   **Includes Delimiters:** The matched delimiters are part of the output list.
*   **Regex Powered:** Leverages the full power of regular expressions for defining separators.
*   **Handles Edge Cases:** Correctly processes matches at the beginning or end of the string, and consecutive matches, by including empty strings to represent zero-length parts.

Examples
--------

Let's explore some practical examples:

**1. Basic Splitting by Numbers:**

.. code-block:: python

   import advertools as adv

   text = "abc123def456ghi"
   regex = r"\\d+"
   result = adv.partition(text, regex)
   print(result)
   # Output: ['abc', '123', 'def', '456', 'ghi']

**2. No Match Found:**

If the regex pattern doesn't find any matches, the original string is returned as a single-element list.

.. code-block:: python

   import advertools as adv

   text = "test"
   regex = r"X"
   result = adv.partition(text, regex)
   print(result)
   # Output: ['test']

**3. Handling Consecutive Delimiters and Edge Matches:**

This example shows how ``partition`` handles cases where delimiters are at the start/end or appear consecutively.

.. code-block:: python

   import advertools as adv

   text = ",a,,b,"
   regex = r","
   result = adv.partition(text, regex)
   print(result)
   # Output: ['', ',', 'a', ',', '', ',', 'b', ',', '']

**4. Case-Insensitive Partitioning:**

You can use regex flags, like ``re.IGNORECASE``, for more flexible matching.

.. code-block:: python

   import advertools as adv
   import re

   text = "TestData"
   regex = r"t"
   result = adv.partition(text, regex, flags=re.IGNORECASE)
   print(result)
   # Output: ['', 'T', 'es', 't', 'Data']

Connecting to Other Use Cases
-----------------------------

While ``partition`` is a general-purpose string manipulation tool, its ability to retain delimiters makes it valuable in various contexts. For instance, if you were working with a function that processes Markdown documents (let's imagine a hypothetical ``generate_markdown_chunks`` function), ``partition`` could be used to split a Markdown document by specific structural elements (e.g., headings, code blocks, lists).

Imagine you want to break down a Markdown document into chunks based on heading levels (e.g., ``## ``, ``### ``). The ``partition`` function could be used to identify these headings and the content between them.

.. code-block:: python

   import advertools as adv
   import re

   markdown_text = '''
   # Document Title

   Some introductory text.

   ## Section 1

   Content for section 1.

   ### Subsection 1.1

   Details for subsection 1.1.

   ## Section 2

   Content for section 2.
   '''
   # Regex to match markdown headings (##, ###, etc.)
   # Matches lines starting with one or more '#' followed by a space
   heading_regex = r"^#+\\s"


   # Partition the markdown text by headings
   # Note: This is a simplified example. A robust markdown parser would be more complex.
   chunks = adv.partition(markdown_text, heading_regex, flags=re.MULTILINE)

   # The 'chunks' list would contain alternating text blocks and the matched headings,
   # allowing further processing of each part of the document.
   for i, chunk in enumerate(chunks):
       if re.match(heading_regex, chunk):
           print(f"Heading: {chunk.strip()}")
       else:
           print(f"Content Block {i // 2 + 1}:\\n{chunk.strip()}\\n")

This demonstrates how ``partition`` can be a foundational tool for more complex text processing tasks, such as breaking down structured documents into manageable pieces.

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
    list[str]
        A list of strings, where elements are alternating parts of the
        original string and the substrings matched by the regex.
        - If `regex` does not match, the list contains `text` as its
          only element.
        - If matches occur at the beginning/end of `text`, or are
          consecutive, empty strings may be included to represent
          zero-length parts.

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
    ['', 'delim', 'text', 'delim', '']
    >>> partition("TestData", r"t", flags=re.IGNORECASE)
    ['', 'T', 'es', 't', 'Data']
    """
    if text == "":
        return [""]

    capturing_regex = f"({regex})"

    parts = re.split(capturing_regex, text, flags=flags)

    return [part.strip() for part in parts if part.strip()]
