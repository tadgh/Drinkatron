import re
import sqlite3


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('D:\Drinkatron\DB\Drinkatron.s3db')
        self.hook = self.conn.cursor()

    def listDrinksByName(self):
        drinks = self.hook.execute(''' select * FROM drinks
        ''')
        self.hook.commit()

        pass

    def updateDrinkScore(self, scoreModifier):
        pass

    def listDrinksByIngredient(self, ingredient):
        pass

    def listDrinksByPopularity(self):
        pass

    def listDrinksByDateCreated(self):
        pass

    def createNewDrink(self,ingredient1, amount1, ingredient2, amount2, ingredient3, amount3, ingredient4, amount4):
        pass

    def increaseDispensedCount(self):
        pass

    def increasePopularity(self):
        pass

    def removeDrink(self, drink_id):
        pass



    

    

    
        
