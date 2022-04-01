function send_img_recognize(e){
	file = document.querySelector("#id_img").files[0]
	formdata = new FormData()

	img = document.getElementById("img_recognize")
	img.src = window.URL.createObjectURL(file)

	formdata.append('csrfmiddlewaretoken',document.querySelector(".form_send_recognize").childNodes[1].value)
	formdata.append("img", file);

	$.ajax({
		type:"POST",
		url: form_recognize_ajax,
		data: formdata,
		processData: false,
		contentType: false,
		success: function (response) {
			e.innerText = response["data"]
		}
	})
}

function img_set(e){
	file = e.files[0]

	img = document.getElementById("img_recognize")
	img.src = window.URL.createObjectURL(file)
}