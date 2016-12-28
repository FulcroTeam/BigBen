from flask import Flask, request, url_for, render_template, redirect, session
import requests
import json

app = Flask(__name__)
app.secret_key = 'stringa segreta'


@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        username = request.form.get('username')
        pin = request.form.get('password')
        r = requests.post('http://localhost:8000/login/', data={'username': username, 'password': pin})
        data = json.loads(r.text)
        print(data['response'])
        if(data['response']==1):
            return redirect(url_for('index'))
        else:
            return render_template('login.html')
    return redirect(url_for('login'))


@app.route('/')
def index():
    if 'username' in session.keys() and session['username'] != '':
        return render_template('index.html')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
