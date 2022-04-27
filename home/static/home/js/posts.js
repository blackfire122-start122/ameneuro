let start_comments = {}
let end_comments = {}

function like(e){
	conn_u.send(JSON.stringify({'type':'like', "id":e.id}))

	e.style.opacity = "0.5"
	e.onclick = null
	e.parentNode.childNodes[3].innerText = parseInt(e.parentNode.childNodes[3].innerText)+1
}

let get_com_can = true

async function get_can_com_true() {
	await sleep(700)
	get_com_can = true
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
function get_comments(e,comments_div){
	$.ajax({
		url: comment_ajax,
		data: {'id':e.id,"start_comments":start_comments[e.id],"end_comments":end_comments[e.id]},
		success: function (response) {
			comments_div.innerHTML += response
			comments_div.style.display = "block"
			start_comments[e.id]+=how_get
			end_comments[e.id]+=how_get

			comments_div.addEventListener('scroll', async function() {
				if($(comments_div).scrollTop()+$(comments_div).height()>=$(comments_div).height()-300){
				  if (get_com_can) {
				 		get_comments(e,comments_div)
				 		get_com_can = false
				 		get_can_com_true()
				 	}
				}
			})

		}
	})
}

function show_comment(comments_div,e){
	comments_div.style.display = "block"
	e.onclick = ()=>{close_comment(comments_div,e)}
}

function close_comment(comments_div,e){
	comments_div.style.display = "none"
	e.onclick = ()=>{show_comment(comments_div,e)}
}

function comments(e){
	start_comments[e.id] = 0
	end_comments[e.id] = how_get
	div_menu_post = document.querySelector(".post_"+e.id)
	comments_div = div_menu_post.childNodes[11]
	
	e.onclick = ()=>{close_comment(comments_div,e)}
	get_comments(e,comments_div)
}


function like_comment(e){
	conn_u.send(JSON.stringify({'type':'comment_like', "id":e.id}))

	e.style.opacity = "0.5"
	e.onclick = null
	e.parentNode.childNodes[3].innerText = parseInt(e.parentNode.childNodes[3].innerText)+1
}

let reply = false
let btn_reply
let user_reply

function comment_user(e){
	let inp_comment = document.querySelector('.inp_comment'+e.value)

	if (reply){
		conn_u.send(JSON.stringify({'type':'comment_reply','com_id':btn_reply.id,'post_id':btn_reply.value,'text':inp_comment.value}))
		
		conn_u_f = new WebSocket("ws://"+window.location.hostname+"/user/"+user_reply)	
		conn_u_f.onopen = ()=>{
			conn_u_f.send(JSON.stringify({'type':'activity'}))
			conn_u_f.close()
		}
	}else{
		conn_u.send(JSON.stringify({'type':'comment_user', "id":e.value,'text':inp_comment.value}))
	}
	reply = false
	inp_comment.value = ""
}


function select_reply(e,user){
	user_reply = user
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

let id_share

function share(id){
	$.ajax({
		url: share_ch_ajax,
		data: {"type":'all'},
		success: function (response) {
			document.querySelector(".chats").innerHTML += response
		}
	})

	id_share = id
	document.querySelector(".friends_share").style.display = "block"
	post_share = document.querySelector(".post_share")
	post_share.innerHTML = ""
	post_share.appendChild(document.querySelector(".post_"+id).querySelector(".header_post_user").cloneNode(deep=true))
	post_share.appendChild(document.querySelector(".post_"+id).childNodes[3].cloneNode(deep=true))
}

function close_sh(){
	document.querySelector(".friends_share").style.display="none"
}
function share_btn(ch_id,friend,ch_pk){
	conn = new WebSocket("ws://"+window.location.hostname+"/chat/"+ch_id)
	conn_u_f = new WebSocket("ws://"+window.location.hostname+"/user/"+friend)
 
	conn.onopen = ()=>{
		conn.send(JSON.stringify({'type':'share','chat':ch_pk,'user': user,'id_share':id_share,'msg':"http://"+window.location.hostname+"/post/"+id_share+ "#@" +document.querySelector("#mess_share").value}))
		conn.close()
	}
	conn_u_f.onopen = ()=>{
		conn_u_f.send(JSON.stringify({'type':'msg','msg':"http://"+window.location.hostname+"/post/"+id_share+ "#@;" +document.querySelector("#mess_share").value,'from_user': user, "from_chat":ch_id}))
		conn_u_f.close()
	}

}

function delete_post(id_post){
	popup = document.createElement('div')
	btn_delete = document.createElement('button')
	btn_not = document.createElement('button')
	h2 = document.createElement('h2')

	popup.className = "popup"

	btn_delete.className = "btn_delete_post"
	btn_delete.innerText = "Delete"

	btn_delete.addEventListener('click',()=>{
		conn_u.send(JSON.stringify({'type':'delete_post', "id":id_post}))
		popup.remove()
	})
	btn_not.className = "btn_not_post"
	btn_not.innerText = "Not delete"
	btn_not.addEventListener('click',()=>{
		popup.remove()
	})
	
	h2.innerText = "Really delete"
	h2.className = "h2_delete"

	popup.append(h2)
	popup.append(btn_not)
	popup.append(btn_delete)

	document.body.append(popup)

	let opt_menu = document.querySelector('#opt_'+id_post)
	let opt_img = document.getElementById(id_post)
	opt_img.value = false
	opt_menu.style.display = "none"
}

let posts_div = document.querySelector('.posts')

try {
	$.ajax({
		url: post_ajax,
		data: {'id':post_id},
		error: (data)=> {
			console.log(data)
		},
		success: (data) =>{
			if (data["info"] != "None post"){
				posts_div.innerHTML += data
			}
		}
	})
} catch (err) {}

function save_post(e,id){
	conn_u.send(JSON.stringify({'type':'save_post', "id":id}))
	e.addEventListener('click',() => {not_save_post(e,id)})
	e.style.opacity = "0.5"
}
function not_save_post(e,id){
	conn_u.send(JSON.stringify({'type':'not_save', "id":id}))
	e.addEventListener('click',() => {save_post(e,id)})
	e.style.opacity = "1"
}

function find_user_share(e){
	$.ajax({
		url: share_ch_ajax,
		data: {"type":'find_ch' ,"find_ch":e.value},
		success: function (response) {
			document.querySelector(".chats").innerHTML = response
		}
	})
}