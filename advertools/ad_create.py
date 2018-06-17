import string

def ad_create(template, replacements, fallback, max_len=30, capitalize=True):
    """Insert each of the replacement strings in its place within template
    
    Parameters
    ----------
    template : a string format template, using braces
    replacements : replacements string to be inserted in template
    fallback : the string to insert in template in case the replacement is too long
    max_len : the maximum allowed length of the full string
    
    Returns
    -------
    formatted : list of strings
    
    Examples
    --------
    >>> ad_create('Let\'s count {}', ['one', 'two', 'three'], 'one', 20)
    ["Let's count one", "Let's count two", "Let's count three"]
    
    >>> ad_create(template='My favorite car is {}', 
                 replacements=['Toyota', 'BMW', 'Mercedes', 'Lamborghini'], 
                 fallback='great', 
                 max_len=28)
    ['My favorite car is Toyota', 'My favorite car is BMW', 'My favorite car is Mercedes', 
    'My favorite car is great']    
    
    
    """
    if len(template.format(fallback)) > max_len:
        raise ValueError('template + fallback should be <= ' + str(max_len) + ' chars')
    final_ad = []
    for rep in replacements:
        if len(template.format(rep)) <= max_len:
            final_ad.append(template.format(rep))
        else:
            final_ad.append(template.format(fallback))
    
    return [string.capwords(s) for s in final_ad] if capitalize else final_ad