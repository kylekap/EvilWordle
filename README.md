# It's a lot like [Wordle](https://www.powerlanguage.co.uk/wordle/), but... mean

## What it is
My attempt at recreating the experience of [:smiling_imp: Evil Wordle :smiling_imp:](https://swag.github.io/evil-wordle/) as a project in Python.


## Goal of the program

1. Take a random guess
2. Evaluate guess against all 5 letter words for what pattern has the most possible results
3. Inform user of how many words remain
4. Keep them guessing as long as possible

## To Do, Program
- [X] Identify issues in check_permutations, see function for details
- [ ] Idenfity issues in leaving guesses in available words for 1 loop too long
- [X] Initial release! :sparkler:
- [X] Add ability to give up :confounded:
- [X] Show letters guessed but not included :page_with_curl:
- [ ] Optimize guess evaluation time :hourglass:
- [ ] Deploy as webpage, see Flask to do list below
- [ ] \(Optional) Add ability to play against other lengths of words :straight_ruler:
- [X] \(Optional) Find more complete list of words :closed_book:

## To Do, Flask
- [ ] Add Flask support
- [ ] Instanced playthrough
- [ ] Solve caching issues
- [ ] Deploy online
- [ ] \(Optional) Generate GUI for playthrough?

## Resources utilized
1. [Primary Word List - Instructables](https://content.instructables.com/ORIG/FLU/YE8L/H82UHPR8/FLUYE8LH82UHPR8.tx)
2. [Secondary Word List - swag](https://github.com/swag/swag.github.io/blob/master/evil-wordle/js/wordlists.js)

<!--[Format Guideline](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)-->