let find_now = "musics"
musics = document.querySelector(".music_all")
playlists = document.querySelector(".playlists")

let how_get = 20
let playlists_start = 0
let playlists_end = how_get

let musics_start = 0
let musics_end = how_get

function music_share(e){
	$.ajax({
		type: $(this).attr('post'),
		url: musics_all_ajax,
		data: {'id':id_user,'type':'music_share'},
		success: function (response) {
			document.querySelector(".musics_share").innerHTML = response
		}
	})
}

function get_musics(){
	$.ajax({
		type: $(this).attr('post'),
		url: musics_all_ajax,
		data: {'type':'user_my_music',"musics_start":musics_start,"musics_end":musics_end},
		success: function (response) {
			document.querySelector(".music_all").innerHTML += response
			musics_start+=how_get
			musics_end+=how_get
		}
	})
}

function get_playlists(){
	$.ajax({
		type: $(this).attr('post'),
		url: playlists_ajax,
		data: {"playlists_start":playlists_start,"playlists_end":playlists_end},
		success: function (response) {
			document.querySelector(".playlists").innerHTML += response
			playlists_start+=how_get
			playlists_end+=how_get
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
		document.querySelector(".add_playlist").style.display = "none"
	}else	if (find_text=="playlists"){
		musics.style.display = "none"
		playlists.style.display = "block"
		document.querySelector(".add_mus").style.display = "none"
		document.querySelector(".add_playlist").style.display = "block"
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

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}
let get_can = true

async function get_can_true() {
	await sleep(700)
	get_can = true
}

window.addEventListener('scroll', async function(e) {
	if($(window).scrollTop()+$(window).height()>=$(document).height()-500){
		if (get_can) {
	 		ajax_elements()
	 		get_can = false
	 		get_can_true()
	 	}
	}
})