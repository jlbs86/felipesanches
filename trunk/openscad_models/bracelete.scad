espessura=2;
raio = 32+espessura;

difference(){
	translate ([0,0,raio/4]) sphere(r=raio);
	translate([-raio, -raio, -raio]) cube([2*raio, 2*raio, raio]);
   translate ([-raio, -raio, raio/2]) cube ([2*raio, 2*raio, raio]);
   translate ([0, 0, -0.1]) cylinder (r=raio -espessura, h=raio);
   
}


