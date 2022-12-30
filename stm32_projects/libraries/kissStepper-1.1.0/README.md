# Keep it Simple Stepper (kissStepper)
This is a lightweight Arduino/Teensyduino library for stepper motor controllers that use STEP/DIR interfaces, such as the Allegro and TI chips, the Easy Driver, Big Easy Driver, and Pololu DRV8825

Written by Rylee Isitt

## Features:
* Fast performance, uses port access to toggle the STEP pin
* Speed is set in Hz (frequency of the STEP pin)
* Approximately linear acceleration/deceleration set in Hz/s
* Very accurate speed timing at typical motor speeds
* Controls the STEP, DIR, and ENABLE pins of your motor controller
* Teensyduino compatibility

## License:
GNU Lesser General Public License (LGPL) V2.1

**Please see the LICENSE file for details**

## Installation Instructions:
1. Download the source code ZIP for the latest release of the library: https://github.com/risitt/kissStepper/releases
2. In the Arduino IDE main menu, select Sketch > Include Library > Add .ZIP Library, then select the downloaded file and click on "Open"
3. Include the library in your sketch: **#include &lt;kissStepper.h&gt;**
4. Read the API Documentation, or see the example sketches for information on how to use the library
