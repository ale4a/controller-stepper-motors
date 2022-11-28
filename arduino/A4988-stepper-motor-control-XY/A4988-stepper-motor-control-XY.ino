/* A4988 Stepper Motor Control with RS232 control
* based on code by Dejan Nedelkovski, www.HowToMechatronics.com
* modified: Alejandro Alvarez 10.10.2022
* commands:
* 'I':     query identity
* 'V':     query program version
* 'Fn': set step frequency to n (default 800 Hz)
* 
* 'PXn': set absolute position to n (default 0)
* 'RXn': move n steps relativ (sign determines direction)
* 'AXn': move to absolute position n
* 
* 'PYn': set absolute position to n (default 0)
* 'RYn': move n steps relativ (sign determines direction)
* 'AYn': move to absolute position n
* 
* 'PZn': set absolute position to n (default 0)
* 'RZn': move n steps relativ (sign determines direction)
* 'AZn': move to absolute position n
* 
* steps  - cm
* 80      0.1 cm 
* 100     0.125 cm
* 200     0.25 cm
* 1000    1.25 cm
*/

// defines pins numbers
int stepPinX = 2; 
int dirPinX = 5;
int stepPinY= 3; 
int dirPinY = 6;
int stepPinZ = 4; 
int dirPinZ = 7;
int currentFrequency; // frequency in Hz (max value 1600 Hz for half step mode)
int stepDelay;   // delay for stepper pulse duration
int secondStepDelay;  // delay for stepper pulse duration

int positionToMove; 
int steps;           
int stepNo;           // steps to do
// current position
int absPositionx;
int absPositiony;
int absPositionz;

char inCommandByte = 0;   // 1st incoming serial byte
char inAxisByte = 0;      // 2nd incomming byte
int inData = 0;
int inByteCount = 0;     // received bytes
char serBuffer[16];
String inDataStr = "";

int MIN_STEP = 20;
int MAX_STEP;
int MIN_SPEED = 12000;
int MAX_SPEED = 6000;

void setup() {
  // Sets the three pins as Outputs
  pinMode(stepPinX,OUTPUT); 
  pinMode(dirPinX,OUTPUT);
  pinMode(stepPinY,OUTPUT); 
  pinMode(dirPinY,OUTPUT);
  pinMode(stepPinZ,OUTPUT); 
  pinMode(dirPinZ,OUTPUT);

  stepDelay = 1500;
  
  // default value of position
  absPositionx = 0; 
  absPositiony = 0; 
  absPositionz = 0;
  positionToMove = 0;
  steps = 0;
  Serial.begin(9600);     // start serial port at 9600 bps and wait for port to open:
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  } 
}

void loop() {
  if (Serial.available() > 0) {
  // get incoming byte:
    delay(100);
    inByteCount = Serial.available();
    inCommandByte = Serial.read();
    if (inByteCount > 2) {
      inAxisByte = Serial.read();
      inByteCount--;
  }
  Serial.readBytes(serBuffer,inByteCount-1);
  serBuffer[inByteCount-2]='\0';
 
  String myStr=String(serBuffer);
  Serial.println(myStr);
  
  switch(inCommandByte) {
    case 'I': 
      Serial.write("Genuino Uno Rev. 3\n");
      break;
    case 'V': 
      Serial.write("Stepper A4988 - KVJ 06-2021\n");
      break;
    case 'R' :          // R: move n steps relative
      switch(inAxisByte) {
        case 'X':
          stepNo = myStr.toInt();
          moveAbsoulteNumberSteps(stepNo, stepDelay, secondStepDelay, stepPinX, dirPinX);
          absPositionx = absPositionx + stepNo;
          Serial.println("--------- Axis: X ---------" );
          showRelativePosition(myStr, steps);
          break;
        case 'Y':  
          stepNo = myStr.toInt();
          moveAbsoulteNumberSteps(stepNo, stepDelay, secondStepDelay, stepPinY, dirPinY);
          absPositiony = absPositiony + stepNo;
          Serial.println("--------- Axis: Y ---------" );
          showRelativePosition(myStr, steps);
          break;
        case 'Z':
          stepNo = myStr.toInt();
          moveAbsoulteNumberSteps(stepNo, stepDelay, secondStepDelay, stepPinZ, dirPinZ);
          absPositionz = absPositionz + stepNo;
          Serial.println("--------- Axis: Z ---------" );
          showRelativePosition(myStr, steps);
          break;
        default:
          Serial.println("No axis detected!");
          break;
      }
      break;
   // A: move to absolute position n
   case 'A':
      switch(inAxisByte) {
        case 'X':
          positionToMove = myStr.toInt();
          stepNo = positionToMove - absPositionx;
          moveAbsoulteNumberSteps(stepNo, stepDelay, secondStepDelay, stepPinX, dirPinX);
          absPositionx = positionToMove;
          Serial.println("--------- Axis: X  ---------" );
          showAbsolutePosition(myStr, steps, absPositionx);
          break;
        case 'Y': 
          positionToMove=myStr.toInt();
          stepNo = positionToMove - absPositiony;
          moveAbsoulteNumberSteps(stepNo, stepDelay, secondStepDelay, stepPinY, dirPinY);
          absPositiony = positionToMove;
          Serial.println("--------- Axis: Y  ---------" );
          showAbsolutePosition(myStr, steps, absPositiony);
          break;
        case 'Z':
          positionToMove=myStr.toInt();
          stepNo = positionToMove - absPositionz;
          moveAbsoulteNumberSteps(stepNo, stepDelay, secondStepDelay, stepPinZ, dirPinZ);
          absPositionz = positionToMove;
          Serial.println("--------- Axis: Z  ---------" );
          showAbsolutePosition(myStr, steps, absPositionz);
          break;
        default:
          Serial.println("No axis detected!");
          break;
      }
      break;  
   case 'F':
      Serial.write("new frequency: ");
      Serial.println(myStr);
      currentFrequency = myStr.toInt();
      stepDelay = 200000 / currentFrequency;
      secondStepDelay = 800000 / currentFrequency;
      Serial.write("step delay: ");
      Serial.println(stepDelay + secondStepDelay);
      break;
   case 'P':
      switch(inAxisByte) {
        case 'X':
          Serial.write("Set position: ");
          Serial.println(myStr);
          positionToMove = myStr.toInt();
          absPositionx = positionToMove;
          Serial.write("Position set to: ");
          Serial.println(absPositionx);
          break;
        case 'Y': 
          Serial.write("Set position: ");
          Serial.println(myStr);
          positionToMove = myStr.toInt();
          absPositiony = positionToMove;
          Serial.write("Position set to: ");
          Serial.println(absPositiony);
          break;
        case 'Z':
          Serial.write("Set position: ");
          Serial.println(myStr);
          positionToMove = myStr.toInt();
          absPositionz = positionToMove;
          Serial.write("Position set to: ");
          Serial.println(absPositionz);
          break;
        default:
          Serial.println("No axis detected!");
          break;
      }    
      break;     
   default:
      Serial.println("Nothing detected!");
      break;
   }
   Serial.flush();
   myStr="";
  }
  inByteCount=0;
}

void showRelativePosition(String myStr, int numberSteps){
  Serial.write("Relative Steps: ");
  Serial.println(myStr);
  Serial.write("Steps done: ");
  Serial.println(numberSteps);
  Serial.write("New position: ");
  Serial.println(absPositionx);
}

void showAbsolutePosition(String myStr, int numberSteps, int absPosition){
  Serial.write("Absolute position: ");
  Serial.println(myStr);
  Serial.write("Steps to do: ");
  Serial.println(numberSteps);
  Serial.write("New position: ");
  Serial.println(absPosition);
}


int getSpeed(int currentStep, int totalStep){
  int currentSpeed = 0;
  if(totalStep < 500)
    return MIN_SPEED;
  if( currentStep <= MIN_STEP ){
    return map(currentStep, 0, MIN_STEP, MIN_SPEED, MAX_SPEED);
  }
  MAX_STEP = totalStep - MIN_STEP;
  if (currentStep >= MAX_STEP){
     return map(currentStep, MAX_STEP, totalStep, MAX_SPEED, MIN_SPEED);
  }
  return MAX_SPEED;
}

int moveAbsoulteNumberSteps(int stepsNumberToDo, int stepDelay, int secondStepDelay, int stepPin, int directionPin){
  if (stepsNumberToDo > 0) {
    digitalWrite(directionPin, LOW); // clockwise direction
  } else {
    digitalWrite(directionPin,HIGH); // anticlockwise direction
  }
  for(int x = 0; x < abs(stepsNumberToDo); x++) {
    int currentStepDelay = getSpeed(x, abs(stepsNumberToDo)) / 2;
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(currentStepDelay); 
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(currentStepDelay); 
  }
}
