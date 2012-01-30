// just a bit of openscad experimentation
// released to the public domain

d = 10;
z=0;
k=50;
N=5;
max_angle=90;
union(){
	for (a=[0:N]){
		for (b=[0:N]){
			rotate([-max_angle+2*max_angle*(a/N), -max_angle+2*max_angle*(b/N), 0])
			for (i=[1:2*N]){
				translate([0,0,sqrt(i)*k]) sphere(r=k/i);
			}
		}
	}
}
