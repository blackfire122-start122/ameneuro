let menu_show_v = true

function menu_show(e){
	if (menu_show_v) {
		document.querySelector(".menu_home").style.display = "flex"
		menu_show_v = false
	}else{
		document.querySelector(".menu_home").style.display = "none"
		menu_show_v = true
	}
}

let video

function get_posts(){
	let posts_div = document.querySelector('.posts')

	$.ajax({
		url: post_ajax,
		data: {'id':id_post},
		error: (data)=> {
			console.log(data.data_text)
		},
		success: (data) =>{
			if (data["info"] != "None post"){
				posts_div.innerHTML += data
				video = document.getElementsByClassName("video_post")
			}
		}
	})
}

get_posts()

function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}

if (!id_post){
	window.addEventListener('scroll', function(e) {
		if($(window).scrollTop()+$(window).height()>=$(document).height()-500){
		    get_posts()
		    sleep(700)
		}
	})
}

window.addEventListener('scroll', function(e){
	for (let i = 0;i<video.length;i++){
		if (!($(video[i]).position().top > $(window).scrollTop())){
			video[i].pause()
		}
	}
})

let msg_point = document.getElementById('chats')
let musics_point = document.getElementById('musics')
let activity_point = document.getElementById('activity')

if (msg_point){
	if(msg_point.childNodes[0].innerText!=0){
		msg_point.style.display = "block"
		menu_id.style.display = "block"
	}
}

if (musics_point){
	if(musics_point.childNodes[0].innerText!=0){
		musics_point.style.display = "block"
		menu_id.style.display = "block"
	}
}

if (activity_point){
	if(activity_point.childNodes[0].innerText!=0){
		activity_point.style.display = "block"
		menu_id.style.display = "block"
	}
}