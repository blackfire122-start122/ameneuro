function toggleAudio (btn) {
  audio = document.getElementById(btn.value)
  timeline = document.getElementById("timeline_"+btn.value)
  
  update_time = false
  setInterval(()=>{
    update_time = true
  },1000)
  
  audio.ontimeupdate = ()=>{
    if (update_time){
      const percentagePosition = (100*audio.currentTime) / audio.duration
      timeline.style.backgroundSize = `${percentagePosition}% 100%`
      timeline.value = percentagePosition
      update_time = false
    }
  }

  if (audio.paused) {
    audio.play()
    btn.childNodes[0].src = play_img
  } else {
    audio.pause()
    btn.childNodes[0].src = pause_img
  }
}

function changeSeek(timeline) {
  audio = document.getElementById(String(timeline.id).slice(9))
  const time = (timeline.value * audio.duration) / 100
  audio.currentTime = time

  const percentagePosition = (100*audio.currentTime) / audio.duration
  timeline.style.backgroundSize = `${percentagePosition}% 100%`
  timeline.value = percentagePosition
}

$.ajax({
  type: $(this).attr('post'),
  url: musics_all_ajax,
  data: {'id':id_user},
  success: function (response) {
     document.querySelector(".music_all").innerHTML = response
  }
})

