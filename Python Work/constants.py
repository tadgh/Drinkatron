import os
import logging

LOGLEVEL = logging.ERROR
INGREDIENTLIST = [
    "Cola", "Sprite", "Cranberry Juice", "Lime Juice", " Orange Juice",
    "Grenadine", "Blue Curacao", "Gin", "Rum", "Triple Sec", "Vodka", "Whiskey"]
NUMBEROFINGREDIENTS = len(INGREDIENTLIST)
VERSION = 0.01
DBLOCATION = os.path.join(os.path.dirname(
    __file__), "..", "DB", "Drinkatron.s3db")
USERSETTINGS = {}
CUPINFO = {}
CUPINFO['Solo'] = 355
CUPINFO['Shot'] = 44
USERSETTINGS['cupType'] = "Solo"
USERSETTINGS['shotsEnabled'] = False
USERSETTINGS['customCupEnabled'] = False
USERSETTINGS['customCupSize'] = 0
USERSETTINGS['unitOfMeasurement'] = 'mL'

print(USERSETTINGS)
print(CUPINFO)
