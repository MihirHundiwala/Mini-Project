var firebaseConfig = {
apiKey: "AIzaSyCqK_WbCz4sM-cxqVgAZWARuNpSel7RaTs",
authDomain: "music-player-3dac7.firebaseapp.com",
databaseURL: "https://music-player-3dac7-default-rtdb.firebaseio.com",
projectId: "music-player-3dac7",
storageBucket: "music-player-3dac7.appspot.com",
messagingSenderId: "963378596642",
appId: "1:963378596642:web:d37ac0d74fcf52d985f37b",
measurementId: "G-6828SD4S6R"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

var usref = firebase.database().ref("/Users/");

let uid = $('#uid').data('uid');
console.log(uid);
// let songM = firebase.database().ref("/SongMatrix/");
// let usersT = firebase.database().ref("/Users/");

// function increase_song_count()
// {
//     let prev = 0 
//     songchild = songM.order_by_child('Song ID').equal_to(songid).get()
//     for z in songchild.values():
//        prev = int(z[uid])
    
//     prev = prev + 1
//     songM.child(songid).child(uid).set(prev)	
// }

function reset_pwd(){
	email1=document.getElementById("reset_email").value;
	if(email1=="")
	{
		alert("Email cannot be left empty!");
	}
	else
	{
		$.ajax({
            url: 'reset_pwd',
            method:'post',
            data: {email:email1}
            });
		alert("Follow the link in your email to reset the password.");
		auth.sendPasswordResetEmail(email1);
	}	
}

function addtoplaylist(uid,sid){
	$.ajax({
            url: 'addtoplaylist',
            method:'post',
            data: { uid:uid,
            	    sid:sid }
            });
	alert("Song added to your playlist");
}

function removefromplaylist(uid,sid){
	$.ajax({
            url: 'removefromplaylist',
            method:'post',
            data: { uid:uid,
            	    sid:sid }
            });
	document.getElementById('MP'+sid).remove();
	All_song=All_song.filter(item=> item.ID!=sid);
	alert("Song removed from your playlist");
}