// (c) Michael Schoeffler 2017, http://www.mschoeffler.de

#include "Wire.h" // This library allows you to communicate with I2C devices.

int VRx = A0;
int VRy = A1;
int jSW = 2;
int bSW = 12;
int xPosition, yPosition, jSW_state, bSW_state, mapX, mapY, X, Y;
const int MPU_ADDR = 0x68; // I2C address of the MPU-6050. If AD0 pin is set to HIGH, the I2C address will be 0x69.

int16_t accelerometer_x, accelerometer_y, accelerometer_z; // variables for accelerometer raw data
int16_t gyro_x, gyro_y, gyro_z; // variables for gyro raw data
int16_t temperature; // variables for temperature data

char tmp_str[7]; // temporary variable used in convert function

char* convert_int16_to_str(int16_t i) { // converts int16 to string. Moreover, resulting strings will have the same length in the debug monitor.
  sprintf(tmp_str, "%6d", i);
  return tmp_str;
}

void setup() {
  Serial.begin(9600);
  Wire.begin();
  Wire.beginTransmission(MPU_ADDR); // Begins a transmission to the I2C slave (GY-521 board)
  Wire.write(0x6B); // PWR_MGMT_1 register
  Wire.write(0); // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);

  pinMode(VRx, INPUT);
  pinMode(VRy, INPUT);
  pinMode(jSW, INPUT_PULLUP); 
  pinMode(bSW, INPUT_PULLUP);
}
void loop() {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B); // starting with register 0x3B (ACCEL_XOUT_H) [MPU-6000 and MPU-6050 Register Map and Descriptions Revision 4.2, p.40]
  Wire.endTransmission(false); // the parameter indicates that the Arduino will send a restart. As a result, the connection is kept active.
  Wire.requestFrom(MPU_ADDR, 7*2, true); // request a total of 7*2=14 registers
  
  // "Wire.read()<<8 | Wire.read();" means two registers are read and stored in the same variable
  accelerometer_x = Wire.read()<<8 | Wire.read(); // reading registers: 0x3B (ACCEL_XOUT_H) and 0x3C (ACCEL_XOUT_L)
  accelerometer_y = Wire.read()<<8 | Wire.read(); // reading registers: 0x3D (ACCEL_YOUT_H) and 0x3E (ACCEL_YOUT_L)
  accelerometer_z = Wire.read()<<8 | Wire.read(); // reading registers: 0x3F (ACCEL_ZOUT_H) and 0x40 (ACCEL_ZOUT_L)
  temperature = Wire.read()<<8 | Wire.read(); // reading registers: 0x41 (TEMP_OUT_H) and 0x42 (TEMP_OUT_L)
  gyro_x = Wire.read()<<8 | Wire.read(); // reading registers: 0x43 (GYRO_XOUT_H) and 0x44 (GYRO_XOUT_L)
  gyro_y = Wire.read()<<8 | Wire.read(); // reading registers: 0x45 (GYRO_YOUT_H) and 0x46 (GYRO_YOUT_L)
  gyro_z = Wire.read()<<8 | Wire.read(); // reading registers: 0x47 (GYRO_ZOUT_H) and 0x48 (GYRO_ZOUT_L)
  
  // Read Joystick Data
  xPosition = analogRead(VRx);
  yPosition = analogRead(VRy);
  jSW_state = digitalRead(jSW);
  bSW_state = digitalRead(bSW);
  // mapX = map(xPosition, 0, 1023, -512, 512);
  // mapY = map(yPosition, 0, 1023, -512, 512);
  mapX = map(xPosition, 0, 663, -331, 331);
  mapY = map(yPosition, 0, 663, -331, 331);  
  mapX = mapX + 7; //manual calibration
  mapY = mapY + 1 ; //manual calibration
  if (mapX > 300) {
    X = 300;        
  } else if (mapX < -300) {
    X = -300;
  } else {
    X = mapX  ;  
  }

  if (mapY > 300) {
    Y = 300;        
  } else if (mapY < -300) {
    Y = -300;
  } else {
    Y = mapY;
  }

  // print out data
  Serial.print("X:");
  Serial.print(X);
  Serial.print("Y:");
  Serial.print(Y);
  Serial.print("R:"); Serial.print(convert_int16_to_str(accelerometer_x));
  Serial.print("P:"); Serial.print(convert_int16_to_str(accelerometer_y));
  Serial.print("A:"); Serial.print(bSW_state);
  Serial.print("B:");
  Serial.print(jSW_state);  
  //Serial.print("|aZ="); Serial.print(convert_int16_to_str(accelerometer_z));
  // the following equation was taken from the documentation [MPU-6000/MPU-6050 Register Map and Description, p.30]
  //Serial.print("|tmp ="); Serial.print(temperature/340.00+36.53);
  // Serial.print("|gX="); Serial.print(convert_int16_to_str(gyro_x));
  // Serial.print("|gY="); Serial.print(convert_int16_to_str(gyro_y));
  // Serial.print("|gZ="); Serial.print(convert_int16_to_str(gyro_z));
  // Serial.print("~");
  Serial.println();
  
  // delay none
}