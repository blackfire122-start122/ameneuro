jQuery.expr.filters.visible = function( elem ) {
    return !!( elem.offsetWidth || elem.offsetHeight || elem.getClientRects().length );
};

let ma = document.getElementsByClassName("ma")

window.addEventListener("scroll",()=>{
	for (let i = ma.length - 1; i >= 0; i--) {
		if (Visible(ma[i])){
      if (ma[i].childNodes[3].className == "point"){
        conn_u.send(JSON.stringify({'type':'visible_ma','id': ma[i].id}))
        ma[i].childNodes[3].className = "not_point"
      }
		}
	}
})

function Visible(target) {
  let targetPosition = {
      top: window.pageYOffset + target.getBoundingClientRect().top,
      left: window.pageXOffset + target.getBoundingClientRect().left,
      right: window.pageXOffset + target.getBoundingClientRect().right,
      bottom: window.pageYOffset + target.getBoundingClientRect().bottom
    },
    windowPosition = {
      top: window.pageYOffset,
      left: window.pageXOffset,
      right: window.pageXOffset + document.documentElement.clientWidth,
      bottom: window.pageYOffset + document.documentElement.clientHeight
    }

  if (targetPosition.bottom > windowPosition.top &&
    targetPosition.top < windowPosition.bottom &&
    targetPosition.right > windowPosition.left &&
    targetPosition.left < windowPosition.right) {
    return true
  } else {
    return false
  }
}

conn_u.onopen = ()=>{
	conn_u.send(JSON.stringify({'type':'first_conn','user': username}))	
	conn_u.send(JSON.stringify({'type':'yes_in_net','user_in': username}))
  conn_u.send(JSON.stringify({'type':'get_play_in_all'}))
	
	for (let i = ma.length - 1; i >= 0; i--) {
		if (Visible(ma[i])){
			conn_u.send(JSON.stringify({'type':'visible_ma','id': ma[i].id}))
		}
	}
}

let mess_start = 0
let mess_end = how_get

function get_mess(){
  $.ajax({
    type: $(this).attr('post'),
    url: activity_mess_ajax,
    data: {"mess_start":mess_start,"mess_end":mess_end},
    success: function (response){
      document.querySelector("main").innerHTML += response
      mess_start+=how_get
      mess_end+=how_get
    }
  })
}

get_mess()

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
let get_can = true

async function get_can_true() {
  await sleep(700)
  get_can = true
}

window.addEventListener('scroll', async function(e) {
  if($(window).scrollTop()+$(window).height()>=$(document).height()-500){
    if (get_can) {
      get_mess()
      get_can = false
      get_can_true()
    }
  }
})