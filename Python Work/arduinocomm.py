import drinks
import constants
import time
import serial
import logging
from threading import *
from time import sleep

class Connection:

    def __init__(self):
        logging.basicConfig(file="runLog.txt", level=logging.INFO)
        self.log = logging.getLogger("COMM")
        self.log.info("Entering -> arduinoComm Consructor")

        try:
            self.ser = serial.Serial('COM3',9600)#com6 is back most Keyboard USB port
        except:
            self.log.error("COULD NOT FIND ARDUINO. THINGS WILL FAIL.")
        finally:
            pass
        self.isDispensing = False
        self.log.info("Leaving -> arduinoComm Consructor")
        threadArduinoListener = Timer(3.0, self.readResponse)
        threadArduinoListener.start()
        self.log.info("Arduino Listener Started!!!!!")


    def sendDrink(self,drink):
        self.log.info("Entering -> sendDrink")
        self.isDispensing = True

        for ingredient in drink.ingredientListCleaned:
           self.log.info("Sending ingredient: %s" %ingredient)
           self.ser.write(str(ingredient).encode()) # ONLY COMMENTED OUT BECAUSE I LACK MY ARDUINO.        self.ser.write(bytes('*', encoding='ascii'))

            #sleep(0.1)
        self.log.info("Leaving -> sendDrink")

    def requestStatus(self):
        self.ser.write("#")
        time.sleep(5)
        ardResp = self.readDrinkResponse()
        return

        pass

    def readResponse(self):
        while True:
            print("waiting...")
            result = []


            try:
                while self.ser.inWaiting() > 0:
                    result.append(self.ser.readline())
                    print(result)
            except:
                self.log.warning("Something wrong with reading Arduino Serial!!!")

            if result == []:
                pass
            else:
                self.log.info("Arduino callback response: %s" %result)

            sleep(3)






  

