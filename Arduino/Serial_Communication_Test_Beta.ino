#include <Servo.h>
//Servo set up
Servo servoC;
Servo servoZ;
int angle = 0;
int newAngle = 0;
const int MaxChars = 4;
char strValue[MaxChars + 1];
int index = 0;

boolean cAng = false;
boolean xAng = false;
boolean yAng = false;
boolean zAng = false;

int setPoint = 55;

void setup() {
  Serial.begin(9600);
  servoC.attach(10);
  servoZ.attach(12);
  angle = 90;
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
      strValue[index++] = c;
    }
    else {
      strValue[index] = 0;
      angle = atoi(strValue);
      newAngle = angle;

      
      if (!(cAng || xAng || yAng || zAng)){
        cAng = true;
      }

      if (cAng == true) {
        Serial.print("Arduino received C Value: ");
        Serial.println(angle);
        newAngle = (angle / 10) * 20;
        servoC.write(newAngle);
        xAng = true;
        cAng = false;
      }
      else if (xAng == true) {
        Serial.print("Arduino received X Value: ");
        Serial.println(angle);
        //myservo.write(newAngle);
        yAng = true;
        xAng = false;
      }
      else if (yAng == true) {
        Serial.print("Arduino received Y Value: ");
        Serial.println(angle);
        //myservo.write(newAngle);
        zAng = true;
        yAng = false;
      }
      else if (zAng == true) {
        Serial.print("Arduino received Z Value: ");
        Serial.println(angle);
        servoZ.write(newAngle);
        zAng = false;
      }


      strValue;
      index = 0;

      Serial.print("Arduino sends: ");
      Serial.println(angle);
      Serial.print("\n");
      Serial.flush();
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


