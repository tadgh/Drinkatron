import drinks
import constants
import time
import serial

class Connection:

    def __init__(self):
        self.ser = serial.Serial('COM6',9600)#com6 is back most Keyboard USB port
        self.isDispensing = False


    def sendDrink(self,drink):
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


  

