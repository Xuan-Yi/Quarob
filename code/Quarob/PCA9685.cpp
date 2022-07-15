#include "PCA9685.h"

servo::servo(uint8_t Servo_num, String Servo_name, float Servo_displacement, float Servo_angle) {
  Number = Servo_num;
  Angle = Servo_angle;
  Displacement = Servo_displacement;
  Name = Servo_name;
}

servo::servo(const servo& old_servo) {
  Number = old_servo.Number;
  Angle = old_servo.Angle;
  Name = old_servo.Name;
}

servo& servo::operator=(const servo& old_servo) {
  if (this == &old_servo)
    return *this;
  else {
    Number = old_servo.Number;
    Angle = old_servo.Angle;
    Name = old_servo.Name;
    return *this;
  }
}

servo& servo::setName(String Servo_name) {
  Name = Servo_name;
  return *this;
}

servo& servo::setServoNum(uint8_t Servo_num) {
  Number = Servo_num;
  return *this;
}

servo& servo::setDisplacement(float Servo_displacement) {
  Displacement = Servo_displacement;
  return *this;
}

servo& servo::setAngle(float Servo_angle) {
  if (Servo_angle == Angle)
    return *this;
  else {
    Angle = Servo_angle;
    AngleChange = true;
    return *this;
  }
}

servo& servo::resumeAngleChange() {
  AngleChange = false;
  return *this;
}

String servo::getName() const {
  return Name;
}

float servo::getAngle() const {
  return Angle;
}

float servo::getDisplacement() const {
  return Displacement;
}

uint8_t servo::getServoNum() const {
  return Number;
}

bool servo::isAngleChange() const {
  return AngleChange;
}

#define MIN_PULSE_WIDTH 510  //us
#define MAX_PULSE_WIDTH 2410 //us
#define SERVO_FREQ 50  // frequency of square waves

PCA9685::PCA9685(uint8_t n): servo_quantity(n) {
  Servos = new servo[servo_quantity];
}

PCA9685::~PCA9685() {
  delete [] Servos;
}

/*void PCA9685::begin(servo servo_set[servo_quantity]) {
  for (int i = 0; i < servo_quantity; i++)
    Servos[i] = servo_set[i];
  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ);
  delay(10);
  }*/

void PCA9685::begin(servo* servo_set) {
  Servos = servo_set;
  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ);
  delay(10);
}

void PCA9685::locateServos() {
  for (int i = 0; i < servo_quantity; i++)
    Servos[i].setAngle(0);
}

void PCA9685::initServos() {
  for (int i = 0; i < servo_quantity; i++) {
    if (i % 3 != 1)
      Servos[i].setAngle(0);
  }
  Servos[1].setAngle(-45);
  Servos[4].setAngle(45);
  Servos[7].setAngle(-45);
  Servos[10].setAngle(45);
}

uint16_t angle_to_pulsewidth_(float angle) {
  //angle = -90~90
  int pulsewidth = map(angle, -90, 90, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH);
  return uint16_t(float(pulsewidth) / 1000000 * SERVO_FREQ * 4096);
}

void PCA9685::update() {
  for (int i = 0; i < servo_quantity; i++) {
    if (Servos[i].isAngleChange()) {
      pwm.setPWM(Servos[i].getServoNum(), 0, angle_to_pulsewidth_(Servos[i].getAngle() + Servos[i].getDisplacement()));
      Servos[i].resumeAngleChange();
    }
  }
}
