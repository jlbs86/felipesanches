largura = 1;
distancia=1;
espessura = 3;
n=4;

module dentes(n){
	for (i=[0:n-1]){
		translate([(largura+distancia)*i, 0, 3]) cube();
		translate([(largura+distancia)*(i+0.5), 0, 1]) cube();
	}
}

cube([2*(n+0.5)*largura, espessura, largura]);
translate([largura*n*2, 0, largura*2]) cube([3*largura, espessura, 2*largura]);
translate([largura*n*2, 0, largura*1]) cube([2*largura, espessura, largura]);
translate([0, 0, largura*4]) cube([2*(n+1)*largura, espessura, largura]);

dentes(n);
translate([0, 2*largura, 0]) dentes(n);