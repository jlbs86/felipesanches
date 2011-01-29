#include "Led_matrix.h"

#define NUMDEV 7
#define X_MAX 23
#define Y_MAX 15

matrix m;
int CS[] = {2,3,4,5,6,7,8};
void setup()
{
  int dev;
  Serial.begin(19200);
//  Serial.begin(38400);
//  Serial.begin(57600);
  m.setData(10);
  m.setWrite(9);
  for (dev=0;dev<NUMDEV;dev++){
    m.setCS(CS[dev]);
    m.setup();
  }
}

#include "font5x7.h"

int count = 0;
int offset = 0;
int scrollspeed=168-2;
boolean y_center=false;

char msg1[29] = "       HACKERSPACE SP       ";
char msg2[29] = "    GAROA  HACKER  CLUBE    ";

#define ENABLE_TEXT_SCROLLING 0
#define DISABLE_TEXT_SCROLLING 1
#define SEND_GRAPHICS_BUFFER 2
#define SEND_LAMP_DATA 3
#define SEND_TEXT_MESSAGE 4
#define ONE_LINE_VERTICAL_CENTER 5
#define TWO_LINES_OF_TEXT 6

void demo_serial_plot ()
{
  int i, index, dev;
  byte val;
  byte mybuffer[48*NUMDEV];
  
#if 0 //Imagens enviadas pela serial

  if (!Serial.available()) return;
  val = Serial.read();
  if (val != SEND_GRAPHICS_BUFFER) return;
  
  for (dev=0;dev<NUMDEV;dev++){
    //Serial.write(dev);
    for (i=0;i<48;i++){
      while(Serial.available() == 0) {}
      mybuffer[48*dev + i] = Serial.read();
    }
  }

#else
// mensagem pré-definida

  if (Serial.available()){
    val = Serial.read();

    if (val == SEND_LAMP_DATA){
      for (i=0;i<32;i++){
        while(Serial.available() == 0) {}
        Serial.read(); //ignore
      }
    }

    if (val == SEND_GRAPHICS_BUFFER){
      for (dev=0;dev<NUMDEV;dev++){
        for (i=0;i<48;i++){
          while(Serial.available() == 0) {}
          Serial.read(); //ignore
        }
      }
    }

    if (val == ENABLE_TEXT_SCROLLING){
      //enable scroll
      scrollspeed=168-2;
    }

    if (val == DISABLE_TEXT_SCROLLING){
      //disable scroll
      scrollspeed=0;
      offset=0;
    }

    if (val == ONE_LINE_VERTICAL_CENTER){
      y_center=true;
    }

    if (val == TWO_LINES_OF_TEXT){
      y_center=false;
    }
    
    if (val == SEND_TEXT_MESSAGE){
      for (i=0;i<28;i++){
        while(Serial.available() == 0) {}
        msg1[i] = Serial.read();
      }

      for (i=0;i<28;i++){
        while(Serial.available() == 0) {}
        msg2[i] = Serial.read();
      }
    }
  }

  int x, idx, col, px;
  int indexing=0;
  x=0;
  px = offset;

  count++;
  if (count>1){
    count=0;
    offset += scrollspeed;
    offset = (offset)%168;
  }  

  for (idx=0;idx<28;idx++){
    for (col=0;col<5;col++){      

#if 1
      if (msg1[idx] == 0x20){
        mybuffer[px*2]=0;
      } else {
        mybuffer[px*2] = chartable[ msg1[idx] - 'A' + 1 ][col];
      }

      if (msg2[idx] == 0x20){
        mybuffer[px*2 + 1]=0;
      } else {
        mybuffer[px*2 + 1] = chartable[ msg2[idx] - 'A' + 1 ][col];
      }
      
#else
        indexing = ascii_indexing[msg1[idx]];
        if (indexing>26) indexing=26;
        mybuffer[px*2] = chartable[indexing][col];

        indexing = ascii_indexing[msg2[idx]];
        if (indexing>26) indexing=26;
        mybuffer[px*2 + 1] = chartable[indexing][col];
#endif

      if (y_center){
        byte temp = mybuffer[px*2];
        mybuffer[px*2] = (temp&0xf0) >> 4;
        mybuffer[px*2+1] = (temp&0x0f) << 4;
      }

      x++;
      px = (x + offset)%168;

    }
    mybuffer[px*2]=0;
    mybuffer[px*2+1]=0;
    x++;
    px = (x + offset)%168;
  }

#endif

  index=0;        
  for (dev=0;dev<NUMDEV;dev++){
    m.setCS(CS[dev]);
       
    for (i=0;i<48;i++){
      val = mybuffer[index++];
      m.ht1632_shadowram[2*i] = (val & 0xf0) >> 4;
      m.ht1632_shadowram[2*i+1] = val & 0x0f;
    }
    m.ShadowDsp();
  }

}

void loop()
{
  demo_serial_plot();
}

