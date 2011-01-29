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

#ifndef Led_matrix_h
#define Led_matrix_h
#include "WProgram.h"
#include "WConstants.h"
#include <avr/pgmspace.h>

#define HT1632_ID_CMD 4		/* ID = 100 - Commands */
#define HT1632_ID_RD  6		/* ID = 110 - Read RAM */
#define HT1632_ID_WR  5		/* ID = 101 - Write RAM */

#define HT1632_CMD_SYSDIS 0x00	/* CMD= 0000-0000-x Turn off oscil */
#define HT1632_CMD_SYSON  0x01	/* CMD= 0000-0001-x Enable system oscil */
#define HT1632_CMD_LEDOFF 0x02	/* CMD= 0000-0010-x LED duty cycle gen off */
#define HT1632_CMD_LEDON  0x03	/* CMD= 0000-0011-x LEDs ON */
#define HT1632_CMD_BLOFF  0x08	/* CMD= 0000-1000-x Blink ON */
#define HT1632_CMD_BLON   0x09	/* CMD= 0000-1001-x Blink Off */
#define HT1632_CMD_SLVMD  0x10	/* CMD= 0001-00xx-x Slave Mode */
#define HT1632_CMD_MSTMD  0x14	/* CMD= 0001-01xx-x Master Mode */
#define HT1632_CMD_RCCLK  0x18	/* CMD= 0001-10xx-x Use on-chip clock */
#define HT1632_CMD_EXTCLK 0x1C	/* CMD= 0001-11xx-x Use external clock */
#define HT1632_CMD_COMS00 0x20	/* CMD= 0010-ABxx-x commons options */
#define HT1632_CMD_COMS01 0x24	/* CMD= 0010-ABxx-x commons options */
#define HT1632_CMD_COMS10 0x28	/* CMD= 0010-ABxx-x commons options */
#define HT1632_CMD_COMS11 0x2C	/* CMD= 0010-ABxx-x commons options */
#define HT1632_CMD_PWM    0xA0	/* CMD= 101x-PPPP-x PWM duty cycle */

//function DEBUGPRINT
#if !defined(DEBUGPRINT)
#define DEBUGPRINT(fmt, args...)
#endif

//#define byte int
//matrix cmatrix(10,11,12);
class matrix
{
  public:
    matrix();
	void sendcmd(byte);
	void senddata (byte, byte);
	void setup();
        
        void setCS(int);
        void setData(int);
        void setWrite(int);
        
	void plot(char, char, char);
	int DrawCharEx(char,int,int);
	void DrawString(char*,int,int);
	void DrawLine(byte,byte,unsigned char, unsigned char,unsigned char val );
	void clear();
	
	void ShadowPlot(int,int);
	void ShadowDsp();
	void ClearShadow();
	
	void start();
	void finish();

        byte ht1632_shadowram[96];
  private:
	int pin_cs;
	int pin_wr;
	int pin_data;
	void chipselect(byte);
	void chipfree(byte);
	void writebits (byte, byte);
	int ft;
};



#endif

