import os
import logging
import configparser

INGREDIENTLIST = [
    "Cola", "Sprite", "Cranberry Juice", "Lime Juice", " Orange Juice",
    "Grenadine", "Blue Curacao", "Gin", "Rum", "Triple Sec", "Vodka", "Whiskey"]
NUMBEROFINGREDIENTS = len(INGREDIENTLIST)
VERSION = 0.01
DBLOCATION = os.path.join(os.path.dirname(
    __file__), "..", "DB", "Drinkatron.s3db")
LOGLEVEL = logging.ERROR


Config = configparser.ConfigParser()
Config.read("Startup.ini")


USERSETTINGS = {}
CUPINFO = {}


#initializing cup info
cupOptions = Config.options('CUPINFO')
for option in cupOptions:
    try:
        CUPINFO[option] = Config.getint('CUPINFO', option)
    except:
        print("SHI")

#initializing user settings
userOptions = Config.options('USERSETTINGS')
for option in userOptions:
    try:
        USERSETTINGS[option] = Config.get('USERSETTINGS', option)
    except:
        print("shi")


print(USERSETTINGS)
print(CUPINFO)
