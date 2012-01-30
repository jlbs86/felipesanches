// re-implementation of the RepRap Wade extruder's large gear
// done as a coding-dojo exercise
// at the free software studies group of the engineering school
// of the University of São Paulo http://www.polignu.org

// This model is released to the public domain

r_corpo=25;
h_corpo=5;

r_2=10;
h_2=7;

r_3=4;
h_3=10;

r_gota=4;
h_gota=7;
t_gota=16;

xc=12;
yc=7;
zc=3;

largura_borda=r_gota;
tamanho_dente=r_gota/2;
num_dentes=50;

difference (){
	
	union () {
		difference() {
			cylinder (r=r_corpo+tamanho_dente/2, h=h_corpo);
			translate ([0,0,h_corpo*0.8])
			cylinder (r=r_corpo-largura_borda, h=h_corpo*0.2+0.1);
			
		}
		cylinder (r=r_2, h=h_2);
	}

	translate([0,0,-1])
	cylinder (r=r_3, h=h_3);
	for (i=[0:6]){
		rotate ([0, 0, i*360/7])
		translate ([t_gota,0,-1]){
			cylinder (r=r_gota, h=h_gota);
			//translate([0,0,0])
			rotate([0,0,2*r_gota])
			cube ([r_gota, r_gota, h_gota]);
			
		}
	}

	for(i=[0:3]){
		rotate([0,0,i*360/3])
		translate([-xc/2,-yc/2,h_2-zc+0.1])
		cube([xc,yc,zc]);
	}

   // dentes
	for (i=[0:num_dentes]){
		rotate ([0,0,i*360/num_dentes])
		translate([-r_corpo-0.1,0,-0.1]) {
			cylinder ($fn=3,r=tamanho_dente, h=h_3);    
     }
	}
}
