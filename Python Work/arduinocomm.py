import time
import serial
import logging
from threading import *
from time import sleep
import platform
import glob
import Canister
import settings


class Connection:

    def __init__(self):
        logging.basicConfig(file="runLog.txt", level=logging.INFO)
        self.log = logging.getLogger("COMM")
        self.log.info("Entering -> arduinoComm Consructor")
        self.listening = True
        if platform.system() is 'Windows':
            try:
                self.ser = serial.Serial(
                    'COM3', 9600)  # com6 is back most Keyboard USB port
            except:
                self.ser = None
            if self.ser:
                self.log.info("Arduino connected on : %s" 'COM15')
        else:
            #arduinoPort = glob.glob("/dev/ttyACM*")[0]
            try:
                self.ser = serial.Serial(arduinoPort, 9600)
            except:
                self.log.error("COULD NOT FIND ARDUINO. THINGS WILL FAIL.")
                self.ser = None
        self.log.info("Leaving -> arduinoComm Consructor")

        if self.ser:
            self.threadArduinoListener = Timer(3.0, self.readResponse)
            self.threadArduinoListener.start()
            self.log.info("Arduino Listener Started!!!!!")
        else:
            self.log.warning(
                '''Unable to start arduino, therefore not
                starting the listener thread!!''')

    def sendDrink(self, drinkArray):
        self.log.info("Entering -> sendDrink")
        if self.ser:
            for ingredient in drinkArray:
                self.log.info("Sending ingredient: %s" % ingredient)
                self.ser.write(str(ingredient).encode())
                self.ser.write("*".encode())
        else:
            self.log.error("Arduino not connected, cannot send drink.")
            return "Arduino not connected, cannot send drink."



        return "Drink dispensing!"
        self.log.info("Leaving -> sendDrink")

    def requestStatus(self):
        self.ser.write("#")
        time.sleep(5)
        ardResp = self.readDrinkResponse()
        if ardResp is None:
            pass
        return

    def disconnect(self):
        self.log.info("Disconnecting -> Arduino on " + self.ser.port)
        # This is a switch to dump out the reader Thread
        self.listening = False
        self.ser.close()

    def readResponse(self):
        while self.listening is True:
            result = []

            try:
                while self.ser.inWaiting() > 0:
                    result.append(self.ser.readline().decode())
            except:
                self.log.warning(
                    "Something wrong with reading Arduino Serial!!!")
            if result == []:
                pass
            else:
                for line in result:
                    self.log.info("Arduino callback response: %s" % line)

            sleep(3)
