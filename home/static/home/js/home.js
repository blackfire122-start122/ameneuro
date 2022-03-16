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
			}
		}
	})
}

get_posts()

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
let get_can = true

async function get_can_true() {
	await sleep(700)
	get_can = true
}

if (!id_post){
	window.addEventListener('scroll', async function(e) {
		if($(window).scrollTop()+$(window).height()>=$(document).height()-500){
		  if (get_can) {
		 		get_posts()
		 		get_can = false
		 		get_can_true()
		 	}
		}
	})
}

window.addEventListener('scroll', function(e){
	let video = document.getElementsByClassName("video_post")
	let audio = document.getElementsByClassName("audio-player")
	for (let i = video.length-1;i>=0;i--){
		if (!Visible(video[i])){
			video[i].pause()
		}
	}
	for (let i = audio.length-1;i>=0;i--){
		if (!Visible(audio[i])){
			audio[i].childNodes[3].pause()
  		audio[i].parentNode.childNodes[5].childNodes[1].childNodes[0].src = pause_img
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

function Visible(target) {
  let targetPosition = {
      top: window.pageYOffset + target.getBoundingClientRect().top,
      left: window.pageXOffset + target.getBoundingClientRect().left,
      right: window.pageXOffset + target.getBoundingClientRect().right,
      bottom: window.pageYOffset + target.getBoundingClientRect().bottom
    },
    windowPosition = {
      top: window.pageYOffset,
      left: window.pageXOffset,
      right: window.pageXOffset + document.documentElement.clientWidth,
      bottom: window.pageYOffset + document.documentElement.clientHeight
    }

  if (targetPosition.bottom > windowPosition.top &&
    targetPosition.top < windowPosition.bottom &&
    targetPosition.right > windowPosition.left &&
    targetPosition.left < windowPosition.right) {
    return true
  } else {
    return false
  }
}