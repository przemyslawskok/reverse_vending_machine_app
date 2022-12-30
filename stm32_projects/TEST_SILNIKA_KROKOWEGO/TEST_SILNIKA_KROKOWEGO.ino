// Bounce.pde
// -*- mode: C++ -*-
//
// Make a single stepper bounce from one limit to another
//
// Copyright (C) 2012 Mike McCauley
// $Id: Random.pde,v 1.1 2011/01/05 01:51:01 mikem Exp mikem $

#include <AccelStepper.h>

// Define a stepper and the pins it will use
AccelStepper stepper(1,PD5,PC13); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5

void setup()
{ 

  Serial.begin(115200);
  pinMode(PA4,OUTPUT);
  digitalWrite(PA4,LOW);
  // Change these to suit your stepper if you want
  stepper.setMaxSpeed(40000);
  stepper.setAcceleration(1000);
  stepper.moveTo(10000);
}

void loop()
{
    // if(Serial.available() == 4){
    
    //   Serial.println(Serial.available(),DEC);
    // }
    if (Serial.available() > 0)
    {
        int Bajt = Serial.read();
        Serial.print("Otrzymalem: ");
        Serial.println(Bajt, DEC);
        if (Bajt == 43){
          Serial.println(stepper.currentPosition());
          stepper.moveTo(stepper.currentPosition()+20000);
        }
        else if (Bajt == 45 )
        {
          Serial.println(stepper.currentPosition());
          stepper.moveTo(stepper.currentPosition()-20000);          
        }
      

    }
    // // If at the end of travel go to the other end
    stepper.run();
}