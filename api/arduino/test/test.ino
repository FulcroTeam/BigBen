#include <Servo.h>
Servo myServo;

String string;
char delimiter = ';';
String splittedString[3];
int index1, index2, index3;
boolean isDoorOpen;
boolean isAlarmOn;
const int piezoPort = 5;
const int triggerPort = 6;
const int echoPort = 7;
long startDuration;
long startDistance;
const int tmpSensorPin = A0;



void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);

  pinMode(2,OUTPUT);            //fan
  pinMode(4, OUTPUT);           //+5V door
  pinMode(piezoPort, OUTPUT);   //Piezo (pin 5)
  pinMode(triggerPort, OUTPUT); //(pin 6)
  pinMode(echoPort, INPUT);     //(pin 7)
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);

  


  myServo.attach(3);     //Door
  myServo.write(70);
  isDoorOpen = false;

  digitalWrite(triggerPort, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPort, LOW);
  startDuration = pulseIn(echoPort, HIGH);
  startDuration -= 30;
  startDistance = 0.034 * startDuration / 2;
  isAlarmOn=false;
  
}

void loop() {
  digitalWrite(triggerPort, LOW);
  
  if (Serial.available() > 0) {
    string = Serial.readString();
    //Serial.println(string);

    //splitting the reveived string in three part
    index1 = string.indexOf(delimiter);
    splittedString[0] = string.substring(0, index1);
    string = string.substring(index1 + 1);
    index2 = string.indexOf(delimiter);
    splittedString[1] = string.substring(0, index2);
    string = string.substring(index2 + 1);
    index3 = string.indexOf(delimiter);
    splittedString[2] = string.substring(0, index3);

    
    //Serial.println(splittedString[0]);
    //Serial.println(splittedString[1]);
    //Serial.println(splittedString[2]);
    

    if (splittedString[0].equals("toggle")) {
      if((splittedString[1].toInt()!=3)&&(splittedString[1].toInt()!=6)){
        digitalWrite(splittedString[1].toInt(), !digitalRead(splittedString[1].toInt()));
        Serial.println(digitalRead(splittedString[1].toInt()));
      }
      else{
        if(splittedString[1].toInt()==3){
          if(!isDoorOpen){
              myServo.write(160);
              isDoorOpen=true;
              Serial.println(1);
              delay(15);
          }
          else{
              myServo.write(70);
              isDoorOpen=false;
              Serial.println(0);
              delay(15);
          } 
        }
        if(splittedString[1].toInt()==6)
          isAlarmOn=!isAlarmOn;
          Serial.println(isAlarmOn);

      }
    }

    if (splittedString[0].equals("temperature")) {
     //getting the voltage reading from the temperature sensor
     int reading = analogRead(tmpSensorPin);  
     
     float voltage = reading * 5.0;
     voltage /= 1024.0;  
     float temperature = (voltage - 0.5) * 100 ;  
     Serial.print(temperature);

    }
    
    if (splittedString[0].equals("digitalWrite")) {
      digitalWrite(splittedString[1].toInt(), splittedString[2].equals("HIGH") ? HIGH : LOW);
      Serial.println("Done");
    }

    if(isAlarmOn){
      digitalWrite(triggerPort, HIGH);
      delayMicroseconds(10);
      digitalWrite(triggerPort, LOW);
      long duration = pulseIn(echoPort, HIGH);
      long distance = 0.034 * duration / 2;
      if(duration < startDuration)
        for(int index1; index1<10; index1++){
          tone(piezoPort , 262 , 250);
          delay(400);
        }
    }
  }
}

