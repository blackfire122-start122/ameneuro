let musics_start = 0
let musics_end = how_get

function get_musics(){
	$.ajax({
	  type: $(this).attr('post'),
	  url: musics_all_ajax,
	  data: {'type':'playlist',"ps":playlist,'musics_start':musics_start,'musics_end':musics_end},
	  success: function (response) {
	     document.querySelector(".musics").innerHTML += response
	  }
	})
	musics_start += how_get
	musics_end += how_get
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
let get_can = true

async function get_can_true() {
	await sleep(700)
	get_can = true
}

get_musics()

window.addEventListener('scroll', async function(e) {
	if($(window).scrollTop()+$(window).height()>=$(document).height()-500){
	  if (get_can) {
	 		get_musics()
	 		get_can = false
	 		get_can_true()
	 	}
	}
})