// (c) 2012 Felipe Correa da Silva Sanches <fsanches@metamaquina.com.br>
// licensed under GPL v3 or (at your option) any later version.

$fn=60;
furo_r1=2;
furo_r2=3;
raio_ext=6;
distancia=20; //entre furos
espessura=3;

difference(){
union(){
 translate([raio_ext, 0]) cube([distancia, raio_ext * (1+1/sqrt(2)) + distancia, espessura]);
 translate([0, raio_ext]) cube([(1+1/sqrt(2))*raio_ext + distancia, distancia, espessura]);

 translate([raio_ext, raio_ext]) cylinder(r=raio_ext, h=espessura);
 translate([raio_ext+distancia, raio_ext]) cylinder(r=raio_ext, h=espessura);
 translate([raio_ext, raio_ext+distancia]) cylinder(r=raio_ext, h=espessura);
}


translate([2*raio_ext+distancia+raio_ext/sqrt(2), raio_ext/sqrt(2), -0.1]) rotate([0, 0, 45]) cube([distancia*sqrt(2) + 2*raio_ext, 100, espessura+0.2]);

 translate([raio_ext, raio_ext, -0.1]) cylinder(r1=furo_r1, r2=furo_r2, h=espessura+0.2);
 translate([raio_ext+distancia, raio_ext, -0.1]) cylinder(r1=furo_r2, r2=furo_r1, h=espessura+0.2);
 translate([raio_ext, raio_ext+distancia, -0.1]) cylinder(r1=furo_r1, r2=furo_r2, h=espessura+0.2);

}