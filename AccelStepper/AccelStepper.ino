/*
    Controlling multiple steppers with the AccelStepper and MultiStepper library

     by Dejan, https://howtomechatronics.com
*/

#include <AccelStepper.h>
#include <MultiStepper.h>

// Define the stepper motor and the pins that is connected to
AccelStepper stepper1(1, 2, 5); // (Typeof driver: with 2 pins, STEP, DIR)
AccelStepper stepper2(1, 3, 6);
AccelStepper stepper3(1, 4, 7);

MultiStepper steppersControl;  // Create instance of MultiStepper

long gotoposition[3]; // An array to store the target positions for each stepper motor
int MIN_STEP = 50;
int MAX_STEP;
int MIN_SPEED = 100;
int MAX_SPEED = 300;
int currentSpeed;


void setup() {

  stepper1.setMaxSpeed(300); // Set maximum speed value for the stepper
  stepper2.setMaxSpeed(300);
  stepper3.setMaxSpeed(300);

  // Adding the 3 steppers to the steppersControl instance for multi stepper control
  steppersControl.addStepper(stepper1);
  steppersControl.addStepper(stepper2);
  steppersControl.addStepper(stepper3);

  Serial.begin(9600);
}

void loop() {
  // Store the target positions in the "gotopostion" array
  stepper1.setSpeed(100);
  stepper2.setSpeed(100);
  stepper3.setSpeed(100);
  gotoposition[0] = 400;  // 400 steps - Two full rotation
  gotoposition[1] = 0;
  gotoposition[2] = 0;
  
  
  steppersControl.moveTo(gotoposition); // Calculates the required speed for all motors
  steppersControl.runSpeedToPosition(); // Blocks until all steppers are in position
  
  Serial.println(stepper1.currentPosition());
  Serial.println(stepper2.currentPosition());
  Serial.println(stepper3.currentPosition());

  delay(1000);
  
  
  gotoposition[0] = 0;
  gotoposition[1] = 0;
  gotoposition[2] = 0;

  
  steppersControl.moveTo(gotoposition);
  steppersControl.runSpeedToPosition();
  Serial.println(stepper1.currentPosition());
  Serial.println(stepper2.currentPosition());
  Serial.println(stepper3.currentPosition());
  
  delay(1000);
}
