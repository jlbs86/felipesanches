// (c) 2012 Felipe Correa da Silva Sanches <fsanches@metamaquina.com.br>
// Licenciado sob GNU GPL v3 (or later)

// Lobster font by Pablo Impallari <http://www.impallari.com/lobster/>

$fn=100;

x=2;
n=25;
altura=3;
altura_42=4;

raio=10;
r2=4;

linear_extrude(height=altura_42) translate([-9, 8.2, 0]) rotate([0, 0, -90]) scale(0.055) import(file="42.dxf");

difference(){
	translate([0, 0, 0]) cylinder(r=raio+x, h=altura);

	for (i=[0:n]){
		rotate([0, 0, i*360/n]) translate([raio, 0, -0.1]) cube([2*x, 1, altura+0.2]);
	}

	translate([0, 0, -0.1]) cylinder(r=10-1, h=altura+0.2);
}

translate([raio-r2, 0, 0]){
	difference(){
		cylinder(r=r2, h=altura);
		translate([0, 0, -0.1]) cylinder(r=r2/2, h=altura+0.2);
	}
}
