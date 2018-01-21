import string
def ad_from_string(s, slots=(30, 30, 80, 15, 15), sep=None, capitalize=False):
    """Convert string `s` to an ad by splitting it into groups of words.
    Each group would have a length of at most the allowed length for that slot. 
    
    If the total length of `s` exceeds the total allowed length, all remaining
    characters would be grouped in the last element of the returned list.
    
    
    Parameters
    ----------
    s : a string of characters, with no restrictions on length.
    slots : an iterable of integers for the maximum lengths for each slot
    sep : by which character to split `s`
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
    
    str_words = s.split(sep=sep)
    text_ad = ['' for x in range(len(slots)+1)]
    counter = 0

    for i, slot in enumerate(slots):
        while counter <= len(str_words) - 1:
            if len(text_ad[i] + str_words[counter]) > slot:
                break
            text_ad[i] += ' ' + str_words[counter] if text_ad[i] else str_words[counter]
            counter += 1
                  
    text_ad[-1] = sep.join(str_words[counter:]) if sep is not None else ' '.join(str_words[counter:]) 

    return [string.capwords(x) if capitalize else x for x in text_ad]