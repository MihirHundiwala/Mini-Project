function loadplaylist(n) {
        // var div = document.createElement('div');
        document.getElementById("playqueue").innerHTML=     "<h2>{{sli["+n.toString()+"][0]['Genre']}}Romance</h2>"
                                                        +    "<br>"
                                                        +    "<button class='playbtn btn-default'>Play All</button>"
                                                        +    "<br><br>{% for lem in sli"+n.toString()+"%}"
                                                        +    "<div class='row pad'>"
                                                        +        '<div class="col-1.5" onclick="playrequest_playlistviewhtml({{loop.index}})">'
                                                        +            '<img src="https://picsum.photos/640/480?pic=10" class="songcov" />'
                                                        +        '</div>'
                                                        +        '<div class="col-10 nopad">'
                                                        +            '<ul class="navbar nav ml-auto" id="playnav">'
                                                        +                '<li onclick="playrequest_playlistviewhtml({{loop.index}})">'
                                                        +                    "<p class='songname'>{{lem['Title']}}</p>"
                                                        +                    "<p class='songinfo'>{{lem['Artist']}} - {{lem['Album']}}</p>"
                                                        +                '</li>'
                                                        +                '<li>'
                                                        +                    '<div class="dropdown dropup">'
                                                        +                        '<button class="btn" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
                                                        +                                '<i class="fa fa-ellipsis-v more" aria-hidden="true"></i>'
                                                        +                            '</button>'
                                                        +                        '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'
                                                        +                            '<a class="dropdown-item" href="#">Play Next</a>'
                                                        +                            '<a class="dropdown-item" href="#">Add to Queue</a>'
                                                        +                            "<label class=\"dropdown-item\" onclick=\"addtoplaylist('{{uid}}','{{lem['ID']}}')\">Add to Playlist</label>"
                                                        +                            "<label class=\"dropdown-item\" onclick=\"removefromplaylist('{{uid}}','{{lem['ID']}}')\">Remove from Playlist</label>"
                                                        +                        '</div>'
                                                        +                    '</div>'
                                                        +                '</li>'
                                                        +            '</ul>'
                                                        +        '</div>'
                                                        +    '</div>'
                                                        +    '{% endfor %}';
        // div.setAttribute('class', 'row pad');
        // div.setAttribute('id', All_song[i]['ID']);
        // div.setAttribute('onclick', 'playrequest_queuehtml(' + i.toString() + ')');
        // document.getElementById("playqueue").appendChild(div);
}

