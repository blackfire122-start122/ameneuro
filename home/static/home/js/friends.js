function add_chat(btn) {
	conn_u.send(JSON.stringify({'type':'add_chat', "id":btn.value}))

	btn.disabled=true
	btn.style.display = "none"
	document.getElementById(btn.value).style.display = "none"
}

function add_friend(btn) {
	conn_u.send(JSON.stringify({'type':'add_friend', "id":btn.value}))
}