// key-chain with the logo of Garoa Hacker Clube
// This openscad script is released to the public domain
// The logo in the DXF file is owned by GaroaHackerClube, but you can use this script
// with your own graphics (in a DWF file).
// http://garoa.net.br/

difference(){
	linear_extrude(height=3) import("logo_garoa.dxf", layer="base");
	translate([0, 0, 2]) linear_extrude(height=5) import("logo_garoa.dxf", layer="bolinhas");
}

difference(){
	linear_extrude(height=5) import("logo_garoa.dxf", layer="guardachuva");
	translate([0, 0, 3]) linear_extrude(height=5) import("logo_garoa.dxf", layer="texto");
}
