musics = document.querySelector('.musics')

musics_s = true
function music_show(){
	if(musics_s){
		musics.style.display = 'block'
	}else{
		musics.style.display = 'none'
	}
	musics_s = !musics_s
}