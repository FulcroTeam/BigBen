#include <Servo.h>
Servo myServo;

String string;
char delimiter = ';';
String splittedString[3];
int index1, index2, index3;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);

  pinMode(2,OUTPUT);  //fan
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(A0, INPUT);
  myServo.attach(3);
  myServo.write(0); 
}

void loop() {
  
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
      digitalWrite(splittedString[1].toInt(), !digitalRead(splittedString[1].toInt()));
      Serial.println(digitalRead(splittedString[1].toInt()));
    }

    if (splittedString[0].equals("temperature")) {
     //getting the voltage reading from the temperature sensor
     int reading = analogRead(splittedString[1].toInt());  
     
     float voltage = reading * 5.0;
     voltage /= 1024.0; 
          
     float temperature = (voltage - 0.5) * 100 ;  

     Serial.print(temperature);
    }
    
    if (splittedString[0].equals("digitalWrite")) {
      digitalWrite(splittedString[1].toInt(), splittedString[2].equals("HIGH") ? HIGH : LOW);
      Serial.println("Done");
    }
  }
}

