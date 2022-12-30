// setupMenus.cpp
/*
   (c)2019 Forward Computing and Control Pty. Ltd.
   NSW Australia, www.forward.com.au
   This code is not warranted to be fit for any purpose. You may only use it at your own risk.
   This generated code may be freely used for both private and commercial use
   provided this copyright is maintained.
*/

#include "setupMenus.h"

const int MAX_SETUP_SPEED = 500;  // max speed while setting position and limits

enum menu {MAIN_MENU, POSITION_MENU, LIMITS_MENU, RUN_MENU};
menu currentMenu = MAIN_MENU;

int32_t posLimit;
int32_t negLimit;
bool firstCall = true; // pickup limits

void displayMainMenu(Stream* io) {
  io->println();
  io->println(F(" SETUP"));
  printPositionAndLimits(io);
  io->println(F(" p -- set Home"));
  io->println(F(" l -- set limits"));
  runStepper(io);
  io->println(F(" h -- goHome"));
  io->println(F(" r -- run"));
  runStepper(io);
  io->print('>');
}

void displayPositionMenu(Stream* io) {
  io->println();
  io->println(F(" SET HOME"));
  printPositionAndLimits(io);
  io->println(F(" x -- setHome here and exit"));
  io->println(F(" + -- Forward"));
  runStepper(io);
  io->println(F(" - -- Reverse"));
  io->println(F(" s -- swap Forward/Reverse"));
  runStepper(io);
  io->println(F(" <else> -- hardStop"));
  io->print('>');
  runStepper(io);
}

void displayLimitsMenu(Stream* io) {
  io->println();
  io->println(F(" SET LIMITS"));
  printPositionAndLimits(io);
  io->println(F(" l -- setLimit here"));
  io->println(F(" + -- Forward"));
  runStepper(io);
  io->println(F(" - -- Reverse"));
  io->println(F(" h -- goHome"));
  runStepper(io);
  io->println(F(" x -- exit"));
  io->println(F(" <else> -- hardStop"));
  runStepper(io);
  io->print('>');
}

void displayCurrentMenu(Stream* io) {
  switch (currentMenu) {
  case RUN_MENU:
    break;
  case POSITION_MENU:
    displayPositionMenu(io);
    break;
  case LIMITS_MENU:
    displayLimitsMenu(io);
    break;
  case MAIN_MENU:
  default:
    displayMainMenu(io);
  }
}

void processMainMenu(char c, Stream * io) {
  if (c == 'p') {
    posLimit = stepper.getPlusLimit();
    negLimit = stepper.getMinusLimit();
    stepper.setPlusLimit(stepper.MAX_INT32_T);
    stepper.setMinusLimit(-stepper.MAX_INT32_T);
    currentMenu = POSITION_MENU; //setupHome(io);
    stepper.hardStop();
    stepperWasRunning = false;

  } else if (c == 'l') {
    posLimit = stepper.getPlusLimit();
    negLimit = stepper.getMinusLimit();
    // clear limits
    stepper.setPlusLimit(stepper.MAX_INT32_T);
    stepper.setMinusLimit(-stepper.MAX_INT32_T);
    currentMenu = LIMITS_MENU; //
    //setLimits(io);
    stepper.hardStop();
    stepperWasRunning = false;

  } else if (c == 'h') {
    stepper.goHome();

  } else if (c == 'r') {
    stepper.setPlusLimit(posLimit);
    stepper.setMinusLimit(negLimit);
    setRunning();
    currentMenu = RUN_MENU; //

  } else {
    // ignore
  }
}

void processPositionMenu(char c, Stream* io) {
  if (c == '+') {
    stepper.setSpeed(MAX_SETUP_SPEED);

  } else if (c == '-') {
    stepper.setSpeed(-MAX_SETUP_SPEED);

  } else if (c == 's') {
    stepper.invertDirectionLogic();

  } else if (c == 'x') {
    currentMenu = MAIN_MENU;
    stepper.stopAndSetHome();
    // restore limits
    stepper.setPlusLimit(posLimit);
    stepper.setMinusLimit(negLimit);

  } else {
    stepper.hardStop();
    stepperWasRunning = false;
  }
}

void processLimitsMenu(char c, Stream* io) {
  if (c == '+') {
    stepper.setSpeed(MAX_SETUP_SPEED);

  } else if (c == '-') {
    stepper.setSpeed(-MAX_SETUP_SPEED);

  } else if (c == 'h') {
    stepper.goHome();

  } else if (c == 'l') {
    stepper.hardStop();
    stepperWasRunning = false;
    int32_t pos = stepper.getCurrentPosition();
    if (pos <= 0) {
      stepper.setMinusLimit(pos);
      negLimit = stepper.getMinusLimit();
      io->print(F(" -limit set:"));
      io->println(negLimit);
    } else {
      stepper.setPlusLimit(pos);
      posLimit = stepper.getPlusLimit();
      io->print(F(" +limit set:"));
      io->println(posLimit);
    }
    //io->println(F(" To extend this limit, exit this menu, x, and select this \"set limits\" menu again"));

  } else if (c == 'x') {
    currentMenu = MAIN_MENU;
    // restore limits
    stepper.setPlusLimit(posLimit);
    stepper.setMinusLimit(negLimit);

  } else {
    stepper.hardStop();
    stepperWasRunning = false;
  }
}

void processChar(char c, Stream* io) {
  if (firstCall) {
    firstCall = false;
    posLimit = stepper.getPlusLimit();
    negLimit = stepper.getMinusLimit();
  }
  if (c == 0) {
    if ((!stepper.isRunning()) && stepperWasRunning) {
      stepperWasRunning = false;
      displayCurrentMenu(io);
    }
    return;
  }
  // else
  if ((c == '\n') || (c == '\r') ) {
    // got empty lime just stop
    io->println();
  } else {
    // echo char
    io->println(c);
  }

  // c != 0 here
  switch (currentMenu) {
  case RUN_MENU:
    // should not get this
    break;
  case POSITION_MENU:
    processPositionMenu(c, io);
    break;
  case LIMITS_MENU:
    processLimitsMenu(c, io);
    break;
  case MAIN_MENU:
  default:
    processMainMenu(c, io);
  }
  c = 0;
  displayCurrentMenu(io);

}
