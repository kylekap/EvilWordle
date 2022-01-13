#https://realpython.com/python-pep8/

import requests
import itertools
import fnmatch
import re
import time
import csv 


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
        for subset in itertools.permutations(guess+'?????',5): #? for wildcards. Need 5 in case there are no correct letters selected
            g_dict[''.join(subset)] = []
    return g_dict


def removeDupWithoutOrder(str): 
    return "".join(set(str)) 


def check_permutation(perm_dict, possible_words,guess):
    """[summary]

    Args:
        perm_dict ([type]): [description]
        possible_words ([type]): [description]

    Returns:
        [type]: [description]
    """
    #how to make faster?
    for key in perm_dict:
        except_letters = ''
        for letter in guess:
            if letter not in key:
                except_letters=removeDupWithoutOrder(except_letters+letter)
        expr = key.replace('?',f'[^{except_letters}]')
        for word in possible_words:
            if None != re.match(expr,word):
               perm_dict[key].append(word)
               
    return perm_dict


def check_positional(actual,guess,included_letters):
    val = {'match':'','others':included_letters}
    for pos in range(0,len(guess)):
        if actual[pos] == guess[pos]: #If it's in the right spot, make sure to include it & remove from wrong pos letters.
            val['match'] = val.get('match','')+actual[pos]
            val['others'] = val.get('others','').replace(actual[pos],'')
        elif guess[pos] in actual: #if in the word but NOT right spot, list it
            val['others']= removeDupWithoutOrder(val.get('others','')+guess[pos])
            val['match']= val.get('match','')+'?'
        else: #if not at all right spot, keep the spot blank
            val['match']= val.get('match','')+'?'
    return val

def main():
    """[summary]
    """
    guess_history = []
    starttime = time.time()
    all_words = get_words()
    possible_words = all_words

    while True:
        guess = get_guess(possible_words)
        guess_history.append(guess)
        included_letters = ''
        result_set = check_permutation(guess_dict(guess),possible_words,guess)
        max_key = max(result_set, key= lambda x: len(set(result_set[x])))
        included_letters = max_key.replace('?','')
        possible_words = result_set.get(max_key)

        #Then need to check if the guess has letters in the right positions or no
        return_prompt = check_positional(max_key,guess,included_letters)
        a = return_prompt.get('match','?????')
        b = return_prompt.get('others','')
        c = len(result_set.get(max_key))
        print(f'Current correct letters: {a}\nCurrent correct but non-ordered letters: {b}\nPossible words left: {c}')
        print(result_set.get(max_key))
        if c == 1:
            print(f'Drat. You got it... the word was {a}')
            break
        else:
            continue
    
    #End Loop
    print(time.time()-starttime)

if __name__ == '__main__':
    """[summary]
    """    
    main()
