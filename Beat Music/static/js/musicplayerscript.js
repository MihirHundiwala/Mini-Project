let previous = document.querySelector('#pre');
let play = document.getElementById('play');
let next = document.querySelector('#next');
let title = document.querySelector('#title');
let album = document.querySelector('#album');
let artist = document.querySelector('#artist');
let recent_volume = document.querySelector('#volume');
let slider = document.getElementById('duration_slider');
let track_image = document.querySelector('#track_image');
let currenttime = document.querySelector('#currenttime');
let totaltime = document.querySelector('#totaltime');
// let email1 = $('#meta-email').data('email');
let uid = $('#uid').data('uid');

if($('#listtype').data('listtype')=='top10')
{
    document.getElementById("listgenre").innerHTML="Trending";
}
else if($('#listtype').data('listtype')=='myplaylist')
{
    document.getElementById("listgenre").innerHTML="My Playlist";
}

let All_song=[];
All_song=All_song.concat($('#my-data').data('previousplaylist'));
loadqueue(All_song);


let songlist=$('#my-data1').data('currentplaylist');

let i =0;
let addcountflag = true;
let flag2 = true;
let timer;


let index_no = i;
// console.log("index_no before:",index_no);

if(index_no < 0)
{   
    console.log("if part index negative");
    console.log(index_no);
    index_no = i+1;
}

// console.log("index_no after:",index_no);
let Playing_song = false;

//create a audio Element
let track = document.createElement('audio');
var ifplay = false;

// function load the track
function load_track(index_no) {

    document.getElementById("nowplayingalbum").innerHTML=All_song[index_no]['Album'];
    document.getElementById("nowplayingtitle").innerHTML=All_song[index_no]['Title'];
    document.getElementById("nowplayinginfo").innerHTML=All_song[index_no]['Artist']+'-'+All_song[index_no]['Album'];
    clearInterval(timer);
    reset_slider();

    track.src = All_song[index_no]['Path'];
    title.innerHTML = All_song[index_no]['Title'];
    // artist.innerHTML = All_song[index_no].artist;
    // track_image.src = All_song[index_no].img;
    album.innerHTML = "(" + All_song[index_no]['Album'] + ")";
    artist.innerHTML = " -  " + All_song[index_no]['Artist'];
    track.load();
    timer = setInterval(range_slider, 1000);
    addcountflag=true;
}


load_track(index_no);


//mute sound function
function mute_sound() {
    document.getElementById('volume_icon').className = "fas fa-volume-mute";
    track.volume = 0;
    volume.value = 0;
}


// checking.. the song is playing or not
function justplay() {
    if (Playing_song == false) {
        playsong();
    } else {
        pausesong();
    }
}


// reset song slider
function reset_slider() {
    slider.value = 0;
}

// play song
function playsong() {
    track.play();
    Playing_song = true;
    play.innerHTML = '<i class="fa fa-pause" aria-hidden="true"></i>';
    totaltime.innerHTML = (Math.floor(track.duration / 60)).toLocaleString('en-US', { minimumIntegerDigits: 2 }) + ':' + (Math.floor(track.duration) % 60).toLocaleString('en-US', { minimumIntegerDigits: 2 });
}

//pause song
function pausesong() {
    track.pause();
    Playing_song = false;
    play.innerHTML = '<i class="fa fa-play" aria-hidden="true"></i>';
}


// next song
function next_song() {
    console.log(All_song);
    if (index_no < All_song.length - 1) {
        index_no += 1;
        load_track(index_no);
        playsong();

    } else {
        index_no = 0;
        load_track(index_no);
        playsong();
    }
}


// previous song
function previous_song() {
    if (index_no > 0) {
        index_no -= 1;
        load_track(index_no);
        playsong();
    } else {
        index_no = All_song.length;
        load_track(index_no);
        playsong();
    }
}


// change volume
function volume_change() {
    // volume_show.innerHTML = recent_volume.value;
    document.getElementById('volume_icon').className = "fas fa-volume-up";
    track.volume = recent_volume.value / 100;
}

// change slider position 
function change_duration() {
    slider_position = track.duration * (slider.value / 100);
    track.currentTime = slider_position;
}

function range_slider() {
    let position = 0;

    // update slider position
    if (!isNaN(track.duration)) {
        position = track.currentTime * (100 / track.duration);
        slider.style.background = 'linear-gradient(to right,#FF2D2D 0%, #FF2D2D ' + position + '%, #fff ' + position + '%,white 100%)'
        slider.value = position;

        ctime = (Math.floor(track.currentTime / 60)).toLocaleString('en-US', { minimumIntegerDigits: 2 }) + ':' + (Math.floor(track.currentTime) % 60).toLocaleString('en-US', { minimumIntegerDigits: 2 });
        currenttime.innerHTML = ctime;
        ttime = (Math.floor(track.duration / 60)).toLocaleString('en-US', { minimumIntegerDigits: 2 }) + ':' + (Math.floor(track.duration) % 60).toLocaleString('en-US', { minimumIntegerDigits: 2 });
        totaltime.innerHTML = ttime;
        //    console.log((ctime/ttime)*100);
        if ((track.currentTime / track.duration) * 100 >= 30 & addcountflag) {
            addcountflag = false;
            $.ajax({
                url: 'addcount',
                method:'post',
                data: { songid: All_song[index_no]['ID'],
                        email:email1
                      }
            });
            console.log("ajax fire");
        }

    }
    // function will run when the song is over
    if (track.ended) {
        play.innerHTML = '<i class="fa fa-pause" aria-hidden="true"></i>';
        ifplay = false;
        next_song();
    }

}

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


function playrequest_indexhtml(index, n) {
    All_song=All_song.filter(item=> item.ID!=songlist[n][index-1].ID);
    All_song=All_song.concat(songlist[n][index-1]);
    index_no=All_song.length-1;
    load_track(index_no);
    playsong();
    addtoqueuedb(All_song[index_no]['ID']);
    addtoqueuemodal(All_song[index_no],index_no);
}

function playrequest_trending(index) {
    All_song=All_song.filter(item=> item.ID!=trending[index].ID);
    All_song=All_song.concat(trending[index]);
    index_no=All_song.length-1;
    load_track(index_no);
    playsong();
    addtoqueuedb(All_song[index_no]['ID']);
    addtoqueuemodal(All_song[index_no]);
    
}

function playrequest_search(index) {
    All_song=All_song.filter(item=> item.ID!=search[index].ID);
    All_song=All_song.concat(search[index]);
    index_no=All_song.length-1;
    load_track(index_no);
    playsong();
    addtoqueuedb(All_song[index_no]['ID']);
    addtoqueuemodal(All_song[index_no]);
    
}

function playrequest_queue(index) {
    index_no = All_song.findIndex(x => x === queue[index]);
    load_track(index_no);
    playsong();
    // addtoqueuedb(All_song[index_no]['ID']);
    // addtoqueuemodal(All_song[index_no]);
}

function playrequest_myplaylist(index) {
    All_song=All_song.filter(item=> item.ID!=myplaylist[index].ID);
    All_song=All_song.concat(myplaylist[index]);
    index_no=All_song.length-1;
    load_track(index_no);
    playsong();
    addtoqueuedb(All_song[index_no]['ID']);
    addtoqueuemodal(All_song[index_no]);
}


function addtoplaylist(uid,i,modal){
    var song1;
    var sid; 
    if (modal=='search'){
        song1=search[i];
        sid=song1['ID'];
    }
    else if (modal=='trending'){
        song1=trending[i];
        sid=trending[i]['ID'];
    }
    else if (modal=='queue'){
        song1=queue[i];
        sid=queue[i]['ID'];
    }

    $.ajax({
            url: 'addtoplaylist',
            method:'post',
            data: { uid:uid,
                    sid:sid}
            });
    addtomyplaylistmodal(song1);
    alert("Song added to your playlist !");
}

function addtoplaylist1(uid,i,n){
    $.ajax({
            url: 'addtoplaylist',
 
            method:'post',
            data: { uid:uid,
                    sid:songlist[n][i-1]['ID']}
            });
    addtomyplaylistmodal(songlist[n][i-1]);
    alert("Song added to your playlist !"); 
}

function removefromplaylist(uid,sid){
    $.ajax({
            url: 'removefromplaylist',
            method:'post',
            data: { uid:uid,
                    sid:sid }
            });
    document.getElementById('MP'+sid).remove();
    alert("Song removed from your playlist !");
}

function addtoqueuedb(sid){
    $.ajax({
            url: 'addtoqueue',
            method:'post',
            data: { email:email1,
                    songid:sid }
    });
}

function addtoqueue1(uid,i,n){
    let song=songlist[n][i-1];
    All_song=All_song.concat(song);
    addtoqueuemodal(song);
    addtoqueuedb(song['ID']);
    alert("Song added to Queue !");
}

function addtoqueue(uid,i,modal){
    var song1;
    var sid; 
    if (modal=='search'){
        song1=search[i];
        sid=song1['ID'];
    }
    else if (modal=='trending'){
        song1=trending[i];
        sid=trending[i]['ID'];
    }
    else if (modal=='myplaylist'){
        song1=myplaylist[i];
        sid=myplaylist[i]['ID'];
    }
    All_song=All_song.concat(song);
    addtoqueuemodal(song);
    addtoqueuedb(sid);
    alert("Song added to Queue !");
}

function removefromqueue(uid,sid){
    $.ajax({
            url: 'removefromqueue',
            method:'post',
            data: { uid:uid,
                    sid:sid }
            });
    document.getElementById('Q'+sid).remove();
    alert("Song removed from Queue !");
}

function playall(listtype,n){
    var list;
    if(listtype=='categories'){
        list=songlist[n];
    }
    else if(listtype=='myplaylist'){
        list=myplaylist;
    }
    else if(listtype=='trending'){
        list=trending;
    }
    else if(listtype=='search'){
        list=search;
    }
    let i=0;
    for(i=0;i<list.length;i++)
    {
        All_song=All_song.filter(item=> item.ID!=list[i].ID);
        All_song=All_song.concat(list[i]);
    }
    index_no=All_song.length-list.length;
    load_track(index_no);
    playsong();
    alert("Feel the vibe!");
}

function saveasplaylist(){
    for(i=0;i<queue.length;i++)
    {
        $.ajax({
            url: 'addtoplaylist',
 
            method:'post',
            data: { uid:uid,
                    sid:queue[i]['ID']}
            });
        addtomyplaylistmodal(queue[i]);
    }
    alert("Added queue songs to playlist !");
}