let msg_user = document.querySelector("#msg_user")
let msg_div = document.querySelector('.messages')

// conn = new WebSocket("ws://127.0.0.1:8000/"+"test")
conn = new WebSocket("ws://"+window.location.hostname+"/"+"test")
conn.onmessage = onmessage

function onmessage(e){
	let data = JSON.parse(e.data)

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

	console.log(data)
}

conn.onopen = ()=>{
	conn.send(JSON.stringify({'user': user,'chat':chat}))
}


function btn_send(btn){
	conn.send(JSON.stringify({'msg': msg_user.value}))
	msg_div
	msg_user.value = ""
}


let chat_options_change = false

function chat_options(e,chat_id) {
	let messages = document.querySelector(".messages")
	let input_mes_send = document.querySelector(".input_mes_send")
	let options_div = document.querySelector(".options")

	if (chat_options_change) {
		messages.style.display='block'
		input_mes_send.style.display='block'
		document.querySelector("body").style.color = "white"
		chat_options_change = false
		options_div.style.display = "none"
		options_div.innerHTML = ''
		return
	}else{
		messages.style.display='none'
		input_mes_send.style.display='none'	
		options_div.style.display = "block"
		document.querySelector("body").style.color = "black"
	}

	$.ajax({
		url: chat_options_ajax,
		data: {'chat_id':chat_id},
		success: function (response) {
            options_div.innerHTML = response
        }
	})
	chat_options_change = true
}