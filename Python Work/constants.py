import os
import logging
import configparser
import sqlite3


DBLOCATION = os.path.join(os.path.dirname(
    __file__), "..", "DB", "Drinkatron.s3db")
LOGLEVEL = logging.ERROR


db = sqlite3.connect(DBLOCATION)
cursor = db.cursor()
ingList = cursor.execute('''SELECT T_CANISTER.canister_id, T_INGREDIENT.ingredient_name
                FROM T_CANISTER LEFT JOIN T_INGREDIENT
                ON T_CANISTER.ingredient_id = T_INGREDIENT.ingredient_id
                ORDER BY T_CANISTER.canister_id
                ''').fetchall()
INGREDIENTLIST = []
for ingredient in ingList:
    INGREDIENTLIST.append(ingredient[1])
print(INGREDIENTLIST)
NUMBEROFINGREDIENTS = len(INGREDIENTLIST)
VERSION = 0.01



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
