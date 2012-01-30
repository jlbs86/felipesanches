raio = 12;
module ranhuras() {
  translate([6.7*raio/12, -raio, -.002]) rotate([-90, 0, 0]) cylinder(r=1.2*raio/12, $fn=6, h=2*raio+1);
  translate([12.7*raio/12, -raio, -.002]) rotate([-90, 0, 0]) cylinder(r=1.2*raio/12, $fn=6, h=2*raio+1);
  translate([19.0*raio/12, -raio, -.002]) rotate([-90, 0, 0]) cylinder(r=1.2*raio/12, $fn=6, h=2*raio+1);
}

module ficha(){
  difference() {
    translate([raio,0.2,0])
    cylinder(r=raio, h=2.42*raio/12);
    translate([0, 0, -0.1]) ranhuras();
    translate([-3.3, 0, 2*1.3*raio/12]) ranhuras();
  }
}

translate([-12, 0, 0]) ficha();
