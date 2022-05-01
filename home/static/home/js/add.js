let add_post = document.querySelector(".add_post")
let add_video = document.querySelector(".add_video")

function all_border_black(){
	btns = document.getElementsByClassName('btn_add')
	for(let i=btns.length-1;i>=0; i--){
			btns[i].style.borderBottom = "3px solid black";
	}
}

function what_add(e,what_add) {
	if (what_add == "post") {
		add_post.style.display = "block"
		add_post.style.display = "block"
		add_video.style.display = "none"
	}else if(what_add == "video"){
		add_video.style.display = "block"
		add_post.style.display = "none"
	}
	all_border_black()
	e.style.borderBottom = "3px solid white"
}

function inp_file_change(e){
	file = e.files[0]
	file_types = {"audio/mpeg":"img","video/mp4":"video","image/jpeg":"img","image/png":"img"}
	
	file_file = document.getElementById("file_post_file")
	parent_file = file_file.parentNode
	file_file.remove()
	file_file = document.createElement(file_types[file.type])
	file_file.id = "file_post_file"
	file_file.alt = "file"
	if (file.type=="audio/mpeg"){
		file_file.src = img_mus
	}else{
		file_file.src = window.URL.createObjectURL(file)
	}
	parent_file.append(file_file)
}

function file_set(e,id){
	file = e.files[0]
	file_file = document.getElementById(id)
	file_file.src = window.URL.createObjectURL(file)
}