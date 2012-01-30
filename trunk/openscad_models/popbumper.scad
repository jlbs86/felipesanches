// (c) 2011 Felipe Corrêa da Silva Sanches
//          <fsanches@metamaquina.com.br>
//
// Licensed under the terms of the GNU GPL version 3 or
// (at your option) any later version.

//$t=1;
$fn=50;
m3_diameter = 3.6;
m3_nut_diameter = 5.3;

module nut(d,h,horizontal=true){
cornerdiameter =  (d / 2) / cos (180 / 6);
cylinder(h = h, r = cornerdiameter, $fn = 6);
if(horizontal){
for(i = [1:6]){
	rotate([0,0,60*i]) translate([-cornerdiameter-0.2,0,0]) rotate([0,0,-45]) cube(size = [2,2,h]);
}}
}

center_hole_radius = 6;
screw_radius = 2;
screw_length = 20;
screw_head_radius = 4;
feet_radius = 4;
feet_height = 8;
body_r1 = 16;
body_r2 = 17.5;
body_height = 22;
side_cuts_height = 26;
side_cuts_radius = 6;
connector_height = 6;

diaf = -0.4;
delta = 0.1;

module connector(){
	difference(){
		translate ([0, 0, connector_height/2]) cylinder(h=connector_height/2, r=body_r2);
		translate ([0, 0, connector_height/2-delta]) cylinder(h=connector_height/2+2*delta, r=body_r2-3*screw_radius);

		for (i=[0:1]){
			rotate([0, 0, i*180]){
				translate([0, -connector_height/4, -delta]) cube([2*body_r2,2*body_r2,connector_height+2*delta]);
				translate([body_r2-3*screw_radius-delta, -connector_height/2, connector_height/2]) rotate([-60, 0, 0]) cube([3*screw_radius, connector_height/2, connector_height/2]);
			}
		}
	}

	rotate([0,0,90]) translate([-body_r2+delta, -connector_height/4, 0]) cube([2*body_r2-2*delta,connector_height/2,connector_height]);

	difference(){
		cylinder(h=connector_height, r=body_r2);
		translate([0,0,-delta]) cylinder(h=connector_height+2*delta, r=body_r2-screw_radius);
	}
}

module pop_bumper_old(){
  difference(){
	union(){
		//body
		translate([0, 0, feet_height]) cylinder(h=body_height, r1=body_r1, r2=body_r2);

		//connector
//		translate([0, 0, feet_height+body_height]) connector();	

		//feet
		for (i=[0:1]){
			rotate([0, 0, 45 + 180*i]) translate([body_r1-feet_radius, 0, 0]) cylinder(h=feet_height+1, r=feet_radius);
		}
	}

	//center hole (removing some mass)
	translate([0,0,feet_height-delta]) cylinder(h=body_height+delta-diaf, r1=center_hole_radius, r2=body_r2-2*screw_head_radius);

	//side cuts
	for (i=[0:1]){
		rotate([0, 0, 180*i]) translate([body_r1, 0, 0]) cylinder(h=side_cuts_height, r=side_cuts_radius);
	}

	//screw holes
	for (i=[0:1]){
		rotate([0, 0, 45 + 180*i]){
			translate([body_r1-feet_radius, 0, -delta]) cylinder(h=screw_length+delta, r=screw_radius);
			translate([body_r1-feet_radius, 0, screw_length+diaf]) cylinder(h=feet_height+body_height-screw_length-2*diaf, r=screw_head_radius);
		}
	}
  }
}

wall_thickness = 1;
module pop_bumper(){

	intersection(){
		translate([0, 0, feet_height]) cylinder(h=body_height, r1=body_r1, r2=body_r2);
		
		union(){
			//support for side cuts
			for (i=[0:1]){
				rotate([0, 0, 180*i]){
					difference(){
						translate([body_r1, 0, feet_height]) cylinder(h=(1/3)*body_height, r=side_cuts_radius+wall_thickness);
						translate([body_r1, 0, feet_height-delta/2]) cylinder(h=(1/3)*body_height+delta, r=side_cuts_radius);
						translate([0,0,feet_height+2*wall_thickness-delta/2]) cylinder(h=(1/3)*body_height, r1=center_hole_radius, r2=(2*body_r1 + body_r2)/3);
					}
				}
			}
		}
	}
	

  difference(){
	union(){
		//body
		difference(){
			translate([0, 0, feet_height]) cylinder(h=body_height, r1=body_r1, r2=body_r2);
			translate([0, 0, feet_height+wall_thickness]) cylinder(h=body_height, r1=body_r1-wall_thickness, r2=body_r2-wall_thickness);
		}

		//close the body
		difference(){
			translate([0, 0, feet_height+body_height]) cylinder(r=body_r2, h=2*wall_thickness);
			for (i=[0:1]){
				rotate([0,0,180*i]) translate([body_r2-5, 0, feet_height+body_height-delta]) {
					//hole for m3 nut
					nut(m3_nut_diameter, wall_thickness+2*delta);

					//hole for m3 bolt
					translate([0, 0, wall_thickness]) cylinder(r=m3_radius, h=wall_thickness+2*delta);
				}
			}
		}

		//support for center hole
		difference(){
			union(){
				translate([0,0,feet_height+wall_thickness-delta]) cylinder(h=(1/3)*body_height, r1=center_hole_radius, r2=(2*body_r1 + body_r2)/3);
				translate([0,0,feet_height+wall_thickness-delta + (1/3)*body_height]) cylinder(h=wall_thickness, r=(2*body_r1 + body_r2)/3);
			}
			translate([0,0,feet_height+2*wall_thickness-delta/2]) cylinder(h=(1/3)*body_height, r1=center_hole_radius, r2=(2*body_r1 + body_r2)/3);
		}

		//feet
		for (i=[0:1]){
			rotate([0, 0, 45 + 180*i]) translate([body_r1-feet_radius, 0, 0]) cylinder(h=feet_height+delta, r=feet_radius);
		}
	}

	//center hole
	translate([0,0,feet_height-delta]) cylinder(h=3*wall_thickness, r=center_hole_radius);

	//side cuts
	for (i=[0:1]){
		rotate([0, 0, 180*i]) translate([body_r1, 0, 0]) cylinder(h=side_cuts_height, r=side_cuts_radius);
	}

	//screw holes
	for (i=[0:1]){
		rotate([0, 0, 45 + 180*i]){
			translate([body_r1-feet_radius, 0, -delta]) cylinder(h=feet_height+wall_thickness+delta-diaf, r=screw_radius);
			translate([body_r1-feet_radius, 0, feet_height+wall_thickness]) cylinder(h=body_height+wall_thickness+delta, r=screw_head_radius);
		}
	}
  }
}

cap_r1 = 77/2;
cap_r2 = 44/2;
cap_height = 17;
cap_sphere_radius = 38;
cap_sphere_height = 50;
cap_bevel_height = 2;

num_links=12;
num_internal_links=6;

module pop_bumper_cap(){
union(){

	//links for strengthening the structure
	for (i = [0:num_links]){
		rotate([0, 0, i*360/num_links]) translate([body_r2, 0, 0]) cube([cap_r1-body_r2-delta, cap_bevel_height, cap_bevel_height/2]);
	}

	difference(){

		//cap volume
		union(){
			cylinder(h=cap_bevel_height, r=cap_r1);
			translate([0, 0, cap_bevel_height]) cylinder(h=cap_height, r1=cap_r1, r2=cap_r2);
		}

		//connector
		union(){
			rotate([0,0,80]) translate([0, 0, -delta]) connector();

			intersection(){
				translate([0, 0, -delta]) cylinder(r=body_r2, h=connector_height);
				union(){
					for (i=[0:1]){
						rotate([0, 0, 90+i*180]) translate([0, -connector_height/4, -delta]) cube([2*body_r2,2*body_r2,connector_height+2*delta]);
					}
					translate([0, 0, -delta]) cylinder(r=body_r2/3, h=connector_height);
				}
			}
		}


		//top spherical cut
		translate([0, 0, cap_bevel_height + cap_sphere_height]) sphere(r=cap_sphere_radius);

		//removing some mass
		difference(){
			translate([0, 0, -cap_bevel_height-diaf]) cylinder(h=cap_height, r1=cap_r1, r2=cap_r2);
			translate([0, 0, -delta]) cylinder(h=cap_height+cap_bevel_height, r=body_r2+connector_height/2);
		}

if(1){

		//removing mass from inside
		difference(){
			translate([0, 0, cap_bevel_height + connector_height]) cylinder(r=body_r2, h=cap_height);
			translate([0, 0, cap_bevel_height + connector_height - delta]) cylinder(r=connector_height/2, h=2*delta + cap_height);
			translate([0, 0, cap_bevel_height + cap_sphere_height - cap_bevel_height]) sphere(r=cap_sphere_radius);
			for (i=[1:num_internal_links]){
				rotate([0, 0, i*360/num_internal_links]) cube([cap_r2, cap_bevel_height/2, cap_height]);
			}
		}

}


	}
}
}

pc = 100*$t;
h=((100-pc)/100)*(feet_height+body_height);

rotate([0,0,$t/2*360]){
translate ([0, 0, feet_height+body_height+2*wall_thickness]){
  difference(){

	rotate([180,0,0]) pop_bumper();
	translate ([-100, -100, -h]) cube([200, 200, h+1]);
  }
}
}
//translate([0, 0, body_height+feet_height+50])
//pop_bumper_cap();