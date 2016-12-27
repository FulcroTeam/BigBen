from flask import Flask, request, url_for, render_template, redirect, session

app = Flask(__name__)
app.secret_key = 'stringa segreta'


@app.route("/login", methods=['GET', 'POST'])
def login(name=None):

    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        session['username'] = request.form.get('username')
        session['password'] = request.form.get('password')
        return redirect(url_for('index'))

    return redirect(url_for('index'))


@app.route('/')
def index():
    if 'username' in session.keys() and session['username'] != '':
        return render_template('index.html')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
