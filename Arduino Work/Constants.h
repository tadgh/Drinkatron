//Serial Comms CONSTANTS
#ifndef __CONSTANTS_H__
#define __CONSTANTS_H__

#include "Arduino.h"
#define nextLine myFile.position()+2

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
const int  WHITERUM_RELAY_PIN = 38;
const int  BLUECURACAO_RELAY_PIN = 41;//should be 31, just testing the pin
const int  CRANBERRY_RELAY_PIN = 40;
const int  WHISKEY_RELAY_PIN = 44;//should be 41, just testing
const int  GRENADINE_RELAY_PIN = 42;
const int  LIME_RELAY_PIN = 43;

const int  MASTER_DISPENSE_PIN =  39;

const int  LOWVIS_DELAY = 500;
const int  MEDVIS_DELAY = 500;
const int  HIGHVIS_DELAY = 500;

//LCD Constants and SD constants
#define sclk 52
#define mosi 51
// You can also just connect the reset pin to +5V (we do a software reset)
#define rst 8
// these pins are required
#define cs 53
#define dc 9
#define SD_CS 4    // Set the chip select line to whatever you use (4 doesnt conflict with the library)


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

//COLOUR CONSTANTS
#define	BLACK           0x0000
#define	BLUE            0x001F
#define	RED             0xF800
#define	GREEN           0x07E0
#define CYAN            0x07FF
#define MAGENTA         0xF81F
#define YELLOW          0xFFE0  
#define WHITE           0xFFFF



#endif

