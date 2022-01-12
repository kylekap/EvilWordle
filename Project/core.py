#https://realpython.com/python-pep8/

import requests
import itertools
import fnmatch
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
    for L in range(1,len(guess)+1):
        for subset in itertools.permutations(guess+'?????',5): #? for wildcards in fnmatch. Need 5 in case there are no correct letters selected
            g_dict[''.join(subset)] = []
    return g_dict


def check_permutation(perm_dict, possible_words):
    """[summary]

    Args:
        perm_dict ([type]): [description]
        possible_words ([type]): [description]

    Returns:
        [type]: [description]
    """
    #how to make faster?    
    for key in perm_dict:
        for word in possible_words:
            if fnmatch.fnmatch(word,key): #Currently including the other letters as a part of the wildcard... need to exclude.
                perm_dict[key].append(word)
            continue

    return perm_dict


def main():
    """[summary]
    """
    all_words = get_words()
    possible_words = all_words
    guess = get_guess(possible_words)
    a = check_permutation(guess_dict(guess),possible_words)
    for k in sorted(a, key=lambda k: len(a[k]), reverse=False):
        print(k,'With:',len(a.get(k)))
    #Find the item with the highest value, that's where the word lies
    #Then need to check if the guess has letters in the right positions or no

if __name__ == '__main__':
    """[summary]
    """    
    main()
