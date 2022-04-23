let msg_user = document.querySelector("#msg_user")
let msg_div = document.querySelector('.messages')
let musics = document.querySelector('.musics')
let music

conn = new WebSocket("ws://"+window.location.hostname+"/chat/"+chat)
conn.onmessage = onmessage

conn_u_f = new WebSocket("ws://"+window.location.hostname+"/user/"+friend)

m_pause = true
m_time = true

function onmessage(e){
	let data = JSON.parse(e.data)

 	if (data['type']=='msg'){
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
		end_readable_send()
		scrollToEndPage()
		
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
	}else if(data['type']=='msg_file'){
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
		end_readable_send()
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
		end_readable_send()
	}
	console.log(data)
}

conn.onopen = ()=>{
	conn.send(JSON.stringify({'type':'first_msg',"chat":chat_id}))	
	end_readable_send()
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

function Visible(target) {
  let targetPosition = {
      top: window.pageYOffset + target.getBoundingClientRect().top,
      left: window.pageXOffset + target.getBoundingClientRect().left,
      right: window.pageXOffset + target.getBoundingClientRect().right,
      bottom: window.pageYOffset + target.getBoundingClientRect().bottom
    },
    windowPosition = {
      top: window.pageYOffset,
      left: window.pageXOffset,
      right: window.pageXOffset + document.documentElement.clientWidth,
      bottom: window.pageYOffset + document.documentElement.clientHeight
    }

  if (targetPosition.bottom > windowPosition.top &&
    targetPosition.top < windowPosition.bottom &&
    targetPosition.right > windowPosition.left &&
    targetPosition.left < windowPosition.right) {
    return true
  } else {
    return false
  }
}

function end_readable_send(){
	let readeble = document.querySelector('.readeble')

	if(readeble.innerText=="Read"){return}

	let messages = document.getElementsByClassName("other_msgs")
	end_mes = messages[messages.length-1]
	
	if (end_mes){
		if (Visible(end_mes) && conn.readyState){
			conn.send(JSON.stringify({'type':'end_readable','user': user}))
		}
	}
}

function close_popups(){
	document.querySelector(".click_mus").style.display = "none"
	document.querySelector(".click_not_mus").style.display = "none"
}

function click_mus(){
	close_popups()
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

			let send_file = document.querySelector("#id_file")
			send_file.addEventListener("change",()=>{
				path = send_file.value.split("\\")
				document.querySelector(".id_file").innerText = path[path.length -1]
			})
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