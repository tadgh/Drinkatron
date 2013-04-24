import os
import logging

LOGLEVEL = logging.ERROR
NUMBEROFINGREDIENTS = 12
INGREDIENTLIST = [
    "Cola", "Sprite", "Cranberry Juice", "Lime Juice", " Orange Juice",
    "Grenadine", "Blue Curacao", "Gin", "Rum", "Triple Sec", "Vodka", "Whiskey"]
VERSION = 0.01
DBLOCATION = os.path.join(os.path.dirname(
    __file__), "..", "DB", "Drinkatron.s3db")
