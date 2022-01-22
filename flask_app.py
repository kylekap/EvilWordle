from flask import Flask, render_template, request
import os
import math
import Project.core as core
import Project.core_utils as core_utils

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    QTc_result = False

    if request.method == 'POST':
        form = request.form
        QTc_result = calculate_qtc(form)
    return render_template('index.html', QTc_result=QTc_result)


def calculate_qtc(form):
    guess_history = []
    all_words = core.get_words(use_file=r'Docs/5Words.CSV')
    possible_words = all_words #Wrong but temp
    exit_phrase = 'surrender'
    debug_phrase = 'thefuck'
    user_guess = request.form['user_guess']
    guess = core.get_guess(all_words,possible_words,guess=user_guess,exit_phrase=exit_phrase,debug_phrase=debug_phrase)    

    guess_history.append(guess)
    included_letters = ''
    result_set = core_utils.remove_empty_dict(core.check_permutation(core.guess_dict(guess),possible_words,guess))
    
    if not guess:
        return (result_set,False)
    else:
        return (guess_history, True)


if __name__ == '__main__':
    app.run(port=5001,debug=True)