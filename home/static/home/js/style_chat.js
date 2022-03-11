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

musics_s = true
function music_show(){
  let musics = document.querySelector('.musics')
  if (musics_s){
    musics.style.display = 'block'
  }else{
    musics.style.display = 'none'
  }
  musics_s = !musics_s
}

window.addEventListener('scroll',()=>{
  if(window.scrollY!=0){return}
  
  $.ajax({
    url: chat_get_mess_ajax,
    data: {'chat_id':chat_id},
    success: function (response) {
      msgs = msg_div.innerHTML 
      msg_div.innerHTML = response+msgs
      // window.scrollTo(0,1)
      fon_msgs()
    }
  })
})

$.ajax({
  url: chat_get_mess_ajax,
  data: {'chat_id':chat_id},
  success: function (response) {
    msgs = msg_div.innerHTML 
    msg_div.innerHTML = response+msgs
    // window.scrollTo(0,1)
    intS = setInterval(scrollToEndPage,5)
    fon_msgs()
    end_readable_send()
  }
})

let intS
let height = 20
let attempt = 5

function scrollToEndPage() {
  if (height < document.body.scrollHeight){
    window.scrollTo(0, height)
    attempt++
    height = parseInt(height) + attempt
  }else{
    clearInterval(intS);
  }
}

function inp_ran(e){
  document.querySelector('#mes_bg').style.opacity = e.value
}


let chat_options_change = false

function chat_options(e) {
  let messages = document.querySelector(".messages")
  let input_mes_send = document.querySelector(".input_mes_send")
  let options_div = document.querySelector(".options")
  let error = document.querySelector('#error')


  if (chat_options_change) {
    messages.style.display='flex'
    input_mes_send.style.display='block'
    chat_options_change = false
    options_div.style.display = "none"
    options_div.innerHTML = ''
    error.style.display='none'
    intS = setInterval(scrollToEndPage,0)
    return
  }else{
    messages.style.display='none'
    input_mes_send.style.display='none'
    options_div.style.display = "block"
    error.style.display='block'
  }

  $.ajax({
    url: chat_options_ajax,
    data: {'chat_id':chat_id},
    success: function (response) {options_div.innerHTML = response}
  })
  chat_options_change = true

}

function hexToRgb(hex) {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return [parseInt(result[1], 16),
          parseInt(result[2], 16),
          parseInt(result[3], 16)
          ]
}
let rgba = hexToRgb(color_mes_bg)

function fon_msgs(){
  my_msgs = document.getElementsByClassName('my_msgs')
  other_msgs = document.getElementsByClassName('other_msgs')
  
  for (let i = my_msgs.length-1; i>=0 ;i-- ){
    my_msgs[i].style.background = "rgba("+rgba[0]+","+rgba[1]+","+rgba[2]+","+color_mes_bg_op + ")"
  }
  for (let i = other_msgs.length-1; i>=0 ;i-- ){
    other_msgs[i].style.background = "rgba("+rgba[0]+","+rgba[1]+","+rgba[2]+","+color_mes_bg_op + ")"
  }
}