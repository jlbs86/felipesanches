//Globar vars:
var mode = "playback";
var current_subtitle = null;
var current_title_sync;
var subtitles_textbox = [];
var autoskipback;
var autoskipback_ammount;
var autoskip_timeout;
var video;
var holdingkey=false;
var subtitles_p;

//---------------

function displaySubtitles_sync(){
  if (current_subtitle == null){
    subtitles_textbox[0].innerHTML = "[silence]";
    subtitles_textbox[1].innerHTML = "[silence]";
    subtitles_textbox[2].innerHTML = "[silence]";
    subtitles_textbox[3].innerHTML = "[silence]";
    subtitles_textbox[4].innerHTML = "[silence]";
    subtitles.innerHTML = "";
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
  subtitles_textbox[0].innerHTML = (i-2>=0 && subs[i-2]["text"] != "") ? subs[i-2]["text"] : "[silence]";
  subtitles_textbox[1].innerHTML = (i-1>=0 && subs[i-1]["text"] != "") ? subs[i-1]["text"] : "[silence]";
  subtitles_p.innerHTML = subtitles_textbox[2].innerHTML = (i>=0 && i < subs.length && subs[i]["text"] != "") ? subs[i]["text"] : "[silence]";
  if (subtitles_p.innerHTML == "[silence]") subtitles_p.innerHTML = ""
  subtitles_textbox[3].innerHTML = (i+1<subs.length && subs[i+1]["text"] != "") ? subs[i+1]["text"] : "[silence]";
  subtitles_textbox[4].innerHTML = (i+2<subs.length && subs[i+2]["text"] != "") ? subs[i+2]["text"] : "[silence]";
}

function sync_mode(){
  var transcriptiondiv = document.getElementById("transcription");
  var syncdiv = document.getElementById("syncing");
  var titlesdiv = document.getElementById("titles_list");
  var textinput = document.getElementById("textinput");

  transcriptiondiv.style.display="none";
  syncdiv.style.display="block";

  textinput.style.display="none";
  titlesdiv.style.display="block";

  var titles = document.getElementById("titles_textarea").value.split('\n');
  var subs = [];
  for (i in titles){
    subs.push({"text": titles[i], "start":-1,"end":-1});
  }
  current_subtitle = {"content":subs};
  current_title_sync = 0;

  //restart playback:
  video.currentTime = 0;

  video.addEventListener('timeupdate', function(e){
    displaySubtitles_sync(e.target.currentTime*1000)
  }, false);

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
  subtitles_p = document.getElementById("subtitles");

  subtitles_textbox.push(document.getElementById("title_1"));
  subtitles_textbox.push(document.getElementById("title_2"));
  subtitles_textbox.push(document.getElementById("title_3"));
  subtitles_textbox.push(document.getElementById("title_4"));
  subtitles_textbox.push(document.getElementById("title_5"));

  autoskipback = document.getElementById("autoskipback");
  autoskipback_ammount = document.getElementById("autoskipback-ammount");
  autoskipback_interval = document.getElementById("autoskipback-interval");

  autoskipback.addEventListener("click", autoskip_clicked, false);


  var select_key = function(value){
    switch (value){
      case "TAB": return 9;
      case "CTRL": return 17;
      case "[": return 219;
      case "]": return 221;
      case "SPACEBAR": return 32;
      case "|": return 220;
    }
  };

  function KeyUpHandler(event){
    holdingkey = false;

    var tap_key = select_key(document.getElementById("taphotkey").value);

    if (event.which == tap_key){
     if(current_title_sync == null) return;
      var subs = current_subtitle["content"];
      var now = Math.round(video.currentTime * 1000);
      if (current_title_sync>0) subs[current_title_sync-1].end = now;
      if (current_title_sync<subs.length){
        subs[current_title_sync].start = now;
        current_title_sync++;
      }
    }

  }

  function KeyDownHandler(event){
    if (holdingkey==true) return;
    holdingkey = true;

    var rewind_key = select_key(document.getElementById("rewindhotkey").value);
    var playpause_key = select_key(document.getElementById("playpausehotkey").value);

    if (event.which == rewind_key){
      var newval = video.currentTime - 3;
      video.currentTime = (newval >= 0 ? newval : 0);
      //TODO: inhibit key event propagation (?)
    }

    if (event.which == playpause_key){
      if (video.paused || video.ended)
          self.video.play();
      else
          video.pause();
      //TODO: inhibit key event propagation (?)
    }

  };

  window.addEventListener("keydown", KeyDownHandler, false);
  window.addEventListener("keyup", KeyUpHandler, false);
  
}
