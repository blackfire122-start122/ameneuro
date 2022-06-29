let loc = window.location
let wsStart = 'ws://'
if (loc.protocol == 'https:') {
  wsStart = 'wss://'
}

conn_u = new WebSocket(wsStart+window.location.hostname+":"+location.port+"/ws/user/"+username)
conn_u.onmessage = onmessage_u
let chats_point = []

let how_get = 20
let musics_start_pia = 0
let musics_end_pia = how_get
let user_ch = false;

function onmessage_u(e){
	let data = JSON.parse(e.data)
	if (data['type']=='msg'){
		msg_span = document.getElementById(data['from_chat'])
		menu_id = document.getElementById('menu_id')
		let msg_point = document.getElementById('chats')

		if (msg_span){
			msg_span.className = 'not_read'
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
	}else if (data['type']=='readable'){
		console.log(data)
		if (data['from'].split(' ').includes('other_msgs')) {
			msg_span = document.getElementById(data['from_chat'])
			msg_span.innerText = data['msg']+" Revised"
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
	}else if (data['type']=='yes_in_net'){
		if (user_ch){
			if(data["user_in"]!=username){
				for (var i = user_ch.length - 1; i >= 0; i--) {
					if(user_ch[i].innerText==data["user_in"]){
						user_ch[i].parentNode.parentNode.childNodes[1].childNodes[3].style.display = "block"
					}
				}
			}
		}
	}else if (data['type']=='disconnect'){
		if (user_ch){
			for (var i = user_ch.length - 1; i >= 0; i--) {
				if(user_ch[i].innerText==data["user_in"]){
					user_ch[i].parentNode.parentNode.childNodes[1].childNodes[3].style.display = "none"
				}
			}
		}

	}else if (data['type']=='get_play_in_all'){
		let div = document.createElement('div')
		let img_right_el = document.createElement('img')
		let img_left_el = document.createElement('img')

		let get_pia

		if (data["type_media"]=="post"){
			post_pia(data,div)
			get_pia = post_pia 
		}else if(data["type_media"]=="music"){
			music_pia(data,div)
			get_pia = music_pia
		}else if(data["type_media"]=="playlist"){
			playlist_pia(data,div)
			get_pia = playlist_pia
		}

		div.addEventListener('scroll', ()=>{
			if(div.scrollHeight-$(div).scrollTop()<200){
			  if (get_can_pia) {
			 		get_pia(data,div)
			 		get_can_pia = false
			 		get_can_true_pia()
			 	}
			}
		})

		img_left_el.id = "img_left_el"
		img_left_el.src = img_left
		img_left_el.style.display = "block"
		img_left_el.style.position = "fixed"
		img_left_el.style.right = "-30px"
		img_left_el.style.bottom = "120px"
		img_left_el.style.height = "40px"

		img_left_el.addEventListener("click",()=>{
			document.querySelector(".play_in_all_div").style.display = "block"
			img_left_el.style.display = "none"
		})

		div.className = "play_in_all_div"
		div.style.position = "fixed"
		div.style.bottom = "8%"
		div.style.right = "0"
		div.style.width = "60%"
		div.style.marginLeft = "0 auto"
		div.style.padding = "5px 2px"
		div.style.background = "rgba(0,0,0,0.6)"
		div.style.borderRadius = "5px"
		div.style.display = "none"
		div.style.maxHeight = "150px"
		div.style.overflowY = "auto"

		img_right_el.src = img_right
		img_right_el.id = "img_right_el"
		img_right_el.style.position = "absolute"
		img_right_el.style.right = "10px"
		img_right_el.style.color = "white"
		img_right_el.style.width = "40px"
		img_right_el.style.zIndex = "10"

		div.appendChild(img_right_el)
		document.body.append(div)
		document.body.append(img_left_el)

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
}

function set_click_audio_timeline(data,audio,timeline){
	document.getElementById("img_right_el").addEventListener("click",()=>{
		document.querySelector(".play_in_all_div").style.display = "none"
		document.querySelector("#img_left_el").style.display = "block"
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
	if (share_now == "ps"){
		conn_u.send(JSON.stringify({'type':'ps_share', "id":share_id, "to_user":e.value}))
		conn_share_ps = new WebSocket(wsStart+window.location.hostname+":"+location.port+"/ws/user/"+name)
		
		conn_share_ps.onopen = ()=>{
			conn_share_ps.send(JSON.stringify({'type':'share_mus'}))
			conn_share_ps.send(JSON.stringify({'type':'activity'}))
			conn_share_ps.close()
		}

	}else if(share_now == "mus"){
		conn_u.send(JSON.stringify({'type':'mus_share', "id":share_id, "to_user":e.value}))
		conn_share_mus = new WebSocket(wsStart+window.location.hostname+":"+location.port+"/ws/user/"+name)
		
		conn_share_mus.onopen = ()=>{
			conn_share_mus.send(JSON.stringify({'type':'share_mus'}))
			conn_share_mus.send(JSON.stringify({'type':'activity'}))
			conn_share_mus.close()
		}
	}
	e.style.opacity = "0.5"
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

function playlist_pia(data,div){
	$.ajax({
		type: $(this).attr('post'),
		url: musics_all_ajax,
		data: {'pia':'play_in_all','type':'playlist','ps':data["id_playlist"],"musics_start":musics_start_pia, "musics_end":musics_end_pia},
		success: function (response) {
	  	resp = $(response)
	    for (let i = resp.length - 1; i >= 0; i--) {
	   		div.appendChild(resp[i])
	    }

			let audio = document.querySelector("#audio_play_in_all_"+data["id"])
			let timeline = document.querySelector("#timeline_play_in_all_"+data["id"])
			musics_start_pia += how_get
			musics_end_pia += how_get
			set_click_audio_timeline(data,audio,timeline)
		}
	})
}

function music_pia(data,div){
	$.ajax({
		type: $(this).attr('post'),
		url: musics_all_ajax,
		data: {'type':'music','pia':'play_in_all',"musics_start":musics_start_pia, "musics_end":musics_end_pia},
		success: function (response) {
	  	resp = $(response)
	    for (let i = resp.length - 1; i >= 0; i--) {
	   		div.appendChild(resp[i])
	    }

			let audio = document.querySelector("#audio_play_in_all_"+data["id"])
			let timeline = document.querySelector("#timeline_play_in_all_"+data["id"])
			musics_start_pia += how_get
			musics_end_pia += how_get
			set_click_audio_timeline(data,audio,timeline)
		}
	})
}

function post_pia(data,div){
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
}

function sleep_pia(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
let get_can_pia = true

async function get_can_true_pia() {
	await sleep_pia(700)
	get_can_pia = true
}

function add_ps_share(e){	
	conn_u.send(JSON.stringify({'type':'add_ps_share', "id":e.value}))
}
function not_add_ps_share(e){
	conn_u.send(JSON.stringify({'type':'not_add_ps_share', "id":e.value}))
}
function delete_ps_form_me(e){
	conn_u.send(JSON.stringify({'type':'delete_ps_form_me', "id":e.value}))
}