def num_format(num):
    """Format a number in a short form using K M B, etc.
    example:
    >>> adv.num_format(1234)
    1.23K

    >>> adv.num_format(1234567)
    1.23M
    """
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.2f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])
