let find_now = "musics"
musics = document.querySelector(".music_all")
playlists = document.querySelector(".playlists")

function music_share(e){
	$.ajax({
	  type: $(this).attr('post'),
	  url: musics_all_ajax,
	  data: {'id':id_user,
			'type':'music_share'},
	  success: function (response) {
	    document.querySelector(".musics_share").innerHTML = response
	  }
	})
}

function get_musics(){
	$.ajax({
	  type: $(this).attr('post'),
	  url: musics_all_ajax,
	  data: {'type':'user_my_music'},
	  success: function (response) {
	     document.querySelector(".music_all").innerHTML += response
	  }
	})
}

function get_playlists(){
	$.ajax({
	  type: $(this).attr('post'),
	  url: playlists_ajax,
	  success: function (response) {
	     document.querySelector(".playlists").innerHTML += response
	  }
	})
}

let music_share_id

function share_menu(e){
	music_share_id = e.id
	document.querySelector(".music_share").style.display = "block"
}
function close_sh(e){
	document.querySelector(".music_share").style.display = "none"
}

function all_border_black(){
	btns = document.getElementsByClassName('h2_now')
	for(let i=btns.length-1;i>=0; i--){
			btns[i].style.borderBottom = "2px solid black";
	}
}

function what_find(e,find_text){
	find_now = find_text
	all_border_black()
	if (find_text=="musics"){
		playlists.style.display = "none"
		musics.style.display = "block"
		document.querySelector(".add_mus").style.display = "block"
	}else	if (find_text=="playlists"){
		musics.style.display = "none"
		playlists.style.display = "block"
		document.querySelector(".add_mus").style.display = "none"
	}
	e.style.borderBottom = "2px solid white";
	ajax_elements()
}

function ajax_elements(){
	if (find_now == "playlists"){
		get_playlists()
	}else if (find_now == "musics"){
		get_musics()
	}	
}

ajax_elements()