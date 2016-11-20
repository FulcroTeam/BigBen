int incomingByte = 0;
void setup() {
  // put your setup code here, to run once:
  pinMode(6,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(8,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(1000);
  if (Serial.available() > 0)
    incomingByte = Serial.read();
  switch(incomingByte){
    case 6:
      digitalWrite(6,HIGH);
      break;
    case 7:
      digitalWrite(7,HIGH);
      break;  
    case 8:
      digitalWrite(8,HIGH);
      break; 
    default:
      Serial.write("Codice non valido");
      break;   
  }
      

}
