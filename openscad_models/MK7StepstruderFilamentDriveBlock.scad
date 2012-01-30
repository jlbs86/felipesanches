//import("/home/felipe/Downloads/thingiverse/filament-drive-block.STL");

delta=0.1;
$fn=30;

module MK7_Stepstruder_Filament_Drive_Block(mouse_ears=true){

if(mouse_ears){
	translate([-20.9, -12.9, 0]) cylinder(r=3, h=0.75);
	translate([20.9, -12.9, 0]) cylinder(r=3, h=0.75);	
}

difference(){
	translate([-21, -13.06 ,0]) cube([42, 29, 15]);

	//screw holes
	translate([15.5, -7.5, -delta]) cylinder(r=2, h=15+2*delta);
	translate([-15.5, -7.5, -delta]) cylinder(r=2, h=15+2*delta);

	//screw head bevels
	translate([15.5, -7.5, -delta]) cylinder(r1=4, r2=2, h=2);
	translate([-15.5, -7.5, -delta]) cylinder(r1=4, r2=2, h=2);

	//screw diagonal cuts

	//filament drive holes

	//plunger holes
	translate([-25, 7.9, 5.4]) rotate([0, 90, 0]) cylinder(r=2, h=50);
	translate([-17, 7.9, 5.4]) rotate([0, 90, 0]) cylinder(r=3.8, h=34);

	//pulley hole
	union(){
		translate([0, 8, -delta]) cylinder(r=6.5, h=15+2*delta);
		translate([-6.5, 7.25, -delta]) cube([13, 20, 15+2*delta]);
	}
}
}

MK7_Stepstruder_Filament_Drive_Block();