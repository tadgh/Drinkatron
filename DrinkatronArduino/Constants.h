//Serial Comms CONSTANTS
#ifndef __CONSTANTS_H__
#define __CONSTANTS_H__

#include "Arduino.h"

const int SERIAL_DELAY = 5;
const int BAUD_RATE = 9600;
const int NUM_DRINKS = 5;


//DRINK CONSTANTS
const int  ING1_RELAY_PIN = 51;
const int  ING2_RELAY_PIN = 49;
const int  ING3_RELAY_PIN = 47;
const int  ING4_RELAY_PIN = 45;
const int  ING5_RELAY_PIN = 43;
const int  ING6_RELAY_PIN = 41;
const int  ING7_RELAY_PIN = 39;
const int  ING8_RELAY_PIN = 37;
const int  ING9_RELAY_PIN = 50;
const int  ING10_RELAY_PIN = 48;
const int  ING11_RELAY_PIN = 46;
const int  ING12_RELAY_PIN = 44;

const int  MASTER_DISPENSE_PIN =  24; //this is a currently useless pin

const int  LOWVIS_DELAY = 65; //THIS IS SOLELY EXPERIMENTAL AS WE ARE USING LARGER VALUES OF THING
const int  MEDVIS_DELAY = 500;
const int  HIGHVIS_DELAY = 500;



//MIXER CONSTANTS
const int SPIN_TIME = 2000;
const int FULL_SPEED = 0;
const int FULL_REVERSE = 180;
const int STOP_SPIN = 95;//to be experimentally determined.
const int MIXER_SERVO_PIN = 13;

//flush constants
const int FLUSH_PIN = 2;

//Master Delay
const int MASTER_VALVE_DELAY = 12000;

#endif
