function like(e){
	$.ajax({
		url: like_ajax,
		data: {'id':e.id},
		error: function (response) {
			console.log(response.data_text)
		}
	})
	e.style.opacity = "0.5"
	e.onclick = null
	e.parentNode.childNodes[3].innerText = parseInt(e.parentNode.childNodes[3].innerText)+1
}

function comments(e){
	let div_menu_post = document.querySelector(".post_"+e.id)
	
	function show_comment(){
		div_menu_post.childNodes[11].style.display = "block"
		e.onclick = close_comment
	}

	function close_comment(){
		div_menu_post.childNodes[11].style.display = "none"
		e.onclick = show_comment
	}

	e.onclick = close_comment 

	$.ajax({
		url: comment_ajax,
		data: {'id':e.id},
		success: function (response) {
			div_menu_post.childNodes[11].innerHTML += response
			div_menu_post.childNodes[11].style.display = "block"
		}
	})

}

function like_comment(e){
	$.ajax({
		url: comment_like_ajax,
		data: {'id':e.id},
		error: function (response) {
			console.log(response.data_text)
		}
	})

	e.style.opacity = "0.5"
	e.onclick = null
	e.parentNode.childNodes[3].innerText = parseInt(e.parentNode.childNodes[3].innerText)+1
}

let reply = false
let btn_reply

function comment_user(e){
	let inp_comment = document.querySelector('.inp_comment'+e.value)

	if (reply){
		$.ajax({
			url: comment_reply_ajax,
			data: {'com_id':btn_reply.id,
					'post_id':btn_reply.value,
					'text':inp_comment.value},
			error: function (response) {
				console.log(response)
			}
		})

	}else{
		$.ajax({
			url: comment_user_ajax,
			data: {'id':e.value,
					'text':inp_comment.value},
			error: function (response) {
				console.log(response)
			}
		})
	}
	reply = false
	inp_comment.value = ""
}

function select_reply(e){
	let com = document.querySelector('.com_'+e.id)
	com.style.background = "rgba(0,0,0,0.1)"
	reply = true
	if(btn_reply){
			document.querySelector('.com_'+btn_reply.id).style.background = "none"
	}
	btn_reply = e
}

function options(e){
	let opt_menu = document.querySelector('#opt_'+e.id)
	if (e.value) {
		opt_menu.style.display = "none"
		e.value = false
		return
	}

	if (!e.value) {
		e.value = true
	}
	opt_menu.style.display = "flex"
}

function copy_link(e){
	e.innerText = "http://"+window.location.hostname+e.value

  	let range = document.createRange()
  	range.selectNode(e)
  	window.getSelection().addRange(range)

	document.execCommand('copy')
	e.innerText="Скопіювати"
}

let video

function get_posts(){
	let posts_div = document.querySelector('.posts')

	$.ajax({
		url: post_ajax,
		data: {'id':id_post},
		error: (data)=> {
			console.log(data.data_text)
		},
		success: (data) =>{
			if (data["info"] != "None post"){
				posts_div.innerHTML += data
				video = document.getElementsByClassName("video_post")
			}
		}
	})
}

get_posts()

function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}

if (!id_post){
	window.addEventListener('scroll', function(e) {
		if($(window).scrollTop()+$(window).height()>=$(document).height()-500){
		    get_posts()
		    sleep(700)
		}
	})
}

window.addEventListener('scroll', function(e){
	for (let i = 0;i<video.length;i++){
		if (!($(video[i]).position().top > $(window).scrollTop())){
			video[i].pause()
		}
	}
})

let id_share

function share(id){
	id_share = id
	document.querySelector(".friends_share").style.display = "block"
}

function close_sh(){
	document.querySelector(".friends_share").style.display="none"
}
function share_btn(ch_id){
	conn = new WebSocket("ws://"+window.location.hostname+"/"+ch_id)
	conn.onopen = ()=>{
		conn.send(JSON.stringify({'type':'share','user': user,'id_share':id_share,'msg':"http://"+window.location.hostname+"/post/"+id_share}))
	}
}

function delete_post(id_post){
	$.ajax({
		url: delete_post_ajax,
		data: {'id':id_post},
		error: (data)=> {
			console.log(data.data_text)
		},
	})
}

let menu_show_v = true

function menu_show(e){
	if (menu_show_v) {
		document.querySelector(".menu_home").style.display = "flex"
		menu_show_v = false
	}else{
		document.querySelector(".menu_home").style.display = "none"
		menu_show_v = true
	}
}