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

	div_sel_th = document.getElementById(select_theme_now)

	if(div_sel_th){
		if (div_sel_th.className == "th", div_sel_th.className == "th_user"){
			let btn = document.createElement("button")
			btn.className = "end_element"
			btn.innerText = "Delete"
			btn.type = "button"
			btn.onclick = ()=>{delete_theme(btn)}
			div_sel_th.append(btn)
		}
	}

	if (div_sel_th.className == "th_user") {
		div_sel_th.className = "th"
	}else if (div_sel_th.className == "th"){
		div_sel_th.className = "th_user"
	}else if (div_sel_th.className == "def_th_user"){
		div_sel_th.className = "def_th"
	}else if (div_sel_th.className == "def_th"){
		div_sel_th.className = "def_th_user"
	}

	parent_node = e.parentNode

	if (parent_node.className == "th_user") {
		parent_node.className = "th"
	}else if (parent_node.className == "th"){
		parent_node.className = "th_user"
	}else if (parent_node.className == "def_th"){
		parent_node.className = "def_th_user"
	}else if (parent_node.className == "def_th_user"){
		parent_node.className = "def_th"
	}

	if (parent_node.querySelector("button")) {
		parent_node.querySelector("button").remove()
	}
	select_theme_now = id
}

function delete_theme(e){
	conn_u.send(JSON.stringify({'type':'delete_theme_all', "id":e.parentNode.id}))
	e.parentNode.remove()
}


function select_file_name(file){
	path = file.value.split("\\")
	file.parentNode.childNodes[3].innerText = path[path.length -1]

	file_inp = file.files[0]
	file_file = file.nextSibling.nextSibling.nextSibling.nextSibling
	file_file.src = window.URL.createObjectURL(file_inp)
}