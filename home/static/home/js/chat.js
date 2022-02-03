let msg_user = document.querySelector("#msg_user")
let msg_div = document.querySelector('.messages')
let musics = document.querySelector('.musics')
let music

conn = new WebSocket("ws://"+window.location.hostname+"/"+"test")
conn.onmessage = onmessage

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
		let div = document.createElement('div')
		let p = document.createElement('p')
		let time = document.createElement('time')
		let readeble = document.querySelector('.readeble')

		if (data["user"]==user) {
			div.className = "my_msgs"
		}else{
			div.className = "other_msgs"
		}
		p.className="mes"
		p.innerText = data["msg"]

		time.className = 'time'
		time.innerText = data["time"].slice(11,16)

		div.append(p)
		div.append(time)
		msg_div.append(div)
		readeble.innerText = 'not read'

	}else if(data['type']=='new_theme'){
		let div = document.createElement('div')
		let p = document.createElement('p')

		div.className = "new_theme"
		p.innerText = data['msg_new_theme']

		div.append(p)
		msg_div.append(div)

	}else if(data['type']=='delete_theme'){
		let error = document.querySelector('#error')
		error.innerText = data["error"]
		error.style.display='block'

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
		let div = document.createElement('div')
		let p = document.createElement('p')
		let img = document.createElement('img')
		let time = document.createElement('time')
		let readeble = document.querySelector('.readeble')

		if (data["user"]==user) {
			div.className = "my_msgs"
		}else{
			div.className = "other_msgs"
		}
		p.className="mes"
		p.innerText = data["msg"]

		img.className = "img_file_mes"
		img.src = data["src"]

		time.className = 'time'
		time.innerText = data["time"]

		div.append(img)
		div.append(p)
		div.append(time)
		msg_div.append(div)
		readeble.innerText = 'not read'
	}
	console.log(data)
}

conn.onopen = ()=>{
	conn.send(JSON.stringify({'type':'first_msg','user': user,'chat':chat}))
}

function btn_send(){
	conn.send(JSON.stringify({'type':'msg','msg': msg_user.value}))
	msg_user.value = ""
	end_readable_send()
}

let chat_options_change = false

function componentToHex(c) {
	var hex = c.toString(16);
	return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
	return "#" + componentToHex(parseInt(r)) + componentToHex(parseInt(g)) + componentToHex(parseInt(b));
}

function chat_options(e) {
	let messages = document.querySelector(".messages")
	let input_mes_send = document.querySelector(".input_mes_send")
	let options_div = document.querySelector(".options")
	let error = document.querySelector('#error')


	if (chat_options_change) {
		messages.style.display='block'
		input_mes_send.style.display='block'
		chat_options_change = false
		options_div.style.display = "none"
		options_div.innerHTML = ''
		error.style.display='none'
		return
	}else{
		messages.style.display='none'
		input_mes_send.style.display='none'
		options_div.style.display = "block"
		error.style.display='block'
	}

	$.ajax({
		url: chat_options_ajax,
		data: {'chat_id':chat_id},
		success: function (response) {
						options_div.innerHTML = response
						bg_inp_val = bg_inp_val.split(",")
						document.querySelector('#bg_op').value = bg_inp_val[3]
						document.querySelector('#mes_bg').style.opacity = bg_inp_val[3]
						document.querySelector('#mes_bg').value = rgbToHex(bg_inp_val[0],bg_inp_val[1],bg_inp_val[2])
				}
	})
	chat_options_change = true

}

function inp_ran(e){
	document.querySelector('#mes_bg').style.opacity = e.value
}

function new_theme(theme){
	conn.send(JSON.stringify({'type':'new_theme','theme_id':theme}))
}

function delete_theme(theme){
	conn.send(JSON.stringify({'type':'delete_theme','theme_id':theme}))
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

window.addEventListener('scroll',()=>{
	if(window.scrollY!=0){return}
	
	$.ajax({
		url: chat_get_mess_ajax,
		data: {'chat_id':chat_id},
		success: function (response) {
			msgs = msg_div.innerHTML 
			msg_div.innerHTML = response+msgs
			// window.scrollTo(0,1)
		}
	})
})

let height = 20
let attempt = 5

function scrollToEndPage() {
	if (height < document.body.scrollHeight){
			window.scrollTo(0, height)
			attempt++
			height = parseInt(height) + attempt
	}else{
			clearInterval(intS);
	}
}
let intS = setInterval(scrollToEndPage,10)

musics_s = true
function music_show(){
	let musics = document.querySelector('.musics')
	if (musics_s){
		musics.style.display = 'block'
	}else{
		musics.style.display = 'none'
	}
	musics_s = !musics_s
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