#include <Servo.h>

Servo thumbServo;  // только один сервопривод

void setup() {
  Serial.begin(9600);       // скорость как в Python
  thumbServo.attach(9);     // подключи жёлтый провод к D9
  thumbServo.write(0);      // начальное положение
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n'); // читаем число от Python
    int val = data.toInt();                     // преобразуем в число

    // Если палец поднят — сервопривод 90°, если опущен — 0°
    thumbServo.write(val ? 90 : 0);
  }
}
