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
	
	for (let i = ma.length - 1; i >= 0; i--) {
		if (Visible(ma[i])){
			conn_u.send(JSON.stringify({'type':'visible_ma','id': ma[i].id}))
		}
	}
}


