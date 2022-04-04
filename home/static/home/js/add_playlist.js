let musics = document.getElementById("id_musics")

let how_get = 20

let music_start = 0
let music_end = how_get

let music_find_start = 0
let music_find_end = how_get

function img_set(e){
	file = e.files[0]

	img = document.querySelector(".img_input")
	img.src = window.URL.createObjectURL(file)
}

function get_musics_find(){
	$.ajax({
		type: $(this).attr('post'),
		url: music_find_ajax,
		data: {"type":"music_select", "find_name":find_str,"music_find_start":music_find_start,"music_find_end":music_find_end},
		success: function (response){
			if (clear){
				musics.innerHTML = response
				clear = false
			}else{
				musics.innerHTML += response
			}
			window.removeEventListener('scroll',scroll_event);
			window.addEventListener('scroll', scroll_event_find)
			music_find_start+=how_get
			music_find_end+=how_get
		}
	})
}
function get_musics(){
	$.ajax({
		type: $(this).attr('post'),
		url: music_get_ajax,
		data: {"type":"music_select","music_start":music_start,"music_end":music_end},
		success: function (response){
			response = $(response)

			for (var i = response.length - 1; i >= 0; i--) {
				musics.append(response[i])
			}
			
			music_start+=how_get
			music_end+=how_get
		}
	})
}

get_musics()

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
	 		get_musics()
	 		get_can = false
	 		get_can_true()
	 	}
	}
})

function sel_mus(e){
	if (e.style.opacity == "0.5") {
		e.style.opacity = "1"
	}else{
		e.style.opacity = "0.5"
	}
}