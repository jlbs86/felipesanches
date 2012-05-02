#define n_dbits 6
#define n_abits 10

int a[n_abits]={2, 3, 4, 5, 6, 7, 8, 9, 10, 11}; //(10, 9, 8, 7, 6, 5, 4, 3, 25, 24), 21, 23, 2, 26, 27
int d[n_dbits]={A0, A1, A2, A3, A4, A5}; //(11, 12, 13, 15, 16, 17), 18, 19
int oe=12; //22
int ce=13; //20

long int address;
int data;

void setup(){
  address=0x0;
  int i;
  pinMode(oe, OUTPUT);
  pinMode(ce, OUTPUT);

  for (i=0;i<n_abits;i++){
    pinMode(a[i], OUTPUT);
  }
  
  for (i=0;i<n_dbits;i++){
    pinMode(d[i], INPUT);
  }
  
  Serial.begin(38400);
}

int read27c256(long int addr){
  int i;
  long int j;
  for (i=0, j=1; i<n_abits; i++,j*=2){
    digitalWrite(a[i], addr&j ? HIGH : LOW);
  }

  digitalWrite(oe, LOW);
  digitalWrite(ce, LOW);
  
  //wait 1 msecond
  //delay(1);
  
  data=0;
  for (i=0, j=1; i<n_dbits; i++,j*=2){
    if (digitalRead(d[i])==HIGH){
       data+=j;
    }
  }

  digitalWrite(oe, HIGH);
  digitalWrite(ce, HIGH);

  return data;
}
long int MAXADDR=0x7fff;
int chunk_size = 32;
void loop(){
  while(address<=MAXADDR){
    
      Serial.print(address, HEX);
      Serial.print("\t");
      for (int i=0; i<chunk_size; i++){
        Serial.print(read27c256(address), HEX);
        Serial.print(" ");
      }
      Serial.println();
    
    address+=chunk_size;
  }
}
