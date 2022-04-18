let comments_div = document.querySelector(".comments")

let start_comments = 0
let end_comments = how_get

function comments(e){
	if (e.style.opacity == "0.5"){
		comments_div.style.display='none'
		e.style.opacity = "1"
		document.querySelector(".inp_sub_com").style.display = "none"
		return
	}
	get_comments()
	e.style.opacity = "0.5"
	document.querySelector(".inp_sub_com").style.display = "flex"

}

function get_comments(){
	$.ajax({
		url: comment_video_ajax,
		data: {'type':'video','id':id_video,"start_comments":start_comments,"end_comments":end_comments},
		success: function (response) {
			comments_div.innerHTML += response
			comments_div.style.display = "block"
			start_comments+=how_get
			end_comments+=how_get
		}
	})
}

function like_video(e,id){
	if (e.style.opacity == "0.5"){
		return
	}

	e.style.opacity = "0.5"

	conn_u.send(JSON.stringify({'type':'like_video','id':id}))
	like_count = document.getElementById("like_count")
	like_count.innerText = parseInt(like_count.innerText)+1
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
let get_can = true

async function get_can_true() {
	await sleep(700)
	get_can = true
}

comments_div.addEventListener('scroll', async function(e) {
	if($(window).scrollTop()+$(window).height()>=$(document).height()-300){
	  if (get_can) {
	 		get_comments()
	 		get_can = false
	 		get_can_true()
	 	}
	}
})


let reply = false
let btn_reply
let user_reply

function comment_video_user(e){
	let inp_comment = document.querySelector('.inp_comment')

	if (reply){
		conn_u.send(JSON.stringify({'type':'comment_video_reply','com_id':btn_reply.id,'video_id':btn_reply.value,'text':inp_comment.value}))
	}else{
		conn_u.send(JSON.stringify({'type':'comment_video_user', "id":e.value,'text':inp_comment.value}))
	}
	reply = false
	inp_comment.value = ""
}


function select_video_reply(e,user){
	user_reply = user
	let com = document.querySelector('.com_'+e.id)
	com.style.background = "rgba(0,0,0,0.1)"
	reply = true
	if(btn_reply){
		document.querySelector('.com_'+btn_reply.id).style.background = "none"
	}
	btn_reply = e
}

function delete_video(e){
	e.remove()
	conn_u.send(JSON.stringify({'type':'delete_video', "id":id_video}))
}