conn_u = new WebSocket("ws://"+window.location.hostname+"/user/"+username)

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
	}else if (data['type']=='get_play_in_all'){
		let div = document.createElement('div')
		let img_left_el = document.createElement('img')
		let img_right_el = document.createElement('img')

		$.ajax({
		  type: $(this).attr('post'),
		  url: post_ajax,
		  data: {"type":"play_in_all", "id":data["id"]},
		  success: function (response) {
		    div.innerHTML += response
		    
		    document.getElementById("img_left_el").addEventListener("click",()=>{
		    	document.querySelector(".play_in_all_div").style.display = "none"
		    	img_right_el.style.display = "block"
		    })
		  }
		})

		img_right_el.src = img_right
		img_right_el.style.display = "none"
		img_right_el.style.position = "fixed"
		img_right_el.style.left = "-30px"
		img_right_el.style.bottom = "100px"
		img_right_el.style.height = "40px"

		img_right_el.addEventListener("click",()=>{
		   	document.querySelector(".play_in_all_div").style.display = "block"
			img_right_el.style.display = "none"
		})

		div.className = "play_in_all_div"
		div.style.position = "fixed"
		div.style.bottom = "0"
		div.style.left = "0"
		div.style.width = "50%"
		div.style.marginLeft = "0 auto"
		div.style.padding = "5px 2px"
		div.style.background = "rgba(0,0,0,0.6)"
		div.style.borderRadius = "5px"

		img_left_el.src = img_left
		img_left_el.id = "img_left_el"
		img_left_el.style.position = "absolute"
		img_left_el.style.right = "10px"
		img_left_el.style.color = "white"
		img_left_el.style.width = "40px"

		div.appendChild(img_left_el)
		document.body.append(div)
		document.body.append(img_right_el)

	}
	console.log(data)
}

conn_u.onopen = ()=>{
	conn_u.send(JSON.stringify({'type':'yes_in_net','user_in': username}))
	conn_u.send(JSON.stringify({'type':'get_play_in_all'}))
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
function play_in_all(e,id){
	e.style.opacity = "0.5"
	conn_u.send(JSON.stringify({'type':'play_in_all',"id":id}))
	document.querySelector(".play_in_all_div").remove()
	conn_u.send(JSON.stringify({'type':'get_play_in_all'}))
}


// conn_u_hac = new WebSocket("ws://"+window.location.hostname+"/chat/"+"Cm3HR4BPQCIGAEwrwJRftmAl6kORuP")
// conn_u_hac.onopen = ()=>{
// 	conn_u_hac.send(JSON.stringify({'type':'first_msg'}))
// 	conn_u_hac.send(JSON.stringify({'type':'msg','msg': "hacceds"}))
// }

// function onmes_hac(e){
// 	let data = JSON.parse(e.data)
// }

// conn_u_hac.onmessage = onmes_hac
