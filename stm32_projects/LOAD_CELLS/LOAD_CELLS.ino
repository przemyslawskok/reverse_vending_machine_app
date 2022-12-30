/**
 *
 * HX711 library for Arduino - example file
 * https://github.com/bogde/HX711
 *
 * MIT License
 * (c) 2018 Bogdan Necula
 *
**/
#include "HX711.h"

// Serial Port Communication Variables
const char startChar = 'X', endChar = 'Y';
// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 32;
const int LOADCELL_SCK_PIN = 33;

const int LOADCELL_DOUT_PIN_2 = 22;
const int LOADCELL_SCK_PIN_2 = 23;


const int LOADCELL_DOUT_PIN_3 = 4;
const int LOADCELL_SCK_PIN_3 = 0;


const int LOADCELL_DOUT_PIN_4 = 2;
const int LOADCELL_SCK_PIN_4 = 15;


HX711 scale1;

HX711 scale2;

HX711 scale3;

HX711 scale4;

void setup() {
  Serial.begin(9600);
  //Serial.println("Initializing the scale 1");
  scale1.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale1.set_scale(2280.f);                    
  scale1.tare();                

  //Serial.println("Initializing the scale 2");
  scale2.begin(LOADCELL_DOUT_PIN_2, LOADCELL_SCK_PIN_2);
  scale2.set_scale(2280.f);                    
  scale2.tare();                

  //Serial.println("Initializing the scale 3");
  scale3.begin(LOADCELL_DOUT_PIN_3, LOADCELL_SCK_PIN_3);
  scale3.set_scale(2280.f);                    
  scale3.tare();                

  //Serial.println("Initializing the scale 4");
  scale4.begin(LOADCELL_DOUT_PIN_4, LOADCELL_SCK_PIN_4);
  scale4.set_scale(2280.f);                    
  scale4.tare();                

 
}

void loop() {
   if (Serial.available() > 0) {
    // read the incoming string:
    String command = Serial.readStringUntil('\n');
     if (command=="TARE"){
        scale1.tare();
        scale2.tare();
        scale3.tare();
        scale4.tare();
      }
  }
  


  //Serial.print("1:  \t");
  float one_reading = scale1.get_units();
  //Serial.print(one_reading);
  //Serial.print("\t| AV:\t");
  //Serial.print(scale1.get_units(10), 1);

  //Serial.print("  2:  \t");
  float two_reading = scale2.get_units();
  //Serial.print(two_reading);
  //Serial.print("\t| AV:\t");
  //Serial.print(scale2.get_units(10), 1);

  //Serial.print("  3:  \t");
  float three_reading = scale3.get_units();
  //Serial.print(three_reading);
  //Serial.print("\t| AV:\t");
  //Serial.print(scale3.get_units(10), 1);

  //Serial.print("  4:  \t");
  float four_reading = scale4.get_units();
  //Serial.print(four_reading);
  //Serial.print("\t| AV:\t");
  //Serial.println(scale4.get_units(10), 1);

  //Serial.print("  SUM:\t");
  float sum = one_reading + two_reading + three_reading + four_reading;
  String sum_string = String(sum,2);
  Serial.print(startChar);
  Serial.print(sum_string);
  Serial.print(endChar);
  delay(100);  
}
