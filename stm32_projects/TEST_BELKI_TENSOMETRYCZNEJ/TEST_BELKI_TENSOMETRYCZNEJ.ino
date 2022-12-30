/**
 * Complete project details at https://RandomNerdTutorials.com/arduino-load-cell-hx711/
 *
 * HX711 library for Arduino - example file
 * https://github.com/bogde/HX711
 *
 * MIT License
 * (c) 2018 Bogdan Necula
 *
**/
#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = PB15;
const int LOADCELL_SCK_PIN = PB14;

HX711 scale;

void setup() {
  Serial.begin(115200);
  Serial.println("HX711 Demo");
  Serial.println("Initializing the scale");
  delay(50);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);

  Serial.println("Readings:");
}

void loop() {
  Serial.println(scale.get_units());
  delay(10);
 
}