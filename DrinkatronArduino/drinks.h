#include "Constants.h"
#include "Arduino.h"
#ifndef __DRINKS_H__
#define __DRINKS_H__

class Drink{
 private:
  byte _Ing1;
  byte _Ing2;
  byte _Ing3;
  byte _Ing4;
  byte _Ing5;
  byte _Ing6;
  byte _Ing7;
  byte _Ing8;
  byte _Ing9;
  byte _Ing10;
  byte _Ing11;
  byte _Ing12;
  boolean _garnished;

 public:
   Drink();

   //Dispensers
   void parallelDispense();
   void finalDump();
   static void flushFunnel();

   //Value setters
   void setIng1(byte x);
   void setIng2(byte x);
   void setIng3(byte x);
   void setIng4(byte x);
   void setIng5(byte x);
   void setIng6(byte x);
   void setIng7(byte x);
   void setIng8(byte x);
   void setIng9(byte x);
   void setIng10(byte x);
   void setIng11(byte x);
   void setIng12(byte x);

   //drink stats
   byte getValvesInUse();
   void printDrink();
   byte componentCount();
   //Checks
   boolean isDispensable();
   byte longestCycle();

};

#endif
