#include "Arduino.h"
#include <Servo.h>
#include "Constants.h"

#ifndef __MIXER_H__
#define __MIXER_H__


class Mixer{
  private:

    Servo _s1;
    int _speed;
    
  public:
    Mixer(int servoPin);
    void spinForward();
    void spinBackward();
    void stopSpinning();
    void MIX_THAT_SHIT();
    int getSpeed();

};



#endif
