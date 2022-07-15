#include "PCA9685.h"

//servo servos[12];
servo* servos; //12-servo dynamic array
PCA9685 pwm(12);  //12 servos

void setup() {
  Serial.begin(9600);

  servos  = new servo [12];
  for (int i = 0; i < 12; i++) {
    uint8_t servo_attach = 4 * (i / 3) + (i % 3); //servo_number
    const String limb_loc[4] = {"front_right_", "front_left_", "back_right_", "back_left_"};
    const String limb_part[3] = {"hip", "thigh", "calf"};
    String servo_name = limb_loc[i / 3] + limb_part[i % 3]; //servo_name

    servos[i] = servo(servo_attach, servo_name, 0);
  }
  servos[0].setDisplacement(-35);
  servos[1].setDisplacement(-5);
  servos[2].setDisplacement(-5);
  servos[3].setDisplacement(35);
  servos[4].setDisplacement(5);
  servos[5].setDisplacement(5);
  servos[6].setDisplacement(20);
  servos[7].setDisplacement(-5);
  servos[8].setDisplacement(-5);
  servos[9].setDisplacement(-30);
  servos[10].setDisplacement(5);
  servos[11].setDisplacement(0);

  pwm.begin(servos);
}

void loop() {
  pwm.locateServos();
  pwm.update();
  delay(5000);
  pwm.initServos();
  pwm.update();
  delay(5000);
}
