<html>
  <script>

var linhas=8;
var colunas=8;
var matriz[linhas][colunas];

function calc_color(l,c){
	if ((l+c)%2){
		return "black";
	} else {
		return "yellow";	
	}
}

function on_load(){
	var body = document.getElementsByTagName("body")[0];
	for (var l=0;l<linhas;l++){
		for (var c=0;c<colunas;c++){
			var new_div = document.createElement("div");
			matriz[l][c] = new_div;
			new_div.style.background = calc_color(l,c);
		}
	}

}

  </script>

  <body ondload="load()">
  </body>
</html>

