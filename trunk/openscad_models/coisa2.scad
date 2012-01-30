// just a bit of openscad experimentation
// released to the public domain

huge=100;
k=19;
R=50;
j=1;
g=1.2;
difference(){
	sphere(r=R);
	sphere(r=R-k/2);

	translate([R/2,0,0]) sphere(r=R-k);
	translate([-R/2,0,0]) sphere(r=R-k);
	translate([0,R/2,0]) sphere(r=R-k);
	translate([0,-R/2,0]) sphere(r=R-k);

	translate([R/g,0,R]) sphere(r=R-j*k);
	translate([-R/g,0,R]) sphere(r=R-j*k);
	translate([0,R/g,R]) sphere(r=R-j*k);
	translate([0,-R/g,R]) sphere(r=R-j*k);

	translate([-huge, -huge, -huge]) cube([2*huge, 2*huge, huge]);
}
