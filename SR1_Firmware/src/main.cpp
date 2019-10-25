#include <Arduino.h>
#include <Servo.h>

// Set up the torso commands
#define TORSO_MOTOR_PIN 0
#define TORSO_POS_CMD 10



void setup() {
  Serial.begin(9600); 
}

void loop() {

  // Check 
  if ( Serial.available() ) {
    switch( Serial.read() ){
      case TORSO_POS_CMD:

        break;    

      default:


        break;
    }  
  }
}