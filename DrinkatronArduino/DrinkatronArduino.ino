#include "Constants.h"
#include "drinks.h"
//#include "spinningplate.h"
#include <string.h>
#include <String.h>


void setup(){
  Serial.begin(9600);


 for(int i = 37; i <= 51; i++){
    pinMode(i, OUTPUT);
    digitalWrite(i, LOW)
  }

}

int ingredientList[12];

Drink toBeDispensed; // STRANGELY, you do not need a new Drink() call to instantiate. Odd stuff.
char incomingByte;
int index = 0;
int integerValue=0;
int drinkSize = 0;

void loop() {
    while (Serial.available()) {   // something came across serial
      integerValue = 0;         // throw away previous integerValue
      while(1)
      {
        incomingByte = Serial.read();
        if (incomingByte == '*')
        {
          break;
        }   // exit the while(1)
        if (incomingByte == -1) continue;  // if no characters are in the buffer read() returns -1

        integerValue *= 10;  // shift left 1 decimal place
        integerValue = ((incomingByte - 48) + integerValue);// convert ASCII to integer, add, and shift left 1 decimal place
      }
    ingredientList[index] = integerValue;
    drinkSize += integerValue;
    index++;
  }

  if(index==12){
   //**********************************************************
   //super ugly initialization code, but it
   //we dont do it this way, we end up blowing the stack space.
   //**********************************************************
   toBeDispensed.setIng1(ingredientList[0]);
   toBeDispensed.setIng2(ingredientList[1]);
   toBeDispensed.setIng3(ingredientList[2]);
   toBeDispensed.setIng4(ingredientList[3]);
   toBeDispensed.setIng5(ingredientList[4]);
   toBeDispensed.setIng6(ingredientList[5]);
   toBeDispensed.setIng7(ingredientList[6]);
   toBeDispensed.setIng8(ingredientList[7]);
   toBeDispensed.setIng9(ingredientList[8]);
   toBeDispensed.setIng10(ingredientList[9]);
   toBeDispensed.setIng11(ingredientList[10]);
   toBeDispensed.setIng12(ingredientList[11]);
   toBeDispensed.printDrink();
   Serial.println(drinkSize);
   toBeDispensed.parallelDispense();
   drinkSize = 0;
   index=0;
  }
}












