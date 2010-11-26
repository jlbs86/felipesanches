var Display = function(mosaic, col, row){
  this.shapes = new Array();

//todo. calc these values instead of using hardcoded width&height
  this.x0 = col*172;
  this.y0 = row*218;

  var svg = mosaic.ownerDocument;
  var theDisplay = mosaic.cloneNode(true);
  
  svg.getElementsByTagName("svg")[0].appendChild(theDisplay);
  theDisplay.setAttribute("transform", "translate("+this.x0+","+this.y0+")");
  
  var group = theDisplay.getElementsByTagName("g")[0];
  for (var n in group.childNodes){
    var node = group.childNodes[n];
    if (node.tagName == "path") this.shapes.push(node);
  }

/*
  var delta_t = 50; //frequency = 1/200ms = 5Hz
  var self = this;
	window.setInterval(function(){self.timer()}, delta_t);
*/
}

Display.prototype.timer = function(){
  this.random_flashing();
}

Display.prototype.turn_on = function(i){
	if (this.shapes[i])	this.turn_on_shape(this.shapes[i]);
}

Display.prototype.turn_off = function(i){
	if (this.shapes[i])	this.turn_off_shape(this.shapes[i]);
}

Display.prototype.turn_on_shape = function(s){
	if (s) s.setAttribute("style", "fill:#fcfb79");
}

Display.prototype.turn_off_shape = function(s){
	if (s) s.setAttribute("style", "fill:#4d1908");
}

Display.prototype.random_flashing = function(){
	for (var i=0;i<20;i++){
		this.turn_on(Math.floor(Math.random()*this.shapes.length));
		this.turn_off(Math.floor(Math.random()*this.shapes.length));
	}
}

Display.prototype.draw = function(func){
	for (var s in this.shapes){
	  var shape = this.shapes[s];
	  if (!shape.points){
	    shape.points = new Array();

      var x=0,y=0;
      var mx=0,my=0;
      var scale = 0.2038;
	    for (var i = 0; i < shape.pathSegList.numberOfItems; i++){
        var seg = shape.pathSegList.getItem(i);

        switch(seg.pathSegType){
          case seg.PATHSEG_MOVETO_REL:
            x += seg.x;
            y += seg.y;
            break;
          case seg.PATHSEG_MOVETO_ABS:
            x = seg.x;
            y = seg.y;
            break;
          case seg.PATHSEG_LINETO_REL:
            mx+=x;
            my+=y;
            shape.points.push([this.x0 + x*scale,this.y0 + y*scale]);
            x += seg.x;
            y += seg.y;
            break;
          case seg.PATHSEG_LINETO_ABS:
            mx+=x;
            my+=y;
            shape.points.push([this.x0 + x*scale,this.y0 + y*scale]);
            x = seg.x;
            y = seg.y;
            break;
          case seg.PATHSEG_CLOSE:
            mx+=x;
            my+=y;
            shape.points.push([this.x0 + x*scale,this.y0 + y*scale]);
          default:
        }
      }

      shape.middle_point = [this.x0 + mx*scale/shape.points.length,this.y0 + my*scale/shape.points.length];
    }

    if (func(shape.points, shape.middle_point))
      this.turn_on_shape(shape);
    else
      this.turn_off_shape(shape);

	}
}


