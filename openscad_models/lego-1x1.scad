lego_unit = 60;
lego_height = 80;
lego_button_radius = 18;
lego_wall_width = lego_unit/2 - lego_button_radius;
lego_button_height = 2*lego_wall_width;
base_pin_radius = lego_wall_width;
base_circle_radius = (lego_unit*1.41 - 2*lego_button_radius)/2;

brick_length = 8;
brick_width = 2;

//buttons
for (i = [0:brick_length-1]) {
	for (j = [0:brick_width-1]) {
		translate([lego_unit/2+i*lego_unit, lego_unit/2+j*lego_unit,lego_height+1]) cylinder(r=lego_button_radius,h=lego_button_height-2,center=true);
	}
}

if (brick_width==1){
	if (brick_length>1){
		//base pins
		for (i = [1:brick_length-1]) {
			translate([i*lego_unit, lego_unit/2, lego_height/2]) cylinder(r=base_pin_radius, h=lego_height, center=true);
		}
	}
} else {
	//base circles
	for (i = [1:brick_length-1]) {
		translate([i*lego_unit, lego_unit, lego_height/2])
		difference(){
			cylinder(r=base_circle_radius, h=lego_height, center=true);
			cylinder(r=lego_button_radius, h=lego_height+1, center=true);
		}
	}
}

difference(){
	cube([lego_unit*brick_length, lego_unit*brick_width, lego_height]);

	translate([lego_wall_width, lego_wall_width, -lego_wall_width])
	  cube([lego_unit*brick_length - 2*lego_wall_width, lego_unit*brick_width - 2*lego_wall_width, lego_height]);
}