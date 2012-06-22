#include "Mixer.h"
#include "Arduino.h"
#include "Constants.h"

#include <Servo.h>

Mixer::Mixer(int servoPin){
  _s1.attach(servoPin);
  _s1.write(95);//figure out expiremental stop value;
}

void Mixer::spinForward(){
  _s1.write(FULL_SPEED);
}
void Mixer::spinBackward(){
  _s1.write(FULL_REVERSE);
}

void Mixer::stopSpinning(){
  _s1.write(STOP_SPIN);
}

int Mixer::getSpeed(){
  return _s1.read();
}

void Mixer::MIX_THAT_SHIT(){
  for(int i =0; i < 2; i++){
    spinForward();
      delay(SPIN_TIME);
    spinBackward();
      delay(SPIN_TIME);
  }
}

