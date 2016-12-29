from flask import Flask, request, url_for, render_template, redirect, session
import requests
import json

app = Flask(__name__)
app.secret_key = 'this must be secret in order to protect the session'

api_host = 'http://localhost:8000/'


@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        r = requests.post(api_host + 'login', data={'username': username, 'password': password})
        data = json.loads(r.text)
        print(data['sessionid'])
        if(data['sessionid']!=""):
            session['sessionid'] = data['sessionid']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', last_was_wrong=True)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('sessionid', None)
    return redirect(url_for('login'))


@app.route('/')
def index():
    if 'sessionid' in session.keys() and session['sessionid'] != '':
        return render_template('index.html')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
