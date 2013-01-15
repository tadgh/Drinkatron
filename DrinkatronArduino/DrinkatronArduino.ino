#include "Constants.h"
#include "drinks.h"
#include <string.h>
#include <Servo.h>
#include "Mixer.h"
#include <String.h>
#include <SD.h>
#include <SPI.h>

void setup(){
  Serial.begin(9600);


 for(int i = 31; i <= 43; i++){
    pinMode(i, OUTPUT);
  }
  
  digitalWrite(38, HIGH);
  digitalWrite(39, HIGH);
  digitalWrite(32, HIGH);
  digitalWrite(33, HIGH);
  digitalWrite(34, HIGH);
  digitalWrite(35, HIGH);
  digitalWrite(36, HIGH);
  digitalWrite(37, HIGH);
  digitalWrite(40, HIGH);
  digitalWrite(41, HIGH);
  digitalWrite(42, HIGH);
  digitalWrite(43, HIGH);
  digitalWrite(31, HIGH);
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
    digitalWrite(13,HIGH);
    if(drinkSize==100)
    {
      ;
    }
    else
    {
      for(int x = 0; x < 12; x++)
        ingredientList[x] = (float(ingredientList[x]) / float(drinkSize)) * 100;
    }


   //**********************************************************
   //super ugly initialization code, but it
   //we dont do it this way, we end up blowing the stack space.
   //********************************************************** 
   toBeDispensed.setCocaCola(ingredientList[0]);
   toBeDispensed.setSprite(ingredientList[1]);
   toBeDispensed.setCranberry(ingredientList[2]);
   toBeDispensed.setLime(ingredientList[3]);
   toBeDispensed.setOrangeJuice(ingredientList[4]);
   toBeDispensed.setGrenadine(ingredientList[5]);
   toBeDispensed.setBlueCuracao(ingredientList[6]);
   toBeDispensed.setGin(ingredientList[7]);
   toBeDispensed.setRum(ingredientList[8]);
   toBeDispensed.setTripleSec(ingredientList[9]);
   toBeDispensed.setVodka(ingredientList[10]);
   toBeDispensed.setWhiskey(ingredientList[11]);
   
   toBeDispensed.printDrink();
   Serial.println(drinkSize);
   drinkSize = 0;
   index=0;
  }
}

  










