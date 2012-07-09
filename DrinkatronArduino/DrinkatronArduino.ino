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



int prevVal = 1;
int currVal = 1;


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




void loop() {


  
  while (true)
  {
    Serial.println("hello broheim");
    delay(2500);
  }  
  while (Serial.available()) {
    const char c = Serial.read();
    if (c != -1 && c != '\n')
      command = c;
    delay(5);
    Serial.println(command);


  }
  //Check for serial input
  if (command == '-'){
    if(currVal == 0){
      currVal = NUM_DRINKS - 1;
    }
    else{
      currVal--;
    }
  }
  else if(command == '+'){
    if(currVal == NUM_DRINKS -1)
      currVal = 0;
    else
      currVal++;
  }
  else if(command == '1'){
    drinks[currVal].parallelDispense();
    command = 'z';
  }
  else if(command == '2'){
    digitalWrite(MASTER_DISPENSE_PIN, LOW);
    delay(1000);
    digitalWrite(MASTER_DISPENSE_PIN, HIGH);
    command = 'z';
  }
    
  if(currVal != prevVal){
    Serial.println("entered changer");

  }
}








