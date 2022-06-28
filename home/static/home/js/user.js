musics = document.querySelector('.musics')
posts = document.querySelector('.posts')
videos = document.querySelector('.videos')
close_musics = document.querySelector(".close_musics")

let friends_start = 0
let friends_end = how_get

let followers_start = 0
let followers_end = how_get

let posts_start = 0
let posts_end = how_get

let videos_start = 0
let videos_end = how_get

let musics_start = 0
let musics_end = how_get

let = friends_show = document.querySelector(".friends_show")
let = followers_show = document.querySelector(".followers_show")

let show_now = "posts"

friends_show.addEventListener("scroll",scroll_fr)
followers_show.addEventListener("scroll",scroll_fl)

document.getElementById("start_show").style.borderBottom = "2px solid white";

function music_show(){
	close_musics.style.display = "block"
	musics.style.display = 'block'
	get_my_musics()
}

function close_musics_f(){
	close_musics.style.display = "none"
	musics.style.display = 'none'
}

function follow(btn,user) {
	conn_u.send(JSON.stringify({'type':'follow', "id":btn.value}))
	
	conn_u_f = new WebSocket(wsStart+window.location.hostname+":"+location.port+"/ws/user/"+user)	
	conn_u_f.onopen = ()=>{
		conn_u_f.send(JSON.stringify({'type':'activity'}))
		conn_u_f.close()
	}

	btn.className = "btn_no_follow"
	btn.innerText = "Not follow"
	btn.onclick = ()=>{not_follow(btn,user)}
}

function not_follow(btn,user){
	conn_u.send(JSON.stringify({'type':'not_follow', "id":btn.value}))

	btn.className = "btn_follow"
	btn.innerText = "Follow"
	btn.onclick = ()=>{follow(btn,user)}
}

function get_my_musics(){
	$.ajax({
	  type: $(this).attr('post'),
	  url: musics_all_ajax,
	  data: {'id':id_user,'type':'user_music_add',"musics_start":musics_start,"musics_end":musics_end},
	  success: function (response){	    
	  	resp = $(response)
	    for (let i = resp.length - 1; i >= 0; i--) {
	   		musics.appendChild(resp[i])
	    }

	    musics_start += how_get
			musics_end += how_get
	  }
	})
}

musics.addEventListener("scroll", ()=>{
	if(musics.scrollHeight-musics.scrollTop<500){
		if (get_can) {
			get_my_musics()
	 		get_can = false
	 		get_can_true()
	 	}
	}
})

function get_friends(){
	$.ajax({
		type: $(this).attr('post'),
		url: users_get_ajax,
		data: {"user":id_user,"type":"friends","users_start":friends_start,"users_end":friends_end},
		success: function (response){
			friends_show.innerHTML += response
			friends_start+=how_get
			friends_end+=how_get
			friends_show.style.display = "block"
		}
	})
	close_followers(document.querySelector("#close_fl"))
}

function get_followers(){
	$.ajax({
		type: $(this).attr('post'),
		url: users_get_ajax,
		data: {"user":id_user,"type":"followers","users_start":followers_start,"users_end":followers_end},
		success: function (response){
			followers_show.innerHTML += response
			followers_start+=how_get
			followers_end+=how_get
			followers_show.style.display = "block"
		}
	})
	close_friends(document.querySelector('#close_fr'))
}

function scroll_fr(e){
	if(e.target.scrollHeight-e.target.scrollTop<500){
		if (get_can) {
			get_friends()
	 		get_can = false
	 		get_can_true()
	 	}
	}
}

function scroll_fl(e){
	if(e.target.scrollHeight-e.target.scrollTop<500){
		if (get_can) {
			get_followers()
	 		get_can = false
	 		get_can_true()
	 	}
	}
}

function close_friends(e){
	e.parentNode.style.display = "none"
}
function close_followers(e){
	e.parentNode.style.display = "none"
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function want_add_friend(btn) {
	conn_u.send(JSON.stringify({'type':'want_add_friend', "id":btn.value}))
	btn.disabled = true
	btn.style.display = "none"
}

function pu_ajax(){
	$.ajax({
		type: $(this).attr('post'),
		url: post_user_ajax,
		data: {"user":id_user,"posts_start":posts_start,"posts_end":posts_end},
		success: function (response){
			posts.innerHTML += response
			posts_start+=how_get
			posts_end+=how_get
		}
	})
}

function vu_ajax(){
	$.ajax({
		type: $(this).attr('post'),
		url: video_user_ajax,
		data: {"user":id_user,"videos_start":videos_start,"videos_end":videos_end},
		success: function (response){
			videos.innerHTML += response
			videos_start+=how_get
			videos_end+=how_get
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

window.addEventListener('scroll', async function(e) {
	if($(window).scrollTop()+$(window).height()>=$(document).height()-500){
	  if (get_can) {
	 		ajax_elements()
	 		get_can = false
	 		get_can_true()
	 	}
	}
})


function ajax_elements(){
	if (show_now == "posts"){
		pu_ajax()
	}else if (show_now == "videos"){
		vu_ajax()
	}
}

function all_border_black(){
	btns = document.getElementsByClassName('what_show_btn')
	for(let i=btns.length-1;i>=0; i--){
			btns[i].style.borderBottom = "2px solid black";
	}
}

function what_find(e,show_text){
	show_now = show_text
	all_border_black()
	if (show_text=="posts"){
		posts.style.display = "grid"
		videos.style.display = "none"
	}else	if (show_text=="videos"){
		posts.style.display = "none"
		videos.style.display = "grid"
	}
	e.style.borderBottom = "2px solid white"
	ajax_elements()
}

ajax_elements()
