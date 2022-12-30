// speedPlot.ino

// thie millisDelay library is available from https://www.forward.com.au/pfod/ArduinoProgramming/TimingDelaysInArduino.html
#include <millisDelay.h>
// the SpeedStepper library is available from https://www.forward.com.au/pfod/Robots/SpeedStepper/index.html
#include <SpeedStepper.h>
#include <limits.h>  // for max,min values
#include <pfodBufferedStream.h>



/*
   (c)2019 Forward Computing and Control Pty. Ltd.
   NSW Australia, www.forward.com.au
   This code is not warranted to be fit for any purpose. You may only use it at your own risk.
   This generated code may be freely used for both private and commercial use
   provided this copyright is maintained.
*/

// stepperPlot.ino
// this sketch will plot speed and position
// on the Arduino IDE MY_SERIAL Plotter
// The plot will start 10sec after the board is programmed/reset
// It illustrates a number of speed changes, hitting a position limit and going home.
// See the speedStepperPlot.jpg in this directory for sample output
// max time to computeNewStep for Arduino UNO is 208us, for Arduino Mega is 216us
// max time time to computeNewStep for SparkFun Redboard Turbo is 154us
//

// ========== MY_SERIAL setting ================
// change this to match your board,  UNO/Mega use Serial, Redboard Turbo USB (slow) use SerialUSB, Redboard Turbo D0/D1 (fast) use Serial1
#define MY_SERIAL Serial
const uint32_t MY_SERIAL_BAUD_RATE = 115200;

const size_t OUTPUT_BUFFER_SIZE = 1024;
uint8_t outputBuffer[OUTPUT_BUFFER_SIZE];
pfodBufferedStream bufferedStream(MY_SERIAL_BAUD_RATE, outputBuffer, OUTPUT_BUFFER_SIZE); // do not block just drop chars if buffere full

// change these pin definitions to match you motor driver
// NOTE carefully do not use pins 6,7,8,9,10,11 on ESP32 / ESP8266
const int STEP_PIN = 16;  
const int DIR_PIN = 17;

SpeedStepper stepper(STEP_PIN, DIR_PIN);

// for Arduino IDE plotting, leave #define DEBUG commented out
// and uncomment #define PLOT_OUTPUT
// plotting will start 10sec after reset
#define PLOT_OUTPUT

// for text debug uncomment #define DEBUG
//#define DEBUG

millisDelay startDelay;
const unsigned long START_DELAY_MS = 1000; // 1sec

millisDelay printDelay;
const uint32_t PRINT_DELAY_MS = 50;

uint32_t start_ms;
bool startPrints = false;

// this struct is defined in SpeedStepper.h
//struct SpeedProfileStruct {
//  float speed;   // the target speed at the end of this step
//  unsigned long deltaTms;   // the time to accelerate from current speed (at start of this step) to the target speed
//};

SpeedProfileStruct profile[] = {
  { 0, 0}, // stop immediately if not already stopped
  { 0, 1000}, // hold zero for 1sec
  { -50, 0}, // jump to -50
  { -200, 2000}, // ramp to -200
  { -200, 6000}, // hold at -200 for 6sec
  { -50, 2000},  // ramp down to -50
  { 0, 0},   // // stop immeadiately
  { 0, 1500}, // hold zero for 1.5sec
  { 50, 0},   // jump to 50
  { 200, 2000},  // ramp to 200
  { 200, 6000},  // hold 200 for 6 sec
  { 50, 2000},   // ramp to 50
  { 0, 0},    // // stop immeadiately
  { 0, 1000}  // hold zero  // for plotting output
};

const size_t PROFILE_LEN = sizeof(profile) / sizeof(SpeedProfileStruct);

Stream* serialIO;

void setup() {
  // change the #define SERIAL at the top of this sketch to use other Serial connections
  MY_SERIAL.begin(MY_SERIAL_BAUD_RATE);
  serialIO = bufferedStream.connect(&MY_SERIAL);
  // ------------------------------

  for (int i = 3; i > 0; i--) {//was 10
#ifdef DEBUG
    serialIO->println(i);
#endif
    delay(1000);
  }
  //stepper.setDebugPrint(serialIO); // also need to uncomment #define DEBUG in SpeedStepper.cpp

  stepper.setProfile(profile, PROFILE_LEN); // set the profile
  startDelay.start(START_DELAY_MS);
}



void loop() {
  bufferedStream.available();

  stepper.run();

  if (startDelay.justFinished()) {
    // start run
    stepper.startProfile();
    start_ms = millis();
    printDelay.start(PRINT_DELAY_MS);
    startPrints = true;
    printValues();
  }

  if (printDelay.justFinished()) {
    printDelay.restart();
    if (stepper.isProfileRunning()) {
      printValues();
    }
  }
}

void printValues() {
#ifdef PLOT_OUTPUT
  //serialIO->print(" Time:"); serialIO->print((millis() - start_ms) / 1000.0);
  serialIO->print(",Speed:"); serialIO->println(stepper.getSpeed());
#endif
#ifdef DEBUG
  serialIO->print(F(" >> at ")); serialIO->print(millis() - start_ms);
  serialIO->print(F(" speed:")); serialIO->print(stepper.getSpeed());  serialIO->print(F(" target Speed:")); serialIO->print(stepper.getSetSpeed());
  serialIO->println();
#endif
}
