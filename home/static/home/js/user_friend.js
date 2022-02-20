let users = document.querySelector(".users")
let how_get = 20
let users_start = 0
let users_end = how_get
let users_find_start = 0
let users_find_end = how_get
let clear = true
let find_str

function find_inp(e){
	if(event.key === 'Enter') {
		find_str = e.value
		clear = true
		users_find_start = 0
		users_find_end = how_get
		get_users_find()
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

function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}

function get_users(){
	$.ajax({
		type: $(this).attr('post'),
		url: users_get_ajax,
		data: {"users_start":users_start,"users_end":users_end},
		success: function (response){
			users.innerHTML += response
			users_start+=how_get
			users_end+=how_get
		}
	})
}

get_users()

window.addEventListener('scroll', scroll_event)
function scroll_event(e) {
	if($(window).scrollTop()+$(window).height()>=$(document).height()-500){
	    get_users()
	    sleep(700)
	}
}

function scroll_event_find(e) {
	if($(window).scrollTop()+$(window).height()>=$(document).height()-500){
	    get_users_find()
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