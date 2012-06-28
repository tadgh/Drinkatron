import re
import sqlite3
import logging
import drinks

logging.basicConfig(file="runLog.txt", level=logging.INFO)
log = logging.getLogger("Master")

class DB:
    def __init__(self):
        log.info("Initializing DB Connection...")
        try:
            self.conn = sqlite3.connect('D:\Drinkatron\DB\Drinkatron.s3db')
        except :
            log.critical("Could not open connection to DB!!")
            return
        if self.conn:
            log.info("Connection to DB established.")


    #####################
    ###LIST FUNCTIONS####
    #####################
    def listDrinksByName(self):
        log.info("Entering -> listDrinksByName()")
        sql = "SELECT * FROM drinks ORDER BY drink_name ASC"
        results = self.listDrinks(sql)
        log.info("Leaving -> listDrinksByName()")
        return results


    def listDrinksByIngredient(self, ingredient):
        log.info("Entering -> listDrinksByIngredient()")
        sql = "SELECT * FROM drinks WHERE ? <> 0 "
        results = self.listDrinks(sql, ingredient)
        log.info("Leaving -> listDrinksByIngredient(%)"%ingredient)
        return results

    def listDrinksByPopularity(self,ingredient):
        log.info("Entering -> listDrinksByPopularity()")
        sql = "SELECT * FROM drinks ORDER BY popularity DESC"

        results = self.listDrinks(sql)
        log.info("Leaving -> listDrinksByPopularity()")
        return results

    def listDrinksByDateCreated(self):
        log.info("Entering -> listDrinksByDateCreated()")
        sql = "SELECT * FROM drinks ORDER BY date_created DESC"
        results = self.listDrinks(sql)
        log.info("Leaving -> listDrinksByDateCreated()")
        return results





    ##########################
    ###MASTER LIST FUNCTIONMASTERLOL###
    ##########################
    def listDrinks(self, sql, values):
        log.info("Entering-> listDrinks()")
        cursor = self.grab_cursor()

        #Shooting off SQL to DB and pulling returned list as tuples.
        if values is None:
            cursor.execute(sql)
        elif values is not None:
            cursor.execute(sql, values)
        else:
            log.error("listDrinks -> Cannot resolve Values parameter")

        drinkList = cursor.fetchall()
        self.cursor.commit()

        #Checking integrity and returning to Drinkatron.py
        if drinkList == None:
            log.error("No rows returned, empty DB? Wrong Table?")
        else:
            log.info("Grabbed Drink list: %" %drinkList)

        log.info("Leaving -> listDrinks")
        return drinkList



    ########################
    #NON-LIST Functions#####
    ########################

    def grab_cursor(self):
        try:
            cursor = self.conn.cursor()
        except:
            log.error("Couldn't grab a cursor. Quitting listDrinksByname")
            return None
        log.info("Grabbed a cursor...")
        return cursor

    def createNewDrink(self,ingredient1, amount1, ingredient2, amount2, ingredient3, amount3, ingredient4, amount4):
        pass

    def updateDrink(self, drink):
        log.info("Entering -> updateDrink()")
        sql = "UPDATE drinks SET popularity=%, dispenseCount=% WHERE drink_id=%" %(drink.popularity, drink.dispenseCount,drink.id)
        cursor = self.grab_cursor()
        cursor.execute(sql)
        cursor.commit()
        log.info("Leaving -> updateDrink()")

    def removeDrink(self, drink_id):
        log.info("Entering -> RemoveDrink()")
        cursor = self.grab_cursor()
        sql = "DELETE * FROM drinks WHERE drink_id = ?"
        cursor.execute(sql,drink_id)
        cursor.commit()

        sql = "SELECT * FROM drinks WHERE drink_id = ?"
        cursor.execute(sql,drink_id)
        results = cursor.fetchall()
        cursor.commit()
        if results == None or results == []:
            log.info("Leaving -> removeDrink")
            return True
        else:
            log.warning("removeDrink -> unable to delete drinkID: %"%drink_id)
            log.info("Leaving -> removeDrink")
            return False



    

    

    
        
