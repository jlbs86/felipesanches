// ==UserScript==
// @name	Youtube Subtitles v0.03 
// @include	http://www.youtube.com/watch*
// ==/UserScript==
//
// This userscript is free software licensed under
//  the General Public License version 3.0 or later.
// (c)2006, 2008 Felipe Corrêa da Silva Sanches <felipe.sanches@gmail.com>
//
// Release notes
//
// v0.03 (September 30th, 2008):
// * Changed to Miro Project server
// * convert first char in videocode to uppercase
// * upgrade to GPLv3 or later licensing
//
// v0.02 (someday in 2006):
// * Support for multiple line subtitles
// * Nicer font face and size
// * Yellow on black
// * Fixed height for the subtitles div 
//
// v0.01 alpha (someday in 2006):
// * First release.
// * Wiki subtitles repository integration


var subtitle_data = null;

var video_id = document.location.search.split("=");
video_id=video_id[1].split("&");
video_id=video_id[0];
upch = video_id.substring(0,1).toUpperCase()
rest = video_id.substring(1);
video_id_upper = upch + rest;

scripts = document.getElementsByTagName("script");
for (i in scripts){
	tvar = scripts[i].textContent.split("fullscreenUrl")
	if (tvar.length > 1){
		tvar = tvar[1].split("t=")[1].split("&")[0]
		break;
	}
}

var subtitles_server = "http://www.wstr.org/subs/index.php?title=";
var ytvideo = document.getElementById("watch-player-div");
flashobj = document.getElementsByTagName("embed");
flashobj.height = "30";
//+= -> = :
ytvideo.innerHTML ='<div id="flowplayer-div" style="height:400px">FLOWPLAYER HERE!</div><div style="height:4em; font-size:3em; font-family: garamond; color:yellow; background-color: black;" id="legenda">The subtitles will be here!</div>';

//Load flashembed.js
var p = unsafeWindow;
function waitForFlashEmbed() {
    if (typeof p.flashembed=='undefined'){
	// set to check every 100 milliseconds if the libary has loaded
        window.setTimeout(waitForFlashEmbed, 100);
    } else {
	//Load flowplayer
	p.flashembed("flowplayer-div", "http://www.wstr.org/grease/FlowPlayerLight.swf", {config: { 
	    videoFile: encodeURIComponent("http://www.youtube.com/get_video.php?video_id=" + video_id + "&fmt=5&t=" + tvar), 
	    initialScale: 'scale'
	}});
    }
}
function loadFlashEmbed() {
	// dynamically creates a script tag
        var newjs = document.createElement('script');
        newjs.type = 'text/javascript';
        newjs.src = 'http://www.wstr.org/grease/flashembed-0.31.js';
        document.getElementsByTagName('head')[0].appendChild(newjs);
        waitForFlashEmbed();
}

//window.addEventListener('load', loadFlashEmbed(), false);
loadFlashEmbed();

var subtdiv = document.getElementById("legenda");
erase_subtitle();

GM_xmlhttpRequest({
  method:"GET",
  url: subtitles_server + "Special:Export/Subtitles/" + video_id_upper,
  onload:function(details) {
//	alert(details.responseText);
    	subtitle_data=details.responseText.split("text");
	if (subtitle_data.length == 1) {
		subtdiv.innerHTML+='Collaborate creating a subtitle for this video in the <a href="'+ subtitles_server +'Subtitles/' + video_id_upper + '" >wiki</a>';
		return;
	}
	subtitle_data=subtitle_data[1].split(">");
	subtitle_data=subtitle_data[1].split("<");
	is_redir = subtitle_data[0].split("#REDIRECT");
	if (is_redir.length > 1){
			subtitle_data=subtitle_data[0].split("[[");
			subtitle_data=subtitle_data[1].split("]]");
			GM_xmlhttpRequest({
			  method:"GET",
			  url:subtitles_server + "Especial:Export/" + subtitle_data[0],
			  onload:function(details) {
			    	subtitle_data=details.responseText.split("text");
				subtitle_data=subtitle_data[1].split(">");
				subtitle_data=subtitle_data[1].split("<");
				subtitle_data=subtitle_data[0].split("\n");
				schedule_next_line();
			  }
			});
	} else {
		subtitle_data=subtitle_data[0].split("\n");
		schedule_next_line();
	}
  }
});

var counter = 0;
var oldtime = 0;

function schedule_next_line(){
//	while (line = (subtitle_data[counter++]) == ""){}; //ignore white space
	counter++; //ignore line number
	time = subtitle_data[counter++].split("\;");
	newtime = parsetime(time[0]);
	newendtime = parsetime(time[1]);
	setTimeout(print_subtitle,  newtime - oldtime);
	setTimeout(erase_subtitle,  newendtime - oldtime);
	oldtime = newtime;
}

function print_subtitle(){
	line = "";
	while(subtitle_data[counter].length > 0){
		if (line != "") line += "<br>";
		line += subtitle_data[counter++];
	}
	subtdiv.innerHTML = '<center>' + line + '</center>';
	counter++; //skip blank line
	schedule_next_line();
}

function erase_subtitle(){
	subtdiv.innerHTML = '';
}

function parsetime(time){
	value = time.split(":");
	hours = parseFloat(value[0]);
	minutes = parseFloat(value[1]);
	seconds = value[2];
	seconds_array = seconds.split(","); //goodbye, comma!
	seconds = parseFloat(seconds_array[0]);
	milis = seconds_array[1]
	//milis = milis.split(" "); //remove trailling spaces
	milis = parseFloat(milis[0]); 
	return (milis + (seconds + (minutes + hours*60)*60)*1000);
}
