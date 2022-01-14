function like(btn){
	console.log(btn.id)
	$.ajax({
		url: like_ajax,
		data: {'id':btn.id},
		success: function (response) {
            console.log(response.data_text)
        }
	})
}

