from flask import Flask, session, redirect, url_for, escape, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.urandom(24))

@app.route('/')
def main():
    if 'username' in session:
        return 'You are already logged in as %s' % escape(session['username'])
            # Escape special HTML characters (such as <, >) in echoing to prevent XSS
    return (redirect(url_for('login')))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # For subsequent POST requests
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username   # Save in session
        return 'Logined in as %s' % escape(username)

    # For the initial GET request
    return '''
        <form method='POST'>
          Enter your name: <input type='text' name='username'>
          <input type='submit' value='Login'>
        </form>'''

@app.route('/logout')
def logout():
    # Remove 'username' from the session if it exists
    session.pop('username', None)
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(port=5001,debug=True)