#include "Constants.h"
#include "drinks.h"
#include <string.h>
#include <Servo.h>
#include "Mixer.h"
#include <String.h>
#include <SD.h>
#include <SPI.h>



Drink drinks[5];

char command;
boolean dispense = true;



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
int incByte;
void loop() {
 
  while(Serial.available() && index < 12){
    incByte = Serial.read();
    ingredientList[index] =  incByte - 48; //FUCKING ASCII CONVERSION SHIT NIGGER FUCKS.
    Serial.println(ingredientList[index]);
    Serial.print("index: ");
    Serial.println(index);
    index++;
    delay(5);
    }
 
  if(index >= 12){
    for(int i = 0; i < 12; i++)
    Serial.print(ingredientList[i]);
    index = 0;
  }
    
}
  










