let users = document.querySelector(".users")
let musics = document.querySelector(".musics")
let videos = document.querySelector(".videos")
let find_now = "users"

let input_find = document.querySelector(".find_user")
input_find.placeholder = "Find "+find_now

let how_get = 20

let users_start = 0
let users_end = how_get
let music_start = 0
let music_end = how_get
let video_start = 0
let video_end = how_get

let users_find_start = 0
let users_find_end = how_get
let music_find_start = 0
let music_find_end = how_get
let video_find_start = 0
let video_find_end = how_get

let clear = true
let find_str

document.getElementById("start_find").style.borderBottom = "2px solid white";

function find_inp(e){
	if(event.key === 'Enter') {
		find_str = e.value
		clear = true
		users_find_start = 0
		users_find_end = how_get
		music_find_start = 0
		music_find_end = how_get	
		ajax_find_elements()
	}
}

function get_users_find(){
	$.ajax({
		type: $(this).attr('post'),
		url: user_find_ajax,
		data: {"find_name":find_str,"users_find_start":users_find_start,"users_find_end":users_find_end},
		success: function (response){
			if (clear){
				users.innerHTML = response
				clear = false
			}else{
				users.innerHTML += response
			}
			window.removeEventListener('scroll',scroll_event);
			window.addEventListener('scroll', scroll_event_find)
			users_find_start+=how_get
			users_find_end+=how_get
		}
	})
}

function get_musics_find(){
	$.ajax({
		type: $(this).attr('post'),
		url: music_find_ajax,
		data: {"find_name":find_str,"music_find_start":music_find_start,"music_find_end":music_find_end},
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

function get_videos_find(){
	$.ajax({
		type: $(this).attr('post'),
		url: video_find_ajax,
		data: {"find_name":find_str,"video_find_start":video_find_start,"video_find_end":video_find_end},
		success: function (response){
			if (clear){
				videos.innerHTML = response
				clear = false
			}else{
				videos.innerHTML += response
			}
			window.removeEventListener('scroll',scroll_event);
			window.addEventListener('scroll', scroll_event_find)
			music_find_start+=how_get
			music_find_end+=how_get
		}
	})
}

function get_users(){
	$.ajax({
		type: $(this).attr('post'),
		url: users_get_ajax,
		data: {"type":"all","users_start":users_start,"users_end":users_end},
		success: function (response){
			users.innerHTML += response
			users_start+=how_get
			users_end+=how_get
		}
	})
}


function get_musics(){
	$.ajax({
		type: $(this).attr('post'),
		url: music_get_ajax,
		data: {"music_start":music_start,"music_end":music_end},
		success: function (response){
			musics.innerHTML += response
			music_start+=how_get
			music_end+=how_get
		}
	})
}


function get_videos(){
	$.ajax({
		type: $(this).attr('post'),
		url: video_get_ajax,
		data: {"video_start":video_start,"video_end":video_end},
		success: function (response){
			videos.innerHTML += response
			video_start+=how_get
			video_end+=how_get
		}
	})
}

function ajax_find_elements(){
	if (find_now == "users"){
		get_users_find()
	}else if (find_now == "musics"){	
		get_musics_find()
	}else if (find_now == "videos"){
		get_videos_find()
	}	
}

function ajax_elements(){
	if (find_now == "users"){
		get_users()
	}else if (find_now == "musics"){
		get_musics()
	}else if (find_now == "videos"){
		get_videos()
	}	
}

function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}


window.addEventListener('scroll', scroll_event)
function scroll_event(e) {
	if($(window).scrollTop()+$(window).height()>=$(document).height()-500){
	    ajax_elements()
	    sleep(700)
	}
}

function scroll_event_find(e) {
	if($(window).scrollTop()+$(window).height()>=$(document).height()-500){
	    ajax_find_elements()
	    sleep(700)
	}
}

function want_add_friend(btn) {
	$.ajax({
		type: $(this).attr('post'),
		url: want_add_friend_ajax,
		data: {'id':btn.value},
	})
	btn.disabled = true
	btn.style.display = "none"
	document.getElementById(btn.value).style.display = "none"
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

function all_border_black(){
	btns = document.getElementsByClassName('find_btn')
	for(let i=btns.length-1;i>=0; i--){
			btns[i].style.borderBottom = "2px solid black";
	}
}

function what_find(e,find_text){
	find_now = find_text
	input_find.placeholder = "Find "+find_now
	all_border_black()
	if (find_text=="users"){
		users.style.display = "block"
		musics.style.display = "none"
		videos.style.display = "none"
	}else	if (find_text=="musics"){
		users.style.display = "none"
		musics.style.display = "block"
		videos.style.display = "none"
	}else	if (find_text=="videos"){
		users.style.display = "none"
		musics.style.display = "none"
		videos.style.display = "block"
	}
	e.style.borderBottom = "2px solid white";
	ajax_elements()
}

ajax_elements()