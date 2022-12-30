#include <Arduino.h>
HardwareTimer timer(TIM1);
HardwareTimer timer15(TIM15);

uint16_t licznik = 800;
volatile uint16_t licznik2 = 0;
uint8_t flaga = 0;



#include <TMCStepper.h>
#include <HardwareSerial.h>

HardwareSerial Serial3(PB9, PB8);
#define SERIAL_PORT Serial3

HardwareSerial Serial4(PA10, PA9);
#define SERIAL_PORT2 Serial4

const int TASMA_DIR = PC13;
const int TASMA_STEP = PD5;
const int TASMA_EN = PA4;
const int TASMA_RX = 25; //PB9
const int TASMA_TX = 24; //PB8
const int MS1 = PA1;
const int MS2 = PA0;

const int TASMA_DIR2 = PA5;
const int TASMA_STEP2 = PA12;
const int TASMA_EN2 = PA7;
const int TASMA_RX2 = PD6; //PB9
const int TASMA_TX2 = PA2; //PB8
const int MS12 = PA11;
const int MS22 = PA6;

TMC2208Stepper driver(&SERIAL_PORT, 0.11f);   
TMC2208Stepper driver2(&SERIAL_PORT2, 0.11f);    


bool ledOn = false;
void OnTimer1Interrupt() {
    ledOn = !ledOn;
    digitalWrite(TASMA_STEP, ledOn ? HIGH : LOW);
    digitalWrite(TASMA_STEP2, ledOn ? HIGH : LOW);
  
}
void OnTimer15Interrupt() {
    //Serial.println(licznik2);
    licznik2++;    
}



void start_tasma(uint8_t kierunek, uint16_t predkosc, uint16_t przyspieszenie)
{ 
  if (kierunek == 1)
  {
    digitalWrite(TASMA_DIR, LOW); //PRZOD
  }
  else digitalWrite(TASMA_DIR, HIGH);    //TYL
  
  
  if (licznik >= predkosc)
  {
    if (flaga == 0)
      {
          licznik2 = 0;
          flaga = 1;
      }
    if (licznik2 == przyspieszenie)
      {
        licznik--;         
        timer.setOverflow(licznik);
        timer.refresh();
        flaga = 0;
      }  
  }      
}






void setup() {

    Serial.begin(115200);

    Serial.println("Inicjacja programu");  
    pinMode(TASMA_EN, OUTPUT);
    pinMode(TASMA_STEP, OUTPUT);
    pinMode(TASMA_DIR, OUTPUT);

    pinMode(TASMA_EN2, OUTPUT);
    pinMode(TASMA_STEP2, OUTPUT);
    pinMode(TASMA_DIR2, OUTPUT);


    digitalWrite(TASMA_EN, LOW);

    digitalWrite(TASMA_EN2, LOW);

    // digitalWrite(TASMA_DIR, HIGH);
    // digitalWrite(TASMA_DIR2, HIGH);

    
    Serial3.begin(115200);

    Serial4.begin(115200);

    driver.begin();
    driver.toff(5);
    driver.rms_current(1200);
    driver.microsteps(32);
    driver.pwm_autoscale(true);
    driver.en_spreadCycle(true); 
    
    driver2.begin();
    driver2.toff(5);
    driver2.rms_current(1500);
    driver2.microsteps(32);
    driver2.pwm_autoscale(true);
    driver2.en_spreadCycle(true); 

    

    // Configure timer
    timer.setPrescaleFactor(4); // Set prescaler to 2564 => timer frequency = 168MHz/2564 = 65522 Hz (from prediv'd by 1 clocksource of 168 MHz)
    timer.setOverflow(1500); // Set overflow to 32761 => timer frequency = 65522 Hz / 32761 = 2 Hz
    timer.attachInterrupt(OnTimer1Interrupt);
    timer.refresh(); // Make register changes take effect
    timer.resume(); // Start

    timer15.setPrescaleFactor(2); // Set prescaler to 2564 => timer frequency = 168MHz/2564 = 65522 Hz (from prediv'd by 1 clocksource of 168 MHz)
    timer15.setOverflow(800); // Set overflow to 32761 => timer frequency = 65522 Hz / 32761 = 2 Hz
    timer15.attachInterrupt(OnTimer15Interrupt);
    timer15.refresh(); // Make register changes take effect
    timer15.resume(); // Start
}
void loop() {


  start_tasma(1, 275, 50);

  
  // for (licznik = 1000; licznik > 200; licznik--){
  //     // timer.setOverflow(licznik);
  //     // timer.refresh();
  //     // delay(50);

      
      
             
  // }
 
 
  // digitalWrite(TASMA_DIR, LOW);
  // digitalWrite(TASMA_DIR2, LOW);
  //   for (licznik = 1000; licznik > 200; licznik--){
  //     timer.setOverflow(licznik);
  //     timer.refresh();
  //     delay(30);
      
  // }
  // delay(1000);
  // digitalWrite(TASMA_DIR, HIGH);
  // digitalWrite(TASMA_DIR2, HIGH);
}