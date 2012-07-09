import re
class drink:

    def __init__(self):
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


    def hasGarnish(self):
        pass

    def dispenseIncrement(self):
        self.dispenseCount += 1

    def popularityIncrement(self):
        self.popularity += 1

    def getDispenseTime(self):
        ingredientList =  [ing1, ing2, ing3, ing4, ing5, ing6, ing7, ing8, ing9, ing10, ing11, ing12]
        return max(ingredientList)

    def generateListForArduino(self):
        self.ingredientListCleaned = [ing1, ing2, ing3, ing4, ing5, ing6, ing7, ing8, ing9, ing10, ing11, ing12]
        return self.ingredientListCleaned

