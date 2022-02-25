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

$.ajax({
  type: $(this).attr('post'),
  url: musics_all_ajax,
  data: {'id':id_user,
		'type':'user_my_music'},
  success: function (response) {
     document.querySelector(".music_all").innerHTML = response
  }
})

let music_share_id

function share_menu(e){
	music_share_id = e.id
	document.querySelector(".music_share").style.display = "block"
}
function close_sh(e){
	document.querySelector(".music_share").style.display = "none"
}

