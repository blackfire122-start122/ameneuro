musics = document.querySelector('.musics')

let musics_s = true

function music_show(){
	if(musics_s){
		musics.style.display = 'block'
	}else{
		musics.style.display = 'none'
	}
	musics_s = !musics_s
}

function follow(btn) {
	$.ajax({
		type: $(this).attr('post'),
		url: follow_ajax,
		data: {'id':btn.value},
	})
	btn.disabled = true
	btn.style.color = "gray"
	btn.style.fontSize = "1em"
	btn.innerText = "follow"
}

$.ajax({
  type: $(this).attr('post'),
  url: musics_all_ajax,
  data: {'id':id_user,
				'type':'user_music_add'},
  success: function (response){
    document.querySelector(".musics").innerHTML = response
  }
})
