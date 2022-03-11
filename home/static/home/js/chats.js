user_ch = document.getElementsByClassName("user_ch")

for (var i = user_ch.length - 1; i >= 0; i--) {
	let user_in = user_ch[i].innerText
	conn_u_f = new WebSocket("ws://"+window.location.hostname+"/user/"+user_in)
	conn_u_f.onopen = (e)=>{
		e.target.send(JSON.stringify({'type':'in_net',"user_in":user_in}))	
	}
	conn_u_f.onmessage = onmessage_u
}

