function want_add_friend(btn) {
	$.ajax({
		type: $(this).attr('post'),
		url: want_add_friend_ajax,
		data: {'id':btn.value},
		success: function (response) {
            console.log(response.data_text)
        }
	})
}
