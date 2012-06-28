import serial
import drinks
import constants
import time

class Connection:

    def __init__(self):
        self.ser = serial.Serial('/dev/tty.usbserial',9600)#temp
        self.isDispensing = False


    def sendDrink(self,drink):
        self.isDispensing = True
        for ingredient in drink.ingredientListCleaned:
            self.ser.write(int(ingredient))
            #todo Look for proper timeouts.


    def readDrinkResponse(self):
        result = ser.read()
        pass


    def requestStatus(self):
        pass




