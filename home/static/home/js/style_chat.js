function toggleAudio_mess (btn) {
  audio = document.getElementById("audio_"+btn.value)
  timeline = document.getElementById("timeline_"+btn.value)
  
  audio.addEventListener("play",play_audio)
  audio.addEventListener("pause",pause_audio)
  
  audio.ontimeupdate = ()=>{
    const percentagePosition = (100*audio.currentTime) / audio.duration
    timeline.style.backgroundSize = `${percentagePosition}% 100%`
    timeline.value = percentagePosition
  }

  if (audio.paused) {
    all_pause_mess()
    audio.play()
  } else {
    audio.pause()
  }
}

function changeSeek_mess(timeline) {
  audio = document.getElementById("audio_"+String(timeline.id).slice(9))
  audio.ontimeupdate = null
  const time = (timeline.value * audio.duration) / 100
  audio.currentTime = time

  const percentagePosition = (100*audio.currentTime) / audio.duration
  timeline.style.backgroundSize = `${percentagePosition}% 100%`
  timeline.value = percentagePosition


  audio.addEventListener("play",play_audio)
  audio.addEventListener("pause",pause_audio)
  
  all_pause_mess()
  audio.play()

}

function all_pause_mess(){
  audios = document.getElementsByClassName("audio_ap")
  for (i=audios.length-1;i>=0;--i){
    audios[i].pause()
  }
}

function play_audio(e){
  e.target.parentNode.childNodes[5].childNodes[1].childNodes[0].src = play_img
}

function pause_audio(e){
  e.target.parentNode.childNodes[5].childNodes[1].childNodes[0].src = pause_img
}

function file_see(e){
  file = e.cloneNode()
  file.className = "file_see_js"
  file.controls = true

  div = document.createElement("div")
  span = document.createElement("span")

  div.className = "file_see"
  span.innerText = "X"
  span.className = "close_file_see"
  span.addEventListener("click",()=>{
    div.remove()
  })


  div.append(span)
  div.append(file)

  document.body.append(div)
}
