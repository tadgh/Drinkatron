#include "drinks.h"
#include "Arduino.h"
#include "Constants.h"
#include <Servo.h>

   Drink::Drink(){
   }
   
   
   void Drink::flushFunnel(){
     digitalWrite(FLUSH_PIN, HIGH);
     delay(5000);
     digitalWrite(FLUSH_PIN, LOW);
  }

   void Drink::parallelDispense(){
     
     if(this->getValvesInUse() > 3){
       digitalWrite(MASTER_DISPENSE_PIN, LOW);
     }

     
     for(byte i = 0; i < this->longestCycle() + 1; i++){
       
       if(_blueCuracao > i){
         digitalWrite(BLUECURACAO_RELAY_PIN, LOW);Serial.println("Dispensing blue curacao.");
       }else
         digitalWrite(BLUECURACAO_RELAY_PIN, HIGH);Serial.println("SHUTTING OFF BLUE CURACAO");
       
       
       if(_vodka > i){
         digitalWrite(VODKA_RELAY_PIN, LOW);Serial.println("Dispensing vodka.");
       }else
         digitalWrite(VODKA_RELAY_PIN, HIGH);
       
       if(_rum > i){
         digitalWrite(RUM_RELAY_PIN, LOW);Serial.println("Dispensing rum.");
     }else
         digitalWrite(RUM_RELAY_PIN, HIGH);
       
       if(_orangeJuice > i){
         digitalWrite(ORANGEJUICE_RELAY_PIN, LOW);Serial.println("Dispensing OJ.");
   }else
         digitalWrite(ORANGEJUICE_RELAY_PIN, HIGH);
       
       if(_cocaCola > i){
         digitalWrite(COCACOLA_RELAY_PIN, LOW);Serial.println("Dispensing coca-cola.");
       }else
         digitalWrite(COCACOLA_RELAY_PIN, HIGH);

       if(_sprite > i){
         digitalWrite(SPRITE_RELAY_PIN, LOW);Serial.println("Dispensing sprite.");
       }else
         digitalWrite(SPRITE_RELAY_PIN, HIGH);

       if(_gin > i){
         digitalWrite(GIN_RELAY_PIN, LOW);Serial.println("Dispensing gin");
       }else
         digitalWrite(GIN_RELAY_PIN, HIGH);       

       if(_tripleSec > i){
         digitalWrite(TRIPLESEC_RELAY_PIN, LOW);Serial.println("Dispensing white rum.");
       }else
         digitalWrite(TRIPLESEC_RELAY_PIN, HIGH);   

       if(_lime > i){
         digitalWrite(LIME_RELAY_PIN, LOW);Serial.println("Dispensing lime.");
       }else
         digitalWrite(LIME_RELAY_PIN, HIGH);   
         
       if(_grenadine > i){
         digitalWrite(GRENADINE_RELAY_PIN, LOW);Serial.println("Dispensing grenadine.");
       }else
         digitalWrite(GRENADINE_RELAY_PIN, HIGH);      
   
       if(_whiskey > i){
         digitalWrite(WHISKEY_RELAY_PIN, LOW);Serial.println("Dispensing whiskey.");
       }else
         digitalWrite(WHISKEY_RELAY_PIN, HIGH);   
        
       if(_cranberry > i){
         digitalWrite(CRANBERRY_RELAY_PIN, LOW);Serial.println("Dispensing white rum.");
       }else
         digitalWrite(CRANBERRY_RELAY_PIN, HIGH);         
         
      delay(LOWVIS_DELAY);
      Serial.println("*****Cycle Complete*****");
      if(i == longestCycle() / 2)
        digitalWrite(MASTER_DISPENSE_PIN, LOW);
     }
     this->finalDump();

     
   }
   
   
   void Drink::finalDump(){    
     digitalWrite(MASTER_DISPENSE_PIN, LOW);
     Serial.println("Opened master dispense valve");
     delay(15000);
     Serial.print("componentCount = ");
   digitalWrite(MASTER_DISPENSE_PIN, HIGH);
   Serial.println("Closed master dispense valve");
 }
 

 //boolean isAvailable(){}  
  
 byte Drink::longestCycle(){
     byte maxCycle = 0;
     if(_vodka > maxCycle)
       maxCycle = _vodka;
       if(_rum > maxCycle)
         maxCycle = _rum;
       if(_orangeJuice > maxCycle)
         maxCycle = _orangeJuice;
       if(_cocaCola > maxCycle)
         maxCycle = _cocaCola;
       if(_sprite > maxCycle)
         maxCycle = _sprite;
       if(_gin > maxCycle)
         maxCycle = _gin;
       if(_blueCuracao > maxCycle)
         maxCycle = _blueCuracao;
       if(_cranberry > maxCycle)
         maxCycle = _cranberry;
       if(_grenadine > maxCycle)
         maxCycle = _grenadine;
       if(_lime > maxCycle)
         maxCycle = _lime;
       if(_whiskey > maxCycle)
         maxCycle = _whiskey;
       if(_tripleSec > maxCycle)
         maxCycle = _tripleSec;  
    
       return maxCycle;     
   }
   

   
   
   //prints out various drink stats
   void Drink::printDrink(){
     Serial.println("******INGREDIENTS*******");
     Serial.print("Vodka: ");
     Serial.println(_vodka);
     Serial.print("Rum: ");
     Serial.println(_rum);
     Serial.print("Orange Juice:  ");
     Serial.println(_orangeJuice);
     Serial.print("Coca Cola: ");
     Serial.println(_cocaCola);
     Serial.print("Sprite: ");
     Serial.println(_sprite);
     Serial.print("gin: ");
     Serial.println(_gin);
     Serial.print("white rum: ");
     Serial.println(_tripleSec); 
     Serial.print("grenadine: ");
     Serial.println(_grenadine);
     Serial.print("lime: ");
     Serial.println(_lime);
     Serial.print("whiskey: ");
     Serial.println(_whiskey);
     Serial.print("cranberry: ");
     Serial.println(_cranberry);
     Serial.print("blue curacao: ");
     Serial.println(_blueCuracao);
     
   }
   
   
   byte Drink::getValvesInUse(){
     byte valvesInUse = 0;
       if(_vodka > 0)
       valvesInUse++;
       if(_rum > 0)
         valvesInUse++;
       if(_orangeJuice > 0)
         valvesInUse++;
       if(_cocaCola > 0)
         valvesInUse++;
       if(_sprite > 0)
         valvesInUse++;
       if(_gin > 0)
         valvesInUse++;
       if(_blueCuracao > 0)
         valvesInUse++;
       if(_cranberry > 0)
         valvesInUse++;
       if(_grenadine > 0)
         valvesInUse++;
       if(_lime > 0)
        valvesInUse++;
       if(_whiskey > 0)
         valvesInUse++;
       if(_tripleSec > 0)
         valvesInUse++;  
    
       return valvesInUse;     
   }
   
   //returns the total number of components * their given portions.
   byte Drink::componentCount(){
     return(_vodka + _rum + _orangeJuice + _cocaCola + _sprite + _gin + _rum + _tripleSec + _lime + _grenadine + _whiskey + _blueCuracao); 
   }

   
   
   //All the setters
   void Drink::setVodka(byte x){
   _vodka = x;
   }

   void Drink::setRum(byte x){
   _rum = x;
   }
   void Drink::setOrangeJuice(byte x){
   _orangeJuice = x;
   }
   void Drink::setCocaCola(byte x){
   _cocaCola = x;
   }
   void Drink::setSprite(byte x){
   _sprite = x;
   }

   void Drink::setGin(byte x){
   _gin = x;
   }
   void Drink::setTripleSec(byte x){
   _tripleSec = x;
   }
   void Drink::setGrenadine(byte x){
   _grenadine = x;
   }
   void Drink::setLime(byte x){
   _lime = x;
   }
   void Drink::setWhiskey(byte x){
   _whiskey = x;
   }
   void Drink::setCranberry(byte x){
   _cranberry = x;
   }
   void Drink::setBlueCuracao(byte x){
   _blueCuracao = x;
   }
