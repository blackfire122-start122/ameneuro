let musics = document.getElementById("id_musics")
let ajax_get_now = "all"

let music_start = 0
let music_end = how_get

let music_find_start = 0
let music_find_end = how_get

let find_str = ""
let clear = false

function get_musics_find(){
	$.ajax({
		type: $(this).attr('post'),
		url: music_find_ajax,
		data: {"type":"music_select", "find_name":find_str,"music_find_start":music_find_start,"music_find_end":music_find_end,'playlist_id':playlist_id},
		success: function (response){
			if (clear){
				musics.innerHTML = response
				clear = false
			}else{
				musics.innerHTML += response
			}

			music_find_start+=how_get
			music_find_end+=how_get
		}
	})
}
function get_musics(){
	$.ajax({
		type: $(this).attr('post'),
		url: music_get_ajax,
		data: {"type":"music_select","music_start":music_start,"music_end":music_end,'playlist_id':playlist_id},
		success: function (response){
			musics.innerHTML += response
			
			music_start+=how_get
			music_end+=how_get
		}
	})
}

ajax_get()

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
let get_can = true

async function get_can_true() {
	await sleep(700)
	get_can = true
}

musics.addEventListener('scroll', async function(e) {
	if($(window).scrollTop()+$(window).height()>=$(document).height()-300){
	  if (get_can) {
	 		ajax_get()
	 		get_can = false
	 		get_can_true()
	 	}
	}
})

function sel_mus(e,music_id,name_mus){
	if (e.style.opacity == "0.5") {
		e.style.opacity = "1"
		conn_u.send(JSON.stringify({'type':'not_add_to_playlists','music_id': music_id,'playlist_id':playlist_id,'name_mus':name_mus}))
	}else{
		e.style.opacity = "0.5"
		conn_u.send(JSON.stringify({'type':'add_to_playlists','music_id': music_id,'playlist_id':playlist_id,'name_mus':name_mus}))
	}
}

function ajax_get(){
	if (ajax_get_now=="all"){
		get_musics()
	}else{
		get_musics_find()
	}
}

function inp_find(e){
	find_str = e.value
	ajax_get_now = "find"
	clear = true
	music_find_start = 0
	music_find_end = how_get
	ajax_get()
}