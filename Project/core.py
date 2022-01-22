#Python code writing guidelines
#https://realpython.com/python-pep8/
#https://docs.python-guide.org/writing/structure/

#Imported functions
import requests
import itertools
import re
import csv

#Local utilities
#import Project.
import core_utils as core_utils

def get_words(min_length=5,max_length=5,capitalization='lower',use_file=''):
    """Gets a list of english words from instructables of a desired length.

    Args:
        min_length (int, optional): Keep words of this length or longer. Defaults to 5.
        min_length (int, optional): Keep words of this length or shorter. Defaults to 5.
        capitalizaton (string, optional): Capitalization rules of the word list to return (lower, upper, title). Defaults to lower.
        use_local (boolean, optional): Alternatively, use a local copy for faster reference

    Returns:
        List: returns a lower case list of words meeting length requirements.
    """
    WordList = []

    if len(use_file) > 0:
        with open(f'Docs/{max_length}Words.csv', newline='') as f:
            for row in csv.reader(f):
                WordList.append(row[0])
    else:
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


def get_guess(possible_guesses,remaining_words,word_case='',exit_phrase='',debug_phrase='',guess=''):
    """Ask for a user input. Reject every input that's not in the list of possible_answers. Will format in same way (lower,upper,title) as possible_answers

    Args:
        possible_answers (list): list of acceptable inputs (string)
        word_case (string, optional) : case of output desired. Defaults to same as possible_answers case style. lower/upper/title
        exit_phrase (string, optional): phrase/word to exit the input loop.
        
    Returns:
        string : users validated input in specified format. Will return exit_phrase when utilized.
    """
    
    if word_case != '' and word_case.lower().isin(['lower','upper','title']):
        a = word_case
    elif possible_guesses[0].isupper():
        a = 'upper'
    elif possible_guesses[0].istitle():
        a = 'title'
    else:
        a = 'lower'

    possible_answers = list(map(lambda x: x.lower(), possible_guesses))

    #print(f"You can always type '{exit_phrase}' to give up")
    if guess == '':
        while True:
            guess = str(input("Enter a 5 Letter word: ")).lower()
        
            if guess.lower() == exit_phrase.lower():
                return exit_phrase
            if guess.lower() == debug_phrase.lower():
                print(remaining_words)
            elif guess in possible_guesses:
                break
            else:
                print("Must pick a valid 5 letter word!\n")
    elif guess in possible_guesses:
        return guess
    else:
        return False
    
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
    #I think there might be an error in here, where if you guess a word like "catch" it'll leave in "cooch" but then say only one matches. 
        # Think it's the double letters on inputs that's messing it up
    try:
        for key in perm_dict:
            except_letters = core_utils.return_unused_chars(guess,key)
            except_letters=core_utils.removeDupWithoutOrder(except_letters)
            if except_letters == '':
                expr = key.replace('?',f'.')
            else:
                expr = key.replace('?',f'[^{except_letters}]')

            rx = re.compile(expr)
            perm_dict[key] = list(filter(rx.match,possible_words))

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
    #I think there might be an error in here, where if you guess a word like "catch" it'll leave in "cooch" but then say only one matches. 
        # Think it's the double letters on inputs that's messing it up
    val = {'match':'','others':included_letters}
    for pos in range(0,len(guess)):
        if actual[pos] == guess[pos]: #If it's in the right spot, make sure to include it & remove from wrong pos letters.
            val['match'] = val.get('match','')+actual[pos]
            val['others'] = val.get('others','').replace(actual[pos],'')
        elif guess[pos] in actual: #if in the word but NOT right spot, list it
            val['others']= core_utils.removeDupWithoutOrder(val.get('others','')+guess[pos])
            val['match']= val.get('match','')+'?'
        else: #if not at all right spot, keep the spot blank
            val['match']= val.get('match','')+'?'
    return val


def incorrect_letters(guess_hist,included_letters):
    letters = core_utils.removeDupWithoutOrder(''.join(guess_hist))
    bad_letters = ''
    for lett in letters:
        if lett not in included_letters:
            bad_letters = bad_letters+lett
    return ''.join(sorted(bad_letters))


def unused_letters(letters):
    """Retuns all letters not in the input string

    Args:
        letters (string): letters already utilized (do not include)

    Returns:
        string : letters not in input
    """    
    letters_left = 'abcdefghijklmnopqrstuvwxyz'
    
    letters = core_utils.removeDupWithoutOrder(letters)
    
    for letter in letters:
        letters_left = letters_left.replace(letter,'')
    
    return letters_left


def main():
    """[summary]
    """
    #start_time = time.time()
    guess_history = []
    all_words = get_words(use_file=r'Docs/5Words.CSV')
    possible_words = all_words
    included_letters = ''
    
    while True:
        exit_phrase = 'surrender'
        guess = get_guess(all_words,possible_words,exit_phrase=exit_phrase,debug_phrase='thefuck')
        if guess == exit_phrase:
            print('Giving up so soon? See you next time!')
            break
        #last_time = time.time()
        guess_history.append(guess) #Track history of guesses

        #get the dictionary of possible word formats, removing any with no words left.
        result_set = core_utils.remove_empty_dict(check_permutation(guess_dict(guess),possible_words,guess)) 

        #Find longest & shorted of the word formats. Will be 1 or greater, since removed empty above.        
        max_key = max(result_set, key= lambda x: len(set(result_set[x])))
        min_key = min(result_set, key= lambda x: len(set(result_set[x])))

        '''
        existing err....->
        Last guess words left ['molls', 'polls']
        guessed polls
        Last Guess letters in right position: polls
        Last Guesses included letters, wrong spot: molls
        '''
        #if we're down to 1 option per set, need to switch up logic to keep user guessing, otherwise maintain logic.
        if len(result_set.get(min_key)) == len(result_set.get(max_key)) and len(result_set.get(max_key))==1:
            possible_words = []
            for key in result_set:
                possible_words.append(result_set.get(key)[0])
        else:
            possible_words = result_set.get(max_key)
        
        #remove all guessed words.
        #Err -> leaving in last guess?
        possible_words = core_utils.removeListDups(possible_words,guess_history)
        if guess in possible_words:
            possible_words.remove(guess)

        #Find what letters belong where, if they're included or not
        included_letters = core_utils.shared_letters(possible_words,guess)
        non_included_letters = incorrect_letters(guess_history,included_letters).replace('?','')
        unused = unused_letters(included_letters+non_included_letters)
        
        #Then to check if the guess has letters in the right positions or no
        return_prompt = check_positional(included_letters,guess,included_letters.replace('?',''))
        included_letters = included_letters.replace('?','')
        a = return_prompt.get('match','?????')
        c = len(possible_words)
        
        if c == 0:#no more possible words
            print(f'Drat. You got it... the word was {a}')
            break

        print(f'Last Guess letters in right position: {a}\nLast Guesses included letters, wrong spot: {included_letters}\
              \nIncorrect letters: {non_included_letters}\nUnused letters: {unused}\nPossible words left: {c}') 
            #\nTimeTaken iteration {round(time.time()-last_time,2)}, Overall {round(time.time()-start_time,2)}')


if __name__ == '__main__':
    """[summary]
    """    
    main()
