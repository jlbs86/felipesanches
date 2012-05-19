int d[8]={2, 3, 4, 5, 6, 7, 8, 9};
int clk[8]={A0, A1, A2, A3, A4, A5, 12, 13};
bool leds[4][16];

void setup(){
  for (int i=0; i<4; i++){
    for (int j=0; j<16; j++){
      leds[i][j]=false;
    }
  }

  for (int i=0; i<8; i++){
    pinMode(d[i], OUTPUT);
    pinMode(clk[i], OUTPUT);
  }
}

void  write_panel_data(){
  for (int ic=0; ic<8; ic++){  
    digitalWrite(clk[ic], LOW);
  }
  
  for (int ic=0; ic<8; ic++){
    for(int led=0; led<8; led++){
      digitalWrite(d[led], leds[ic/2][8*(ic%2)+led] ? LOW : HIGH);
      digitalWrite(clk[ic], HIGH);
      digitalWrite(clk[ic], LOW);
    }
  }
} 

int counter=0, timer=0;
void loop(){
  timer++;
  if (timer>5){
    timer=0;
    counter++;
    if (counter>64){
      counter=0;
    }
  }

//animacao senoidal
  for (int i=0; i<4; i++){
    for (int j=0; j<16; j++){
      leds[i][j]=(j >= 8-8*abs(sin(2*3.14*(counter+i*6)/64))-1 && j <= 8+8*abs(sin(2*3.14*(counter+i*6)/64)));
    }
  }
 
  write_panel_data();

}

