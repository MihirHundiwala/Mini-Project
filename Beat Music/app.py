import firebase_admin
from firebase_admin import credentials, firestore, storage, db
import re
import random
import json
import pyrebase
from flask import Flask, render_template, app, request, session, redirect, json, jsonify
from collections import OrderedDict
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
print("X")

app = Flask(__name__)
app.secret_key = "super secret key"

cred = credentials.Certificate('serviceAccount.json')
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

df = None


def getmatrix():

    dc = dict(refM.get())
    df = pd.DataFrame(dc)
    df = df.transpose()
    df = df.fillna(0)
    return df
    """ print(df) """


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
    if(usall != None):
        for v in usall.values():
            for k, v in usall.items():
                if k == "UserID":
                    usid.append(v)
        while True:
            uid = 'u' + str(random.sample(range(10000, 100000), 1)[0])
            if uid not in usid:
                break
    else:
        uid = 'u' + str(random.sample(range(10000, 100000), 1)[0])

    file_contents = {
        "UserID": uid,
        "email": email,
        "categories": [],
        "Playlist": []
    }
    usref.child(uid).set(file_contents)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        strm = request.form['strm']
        if strm == '' or strm == None:
            return ()
    retval = list()
    sear = ref.order_by_child('Genre').get()
    for val in sear.values():
        if re.search(strm, val['Title'], re.IGNORECASE) or re.search(strm, val['Album'], re.IGNORECASE) or re.search(strm, val['Artist'], re.IGNORECASE):
            retval.append(val)
    return json.dumps(tuple(retval))


def get_uid(email):
    usref = db.reference("/Users/")
    uid = ''
    userlist = usref.order_by_child('UserID').get()
    for z in userlist.values():
        if z['email'] == email:
            uid = z['UserID']
            break
    return uid


def popular_playlist():
    dc = dict(refM.get())
    df = pd.DataFrame(dc)
    df = df.transpose()
    playcount_df = dict(df.sum(axis=1))
    k = dict(sorted(playcount_df.items(), key=lambda x: x[1], reverse=True))
    k = list(k)
    k = k[0:10]
    top10 = []
    songs = dict(ref.get())
    for songid in k:
        top10.append(songs[songid])
    return top10


def load_myplaylist(uid):
    myplaylist = []
    try:
        p = list((usref.child(uid).child('Playlist').get()).values())
        for s in p:
            myplaylist.append(ref.child(s).get())
        return myplaylist
    except:
        myplaylist.append({'Title': 'Empty Playlist'})
        return myplaylist


def getsong(category):
    play = list()
    playli = ref.order_by_child('Genre').equal_to(category).get()
    for v in playli.values():
        play.append(v)
    return play


def add2queue(songid, uid):
    try:
        q = usref.child(uid).child('Queue').get()
        for x, y in q.items():
            if songid == y:
                usref.child(uid).child('Queue').child(x).delete()
                q.pop(x)
                break
        # usref.child(uid).child('Queue').push(songid)
        if len(q) == 15:
            q.pop(next(iter(q)))
        usref.child(uid).child('Queue').push(songid)
        return "done1"
    except:
        usref.child(uid).child('Queue').push(songid)
        return 'done2'


soulful = getsong('Soulful')
romance = getsong('Romance')
bollywoodparty = getsong('Bollywood Party')
pop = getsong('Pop')
hiphop = getsong('Hip-Hop, Rap')
oldsongs = getsong('Old Songs')

allsongs = [soulful, romance, bollywoodparty, pop, hiphop, oldsongs]

categories = {0: soulful,
              1: romance,
              2: bollywoodparty,
              3: pop,
              4: hiphop,
              5: oldsongs
              }

categories_s = {'Soulful': soulful,
                'Romance': romance,
                'Bollywood Party': bollywoodparty,
                'Pop': pop,
                'Hip-Hop, Rap': hiphop,
                'Old Songs': oldsongs
                }

top10 = popular_playlist()


@app.route('/addcount', methods=['POST', 'GET'])
def addcount():
    if request.method == "POST":
        songid = request.form['sid']
        uid = request.form['uid']
        # print("id:",songid)
        # uid = get_uid(email)
        try:
            count = refM.child(songid).child(uid).get()
            count = count + 1
            refM.child(songid).child(uid).set(count)
        except:
            refM.child(songid).child(uid).set(1)
        add2queue(songid, uid)
        return "successful"
    else:
        return "failed"


@app.route('/addtoqueue', methods=['POST', 'GET'])
def addtoqueue():
    if request.method == "POST":
        songid = request.form['sid']
        uid = request.form['uid']
        # uid = get_uid(email)
        add2queue(songid, uid)
    return 'successful'


@app.route('/removefromqueue', methods=['POST', 'GET'])
def removefromqueue():
    if request.method == "POST":
        songid = request.form['sid']
        uid = request.form['uid']
    q = usref.child(uid).child('Queue').get()
    for x, y in q.items():
        if songid == y:
            usref.child(uid).child('Queue').child(x).delete()
            break
    return 'successful'


@app.route('/home', methods=['GET', 'POST'])
def home():
    log = "Logged in"
    email = request.args.get('email')
    uid = get_uid(email)
    return render_template('index.html', uid=uid, email=email, s=log, sli=allsongs, previousplayli=json.dumps(top10), currentplayli=json.dumps(allsongs))


@app.route('/', methods=['GET', 'POST'])
def basic():
    email = None
    searli = list()
    log = "Logged in"
    logfail = "Please Enter Correct Credentials"
    cre = "Account Created"
    crefail = "Account Not Created"
    session['logged_in'] = False
    if request.method == 'POST':
        # dummy=None
        # dummy=request.form['dummy']
        # print(dummy)
        if 'signin' in request.form:
            email = request.form['email']
            password = request.form['psw']
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                session['logged_in'] = True
                uid = get_uid(email)
                initialqueue = []
                try:
                    k = list((usref.child(uid).child('Queue').get()).values())
                    if k == None or k == []:
                        initialqueue = top10
                    else:
                        songs = dict(ref.get())
                        for songid in k:
                            initialqueue.append(songs[songid])
                except:
                    initialqueue = top10
                getmatrix()
                return render_template('index.html', uid=uid, email=email, s=log, sli=allsongs, previousplayli=json.dumps(initialqueue), currentplayli=json.dumps(allsongs))
            except:
                print(str(e))
                return render_template('index.html', email=email, us=logfail, sli=allsongs, previousplayli=json.dumps(top10), currentplayli=json.dumps(allsongs))

        if 'signup' in request.form:
            email = request.form['email']
            # print(email)
            password = request.form['psw']
            categories = request.form.getlist('int_cat_chec')
            print(categories)
            try:
                user = auth.create_user_with_email_and_password(
                    email, password)
                auth.send_email_verification(user['idToken'])
                user = auth.sign_in_with_email_and_password(email, password)
                session['logged_in'] = True
                unetry(email)
                uid = get_uid(email)
                usref.child(uid).child('categories').set(categories)
                return render_template('index.html', uid=uid, email=email, s=cre, sli=allsongs, previousplayli=json.dumps(top10), currentplayli=json.dumps(allsongs))
            except Exception as e:
                print(str(e))
                return render_template('index.html', email=email, us=crefail, sli=allsongs, previousplayli=json.dumps(top10), currentplayli=json.dumps(allsongs))
    return render_template('index.html', email=email,  sli=allsongs, previousplayli=json.dumps(top10), currentplayli=json.dumps(allsongs))


@app.route("/reset_pwd", methods=['POST', 'GET'])
def reset_pwd():
    if request.method == 'POST':
        email = request.form['email']
    auth.send_password_reset_email(email)
    return 'sent email'


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect("/")


@app.route('/myplaylist', methods=['POST', 'GET'])
def myplaylist():
    if request.method == 'POST':
        uid = request.form['uid']
    # uid = get_uid(email)
    user_playlist = load_myplaylist(uid)
    # print(user_playlist)
    return json.dumps(user_playlist)


# @app.route('/playlist', methods=['POST', 'GET'])
# def playlist():
#     l = request.args.get('data')
#     l = l.split('=')
#     n = int(l[0])
#     i = int(l[1])
#     email = l[2]
#     uid = get_uid(email)
#     return render_template('PlaylistView.html', listtype="categories", uid=str(uid), email=email, i=i, sli=categories[n], previousplayli=json.dumps(allsongs[n]), currentplayli=json.dumps(categories[n]))


@app.route('/popular10', methods=['POST', 'GET'])
def popular10():
    top10 = popular_playlist()
    top10 = tuple(top10)
    return json.dumps(top10)


@app.route('/addtoplaylist', methods=['POST', 'GET'])
def addtoplaylist():
    if request.method == "POST":
        uid = request.form['uid']
        sid = request.form['sid']
    try:
        d = usref.child(uid).child('Playlist').get()
        p = list((d).values())
        if sid not in p:
            usref.child(uid).child('Playlist').push(sid)
        else:
            for x, y in d.items():
                if y == sid:
                    d = usref.child(uid).child('Playlist').child(x).delete()
                    break
            usref.child(uid).child('Playlist').push(sid)
        return "successful1"
    except Exception as e:
        print(str(e))
        usref.child(uid).child('Playlist').push(sid)
        return "successful2"


@app.route('/removefromplaylist', methods=['POST', 'GET'])
def removefromplaylist():
    if request.method == "POST":
        uid = request.form['uid']
        sid = request.form['sid']
    try:
        p = usref.child(uid).child('Playlist').get()
        for x, y in p.items():
            if y == sid:
                usref.child(uid).child('Playlist').child(x).delete()
                break
        return "successful1"
    except:
        return "successful2"


@app.route('/removefromrecommended', methods=['POST', 'GET'])
def removefromrecommended():
    if request.method == "POST":
        uid = request.form['uid']
        sid = request.form['sid']
    try:
        if sid not in list(usref.child(uid).child('Blacklist').get().values()):
            usref.child(uid).child('Blacklist').push(sid)
        return "successful1"
    except:
        usref.child(uid).child('Blacklist').set([])
        usref.child(uid).child('Blacklist').push(sid)
        return "successful2"


@app.route('/recommend', methods=['POST', 'GET'])
def recommend():

    if request.method == 'POST':
        uid = request.form['uid']

    rec_songs = []
    songs = dict(ref.get())

    # ----------------------Recommending based on user history-----------------
    try:
        queue = list(usref.child(uid).child('Queue').get().values())

        df = getmatrix()
        list_id = list(df.index)
        rec_list = []

        song_df_matrix = csr_matrix(df.values, dtype=float)

        model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
        model_knn.fit(song_df_matrix)

        for song in queue[-5:]:
            query_index = list_id.index(song)
            distances, indices = model_knn.kneighbors(
                df.iloc[query_index, :].values.reshape(1, -1), n_neighbors=3)

            for i in range(1, len(distances.flatten())):
                rec_list.append(df.index[indices.flatten()[i]])

    except Exception as e:
        print(str(e))
        pass

    # ------------------ Removing non-interested songs from recommendation ----------------
    try:
        blacklisted = list(usref.child(uid).child('Blacklist').get().values())
        for songid in blacklisted:
            rec_list = [sid for sid in rec_list if sid != songid]
    except Exception as e:
        print(str(e))
        pass

    for songid in rec_list:
        rec_songs.append(songs[songid])

    # ------------------Recommending based on user interested categories----------------
    try:
        int_cat = usref.child(uid).child('categories').get()
        for cat in int_cat:
            random_rec = random.sample(categories_s[cat], 3)
            for song in random_rec:
                rec_songs.append(song)
    except Exception as e:
        print(str(e))
        pass

    if rec_songs == []:
        return json.dumps(tuple(top10))

    return json.dumps(tuple(rec_songs))


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)
