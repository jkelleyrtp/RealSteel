#include <Arduino.h>
#include <Servo.h>

// Set up the torso commands
#define TORSO_MOTOR_PIN 0
#define TORSO_POS_CMD 10

Servo myservo1;  // create servo object to control a servo
Servo myservo2;  // create servo object to control a servo
Servo myservo3;  // create servo object to control a servo


void setup() {
  Serial.begin(9600); 
  myservo1.attach(11);  // attaches the servo on pin 9 to the servo object
  myservo2.attach(12);  // attaches the servo on pin 9 to the servo object
  myservo3.attach(13);  // attaches the servo on pin 9 to the servo object

}

int pos = 0;    // variable to store the servo position

void loop() {
  for (pos = 60; pos <= 160; pos += 1) { // goes from 0 degrees to 180 degrees
    myservo1.write(pos);
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 120; pos >= 60; pos -= 1) { // goes from 180 degrees to 0 degrees
    myservo1.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach 
  }  
  for (pos = 60; pos <= 90; pos += 1) { // goes from 0 degrees to 180 degrees
    myservo1.write(pos);
    delay(15);                       // waits 15ms for the servo to reach the position
  }


  for (pos = 60; pos <= 160; pos += 1) { // goes from 0 degrees to 180 degrees
    myservo2.write(pos);
    myservo3.write(pos);
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 120; pos >= 60; pos -= 1) { // goes from 180 degrees to 0 degrees
    myservo2.write(pos);              // tell servo to go to position in variable 'pos'
    myservo3.write(pos);
    delay(15);                       // waits 15ms for the servo to reach 
  }  




  // if ( Serial.available() ) {
  //   switch( Serial.read() ){
  //     case TORSO_POS_CMD:

  //       break;    

  //     default:


  //       break;
  //   }  
  // }
}