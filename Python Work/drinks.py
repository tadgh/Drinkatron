import re
import logging
from tkinter import PhotoImage
import os

class drink:
    def __init__(self,drinkID, drinkName, ing1, ing2, ing3, ing4, ing5, ing6, ing7, ing8, ing9, ing10, ing11, ing12, garnish, description, positiveVoteCount, cost, dispenseCount, imagePath):
        logging.basicConfig(file="runLog.txt", level=logging.INFO)
        self.log = logging.getLogger("DRINKS")
        self.log.info("Entering -> drinks.py Consructor")

        if drinkID == None:
            self.ing1 = 0
            self.ing2 = 0
            self.ing3 = 0
            self.ing4 = 0
            self.ing5 = 0
            self.ing6 = 0
            self.ing7 = 0
            self.ing8 = 0
            self.ing9 = 0
            self.ing10 = 0
            self.ing11 = 0
            self.ing12 = 0

            self.hasGarnish = False
            self.dispenseCount = 0
            self.popularity = 0
            self.id = 0
            self.drinkName = ""
            self.cost = 0.00
            self.ingredientListCleaned = []
            self.ozSize = 0
            self.description = "Placeholder"
            self.image = None
        else:
            self.id = drinkID
            self.drinkName = drinkName
            self.ing1 = ing1
            self.ing2 = ing2
            self.ing3 = ing3
            self.ing4 = ing4
            self.ing5 = ing5
            self.ing6 = ing6
            self.ing7 = ing7
            self.ing8 = ing8
            self.ing9 = ing9
            self.ing10 = ing10
            self.ing11 = ing11
            self.ing12 = ing12
            self.garnish = garnish
            self.description = description
            self.positiveVoteCount = positiveVoteCount
            self.cost = cost
            self.dispenseCount = dispenseCount
            self.imagePath = imagePath
            self.image = PhotoImage(file = os.path.join(os.path.dirname(__file__),"..", "Resources", "Images", imagePath))


        self.hasBeenModded = False
        self.generateListForArduino()


    def hasGarnish(self):
        pass

    def dispenseIncrement(self):
        self.dispenseCount += 1
        self.hasBeenModded = False

    def popularityIncrement(self):
        self.popularity += 1
        self.hasBeenModded = False

    def getDispenseTime(self):
        return max(self.ingredientListCleaned)

    def generateListForArduino(self):
        self.ingredientListCleaned = [self.ing1, self.ing2, self.ing3, self.ing4, self.ing5, self.ing6, self.ing7, self.ing8, self.ing9, self.ing10, self.ing11, self.ing12]
        return self.ingredientListCleaned

    def printDrink(self):
        self.log.info("******\nName: %s\nIngList:%s\n******************" %(self.drinkName, self.ingredientListCleaned))

