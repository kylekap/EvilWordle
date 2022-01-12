#https://realpython.com/python-pep8/

import requests
import itertools

import config


def get_words():
    """[summary]

    Returns:
        [type]: [description]
    """    
    WordList = []
    InitialList = requests.get("https://content.instructables.com/ORIG/FLU/YE8L/H82UHPR8/FLUYE8LH82UHPR8.txt").text
    InitialList = str.splitlines(InitialList)
    for word in InitialList:
        if len(word) == 5:
            WordList.append(word.lower())
    return WordList


def get_guess(possible_words):
    """[summary]

    Args:
        possible_words ([type]): [description]

    Returns:
        [type]: [description]
    """    
    while True:
        guess = str(input("Enter a 5 Letter word:")).lower()
        if guess in set(possible_words):
            break
        else:
            print("Must pick a valid 5 letter word!")
    return guess
    

def guess_dict(guess):
    """[summary]

    Args:
        guess ([type]): [description]

    Returns:
        [type]: [description]
    """    
    g_dict = {}
    for L in range(1,len(''.join(set(guess)))+1):
        for subset in itertools.combinations(guess,L):
            g_dict[''.join(subset)] = []
    return g_dict


def check_with(letter_dict, possible_words):
    """[summary]

    Args:
        letter_dict ([type]): [description]
        possible_words ([type]): [description]

    Returns:
        [type]: [description]
    """    
    for word in possible_words:
        for key in letter_dict:
            if set(list(key)).issubset(list(word)):
                letter_dict[key].append(word)
    return letter_dict


def check_without(letter_dict, possible_words):
    """[summary]

    Args:
        letter_dict ([type]): [description]
        possible_words ([type]): [description]

    Returns:
        [type]: [description]
    """    
    for word in possible_words:
        for key in letter_dict:
            if not set(list(key)).issubset(list(word)):
                letter_dict[key].append(word)
    return letter_dict


def check_position(letter, possible_words):
    """[summary]

    Args:
        letter ([type]): [description]
        possible_words ([type]): [description]

    Returns:
        [type]: [description]
    """
    pos_dict = {}
    
    for pos in range(1,6-len(letter)):
        next_pos = pos+len(letter)
        for word in possible_words:
            if word[pos:next_pos] == letter:            
                pos_dict[pos].append(word)
                continue
    return pos_dict


def main():
    """[summary]
    """
    all_words = get_words()
    possible_words = all_words
    #loop here
    guess = get_guess(possible_words)
    a = check_with(guess_dict(guess),possible_words)
    b = check_without(guess_dict(guess),possible_words)
    for key in a:
        print(key,'With:',len(a.get(key)),'Without:',len(b.get(key)))


if __name__ == '__main__':
    """[summary]
    """    
    main()
