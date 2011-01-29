// ==UserScript==
// @name           DMD subtitles
// @namespace      subtitles in a dot matrix display
// @include        http://universalsubtitles.org/en/videos/*
// ==/UserScript==


(function (){


var dmd;
function send_dmd_text(text){
       dmd.innerHTML=text;
       //todo: add actual dmd messaging here



 setTimeout(function() {
       GM_xmlhttpRequest({
           method: 'GET',
           url: 'http://192.168.0.143:8080/&'+text,
       });
 }, 0);



}


function widgetChanged(w){
       var div = document.getElementsByClassName("mirosubs-captionDiv")[0];
       if (div){
               send_dmd_text(div.textContent);
       }
}

function do_it_later(){
       var widget = document.getElementsByClassName("mirosubs-widget")[0];
       widget.addEventListener("DOMSubtreeModified", widgetChanged, false);
       dmd = document.getElementsByClassName("title-container")[0];
}

window.setTimeout(do_it_later, 1000);

})();
