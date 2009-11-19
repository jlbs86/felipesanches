//Globar vars:
var mode = "playback";
var current_subtitle = null;
var subtitles_textbox = [];
var autoskipback;
var autoskipback_ammount;
var autoskip_timeout;

//---------------


function displaySubtitles_sync(){
  if (current_subtitle == null){
    subtitles_textbox[0].value = "";
    subtitles_textbox[1].value = "";
    subtitles_textbox[2].value = "";
    subtitles_textbox[3].value = "";
    subtitles_textbox[4].value = "";
    return;
  }

  var subs = current_subtitle["content"];
  var currentTime = Math.round(video.currentTime * 1000);
  if (subs[0].start>=0 && currentTime < subs[0].start) current_title_sync = 0;

  for (i=0; i < subs.length; i++){
    if ((subs[i].start != -1) && (currentTime >= subs[i].start) && ((currentTime < subs[i].end) || (subs[i].end==-1))){
      current_title_sync = i+1;
      break;
    }
  }

  var i = current_title_sync-1;
  subtitles_textbox[0].value = (i-2>=0) ? subs[i-2]["text"] : "";
  subtitles_textbox[1].value = (i-1>=0) ? subs[i-1]["text"] : "";
  subtitles_textbox[2].value = (i>=0 && i < subs.length) ? subs[i]["text"] : "";
  subtitles_textbox[3].value = (i+1<subs.length) ? subs[i+1]["text"] : "";
  subtitles_textbox[4].value = (i+2<subs.length) ? subs[i+2]["text"] : "";
}

function setup_autoskip(){
  if (autoskip_timeout)
    clearTimeout(autoskip_timeout);

  autoskip_timeout = setTimeout( auto_skip, autoskipback_interval.value*1000);
}

function auto_skip(){                        
  if (autoskipback.checked){
    var newval = video.currentTime - autoskipback_ammount.value;
    video.currentTime = (newval >= 0 ? newval : 0);
    setup_autoskip();
  } else {
    if (autoskip_timeout)
      clearTimeout(autoskip_timeout);  
  }
}

function autoskip_clicked(event){
  if (autoskipback.checked) setup_autoskip();
}

function load(event){
  video = document.getElementById("video");
  subtitles_textbox.push(document.getElementById("textbox1"));
  subtitles_textbox.push(document.getElementById("textbox2"));
  subtitles_textbox.push(document.getElementById("textbox3"));
  subtitles_textbox.push(document.getElementById("textbox4"));
  subtitles_textbox.push(document.getElementById("textbox5"));

  autoskipback = document.getElementById("autoskipback");
  autoskipback_ammount = document.getElementById("autoskipback-ammount");
  autoskipback_interval = document.getElementById("autoskipback-interval");

  autoskipback.addEventListener("click", autoskip_clicked, false);
  
}
