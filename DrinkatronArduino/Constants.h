//Serial Comms CONSTANTS
#ifndef __CONSTANTS_H__
#define __CONSTANTS_H__

#include "Arduino.h"

const int SERIAL_DELAY = 5;
const int BAUD_RATE = 9600;
const int NUM_DRINKS = 5;


//DRINK CONSTANTS
const int  VODKA_RELAY_PIN = 32;
const int  RUM_RELAY_PIN = 33;
const int  ORANGEJUICE_RELAY_PIN = 34;
const int  COCACOLA_RELAY_PIN = 35;
const int  SPRITE_RELAY_PIN = 36;
const int  GIN_RELAY_PIN = 37;
const int  TRIPLESEC_RELAY_PIN = 38;
const int  BLUECURACAO_RELAY_PIN = 41;//should be 31, just testing the pin
const int  CRANBERRY_RELAY_PIN = 40;
const int  WHISKEY_RELAY_PIN = 44;//should be 41, just testing
const int  GRENADINE_RELAY_PIN = 42;
const int  LIME_RELAY_PIN = 43;

const int  MASTER_DISPENSE_PIN =  39;

const int  LOWVIS_DELAY = 50; //THIS IS SOLELY EXPERIMENTAL AS WE ARE USING LARGER VALUES OF THING
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

