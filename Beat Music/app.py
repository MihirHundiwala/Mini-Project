import firebase_admin
from firebase_admin import credentials, firestore, storage, db
import re, random
import json
import pyrebase
from flask import Flask, render_template, app, request, session, redirect, json, jsonify
from collections import OrderedDict
import pandas as pd

app = Flask(__name__)
app.secret_key = "super secret key"

cred=credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://music-player-3dac7-default-rtdb.firebaseio.com'
})

config = {
    "apiKey": "AIzaSyCqK_WbCz4sM-cxqVgAZWARuNpSel7RaTs",
    "authDomain": "music-player-3dac7.firebaseapp.com",
    "projectId": "music-player-3dac7",
    "storageBucket": "music-player-3dac7.appspot.com",
    "messagingSenderId": "963378596642",
    "databaseURL": "https://music-player-3dac7-default-rtdb.firebaseio.com",
    "serviceAccount": "serviceAccount.json"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
ref = db.reference("/Songs/")
refM = db.reference("/SongMatrix/")
usref = db.reference("/Users/")

email = None

@app.after_request
def add_header(r):
    
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

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
                "Categories": [],
                "Playlist": []
    }
    usref.child(uid).set(file_contents)
    songs = refM.order_by_child('Song ID').get()
    for v in songs:
        refM.child(v).child(uid).set(random.choice([0,0,0,3,4,5,2,6]));

@app.route('/search' ,methods=['POST','GET'])
def search():
    if request.method=='POST':
        strm=request.form['strm']
        if strm=='' or strm==None:
            return ()
    retval = list()
    sear = ref.order_by_child('Genre').get()
    for val in sear.values():
        if re.search(strm, val['Title'], re.IGNORECASE) or re.search(strm, val['Album'], re.IGNORECASE) or re.search(strm, val['Artist'], re.IGNORECASE):
            retval.append(val)


            # if k == 'Title':
            #     if re.search(strm, v, re.IGNORECASE):
            #         retval.append(v)
            # if k == 'Album':
            #     if re.search(strm, v, re.IGNORECASE):
            #         retval.append(v)
            # if k == 'Artist':
            #     if re.search(strm, v, re.IGNORECASE):
            #         retval.append(v)
    return json.dumps(tuple(retval))

def get_uid(email):
    usref = db.reference("/Users/")
    uid = ''
    userlist = usref.order_by_child('UserID').get()
    for z in userlist.values():
        if z['email'] == email:
            uid = z['UserID']
    return uid

def popular_playlist():
    d=dict(refM.get())
    df=pd.DataFrame(d)
    df=df.transpose()
    playcount_df=dict(df.sum(axis=1))
    k = dict(sorted(playcount_df.items(),key=lambda x:x[1],reverse =True))
    k=list(k)
    k=k[0:10]
    top10=[]
    songs=dict(ref.get())
    for songid in k:
        top10.append(songs[songid])
    return top10

def load_myplaylist(uid):
    myplaylist=[]
    try:
        p=list((usref.child(uid).child('Playlist').get()).values())
        for s in p:
            myplaylist.append(ref.child(s).get())
        return myplaylist
    except:
        myplaylist.append({'Title':'Empty Playlist'})
        return myplaylist

def getsong(category):
    play = list()
    playli = ref.order_by_child('Genre').equal_to(category).get()
    for v in playli.values():
        play.append(v)
    return play

soulful=getsong('Soulful')
romance=getsong('Romance')
bollywoodparty=getsong('Bollywood Party')
pop=getsong('Pop')
hiphop=getsong('Hip-Hop, Rap')
oldsongs=getsong('Old Songs')

allsongs=[soulful,romance,bollywoodparty,pop,hiphop,oldsongs]

categories={    0:soulful,
                1:romance,
                2:bollywoodparty,
                3:pop,
                4:hiphop,
                5:oldsongs
            } 

top10=popular_playlist()

@app.route('/addcount' ,methods=['POST','GET'])
def addcount():
    if request.method == "POST":
        songid = request.form['songid']
        email=request.form['email']
        # print("id:",songid)
        uid = get_uid(email)
        prev=0
        songchild = refM.order_by_child('Song ID').equal_to(songid).get()
        for z in songchild.values():
            prev = int(z[uid])
        prev = prev + 1
        refM.child(songid).child(uid).set(prev)
        return "successful"
    else:
        return "failed"

@app.route('/home', methods = ['GET', 'POST'])
def home():
    log = "Logged in"
    email=request.args.get('email')
    return render_template('index.html', email=email, s=log, sli=allsongs, previousplayli=json.dumps(top10), currentplayli=json.dumps(allsongs))

@app.route('/', methods = ['GET', 'POST'])
def basic():
    email=None
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
                uid=get_uid(email)
                return render_template('index.html', email=email, s=log, sli=allsongs, previousplayli=json.dumps(top10), currentplayli=json.dumps(allsongs))
            except:
                return render_template('index.html', email=email, us=logfail, sli=allsongs, previousplayli=json.dumps(top10), currentplayli=json.dumps(allsongs))

        if 'signup' in request.form:
            email = request.form['email']
            # print(email)
            password = request.form['psw']
            try:
                user = auth.create_user_with_email_and_password(email,password)
                user = auth.sign_in_with_email_and_password(email, password)
                session['logged_in'] = True
                auth.send_email_verification(user['idToken'])
                unetry(email)
                uid=get_uid(email)
                # print("UID: ",uid) 
                return render_template('index.html', email=email, s=cre, sli=allsongs, previousplayli=json.dumps(top10), currentplayli=json.dumps(allsongs))
            except Exception as e:
                # print(str(e))
                return render_template('index.html', email=email, us=crefail, sli=allsongs, previousplayli=json.dumps(top10), currentplayli=json.dumps(allsongs))
    return render_template('index.html', email=email,  sli=allsongs, previousplayli=json.dumps(top10), currentplayli=json.dumps(allsongs))

@app.route("/reset_pwd", methods=['POST','GET'])
def reset_pwd():
    
    auth.send_password_reset_email(email)
    return redirect('/')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect("/")

@app.route('/myplaylist' ,methods=['POST','GET'])
def myplaylist():
    if request.method=='POST':
        email=request.form['email']
    uid=get_uid(email)
    user_playlist=load_myplaylist(uid)
    # print(user_playlist)
    return json.dumps(user_playlist)

@app.route('/playlist' ,methods=['POST','GET'])
def playlist():
    l = request.args.get('data')
    l=l.split('=')
    n=int(l[0])
    i=int(l[1])
    email=l[2]
    uid=get_uid(email)
    return render_template('PlaylistView.html',listtype="categories", uid=str(uid), email=email, i=i, sli=categories[n], previousplayli=json.dumps(allsongs[n]) ,currentplayli=json.dumps(categories[n]))


@app.route('/popular10', methods=['POST','GET'])
def popular10():
    email=request.args.get('email')
    top10=popular_playlist()
    top10=tuple(top10)
    return json.dumps(top10)

@app.route('/addtoplaylist', methods=['POST','GET'])
def addtoplaylist():
    if request.method == "POST":
        uid=request.form['uid']
        sid=request.form['sid']
    # print(sid,uid)
    try:
        p=list((usref.child(uid).child('Playlist').get()).values())
        if sid not in p:
            usref.child(uid).child('Playlist').push(sid);
        return "successful1"
    except:
        usref.child(uid).child('Playlist').push(sid);
        return "successful2"

@app.route('/removefromplaylist', methods=['POST','GET'])
def removefromplaylist():
    if request.method == "POST":
        uid=request.form['uid']
        sid=request.form['sid']
    # print(sid,uid)
    try:
        p=usref.child(uid).child('Playlist').get()
        for x,y in p.items():
            if y==sid:
                usref.child(uid).child('Playlist').child(x).delete();
        return "successful1"
    except:
        return "successful2"

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)

