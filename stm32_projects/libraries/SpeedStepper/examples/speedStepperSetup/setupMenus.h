// setupMenus.h
/*
   (c)2019 Forward Computing and Control Pty. Ltd.
   NSW Australia, www.forward.com.au
   This code is not warranted to be fit for any purpose. You may only use it at your own risk.
   This generated code may be freely used for both private and commercial use
   provided this copyright is maintained.
*/

#include <Stream.h>
#include <millisDelay.h>
#include <SpeedStepper.h>

/**
 * This needs to be defined in the main sketch
 * to set it in normal running mode
 * It is called when the user select the run menu item.
 */
extern void setRunning();
extern void runStepper(Stream* io);
extern void printPositionAndLimits(Stream* io);
extern SpeedStepper stepper;
extern void runStepper(Stream* io);
extern bool stepperWasRunning;
void displayCurrentMenu();
void processChar(char c, Stream* io);
