#ifndef PCA9685_H
#define PCA9685_H

#include <Adafruit_PWMServoDriver.h>

class servo;
class PCA9685;

class servo {
  private:
    uint8_t Number;  //the attach number on PCA9685, 0~15
    //real_angle = Angle + Displacement
    float Angle; //-90~90
    float Displacement; //angle displacement
    String Name;
    bool AngleChange = true;
  public:
    servo(uint8_t Servo_num = 16, String Servo_name = "Not_Set", float Servo_displacement = 0, float Servo_angle = 0);
    servo(const servo&);  //copy constructor
    servo& operator=(const servo&); //assignment operator
    servo& setName(String Servo_name); //allow cascaded
    servo& setServoNum(uint8_t Servo_num); //allow cascaded
    servo& setDisplacement(float Servo_displacement);  //allow cascaded
    servo& setAngle(float Servo_angle);  //allow cascaded
    servo& resumeAngleChange();  //allow cascaded
    String getName() const;
    float getAngle() const;
    float getDisplacement() const;
    uint8_t getServoNum() const;
    bool isAngleChange() const;
};

class PCA9685 {
  private:
    //static const uint8_t servo_quantity = 12;
    const uint8_t servo_quantity;
    Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();  //Use default address 0x40.
    //servo Servos[servo_quantity];  //dynamic array to store servos
    servo* Servos; //dynamic array to store servos
  public:
    //PCA9685() {};
    PCA9685(uint8_t );
    ~PCA9685();
    //void begin(servo [servo_quantity]);
    void begin(servo*);
    void locateServos();  //locating limbs
    void initServos();  //initiate limbs
    void update();
};
# endif
