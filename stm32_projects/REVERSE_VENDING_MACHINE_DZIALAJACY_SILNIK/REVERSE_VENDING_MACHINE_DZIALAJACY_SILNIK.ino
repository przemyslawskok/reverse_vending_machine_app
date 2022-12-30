// PRZERWANIA 
HardwareTimer timer(TIM1);
HardwareTimer timer15(TIM15);

uint16_t licznik = 800;
volatile uint16_t licznik2 = 0;
volatile uint16_t licznik_led = 0;
uint8_t flaga = 0;
uint8_t flaga_led = 0;
bool toggle = false;
bool toggle_led = false;

int Bajt = 0;
//----

// BELKI TENSOMETRYCZNE
#include "HX711.h"
const int BT1_SCK = PA8;
const int BT1_DT = PB6;
const int BT2_SCK = PB14;
const int BT2_DT = PB15;
const int BT3_SCK = PB4;
const int BT3_DT = PB10;
const int BT4_SCK = PB5;
const int BT4_DT = PB13;
HX711 BT1;
HX711 BT2;
HX711 BT3;
HX711 BT4;
//----

// LED
const int RING_LED_WS = PC3; 
//----


// SILNIK KROKOWY
#include <AccelStepper.h>
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

AccelStepper tasma(1,TASMA_STEP,TASMA_DIR);
TMC2208Stepper driver(&SERIAL_PORT, 0.11f);    

AccelStepper tasma2(1,TASMA_STEP2,TASMA_DIR2);
TMC2208Stepper driver2(&SERIAL_PORT2, 0.11f);    
//----

// MOSFETY
const int OUT_MOS_1 = PD9;
const int OUT_MOS_2 = PC5;
const int OUT_MOS_3 = PD8;
const int OUT_MOS_4 = PB2;
//----

// PRZEKAZNIKI
const int T_PK_1 = PC0;
const int T_PK_2 = PC7;
const int T_PK_3 = PB3;
//----

// SWITCH
const int IN_SW_1 = PC2;
//----

// CZUJNIKI
const int IN_PHOTO_HAND = PB1;
const int IN_PHOTO_BOTTLE = PB7;
//----

// REZERWOWE
const int IN_RES_1 = PD4;
const int IN_RES_2 = PD3;
const int IN_RES_3 = PD1;
const int IN_RES_4 = PD0;
const int IN_RES_5 = PA14;
const int IN_RES_6 = PD2;
const int IN_RES_7 = PC12;
const int IN_RES_8 = PC11;
const int IN_RES_9 = PC10;
//----s

void setup() {

  // KOMUNIKACJA
  Serial.begin(115200);
  // Serial2.begin(115200);
  Serial.println("Inicjacja programu");
  //----


  //LED
  pinMode(LED_BUILTIN,OUTPUT);
  //----

  // MOSFETY
  pinMode(OUT_MOS_1,OUTPUT);
  pinMode(OUT_MOS_2,OUTPUT); 
  pinMode(OUT_MOS_3,OUTPUT); 
  pinMode(OUT_MOS_4,OUTPUT); 
  //----


  // BELKI TENSOMETRYCZNE
  BT1.begin(BT1_DT,BT1_SCK);
  BT2.begin(BT2_DT,BT2_SCK);
  BT3.begin(BT3_DT,BT3_SCK);
  BT4.begin(BT4_DT,BT4_SCK);
  //----

  // PRZEKAZNIKI 
  pinMode(T_PK_1,OUTPUT);
  pinMode(T_PK_2,OUTPUT); 
  pinMode(T_PK_3,OUTPUT); 
  //----

   
  // SWITCH
  pinMode(IN_SW_1,INPUT_PULLUP);
  //----
  
  
  // CZUJNIKI
  pinMode(IN_PHOTO_HAND,INPUT_PULLUP);
  pinMode(IN_PHOTO_BOTTLE,INPUT_PULLUP);
  //----

  // REZERWOWE
  pinMode(IN_RES_1,INPUT_PULLUP);
  pinMode(IN_RES_2,INPUT_PULLUP);
  pinMode(IN_RES_3,INPUT_PULLUP);
  pinMode(IN_RES_4,INPUT_PULLUP);
  pinMode(IN_RES_5,INPUT_PULLUP);
  pinMode(IN_RES_6,INPUT_PULLUP);
  pinMode(IN_RES_7,INPUT_PULLUP);
  pinMode(IN_RES_8,INPUT_PULLUP);
  pinMode(IN_RES_9,INPUT_PULLUP);
  //----



  // SILNIK KROKOWY
  pinMode(TASMA_EN, OUTPUT);
  pinMode(TASMA_STEP, OUTPUT);
  pinMode(TASMA_DIR, OUTPUT);

  pinMode(TASMA_EN2, OUTPUT);
  pinMode(TASMA_STEP2, OUTPUT);
  pinMode(TASMA_DIR2, OUTPUT);


  Serial3.begin(115200);
  Serial4.begin(115200);

  driver.begin();
  driver.toff(5);
  driver.rms_current(1500);
  driver.microsteps(32);
  driver.pwm_autoscale(true);
  driver.en_spreadCycle(true); 
  
  driver2.begin();
  driver2.toff(5);
  driver2.rms_current(1500);
  driver2.microsteps(32);
  driver2.pwm_autoscale(true);
  driver2.en_spreadCycle(true); 


  stop_tasma();  
  // ----

  // TIMERY
  timer.setPrescaleFactor(4); // Set prescaler to 2564 => timer frequency = 168MHz/2564 = 65522 Hz (from prediv'd by 1 clocksource of 168 MHz)
  timer.setOverflow(1500); // Set overflow to 32761 => timer frequency = 65522 Hz / 32761 = 2 Hz
  timer.attachInterrupt(sterowanie_silnikiem_interrupt);
  timer.refresh(); // Make register changes take effect
  timer.resume(); // Start

  timer15.setPrescaleFactor(2); // Set prescaler to 2564 => timer frequency = 168MHz/2564 = 65522 Hz (from prediv'd by 1 clocksource of 168 MHz)
  timer15.setOverflow(800); // Set overflow to 32761 => timer frequency = 65522 Hz / 32761 = 2 Hz
  timer15.attachInterrupt(sterowanie_silnikiem_interrupt2);
  timer15.refresh(); // Make register changes take effect
  timer15.resume(); // Start
  // ----



  // ROZGRZANIE /TEST
  // start_tasma(1, 275, 50);
  // delay(5000);
  // stop_tasma();
  // -----

}

void loop() {

  if (licznik_led == 10000)
  {
    
    toggle_led = !toggle_led;
    digitalWrite(LED_BUILTIN, toggle_led ? HIGH : LOW);
    licznik_led = 0;
  }






  if (Serial.available())
    {   
        Bajt = Serial.read();
        
    }
  if (Bajt == 65)
  {
    start_tasma(1, 275, 50);
    Bajt = 0;
  }
  else if (Bajt == 66)
  {
    start_tasma(0, 275, 50);
    Bajt = 0;         
  } 
  else if (Bajt == 67)
  {
    stop_tasma();
    Bajt = 0;         
  }
  else if (Bajt == 68)
  {
    
  }
  else if (Bajt == 69)
  {
    String value = "e" + String(BT1.get_units()+BT2.get_units()) + "e";
    Serial.println(value);
    Bajt = 0;        
  }
  else if (Bajt == 70)
  {
    //photo_in_hand sensor
    //Serial.println(analogRead(IN_PHOTO_HAND));
    Serial.println("f1f");
    Bajt = 0;
  }  
}









void sterowanie_silnikiem_interrupt() {
    toggle = !toggle;
    digitalWrite(TASMA_STEP, toggle ? HIGH : LOW);
    digitalWrite(TASMA_STEP2, toggle ? HIGH : LOW);

    // if (licznik_led == 1)
    // {
      
    //   toggle_led = !toggle_led;
    //   digitalWrite(LED_BUILTIN, toggle_led ? HIGH : LOW);
    //   licznik_led = 0;
    // }
  
}
void sterowanie_silnikiem_interrupt2() {
    //Serial.println(licznik2);
    licznik2++;
    licznik_led++;     
}






void start_tasma(uint8_t kierunek, uint16_t predkosc, uint16_t przyspieszenie)
{ 

  
  digitalWrite(TASMA_EN, LOW);
  digitalWrite(TASMA_EN2, LOW);


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
void stop_tasma()
{
  digitalWrite(TASMA_EN, HIGH);
  digitalWrite(TASMA_EN2, HIGH);  
}



