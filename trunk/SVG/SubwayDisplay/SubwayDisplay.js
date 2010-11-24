var svgDocument;
var sprites;
var NUM_SPRITES;

var delta_t = 50; //frequency = 1/50ms = 20Hz

function init(evt){
	sprites = new Array();

	var O=evt.target;
	svgDocument=O.ownerDocument;

  for (var i=0;i<10;i++)
  	sprites.push(svgDocument.getElementById("seg0"+i));
  for (var i=10;i<=64;i++)
  	sprites.push(svgDocument.getElementById("seg"+i));

	NUM_SPRITES=64;
	window.setInterval(mytimer, delta_t);
}

function mytimer(){
		random_flashing();
}

function turn_on(i){
	if (sprites[i]){
		sprites[i].setAttribute("style", "fill:#fcfb79");
	}
}

function turn_off(i){
	if (sprites[i]){
		sprites[i].setAttribute("style", "fill:#4d1908");
  }
}

function random_flashing(){
	for (i=0;i<20;i++){
		turn_on(Math.floor(Math.random()*NUM_SPRITES));
		turn_off(Math.floor(Math.random()*NUM_SPRITES));
	}
}
