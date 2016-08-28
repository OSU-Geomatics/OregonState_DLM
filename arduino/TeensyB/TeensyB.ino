#include <Wire.h> // Must include Wire library for I2C
#include <SparkFun_MMA8452Q.h> // Includes the SFE_MMA8452Q library

// Global Constants
MMA8452Q accelC(0x1C);
MMA8452Q accelD(0x1D);

const long BAUD = 921600;
const byte TXPIN = 10;
const byte RXPIN = 9;
const byte LEDPIN = 13;

unsigned long startTime = 0;

char accelIDc = 'c';
char accelIDd = 'd';

void setup() {
  // Sync Data
  pinMode(RXPIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(RXPIN), syncTime, RISING);
  pinMode(LEDPIN, OUTPUT);
  digitalWrite(LEDPIN, HIGH);
  
  delay(5000); //wait 5 seconds to get a sync trigger

  digitalWrite(LEDPIN, HIGH);
  
  if (startTime!=0) {
    accelIDc = 'C';
    accelIDd = 'D';
  }
  
  // Open Port for transmitting data
  Serial.begin(BAUD);
  accelD.init(SCALE_8G, ODR_200);
  accelC.init(SCALE_8G, ODR_200);
}


void loop()
{
  if (accelC.available())
  {
    accelC.read();
    long curTime = millis() - startTime;
    printCalculatedAccels(accelC, accelIDc, curTime);
  }
  
  if (accelD.available())
  {
    accelD.read();
    long curTime = millis() - startTime;
    printCalculatedAccels(accelD, accelIDd, curTime);
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

void syncTime() {
  startTime = millis();
  digitalWrite(LEDPIN, LOW);
}

