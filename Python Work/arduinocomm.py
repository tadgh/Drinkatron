import drinks
import constants
import time
import serial
import logging


class Connection:

    def __init__(self):
        logging.basicConfig(file="runLog.txt", level=logging.INFO)
        self.log = logging.getLogger("COMM")
        self.log.info("Entering -> arduinoComm Consructor")
        self.ser = serial.Serial('COM6',9600)#com6 is back most Keyboard USB port
        self.isDispensing = False
        self.log.info("Leaving -> arduinoComm Consructor")


    def sendDrink(self,drink):
        self.log.info("Entering -> sendDrink")
        self.isDispensing = True
        for ingredient in drink.ingredientListCleaned:
            self.ser.write(int(ingredient))
            #todo Look for proper timeouts.


    def readDrinkResponse(self):
        result = []
        while self.ser.inWaiting() != 0:
            result.append(self.ser.readline())
        if result == []: return None
        return result


    def requestStatus(self):
        self.ser.write("RQ###")
        time.sleep(5)
        ardResp = self.readDrinkResponse()
        return

        pass


  

