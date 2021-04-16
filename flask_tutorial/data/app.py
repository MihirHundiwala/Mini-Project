import threading
import firebase_admin
from firebase_admin import credentials, firestore, storage, db
import re, random
from collections import OrderedDict
import json

cred=credentials.Certificate('env\serviceAccount.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://music-player-3dac7-default-rtdb.firebaseio.com'
})

# usref = db.reference("/Songs/")
# usid = list()
# usall = usref.order_by_child('Genre').get()
# for v in usall.values():
#     for k,v in usall.items():
#         if k == "ID":
#             print(k)
#             usid.append(v)
# print(usid)
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

# ref = db.reference("/SongMatrix/")
# # for i in usid:
# #     file_contents = {
# #     "SongID": i,
# #     "PlayCount": 0,
# #     "UserID": "u11914"
# #     }
# with open("data\play2.json", "r") as f:
# 	file_contents = json.load(f)
# ref.set(file_contents)

""" ref = db.reference("/SongMatrix/")

with open("data\play_count.json", "r") as f:

    file_contents = json.load(f)

ref.set(file_contents) """


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
    catg = ['Soulful', 'Bollywood Party', 'Romance', 'Old Songs', 'Hip-Hop, Rap', 'Pop']
    slist = []
    blist = []
    rlist = []
    olist = []
    hlist = []
    plist = []
    allist = []
    for i in catg:
        songs = ref.order_by_child('Genre').equal_to(i).get()
        for val in songs.values():
            for k,v in val.items():
                if k == 'Title':
                    name = v
                if k == 'Path':
                    path = v
                if k == 'Artist':
                    artist = v
                if k == 'Album':
                    album = v
                if k == 'Genre':
                    genre = v
            if i == 'Soulful':
                slist.append({'Title':name, 'Path':path, 'Artist':artist, 'Album':album, 'Genre':genre}) 
            if i == 'Bollywood Party':
                blist.append({'Title':name, 'Path':path, 'Artist':artist, 'Album':album, 'Genre':genre}) 
            if i == 'Romance':
                rlist.append({'Title':name, 'Path':path, 'Artist':artist, 'Album':album, 'Genre':genre}) 
            if i == 'Old Songs':
                olist.append({'Title':name, 'Path':path, 'Artist':artist, 'Album':album, 'Genre':genre}) 
            if i == 'Hip-Hop, Rap':
                hlist.append({'Title':name, 'Path':path, 'Artist':artist, 'Album':album, 'Genre':genre}) 
            if i == 'Pop':
                plist.append({'Title':name, 'Path':path, 'Artist':artist, 'Album':album, 'Genre':genre})  
    allist.append(slist)
    allist.append(rlist)
    allist.append(blist)
    allist.append(plist)
    allist.append(hlist) 
    allist.append(olist)       
    return allist

def unetry(email):
    usid = list()
    usall = usref.order_by_child('UserID').get()
    if(usall!=None):
        for v in usall.values():
            for k,v in usall.items():
                if k == "UserID":
                    usid.append(v)
        while True:
            uid = 'u' + str(random.sample(range(10000,100000),1)[0])
            if uid not in usid:
                break
    else:
        uid = 'u' + str(random.sample(range(10000,100000),1)[0])

    file_contents = {
                "UserID": uid,
                "email": email,
                "Categories": " ",
                "Playlist": " "
    }
    usref.child(uid).set(file_contents)

    ref = db.reference("/SongMatrix/")
    songs = ref.order_by_child('SongID').get()
    for v in songs:
        ref.child(v).child(uid).set("0");


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
    playli = ref.order_by_child('Genre').equal_to('Soulful').get()
    for v in playli.values():
        play.append(v)
    play = str(play)
    play = play.replace("\'","\"")
    return play

def addcount():
    if request.method == "POST":
        data = request.form['songid']
        print(data)
    return render_template('index.html',  sli=songs(), playli=getsong())

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
                session['logged_in'] = True
                auth.send_email_verification(user['idToken'])
                threading.Thread(target=unetry(email)).start() 
                """ unetry(email) """
                #   reset the password
                #   auth.send_password_reset_email(email)
                return render_template('index.html', s=cre, sli=sli, playli=getsong())
            except:
                return render_template('index.html', us=crefail, sli=sli, playli=getsong())
        if 'search' in request.form:
            searli = search(request.form['songsearch'])
            print(searli)
            return render_template('index.html', sli=sli, searli=searli, playli=getsong())
    addcount()
    return render_template('index.html',  sli=sli, playli=getsong())


@app.route("/logout")

def logout():
    session['logged_in'] = False
    return redirect("/")

@app.route('/playlist')
def playlist():
    return render_template('PlaylistView.html',sli=songs())

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)
