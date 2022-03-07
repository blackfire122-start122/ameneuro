musics = document.querySelector('.musics')

let musics_s = true
let how_get = 20

let friends_start = 0
let friends_end = how_get

let followers_start = 0
let followers_end = how_get

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
		get_friends()
		sleep(700)
	}
}

function scroll_fl(e){
	if(e.target.scrollHeight-e.target.scrollTop<500){
		get_followers()
		sleep(700)
	}
}

function close_friends(e){
	e.parentNode.style.display = "none"
}
function close_followers(e){
	e.parentNode.style.display = "none"
}

function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}