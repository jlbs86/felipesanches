function ajaxGet(url, callBack) {
  // Signature: callBack(success, xmlhttp)
  var req = new XMLHttpRequest();
  req.open("GET", url, true);
  req.onreadystatechange = function(){
    if ( req.readyState == 4 ) {
      var success = (req.status == 200) || (req.status == 0);
      callBack( success, req );
    }
  };
  req.send(null);
}

var Display = function(svg, template_filename, col, row){
  this.shapes = new Array();

//todo. calc these values instead of using hardcoded width&height
  this.x0 = col*172;
  this.y0 = row*218;

  var self = this;
  this.load_template(template_filename, function(template){self.init(svg, template)});
}

Display.prototype.init = function(svg, template){
  svg.appendChild(template);
  template.setAttribute("transform", "translate("+this.x0+","+this.y0+")");
  
  var group = template.getElementsByTagName("g")[0];
  for (var n in group.childNodes){
    var node = group.childNodes[n];
    if (node.tagName == "path") this.shapes.push(node);
  }
}

Display.prototype.load_template = function(filename, callback){
  var self = this;
  ajaxGet(
    filename,
    function(success, req){
      if ( success ) {
        callback( req.responseXML.getElementById("display").cloneNode(true) );
      } else {
        alert("error while loading display template.");
      }
    });
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


