#include "drinks.h"
#include "Arduino.h"
#include "Constants.h"

   Drink::Drink(){
   }


   void Drink::flushFunnel(){
     digitalWrite(FLUSH_PIN, HIGH);
     delay(5000);
     digitalWrite(FLUSH_PIN, HIGH);
  }

   void Drink::parallelDispense(){

     this->setDelay();


     for(byte i = 0; i < this->longestCycle() + 1; i++){

       if(_Ing1 > i){
         digitalWrite(ING1_RELAY_PIN, LOW);Serial.println("Dispensing Ing1");
       }else
         digitalWrite(ING1_RELAY_PIN, HIGH);

       if(_Ing2 > i){
         digitalWrite(ING2_RELAY_PIN, LOW);Serial.println("Dispensing Ing2.");
       }else
         digitalWrite(ING2_RELAY_PIN,HIGH);

       if(_Ing3 > i){
         digitalWrite(ING3_RELAY_PIN, LOW);Serial.println("Dispensing Ing3.");
       }else
         digitalWrite(ING3_RELAY_PIN, HIGH);

       if(_Ing4 > i){
         digitalWrite(ING4_RELAY_PIN, LOW);Serial.println("Dispensing Ing4.");
       }else
         digitalWrite(ING4_RELAY_PIN, HIGH);

       if(_Ing5 > i){
         digitalWrite(ING5_RELAY_PIN, LOW);Serial.println("Dispensing Ing5.");
       }else
         digitalWrite(ING5_RELAY_PIN, HIGH);

       if(_Ing6 > i){
         digitalWrite(ING6_RELAY_PIN, LOW);Serial.println("Dispensing Ing6.");
       }else
         digitalWrite(ING6_RELAY_PIN, HIGH);

       if(_Ing7 > i){
         digitalWrite(ING7_RELAY_PIN, LOW);Serial.println("Dispensing Ing7.");
       }else
         digitalWrite(ING7_RELAY_PIN, HIGH);

       if(_Ing8 > i){
         digitalWrite(ING8_RELAY_PIN, LOW);Serial.println("Dispensing Ing8");
       }else
         digitalWrite(ING8_RELAY_PIN, HIGH);

       if(_Ing9 > i){
         digitalWrite(ING9_RELAY_PIN, LOW);Serial.println("Dispensing Ing9.");
       }else
         digitalWrite(ING9_RELAY_PIN, HIGH);

       if(_Ing10 > i){
         digitalWrite(ING10_RELAY_PIN, LOW);Serial.println("Dispensing Ing10.");
       }else
         digitalWrite(ING10_RELAY_PIN, HIGH);

       if(_Ing11 > i){
         digitalWrite(ING11_RELAY_PIN, LOW);Serial.println("Dispensing Ing11.");
       }else
         digitalWrite(ING11_RELAY_PIN, HIGH);

       if(_Ing12 > i){
         digitalWrite(ING12_RELAY_PIN, LOW);Serial.println("Dispensing Ing12.");
       }else
         digitalWrite(ING12_RELAY_PIN, HIGH);



      delay(_delay);
      Serial.print("*****Cycle ");
      Serial.print(i);
      Serial.println(" Complete*****");
     }
   }

   byte getNumberOfIngredients()
   {
     byte numIng = 0;
     if(_Ing11 > 0)
       numIng ++
       if(_Ing9 > 0)
         numIng++
       if(_Ing5 > 0)
         numIng++
       if(_Ing1 > 0)
         numIng++;
       if(_Ing2 > 0)
         numIng++;
       if(_Ing8 > 0)
         numIng++;
       if(_Ing7 > 0)
         numIng++;
       if(_Ing3 > 0)
         numIng++;
       if(_Ing6 > 0)
         numIng++;
       if(_Ing4 > 0)
         numIng++;
       if(_Ing12 > 0)
         numIng++;
       if(_Ing10 > 0)
         numIng++;

       return numIng;
   }

 //boolean isAvailable(){}

 byte Drink::longestCycle(){
     byte maxCycle = 0;
     if(_Ing11 > maxCycle)
       maxCycle = _Ing11;
       if(_Ing9 > maxCycle)
         maxCycle = _Ing9;
       if(_Ing5 > maxCycle)
         maxCycle = _Ing5;
       if(_Ing1 > maxCycle)
         maxCycle = _Ing1;
       if(_Ing2 > maxCycle)
         maxCycle = _Ing2;
       if(_Ing8 > maxCycle)
         maxCycle = _Ing8;
       if(_Ing7 > maxCycle)
         maxCycle = _Ing7;
       if(_Ing3 > maxCycle)
         maxCycle = _Ing3;
       if(_Ing6 > maxCycle)
         maxCycle = _Ing6;
       if(_Ing4 > maxCycle)
         maxCycle = _Ing4;
       if(_Ing12 > maxCycle)
         maxCycle = _Ing12;
       if(_Ing10 > maxCycle)
         maxCycle = _Ing10;

       return maxCycle;
   }




   void Drink::setDelay()
   {
    int ingCount = this->getValvesInUse();
    _delay = VALVE_DELAYS[ingCount];
   }

   //prints out various drink stats
   void Drink::printDrink(){
     Serial.println("******INGREDIENTS*******");
     Serial.print(_Ing1);
     Serial.print(_Ing2);
     Serial.print(_Ing3);
     Serial.print(_Ing4);
     Serial.print(_Ing5);
     Serial.print(_Ing6);
     Serial.print(_Ing7);
     Serial.print(_Ing8);
     Serial.print(_Ing9);
     Serial.print(_Ing10);
     Serial.print(_Ing11);
     Serial.print(_Ing12);
   }


   byte Drink::getValvesInUse(){
     byte valvesInUse = 0;
       if(_Ing11 > 0)
       valvesInUse++;
       if(_Ing9 > 0)
         valvesInUse++;
       if(_Ing5 > 0)
         valvesInUse++;
       if(_Ing1 > 0)
         valvesInUse++;
       if(_Ing2 > 0)
         valvesInUse++;
       if(_Ing8 > 0)
         valvesInUse++;
       if(_Ing7 > 0)
         valvesInUse++;
       if(_Ing3 > 0)
         valvesInUse++;
       if(_Ing6 > 0)
         valvesInUse++;
       if(_Ing4 > 0)
        valvesInUse++;
       if(_Ing12 > 0)
         valvesInUse++;
       if(_Ing10 > 0)
         valvesInUse++;

       return valvesInUse;
   }

   //returns the total number of components * their given portions.
   byte Drink::componentCount(){
     return(_Ing1 + _Ing2 + _Ing3 + _Ing4 + _Ing5 + _Ing6 + _Ing7 + _Ing8 + _Ing9 + _Ing10 + _Ing11 + _Ing12);
   }



   //All the setters
   void Drink::setIng1(byte x){
   _Ing1 = x;
   }
   void Drink::setIng2(byte x){
   _Ing2 = x;
   }
   void Drink::setIng3(byte x){
   _Ing3 = x;
   }
   void Drink::setIng4(byte x){
   _Ing4 = x;
   }
   void Drink::setIng5(byte x){
   _Ing5 = x;
   }
   void Drink::setIng6(byte x){
   _Ing6 = x;
   }
   void Drink::setIng7(byte x){
   _Ing7 = x;
   }
   void Drink::setIng8(byte x){
   _Ing8 = x;
   }
   void Drink::setIng9(byte x){
   _Ing9 = x;
   }
   void Drink::setIng10(byte x){
   _Ing10 = x;
   }
   void Drink::setIng11(byte x){
   _Ing11 = x;
   }
   void Drink::setIng12(byte x){
   _Ing12 = x;
   }
