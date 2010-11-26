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

var xx=0;
function drawing_function(points, middle){
  var x=middle[0];
  var y=middle[1];
  return (x+y<xx);
}

function timer(){
  for (m in modules){
    var mod = modules[m];
    mod.draw(drawing_function);
  }
  xx+=20;
  if (xx>1500) xx=0;
}

