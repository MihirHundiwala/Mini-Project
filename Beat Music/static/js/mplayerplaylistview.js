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
let All_song = $('#my-data').data('playlist');
let i = $('#my-data2').data('index');
i=parseInt(i)

// console.log("Start of javascript file while loading default songs");
// console.log(typeof(All_song));
// console.log(All_song);
// let All_song = document.getElementById('list');
// let show_duration = document.querySelector('#show_duration');
// let volume_show = document.querySelector('#volume_show');
// let auto_play = document.querySelector('#auto');
// let present = document.querySelector('#present');
// let total = document.querySelector('#total');
let flag = true;
let flag3 = true;

let timer;
// let autoplay = 0;

let index_no = i;
console.log("index_no before:",index_no);

if(index_no == -1)
{   
    console.log("if part");
    index_no = i+1;
}

console.log("index_no after:",index_no);
let Playing_song = false;

//create a audio Element
let track = document.createElement('audio');
var ifplay = false;

//All songs list
// let All_song = [
//    {
//      name: "No Control",
//      artist: "",
//      path: "https://firebasestorage.googleapis.com/v0/b/music-player-3dac7.appspot.com/o/Music%2FNo%20Control.mp3?alt=media&token=a53e93d0-b672-4f0d-b701-ff69c6343a95",
//      img: "images/trackimg.jpg",
//      singer: "One Direction"
//    },
//    {
//      name: "Circles",
//      path: "https://firebasestorage.googleapis.com/v0/b/music-player-3dac7.appspot.com/o/Music%2FCircles.mp3?alt=media&token=8f4a95f5-30a2-49eb-86cd-b3c4b26ed756",
//      img: "images/trackimg.jpg",
//      singer: "Post Malone"
//    },
//    {
//      name: "Havana",
//      path: "https://firebasestorage.googleapis.com/v0/b/music-player-3dac7.appspot.com/o/Music%2FHavana.mp3?alt=media&token=9218052f-136d-4c07-aa9f-425c3bb64823",
//      img: "images/trackimg.jpg",
//      singer: "Camila Cabello"
//    },
//    {
//      name: "Shape Of You",
//      path: "https://firebasestorage.googleapis.com/v0/b/music-player-3dac7.appspot.com/o/Music%2FShape%20Of%20You.mp3?alt=media&token=00c7a60f-8fc4-4ddf-95d2-135aa14f4453",
//      img: "images/trackimg.jpg",
//      singer: "Ed Sheeran"
//    },
//    {
//      name: "Smack that",
//      path: "https://firebasestorage.googleapis.com/v0/b/music-player-3dac7.appspot.com/o/Music%2FSmack%20that.mp3?alt=media&token=1a2fd316-b02a-4688-8249-8c0d4c8effb7",
//      img: "images/trackimg.jpg",
//      singer: "Akon ft.Eminem"
//    }
// ];


// All functions

// function load the track
function load_track(index_no) {
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
    //totaltime.innerHTML=(Math.floor(track.duration/60)).toLocaleString('en-US',{minimumIntegerDigits:2})+':'+(Math.floor(track.duration)%60).toLocaleString('en-US',{minimumIntegerDigits:2});

    // total.innerHTML = All_song.length;
    // present.innerHTML = index_no + 1;	
}


load_track(index_no);


//mute sound function
function mute_sound() {
    document.getElementById('volume_icon').className = "fas fa-volume-mute";
    track.volume = 0;
    volume.value = 0;
    // volume_show.innerHTML = 0;
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
        if ((track.currentTime / track.duration) * 100 >= 30 & flag) {
            flag = false;
            console.log(All_song[index_no]['ID']);
            console.log(typeof(All_song[index_no]['ID']));
            $.ajax({
                url: 'playlist2',
                // type: 'POST',
                method:'post',
                data: { songid: JSON.stringify(All_song[index_no]['ID'] )}
            });
            console.log("ajax fire");
            return false;
        }

    }
    // function will run when the song is over
    if (track.ended) {
        play.innerHTML = '<i class="fa fa-pause" aria-hidden="true"></i>';
        ifplay = false;
        next_song();
    }

}

// function songqueue(songlist, index, n) {
//     index = index - 1;
//     index_no = index;
//     All_song = songlist;
//     //Email = email;
//     console.log('inside songqueue')
//     $.ajax({
//         url: 'playlist',
//         method: 'post',
//         data: { playlist: JSON.stringify(All_song),
//                 number : n.toString()+index.toString()
//               },

//         success: function(response1) {
//             window.location = "playlist1?data=" + response1;
//         }
//     });

// }

function songqueue(index, n) {

    window.location = "playlist?data=" + (n).toString()+(index-1).toString();

}


function playsong_request_from_playlistviewhtml(songlist, index) {
    index_no = index-1;
    load_track(index_no);
    playsong();  
}