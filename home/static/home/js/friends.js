friends = document.querySelector(".friends")

let friends_start = 0
let friends_end = how_get

let users_find_start = 0
let users_find_end = how_get

let clear = true
let find_str

function add_chat(btn) {
	conn_u.send(JSON.stringify({'type':'add_chat', "id":btn.value}))
	btn.style.display = "none"
}

function add_friend(btn) {
	conn_u.send(JSON.stringify({'type':'add_friend', "id":btn.value}))
	
	let pn = btn.parentNode

	let button = document.createElement('button')
	button.innerText = 'Add chat'
	button.className = "write_btn"
	button.value = btn.value
	button.onclick = () => {add_chat(button)}

	let button_del = document.createElement('button')
	button_del.innerText = 'Delete friend'
	button_del.className = "btn_delete_friend"
	button_del.onclick = () => {del_friend(button_del,btn.value)}

	pn.append(button_del)
	pn.append(button)

	pn.childNodes[3].remove()
	pn.childNodes[4].remove()
}

function no_add_friend(btn) {
	conn_u.send(JSON.stringify({'type':'no_add_friend', "id":btn.value}))
	btn.parentNode.remove()
}

function get_friends(){
	$.ajax({
		type: $(this).attr('post'),
		url: users_get_ajax,
		data: {"user":id_user,"type":"friends_and_want","users_start":friends_start,"users_end":friends_end},
		success: function (response){
			friends.innerHTML += response
			friends_start+=how_get
			friends_end+=how_get
		}
	})
}

function find_inp(e){
	find_str = e.value
	clear = true
	users_find_start = 0
	users_find_end = how_get
	get_users_find()
}

function get_users_find(){
	$.ajax({
		type: $(this).attr('post'),
		url: user_find_ajax,
		data: {"type":"friends_and_want","find_name":find_str,"users_find_start":users_find_start,"users_find_end":users_find_end},
		success: function (response){
			if (clear){
				friends.innerHTML = response
				clear = false
			}else{
				friends.innerHTML += response
			}
			window.removeEventListener('scroll',scroll_event);
			window.addEventListener('scroll', scroll_event_find)
			users_find_start+=how_get
			users_find_end+=how_get
		}
	})
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

window.addEventListener('scroll', scroll_event)
function scroll_event(e) {
	if($(window).scrollTop()+$(window).height()>=$(document).height()-500){
	    if (get_can){
	    	get_friends()
	    	get_can = false
	    	get_can_true()
		}
	}
}

function scroll_event_find(e) {
	if($(window).scrollTop()+$(window).height()>=$(document).height()-500){
	    if (get_can){
	    	get_users_find()
	    	get_can = false
	    	get_can_true()
		}
	}
}

let get_can = true
async function get_can_true() {
	await sleep(700)
	get_can = true
}

get_friends()