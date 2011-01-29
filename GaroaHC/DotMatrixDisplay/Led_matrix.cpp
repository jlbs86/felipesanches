/***********************************************************************
 * 	Arduino lib for Holtek HT1632 LED driver chip,
 *            As implemented on the Sure Electronics DE-DP016 display board
 *            (16*24 dot matrix LED module.)
 *
 *   Nov, 2008 Bill Westfield ("WestfW")
 *		original code
 *   Dec, 2008 ("Ced2911")
 *		transformed it into a lib
 *
 *   Copyrighted and distributed under the terms of the Berkely license
 *   (copy freely, but include this notice of original author.)
 ***********************************************************************/


#include "Led_matrix.h"

matrix::matrix (){}

void matrix::setCS(int cs){
  pin_cs = cs;
}

void matrix::setData(int data){
  pin_data = data;
}

void matrix::setWrite(int wr){
  pin_wr = wr;
}
        
void matrix::setup()
{
	pinMode(pin_cs, OUTPUT);
	digitalWrite(pin_cs, HIGH); 	/* unselect (active low) */
	pinMode(pin_wr, OUTPUT);
	pinMode(pin_data, OUTPUT);

	//setup
	sendcmd(HT1632_CMD_SYSDIS);  // Disable system
	sendcmd(HT1632_CMD_COMS11);  // 16*32, PMOS drivers
	sendcmd(HT1632_CMD_MSTMD); 	/* Master Mode */
	sendcmd(HT1632_CMD_SYSON); 	/* System on */
	sendcmd(HT1632_CMD_LEDON); 	/* LEDs on */
	
	clear();

	//wait
	//delay(1000);

}

void matrix::chipselect(byte chipno)
{
  digitalWrite(chipno, 0);
}

void matrix::chipfree(byte chipno)
{
  digitalWrite(chipno, 1);
}

void matrix::writebits (byte bits, byte firstbit)
{
  DEBUGPRINT(" ");
  while (firstbit) {
    DEBUGPRINT((bits&firstbit ? "1" : "0"));
    digitalWrite(pin_wr, LOW);
    if (bits & firstbit) {
      digitalWrite(pin_data, HIGH);
    }
    else {
      digitalWrite(pin_data, LOW);
    }
    digitalWrite(pin_wr, HIGH);
    firstbit >>= 1;
  }
}

void matrix::sendcmd (byte command)
{
  chipselect(pin_cs);  				// Select chip
  writebits(HT1632_ID_CMD, 1<<2); 	// send 3 bits of id: COMMAND
  writebits(command, 1<<7);  		// send the actual command
  writebits(0, 1); 					/* one extra dont-care bit in commands. */
  chipfree(pin_cs); 				// done
}

void matrix::senddata (byte address, byte data)
{
  chipselect(pin_cs);  				// Select chip
  writebits(HT1632_ID_WR, 1<<2);  	// send ID: WRITE to RAM
  writebits(address, 1<<6); 		// Send address
  writebits(data, 1<<3); 			// send 4 bits of data
  chipfree(pin_cs); 				// done
}


void matrix::clear()
{
	char i;

	chipselect(pin_cs);  // Select chip
	writebits(HT1632_ID_WR, 1<<2);  // send ID: WRITE to RAM
	writebits(0, 1<<6); // Send address
	for (i = 0; i < 96/2; i++) // Clear entire display
		writebits(0, 1<<7); // send 8 bits of data
	chipfree(pin_cs); // done
	for (i=0; i < 96; i++)
		ht1632_shadowram[i] = 0;
} 

void matrix::plot (char x, char y, char val)
{
	char addr, bitval;
	bitval = 8>>(y&3);  // compute which bit will need set
	addr = (x<<2) + (y>>2);  // compute which memory word this is in
	if (val) {  // Modify the shadow memory
		ht1632_shadowram[addr] |= bitval;
	}
	else {
		ht1632_shadowram[addr] &= ~bitval;
	}
	// Now copy the new memory value to the display
	senddata(addr, ht1632_shadowram[addr]);
}

void matrix::DrawLine(byte x1, byte y1,
unsigned char x2, unsigned char y2,
unsigned char val )
{
  char deltax = abs(x2 - x1);        // The difference between the x's
  char deltay = abs(y2 - y1);        // The difference between the y's
  char x = x1;                       // Start x off at the first pixel
  char y = y1;                       // Start y off at the first pixel
  char xinc1, xinc2, yinc1, yinc2, den, num, numadd, numpixels, curpixel;

  if (x2 >= x1) {                // The x-values are increasing
    xinc1 = 1;
    xinc2 = 1;
  }  
  else {                          // The x-values are decreasing
    xinc1 = -1;
    xinc2 = -1;
  }

  if (y2 >= y1)                 // The y-values are increasing
  {
    yinc1 = 1;
    yinc2 = 1;
  }
  else                          // The y-values are decreasing
  {
    yinc1 = -1;
    yinc2 = -1;
  }

  if (deltax >= deltay)         // There is at least one x-value for every y-value
  {
    xinc1 = 0;                  // Don't change the x when numerator >= denominator
    yinc2 = 0;                  // Don't change the y for every iteration
    den = deltax;
    num = deltax / 2;
    numadd = deltay;
    numpixels = deltax;         // There are more x-values than y-values
  }
  else                          // There is at least one y-value for every x-value
  {
    xinc2 = 0;                  // Don't change the x for every iteration
    yinc1 = 0;                  // Don't change the y when numerator >= denominator
    den = deltay;
    num = deltay / 2;
    numadd = deltax;
    numpixels = deltay;         // There are more y-values than x-values
  }

  for (curpixel = 0; curpixel <= numpixels; curpixel++)
  {
    //plot(x, y, val);             // Draw the current pixel
	ShadowPlot(x,y);
    num += numadd;              // Increase the numerator by the top of the fraction
    if (num >= den)             // Check if numerator >= denominator
    {
      num -= den;               // Calculate the new numerator value
      x += xinc1;               // Change the x as appropriate
      y += yinc1;               // Change the y as appropriate
    }
    x += xinc2;                 // Change the x as appropriate
    y += yinc2;                 // Change the y as appropriate
  }
}


void matrix::start()
{
	chipselect(pin_cs);  // Select chip
	writebits(HT1632_ID_WR, 1<<2);  // send ID: WRITE to RAM
	writebits(0, 1<<6); // Send address
}

void matrix::finish()
{
	chipfree(pin_cs); 				// done
}

void matrix::ShadowPlot(int x,int y)
{
	int dy=y/(4);
	int dx=x*(16/4)+dy;
	int sy=8>>(y%4);
	ht1632_shadowram[dx]+=sy;
}

//clear the Shadow array (ie: for next display)
void matrix::ClearShadow()
{
	for (int i=0; i < 96; i++)
    ht1632_shadowram[i] = 0;
}

void matrix::ShadowDsp()
{
	start();
	//Draw shadow
	int i;
	for(i=0;i<96;i++)
	{	
		writebits((ht1632_shadowram[i]), 1<<3);
	}
	finish();
	//Blank the shadow array
	ClearShadow();
}



//return the width of a letter
int matrix::DrawCharEx(char letter,int Dx,int Dy)
{
	byte col[6];
	int letter_len=0;
	int max_letter=6;
	
	switch (letter) 
	{
		case 'a': case 'A':
			col[0]= 0b1111100;
			col[1]=	0b0010110;
			col[2]=	0b0010011;
			col[3]=	0b0010011;
			col[4]=	0b0010110;
			col[5]=	0b1111100;
			letter_len=6;
			break;
		
		case 'b': case 'B':
			col[0]= 0b1111111;
			col[1]=	0b1001001;
			col[2]=	0b1001001;
			col[3]=	0b1001001;
			col[4]=	0b0101010;
			col[5]=	0b0010100;
			letter_len=6;
			break;
			
		case 'c': case 'C':
			col[0]= 0b0011100;
			col[1]=	0b0100010;
			col[2]=	0b1000001;
			col[3]=	0b1000001;
			col[4]=	0b1000001;
			col[5]=	0b1000001;
			letter_len=6;
			break;
		
		case 'd': case 'D':
			col[0]= 0b1111111;
			col[1]=	0b1000001;
			col[2]=	0b1000001;
			col[3]=	0b1000001;
			col[4]=	0b0100010;
			col[5]=	0b0011100;
			letter_len=6;
			break;
			
		case 'e': case 'E':
			col[0]= 0b1111111;
			col[1]=	0b1001001;
			col[2]=	0b1001001;
			col[3]=	0b1001001;
			col[4]=	0b1001001;
			col[5]=	0b1001001;
			letter_len=6;
			break;
		
					
		case 'f': case 'F':
			col[0]= 0b1111111;
			col[1]=	0b0001001;
			col[2]=	0b0001001;
			col[3]=	0b0001001;
			col[4]=	0b0001001;
			col[5]=	0b0001001;
			letter_len=6;
			break;	
		
		case 'g': case 'G':
			col[0]= 0b0011100;
			col[1]=	0b0100010;
			col[2]=	0b1000001;
			col[3]=	0b1001001;
			col[4]=	0b1001001;
			col[5]=	0b1111001;
			letter_len=6;
			break;		
				
		case 'h': case 'H':
			col[0]= 0b1111111;
			col[1]=	0b0001000;
			col[2]=	0b0001000;
			col[3]=	0b0001000;
			col[4]=	0b0001000;
			col[5]=	0b1111111;
			letter_len=6;
			break;		
					
		case 'i': case 'I':
			col[0]= 0b0000000;
			col[1]=	0b0000000;
			col[2]=	0b1111111;
			col[3]=	0b0000000;
			col[4]=	0b0000000;
			col[5]=	0b0000000;
			letter_len=6;
			break;		
					
		case 'j': case 'J':
			col[0]= 0b0011000;
			col[1]=	0b0100000;
			col[2]=	0b1000000;
			col[3]=	0b0111111;
			col[4]=	0b0000000;
			col[5]=	0b0000000;
			letter_len=6;
			break;	
			
		case 'k': case 'K':
			col[0]= 0b1111111;
			col[1]=	0b0001000;
			col[2]=	0b0001000;
			col[3]=	0b0010100;
			col[4]=	0b0100010;
			col[5]=	0b1000001;
			letter_len=6;
			break;		
					
		case 'l': case 'L':
			col[0]= 0b0000000;
			col[1]=	0b0000000;
			col[2]=	0b1111111;
			col[3]=	0b1000000;
			col[4]=	0b1000000;
			col[5]=	0b0000000;
			letter_len=6;
			break;	
			
		case 'm': case 'M':
			col[0]= 0b1111111;
			col[1]=	0b0000010;
			col[2]=	0b0000100;
			col[3]=	0b0000100;
			col[4]=	0b0000010;
			col[5]=	0b1111111;
			letter_len=6;
			break;		
					
		case 'n': case 'N':
			col[0]= 0b1111111;
			col[1]=	0b0000010;
			col[2]=	0b0000100;
			col[3]=	0b0001000;
			col[4]=	0b0010000;
			col[5]=	0b1111111;
			letter_len=6;
			break;		
		
		case 'o': case 'O':
			col[0]= 0b0011100;
			col[1]=	0b0100010;
			col[2]=	0b1000001;
			col[3]=	0b1000001;
			col[4]=	0b0100010;
			col[5]=	0b0011100;
			letter_len=6;
			break;		
					
		case 'p': case 'P':
			col[0]= 0b1111111;
			col[1]=	0b0010001;
			col[2]=	0b0010001;
			col[3]=	0b0010001;
			col[4]=	0b0010010;
			col[5]=	0b0001100;
			letter_len=6;
			break;	
		
		case 'q': case 'Q':
			col[0]= 0b0011100;
			col[1]=	0b0100010;
			col[2]=	0b1000001;
			col[3]=	0b1010001;
			col[4]=	0b0100010;
			col[5]=	0b1011100;
			letter_len=6;
			break;		
					
		case 'r': case 'R':
			col[0]= 0b1111111;
			col[1]=	0b0001001;
			col[2]=	0b0001001;
			col[3]=	0b0011001;
			col[4]=	0b0101010;
			col[5]=	0b1000100;
			letter_len=6;
			break;	

		case 's': case 'S':
			col[0]= 0b1000100;
			col[1]=	0b1001010;
			col[2]=	0b1001001;
			col[3]=	0b1001001;
			col[4]=	0b0101001;
			col[5]=	0b0010001;
			letter_len=6;
			break;	
		
		case 't': case 'T':
			col[0]=	0b0000001;
			col[1]=	0b0000001;
			col[2]=	0b1111111;
			col[3]=	0b0000001;
			col[4]=	0b0000001;
			col[5]=	0b0000000;
			letter_len=6;
			break;		
					
		case 'u': case 'U':
			col[0]= 0b0011111;
			col[1]=	0b0100000;
			col[2]=	0b1000000;
			col[3]=	0b1000000;
			col[4]=	0b0100000;
			col[5]=	0b0011111;
			letter_len=6;
			break;	
		
		case 'v': case 'V':
			col[0]= 0b0000011;
			col[1]=	0b0001100;
			col[2]=	0b0110000;
			col[3]=	0b0110000;
			col[4]=	0b0001100;
			col[5]=	0b0000011;
			letter_len=6;
			break;		
					
		case 'w': case 'W':
			col[0]= 0b0001111;
			col[1]=	0b1110000;
			col[2]=	0b0011000;
			col[3]=	0b0011000;
			col[4]=	0b1110000;
			col[5]=	0b0001111;
			letter_len=6;
			break;	
		
		case 'x': case 'X':
			col[0]= 0b1000001;
			col[1]=	0b0100010;
			col[2]=	0b0011100;
			col[3]=	0b0011100;
			col[4]=	0b0100010;
			col[5]=	0b1000001;
			letter_len=6;
			break;		
					
		case 'y': case 'Y':
			col[0]= 0b0000001;
			col[1]=	0b0000010;
			col[2]=	0b1111100;
			col[3]=	0b1111100;
			col[4]=	0b0000010;
			col[5]=	0b0000001;
			letter_len=6;
			break;	
		
		case 'z': case 'Z':
			col[0]= 0b1100001;
			col[1]=	0b1010001;
			col[2]=	0b1001001;
			col[3]=	0b1000101;
			col[4]=	0b1000011;
			col[5]=	0b1000001;
			letter_len=6;
			break;		
					
		case '0':
			col[0]= 0b0011100;
			col[1]=	0b0100010;
			col[2]=	0b1000001;
			col[3]=	0b1000001;
			col[4]=	0b0100010;
			col[5]=	0b0011100;
			letter_len=6;
			break;	
			
		case '1':
			col[0]= 0b0000000;
			col[1]=	0b0000000;
			col[2]=	0b1000010;
			col[3]=	0b1111111;
			col[4]=	0b1000000;
			col[5]=	0b0000000;
			letter_len=6;
			break;		
			
		case '2':
			col[0]= 0b1110010;
			col[1]=	0b1001001;
			col[2]=	0b1001001;
			col[3]=	0b1001001;
			col[4]=	0b1001001;
			col[5]=	0b1000110;
			letter_len=6;
			break;	
			
		case '3':
			col[0]= 0b1001001;
			col[1]=	0b1001001;
			col[2]=	0b1001001;
			col[3]=	0b1001001;
			col[4]=	0b0101010;
			col[5]=	0b0010100;
			letter_len=6;
			break;	
			
			
		case '4':
			col[0]= 0b0010000;
			col[1]=	0b0011000;
			col[2]=	0b0010100;
			col[3]=	0b0010010;
			col[4]=	0b1111111;
			col[5]=	0b0010000;
			letter_len=6;
			break;	
			
		case '5':
			col[0]= 0b1101111;
			col[1]=	0b1001001;
			col[2]=	0b1001001;
			col[3]=	0b1001001;
			col[4]=	0b1001001;
			col[5]=	0b0110001;
			letter_len=6;
			break;		
		
		case '6':
			col[0]= 0b0111110;
			col[1]=	0b1001001;
			col[2]=	0b1001001;
			col[3]=	0b1001001;
			col[4]=	0b1001001;
			col[5]=	0b0110000;
			letter_len=6;
			break;
		
				
		case '7':
			col[0]= 0b0000001;
			col[1]=	0b1100001;
			col[2]=	0b0110001;
			col[3]=	0b0001001;
			col[4]=	0b0000101;
			col[5]=	0b0000011;
			letter_len=6;
			break;	
			
				
		case '8':
			col[0]= 0b0110110;
			col[1]=	0b1001001;
			col[2]=	0b1001001;
			col[3]=	0b1001001;
			col[4]=	0b1001001;
			col[5]=	0b0110110;
			letter_len=6;
			break;	
		
					
		case '9':
			col[0]= 0b0100110;
			col[1]=	0b1001001;
			col[2]=	0b1001001;
			col[3]=	0b1001001;
			col[4]=	0b1001001;
			col[5]=	0b0111110;
			letter_len=6;
			break;	
					
		case '.':
			col[0]= 0b0000000;
			col[1]=	0b0000000;
			col[2]=	0b0110000;
			col[3]=	0b0110000;
			col[4]=	0b0000000;
			col[5]=	0b0000000;
			letter_len=6;
			break;
		
		case '/':
			col[0]= 0b1000000;
			col[1]=	0b0100000;
			col[2]=	0b0010000;
			col[3]=	0b0001000;
			col[4]=	0b0000100;
			col[5]=	0b0000010;
			letter_len=6;
			break;	
			
		
		case 'ª':
			col[0]= 0b0000000;
			col[1]=	0b0000000;
			col[2]=	0b0000000;
			col[3]=	0b0000110;
			col[4]=	0b0000110;
			col[5]=	0b0000000;
			letter_len=6;
			break;	
			
		
		case 'º':
			col[0]= 0b0001100;
			col[1]=	0b0011111;
			col[2]=	0b1111110;
			col[3]=	0b1111110;
			col[4]=	0b0011111;
			col[5]=	0b0001100;
			letter_len=6;
			break;	
			
		default://�space
			col[0]= 0b0000000;
			col[1]=	0b0000000;
			col[2]=	0b0000000;
			col[3]=	0b0000000;
			col[4]=	0b0000000;
			col[5]=	0b0000000;
			break;
	}

	for (byte x=0; x<max_letter; ++x) 
	{
		byte row = col[x];
		for (byte y=0; y<7; ++y) {
			byte data = row & 1;  
			if (data) {
				ShadowPlot(x+Dx,y+Dy);
			}
			else
			{
				//plot(x+Dx,y+Dy,0);
			}
			row>>=1;//decale a droite
		}
	}

	return letter_len+1;//+1=espace
}

void matrix::DrawString(char* str,int Dx,int Dy)
{
	int Px=Dx;
	int Py=Dy;
	int StrSize=sizeof(str);
	for(int i=0;i<=StrSize;i++)
	{
		Dx+=DrawCharEx(str[i],Dx, Dy);
		if(Dx>24)
		{
			Dx=Px;
			Dy=Dy+6;
			//ligne suivante ...
		}
	}
}
