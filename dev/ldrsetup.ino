//LDR pin which it is connected to 
const int ldrPIN = A0; 
int ldrStatus = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  int ldrStatus = analogRead(ldrPIN);
  //Serial writes LDR values
  Serial.println(ldrStatus);
  if (ldrStatus <= 200){
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.print("Darkness over here,turn on the LED :");
    Serial.println(ldrStatus);
  }
  else{
    digitalWrite(LED_BUILTIN, LOW);Serial.print("There is sufficient light , turn off the LED : ");
    Serial.println(ldrStatus);
  }
  delay(600);
}
