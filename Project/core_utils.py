def removeDupWithoutOrder(str):
    """Remove duplicates from a string. Order will not be preserved

    Args:
        str (string): string to remove duplicate values from

    Returns:
        string : Duplicate free string
    """    
    return "".join(set(str)) 


def removeListDups(base_list,remove_list):
    """Remove items from one list from another

    Args:
        base_list (list): list to keep the non-duplicated values from
        remove_list (list): list of items to remove from base_list

    Returns:
        list : list of items in base_list NOT in remove_list
    """    
    return [x for x in base_list if x not in remove_list]


def remove_empty_dict(dict_name):
    """Remove dict items with no values

    Args:
        dict_name (dict): dictionary to remove empty items from

    Returns:
        dict : dictionary with empty keys removed
    """    
    return_dict = {}
    
    for key in dict_name:
        if dict_name[key]:
            return_dict[key] = dict_name.get(key) 
    return return_dict

def wildcard_string_match(val,pattern,wildcard='?',wildcard_exclude=''):
    """Generate a TRUE / FALSE for matching the given value against a pattern. Enables wildcard searching & excludable characters from wildcard.

    Args:
        val (string): Value to check if matches.
        pattern (string): Pattern to check the val against.
        wildcard (str, optional): Wildcard character used in pattern. Defaults to '?'.
        wildcard_exclude (str, optional): Characters to exclude from wildcard. Defaults to ''.

    Returns:
        bool : TRUE == match, FALSE == no match
    """
    
    if len(val) == 0 or len(pattern) == 0:
        return True
    
    if val[0] in wildcard_exclude:
        return False
    elif pattern[0] == wildcard or pattern[0] == val[0]:
        return wildcard_string_match(val[1:],pattern[1:],wildcard,wildcard_exclude)
    else:
        return False
    
