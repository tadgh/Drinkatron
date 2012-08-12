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


  

  while (Serial.available()) {
    const char c = Serial.read();
    if (c != -1 && c != '\n')
      command = c;
    delay(5);
    Serial.println(command);


  }
 
}








