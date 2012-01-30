// (c) 2012 Felipe Correa da Silva Sanches <fsanches@metamaquina.com.br>
// licensed under GPL v3 or (at your option) any later version.

raio_da_mangueira = 7;
raio_do_parafuso = 2.5;

module suporte_para_chuveirinho(){
	difference(){
		union(){
			translate([-1.5*raio_da_mangueira, 1.2*raio_da_mangueira,0]) cube([3*raio_da_mangueira, 0.5*raio_da_mangueira,2*raio_da_mangueira]);
			translate([-1.5*raio_da_mangueira, -1.5*raio_da_mangueira,0]) cube([3*raio_da_mangueira, 3*raio_da_mangueira,raio_da_mangueira]);
			translate([-1.5*raio_da_mangueira -0.8, -1.5*raio_da_mangueira +0.5, 0]) scale(0.4) rotate([90, 0, 0]) linear_extrude(height=3) import (file="GAROA.dxf");
		}

		//furo para a mangueira
		translate([0,0,-5*raio_da_mangueira]) cylinder(r=raio_da_mangueira, h=10*raio_da_mangueira);
		translate([0,-0.7*raio_da_mangueira,-1]) cube([2*raio_da_mangueira, 1.4*raio_da_mangueira, raio_da_mangueira+2]);

		//furos para parafusos
		translate([0.7*raio_da_mangueira,2*raio_da_mangueira,1.5*raio_da_mangueira]) rotate([90,0,0]) cylinder(r=raio_do_parafuso, h=raio_da_mangueira);
		translate([-0.7*raio_da_mangueira,2*raio_da_mangueira,1.5*raio_da_mangueira]) rotate([90,0,0]) cylinder(r=raio_do_parafuso, h=raio_da_mangueira);
	}
}

suporte_para_chuveirinho();
