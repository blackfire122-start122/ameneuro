conn_u = new WebSocket("ws://"+window.location.hostname+"/user/"+username)

// conn_u_hac = new WebSocket("ws://"+window.location.hostname+"/user/"+"igor")
// conn_u_hac.onopen = ()=>{
// 	conn_u_hac.send(JSON.stringify({'type':'add_mus_share','id':3, 'hac':"test hac"}))
// 	conn_u_hac.send(JSON.stringify({'type':'delete_theme','th_id':theme,'del_el':4}))
// }

conn_u.onmessage = onmessage_u

let chats_point = []

function onmessage_u(e){
	let data = JSON.parse(e.data)
	if (data['type']=='msg'){
		msg_span = document.getElementById(data['from_chat'])
		menu_id = document.getElementById('menu_id')
		let msg_point = document.getElementById('chats')

		if (msg_span){
			msg_span.innerText = data["msg"]
			msg_span.parentNode.parentNode.childNodes[5].className = "point"
		}
		if(msg_point){
			msg_point.style.display = "block"
			if (!chats_point.includes(data['from_chat'])) {
				msg_point.childNodes[0].innerText = parseInt(msg_point.innerText)+1
				chats_point.push(data['from_chat'])
			}
		}
		if(menu_id){
			menu_id.style.display = "block"
		}

	}else if (data['type']=='share_mus'){
		menu_id = document.getElementById('menu_id')

		if(musics_point){
			musics_point.style.display = "block"
			musics_point.childNodes[0].innerText = parseInt(musics_point.innerText)+1
		}
		if(menu_id){
			menu_id.style.display = "block"
		}
		
	}else if (data['type']=='activity'){
		menu_id = document.getElementById('menu_id')

		if(activity_point){
			activity_point.style.display = "block"
			activity_point.childNodes[0].innerText = parseInt(activity_point.innerText)+1
		}
		if(menu_id){
			menu_id.style.display = "block"
		}

	} else if (data['type']=='in_net'){
		if (data["user_in"] == username){
			conn_u.send(JSON.stringify({'type':'yes_in_net','user_in': username}))	
		}
	} else if (data['type']=='yes_in_net'){
		if(data["user_in"]!=username){
			for (var i = user_ch.length - 1; i >= 0; i--) {
				if(user_ch[i].innerText==data["user_in"]){
					user_ch[i].parentNode.parentNode.childNodes[1].childNodes[3].style.display = "block"
				}
			}
		}
	} else if (data['type']=='disconnect'){
		for (var i = user_ch.length - 1; i >= 0; i--) {
			if(user_ch[i].innerText==data["user_in"]){
				user_ch[i].parentNode.parentNode.childNodes[1].childNodes[3].style.display = "none"
			}
		}
	}
	console.log(data)
}

conn_u.onopen = ()=>{
	conn_u.send(JSON.stringify({'type':'yes_in_net','user_in': username}))
}

function add_mus_share(e){	
	conn_u.send(JSON.stringify({'type':'add_mus_share', "id":e.value}))
}
function not_add_mus_share(e){
	conn_u.send(JSON.stringify({'type':'not_add_mus_share', "id":e.value}))
}
function mus_share(e,name){
	e.style.opacity = "0.5"
	conn_u.send(JSON.stringify({'type':'mus_share', "id":music_share_id, "to_user":e.value}))
	conn_share_mus = new WebSocket("ws://"+window.location.hostname+"/user/"+name)
	
	conn_share_mus.onopen = ()=>{
		conn_share_mus.send(JSON.stringify({'type':'share_mus'}))
		conn_share_mus.send(JSON.stringify({'type':'activity'}))
		conn_share_mus.close()
	}
}
function add_mus(e){
	e.remove()
	conn_u.send(JSON.stringify({'type':'add_to_me', "id":e.value}))
}
function delete_mus(e){
	conn_u.send(JSON.stringify({'type':'delete_mus', "id":e.value}))
}
function del_friend(e,id){
	conn_u.send(JSON.stringify({'type':'delete_friend', "id":id}))
	e.parentNode.remove()
}
