let msg_user = document.querySelector("#msg_user")
let msg_div = document.querySelector('.messages')
let reply = document.querySelector('.reply')
let emojis_select = document.querySelector('.emojis_select')
let	circles = document.getElementsByClassName("circle")
const timeout = 700;
let idTimeout;

function connect() {
	conn = new WebSocket("ws://"+window.location.hostname+":"+location.port+"/ws/chat/"+chat)
	conn.onmessage = onmessage

	conn.onclose = (e)=>{
	  setTimeout(()=>{
	    connect()
	  }, 100)
	}

	conn.onopen = ()=>{
		conn.send(JSON.stringify({'type':'first_msg',"chat":chat_id}))	
		end_readable_send()
	}
}
connect()
conn_u_f = new WebSocket("ws://"+window.location.hostname+":"+location.port+"/ws/user/"+friend)

function onmessage(e){
	let data = JSON.parse(e.data)
	let readeble = document.querySelector('.readeble')

	if (data['type']=='msg'){
		conn_u_f.send(JSON.stringify({'type':'msg','msg':data["msg"],'from_user': user, "from_chat":chat}))
		
		let div_ = document.createElement('div')
		div_.onclick = () => {emoji(div_,data["id_msg"])}
		div_.ontouchstart= () =>{reply_check(div_)}
		div_.onmousedown= () =>{reply_check(div_)}
		div_.id = data['id_msg']
		let div = document.createElement('div')
		let p = document.createElement('p')
		let time = document.createElement('time')

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
		if (data['readeble'] == 'True'){
			readeble.innerText = 'Read'
		}else{
			readeble.innerText = 'not read'
		}
	}else if(data['type']=='msg_file'){
		conn_u_f.send(JSON.stringify({'type':'msg','msg':data["msg"],'from_user': user, "from_chat":chat}))
		let className
		if (data["user"]==user) {
			className = "my_msgs"
		}else{
			className = "other_msgs"
		}

		if (data["type_file"] == "audio"){
			element = `
				<div id="`+data["id"]+`" ontouchstart="reply_check(this)" onmousedown="reply_check(this)" onclick="emoji(this,'`+data["id"]+`')">
					<div class="`+className+`" style="background: rgba(` + rgba[0] + `,` + rgba[1] + `,`+ rgba[2] +`,`+ color_mes_bg_op + `);">
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
		div_.id = data['id']
		div_.onclick = () => {emoji(div_,data["id"])}
		div_.ontouchstart= () =>{reply_check(div_)}
		div_.onmousedown= () =>{reply_check(div_)}
		let div = document.createElement('div')
		let p = document.createElement('p')
		let time = document.createElement('time')
		let file = document.createElement(data["type_file"])
		
		if (data["user"]==user) {
			div.className = "my_msgs my_file_mes"
			file.className = "my_file_mes"
		}else{
			div.className = "other_msgs other_file_mes"
			file.className = "other_file_mes"
		}
		div.style.background = "rgba("+rgba[0]+","+rgba[1]+","+rgba[2]+","+color_mes_bg_op + ")"

		p.className="mes"
		p.innerText = data["msg"]

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
		div_.onclick = () => {emoji(div_,data["id_msg"])}
		div_.ontouchstart= () =>{reply_check(div_)}
		div_.onmousedown= () =>{reply_check(div_)}
		div_.id = data['id_msg']
		let div = document.createElement('div')
		let file
		
		if (data["type_file"] == "audio"){
			file = document.createElement("img")
			file.className="other_msgs"
			file.src = user_music_theme
		}else{
			file = document.createElement(data['type_file'])
			file.className="other_file_mes"
			file.src = data["url_file"]
		}
		
		let a = document.createElement('a')
		let p = document.createElement('p')
		let time = document.createElement('time')

		if (data["user"]==user) {
			div.className = "my_msgs my_file_mes"
		}else{
			div.className = "other_msgs other_file_mes"
		}
		div.style.background = "rgba("+rgba[0]+","+rgba[1]+","+rgba[2]+","+color_mes_bg_op + ")"

		a.href = data["url_post"]

		time.className = 'time'
		time.innerText = data["time"].slice(11,16)
		p.innerText = data["msg"].split("#@;")[1]

		a.append(file)
		div.append(a)
		div.append(p)
		div.append(time)
		div_.append(div)
		msg_div.append(div_)
		readeble.innerText = 'not read'
		end_readable_send()

	}else if (data['type']=='emogi_msg'){
		let msg_emoji = document.getElementById(data['msg_id'])

		if (msg_emoji.nextElementSibling){
			let emojis = get_node_chield(msg_emoji.nextElementSibling.childNodes)
			for (var i = emojis.length - 1; i >= 0; i--) {
				if(emojis[i].id == "emoji_" + data['user']){
					emojis[i].innerHTML = data['emoji']
					return
				}
			}
			let span = document.createElement("span")
			span.innerHTML = data['emoji']
			span.className = "emoji_msg"
			span.id = "emoji_"+data['user']
			msg_emoji.nextElementSibling.append(span)
		}else{
			let div = document.createElement('div')
			let span = document.createElement("span")

			classname_msg = get_node_chield(msg_emoji.childNodes)[0].className.split(" ")
			if (classname_msg.includes("my_msgs")){
				div.className = "emoji_my"
			}else if(classname_msg.includes("other_msgs")){
				div.className = "emoji_other"
			}
			span.innerHTML = data['emoji']
			span.className = "emoji_msg"
			span.id = "emoji_"+data['user']
			div.append(span)
			msg_emoji.after(div)
		}
	}else if (data['type']=='reply_msg'){
		conn_u_f.send(JSON.stringify({'type':'msg','msg':data["msg"],'from_user': user, "from_chat":chat}))
		
		let div_reply = document.createElement('div')
		let div_parent = document.createElement('div')
		let div_vertical = document.createElement('div')
		let p_parent = document.createElement('p')

		div_parent.style.background = "rgba("+rgba[0]+","+rgba[1]+","+rgba[2]+","+color_mes_bg_op + ")"

		p_parent.className = 'mes'
		p_parent.innerText = data['msg_parent']

		div_reply.append(div_parent)
		div_parent.append(div_vertical)
		div_parent.append(p_parent)
		msg_div.append(div_reply)

		let div_ = document.createElement('div')
		div_.onclick = () => {emoji(div_,data["id_msg"])}
		div_.ontouchstart= () =>{reply_check(div_)}
		div_.onmousedown= () =>{reply_check(div_)}
		div_.id = data['id_msg']
		let div = document.createElement('div')
		let p = document.createElement('p')
		let time = document.createElement('time')

		if (data["user"]==user) {
			div_parent.className = "my_msgs parent_my_msg"
			div_vertical.className = 'my_vertical_line'
			div.className = "my_msgs"
		}else{
			div_parent.className = "other_msgs parent_other_msg"
			div_vertical.className = 'other_vertical_line'
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
	}
}

function reply_close(e=reply_div){
  send_msg_func = btn_send

	reply.style.display = "none"
	e.style.margin = "0" 
  e.style.opacity = "1" 

  let classname_msg = get_node_chield(e.childNodes)[0].className.split(" ")

	if (classname_msg.includes("my_msgs")){
		get_node_chield(e.childNodes)[0].style.borderRadius = "10px 0 0 10px" 
	}else if(classname_msg.includes("other_msgs")){
  	get_node_chield(e.childNodes)[0].style.borderRadius = "0 10px 10px 0" 
	}
  
}

function reply_send(e){
	reply_close(e)
	conn.send(JSON.stringify({'type':'reply_msg','msg_id': e.id,'msg':msg_user.value}))
	msg_user.value = ""
}

function reply_style(e){
  send_msg_func = () => {reply_send(e)}
	reply.style.display = "block"
  e.style.margin = "1%" 
  e.style.opacity = "0.5" 
  get_node_chield(e.childNodes)[0].style.borderRadius = "10px" 
	reply_div = e
}

let reply_div

function reply_check(e){
  let idTimeout = setTimeout(()=>{reply_style(e)},timeout)

	e.addEventListener('mouseup', function() {
	  clearTimeout(idTimeout)
	})

	e.addEventListener('touchend', function() {
	  clearTimeout(idTimeout)
	})
}

function get_node_chield(chields){
	let res = []
	for (let i = chields.length - 1; i >= 0; i--) {
		if(chields[i].nodeType == chields[i].ELEMENT_NODE){
			res.push(chields[i])
		}
	}
	return res
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

let send_msg_func = btn_send

function inp_msg_user(inp){
	if (inp.value == "" || inp.value.split(' ').join('')==""){return}
	else if(event.key === 'Enter') {
		send_msg_func()
	 }
}

let open_emoji = false
let msg_emoji
function emoji(e,id){
	if (open_emoji) {
		close_emoji()
		open_emoji = false
		return
	}else{
		open_emoji = true
	}
	msg_emoji = [e,id]
	emojis_select.style.display="block"
}
function close_emoji(){
	emojis_select.style.display="none"
}

function emoji_p_select(e){
	conn.send(JSON.stringify({'type':'emogi_msg','msg_id':msg_emoji[1],'emoji':e.target.innerHTML}))
	close_emoji()
}

let emojis = document.getElementById('emojis')
let newEl;
let emojRange = [
  [128513, 128591], [9986, 10160], [128640, 128704]
];

for (let i = 0; i < emojRange.length; i++) {
  let range = emojRange[i];
  let newdiv = document.createElement("div")
  newdiv.className = "emoji_tab"
  newdiv.id = "emoji_tab_"+i
  for (let x = range[0]; x < range[1]; x++) {
    newEl = document.createElement('p')
  	newEl.className = "emoji_p"
    newEl.innerHTML = "&#" + x + ";"
    newEl.addEventListener("click", emoji_p_select)
    newdiv.appendChild(newEl)
  }
  emojis.appendChild(newdiv)
}
btns_emoji_tab = document.getElementsByClassName("emogi_tab_btn")
document.getElementById("emoji_tab_0").style.display = 'grid'
btns_emoji_tab[0].style.borderBottom = "1px solid white"

function select_emoji_tab(btn,id){
	all_btn_black()
	btn.style.borderBottom = "1px solid white"
	emojis_tabs = emojis.childNodes
	for (var i = emojis_tabs.length - 1; i >= 0; i--) {
		emojis_tabs[i].style.display = "none"
	}
	document.getElementById(id).style.display = 'grid'
}

function all_btn_black(){
	for (let i = btns_emoji_tab.length - 1; i >= 0; i--) {
		btns_emoji_tab[i].style.borderBottom = "1px solid black"
	}
}

function voice_style(){
	for (var i = circles.length - 1; i >= 0; i--) {
		rand = Math.random() * 2
		circles[i].style.transform = "scale("+rand+","+rand+")"
	}
	setTimeout(()=>{
		if (!stop_voice_anim) {
			voice_style()
		}else{
			for (var i = circles.length - 1; i >= 0; i--) {
				circles[i].style.display = "none"
			}
			return
		}
	},300)
}

let stop_voice_anim = false

function send_voice_mes(e) {
	stop_voice_anim = false
	setTimeout(()=>{
		for (var i = circles.length - 1; i >= 0; i--) {
			circles[i].style.display = "block"
		}
		voice_style()
	},0)

	navigator.mediaDevices.getUserMedia({ audio: true})
    .then(stream => {
        const mediaRecorder = new MediaRecorder(stream);
        let voice = []
        mediaRecorder.start()

        mediaRecorder.addEventListener("dataavailable",function(event) {
            voice.push(event.data)
        })

        e.addEventListener('mouseup', function(){
						stop_voice_anim = true
						if(mediaRecorder.state!="inactive"){
            	mediaRecorder.stop()
						}
        })
        e.addEventListener('touchend', function(){
						stop_voice_anim = true
						if(mediaRecorder.state!="inactive"){
            	mediaRecorder.stop()
						}
        })

				mediaRecorder.addEventListener("stop", () => {
				  const voiceBlob = new Blob(voice, {type: 'audio/mp3'})

					const voice_file = new File(
					    [voiceBlob],
					    "voice.mp3",
					    { type: 'audio/mp3' }
					)

				  let fd = new FormData()
				  
					msg = msg_user.value
					if (!msg) {
						msg = "file"
					}

					fd.append('file', voice_file)
					fd.append("chat_id", chat_id)
					fd.append("text", msg);
					fd.append('csrfmiddlewaretoken',document.querySelector("#csrf_voice").childNodes[1].value)

					$.ajax({
						type:"POST",
						url: send_voice_mes_ajax,
						data: fd,
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
				})
    })
}