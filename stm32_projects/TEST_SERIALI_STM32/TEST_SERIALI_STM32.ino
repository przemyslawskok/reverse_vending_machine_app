#include <HardwareSerial.h>


HardwareSerial Serial3(PB9, PB8);

void setup() {
  // put your setup code here, to run once:
  Serial3.begin(9600);
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  Serial3.println("D");
  Serial.println(Serial3.read());
  delay(25);
}
