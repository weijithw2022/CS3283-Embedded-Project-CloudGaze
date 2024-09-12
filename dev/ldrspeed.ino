/*
   This program is written to calculate the speed of a cloud by measuring 
   the time difference between two adjacent LDR (Light Dependent Resistor) sensors.
   The speed is calculated based on the time it takes for the cloud's shadow
   to pass from one LDR to the other, using the distance between them. 
*/


//LDR pin which it is connected to 
const int ldrPIN1 = A0; 
const int ldrPIN2 = A1; 
int ldrStatus1 = 0;
int ldrStatus2 = 0;
int previousldrStatus1 = 0;
int previousldrStatus2 = 0;
int threshold = 100;
unsigned long t0;
unsigned long t1;
float length = 4.8;
float speed;
unsigned long duration;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  int length;
}

void loop() {
  // put your main code here, to run repeatedly:
  int ldrStatus1 = analogRead(ldrPIN1);
  int ldrStatus2 = analogRead(ldrPIN2);
  //Serial writes LDR values
  Serial.print("LDR1:");
  Serial.println(ldrStatus1);
  Serial.print("LDR2:");
  Serial.println(ldrStatus2);


  if(abs(ldrStatus1 - previousldrStatus1)> threshold){
    t0=millis();
    Serial.println("LDR1 change detected.");
    Serial.println(t0);
    previousldrStatus1 = ldrStatus1;
  }
  
  if(abs(ldrStatus2-previousldrStatus2)> threshold ){
    t1=millis();
    Serial.println("LDR2 change detected.");
    Serial.println(t1);
    previousldrStatus2 = ldrStatus2;

    if (t0 > 0) {
      duration = t1 - t0;  // Calculate the time difference
      Serial.print("Duration: ");
      Serial.print(duration);
      Serial.println(" ms");
      //Calculate the speed
      speed = (length*0.01)/(duration*0.001);
      Serial.print("Speed: ");
      Serial.print(speed);
      Serial.println(" ms-1");
      // Reset t0 and t1 for the next measurement
      t0 = 0;
      t1 = 0;
      while (true) {
        // Do nothing, effectively halting the loop
      }
    }
  }
  
}
