/*
  This code uses 3 LDR sensors (LDR1, LDR2, LDR3) to detect the direction of a moving cloud.
  The idea is to determine whether the cloud is moving East or South based on the sequence 
  in which the LDR values change by a certain threshold.

*/

enum Direction{
  North,
  East,
  South,
  West
};

Direction currentDirection; 

const int ldrPIN1 = A0; 
const int ldrPIN2 = A1; 
const int ldrPIN3 = A2; 

int ldrStatus1 = 0;
int ldrStatus2 = 0;
int ldrStatus3 = 0;

int previousldrStatus1 = 0;
int previousldrStatus2 = 0;
int previousldrStatus3 = 0;

int changeStatus1; 
int changeStatus2; 
int changeStatus3; 

int threshold = 50;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  previousldrStatus1 = analogRead(ldrPIN1);
  previousldrStatus2 = analogRead(ldrPIN2);
  previousldrStatus3 = analogRead(ldrPIN3);
}

void loop() {
  // put your main code here, to run repeatedly:
  int ldrStatus1 = analogRead(ldrPIN1);
  int ldrStatus2 = analogRead(ldrPIN2);
  int ldrStatus3 = analogRead(ldrPIN3);
  //Serial writes LDR values
  Serial.print("LDR1:");
  Serial.println(ldrStatus1);
  Serial.print("LDR2:");
  Serial.println(ldrStatus2);
  Serial.print("LDR3:");
  Serial.println(ldrStatus3);

  if(abs(ldrStatus1- previousldrStatus1)> threshold){
    changeStatus1 = abs(ldrStatus1- previousldrStatus1);
    Serial.println("LDR1 change detected.");
    previousldrStatus1 = ldrStatus1;
  }

  if(abs(ldrStatus2- previousldrStatus2)> threshold){
    changeStatus2 = abs(ldrStatus2- previousldrStatus2);
    Serial.println("LDR2 change detected.");
    previousldrStatus2 = ldrStatus2;
  }

  if(abs(ldrStatus3- previousldrStatus3)> threshold){
    changeStatus3 = abs(ldrStatus3- previousldrStatus3);
    Serial.println("LDR3 change detected.");
    previousldrStatus3 = ldrStatus3;
  }

  if(changeStatus1>threshold && changeStatus2>threshold && changeStatus2> changeStatus3){
    currentDirection = East;  
    Serial.println("Direction: East");
    while(true){

    }
  }
  else if(changeStatus1>threshold && changeStatus3>threshold && changeStatus3> changeStatus2){
    currentDirection = South;  
    Serial.println("Direction: South");
    while(true){
      
    }
  }
  changeStatus2= 0;
  changeStatus3= 0;
}
