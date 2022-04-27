function toggleAudio (btn,selector_audio="audio_",selector_timeline="timeline_") {
  audio = document.getElementById(selector_audio+btn.value)
  timeline = document.getElementById(selector_timeline+btn.value)
  
  audio.addEventListener("play",play_audio)
  audio.addEventListener("pause",pause_audio)

  if (audio.paused) {
    all_pause()
    audio.play()
  } else {
    audio.pause()
  }

  audio.ontimeupdate = ()=>{
    const percentagePosition = (100*audio.currentTime) / audio.duration
    timeline.style.backgroundSize = `${percentagePosition}% 100%`
    timeline.value = percentagePosition
    if(timeline.value >= 100){
      toggleAudio(audio.parentNode.nextSibling.nextSibling.childNodes[5].childNodes[1])
    }
  }
}

function changeSeek(timeline) {
  audio = document.getElementById("audio_"+String(timeline.id).slice(9))
  const time = (timeline.value * audio.duration) / 100
  audio.currentTime = time

  const percentagePosition = (100*audio.currentTime) / audio.duration
  timeline.style.backgroundSize = `${percentagePosition}% 100%`
  timeline.value = percentagePosition


  audio.addEventListener("play",play_audio)
  audio.addEventListener("pause",pause_audio)
  
  all_pause()

  audio.ontimeupdate = ()=>{
    const percentagePosition = (100*audio.currentTime) / audio.duration
    timeline.style.backgroundSize = `${percentagePosition}% 100%`
    timeline.value = percentagePosition
    if(timeline.value >= 100){
      toggleAudio(audio.parentNode.nextSibling.nextSibling.childNodes[5].childNodes[1])
    }
  }
}

function all_pause(){
  audios = document.getElementsByClassName("audio_ap")
  for (i=audios.length-1;i>=0;--i){
    audios[i].pause()
    audios[i].ontimeupdate = null  
  }
}

function play_audio(e){
  e.target.parentNode.childNodes[5].childNodes[1].childNodes[0].src = play_img
}

function pause_audio(e){
  e.target.parentNode.childNodes[5].childNodes[1].childNodes[0].src = pause_img
}