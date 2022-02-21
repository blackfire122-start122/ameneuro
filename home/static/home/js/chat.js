let msg_user = document.querySelector("#msg_user")
let msg_div = document.querySelector('.messages')
let musics = document.querySelector('.musics')
let music

conn = new WebSocket("ws://"+window.location.hostname+"/chat/"+chat)
conn.onmessage = onmessage

conn_u_f = new WebSocket("ws://"+window.location.hostname+"/user/"+friend)

m_play = true
m_pause = true
m_time = true

function onmessage(e){
	let data = JSON.parse(e.data)
	if (data['type']=='first_msg'){
		for (i=0;i<data['musics_url'].length;i++){

			musics.innerHTML += `<div class="audio-player"><h4 class="name_mus">` + "name" +
			`</h4><audio onseeked="seeked_m(this)" onplay="play_m(this)" onpause="pause_m(this)" class="music" id="` + data['musics_url'][i][1] + 
			`" src="` + data['musics_url'][i][0] + 
			`"></audio><div class="controls"><button value="` + data['musics_url'][i][1] + 
			`" onclick="toggleAudio(this)" class="player-button"><img class="play_pause_img" src="/static/home/images/pause.png" alt=""></button><input id="timeline_` + data['musics_url'][i][1] + 
			`" onchange ="changeSeek(this)" type="range" class="timeline" max="100" value="0"></div></div>`	
		}

	}else if (data['type']=='msg'){
		conn_u_f.send(JSON.stringify({'type':'msg','msg':data["msg"],'from_user': user, "from_chat":chat}))
		
		let div_ = document.createElement('div')
		let div = document.createElement('div')
		let p = document.createElement('p')
		let time = document.createElement('time')
		let readeble = document.querySelector('.readeble')

		if (data["user"]==user) {
			div.className = "my_msgs"
		}else{
			div.className = "other_msgs"
		}

		div.style.background = "rgba("+rgba[0]+","+rgba[1]+","+rgba[2]+","+color_mes_bg_op + ")"

		p.className="mes"
		p.innerText = data["msg"]

		time.className = 'time'
		time.innerText = data["time"].slice(11,16)

		div.append(p)
		div.append(time)
		div_.append(div)
		msg_div.append(div_)
		readeble.innerText = 'not read'

	}else if(data['type']=='new_theme'){
		conn_u_f.send(JSON.stringify({'type':'msg','msg':data['msg_new_theme'],'from_user': user, "from_chat":chat}))

		let div = document.createElement('div')
		let p = document.createElement('p')

		div.className = "new_theme"
		p.innerText = data['msg_new_theme']

		div.append(p)
		msg_div.append(div)

	}else if(data['type']=='delete_theme'){
		if (data["error"]){
			let error = document.querySelector('#error')
			error.innerText = data["error"]
			error.style.display='block'
		}
		if (data["error"]!="This chat theme"){
			document.getElementById(data["del_el"]).remove()
		}

	}else if(data['type']=='end_readable'){
		let readeble = document.querySelector('.readeble')
		if (data['readeble'] == 'True'){
			readeble.innerText = 'Read'
		}else{
			readeble.innerText = 'not read'
		}
	}else if(data['type']=='play_mus'){
		all_pause()
		music = document.getElementById(data['m_id'])
		music.play()
		setTimeout(()=>{m_play = true},300)
	}else if(data['type']=='pause_mus'){
		all_pause()
		music.pause()
		setTimeout(()=>{m_pause = true},300)
	}else if(data['type']=='seeked'){
		music = document.getElementById(data['m_id'])
		all_pause()
		music.currentTime = data['time']
		setTimeout(()=>{
			m_time = true
			music.play()
			},300)
	}else if(data['type']=='get_seeked'){
		if (music){
			conn.send(JSON.stringify({'type':'set_seeked','time':music.currentTime, 'm_id':music.id}))
		}
	}
	else if(data['type']=='set_seeked'){
		music.ontimeupdate = null
		music = document.getElementById(data['m_id'])
		music.currentTime = data["time"]
		setTimeout(()=>{
			m_time = true
			music.play()
		},300)
	}
	else if(data['type']=='msg_file'){
		conn_u_f.send(JSON.stringify({'type':'msg','msg':data["msg"],'from_user': user, "from_chat":chat}))

		if (data["type_file"] == "audio"){
			element = `
				<div>
					<div class="my_msgs file_mes">
						<div class="audio-player">
							<h4 class="name_mus">` + data["msg"] + `</h4>
							<audio class="audio_ap" id="audio_`+data["id"]+`" src="`+data["src"]+`"></audio>
							<div class="controls">
								<button value="`+data["id"]+`" onclick="toggleAudio_mess(this)" class="player-button"><img class="play_pause_img" src="`+pause_img+`" alt=""></button>
								<input id="timeline_`+data["id"]+`" onchange ="changeSeek_mess(this)" type="range" class="timeline" max="100" value="0">
							</div>
						</div>
						<p class="mes">` + data["msg"] + `</p>
						<time class='time'>` +data["time"]+ `</time>
					</div>
				</div>
			`
			msg_div.innerHTML += element
			readeble.innerText = 'not read'
			return
		}

		let div_ = document.createElement('div')
		let div = document.createElement('div')
		let p = document.createElement('p')
		let time = document.createElement('time')
		let readeble = document.querySelector('.readeble')
		let file = document.createElement(data["type_file"])
		
		if (data["user"]==user) {
			div.className = "my_msgs file_mes"
		}else{
			div.className = "other_msgs file_mes"
		}
		div.style.background = "rgba("+rgba[0]+","+rgba[1]+","+rgba[2]+","+color_mes_bg_op + ")"

		p.className="mes"
		p.innerText = data["msg"]

		file.className = "img_file_mes"
		file.src = data["src"]
		file.addEventListener("click", ()=>{file_see(file)})

		time.className = 'time'
		time.innerText = data["time"]

		div.append(file)
		div.append(p)
		div.append(time)
		div_.append(div)
		msg_div.append(div_)
		readeble.innerText = 'not read'
	}
	else if (data['type']=='share'){
		let div_ = document.createElement('div')
		let div = document.createElement('div')
		let file
		
		if (data["type_file"] == "audio"){
			file = document.createElement("img")
			file.className="file_mes"
			file.src = user_music_theme
		}else{
			file = document.createElement(data['type_file'])
			file.className="img_file_mes"
			file.src = data["url_file"]
		}
		
		let a = document.createElement('a')
		let p = document.createElement('p')
		let time = document.createElement('time')
		let readeble = document.querySelector('.readeble')

		if (data["user"]==user) {
			div.className = "my_msgs"
		}else{
			div.className = "other_msgs"
		}
		div.style.background = "rgba("+rgba[0]+","+rgba[1]+","+rgba[2]+","+color_mes_bg_op + ")"

		a.href = data["url_post"]

		time.className = 'time'
		time.innerText = data["time"].slice(11,16)
		p.innerText = "share"

		a.append(file)
		div.append(a)
		div.append(p)
		div.append(time)
		div_.append(div)
		msg_div.append(div_)
		readeble.innerText = 'not read'
	}
	// console.log(data)
}

conn.onopen = ()=>{
	conn.send(JSON.stringify({'type':'first_msg','user': user}))	
}

function btn_send(){
	conn.send(JSON.stringify({'type':'msg','msg': msg_user.value}))
	msg_user.value = ""
	end_readable_send()
}

function new_theme(theme){
	conn.send(JSON.stringify({'type':'new_theme','theme_id':theme}))
}

function delete_theme(e,theme){
	conn.send(JSON.stringify({'type':'delete_theme','th_id':theme,'del_el':e.parentNode.id}))
}
window.addEventListener('scroll',end_readable_send)

jQuery.expr.filters.offscreen = function(el) {
	let rect = el.getBoundingClientRect()
	return ((rect.x + rect.width) < 0 
					|| (rect.y + rect.height) < 0
					|| (rect.x > window.innerWidth || rect.y > window.innerHeight)
			 )
}

function end_readable_send(){
	let readeble = document.querySelector('.readeble')

	if(readeble.innerText=="Read"){return}

	let messages = document.getElementsByClassName("other_msgs")
	end_mes = messages[messages.length-1]
	
	if ($(end_mes).is(':offscreen') && conn.readyState){
		conn.send(JSON.stringify({'type':'end_readable','user': user}))
	}
}

function play_m(music_e){
	music.ontimeupdate = null
	update_time = false
	setInterval(()=>{
		update_time = true
	},1000)
	timeline = document.getElementById("timeline_"+music_e.id)
	music_e.ontimeupdate = ()=>{
		if (update_time){
			const percentagePosition = (100*music_e.currentTime) / music_e.duration
			timeline.style.backgroundSize = `${percentagePosition}% 100%`
			timeline.value = percentagePosition
			update_time = false
		}
	}

	all_pause()
	if (m_play){
		conn.send(JSON.stringify({'type':'play_mus','m_id':music_e.id}))
		style_play_audio(music_e)
	}
	m_play = false

}

function pause_m(music){
	all_pause()
	if (m_pause){
		conn.send(JSON.stringify({'type':'pause_mus'}))
		style_pause_audio(music)
	}
	m_pause = false
}

function seeked_m(music){
	all_pause()
	if (m_time){
		conn.send(JSON.stringify({'type':'seeked','m_id':music.id,'time':music.currentTime}))
		music.play()
	}
	m_time = false
}

function all_pause(){
	let musics = document.getElementsByClassName('music')
	for (i=0;i<musics.length;i++){
		if (musics[i]!=music){
			musics[i].pause()
		}
	}
}

function click_mus(e){
	e.style.display = "none"
	conn.send(JSON.stringify({'type':'get_seeked'}))
}

let sel_f_vis = true

function send_file_mes(){
	if (!sel_f_vis) {
		sel_f_vis = true
		form_mes.style.display="none"
		return
	}
	sel_f_vis = false
	$.ajax({
		url: send_file_mes_ajax,
		data: {},
		success: function (response) {
			form_mes = document.querySelector(".file_mes_form")
			form_mes.innerHTML = response
			form_mes.style.display="block"
		}
	})
}

function send_file_mes_btn(btn){
	file = document.querySelector("#id_file").files[0]
	formdata = new FormData()

	msg = msg_user.value
	if (!msg) {
		msg = "file"
	}
	formdata.append('csrfmiddlewaretoken',document.querySelector(".form_send_file").childNodes[1].value)
	formdata.append("text", msg);
	formdata.append("chat_id", chat_id);
	formdata.append("file", file);

	$.ajax({
		type:"POST",
		url: send_file_mes_ajax,
		data: formdata,
		processData: false,
		contentType: false,
		success: function (response) {
			conn.send(JSON.stringify({'type':'msg_file',
									"src":response["src"],
									"msg":msg,
									"id":response["id"],
									"type_file":response["type_file"],
									"user":user,
									"time":String(new Date()).slice(16,21)
			}))
			msg_user.value = ""
			end_readable_send()
		}
	})
}

function inp_msg_user(inp){
	if (inp.value == "" || inp.value.split(' ').join('')==""){return}
	else if(event.key === 'Enter') {
		btn_send()
	 }
}

function toggleAudio (btn) {
	music = document.getElementById(btn.value)

	if (music.paused) {
		music.play()
	} else {
		music.pause()
	}
}

function changeSeek(timeline) {
	music = document.getElementById(String(timeline.id).slice(9))
	music.ontimeupdate = null
	const time = (timeline.value * music.duration) / 100
	music.currentTime = time

	const percentagePosition = (100*music.currentTime) / music.duration
	timeline.style.backgroundSize = `${percentagePosition}% 100%`
	timeline.value = percentagePosition
}

function style_pause_audio(music){
	music.parentNode.childNodes[2].childNodes[0].childNodes[0].src = pause_img
}

function style_play_audio(music){
	music.parentNode.childNodes[2].childNodes[0].childNodes[0].src = play_img
}

