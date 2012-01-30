// key-chain with the logo of Casa da Cultura Digital
// This openscad script is released to the public domain
// The logo in the DXF file is owned by Casa da Cultura Digital,
// but you can use this script with your own graphics (in a DWF file).
// http://casadeculturadigital.com.br/

linear_extrude(height=3) import("chaveiroCCD.dxf", layer="fundo");
linear_extrude(height=4) import("chaveiroCCD.dxf", layer="argola");
linear_extrude(height=5) import("chaveiroCCD.dxf", layer="desenho");
