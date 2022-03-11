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
	conn_u.send(JSON.stringify({'type':'new_theme_all', "id":id}))
}

function delete_theme(e,id){
	conn_u.send(JSON.stringify({'type':'delete_theme_all', "id":id}))
	e.parentNode.remove()
}


function select_file_name(file){
	path = file.value.split("\\")
	file.parentNode.childNodes[3].innerText = path[path.length -1]
}