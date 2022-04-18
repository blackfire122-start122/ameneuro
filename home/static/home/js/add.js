let add_post = document.querySelector(".add_post")
let add_video = document.querySelector(".add_video")

function what_add(e,what_add) {

	if (what_add == "post") {
		add_post.style.display = "block"
		add_video.style.display = "none"
	}else if(what_add == "video"){
		add_video.style.display = "block"
		add_post.style.display = "none"
	}
}