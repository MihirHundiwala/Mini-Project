import firebase_admin
from firebase_admin import credentials, firestore, storage, db
import re, random
from collections import OrderedDict

cred=credentials.Certificate('env\serviceAccount.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://music-player-3dac7-default-rtdb.firebaseio.com'
})
# usref = db.reference("/Users/")
# usid = list()
# usall = usref.order_by_child('UserID').get()
# for v in usall.values():
#     for k,v in usall.items():
#         if k == "UserID":
#             usid.append(v)
# while True:
#     uid = 'u' + str(random.sample(range(10000,100000),1)[0])
#     if uid not in usid:
#         break
# email = "patilgayatri086@gmail.com"
# file_contents = {
#             "UserID": uid,
#             "email": email,
#             "Categories": " ",
#             "Playlist": " "
# }
# usref.child(uid).set(file_contents)

# ref = db.reference("/Users/")
# file_contents = {
#     "User1":{
#         "email": "patil.gv@somaiya.edu"
#     }
# }
# ref.set(file_contents)

import pyrebase
from flask import Flask, render_template, app, request, session, redirect, json
from collections import OrderedDict

config = {
    "apiKey": "AIzaSyCqK_WbCz4sM-cxqVgAZWARuNpSel7RaTs",
    "authDomain": "music-player-3dac7.firebaseapp.com",
    "projectId": "music-player-3dac7",
    "storageBucket": "music-player-3dac7.appspot.com",
    "messagingSenderId": "963378596642",
    "databaseURL": "https://music-player-3dac7-default-rtdb.firebaseio.com",
    "serviceAccount": "env\serviceAccount.json"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
ref = db.reference("/Songs/")
usref = db.reference("/Users/")

app = Flask(__name__)
app.secret_key = "super secret key"

@app.after_request
def add_header(r):
    
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
#@app.route('/')

def songs():
    songs = ref.order_by_child('Genre').equal_to('Bollywood Party').get()
    slist = list()
    for val in songs.values():
        for k,v in val.items():
            if k == 'Title':
                name = v
        slist.append(name)
    return slist


def unetry(email):
    usid = list()
    usall = usref.order_by_child('UserID').get()
    for v in usall.values():
        for k,v in usall.items():
            if k == "UserID":
                usid.append(v)
    while True:
        uid = 'u' + str(random.sample(range(10000,100000),1)[0])
        if uid not in usid:
            break
    file_contents = {
                "UserID": uid,
                "email": email,
                "Categories": " ",
                "Playlist": " "
    }
    usref.child(uid).set(file_contents)


def search(strm):
    retval = list()
    sear = ref.order_by_child('Genre').get()
    for val in sear.values():
        for k,v in val.items():
            if k == 'Title':
                if re.search(strm, v, re.IGNORECASE):
                    retval.append(v)
            if k == 'Album':
                if re.search(strm, v, re.IGNORECASE):
                    retval.append(v)
            if k == 'Artist':
                if re.search(strm, v, re.IGNORECASE):
                    retval.append(v)
    return retval
        


def getsong():
    play = list()
    playli = ref.order_by_child('Genre').equal_to('Soulful').limit_to_last(5).get()
    for v in playli.values():
        play.append(v)
    # play = json.loads(play)
    play = str(play)
    play = play.replace("\'","\"")
    return play


@app.route('/', methods = ['GET', 'POST'])
def basic():
    sli = list()
    sli = songs()
    searli = list()
    log = "Logged in"
    logfail = "Please Enter Correct Credentials"
    cre = "Account Created"
    crefail = "Account Not Created"
    session['logged_in'] = False
    if request.method == 'POST':        
        if 'signin' in request.form:
            email = request.form['email']
            password = request.form['psw']
            try:
                user = auth.sign_in_with_email_and_password(email, password)                 
                session['logged_in'] = True
                return render_template('index.html', s=log, sli=sli, playli=getsong())
            except:
                return render_template('index.html', us=logfail, sli=sli, playli=getsong())

        if 'signup' in request.form:
            email = request.form['email']
            password = request.form['psw']
            try:
                user = auth.create_user_with_email_and_password(email,password)
                user = auth.sign_in_with_email_and_password(email, password)
                auth.send_email_verification(user['idToken']) 
                unetry(email)
                  #reset the password
                #   auth.send_password_reset_email(email)
                session['logged_in'] = True
                return render_template('index.html', s=cre, sli=sli, playli=getsong())
            except:
                return render_template('index.html', us=crefail, sli=sli, playli=getsong())
        if 'search' in request.form:
            searli = search(request.form['songsearch'])
            print(searli)
            return render_template('index.html', sli=sli, searli=searli, playli=getsong())
    #getsong()
    return render_template('index.html',  sli=sli, playli=getsong())


@app.route("/logout")

def logout():
    session['logged_in'] = False
    return redirect("/")
    # render_template("index.html")

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)
