//#include <Wire.h> (needn't this library if default address 0x40 is assigned)
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(); //default 0x40

#define MIN_PULSE_WIDTH 510  //us
#define MAX_PULSE_WIDTH 2410 //us
#define SERVO_FREQ 50  // frequency of square waves

int angle = 90;

uint16_t angle_to_pulsewidth(int angle) {
  int pulsewidth = map(float(angle), 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH);
  return uint16_t(float(pulsewidth) / 1000000 * SERVO_FREQ * 4096);
}

void setup() {
  Serial.begin(9600);
  Serial.println("PCA9685 Servo Driver Test!");
  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates
  delay(10);
  for (uint8_t servo_num = 0; servo_num < 16; servo_num++)
    pwm.setPWM(servo_num, 0, angle_to_pulsewidth(90));
  Serial.println("Servos set to 90 deg.");
  Serial.println("---Test Start---");
}

void loop() {
  if (Serial.available()) {
    switch (Serial.read()) {
      case '0':
        angle  = 0;
        break;
      case '9':
        angle = 90;
        break;
      case '1':
        angle = 180;
        break;
    }
    delay(100);
    Serial.print("Degree: ");
    Serial.print(angle);
    Serial.print("\tPulse width: ");
    Serial.println(angle_to_pulsewidth(angle));
  }
  for (uint8_t servo_num = 0; servo_num < 16; servo_num++)
    pwm.setPWM(servo_num, 0, angle_to_pulsewidth(angle));
}
