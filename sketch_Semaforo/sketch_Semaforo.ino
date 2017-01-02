int incomingByte = 0;
void setup() {
  // put your setup code here, to run once:
  const int tmpSensorPin = A0;
  const float baselineTemp = 18.0;
  pinMode(3,OUTPUT);  
  pinMode(4,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(8,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(1000);
  if (Serial.available() > 0)
    incomingByte = int(Serial.read())-48;
  switch(incomingByte){
    case 3:
      digitalWrite(3,HIGH);
      break;
    case 4:
      digitalWrite(4,HIGH);
      break;
   /* case 6:
      digitalWrite(6,HIGH);
      break;
    case 7:
      digitalWrite(7,HIGH);
      break;  
    case 8:
      digitalWrite(8,HIGH);
      break; */
    default:
      Serial.write("Codice non valido");
      break; 
   }  
  
  int tmpSensorValue = analogRead(A0);
  //Serial.print("TMP: ");
  //Serial.print(tmpSensorValue);
  float voltage = (tmpSensorValue/1024.0)*5.0;
  //Serial.print("  --- Volts: ");
  //Serial.print(voltage);
  //Serial.print("  --- Temperature: ");
  float temperature = (voltage - .5)*100;
  //Serial.println(temperature);
  
  if(temperature>=30){
     digitalWrite(3, HIGH);
     digitalWrite(4, HIGH);
  }

       

}
