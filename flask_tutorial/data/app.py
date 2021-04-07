
import pyrebase
from flask import Flask, render_template, app, request

config = {
    "apiKey": "AIzaSyCqK_WbCz4sM-cxqVgAZWARuNpSel7RaTs",
    "authDomain": "music-player-3dac7.firebaseapp.com",
    "projectId": "music-player-3dac7",
    "storageBucket": "music-player-3dac7.appspot.com",
    "messagingSenderId": "963378596642",
    "databaseURL": "https://music-player-3dac7-default-rtdb.firebaseio.com"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])

def basic():
    log = "Logged in"
    logfail = "Please Enter Correct Credentials"
    cre = "Account Created"
    crefail = "Account Not Created"
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['psw']
        if 'signin' in request.form:
            try:
                user = auth.sign_in_with_email_and_password(email, password) 
                return render_template('index.html', s=log)
            except:
                return render_template('index.html', us=logfail)

        if 'signup' in request.form:
            try:
                user = auth.create_user_with_email_and_password(email,password)
                return render_template('index.html', s=cre)
            except:
                return render_template('index.html', us=crefail)
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
