lego_unit = 60;
lego_height = 60;
lego_button_radius = 18;
lego_wall_width = lego_unit/2 - lego_button_radius;
lego_button_height = 2*lego_wall_width;
base_pin_radius = lego_wall_width;
base_circle_radius = (lego_unit*sqrt(2) - 2*lego_button_radius)/2;

module lego_brick(brick_length=4, brick_width=2){

union(){
	difference(){
		cube([lego_unit*brick_length, lego_unit*brick_width, lego_height]);

		translate([lego_wall_width, lego_wall_width, -lego_wall_width])
		  cube([lego_unit*brick_length - 2*lego_wall_width, lego_unit*brick_width - 2*lego_wall_width, lego_height]);
	}

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

		if (brick_length > 3){
			for (i = [1:(brick_length/2-1)]) {
				translate([i*2*lego_unit, lego_unit/2, lego_height/2+lego_wall_width/4]) cube([lego_wall_width, lego_unit,lego_height-lego_wall_width/2], center=true);
			}
		}
	} else {
		difference(){
			union(){
				//body of the base circles
				for (i = [1:brick_length-1]) {
					translate([i*lego_unit, lego_unit, lego_height/2])
					difference(){
						cylinder(r=base_circle_radius, h=lego_height, center=true);
					}
				}

				//inner walls
				if (brick_length > 3){
					for (i = [1:(brick_length/2-1)]) {
						translate([i*2*lego_unit, lego_unit, lego_height/2+lego_wall_width/2]) cube([lego_wall_width/4, 2*lego_unit,lego_height-lego_wall_width], center=true);
					}
				}
			}
			
			//holes of the base circles
			for (i = [1:brick_length-1]) {
				translate([i*lego_unit, lego_unit, lego_height/2])
				cylinder(r=lego_button_radius, h=lego_height+1, center=true);
			}

		}

	}
}

}

lego_brick();