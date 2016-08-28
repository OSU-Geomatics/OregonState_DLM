#include <Wire.h> // Must include Wire library for I2C
#include <SparkFun_MMA8452Q.h> // Includes the SFE_MMA8452Q library

// Global Constants
MMA8452Q accelA(0x1C);
MMA8452Q accelB(0x1D);

const long BAUD = 921600;
const byte TXPIN = 10;
const byte RXPIN = 9;
const byte LEDPIN = 13;

unsigned long startTime = 0;

char accelIDa = 'A';
char accelIDb = 'B';


void setup() {
  // Sync Data
  pinMode(TXPIN, OUTPUT);
  pinMode(LEDPIN, OUTPUT);
  
  delay(2000); //wait 2 seconds before sending trigger pulse
  digitalWrite(TXPIN, HIGH);
  startTime = millis();
  digitalWrite(LEDPIN, HIGH);
  delay(100);
  digitalWrite(TXPIN, LOW);
  digitalWrite(LEDPIN, LOW);
  delay(2900);// total of 5 seconds before starting acquisition
  
  // Open Port for transmitting data
  Serial.begin(BAUD);
  accelB.init(SCALE_8G, ODR_200);
  accelA.init(SCALE_8G, ODR_200);
}


void loop()
{
  if (accelA.available())
  {
    accelA.read();
    long curTime = millis() - startTime;
    printCalculatedAccels(accelA, accelIDa, curTime);
  }
  
  if (accelB.available())
  {
    accelB.read();
    long curTime = millis() - startTime;
    printCalculatedAccels(accelB, accelIDb, curTime);
  }  
}

void printCalculatedAccels(MMA8452Q accel, char accelID, long curTime)
{
  Serial.print(accelID);
  Serial.print(",");
  Serial.print(curTime);
  Serial.print(",");
  Serial.print(accel.cx, 3);
  Serial.print(",");
  Serial.print(accel.cy, 3);
  Serial.print(",");
  Serial.println(accel.cz, 3);
}
