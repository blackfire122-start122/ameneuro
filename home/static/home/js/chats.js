user_ch = document.getElementsByClassName("user_ch")
let chats = document.querySelector(".chats")

let start_chat = 0
let end_chat = how_get
let clear = true
let find_ch

let ajax_now = "get"

for (var i = user_ch.length - 1; i >= 0; i--) {
	let user_in = user_ch[i].innerText
	conn_u_f = new WebSocket(wsStart+window.location.hostname+":"+location.port+"/ws/user/"+user_in)
	conn_u_f.onopen = (e)=>{
		e.target.send(JSON.stringify({'type':'in_net',"user_in":user_in}))	
	}
	conn_u_f.onmessage = onmessage_u
}

function find_inp(e){
	clear = true
	find_ch = e.value
	ajax_now = "find"
	start_chat = 0
	end_chat = how_get
	ajax_new()
}

function find_chat(){
	$.ajax({
		url:chat_find_ajax,
		data: {"find_ch":find_ch,"start_chat":start_chat, "end_chat":end_chat},
		success: function (response){
			chats.innerHTML += response
			if (clear){
				chats.innerHTML = response
				clear = false
			}else{
				chats.innerHTML += response
			}
			start_chat += how_get
			end_chat += how_get
		}
	})
}

function get_chats(e){
	$.ajax({
		url:get_chats_ajax,
		data: {"start_chat":start_chat, "end_chat":end_chat},
		success: function (response){
			if (clear){
				chats.innerHTML = response
				clear = false
			}else{
				chats.innerHTML += response
			}
			start_chat += how_get
			end_chat += how_get
		}
	})
}

function ajax_new(){
	if (ajax_now=="get"){
		get_chats()
	}else if(ajax_now=="find"){
		find_chat()
	}
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
let get_can = true

async function get_can_true() {
	await sleep(700)
	get_can = true
}

window.addEventListener('scroll', ()=>{
	if($(window).scrollTop()+$(window).height()>=$(document).height()-500){
		if (get_can) {
		    ajax_new()
		    get_can = false
		    get_can_true(700)
		}
	}
})

ajax_new()