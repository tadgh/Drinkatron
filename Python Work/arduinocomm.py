import serial
import drinks
import drinkatron
import constants
import time

class Connection:

    def __init__(self):
        self.ser = serial.Serial('/dev/tty.usbserial',9600)#temp



    def sendDrink(self,drink):
        for ingredient in drink.ingredientListCleaned:
            self.ser.write(int(ingredient))
            #todo Look for proper timeouts.



    def readDrinkResponse(self):
        result = ser.read()
        pass


    def requestStatus(self):
        pass




