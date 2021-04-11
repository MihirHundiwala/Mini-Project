
import pyrebase
from flask import Flask, render_template, app, request, session, redirect

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
app.secret_key = "super secret key"

@app.after_request
def add_header(r):
    
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/', methods = ['GET', 'POST'])

def basic():
    log = "Logged in"
    logfail = "Please Enter Correct Credentials"
    cre = "Account Created"
    crefail = "Account Not Created"
    session['logged_in'] = False
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['psw']
        if 'signin' in request.form:
            try:
                user = auth.sign_in_with_email_and_password(email, password) 
                session['logged_in'] = True
                return render_template('index.html', s=log)
            except:
                return render_template('index.html', us=logfail)

        if 'signup' in request.form:
            try:
                user = auth.create_user_with_email_and_password(email,password)
                user = auth.sign_in_with_email_and_password(email, password)
                session['logged_in'] = True
                return render_template('index.html', s=cre)
            except:
                return render_template('index.html', us=crefail)
    return render_template('index.html')

@app.route("/logout")

def logout():
    session['logged_in'] = False
    return redirect("/")
    # render_template("index.html")

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)
