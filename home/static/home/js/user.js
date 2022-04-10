musics = document.querySelector('.musics')
posts = document.querySelector('.posts')

let musics_s = true

let friends_start = 0
let friends_end = how_get

let followers_start = 0
let followers_end = how_get

let posts_start = 0
let posts_end = how_get

let = friends_show = document.querySelector(".friends_show")
let = followers_show = document.querySelector(".followers_show")

friends_show.addEventListener("scroll",scroll_fr)
followers_show.addEventListener("scroll",scroll_fl)

function music_show(){
	if(musics_s){
		musics.style.display = 'block'
	}else{
		musics.style.display = 'none'
	}
	musics_s = !musics_s
}

function follow(btn,user) {
	conn_u.send(JSON.stringify({'type':'follow', "id":btn.value}))
	
	conn_u_f = new WebSocket("ws://"+window.location.hostname+"/user/"+user)	
	conn_u_f.onopen = ()=>{
		conn_u_f.send(JSON.stringify({'type':'activity'}))
		conn_u_f.close()
	}
	
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
		if (get_fr_can) {
			get_friends()
	 		get_fr_can = false
	 		get_can_fr_true()
	 	}
	}
}

function scroll_fl(e){
	if(e.target.scrollHeight-e.target.scrollTop<500){
		if (get_fl_can) {
			get_followers()
	 		get_fl_can = false
	 		get_can_fl_true()
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
let get_fr_can = true
let get_fl_can = true

async function get_can_fr_true() {
	await sleep(700)
	get_fr_can = true
}
async function get_can_fl_true() {
	await sleep(700)
	get_fl_can = true
}

function want_add_friend(btn) {
	conn_u.send(JSON.stringify({'type':'want_add_friend', "id":btn.value}))
	btn.disabled = true
	btn.style.display = "none"
	document.getElementById(btn.value).style.display = "none"
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

pu_ajax()

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
	 		pu_ajax()
	 		get_can = false
	 		get_can_true()
	 	}
	}
})

