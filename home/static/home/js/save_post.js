let posts_save = document.querySelector(".posts_save")

$.ajax({
	type: $(this).attr('post'),
	url: saves_posts_ajax,
	data: {},
	error: function (response) {
		console.log(response)
    },
    success: function(response){
    	posts_save.innerHTML += response
    }
})

