String string;
char delimiter = ';';
String splittedString[3];
int index1, index2, index3;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);

  pinMode(3,OUTPUT);
  pinMode(13, OUTPUT);
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
    
    if (splittedString[0].equals("digitalWrite")) {
      digitalWrite(splittedString[1].toInt(), splittedString[2].equals("HIGH") ? HIGH : LOW);
      Serial.println("Done");
    }
  }
}

