var modules = new Array();

function init(evt){
	var O=evt.target;
	var svgDoc=O.ownerDocument;
  var mosaic = svgDoc.getElementById("display");

  for (var i=0;i<5;i++){
    modules.push(new Display(mosaic, i, 0));
  }
  for (var i=0;i<5;i++){
    modules.push(new Display(mosaic, i, 1));
  }

  var delta_t = 100;
   //frequency = 1/200ms = 5Hz
	window.setInterval(timer, delta_t);
}

var r,cx,cy;
function reset_coordinates(){
  cy=600;
  cx=-100;
  r=20;
}
reset_coordinates();

function draw_rings(points, middle){
  var x=middle[0];
  var y=middle[1];

  var d = Math.sqrt((x-cx)*(x-cx) + (y-cy)*(y-cy))
  return (d<r && d>(r*0.8) || d<(r*0.6) && d>(r*0.5) || d<(r*0.3));
}

function timer(){
  for (m in modules){
    var mod = modules[m];
    mod.draw(draw_rings);
  }

  cx += 20;
  cy -= 5;
  r +=10;
  if (cx>1500) {
    reset_coordinates();
  }
}

