function change_btn(e){
	if (!e.value) {
		e.parentNode.childNodes[3].style.display = "flex"
		e.style.height = "50px"
		e.style.borderRadius = "20px 20px 0 0"
		e.style.background = "#1c1f3a"
		e.value = true


	}else{
		e.parentNode.childNodes[3].style.display = "none"
		e.value = false
		e.style.borderRadius = "20px"
		e.style.background = "#15172b"
		e.style.height = "30px"
	}
}

function select_theme(e,id){
	$.ajax({
		url: new_theme_all_ajax,
		data: {'id':id},
		error: function (response) {
			console.log(response.data_text)
		}
	})
}

function delete_theme(e,id){
	$.ajax({
		url: delete_theme_all_ajax,
		data: {'id':id},
		error: function (response) {
			console.log(response.data_text)
		}
	})
	e.parentNode.remove()
}

