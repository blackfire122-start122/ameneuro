function set_name_music(e) {
	document.querySelector(".label_file_inp").querySelector("h3").innerText = e.files[0].name.slice(0,40)
}