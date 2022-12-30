


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
const int TASMA_DIR = PC13;
const int TASMA_STEP = PD5;
const int TASMA_EN = PA4;
const int MS1 = PA1;
const int MS2 = PA0;

AccelStepper tasma(1,TASMA_STEP,TASMA_DIR);
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
  Serial2.begin(115200);
  Serial.println("Inicjacja programu");
  //----


  //TEST
  pinMode(TASMA_EN,OUTPUT);
  pinMode(MS1,OUTPUT);
  pinMode(MS2,OUTPUT);
  digitalWrite(TASMA_EN,LOW);
  digitalWrite(MS1,HIGH);
  digitalWrite(MS2,HIGH);  
  //----

  // MOSFETY
  pinMode(OUT_MOS_1,OUTPUT);
  pinMode(OUT_MOS_2,OUTPUT); 
  pinMode(OUT_MOS_3,OUTPUT); 
  pinMode(OUT_MOS_4,OUTPUT); 
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
  tasma.setMaxSpeed(60000);
  tasma.setAcceleration(15000);

  tasma.moveTo(tasma.currentPosition()+400000);  
  //


}

void loop() {

  if (Serial.available() > 0)
    {
        int Bajt = Serial.read();
        Serial.print("Otrzymalem: ");
        Serial.println(Bajt, DEC);
        if (Bajt == 43){
          tasma.moveTo(tasma.currentPosition()+40000);
        }
        else if (Bajt == 45 )
        {
          tasma.moveTo(tasma.currentPosition()-40000);          
        }
        else if (Bajt == 49 )
        {
          digitalWrite(OUT_MOS_1,HIGH);
        }
        else if (Bajt == 50 )
        {
          digitalWrite(OUT_MOS_2,HIGH);
        }
        else if (Bajt == 51 )
        {
          digitalWrite(OUT_MOS_3,HIGH);
        }
        else if (Bajt == 52 )
        {
          digitalWrite(OUT_MOS_4,HIGH);
        }
        else if (Bajt == 53 )
        {
          digitalWrite(OUT_MOS_1,LOW);
        }
        else if (Bajt == 54 )
        {
          digitalWrite(OUT_MOS_2,LOW);
        }
        else if (Bajt == 55 )
        {
          digitalWrite(OUT_MOS_3,LOW);
        }
        else if (Bajt == 56 )
        {
          digitalWrite(OUT_MOS_4,LOW);
        }
        else if (Bajt == 122 )
        {
          digitalWrite(T_PK_1,HIGH);
        }
        else if (Bajt == 120 )
        {
          digitalWrite(T_PK_2,HIGH);
        }
        else if (Bajt == 99 )
        {
          digitalWrite(T_PK_3,HIGH);
        }
        
        else if (Bajt == 118 )
        {
          digitalWrite(T_PK_1,LOW);
        }
        else if (Bajt == 98 )
        {
          digitalWrite(T_PK_2,LOW);
        }
        else if (Bajt == 110 )
        {
          digitalWrite(T_PK_3,LOW);
        }

      

    }


  tasma.run();
}
