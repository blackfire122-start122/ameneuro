let msg_user = document.querySelector("#msg_user")
let msg_div = document.querySelector('.messages')

// conn = new WebSocket("ws://127.0.0.1:8000/"+"test")
conn = new WebSocket("ws://192.168.0.105/"+"test")
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
	p.innerText = data["msg"]
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
