//int a[18]={22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,31,33};
//int d[8]={35,37,39,41,43,45,47,49};
int a[18]={33,31,52,50,48,46,44,42,40,38,36,34,32,30,28,26,24,22};
int d[8]={49,47,45,43,41,39,37,35};
int oe=51;
int ce=53;

//int a[19]={38, 24, 26, 28, 39,40,41, 50,51,52,53, 42,43,44,45,46,47,48,49};
//int d[8]={30,31,32,33,34,35,36,37};
//int oe=22;


long int address;
int data;

void setup(){
  address=0x0;
  int i;
  pinMode(oe, OUTPUT);
  pinMode(ce, OUTPUT);

  for (i=0;i<18;i++){
    pinMode(a[i], OUTPUT);
  }
  
  for (i=0;i<8;i++){
    pinMode(d[i], INPUT);
  }
  
  Serial.begin(38400);
}

int read27c040(long int addr){
  int i;
  long int j;
  for (i=0, j=1; i<18; i++,j*=2){
    digitalWrite(a[i], addr&j ? HIGH : LOW);
  }

  digitalWrite(oe, LOW);
  digitalWrite(ce, LOW);
  
  //wait 1 msecond
  //delay(1);
  
  data=0;
  for (i=0, j=1; i<8; i++,j*=2){
    if (digitalRead(d[i])==HIGH){
       data+=j;
    }
  }

  digitalWrite(oe, HIGH);
  digitalWrite(ce, HIGH);

  return data;
}

void loop(){
  while(address<0x40000){
    
      Serial.print(address, HEX);
      Serial.print("\t");
      Serial.print(read27c040(address), HEX);
      Serial.println();
    

    //Serial.print(char(read27c040(address)));
    
    address++;
  }
}
