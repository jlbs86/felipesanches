// key-chain with an image representing the feminist movement
// This openscad script is released to the public domain

union(){
	linear_extrude(height=5) import (file="chaveiro-feminismo-base.dxf");
	linear_extrude(height=10) import (file="chaveiro-feminismo-desenho.dxf");
}
