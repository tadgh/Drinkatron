#include "Constants.h"
#include "drinks.h"
#include <string.h>
#include <Servo.h>
#include "Mixer.h"
#include <String.h>
#include <Adafruit_ST7735.h>
#include <SD.h>
#include <SPI.h>



Drink drinks[5];

char command;
char BMPNAME[13];
boolean dispense = true;
File bmpFile;
File myFile;
int bmpWidth, bmpHeight;
uint8_t bmpDepth, bmpImageoffset;


int prevVal = 1;
int currVal = 1;

Adafruit_ST7735 tft = Adafruit_ST7735(cs, dc, rst);

void setup(){
  Serial.begin(9600);
  pinMode(cs, OUTPUT);
  digitalWrite(cs, HIGH);
  tft.initR(INITR_GREENTAB);             
  tft.writecommand(ST7735_DISPON);
  tft.fillScreen(WHITE);
  tft.drawRect(10,60,50,15,BLUE);
  tft.drawString(20,70,"NIGGERS",BLACK);
  Serial.print("Initializing SD card...");

  if (!SD.begin(SD_CS)) {
    Serial.println("failed!");
    return;
  }
  Serial.println("SD OK!");


  myFile = SD.open("test1.txt");
  if (myFile) {
    Serial.println("test1.txt:");

    // read from the file until there's nothing else in it:
    while (myFile.available()) {
      Serial.write("-");
      Serial.write(myFile.read());
    }
    myFile.seek(0);

    for(int i = 0; i < 5; i++){
      //check if next byte is a newline or a carriage return, if so, jumps to next line.
      if(myFile.peek() == 13 || myFile.peek() == 10){
        myFile.seek(nextLine);
      }
      drinks[i].setVodka(myFile.read()- 48);
      drinks[i].setRum(myFile.read() - 48);    
      drinks[i].setOrangeJuice(myFile.read() - 48);
      drinks[i].setCocaCola(myFile.read() - 48);
      drinks[i].setSprite(myFile.read() - 48);
      drinks[i].setGin(myFile.read() - 48);
      drinks[i].setWhiteRum(myFile.read() - 48);
      drinks[i].setCranberry(myFile.read() - 48);
      drinks[i].setLime(myFile.read() - 48);
      drinks[i].setWhiskey(myFile.read() - 48);
      drinks[i].setGrenadine(myFile.read() - 48);
      drinks[i].setBlueCuracao(myFile.read() - 48);

      drinks[i].setOzSize(myFile.read() - 48);
      drinks[i].setCost(myFile.read() - 48);
    }
    myFile.close();


    myFile = SD.open("Names.txt");
    int j = 0;
    int k = 0;
    while(myFile.available()){
      if(myFile.peek() == 10 || myFile.peek() == 13 ||myFile.peek() == -1){
        myFile.seek(myFile.position() + 1);
        continue;
      }
      BMPNAME[k] = (char)myFile.read();
      k++;
      if(k == 12){
        BMPNAME[k] = '\0';
        k = 0;
        Serial.println(BMPNAME);
      drinks[j].setBmpName(BMPNAME);      
      j++;
      //myFile.seek(nextLine);     
      }

    }
    myFile.close();

  }

  Serial.println("Printing out drink list");
  for(int i = 0; i < 5; i++)
    drinks[i].printDrink();  


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

    char p[drinks[currVal].getBmpName().length() + 1];
    drinks[currVal].getBmpName().toCharArray(p, drinks[currVal].getBmpName().length() + 1);

    Serial.println(p);
    bmpFile = SD.open(p, FILE_READ);
    if (! bmpFile) {
      Serial.println("didnt find image");
      while (1);
    }

    if (! bmpReadHeader(bmpFile)) { 
      Serial.println("bad bmp");
      bmpFile.close();
      return;
    }

    Serial.print("image size "); 
    Serial.print(bmpWidth, DEC);
    Serial.print(", ");
    Serial.println(bmpHeight, DEC);


    bmpdraw(bmpFile, 0, 0);
    prevVal = currVal;
    bmpFile.close();
    command = 'z';
  }
}





void testfastlines(uint16_t color1, uint16_t color2) {
  tft.fillScreen(BLACK);
  for (uint16_t y=0; y < tft.height(); y+=5) {
    tft.drawHorizontalLine(0, y, tft.width(), color1);
  }
  for (uint16_t x=0; x < tft.width(); x+=5) {
    tft.drawVerticalLine(x, 0, tft.height(), color2);
  }
}

/*********************************************/
// This procedure reads a bitmap and draws it to the screen
// its sped up by reading many pixels worth of data at a time
// instead of just one pixel at a time. increading the buffer takes
// more RAM but makes the drawing a little faster. 20 pixels' worth
// is probably a good place

#define BUFFPIXEL 20

void bmpdraw(File f, int x, int y) {
  bmpFile.seek(bmpImageoffset);

  uint32_t time = millis();
  uint16_t p; 
  uint8_t g, b;
  int i, j;

  uint8_t sdbuffer[3 * BUFFPIXEL];  // 3 * pixels to buffer
  uint8_t buffidx = 3*BUFFPIXEL;

  //Serial.print("rotation = "); Serial.println(tft.getRotation(), DEC);

  //set up the 'display window'
  tft.setAddrWindow(x, y, x+bmpWidth-1, y+bmpHeight-1);

  uint8_t rotback = tft.getRotation();
  //tft.setRotation();

  for (i=0; i< bmpHeight; i++) {
    // bitmaps are stored with the BOTTOM line first so we have to move 'up'

    for (j=0; j<bmpWidth; j++) {
      // read more pixels
      if (buffidx >= 3*BUFFPIXEL) {
        bmpFile.read(sdbuffer, 3*BUFFPIXEL);
        buffidx = 0;
      }

      // convert pixel from 888 to 565
      b = sdbuffer[buffidx++];     // blue
      g = sdbuffer[buffidx++];     // green
      p = sdbuffer[buffidx++];     // red

      p >>= 3;
      p <<= 6;

      g >>= 2;
      p |= g;
      p <<= 5;

      b >>= 3;
      p |= b;
      //Serial.print(p, HEX);
      // write out the 16 bits of color
      //tft.drawPixel(i, j, p);
      tft.pushColor(p);
    }
  }
  Serial.print(millis() - time, DEC);
  Serial.println(" ms");
}

boolean bmpReadHeader(File f) {
  // read header
  uint32_t tmp;

  if (read16(f) != 0x4D42) {
    // magic bytes missing
    return false;
  }

  // read file size
  tmp = read32(f);  
  Serial.print("size 0x"); 
  Serial.println(tmp, HEX);

  // read and ignore creator bytes
  read32(f);

  bmpImageoffset = read32(f);  
  Serial.print("offset "); 
  Serial.println(bmpImageoffset, DEC);

  // read DIB header
  tmp = read32(f);
  Serial.print("header size "); 
  Serial.println(tmp, DEC);
  bmpWidth = read32(f);
  bmpHeight = read32(f);


  if (read16(f) != 1)
    return false;

  bmpDepth = read16(f);
  Serial.print("bitdepth "); 
  Serial.println(bmpDepth, DEC);

  if (read32(f) != 0) {
    // compression not supported!
    return false;
  }

  Serial.print("compression "); 
  Serial.println(tmp, DEC);

  return true;
}

/*********************************************/

// These read data from the SD card file and convert them to big endian 
// (the data is stored in little endian format!)

// LITTLE ENDIAN!
uint16_t read16(File f) {
  uint16_t d;
  uint8_t b;
  b = f.read();
  d = f.read();
  d <<= 8;
  d |= b;
  return d;
}


// LITTLE ENDIAN!
uint32_t read32(File f) {
  uint32_t d;
  uint16_t b;

  b = read16(f);
  d = read16(f);
  d <<= 16;
  d |= b;
  return d;
}








