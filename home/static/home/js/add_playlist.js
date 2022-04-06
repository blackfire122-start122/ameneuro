function img_set(e){
	file = e.files[0]

	img = document.querySelector(".img_input")
	img.src = window.URL.createObjectURL(file)
}