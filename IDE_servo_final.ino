#include <Servo.h>

Servo thumbServo;
Servo indexServo;
Servo middleServo;
Servo ringServo;
Servo pinkyServo;

void setup() {
  Serial.begin(9600);
  thumbServo.attach(3);
  indexServo.attach(5);
  middleServo.attach(6);
  ringServo.attach(9);
  pinkyServo.attach(10);
  thumbServo.write(0);
  indexServo.write(0);
  middleServo.write(0);
  ringServo.write(0);
  pinkyServo.write(0);
}
void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n'); 
    int vals[5];
    int start = 0;
    for(int i=0; i<5; i++){
      int commaIndex = data.indexOf(',', start);
      if(commaIndex == -1 && i < 4){
        vals[i] = 0;
      } else {
        vals[i] = data.substring(start, commaIndex).toInt();
        start = commaIndex + 1;
      }
    }
    thumbServo.write(vals[0] ? 90 : 0);
    indexServo.write(vals[1] ? 90 : 0);
    middleServo.write(vals[2] ? 90 : 0);
    ringServo.write(vals[3] ? 90 : 0);
    pinkyServo.write(vals[4] ? 90 : 0);
  }
}