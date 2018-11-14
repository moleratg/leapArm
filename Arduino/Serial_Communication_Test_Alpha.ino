#include <Servo.h>
//Servo set up
Servo servoC;
Servo servoZ;
int angle_c = 0;
int angle_x = 0;
int angle_y = 0;
int angle_z = 0;

int newAngle_c = 0;
const int MaxChars = 13;
char strValue[MaxChars + 1];
int index = 0;

int count = 0;

int setPoint = 55;

void setup() {
  Serial.begin(9600);
  servoC.attach(10);
  servoZ.attach(12);

}

void loop()
{
  while (!Serial.available())
  {

  }
  // Serial read section
  while (Serial.available())
  {
    char c = Serial.read();
    if (index < MaxChars && isDigit(c)) {
      strValue[index] = c;
      index++;
    }
    else if (c == 'c') {
      strValue[index] = 0;
      angle_c = atoi(strValue);
      strValue;
      index = 0;
    }
    else if (c == 'x') {
      strValue[index] = 0;
      angle_x = atoi(strValue);
      strValue;
      index = 0;
    }
    else if (c == 'y') {
      strValue[index] = 0;
      angle_y = atoi(strValue);
      strValue;
      index = 0;
    }

    else {
      strValue[index] = 0;
      angle_z = atoi(strValue);

      if (angle_c > 0) {
        Serial.print("C: ");
        Serial.println(angle_c);
        newAngle_c = (angle_c / 10) * 20;
        servoC.write(newAngle_c);
      }
      if (angle_x > 0) {
        Serial.print("X: ");
        Serial.println(angle_x);
        //servoX.write(angle_x);
      }
      if (angle_y > 0) {
        Serial.print("Y: ");
        Serial.println(angle_y);
        //servoY.write(angle_y);
      }
      if (angle_z > 0) {
        Serial.print("Z: ");
        Serial.println(angle_z);
        servoZ.write(angle_z);
      }

      strValue;
      index = 0;

    }
  }


  /* if(newAngle > 0 && newAngle < 180){
         if(newAngle < angle){
           for(; angle > newAngle; angle -=1) {
             myservo.write(angle);
           }
         }
         else {
           for(; angle < newAngle; angle +=1){
             myservo.write(angle);
           }
         }
       }
  */


}


