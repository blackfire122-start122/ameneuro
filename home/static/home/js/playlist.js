function get_musics(){
	$.ajax({
	  type: $(this).attr('post'),
	  url: musics_all_ajax,
	  data: {'type':'playlist',"ps":playlist},
	  success: function (response) {
	     document.querySelector(".musics").innerHTML += response
	  }
	})
}

get_musics()