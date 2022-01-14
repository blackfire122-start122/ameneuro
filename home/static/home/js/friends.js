function add_chat(btn) {
	$.ajax({
		type: $(this).attr('post'),
		url: add_chat_ajax,
		data: {'id':btn.value},
		success: function (response) {
            console.log(response.data_text)
        }
	})
}

function add_friend(btn) {
	$.ajax({
		type: $(this).attr('post'),
		url: add_friend_ajax,
		data: {'id':btn.value},
		success: function (response) {
            console.log(response.data_text)
        }
	})
}