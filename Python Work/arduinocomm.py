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
            self.ser = serial.Serial('COM6',9600)#com6 is back most Keyboard USB port
        except:
            self.log.error("COULD NOT FIND ARDUINO. THINGS WILL FAIL.")
        finally:
            pass
        self.isDispensing = False
        self.log.info("Leaving -> arduinoComm Consructor")
        threadArduinoListener = Timer(3.0, self.readResponse)
        threadArduinoListener.start()


    def sendDrink(self,drink):
        self.log.info("Entering -> sendDrink")
        self.isDispensing = True
        for ingredient in drink.ingredientListCleaned:
            self.ser.write(int(ingredient))
            sleep(0.5)

    def requestStatus(self):
        self.ser.write("RQ###")
        time.sleep(5)
        ardResp = self.readDrinkResponse()
        return

        pass

    def readResponse(self):
        while True:
            result = []

            while self.ser.inWaiting() != 0:
                result.append(self.ser.readline())

            if result == []:
                pass
            else:
                self.log.info("Arduino Response: %s" %result)

            sleep(3)






  

