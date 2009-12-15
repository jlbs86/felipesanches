var current_line = null;
var input_fields = null;
var MAXCHARS = 100;
var transcript_disabled = false;

function add_line(){
  if (current_line){
    current_line.style.background = "#ffd";

    //insert a silence marker:
    if (current_line.value.length==0){
      var silence = document.createElement("p");
      silence.innerHTML="(silence)";
      silence["className"] = "silence_marker";
      current_line.parentNode.insertBefore(silence, current_line);

      return current_line;
    }
  }

  var line = document.createElement("input");
  line.setAttribute("type", "text");
  line.setAttribute("class", "inputline");
  input_fields.appendChild(line);
  input_fields.appendChild(document.createElement("br"));
  line.focus();
  return line;
}

function hex(i){
  i = Math.floor(i);
  var code = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'];
  return code[i];
}

function color_scale(i){
  var first_chars = 40;
  if (i<first_chars) i=0
  else i-=first_chars;

  r=15;
  g = 16 - 16*i/(MAXCHARS-first_chars);
  b = 12 - 12*i/(MAXCHARS-first_chars);
  return "#" + hex(r) + hex(g) + hex(b);
}

function TranscriptWidgetKeyHandler(e){
  if (current_step !=1) return;
  current_line.style.background=color_scale(current_line.value.length);
  subtitles_p.innerHTML = check_and_prepare_for_double_line(current_line.value);

  if (((current_line.value.length > MAXCHARS) /* && e.type == "keypress" */ && e.keyCode == 32) ||
      (e.type == "keydown" && e.keyCode==13)){
    current_line = add_line();
  }

  var line = current_line;
  if (e.type == "keydown" && e.keyCode == 38){//up-arrow
    line = line.previousSibling;
    while (line && line.tagName != "INPUT"){
      line = line.previousSibling;
    }

    if (line){
      current_line.style.background = "#ffd";
      current_line = line;
      current_line.focus();
    }

  }

  if (e.type == "keydown" && e.keyCode == 40){//down-arrow
    line = line.nextSibling;
    while (line && line.tagName != "INPUT"){
      line = line.nextSibling;
    }

    if (line){
      current_line.style.background = "#ffd";
      current_line = line;
      current_line.focus();
    }
  }

}

function init_transcript_widget(event){
  input_fields = document.getElementById("inputfields");
  current_line = add_line();

  input_fields.addEventListener("keydown", TranscriptWidgetKeyHandler, true);
  input_fields.addEventListener("keyup", TranscriptWidgetKeyHandler, true);
  input_fields.addEventListener("keypress", TranscriptWidgetKeyHandler, true);
}
