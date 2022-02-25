conn_u = new WebSocket("ws://"+window.location.hostname+"/user/"+username)
conn_u.onmessage = onmessage_u

let chats_point = []

function onmessage_u(e){
	let data = JSON.parse(e.data)
	if (data['type']=='msg'){
		msg_span = document.getElementById(data['from_chat'])
		msg_point = document.getElementById('chats')
		menu_id = document.getElementById('menu_id')

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
	}
	console.log(data)
}

msg_point = document.getElementById('chats')
if (msg_point){
	if(msg_point.childNodes[0].innerText!=0){
		msg_point.style.display = "block"
		menu_id.style.display = "block"
	}
}

conn_u.onopen = ()=>{
	conn_u.send(JSON.stringify({'type':'first_conn','user': username}))	
}

function add_mus_share(e){
	conn_u.send(JSON.stringify({'type':'add_mus_share', "id":e.value}))
}
function not_add_mus_share(e){
	conn_u.send(JSON.stringify({'type':'not_add_mus_share', "id":e.value}))
}
function mus_share(e){
	conn_u.send(JSON.stringify({'type':'mus_share', "id":music_share_id, "to_user":e.value}))
}
function add_mus(e){
	conn_u.send(JSON.stringify({'type':'add_to_me', "id":e.value}))
}
function delete_mus(e){
	conn_u.send(JSON.stringify({'type':'delete_mus', "id":e.value}))
}
