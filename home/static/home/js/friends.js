function add_chat(btn) {
	$.ajax({
		type: $(this).attr('post'),
		url: add_chat_ajax,
		data: {'id':btn.value},
		error: function (response) {
            console.log(response.data_text)
        },
        success: function(response){
        	console.log(response)
        	window.location.href = response["url"]
        }
	})
	btn.disabled=true
	btn.style.display = "none"
	document.getElementById(btn.value).style.display = "none"
}

function add_friend(btn) {
	$.ajax({
		type: $(this).attr('post'),
		url: add_friend_ajax,
		data: {'id':btn.value},
		error: function (response) {
            console.log(response.data_text)
        }
	})
}