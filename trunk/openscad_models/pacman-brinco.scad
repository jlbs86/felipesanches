$fn=40;

intersection(){
translate([15, 15])
scale([1, 1, 0.5]){
difference(){
	sphere(r=15);
	translate([-15, -15, -30]) cube([30, 30, 30]);
	translate([-15, -15, 14]) cube([30, 30, 30]);
}
}

linear_extrude(height=10) import("pacman.dxf", layer="pacman");
}

linear_extrude(height=2) import("pacman.dxf", layer="argola");
