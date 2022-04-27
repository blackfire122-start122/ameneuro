let menu_show_v = true
let posts = document.querySelector('.posts')
let videos = document.querySelector('.videos')

let start_element = 0
let end_element = get_posts_how
let start_rec_post = 0
let end_rec_post = get_posts_how
let start_rec_user = 0
let end_rec_user = get_user_how
let defolt_posts = 0
let start_element_video = 0
let end_element_video = get_posts_how
let start_rec_video = 0
let end_rec_video = get_posts_how
let start_rec_video_user = 0
let end_rec_video_user = get_user_how
let defolt_video = 0
let end_scroll = 0
let end_scroll_video = 0

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
	$.ajax({
		data:{"start_element":start_element,
				"end_element":end_element,
				"start_rec_post":start_rec_post,
				"end_rec_post":end_rec_post,
				"start_rec_user":start_rec_user,
				"end_rec_user":end_rec_user,
				"defolt_posts":defolt_posts,
				"end_scroll":end_scroll,
			},
		url: post_ajax,
		success: (data) =>{
			posts.innerHTML += data["html"]

			start_element=data["next_data"]["start_element"]
			end_element=data["next_data"]["end_element"]
			start_rec_post=data["next_data"]["start_rec_post"]
			end_rec_post=data["next_data"]["end_rec_post"]
			start_rec_user=data["next_data"]["start_rec_user"]
			end_rec_user=data["next_data"]["end_rec_user"]
			defolt_posts=data["next_data"]["defolt_posts"]
			end_scroll=data["next_data"]["end_scroll"]
		}
	})
}

function get_videos(){
	$.ajax({
		data:{"start_element_video":start_element_video,
				"end_element_video":end_element_video,
				"start_rec_video":start_rec_video,
				"end_rec_video":end_rec_video,
				"start_rec_video_user":start_rec_video_user,
				"end_rec_video_user":end_rec_video_user,
				"defolt_video":defolt_video,
				"end_scroll_video":end_scroll_video,
		},
		url: video_ajax,
		success: (data) =>{
			videos.innerHTML += data["html"]
			start_element_video=data["next_data"]["start_element_video"]
			end_element_video=data["next_data"]["end_element_video"]
			start_rec_video=data["next_data"]["start_rec_video"]
			end_rec_video=data["next_data"]["end_rec_video"]
			start_rec_video_user=data["next_data"]["start_rec_video_user"]
			end_rec_video_user=data["next_data"]["end_rec_video_user"]
			defolt_video=data["next_data"]["defolt_video"]
			end_scroll_video=data["next_data"]["end_scroll_video"]
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

function remove_all_listener_window(){
	window.removeEventListener('scroll',scroll_get_posts);
	window.removeEventListener('scroll',scroll_pause_media);
	window.removeEventListener('scroll',scroll_get_videos);
	window.removeEventListener('scroll',scroll_pause_videos);
}

async function scroll_get_posts() {
	if($(window).scrollTop()+$(window).height()>=$(document).height()-500){
	  if (get_can) {
	 		get_posts()
	 		get_can = false
	 		get_can_true()
	 	}
	}
}

function scroll_pause_media(){
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
			if (audio[i].parentNode.childNodes[5].childNodes[1]) {
	  		audio[i].parentNode.childNodes[5].childNodes[1].childNodes[0].src = pause_img
			}
		}
	}
}

async function scroll_get_videos() {
	if($(window).scrollTop()+$(window).height()>=$(document).height()-500){
	  if (get_can) {
	 		get_videos()
	 		get_can = false
	 		get_can_true()
	 	}
	}
}

function scroll_pause_videos(){
	let video = document.getElementsByClassName("video_video")
	for (let i = video.length-1;i>=0;i--){
		if (!Visible(video[i])){
			video[i].pause()
		}
	}
}

function start_posts(){
	get_posts()

	window.addEventListener('scroll',scroll_get_posts)
	window.addEventListener('scroll',scroll_pause_media)
}

function start_videos(){
	get_videos()
	window.addEventListener('scroll',scroll_get_videos)
	window.addEventListener('scroll',scroll_pause_videos)
}

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

function wath_now(e,now){
	btns = document.getElementsByClassName('btn_wath_now')

	for (var i = btns.length - 1; i >= 0; i--) {
		btns[i].style.opacity = "1"
	}
	e.style.opacity = '0.5'
	remove_all_listener_window()
	if (now=="posts") {
		posts.style.display = "block"
		videos.style.display = "none"

		start_posts()
	}else if (now =="videos") {
		videos.style.display = "block"
		posts.style.display = "none"

		start_videos()
	}
}

wath_now(document.getElementById("posts"),'posts')