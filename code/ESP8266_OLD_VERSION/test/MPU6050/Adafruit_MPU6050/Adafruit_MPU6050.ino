#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;
sensors_event_t a, g, temp;

void setup() {
  Serial.begin(9600);
  Serial.println("***Adafruit_MPU6050 Test***");
  if (!mpu.begin()) {
    Serial.println("MPU6050 not Found.");
    delay(1000);
  }
  Serial.println("MPU6050 Found!");
}

void loop() {
  mpu.enableSleep(false);
  mpu.getEvent(&a, &g, &temp);
  Serial.print("Ratation X: ");
  Serial.print(g.gyro.x);
  Serial.print("\tAcceleration X: ");
  Serial.print(a.acceleration.x);
  Serial.print("\tTemperature: ");
  Serial.println(temp.temperature);

  delay(500);
}
