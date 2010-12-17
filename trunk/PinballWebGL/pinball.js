const GRAVITY = 9.8; // m/s²
const PIXELS_PER_METER = 300; // px/m

function ball(x,y, vx, vy){
  //TODO: do we need Z coordinate? Will our ball jump in certain conditions?

  //ball position:
  this.x = x;
  this.y = y;
  
  if (!vx) vx=0;
  if (!vy) vy=0;

  //ball speed:
  this.vx = vx;
  this.vy = vy;
  
  //rotation speed for each spin axis:
  this.spinX = 0;
  this.spinY = 0;
  this.spinZ = 0;
  
  //TODO: figure out what are the weigth and size of a real pinball ball.
  this.mass = 0.010; // kg -> 10g ?
  this.radius = 0.012; // m -> 2.4cm diameter
}

ball.prototype.update = function(game){
  var delta_t = (Date.now() - game.time)/1000; // seconds

  //this.x += this.vx * delta_t;
  //this.y += this.vy * delta_t;
    
  //TODO: hit detection / selection of current rolling surface
  // lets suppose it is always rolling on the main playfield:
  var surface = game.playfield;

  var ax = 0;
  var ay = GRAVITY * Math.sin(surface.angle);
  
  this.vx += ax * delta_t;
  this.vy += ay * delta_t;
}

function playfieldStructure(path){
  this.path = path;
}

playfieldStructure.prototype.hit = function(ball){
  var ballHit = false;
  var x0=0,y0=0;
  ball.data="";
  //TODO: implement normalizedPathSegList in Firefox!!!
  for (var i = 0; i < this.path.pathSegList.numberOfItems; i++){
    var seg = this.path.pathSegList.getItem(i);

    switch(seg.pathSegType){
      case seg.PATHSEG_MOVETO_REL:
        //alert("PATHSEG_MOVETO_REL x:"+seg.x+" y:"+seg.y);
        x += seg.x;
        y += seg.y;
        break;
      case seg.PATHSEG_MOVETO_ABS:
        //alert("PATHSEG_MOVETO_ABS x:"+seg.x+" y:"+seg.y);
        x = seg.x;
        y = seg.y;
        break;
      case seg.PATHSEG_LINETO_REL:
        //alert("PATHSEG_LINETO_REL x:"+seg.x+" y:"+seg.y);
        x += seg.x;
        y += seg.y;
        ballHit = this.hitsLine(ball, x,y,x+seg.x,y+seg.y);
        break;
      case seg.PATHSEG_LINETO_ABS:
        //alert("PATHSEG_LINETO_ABS x:"+seg.x+" y:"+seg.y);
        ballHit = this.hitsLine(ball, x,y,x+seg.x,y+seg.y);
        x = seg.x;
        y = seg.y;
        break;
      default:
        alert("unhandled path seg type: \""+seg.pathSegTypeAsLetter+ "\"")
    }
    if (ballHit) return ballHit;
  }
  return false;
}

playfieldStructure.prototype.hitsLine = function(ball, x0,y0, x1,y1){
  var xc = ball.x*PIXELS_PER_METER;
  var yc = ball.y*PIXELS_PER_METER;
  var r = ball.radius*PIXELS_PER_METER;

  ball.data += " --- x0:"+x0+" y0:"+y0+" x1:"+x1+" y1:"+y1+" xc:"+xc+" yc:"+yc;

  if (x1==x0){
    if (x0>(xc-r) && x0<(xc+r))
      return true; //TODO: return a vector indicating hit direction
    else
      return false;
  }
  
  //angular coeficient;
  var m = (y1-y0)/(x1-x0);

  //equation of the line:  
  //y = m*(x - x0) + y0

  //equation of the circle:
  //(y-yc)² + (x-xc)² = radius²
  
  //solving the system:
  // (m*(x - x0) + y0 - yc)² + (x-xc)² = radius²
  // m²*(x - x0)² + 2*m*(x - x0)*(y0-yc) + (y0-yc)² + (x-xc)² = radius²

  //substituting variables:
  //X = x-x0

  // m²X² + 2m(y0-yc)X + (y0-yc)² + (X + x0-xc)² = radius²
  // m²X² + 2m(y0-yc)X + (y0-yc)² + X² + 2X(x0-xc) + (x0-xc)² = radius²
  // (m²+1)X² + (2m(y0-yc) + 2(x0-xc))X + (y0-yc)² + (x0-xc)² - radius² = 0
  // aX² + bX + c = 0 with:

  var a = (m^2+1);
  var b = (2*m*(y0-yc) + 2*(x0-xc));
  var c = (y0-yc)^2 + (x0-xc)^2 - r^2;

  var delta = b^2 - 4*a*c;
  if (delta<0) return false;

  var x = x0 + (-b + Math.sqrt(delta))/(2*a);
  var y = m*(x - x0) + y0;
  ball.root1_shape.setAttribute("cx", x);
  ball.root1_shape.setAttribute("cy", y);

  ball.root1_alert.setAttribute("style", "fill:green");
  ball.root2_alert.setAttribute("style", "fill:green");
  if ((x0<x1 && x>x0 && x<x1) || (x1 < x0 && x>x1 && x<x0)) return true;
  ball.root1_alert.setAttribute("style", "fill:red");

  x = x0 + (-b - Math.sqrt(delta))/(2*a);
  y = m*(x - x0) + y0;
  ball.root2_shape.setAttribute("cx", x);
  ball.root2_shape.setAttribute("cy", y);

  if ((x0<x1 && x>x0 && x<x1) || (x1 < x0 && x>x1 && x<x0)) return true;
  ball.root2_alert.setAttribute("style", "fill:red");

  return false;
}

const FLIPPER_LEFT = 0;
const FLIPPER_RIGHT = 1;

function flipper(x, y, type, initial_angle){
  this.type = type;
  this.x = x;
  this.y = y;
  if (initial_angle)
    this.angle = initial_angle;
  else
    this.angle = 0; //TODO: choose a better default value
}

flipper.prototype.flip = function(){
  //TODO: implement me
}

flipper.prototype.release = function(){
  //TODO: implement me
}

function playfield(w,h,angle){
  this.width = w;
  this.height = h;
  this.angle = 2*3.1415*angle/360.0; //convert to radians

  this.bumpers = [];
  this.flippers = [new flipper(30,30,FLIPPER_LEFT), new flipper(170,30, FLIPPER_RIGHT)];
}

function WebGLRenderer(){
  //init WebGL

  //TODO: implement me
}

WebGLRenderer.prototype.update = function(game){
  //TODO: implement me  
}

const PADDING = 20 //(pixels);

const SVGNS = "http://www.w3.org/2000/svg";
function SVGRenderer(game){
  this.svg = document.getElementsByTagName("svg")[0];
  this.svg.setAttribute("width", 2*PADDING + game.playfield.width*PIXELS_PER_METER );
  this.svg.setAttribute("height", 2*PADDING + game.playfield.height*PIXELS_PER_METER );

  this.playfield_shape = document.createElementNS(SVGNS, "rect");
  this.playfield_shape.setAttribute("style", "fill:#0bf");
  this.playfield_shape.setAttribute("x", PADDING);
  this.playfield_shape.setAttribute("y", PADDING);
  this.playfield_shape.setAttribute("width", game.playfield.width*PIXELS_PER_METER);    
  this.playfield_shape.setAttribute("height", game.playfield.height*PIXELS_PER_METER);    
  this.svg.appendChild(this.playfield_shape);

  this.ball_shape = document.createElementNS(SVGNS, "circle");
  this.ball_shape.setAttribute("style", "fill:grey");
  this.ball_shape.setAttribute("r", game.balls[0].radius*PIXELS_PER_METER);    
  this.svg.appendChild(this.ball_shape);

  var ball = game.balls[0];
  ball.root1_shape = document.createElementNS(SVGNS, "circle");
  ball.root1_shape.setAttribute("style", "fill:green");
  ball.root1_shape.setAttribute("r", (ball.radius*PIXELS_PER_METER)/4);    
  this.svg.appendChild(ball.root1_shape);

  ball.root2_shape = document.createElementNS(SVGNS, "circle");
  ball.root2_shape.setAttribute("style", "fill:red");
  ball.root2_shape.setAttribute("r", (ball.radius*PIXELS_PER_METER)/4);    
  this.svg.appendChild(ball.root2_shape);

  ball.root1_alert = document.createElementNS(SVGNS, "circle");
  ball.root1_alert.setAttribute("r", 10);
  ball.root1_alert.setAttribute("cx", 10);
  ball.root1_alert.setAttribute("cy", 10);    
  this.svg.appendChild(ball.root1_alert);
  ball.root2_alert = document.createElementNS(SVGNS, "circle");
  ball.root2_alert.setAttribute("r", 10);
  ball.root2_alert.setAttribute("cx", 30);
  ball.root2_alert.setAttribute("cy", 10);    
  this.svg.appendChild(ball.root2_alert);
  
  var paths = this.svg.getElementsByTagName("path");
  game.structures = [];
  for (var p in paths){
    if (paths[p].tagName && paths[p].tagName == "path"){
      game.structures.push( new playfieldStructure(paths[p]) );
    }
  }
}

SVGRenderer.prototype.update = function(game){
  //TODO: implement-me

  this.ball_shape.setAttribute("cx", PADDING + game.balls[0].x*PIXELS_PER_METER);
  this.ball_shape.setAttribute("cy", PADDING + game.balls[0].y*PIXELS_PER_METER);
}

const SVG_MODE = 0;
const WEBGL_MODE = 1;

function game(balls_per_credit, rendering_mode){
  this.ball_in_play = 1;
  this.playfield = new playfield(0.6,1.2,0.1); //60cm x 1m20cm with 10 degrees
  this.balls = [new ball(0,0, 0,0)];
  this.time = Date.now();

  switch (rendering_mode){
    case SVG_MODE:
      this.renderer = new SVGRenderer(this);
      break;
    case WEBGL_MODE:
      this.renderer = new WebGLRenderer(this);
      break;
  }

/*
  while(this.ball_in_play <= balls_per_credit){ //TODO: handle extraballs
    this.main_loop();
  }
*/
  var self = this;
  window.setInterval(function(event){self.main_loop(event);}, 100);

  var myball = this.balls[0];
/*
  document.onmousemove = function(e){
    myball.x = e.clientX/PIXELS_PER_METER;
    myball.y = e.clientY/PIXELS_PER_METER;
  }
*/

  myball.x = 1;
  myball.y = 1;

}

game.prototype.main_loop = function(e){
  for (var b in this.balls){
    var ball = this.balls[b];
    for (var s in this.structures){
      var structure = this.structures[s];
      if (structure.hit(ball)){
        //ball.y-=1000;
      }
      ball.root1_shape.setAttribute("data", ball.data);
    }
    this.balls[b].update(this);
  }

  this.renderer.update(this);
}

function init_pinball_simulator(event){
  //TODO: implement classes for the machine with methods for inserting coins and pressing buttons
  var theGame = new game(5, SVG_MODE);
}
