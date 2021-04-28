var trending;
var search;
var myplaylist;

function loadqueue(All_song) {
    let i = 0;
    for (i = 0; i < All_song.length; i++) {
        var div = document.createElement('div');
        div.innerHTML = '<div class="col-1.5">' +
            '<img src="https://picsum.photos/640/480?pic=5" class="songcov" />' +
            '</div>' +
            '<div class="col-10 nopad">' +
            '<ul class="navbar nav ml-auto" id="playnav">' +
            '<li>' +
            '<p class="songname">' + All_song[i]['Title'] + '</p>' +
            '<p class="songinfo">' + All_song[i]['Artist'] + '-' + All_song[i]['Album'] + '</p>' +
            '</li>' +
            '<li>' +
            '<div class="dropdown dropleft song_options">' +
            '<button class="btn more_btn" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">' +
            '<i class="fa fa-ellipsis-v" aria-hidden="true"></i>' +
            '</button>' +
            '<div class="dropdown-menu queuesong" aria-labelledby="dropdownMenuButton">' +
            '<label class="dropdown-item" onclick="addtoplaylist(' + "{{uid}}" + ',' + All_song[i]['ID'] + ')">Add to Playlist</label>' +
            '<label class="dropdown-item" onclick="removefromplaylist(' + "{{uid}}" + ',' + All_song[i]['ID'] + ')">Remove from Playlist</label>' +
            '</div>' +
            '</div>' +
            '</li>' +
            '</ul>' +
            '</div>';
        div.setAttribute('class', 'row pad');
        div.setAttribute('id', 'Q'+All_song[i]['ID']);
        div.setAttribute('onclick', 'playrequest_queue(' + i.toString() + ')');
        document.getElementById("loadqueue").appendChild(div);
    }
}

function addtoqueue(song) {
    $('#' + song['ID']).remove();
    var div = document.createElement('div');
    div.innerHTML = '<div class="col-1.5">' +
        '<img src="https://picsum.photos/640/480?pic=5" class="songcov" />' +
        '</div>' +
        '<div class="col-10 nopad">' +
        '<ul class="navbar nav ml-auto id="playnav"">' +
        '<li>' +
        '<p class="songname">' + song['Title'] + '</p>' +
        '<p class="songinfo">' + song['Artist'] + '-' + song['Album'] + '</p>' +
        '</li>' +
        '<li>' +
        '<div class="dropdown dropleft song_options">' +
        '<button class="btn more_btn" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">' +
        '<i class="fa fa-ellipsis-v" aria-hidden="true"></i>' +
        '</button>' +
        '<div class="dropdown-menu queuesong" aria-labelledby="dropdownMenuButton">' +
        '<a class="dropdown-item" href="#">Remove</a>' +
        '<a class="dropdown-item" href="#">Add to Playlist</a>' +
        '</div>' +
        '</div>' +
        '</li>' +
        '</ul>' +
        '</div>';
    div.setAttribute('class', 'row pad');
    div.setAttribute('id','Q'+song['ID']);
    div.setAttribute('onclick', 'playrequest_queue' + index_no + ')');
    document.getElementById("loadqueue").appendChild(div);
}
flag4=true;
function loadpopular(){
    $('#popular').modal('show');
    if(flag4){
        $.ajax({
                    url: 'popular10',
                    method:'post',
                    success:function(trending1){
                        trending=JSON.parse(trending1);
                        flag4=false;
                        let i = 0;
                        for (i = 0; i < trending.length; i++) {
                            var div = document.createElement('div');
                            div.innerHTML = '<div class="col-1.5">' +
                                '<img src="https://picsum.photos/640/480?pic=5" class="songcov" />' +
                                '</div>' +
                                '<div class="col-10 nopad">' +
                                '<ul class="navbar nav ml-auto" id="playnav">' +
                                '<li>' +
                                '<p class="songname">' + trending[i]['Title'] + '</p>' +
                                '<p class="songinfo">' + trending[i]['Artist'] + '-' + trending[i]['Album'] + '</p>' +
                                '</li>' +
                                '<li>' +
                                '<div class="dropdown dropleft song_options">' +
                                '<button class="btn more_btn" type="button" id="dropdownMenuButton" trending-toggle="dropdown" aria-haspopup="true" aria-expanded="false">' +
                                '<i class="fa fa-ellipsis-v" aria-hidden="true"></i>' +
                                '</button>' +
                                '<div class="dropdown-menu queuesong" aria-labelledby="dropdownMenuButton">' +
                                '<label class="dropdown-item" onclick="addtoplaylist(' + "{{uid}}" + ',' + trending[i]['ID'] + ')">Add to Playlist</label>' +
                                '<label class="dropdown-item" onclick="removefromplaylist(' + "{{uid}}" + ',' + trending[i]['ID'] + ')">Remove from Playlist</label>' +
                                '</div>' +
                                '</div>' +
                                '</li>' +
                                '</ul>' +
                                '</div>';
                            div.setAttribute('class', 'row pad');
                            div.setAttribute('id', 'P'+trending[i]['ID']);
                            div.setAttribute('onclick', 'playrequest_trending(' + i.toString() + ')');
                            document.getElementById("popularqueue").appendChild(div);
                        }
                    }
        });
    }
}

function searchsong(){
    document.getElementById("searchqueue").innerHTML="";
    strm=document.getElementById("strm").value;
    console.log('string:',strm);
        $('#searchmodal').modal('show');
        $.ajax({
                    url: 'search',
                    method:'post',
                    data:{strm:strm},
                    success:function(search1){
                        search=JSON.parse(search1);
                        flag4=false;
                        let i = 0;
                        for (i = 0; i < search.length; i++) {
                            var div = document.createElement('div');
                            div.innerHTML = '<div class="col-1.5">' +
                                '<img src="https://picsum.photos/640/480?pic=5" class="songcov" />' +
                                '</div>' +
                                '<div class="col-10 nopad">' +
                                '<ul class="navbar nav ml-auto" id="playnav">' +
                                '<li>' +
                                '<p class="songname">' + search[i]['Title'] + '</p>' +
                                '<p class="songinfo">' + search[i]['Artist'] + '-' + search[i]['Album'] + '</p>' +
                                '</li>' +
                                '<li>' +
                                '<div class="dropdown dropleft song_options" style="right: -80px;">' +
                                '<button class="btn more_btn" type="button" id="dropdownMenuButton" search-toggle="dropdown" aria-haspopup="true" aria-expanded="false">' +
                                '<i class="fa fa-ellipsis-v" aria-hidden="true"></i>' +
                                '</button>' +
                                '<div class="dropdown-menu queuesong" aria-labelledby="dropdownMenuButton">' +
                                '<label class="dropdown-item" onclick="addtoplaylist(' + "{{uid}}" + ',' + search[i]['ID'] + ')">Add to Playlist</label>' +
                                '<label class="dropdown-item" onclick="removefromplaylist(' + "{{uid}}" + ',' + search[i]['ID'] + ')">Remove from Playlist</label>' +
                                '</div>' +
                                '</div>' +
                                '</li>' +
                                '</ul>' +
                                '</div>';
                            div.setAttribute('class', 'row pad');
                            div.setAttribute('id', 'S'+search[i]['ID']);
                            div.setAttribute('onclick', 'playrequest_search(' + i.toString() + ')');
                            document.getElementById("searchqueue").appendChild(div);
                        }
                    }
        });

}

flag5=true
function loadmyplaylist(){
    $('#myplaylist').modal('show');
    if(flag5){
        $.ajax({
                    url: 'myplaylist',
                    method:'post',
                    data:{email:email1},
                    success:function(myplaylist1){
                        myplaylist=JSON.parse(myplaylist1);
                        flag5=false;
                        let i = 0;
                        for (i = 0; i < myplaylist.length; i++) {
                            var div = document.createElement('div');
                            div.innerHTML = '<div class="col-1.5">' +
                                '<img src="https://picsum.photos/640/480?pic=5" class="songcov" />' +
                                '</div>' +
                                '<div class="col-10 nopad">' +
                                '<ul class="navbar nav ml-auto" id="playnav">' +
                                '<li>' +
                                '<p class="songname">' + myplaylist[i]['Title'] + '</p>' +
                                '<p class="songinfo">' + myplaylist[i]['Artist'] + '-' + myplaylist[i]['Album'] + '</p>' +
                                '</li>' +
                                '<li>' +
                                '<div class="dropdown dropleft song_options">' +
                                '<button class="btn more_btn" type="button" id="dropdownMenuButton" myplaylist-toggle="dropdown" aria-haspopup="true" aria-expanded="false">' +
                                '<i class="fa fa-ellipsis-v" aria-hidden="true"></i>' +
                                '</button>' +
                                '<div class="dropdown-menu queuesong" aria-labelledby="dropdownMenuButton">' +
                                '<label class="dropdown-item" onclick="addtoplaylist(' + "{{uid}}" + ',' + myplaylist[i]['ID'] + ')">Add to Playlist</label>' +
                                '<label class="dropdown-item" onclick="removefromplaylist(' + "{{uid}}" + ',' + myplaylist[i]['ID'] + ')">Remove from Playlist</label>' +
                                '</div>' +
                                '</div>' +
                                '</li>' +
                                '</ul>' +
                                '</div>';
                            div.setAttribute('class', 'row pad');
                            div.setAttribute('id', 'MP'+myplaylist[i]['ID']);
                            div.setAttribute('onclick', 'playrequest_myplaylist(' + i.toString() + ')');
                            document.getElementById("myplaylistqueue").appendChild(div);
                        }
                    }
        });
    }
}