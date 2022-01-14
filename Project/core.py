#https://realpython.com/python-pep8/

import requests
import itertools
import re

#import config


def get_words(min_length=5,max_length=5,capitalization='lower'):
    """Gets a list of english words from instructables of a desired length.

    Args:
        min_length (int, optional): Keep words of this length or longer. Defaults to 5.
        min_length (int, optional): Keep words of this length or shorter. Defaults to 5.
        capitalizaton (string, optional): Capitalization rules of the word list to return (lower, upper, title). Defaults to lower.

    Returns:
        List: returns a lower case list of words meeting length requirements.
    """
    WordList = []
    InitialList = requests.get("https://content.instructables.com/ORIG/FLU/YE8L/H82UHPR8/FLUYE8LH82UHPR8.txt").text
    InitialList = str.splitlines(InitialList)
    for word in InitialList:
        if len(word) >= min_length and len(word) <= max_length:
            if capitalization.lower() == 'upper':
                WordList.append(word.upper())
            elif capitalization.lower() == 'title':
                WordList.append(word.title())
            else:
                WordList.append(word.lower())
    return WordList


def get_guess(possible_answers,a=''):
    """Ask for a user input. Reject every input that's not in the list of possible_answers. Will format in same way (lower,upper,title) as possible_answers

    Args:
        possible_answers (list): list of acceptable inputs (string)
        case () : case of output desired. Defaults to same as possible_answers case style
    Returns:
        string : users validated input in specified format
    """
    if a != '' and a.lower().isin(['lower','upper','title']):
        a = a
    elif possible_answers[0].isupper():
        a = 'upper'
    elif possible_answers[0].istitle():
        a = 'title'
    else:
        a = 'lower'

    possible_answers = (map(lambda x: x.lower(), possible_answers))
    while True:
        guess = str(input("Enter a 5 Letter word: ")).lower()
        
        if guess in set(possible_answers):
            break
        else:
            print("Must pick a valid 5 letter word!\n")
    
    if a == 'upper':
        return guess.upper()
    elif a == 'title':
        return guess.title()
    else:
        return guess.lower()
    

def guess_dict(guess,wildcard_char='?'):
    """Get a dictionary of possible things / combinations that the guess word could make. Example 'arise' has '????e' and 'er???'

    Args:
        guess (string): word to generate the combinations with
        wildcard_char (string, optional): wildcard character to use. Defaults to '?'

    Returns:
        dictionary: dictionary where each key is a different combination, and the value is an empty string 
    """    
    g_dict = {}
    for L in range(1,len(guess)+1):
        for subset in itertools.permutations(guess+f'{wildcard_char}'*5,5): #? for wildcards. Need 5 in case there are no correct letters selected
            g_dict[''.join(subset)] = []
    return g_dict


def removeDupWithoutOrder(str):
    """Remove duplicates from a string. Order will not be preserved

    Args:
        str (string): string to remove duplicate values from

    Returns:
        string : Duplicate free string
    """    
    return "".join(set(str)) 


def check_permutation(perm_dict, possible_words,guess,wildcard_char='?'):
    """[summary]

    Args:
        perm_dict (dict): Keys are the combinations of letters to use. Will regex match wildcard characters to find matches in possible_words
        possible_words (list): List of remaining words to distribute among the perm_dict
        guess (string): Users guess
        wildcard_char (string, optional): wildcard character in the keys of the perm_dict. Defaults to ?

    Returns:
        dict : perm_dict filled out with values being lists of words from possible_words that correlate to that key.
    """    
    #how to make faster?
    try:
        for key in perm_dict:
            except_letters = ''
            for letter in guess:
                if letter not in key:
                    except_letters=removeDupWithoutOrder(except_letters+letter)
            if except_letters == '':
                expr = key.replace('?',f'.')
            else:
                expr = key.replace('?',f'[^{except_letters}]')
            for word in possible_words:
                if None != re.match(expr,word):
                   perm_dict[key].append(word)
    except Exception as E:
        print(f'{key}\n{except_letters}\nhad regex: {expr}\nand gave error: {E}')
    return perm_dict


def check_positional(actual,guess,included_letters):
    """Check if the positions of the guess line up with the actual words left.

    Args:
        actual (string): string of the actual answer (wildcards for non-locked down spots)
        guess (string): Users original guess
        included_letters (string): letters required to be in final solution

    Returns:
        dict : dictionary with characters that 'match' and those that are in the solution but not in right position 'others'
    """    
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
    all_words = get_words()
    possible_words = all_words

    while True:
        guess = get_guess(all_words)
        guess_history.append(guess)
        included_letters = ''
        result_set = check_permutation(guess_dict(guess),possible_words,guess)
        max_key = max(result_set, key= lambda x: len(set(result_set[x]))) #Need to fix what happens at 1 option as max key, currently accepts that as final, need to keep them guessing if possible?
        included_letters = max_key.replace('?','')
        possible_words = result_set.get(max_key)

        #Then need to check if the guess has letters in the right positions or no
        return_prompt = check_positional(max_key,guess,included_letters)
        a = return_prompt.get('match','?????')
        b = return_prompt.get('others','')
        c = len(result_set.get(max_key))
        print(f'Current correct letters: {a}\nCurrent correct but non-ordered letters: {b}\nPossible words left: {c}')
        #print(result_set.get(max_key))
        if c == 1:
            print(f'Drat. You got it... the word was {a}')
            break
        else:
            continue

if __name__ == '__main__':
    """[summary]
    """    
    main()
