
from flask import Flask, render_template, request, session, redirect, url_for
import os
from flask_caching import Cache
from cachetools import cached, TTLCache
import Project.core as core
import Project.core_utils as core_utils

app = Flask(__name__)
app.config["SECRET_KEY"] = str(os.urandom(24))


@app.route('/', methods=['GET', 'POST'])
def index():
    QTc_result = False
    if request.method == 'POST':
        form = request.form
        QTc_result = calculate_qtc(form)
    return render_template('index.html', QTc_result=QTc_result)

@app.route('/clear')
def logout():
    session.clear()
    return redirect(url_for('index'))

def calculate_qtc(form):
    all_words = core.get_words(use_file=r'Docs/5Words.CSV')
    possible_words = all_words #Wrong but temp

    exit_phrase = 'surrender'
    debug_phrase = 'thefuck'
    user_guess = request.form['user_guess']
    guess = core.get_guess(all_words,possible_words,guess=user_guess,exit_phrase=exit_phrase,debug_phrase=debug_phrase)    
    
    if 'guess_history' in session:
        session['guess_history'] = session['guess_history'].append(guess)
    else:
        session['guess_history'] = [guess]

    included_letters = ''
    result_set = core_utils.remove_empty_dict(core.check_permutation(core.guess_dict(guess),possible_words,guess))
        
    if not guess:
        return (result_set,False)
    else:
        return (session['guess_history'], True)


if __name__ == '__main__':
    app.run(port=5001,debug=True)
