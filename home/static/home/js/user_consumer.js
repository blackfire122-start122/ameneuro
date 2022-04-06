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

		if (data["type_media"]=="post"){
			$.ajax({
				type: $(this).attr('post'),
				url: post_ajax,
				data: {"type":"play_in_all", "id":data["id"]},
				success: function (response) {
					div.innerHTML += response
					let audio = document.querySelector("#audio_play_in_all")
					let timeline = document.querySelector("#timeline_play_in_all")
					set_click_audio_timeline(data,audio,timeline)
				}
			})
		}else if(data["type_media"]=="music"){
			$.ajax({
				type: $(this).attr('post'),
				url: musics_all_ajax,
				data: {'type':'music','pia':'play_in_all'},
				success: function (response) {
					div.innerHTML += response
					let audio = document.querySelector("#audio_play_in_all_"+data["id"])
					let timeline = document.querySelector("#timeline_play_in_all_"+data["id"])
					set_click_audio_timeline(data,audio,timeline)
				}
			})
		}else if(data["type_media"]=="playlist"){
			$.ajax({
				type: $(this).attr('post'),
				url: musics_all_ajax,
				data: {'pia':'play_in_all','type':'playlist','ps':data["id_playlist"]},
				success: function (response) {
					div.innerHTML += response
					let audio = document.querySelector("#audio_play_in_all_"+data["id"])
					let timeline = document.querySelector("#timeline_play_in_all_"+data["id"])
					
					set_click_audio_timeline(data,audio,timeline)
				}
			})
		}

		img_right_el.id = "img_right_el"
		img_right_el.src = img_right
		img_right_el.style.display = "block"
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
		div.style.display = "none"
		div.style.maxHeight = "150px"
		div.style.overflowY = "auto"

		img_left_el.src = img_left
		img_left_el.id = "img_left_el"
		img_left_el.style.position = "absolute"
		img_left_el.style.right = "10px"
		img_left_el.style.color = "white"
		img_left_el.style.width = "40px"
		img_left_el.style.zIndex = "10"

		div.appendChild(img_left_el)
		document.body.append(div)
		document.body.append(img_right_el)

	}else if (data['type']=='recognize'){
		h2 = document.getElementById("recognize_h2")
		p = document.getElementById("p_confidence")

		p.innerText = "On "+data["procent"]+"%"
		h2.innerText = data['recognize']
	}else if(data['type']=='add_to_playlists'){
		p = document.createElement("p")
		p.innerText = data["name_mus"]+','
		document.querySelector(".musics_in_playlists").append(p)
	}else if(data['type']=='not_add_to_playlists'){
		mip = document.querySelector(".musics_in_playlists").childNodes
		for (var i = mip.length - 1; i >= 0; i--) {
			if(mip[i].innerText==data["name_mus"]+','){
				mip[i].remove()
			}
		}
	}
	console.log(data)
}

function set_click_audio_timeline(data,audio,timeline){
	document.getElementById("img_left_el").addEventListener("click",()=>{
		document.querySelector(".play_in_all_div").style.display = "none"
		document.querySelector("#img_right_el").style.display = "block"
	})

	audio.currentTime = data["currentTime"]
	audio.addEventListener("timeupdate", ()=>{
		const percentagePosition = (100*audio.currentTime) / audio.duration
		timeline.style.backgroundSize = `${percentagePosition}% 100%`
		timeline.value = percentagePosition
		if(Math.round(percentagePosition)%2==0){
			conn_u.send(JSON.stringify({'type':'play_in_all_current_time',"currentTime":audio.currentTime}))
		}
	})
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
function play_in_all(e,id,type){
	e.style.opacity = "0.5"
	if (type=="post") {
		conn_u.send(JSON.stringify({'type':'play_in_all',"type_media":type,"id":id,"currentTime":e.parentNode.childNodes[3].currentTime}))
	}else if (type=="music") {
		conn_u.send(JSON.stringify({'type':'play_in_all',"type_media":type,"id":id,"currentTime":e.parentNode.parentNode.childNodes[3].currentTime}))
	}else if (type=="playlist") {
		conn_u.send(JSON.stringify({'type':'play_in_all',"type_media":type,"id_playlist":id,"id":"first_id_music","currentTime":0}))
	}
	document.querySelector(".play_in_all_div").remove()
	conn_u.send(JSON.stringify({'type':'get_play_in_all'}))
}

function toggleAudio_play_in_all(btn,id,type,id_playlist){
	if (type == "musics"){
		conn_u.send(JSON.stringify({'type':'play_in_all',"type_media":type,"id":id,"currentTime":btn.parentNode.parentNode.childNodes[3].currentTime}))
	}else if(type == "playlist"){
		conn_u.send(JSON.stringify({'type':'play_in_all',"type_media":type,"id_playlist":id_playlist,"id":id,"currentTime":btn.parentNode.parentNode.childNodes[3].currentTime}))
	}
	toggleAudio(btn,selector_audio='audio_play_in_all_',selector_timeline='timeline_play_in_all_')
}

function changeSeek_play_in_all(timeline,id,type,id_playlist){
	audio = timeline.parentNode.parentNode.childNodes[3]
	if (type == "musics"){
		conn_u.send(JSON.stringify({'type':'play_in_all',"type_media":type,"id":id,"currentTime":audio.currentTime}))
	}else if(type == "playlist"){
		conn_u.send(JSON.stringify({'type':'play_in_all',"type_media":type,"id_playlist":id_playlist,"id":id,"currentTime":audio.currentTime}))
	}
	changeSeek(timeline)

	audio.addEventListener("timeupdate", ()=>{
		const percentagePosition = (100*audio.currentTime) / audio.duration
		if(Math.round(percentagePosition)%2==0){
			conn_u.send(JSON.stringify({'type':'play_in_all_current_time',"currentTime":audio.currentTime}))
		}
	})
}
