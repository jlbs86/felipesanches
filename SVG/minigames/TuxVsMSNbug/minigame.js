//Released to the public domain
//original author: Felipe Corrêa da Silva Sanches <juca@members.fsf.org>

var svgDocument;
var sprites;
var NUM_SPRITES;

var butterfly = new Array()
var hit;
var miss;
var time = 0;

var delta_t = 50; //frequency = 1/50ms = 20Hz

function on_load (evt){
	sprites = new Array();

	O=evt.target;
	svgDocument=O.ownerDocument;

	svgDocument.onkeydown = keydown;
	svgDocument.onkeyup = keyup;

	svgDocument.getElementById("start_button").onclick = start;
	svgDocument.getElementById("quit_button").onclick = game_over;
	svgDocument.getElementById("pause_button").onclick = pause;
	svgDocument.getElementById("rules_button").onclick = show_rules;

	svgDocument.getElementById("right_button").onclick = tux_right;
	svgDocument.getElementById("left_button").onclick = tux_left;
	svgDocument.getElementById("action_button").onmousedown = tux_hit;
	svgDocument.getElementById("action_button").onmouseup = tux_wing_down;
	svgDocument.getElementById("OK").onclick = hide_rules;

	sprites.push(svgDocument.getElementById("tuxA"));
	sprites.push(svgDocument.getElementById("downA"));

	sprites.push(svgDocument.getElementById("tuxB"));
	sprites.push(svgDocument.getElementById("downB"));

	sprites.push(svgDocument.getElementById("tuxC"));
	sprites.push(svgDocument.getElementById("downC"));

	sprites.push(svgDocument.getElementById("tuxD"));
	sprites.push(svgDocument.getElementById("downD"));

	sprites.push(svgDocument.getElementById("tuxE"));
	sprites.push(svgDocument.getElementById("downE"));

	sprites.push(svgDocument.getElementById("msn1A"));
	sprites.push(svgDocument.getElementById("msn2A"));
	sprites.push(svgDocument.getElementById("msn3A"));
	sprites.push(svgDocument.getElementById("msn4A"));

	sprites.push(svgDocument.getElementById("msn1B"));
	sprites.push(svgDocument.getElementById("msn2B"));
	sprites.push(svgDocument.getElementById("msn3B"));
	sprites.push(svgDocument.getElementById("msn4B"));

	sprites.push(svgDocument.getElementById("msn1C"));
	sprites.push(svgDocument.getElementById("msn2C"));
	sprites.push(svgDocument.getElementById("msn3C"));
	sprites.push(svgDocument.getElementById("msn4C"));

	sprites.push(svgDocument.getElementById("msn1D"));
	sprites.push(svgDocument.getElementById("msn2D"));
	sprites.push(svgDocument.getElementById("msn3D"));
	sprites.push(svgDocument.getElementById("msn4D"));

	sprites.push(svgDocument.getElementById("msn1E"));
	sprites.push(svgDocument.getElementById("msn2E"));
	sprites.push(svgDocument.getElementById("msn3E"));
	sprites.push(svgDocument.getElementById("msn4E"));

	sprites.push(svgDocument.getElementById("upA"));
	sprites.push(svgDocument.getElementById("upB"));
	sprites.push(svgDocument.getElementById("upC"));
	sprites.push(svgDocument.getElementById("upD"));
	sprites.push(svgDocument.getElementById("upE"));

	sprites.push(svgDocument.getElementById("missA"));
	sprites.push(svgDocument.getElementById("missB"));
	sprites.push(svgDocument.getElementById("missC"));
	sprites.push(svgDocument.getElementById("missD"));
	sprites.push(svgDocument.getElementById("missE"));

	sprites.push(svgDocument.getElementById("hitA"));
	sprites.push(svgDocument.getElementById("hitB"));
	sprites.push(svgDocument.getElementById("hitC"));
	sprites.push(svgDocument.getElementById("hitD"));
	sprites.push(svgDocument.getElementById("hitE"));


        sprites.push(svgDocument.getElementById("share_label"));

	for (i=1;i<=23;i++){
		sprites.push(svgDocument.getElementById("gnu-share-"+i));
	}

	sprites.push(svgDocument.getElementById("gnu"));
	sprites.push(svgDocument.getElementById("win"));

	NUM_SPRITES=48+23;
	window.setInterval(game_timer, delta_t);
	turn_off_by_id("rules")
	turn_off_by_id("loading");
}

var game_is_running = false;
function game_timer(){
	if (game_is_running)
		game_loop();
	else
		sequential_light();
		//random_light();
}

function show_rules(){
	turn_on_by_id("rules");
}

function hide_rules(){
	turn_off_by_id("rules");
}

var count_ticks = 0;
var probability = 0.1;
var ticks_per_level = new Array();

var is_paused = false;
function pause(){
	if (!game_is_running) return;
	if (is_paused){
		is_paused = false;
		turn_off_by_id("paused");
	} else {
		is_paused = true;
		turn_on_by_id("paused");
	}
}

(function() {

var base64EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

function base64encode(str) {
    var out, i, len;
    var c1, c2, c3;

    len = str.length;
    i = 0;
    out = "";
    while(i < len) {
	c1 = str.charCodeAt(i++) & 0xff;
	if(i == len)
	{
	    out += base64EncodeChars.charAt(c1 >> 2);
	    out += base64EncodeChars.charAt((c1 & 0x3) << 4);
	    out += "==";
	    break;
	}
	c2 = str.charCodeAt(i++);
	if(i == len)
	{
	    out += base64EncodeChars.charAt(c1 >> 2);
	    out += base64EncodeChars.charAt(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4));
	    out += base64EncodeChars.charAt((c2 & 0xF) << 2);
	    out += "=";
	    break;
	}
	c3 = str.charCodeAt(i++);
	out += base64EncodeChars.charAt(c1 >> 2);
	out += base64EncodeChars.charAt(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4));
	out += base64EncodeChars.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >>6));
	out += base64EncodeChars.charAt(c3 & 0x3F);
    }
    return out;
}

if (!window.base64encode) window.base64encode = base64encode;

})();

var sampleRate = 44100;

function encodeAudio8bit(data) {
  var n = data.length;
  var integer = 0, i;
  
  // 8-bit mono WAVE header template
  var header = "RIFF<##>WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00<##><##>\x01\x00\x08\x00data<##>";

  // Helper to insert a 32-bit little endian int.
  function insertLong(value) {
    var bytes = "";
    for (i = 0; i < 4; ++i) {
      bytes += String.fromCharCode(value % 256);
      value = Math.floor(value / 256);
    }
    header = header.replace('<##>', bytes);
  }

  // ChunkSize
  insertLong(36 + n);
  
  // SampleRate
  insertLong(sampleRate);

  // ByteRate
  insertLong(sampleRate);

  // Subchunk2Size
  insertLong(n);
  
  // Output sound data
  for (var i = 0; i < n; ++i) {
    header += String.fromCharCode(data[i] * 255);
  }
  
  return 'data:audio/wav;base64,' + base64encode(header);
}

function new_tone(n) {
    var audio = new Audio();
    var samples = [];
    for (var i=0;i<sampleRate/30;i++){
        samples.push( i%(n*50) > (n*25) ? 0 : 1);
    }

    audio.setAttribute("src",encodeAudio8bit(samples));

    audio.load();
    audio.autoplay = false;
    return function() {audio.play();};
}

window.boop = new_tone(1);
window.beep = new_tone(2);

function game_loop(){
	if(is_paused) return;

	count_ticks++;
	if (count_ticks%(Math.floor(1000/delta_t))==0){
		time--;
		if (time==0) game_over();
	}

	if (count_ticks%(ticks_per_level[level-1])==0){
        boop();
		for (i=0;i<5;i++){
			//count buterflies that were missed (not slapped by tux)
			if (butterfly[4][i]==1)	miss++;

			//Scroll down the butterflies:
			for (j=4;j>0;j--){
				butterfly[j][i]=butterfly[j-1][i];
			}
			
			if (Math.random() < probability)
				butterfly[0][i]=1;
			else
				butterfly[0][i]=0;
		}

		for (i=0;i<5;i++){
			for (j=4;j>0;j--){
				if (butterfly[j][i]==1)
					turn_sprite_on("msn"+j, i);
				else
					turn_sprite_off("msn"+j, i);
			}
		}
	}

	//update market share bar
	//  and blink GNU and MS-Windows Logos in frequencies also indicating the
	//  size of their market share
	display_share();
	display_time();
}

function game_over(){
	game_is_running=false;
	turn_on_by_id("game-over");
}

function init_game(){
	ticks_per_level[0]=20;
	ticks_per_level[1]=15;
	ticks_per_level[2]=13;
	ticks_per_level[3]=12;
	ticks_per_level[4]=11;
	ticks_per_level[5]=10;
	ticks_per_level[6]=9;
	ticks_per_level[7]=8;
	ticks_per_level[8]=7;

	for (i=0;i<5;i++){
		butterfly.push(new Array());
		for (j=0;j<5;j++){
			butterfly[i][j]=0;
		}
	}
	
	set_score(0);
	set_level(1);

	//we start with 5% of a gnu/Linux market share
	// and the player has to defeat by slapping as much msn butterflies as she can :-)	
	//And yeah! A missed one costs you the same you gain from 5 good hits. Life is not easy for the Free Software Movement...

	share_k = 5
	hit = 0.5 * share_k;
	miss = 10;

	position = 2;
	game_is_running = true;
	is_paused = false;
	time = 4 * 60; //four minutes to save the world :-D TODO: change it to 2 minutes and add 'bonus times' rule
	clear_sprites();
}

function turn_on_by_id(id){
	svgDocument.getElementById(id).setAttribute("visibility", "visible");
}

function turn_off_by_id(id){
	svgDocument.getElementById(id).setAttribute("visibility", "hidden");
}

function set_digit(id, val){
	switch(val){
		case 0:
		turn_on_by_id(id+1);
		turn_on_by_id(id+2);
		turn_on_by_id(id+3);
		turn_off_by_id(id+4);
		turn_on_by_id(id+5);
		turn_on_by_id(id+6);
		turn_on_by_id(id+7);
		break;
		case 1:
		turn_off_by_id(id+1);
		turn_off_by_id(id+2);
		turn_on_by_id(id+3);
		turn_off_by_id(id+4);
		turn_off_by_id(id+5);
		turn_on_by_id(id+6);
		turn_off_by_id(id+7);
		break;
		case 2:
		turn_on_by_id(id+1);
		turn_off_by_id(id+2);
		turn_on_by_id(id+3);
		turn_on_by_id(id+4);
		turn_on_by_id(id+5);
		turn_off_by_id(id+6);
		turn_on_by_id(id+7);
		break;
		case 3:
		turn_on_by_id(id+1);
		turn_off_by_id(id+2);
		turn_on_by_id(id+3);
		turn_on_by_id(id+4);
		turn_off_by_id(id+5);
		turn_on_by_id(id+6);
		turn_on_by_id(id+7);
		break;
		case 4:
		turn_off_by_id(id+1);
		turn_on_by_id(id+2);
		turn_on_by_id(id+3);
		turn_on_by_id(id+4);
		turn_off_by_id(id+5);
		turn_on_by_id(id+6);
		turn_off_by_id(id+7);
		break;
		case 5:
		turn_on_by_id(id+1);
		turn_on_by_id(id+2);
		turn_off_by_id(id+3);
		turn_on_by_id(id+4);
		turn_off_by_id(id+5);
		turn_on_by_id(id+6);
		turn_on_by_id(id+7);
		break;
		case 6:
		turn_on_by_id(id+1);
		turn_on_by_id(id+2);
		turn_off_by_id(id+3);
		turn_on_by_id(id+4);
		turn_on_by_id(id+5);
		turn_on_by_id(id+6);
		turn_on_by_id(id+7);
		break;
		case 7:
		turn_on_by_id(id+1);
		turn_off_by_id(id+2);
		turn_on_by_id(id+3);
		turn_off_by_id(id+4);
		turn_off_by_id(id+5);
		turn_on_by_id(id+6);
		turn_off_by_id(id+7);
		break;
		case 8:
		turn_on_by_id(id+1);
		turn_on_by_id(id+2);
		turn_on_by_id(id+3);
		turn_on_by_id(id+4);
		turn_on_by_id(id+5);
		turn_on_by_id(id+6);
		turn_on_by_id(id+7);
		break;
		case 9:
		turn_on_by_id(id+1);
		turn_on_by_id(id+2);
		turn_on_by_id(id+3);
		turn_on_by_id(id+4);
		turn_off_by_id(id+5);
		turn_on_by_id(id+6);
		turn_on_by_id(id+7);
		break;
		case 10: //means void
		turn_off_by_id(id+1);
		turn_off_by_id(id+2);
		turn_off_by_id(id+3);
		turn_off_by_id(id+4);
		turn_off_by_id(id+5);
		turn_off_by_id(id+6);
		turn_off_by_id(id+7);
		break;

	}
}

var share_k;
//FLASH = 10;
function display_share(){
	gnu_share = hit/(hit+share_k*miss);

	//Market share bar:
	for (i=1;i<=23;i++){
		if (i<23*gnu_share)
			turn_on_by_id("gnu-share-"+i);
		else
			turn_off_by_id("gnu-share-"+i);
	}


	set_digit("MS1_", Math.floor(10*gnu_share));
	set_digit("MS0_", Math.floor(100*gnu_share)%10);


/*
	//Blinking GNU logo
	if (count_ticks%(Math.floor(FLASH * gnu_share))==0)
		turn_on_by_id("gnu");
	else
		turn_off_by_id("gnu");

	//Blinking MS-Windows(r) logo
	if (count_ticks%(Math.floor(FLASH*(1 - gnu_share)))==0)
		turn_on_by_id("win");
	else
		turn_off_by_id("win");
*/
		
}

function display_time(){
	set_digit("TMin1_", Math.floor(time/600)%10);
	set_digit("TMin0_", Math.floor(time/60)%10);

	set_digit("TSec1_", Math.floor(time/10)%6);
	set_digit("TSec0_", Math.floor(time%10));
}

POINTS_NEEDED_IN_ORDER_TO_INCREASE_LEVEL = 50

var score;
function set_score(val){
	if (Math.floor(val / (level * POINTS_NEEDED_IN_ORDER_TO_INCREASE_LEVEL)) != 
		Math.floor(score / (level * POINTS_NEEDED_IN_ORDER_TO_INCREASE_LEVEL)) && level <9)
		set_level(level+1);

	score = val;
	
	var i=0;
	while(i < 5){
		if (val==0 && i > 0) set_digit("S"+i+"_", 10);
		else set_digit("S"+i+"_", val%10);
		val = Math.floor(val/10);
		i++;
	}
}

var level;
function set_level(n){
	level = n;
	set_digit("L", n%10);
}

function clear_sprites(){
	for (i=0;i<NUM_SPRITES;i++){
		turn_off(i);
	}
	turn_sprite_on("tux", position);
	turn_sprite_on("down", position);
	turn_on_by_id("share_label");
	turn_on_by_id("gnu");
	turn_on_by_id("win");
	turn_off_by_id("game-over");
	turn_off_by_id("paused");
}

function turn_sprite_on(id, i){
//	O=event.target;
//	svgDocument=O.ownerDocument;
	switch(i){
		case 0: i="A"; break;
		case 1: i="B"; break;
		case 2: i="C"; break;
		case 3: i="D"; break;
		case 4: i="E"; break;
	}

	turn_on_by_id(id+i);
}

function turn_sprite_off(id, i){
//	O=event.target;
//	svgDocument=O.ownerDocument;
	switch(i){
		case 0: i="A"; break;
		case 1: i="B"; break;
		case 2: i="C"; break;
		case 3: i="D"; break;
		case 4: i="E"; break;
	}

	turn_off_by_id(id+i)
}

function turn_on(i){
	if (sprites[i]){
		sprites[parseInt(i)].setAttribute("visibility", "visible");
	}
}

function turn_off(i){
	if (sprites[i])
		sprites[parseInt(i)].setAttribute("visibility", "hidden");
}


function random_light(){
	for (i=0;i<20;i++){
		turn_on(Math.floor(Math.random()*NUM_SPRITES));
		turn_off(Math.floor(Math.random()*NUM_SPRITES));
	}
}

var current_lamp = 0;
function sequential_light(){
	turn_on(current_lamp%NUM_SPRITES);
	turn_off((current_lamp + Math.floor(NUM_SPRITES/2))%NUM_SPRITES);
	current_lamp=(current_lamp+1)%NUM_SPRITES;
}

var position = 2;
function tux_right(){
	if (is_paused || !game_is_running) return;
	tux_wing_down();
	if (position < 4){
		turn_sprite_off("tux", position);
		turn_sprite_off("down", position);
		position++;
		turn_sprite_on("tux", position);
		turn_sprite_on("down", position);
	}
}


function tux_left(){
	if (is_paused || !game_is_running) return;
	tux_wing_down();
	if (position > 0){
		turn_sprite_off("tux", position);
		turn_sprite_off("down", position);
		position--;
		turn_sprite_on("tux", position);
		turn_sprite_on("down", position);
	}
}

function tux_hit(){
	if (is_paused || !game_is_running) return;
	turn_sprite_off("down", position);
	turn_sprite_on("up", position);
	if (butterfly[4][position]){
		turn_sprite_on("hit", position);
		set_score(score+level);
		hit++;
        beep();
	} else {
		turn_sprite_on("miss", position);
        boop();
	}
}

function tux_wing_down(){
	if (is_paused || !game_is_running) return;
	turn_sprite_on("down", position);
	turn_sprite_off("up", position);
	turn_sprite_off("hit", position);
	turn_sprite_off("miss", position);
	if (butterfly[4][position]){
		butterfly[4][position]=0;
		turn_sprite_off("msn4", position);
	}
}

function start(){
		if (game_is_running == false){
			init_game();
		}
}

RIGHT_KEY = 39
LEFT_KEY = 37
SPACEBAR_KEY = 32
ENTER_KEY = 13
PAUSE_KEY = 19
H_KEY = 72
P_KEY = 80
Q_KEY = 81
R_KEY = 82
S_KEY = 83
ESC_KEY = 27

function keydown(event){
	O=event.target;
	svgDocument=O.ownerDocument;
	switch(event.which){
		case LEFT_KEY:
			tux_left();
			break;
		case RIGHT_KEY:
			tux_right();
			break;
		case ENTER_KEY:
		case S_KEY:
			start();
			break;
		case PAUSE_KEY:
		case P_KEY:
			pause();
			break;
		case R_KEY:
			show_rules();
			break;
		case SPACEBAR_KEY:
		case H_KEY:
			tux_hit();
			break;
		case ESC_KEY:
		case Q_KEY:
			game_over();
//		default:
//			alert(event.which)
	}
}

function keyup(event){
	O=event.target;
	svgDocument=O.ownerDocument;
	switch(event.which){
		case SPACEBAR_KEY:
			tux_wing_down();
			break;
	}
}

