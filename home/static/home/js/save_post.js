let posts_save = document.querySelector(".posts_save")

let how_get = 20
let start_post = 0
let end_post = how_get

function get_posts(){
	$.ajax({
		type: $(this).attr('post'),
		url: saves_posts_ajax,
		data: {"start_post":start_post,"end_post":end_post},
		error: function (response) {
			console.log(response)
	    },
	    success: function(response){
	    	posts_save.innerHTML += response
	    	start_post += how_get
	    	end_post += how_get
	    }
	})
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
let get_can = true

async function get_can_true() {
	await sleep(700)
	get_can = true
}

get_posts()

window.addEventListener('scroll', async function(e) {
	if($(window).scrollTop()+$(window).height()>=$(document).height()-500){
	  if (get_can) {
	 		get_posts()
	 		get_can = false
	 		get_can_true()
	 	}
	}
})