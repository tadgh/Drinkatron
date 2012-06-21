#include "Constants.h"
#include "Arduino.h"
#include <Servo.h>
#ifndef __DRINKS_H__
#define __DRINKS_H__

class Drink{
 private:

  byte _vodka;
  byte _rum;
  byte _gin;
  byte _whiteRum;
  byte _sprite;
  byte _cocaCola;  
  byte _orangeJuice;
  byte _blueCuracao;
  byte _cranberry;
  byte _grenadine;
  byte _lime;
  byte _whiskey;  

  byte _ozSize;
  byte _cost;
  byte _numberDispensed;
  
  String _bmpName;

  
 public:

   
   //constructor
   Drink();
   
   //Dispensers
   void parallelDispense();
   void finalDump();
   static void flushFunnel();
   
   //Value setters
   void setVodka(byte x);
   void setRum(byte x);
   void setOrangeJuice(byte x);
   void setCocaCola(byte x);
   void setSprite(byte x);
   void setLime(byte x);
   void setCranberry(byte x);
   void setWhiteRum(byte x);
   void setGrenadine(byte x);
   void setGin(byte x);
   void setBlueCuracao(byte x);
   void setWhiskey(byte x);
   
   void setOzSize(byte x);
   void setBmpName(char x[]);
   void setCost(byte x);
   String getBmpName();
   
   //drink stats
   void printDrink();
   byte componentCount();
   byte longestCycle();
   byte getNumberDispensed();
   byte getValvesInUse();
   
   //Checks
   boolean isDispensable();

     
};

#endif
