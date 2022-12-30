// speedPlot.ino

// thie millisDelay library is available from https://www.forward.com.au/pfod/ArduinoProgramming/TimingDelaysInArduino.html
#include <millisDelay.h>
// the SpeedStepper library is available from https://www.forward.com.au/pfod/Robots/SpeedStepper/index.html
#include <SpeedStepper.h>

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

millisDelay stopDelay;
const uint32_t STOP_DELAY_MS = 25000;
millisDelay stopPrintDelay;
const uint32_t STOP_PRINT_DELAY_MS = 50000;
millisDelay printDelay;
const uint32_t PRINT_DELAY_MS = 50;

// starting speed
const float target0speed = +50;
millisDelay startRun0Delay;
const uint32_t START_RUN0_DELAY_MS = 1000;

const float target1speed = +100;
millisDelay speedChange1Delay;
const uint32_t SPEED_CHANGE1_DELAY_MS = 3000;

const float target2speed = -120;
millisDelay speedChange2Delay;
const uint32_t SPEED_CHANGE2_DELAY_MS = 8000;

const float target3speed = -100;
millisDelay speedChange3Delay;
const uint32_t SPEED_CHANGE3_DELAY_MS = 12000;

const float target4speed = 0;
millisDelay speedChange4Delay;
const uint32_t SPEED_CHANGE4_DELAY_MS = 15000;

millisDelay goHomeDelay;
const uint32_t GO_HOME_DELAY_MS = 19000;

uint32_t start_ms;

Stream* serialIO;

void setup() {

  // change the #define MY_SERIAL at the top of this sketch to use other Serial connections
  MY_SERIAL.begin(MY_SERIAL_BAUD_RATE);
  serialIO = &MY_SERIAL;
  // ------------------------------

  for (int i = 10; i > 0; i--) {
#ifdef DEBUG
    serialIO->println(i);
#endif
    delay(1000);
  }
  // stepper.setDebugPrint(serialIO); // also need to uncomment #define DEBUG in SpeedStepper.cpp
#ifdef DEBUG
  serialIO->println();
  serialIO->println(F(" press any key to start"));
  while (!serialIO->available()) {
    delay(10);
  }
  serialIO->println(F("SpeedStepper test!"));
#endif

  stepper.setPlusLimit(360);
  stepper.setMinusLimit(-510);
  stepper.setMaxSpeed(1000);
  stepper.setMinSpeed(1);
  stepper.stopAndSetHome();
  stepper.setAcceleration(50);
  stepper.hardStop();

  printDelay.start(PRINT_DELAY_MS);

  startRun0Delay.start(START_RUN0_DELAY_MS);
  speedChange1Delay.start(SPEED_CHANGE1_DELAY_MS);
  speedChange2Delay.start(SPEED_CHANGE2_DELAY_MS);
  speedChange3Delay.start(SPEED_CHANGE3_DELAY_MS);
  speedChange4Delay.start(SPEED_CHANGE4_DELAY_MS);

  goHomeDelay.start(GO_HOME_DELAY_MS);

  stopDelay.start(STOP_DELAY_MS);
  stopPrintDelay.start(STOP_PRINT_DELAY_MS);
  start_ms = millis();
}

bool stopPrints = false;

float lastSpeed = 0.0;
bool stopped = false;
void loop() {
  stepper.run();
  if (startRun0Delay.justFinished()) {
#ifdef DEBUG
    serialIO->println(F(" >>start run"));
#endif
    // start running at this speed
    // motor will move one step when setSpeed is called and then
    // on next call to run();
    stepper.setSpeed(target0speed);
  }

  if (stopDelay.justFinished()) {
    stopped = true;
    stepper.hardStop();
  }
  if (goHomeDelay.justFinished()) {
    stepper.goHome();
  }
  if (speedChange1Delay.justFinished()) {
    if (!stopped) {
#ifdef DEBUG
      serialIO->println(F(" >>change speed"));
#endif
      stepper.setSpeed(target1speed);
    }
  }
  if (speedChange2Delay.justFinished()) {
    if (!stopped) {
#ifdef DEBUG
      serialIO->println(F(" >>change speed"));
#endif
      stepper.setSpeed(target2speed);
    }
  }
  if (speedChange3Delay.justFinished()) {
    if (!stopped) {
#ifdef DEBUG
      serialIO->println(F(" >>change speed"));
#endif
      stepper.setSpeed(target3speed);
    }
  }
  if (speedChange4Delay.justFinished()) {
    if (!stopped) {
#ifdef DEBUG
      serialIO->println(F(" >>change speed"));
#endif
      stepper.setSpeed(target4speed);
    }
  }

  if (stopPrintDelay.justFinished()) {
    stopPrints = true;
  }

  if (printDelay.justFinished()) {
    if ((!stopPrints) && (!stopped)) {
      printDelay.restart();
#ifdef PLOT_OUTPUT
      serialIO->print(stepper.getCurrentPosition());
      serialIO->print(',');
      serialIO->println(stepper.getSpeed());
#endif
#ifdef DEBUG
      serialIO->print(F(" >> at "));
      serialIO->print(millis() - start_ms);
      serialIO->print(F(" speed:"));
      serialIO->print(stepper.getSpeed());
      serialIO->print(F(" target Speed:"));
      serialIO->print(stepper.getSetSpeed());
      serialIO->print(F(" deltaSpeed:"));
      serialIO->print(((stepper.getSpeed() - lastSpeed) * 1000) / PRINT_DELAY_MS);
      serialIO->println();
#endif
      lastSpeed = stepper.getSpeed();
    }
  }
}
