import string
def ad_from_string(s, capitalize=True):
    """Convert string `s` to an ad by splitting it into groups of words.
    Each group would have a length of at most the allowed length for that slot. 
    
    If the total length of `s` exceeds the total allowed length, all remaining
    characters would be grouped in the last element of the returned list.
    
    Main ad slots:
    
    Headline 1: 30 chars
    Headline 2: 30 chars
    Description: 80 chars
    Path1: 15 chars
    Path2: 15 chars
    
    Parameters
    ----------
    s : a string of characters, with no restrictions on length.
    capitalize : whether or not to capitalize each word after grouping. Setting 
        it as False would leave the input string as is. 
    
    Returns
    -------
    text ad : a list of strings 
    
    Examples
    --------
    >>> ad_from_string('this is a short ad')
    ... ['This Is A Short Ad', '', '', '', '', '']
    
    >>> ad_from_string('this is a longer ad and would take two of the first slots')
    ... ['This Is A Longer Ad And Would', 'Take Two Of The First Slots', '', '', '', '']
    
    """
    str_words = [x for x in s.split(' ')]

    h1 = ''
    h2 = ''
    desc = ''
    path1 = ''
    path2 = ''
    remain = ''
    
    text_ad = []
    counter = 0

    for ad in [[h1, 30],[h2, 30],[desc, 80],[path1, 15],[path2, 15]]:
        while (len(ad[0]) <= ad[1]) and (counter <= len(str_words) -1):
            if len(ad[0] + str_words[counter]) > ad[1]:
                break
            ad[0] += ' ' + str_words[counter]
            counter += 1
        text_ad.append(ad[0][1:])
        
    remain = ' '.join(str_words[counter:]) 
    text_ad.append(remain)

    return [string.capwords(x) if capitalize else x for x in text_ad]
