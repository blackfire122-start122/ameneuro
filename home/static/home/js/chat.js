let msg_user = document.querySelector("#msg_user")
let msg_div = document.querySelector('.messages')

// conn = new WebSocket("ws://127.0.0.1:8000/"+"test")
conn = new WebSocket("ws://"+window.location.hostname+"/"+"test")
conn.onmessage = onmessage

function onmessage(e){
	let data = JSON.parse(e.data)

	if (data['type']=='msg'){
		let div = document.createElement('div')
		let p = document.createElement('p')
		let time = document.createElement('time')

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

	}else if(data['type']=='new_theme'){
		let div = document.createElement('div')
		let p = document.createElement('p')

		div.className = "new_theme"
		p.innerText = data['msg_new_theme']

		div.append(p)
		msg_div.append(div)

	}
	console.log(data)
}

conn.onopen = ()=>{
	conn.send(JSON.stringify({'type':'first_msg','user': user,'chat':chat}))
}


function btn_send(btn){
	conn.send(JSON.stringify({'type':'msg','msg': msg_user.value}))
	msg_div
	msg_user.value = ""
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

chat_options(null,chat_id)

function inp_ran(e){
	document.querySelector('#mes_bg').style.opacity = e.value
}

function new_theme(theme){
	conn.send(JSON.stringify({'type':'new_theme','theme_id':theme}))
}