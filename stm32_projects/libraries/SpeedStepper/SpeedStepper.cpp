// SpeedStepper.cpp
#include "SpeedStepper.h"

/*
   Modification (c)2019 Forward Computing and Control Pty. Ltd.
   NSW Australia, www.forward.com.au
   This code is not warranted to be fit for any purpose. You may only use it at your own risk.
   The modifications may be freely used for both private and commercial use
   provided this copyright is maintained.

   This code is based on http://www.airspayce.com/mikem/arduino/AccelStepper/ code and uses
   David Austin's equations from "Generate stepper-motor speed profiles in real time"
   with the exception that AccelStepper and SpeedStepper uses steps per second rather than radians per second (because we dont know the step angle of the motor)

   AccelStepper code is available under the following copyright
   Copyright
   This software is Copyright (C) 2010-2018 Mike McCauley. Use is subject to license
   conditions. The main licensing options available are GPL V2 or Commercial:

   Open Source Licensing GPL V2
    This is the appropriate option if you want to share the source code of your
   application with everyone you distribute it to, and you also want to give them
   the right to share who uses it. If you wish to use this software under Open
   Source Licensing, you must contribute all your source code to the open source
   community in accordance with the GPL Version 2 when your application is
   distributed. See https://www.gnu.org/licenses/gpl-2.0.html

   Commercial Licensing
   This is the appropriate option if you are creating proprietary applications
   and you are not prepared to distribute and share the source code of your
   application. To purchase a commercial license, contact info@airspayce.com
*/

// need to call setDebugPrint(..) as well as uncommenting one of these
//#define DEBUG
//#define COMPUTE_NEW_STEP_TIMING

/**
   Stepper(int stepPin, int dirPin)
   sets the pin connected to the driver step input
   and the pin connected to the driver's dir input
   Default for dir pin is HIGH for forward
   Use InvertDirectionPin() to change this if needed
*/
SpeedStepper::SpeedStepper(int stepPin, int dirPin) :  maxMaxSpeed(1000.0), minMaxSpeed(0.0003), minPulseWidth(2) {
  DIR_PIN = dirPin;
  STEP_PIN = stepPin;
  totalComputeTime = 0;
  maxComputeTime = 0;
  currentPosition = 0;
  maxPositionLimit = MAX_INT32_T;
  minPositionLimit = -MAX_INT32_T;
  profileArray = NULL;
  runningProfile = false;
  hardStop();
  setMaxSpeed(maxMaxSpeed); // sets cmax,cmin
  setMinSpeed(minMaxSpeed);
  setAcceleration(1.0); // sets c0, final_cn
  hardStop(); // picks up c0;
  pinMode(DIR_PIN, OUTPUT);
  digitalWrite(DIR_PIN, LOW);
  pinMode(STEP_PIN, OUTPUT);
  digitalWrite(STEP_PIN, LOW);
}

/**
   setAcceleration(float)
   Set the acceleration rate in steps/sec^2 used to change speeds
   Rates < 0.0001 are set to 0.0001
*/
void SpeedStepper::setAcceleration(float newAcceleration) {
  if (newAcceleration < 0.0) {
    newAcceleration = -newAcceleration;
  }
  if (newAcceleration <= 1e-4) {
    newAcceleration = 1e-4;
  }
  if (acceleration != newAcceleration)  {
    // Recompute _n per Equation 17
    n = n * (acceleration / newAcceleration); //
    // New c0 per Equation 7, with correction per Equation 15
    //min accel of 1e-4 => initial speed of 0.01 c0 = 95e6
    c0 = 0.676 * sqrt(2.0 / newAcceleration) * 1000000.0; // Equation 15
    acceleration = newAcceleration;
    // recalculate n using this new accel
    internalSetSpeed(targetSpeed);
#ifdef DEBUG
    if (debugPtr != NULL) {
      debugPtr->print(F(" >> setAcc"));
      debugPtr->print(F(" acc:"));
      debugPtr->print(acceleration);
      debugPtr->print(F(" n:"));
      debugPtr->print(n);
      debugPtr->print(F(" c0:"));
      debugPtr->print(c0);
      debugPtr->println();
    }
#endif
    computeNewSpeed();
  }
}

/**
   hardStop()
   Just stops the motor without any deceleration
*/
void SpeedStepper::hardStop() {
#ifdef DEBUG
  if (debugPtr != NULL) {
    debugPtr->println(F(" hardStop()"));
  }
#endif
#ifdef COMPUTE_NEW_STEP_TIMING
  if (debugPtr != NULL) {
    debugPtr->print(F(" max ComputeNewStep time:"));
    debugPtr->print(maxComputeTime);
    debugPtr->println(F("us"));
    debugPtr->print(F(" total ComputeNewStep time:"));
    debugPtr->print(totalComputeTime);
    debugPtr->println(F("us"));
  }
#endif
  stepInterval = 0; // stop;
  goingHome = false;
  speed = 0.0;
  a_speed = 0.0;
  targetSpeed = 0.0;
  a_targetSpeed = 0.0;
  final_cn = 1000000000.0; // very big
  targetDir = true;
  setDir(true); // sets forward
  n = 0;
  cn = c0;
}

/**
  hardStart(float speed)
  Just jump to this speed from current speed ignoring acceleration limits
  Still limited by speed limits and deceleration to position limits
  Clears goingHome flag
**/
void SpeedStepper::hardStart(float sp) {
#ifdef DEBUG
  if (debugPtr != NULL) {
    debugPtr->print(F(" hardStart("));
    debugPtr->print(sp);
    debugPtr->println(F(")"));
  }
#endif
#ifdef COMPUTE_NEW_STEP_TIMING
  if (debugPtr != NULL) {
    debugPtr->print(F(" max ComputeNewStep time:")); debugPtr->print(maxComputeTime); debugPtr->println(F("us"));
    debugPtr->print(F(" total ComputeNewStep time:")); debugPtr->print(totalComputeTime); debugPtr->println(F("us"));
  }
#endif
  goingHome = false; // always
  bool isTargetSpDirForward = (sp >= 0);
  setDir(isTargetSpDirForward);
  float a_sp = isTargetSpDirForward ? sp : -sp;

  if (a_sp < minSpeed) {
    hardStop();
    return;
  }
  bool starting = (stepInterval == 0);

  if (a_sp > maxSpeed) {
    a_sp = maxSpeed;
    sp = isTargetSpDirForward ? a_sp : -a_sp;
  }

  // assume newSpeed will be ok
  final_cn = 1000000.0 / a_sp;
  cn = final_cn;
  n = LARGE_N; // this suppresses further changes
  targetSpeed = sp;
  a_targetSpeed = a_sp;
  speed = sp;
  a_speed = a_sp;

#ifdef DEBUG
  if (debugPtr != NULL) {
    debugPtr->print(F(" targetSpeed : "));
    debugPtr->print(targetSpeed);
    debugPtr->print(F(" speed : "));
    debugPtr->print(speed);
    debugPtr->println();
  }
#endif

  uint32_t laststepInterval = stepInterval;
  stepInterval = cn;
  bool stepTaken = computeNewSpeed(); // apply limits here
  // here stepInterval may have been limited and updated
  if ( (starting) ||
       ( (!stepTaken) && ((micros() - lastStepTime) >= stepInterval))
     ) {
    // was stopped so do one step NOW
    // OR new stepInterval passed and step not taken
#ifdef DEBUG
    if (debugPtr != NULL) {
      debugPtr->print(F(" hardStart takes oneStep "));
    }
#endif
    oneStep();
  }
}


/**
   setDebugPtr(Stream*)
   Set where to send debug output, if any
   Need to uncomment #define DEBUG as well as calling this method

   param: s - the Stream to send debug output to

*/
void SpeedStepper::setDebugPrint(Print* s) {
  debugPtr = s;
}

/**
  goHome()
  set targetSpeed to maxSpeed
  in the direction to return to 0
  stop at 0
  calling setSpeed() will disable goingHome
*/
void SpeedStepper::goHome() {
#ifdef DEBUG
  if (debugPtr != NULL) {
    debugPtr->print(F(" >> goHome "));
  }
#endif
  if (currentPosition == 0) {
    hardStop();
    return;
  }

  goingHome = true;
  float homeSpeed = maxMaxSpeed;
  if (currentPosition > 0) {
    homeSpeed = -homeSpeed;
  } // else +ve
#ifdef DEBUG
  if (debugPtr != NULL) {
    debugPtr->print(F(" homeSpeed: "));
    debugPtr->print(homeSpeed);
    debugPtr->println();
  }
#endif

  internalSetSpeed(homeSpeed); // calls computeNewSpeed
}

/**
   isGoingHome()
   returns true if currently returning to position 0
*/
boolean SpeedStepper::isGoingHome() {
  return goingHome;
}


/**
   setPlusLimit(int32_t)
   sets the max positive limit position (in steps)
   param: mPos - the upper limit, must be >= 0
   if < currentPosition, set to currentPosition
   that is the currentPosition is alwayy within the limits
*/
void SpeedStepper::setPlusLimit(int32_t mPos) {
  if (mPos > MAX_INT32_T) {
    mPos = MAX_INT32_T;
  }
  if (mPos < currentPosition) {
    mPos = currentPosition;
  }
  if (mPos < 0) {
    mPos = 0;
  }
  maxPositionLimit = mPos;
}

/**
   getPlusLimit()
   returns the max positive limit position (in steps)
*/
int32_t SpeedStepper::getPlusLimit() {
  return maxPositionLimit;
}


/**
   setMinusLimit(int32_t)
   sets the max negative limit position (in steps)
   param: mPos - the upper limit, must be <= 0
   if > currentPosition, set to currentPosition
   that is the currentPosition is always within the limits
*/
void SpeedStepper::setMinusLimit(int32_t mPos) {
  if (mPos < -MAX_INT32_T) {
    mPos = -MAX_INT32_T;
  }
  if (mPos > currentPosition) {
    mPos = currentPosition;
  }
  if (mPos > 0) {
    mPos = 0;
  }
  minPositionLimit = mPos;
}

/**
   getMinusLimit()
   returns the max negative limit position (in steps)
*/
int32_t SpeedStepper::getMinusLimit() {
  return minPositionLimit;
}

/**
   setCurrentPosition(int32_t)
   set the current position in steps from 0, plus or minus
   It is limited to be within the set limits.
*/
void SpeedStepper::setCurrentPosition(int32_t pos) {
#ifdef DEBUG
  if (debugPtr != NULL) {
    debugPtr->print(F(" setCurrentPosition("));
    debugPtr->println(pos);
  }
#endif

  if (pos < minPositionLimit) {
    pos = minPositionLimit;
  }
  if (pos > maxPositionLimit) {
    pos = maxPositionLimit;
  }
  currentPosition = pos;
#ifdef DEBUG
  if (debugPtr != NULL) {
    debugPtr->print(F(" currentPosition set to "));
    debugPtr->println(getCurrentPosition());
  }
#endif
}

/**
   getCurrentPosition()
   return the current step count
*/
int32_t SpeedStepper::getCurrentPosition() {
  return currentPosition;
}

/**
   isDirForward()
   returns true if direction is FORWARD
*/
boolean SpeedStepper::isDirForward() {
  return dir;
}

/**
    setDirForward()
    set direction FORWARD
*/
void SpeedStepper::setDirForward() {
  dir = true;
  digitalWrite(DIR_PIN, HIGH);
  delayMicroseconds(minPulseWidth);
}

/**
    setDirReverse()
    set direction REVERSE
*/
void SpeedStepper::setDirReverse() {
  dir = false;
  digitalWrite(DIR_PIN, LOW);
  delayMicroseconds(minPulseWidth);
}


/**
   stop()
   Sets speed to 0.0 and decelerates to a stop
*/
void SpeedStepper::stop() {
  setSpeed(0.0);
}

/**
   oneStep()
   Takes a single step in the current direction
*/
void SpeedStepper::oneStep() {
  lastStepTime = micros(); // set lastStep
  digitalWrite(STEP_PIN, HIGH);
  // Delay the minimum allowed pulse width
  delayMicroseconds(minPulseWidth);
  digitalWrite(STEP_PIN, LOW);
}

/**
   stepForward()
   Take one step in the FORWARD direction
*/
void SpeedStepper::stepForward() {
  if (!isDirForward()) {
    setDirForward();
  }
  oneStep();
}

/**
   stepReverse()
   Take one step in the REVERSE direction
*/
void SpeedStepper::stepReverse() {
  if (isDirForward()) {
    setDirReverse();
  }
  oneStep();
}

/**
   stopAndSetHome()
   Does a hardStop() and then setCurrentPosition(0)
   for goHome()
*/
void SpeedStepper::stopAndSetHome() {
  //sets speed to zero also
  hardStop();
  setCurrentPosition(0);
}

/**
   run()
   This needs to be called often, at least once per loop()
   Checks if need to increment to next profile index
   Takes a step if it has been stepInterval since last step
   and then calculated new stepInterval
   returns true if stepper still running
*/
boolean SpeedStepper::run() {
  if (runningProfile) {
    // check end time
    unsigned long ms = millis();
    if ((ms - profileStepStartMs) >= profileStepLenMs ) {
      profileStepStartMs += profileStepLenMs; // new start allowing for slippage
      hardStart(profileTargetSpeed); // force to final speed
      // move to next step
      profileIdx++;
#ifdef DEBUG
      printCurrentProfileStep();
#endif
      if (profileIdx >= profileArraySize) {
        stopProfile();
      } else {
        profileTargetSpeed = profileArray[profileIdx].speed;
        profileStepLenMs = profileArray[profileIdx].deltaTms;
        // set acceleration
        // avoid large accelerations and handle small and zero deltaTms
        if (profileStepLenMs <= (stepInterval / 1000)) {
          hardStart(profileTargetSpeed);
        } else {
          float deltaSp = (profileTargetSpeed - getSpeed());
          setAcceleration( (deltaSp / ((float)(profileStepLenMs) )) * 1000.0); // setAcceleration handles -ve arg
          setSpeed(profileTargetSpeed);
        }
      }
    }
  }

  if (runSpeed()) {
    computeNewSpeed(); // does ramping if runningProfile
  }
  return (stepInterval != 0.0); // can also use isRunning() to check that
}


/**
   runSpeed()
   return false if nothing to do
   else takes a step if it has been stepInterval since last step
*/
boolean SpeedStepper::runSpeed() {
  // Dont do anything unless we actually have a step interval
  if (stepInterval == 0) {
    return false;
  }

  unsigned long time = micros();
  if (time - lastStepTime >= stepInterval) {
    if (isDirForward()) {
      // Clockwise
      if (currentPosition < MAX_INT32_T) {
        currentPosition += 1;
      }
    }  else  {
      // Anticlockwise
      if (currentPosition > -MAX_INT32_T) {
        currentPosition -= 1;
      }
    }
    oneStep();
    lastStepTime = time;
    return true;
  }  else    {
    return false;
  }
}

/**
   distanceToGo()
  calculate distance to go to limit based on direction of current speed
  +ve speed increases position, -ve speed decreases position
  if stopped use targetSpeed
  Always returns a +ve number
*/
int32_t SpeedStepper::distanceToGo() {
  int32_t dist = 0;
  if (goingHome) {
    dist = (currentPosition >= 0) ? currentPosition : -currentPosition; // TODO fix this for non-zero homes
  } else {
    bool increasing = isDirForward();
    if (!isRunning()) {
      increasing = targetDir;
    }
    if (increasing) {
      dist = (maxPositionLimit - currentPosition);
    } else {
      dist = (currentPosition - minPositionLimit);
    }
  }
  return dist; // always +ve
}


/**
   printComputeNewStepDebug()
   Outputs debug info on new Step calculation
*/
void SpeedStepper::printComputeNewStepDebug() {
#ifdef DEBUG
  if (debugPtr != NULL) {
    debugPtr->println();
    debugPtr->print(F(" speed "));
    debugPtr->print(speed);
    debugPtr->print(F(" target "));
    debugPtr->println(targetSpeed);
    debugPtr->print(F(" p "));
    debugPtr->print(currentPosition);
    debugPtr->print(F(" a "));
    debugPtr->println(acceleration);
    debugPtr->print(F(" cn "));
    debugPtr->println(cn);
    debugPtr->print(F(" c0 "));
    debugPtr->print(c0);
    debugPtr->print(F(" c0 Speed: "));
    debugPtr->println(1000000.0 / c0);
    debugPtr->print(F(" n "));
    debugPtr->println(n);
    debugPtr->print(F(" sInt "));
    debugPtr->println(stepInterval);
    debugPtr->println(F("******"));
  }
#endif
}

/**
   updateComputeTimes()
   Keeps track of maximum time computeNewSpeed() takes to execute
   and the total time spent in computeNewSpeed();
*/
void SpeedStepper::updateComputeTimes() {
#ifdef COMPUTE_NEW_STEP_TIMING
  uint32_t t = micros() - start_t;
  if (t > maxComputeTime) {
    maxComputeTime = t;
  }
  totalComputeTime += t;
#endif
}

/**
   computeNewSpeed()
   This calculates the next stepInterval based on the requested setSpeed
   the setAcceleration and the current speed.
   Modified by the set limits
   returns true if oneStep taken.
*/
bool SpeedStepper::computeNewSpeed() {
  bool rtn = false;
#ifdef COMPUTE_NEW_STEP_TIMING
  start_t = micros();
#endif
#ifdef DEBUG
  if (debugPtr != NULL) {
    debugPtr->print(F(" computeNewSpeed "));
  }
#endif
  int32_t distanceTo = distanceToGo(); // always +v adjusted for dir compared to 0 if going home
  if (distanceTo == 0) {
    // hit the limit
#ifdef COMPUTE_NEW_STEP_TIMING
    updateComputeTimes();
#endif
    hardStop();
    return rtn;
  }

  int32_t stepsToStop = (int32_t)((speed * speed) / (2.0 * acceleration)); // Equation 16

#ifdef DEBUG
  if (debugPtr != NULL) {
    debugPtr->println();
    debugPtr->print(F(" distanceTo "));
    debugPtr->print(distanceTo);
    debugPtr->print(F(" stepsToStop "));
    debugPtr->print(stepsToStop);
    debugPtr->println();
  }
#endif

  bool approachingLimit = false;
  if (stepsToStop >= distanceTo) { // set approachingLimit true
    // need to slow down
    n = -distanceTo; // may be zero, but check above and hardStop of zero
    approachingLimit = true;
#ifdef DEBUG
    if (debugPtr != NULL) {
      debugPtr->print(F(" update n to "));
      debugPtr->print(n);
      debugPtr->println();
    }
#endif
  }

  if (n == 0) {
#ifdef DEBUG
    if (debugPtr != NULL) {
      debugPtr->print(F(" n==0"));
    }
#endif

    if (a_targetSpeed < minSpeed) {
#ifdef COMPUTE_NEW_STEP_TIMING
      updateComputeTimes();
#endif
      hardStop();
      return rtn;
    }

    // else do first step
    cn = c0;
    setDir(targetDir); // was at n==0 so change dir now
    if (cn > final_cn) { // i.e. first step slower then final
      // first step of acceleration
      n++; // increment for next call n goes from 0 to 1
      // next call will reduce cn and increase speed towards final

    } else { // (final_cn > cn)
#ifdef DEBUG
      if (debugPtr != NULL) {
        debugPtr->print(F(" final_cn > cn"));
      }
#endif
      // go straight to target speed as less the first acceleration step
      cn = final_cn;
      n = LARGE_N; // this suppresses further changes
    }

    // set stepInterval and speed
    uint32_t laststepInterval = stepInterval;
    stepInterval = cn;
    a_speed = 1000000.0 / cn;
    if (isDirForward()) {
      speed = a_speed;
    } else {
      speed = -a_speed;
    }
    if (laststepInterval == 0) {
      // was stopped so do one step NOW
#ifdef DEBUG
      if (debugPtr != NULL) {
        debugPtr->print(F(" computeNewSpeed takes oneStep "));
      }
#endif
      oneStep();
      rtn = true;
    }
#ifdef DEBUG
    printComputeNewStepDebug();
#endif
#ifdef COMPUTE_NEW_STEP_TIMING
    updateComputeTimes();
#endif
    return rtn;
  } // end if (n == 0)

  // else not n==0
  if (n == LARGE_N) {
    // have reached final speed just keep going
#ifdef DEBUG
    if (debugPtr != NULL) {
      debugPtr->println();
      debugPtr->print(F(" no speed change needed "));
      debugPtr->println();
    }
#endif
#ifdef COMPUTE_NEW_STEP_TIMING
    updateComputeTimes();
#endif
    return rtn;
  }

  // else need to adjust speed
  float deltaCn = - ((2.0 * cn) / ((4.0 * n) + 1));
  float final_deltaCn = final_cn - cn;
  float a_deltaCn = (deltaCn >= 0) ? deltaCn : -deltaCn;
  float a_final_deltaCn = (final_deltaCn >= 0) ? final_deltaCn : -final_deltaCn;
#ifdef DEBUG
  if (debugPtr != NULL) {
    debugPtr->println();
    debugPtr->print(F(" a_final_deltaCn "));
    debugPtr->print(a_final_deltaCn);
    debugPtr->print(F(" a_deltaCn "));
    debugPtr->print(a_deltaCn);
    debugPtr->println();
  }
#endif
  if ((!approachingLimit) && (isDirForward() == targetDir) && (a_final_deltaCn < a_deltaCn)) {
#ifdef DEBUG
    if (debugPtr != NULL) {
      debugPtr->print(F(" final_cn "));
      debugPtr->println();
    }
#endif
    cn = final_cn;  // limited in setSpeed to be > cmin
    n = LARGE_N;
  } else {
    cn = cn + deltaCn; // Equation 13
    if (n < MAX_INT32_T) {
      n++; // for next loop
    }
  }
  stepInterval = cn;
  a_speed = 1000000.0 / cn;

  if (isDirForward()) {
    speed = a_speed;
  } else {
    speed = -a_speed;
  }
#ifdef DEBUG
  printComputeNewStepDebug();
#endif
#ifdef COMPUTE_NEW_STEP_TIMING
  updateComputeTimes();
#endif
  return rtn;
}


/**
   invertDirectionLogic()
   Changes logic of DIR_PIN output.
   Default is HIGH => Forward
   Calling this method toggles the current setting.
   invertDirectionLogic(); // -> LOW for Forward
   invertDirectionLogic(); // -> back to HIGH for Forward
*/
void SpeedStepper::invertDirectionLogic() {
  hardStop();
  dirPinInverted = !dirPinInverted;
  setDir(!dir); // force rewrite of pin
  hardStop(); // set back to normal stop
}

/**
   setDir(bool)
   Set the direction output to the stepper driver on the DIR_PIN
   Default is HIGH for forward
   Use InvertDirectionPin() to change to opposite polarity (e.g. LOW for forward)
*/
void SpeedStepper::setDir(boolean flag) {
  dir = flag;
  if (dir) {
    digitalWrite(DIR_PIN, dirPinInverted ? LOW : HIGH);
  } else {
    digitalWrite(DIR_PIN, dirPinInverted ? HIGH : LOW);
  }
  delayMicroseconds(minPulseWidth);
}

/**
   isRunning()
   returns true if stepInterval not zero
   i.e. will generate step at some time in the future.
*/
boolean SpeedStepper::isRunning() {
  return (stepInterval != 0);
}

/**
   getSpeed()
   return current speed
*/
float SpeedStepper::getSpeed() {
  return speed;
}

/**
   setSpeed(float)
   Set the speed and direction to drive the stepper
   +ve for Forward, -ve for Reverse
   The acceleration setting sets the ramp rate for changes in speed.
   Calling this method terminates goHome()
   param: sp - the required speed,
     Speeds < minSpeed are set as 0.0
     Speeds > maxSpeed are set as maxSpeed
*/
void SpeedStepper::setSpeed(float sp) {
  goingHome = false; // calls to setSpeed disable goingHome
  if (sp == targetSpeed) { // already at this speed nothing to do
    return; // nothing to do
  }
  internalSetSpeed(sp);
}

/**
   getSetSpeed()
   Get the speed that has been set by setSpeed
   +ve for Forward, -ve for Reverse
*/
float SpeedStepper::getSetSpeed() {
  return targetSpeed;
}

/**
   New speed, limited to maxSpeed and minSpeed
   if it is < minSpeed it is set to 0.0
*/
void SpeedStepper::internalSetSpeed(float sp) {
#ifdef DEBUG
  if (debugPtr != NULL) {
    debugPtr->print(F(" >> setSpeed "));
  }
#endif

  float a_sp = (sp >= 0.0) ? sp : -sp;
  if (a_sp > maxSpeed) {
    a_sp = maxSpeed;
  }

  // limits targetSpeed and sets final_cn === targetSpeed
  targetSpeed = (sp >= 0) ? a_sp : -a_sp;
  a_targetSpeed = a_sp;
  if (a_targetSpeed < minSpeed) {
    a_targetSpeed = 0.0;
    final_cn = 1000000000.0; // very big
  } else {
    final_cn = 1000000.0 / a_targetSpeed;
  }
#ifdef DEBUG
  if (debugPtr != NULL) {
    debugPtr->print(F(" final_cn: "));
    debugPtr->print(final_cn);
  }
#endif

  targetDir = targetSpeed >= 0;  // the final direction we want to go in

  long stepsToStop = ((long)((speed * speed) / (2.0 * acceleration))); // Equation 16
  // can be zero, will be zero if stopped
  n = stepsToStop; // new n for acceleration

  // find the step sign to change speed
  if (stepInterval == 0) {
    // stopped;  set new dir
    setDir(targetDir); // always
  }
  if (targetDir == isDirForward()) { // same direction
    setDir(targetDir); // always
    if (a_targetSpeed > a_speed) {
      // n +ve
      if (n > 0) {
        //  n = n+1;  // this needs more work to adjust ramp rates between speeds
      }
    } else {
      n = -n; // decelerate
    }
  } else {
    // change in direction
    // need to decelerate to 0 first
    n = -n;
    if (n == 0) { // stopped or just about to
      // change dir to target direction
      setDir(targetDir);
    } else {
      setDir(isDirForward()); // this should be the current setting
    }
  }

#ifdef DEBUG
  if (debugPtr != NULL) {
    debugPtr->print(F("  targetSpeed:"));
    debugPtr->print(targetSpeed);
    debugPtr->print(F("  speed:"));
    debugPtr->print(speed);
    debugPtr->print(F("  n:"));
    debugPtr->print(n);
    debugPtr->println();
  }
#endif

  computeNewSpeed();
}

/**
   setMaxSpeed(float)
   Sets the maximum abs(speed) that setSpeed can set
   Is limited to < 1000
   Must be called by this class' construction
   to initialize cmin,cmax
*/
void SpeedStepper::setMaxSpeed(float maxSp) {
  if (maxSp < 0) {
    maxSp = -maxSp;
  }
  if (maxSp < minSpeed) {
    maxSp = minSpeed;
  }
  if (maxSp > maxMaxSpeed) {
    maxSp = maxMaxSpeed;
  }
  maxSpeed = maxSp;
  if (maxSpeed < minSpeed) {
    // swap
    float temp = minSpeed;
    minSpeed = maxSpeed;
    maxSpeed = temp;
  }
  cmin = (1000000.0 / maxSpeed); // to compare to cn float
  cmax = (1000000.0 / minSpeed); // to compare to cn float
#ifdef DEBUG
  if (debugPtr != NULL) {
    debugPtr->print(F("  maxSpeed:"));
    debugPtr->print(maxSpeed);
    debugPtr->print(F("  cmin:"));
    debugPtr->print(cmin);
    debugPtr->println();
  }
#endif
}

/**
   setMinSpeed(float)
   Sets the minimum abs(speed) that setSpeed can set
   minSpeed is limited to > 0.0003
   Must be called by this class' construction
   to initialize cmin,cmax
*/
void SpeedStepper::setMinSpeed(float minSp) {
  if (minSp < 0) {
    minSp = -minSp;
  }
  if (minSpeed < minMaxSpeed) {
    minSpeed = minMaxSpeed;
  }
  if (minSp > maxMaxSpeed) {
    minSp = maxMaxSpeed;
  }
  minSpeed = minSp;
  if (maxSpeed < minSpeed) {
    // swap
    float temp = minSpeed;
    minSpeed = maxSpeed;
    maxSpeed = temp;
  }
  cmin = (1000000.0 / maxSpeed); // to compare to cn float
  cmax = (1000000.0 / minSpeed); // to compare to cn float
#ifdef DEBUG
  if (debugPtr != NULL) {
    debugPtr->print(F("  minSpeed:"));
    debugPtr->print(minSpeed);
    debugPtr->print(F("  cmax:"));
    debugPtr->print(cmax);
    debugPtr->println();
  }
#endif
}

/**
  setProfile
  Sets a speed profile to be run when startProfile() called
*/
void SpeedStepper::setProfile(SpeedProfileStruct* _profileArray, size_t _arrayLen) {
  profileArray = _profileArray;
  profileArraySize = _arrayLen;
}

/**
  printCurrentProfileStep()
  A debug helper method
*/
void SpeedStepper::printCurrentProfileStep() {
#ifdef DEBUG
  if (debugPtr) {
    if ((profileArray) && (profileIdx < profileArraySize)) {
      debugPtr->print(F(" ms:"));    debugPtr->print(millis());
      debugPtr->print(F(" start_ms:"));    debugPtr->print(profileStepStartMs);
      debugPtr->print(F(" profileIdx:"));    debugPtr->print(profileIdx);
      debugPtr->print(F(" sp:")); debugPtr->print(profileArray[profileIdx].speed);
      debugPtr->print(F(" deltaT:")); debugPtr->print(profileArray[profileIdx].deltaTms);
      debugPtr->print(F(" stepInterval:")); debugPtr->print(stepInterval);
      debugPtr->print(F(" acc:")); debugPtr->print(acceleration);
      debugPtr->println();
    }
  }
#endif
}

/**
  startProfile()
  Starts running the set profile from the current speed
*/
void SpeedStepper::startProfile() {
  runningProfile = false;
  if (!profileArray) {
    return;
  } // else
  profileIdx = 0;
  if (profileIdx > profileArraySize) {
    return;
  }
  profileStepStartMs = millis();
  profileTargetSpeed = profileArray[profileIdx].speed;
  profileStepLenMs = profileArray[profileIdx].deltaTms;
  // set acceleration
  // avoid large accelerations and handle small and zero deltaTms
  if (profileStepLenMs <= (stepInterval / 1000)) {
     hardStart(profileTargetSpeed);
  } else {
     float deltaSp = (profileTargetSpeed - getSpeed());
     setAcceleration( (deltaSp / ((float)(profileStepLenMs) )) * 1000.0); // setAcceleration handles -ve arg
     setSpeed(profileTargetSpeed);
  }
  run(); // action this new speed now with runningProfile false so we do not increment the idx
  runningProfile = true; // then set to true
#ifdef DEBUG
  printCurrentProfileStep();
#endif
}

/**
  stopProfile();
  stops running profile and stops
*/
void SpeedStepper::stopProfile() {
  runningProfile = false; // stop processing profile
  hardStop();
}

/**
  isProfileRunning();
  returns true if running a profile
*/
bool SpeedStepper::isProfileRunning() {
  return runningProfile;
}

