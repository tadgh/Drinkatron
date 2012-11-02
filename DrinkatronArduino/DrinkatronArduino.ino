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

byte ingredientList[12];
int index = 0;
Drink toBeDispensed; // STRANGELY, you do not need a new Drink() call to instantiate. Odd stuff. 
void loop() {
 
  
  if(Serial.available()){
    delay(1000);
    while(Serial.available() && index < 12){
      const char c = Serial.read();
      ingredientList[index] =  c - 48; //FUCKING ASCII CONVERSION SHIT NIGGER FUCKS.
     // Serial.print(ingredientList[index]);
     // Serial.print("   index: ");
     // Serial.println(index);
      index++;
      delay(3);
    }
  }
 
  if(index >= 12){
    int sum = 0;
    digitalWrite(13,HIGH);
    Serial.print("Values found: ");
    for(int i = 0; i < 12; i++){
      //sum += ingredientList[i];
      Serial.print(ingredientList[i]);
    }
    Serial.println(sum);
    index = 0;
   //**********************************************************
   //super ugly initialization code, but it
   //we dont do it this way, we end up blowing the stack space.
   //********************************************************** 
   toBeDispensed.setVodka(ingredientList[0]);
   toBeDispensed.setRum(ingredientList[1]);
   toBeDispensed.setOrangeJuice(ingredientList[2]);
   toBeDispensed.setCocaCola(ingredientList[3]);
   toBeDispensed.setSprite(ingredientList[4]);
   toBeDispensed.setLime(ingredientList[5]);
   toBeDispensed.setCranberry(ingredientList[6]);
   toBeDispensed.setWhiteRum(ingredientList[7]);
   toBeDispensed.setGrenadine(ingredientList[8]);
   toBeDispensed.setGin(ingredientList[9]);
   toBeDispensed.setBlueCuracao(ingredientList[10]);
   toBeDispensed.setWhiskey(ingredientList[11]);
   
   toBeDispensed.printDrink();
  }
    
}
  










