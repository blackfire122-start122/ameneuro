let msg_user = document.querySelector("#msg_user")
let msg_div = document.querySelector('.messages')
let musics = document.querySelector('.musics')
let music

// conn = new WebSocket("ws://127.0.0.1:8000/"+"test")
conn = new WebSocket("ws://"+window.location.hostname+"/"+"test")
conn.onmessage = onmessage

m_play = true
m_pause = true
m_time = true

function onmessage(e){
	let data = JSON.parse(e.data)
	if (data['type']=='first_msg'){
		for (i=0;i<data['musics_url'].length;i++){
			audio = document.createElement('audio')

			audio.src = data['musics_url'][i][0]
			audio.controls = true
			audio.className = 'music'
			audio.id = data['musics_url'][i][1]

			audio.addEventListener('play',play_m)
			audio.addEventListener('pause',pause_m)
			audio.addEventListener('seeked',seeked_m)

			musics.append(audio)
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
		time.innerText = data["time"]

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
		music = document.getElementById(data['m_id'])
		music.play()
		setTimeout(()=>{m_play = true},300)
	}else if(data['type']=='pause_mus'){
		music.pause()
		setTimeout(()=>{m_pause = true},300)
	}else if(data['type']=='seeked'){
		music.currentTime = data['time']
		setTimeout(()=>{
			m_time = true
			music.play()
		},300)
	}else if(data['type']=='get_seeked'){
	  conn.send(JSON.stringify({'type':'set_seeked','time':music.currentTime, 'm_id':music.id}))
	}
	else if(data['type']=='set_seeked'){
		music = document.getElementById(data['m_id'])
		music.currentTime = data["time"]
		setTimeout(()=>{
			m_time = true
			music.play()
		},300)
	}
}

conn.onopen = ()=>{
	conn.send(JSON.stringify({'type':'first_msg','user': user,'chat':chat}))
}


function btn_send(btn){
	conn.send(JSON.stringify({'type':'msg','msg': msg_user.value}))
	msg_div
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

function play_m(e){
	music = e.srcElement
	all_pause(music)
	if (m_play){
	  conn.send(JSON.stringify({'type':'play_mus','m_id':music.id}))
  }
  m_play = false
}

function pause_m(e){
	music = e.srcElement
	all_pause()
	if (m_pause){
	  conn.send(JSON.stringify({'type':'pause_mus'}))
	}
	m_pause = false
}

function seeked_m(e){
	music = e.srcElement
	all_pause()
	if (m_time){
  	conn.send(JSON.stringify({'type':'seeked','time':music.currentTime}))
		music.play()
	}
	m_time = false
}

function all_pause(music){
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