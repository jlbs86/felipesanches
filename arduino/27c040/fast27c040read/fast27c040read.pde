// address:
// PA2 PA4 PA6 PG2-0 PB3-0 PL7-0
// arduino pins:
int addr_out[] = {24, 26, 28, 39,40,41, 50,51,52,53, 42,43,44,45,46,47,48,49};

// data:
// PC7-0
// arduino pins:
int data_in[] = {30,31,32,33,34,35,36,37};

// OE:
// PA0
// arduino pins: 22
int oe_out = 22;

// CE:
// PD7
// arduino pins:
int ce_out = 38;

long int address;
int data;

void setup(){
  address=0;
  int i;

  for(i=0;i<18;i++){
    pinMode(addr_out[i], OUTPUT);
  }
  pinMode(oe_out, OUTPUT);
  pinMode(ce_out, OUTPUT);

  for(i=0;i<8;i++){
    pinMode(data_in[i], INPUT);
  }  
  Serial.begin(9600);
}

int read27c040(long int addr){
// address:
// PA2 PA4 PA6 PG0-2 PB0-3 PL0-7
  PORTL = addr & 0xff;
  PORTB =  (PORTB & 0xf0) | ((addr >> 8) & 0x0f);
  PORTG =  (PORTG & 0xf8) | ((addr >> 12) & 0x07);
  PORTA =  (PORTA & 0b10101011) | (((addr >> 15) & 1) << 6) | (((addr >> 16) & 1) << 4) | (((addr >> 17) & 1) << 2);

// CE -> low
// PD7
  PORTD &= 0x7f;

// OE -> low
// PA0
  PORTA &= 0xfe;

//delay here?
delay(1);

// data:
// PC0-7
  data = PORTC;
  
// OE -> high
// PA0
  PORTA |= 0x01;

// CE -> high
// PD7
  PORTD |= 0x80;

  return data;
}

void loop(){
  while(address<0x40000){
    Serial.print(address, HEX);
    Serial.print("\t");
    Serial.print(read27c040(address), HEX);
    Serial.println();
    address++;
  }
}
