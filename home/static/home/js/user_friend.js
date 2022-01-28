function want_add_friend(btn) {
	$.ajax({
		type: $(this).attr('post'),
		url: want_add_friend_ajax,
		data: {'id':btn.value},
	})
	btn.disabled = true
	btn.style.display = "none"
	document.getElementById(btn.value).style.display = "none"
}

function follow(btn) {
	$.ajax({
		type: $(this).attr('post'),
		url: follow_ajax,
		data: {'id':btn.value},
	})
	btn.disabled = true
	btn.style.color = "gray"
	btn.style.fontSize = "1em"
	btn.innerText = "follow"
}
