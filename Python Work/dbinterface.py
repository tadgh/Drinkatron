import re
import sqlite3
import logging
import drinks
import constants


logging.basicConfig(file="runLog.txt", level=logging.INFO)
log = logging.getLogger("Master")

class DB:
    def __init__(self):
        logging.basicConfig(file="runLog.txt", level=logging.INFO)
        self.log = logging.getLogger("DB")
        self.log.info("Initializing DB Connection...")
        try:
            self.conn = sqlite3.connect(constants.DBLOCATION)
        except :
            self.log.critical("Could not open connection to DB at %s"%constants.DBLOCATION)
            return
        if self.conn:
            self.log.info("Connection to DB established.")
            #test


    #####################
    ###LIST FUNCTIONS####
    #####################
    def listDrinksByName(self):
        self.log.info("Entering -> listDrinksByName()")
        sql = "SELECT * FROM drinks ORDER BY drink_name ASC"
        results = self.listDrinks(sql, None)
        self.log.info("Leaving -> listDrinksByName()")
        return results


    def listDrinksByIngredient(self, ingredient):
        self.log.info("Entering -> listDrinksByIngredient()")
        sql = "SELECT * FROM drinks WHERE ? <> 0 "
        results = self.listDrinks(sql, ingredient)
        self.log.info("Leaving -> listDrinksByIngredient(%)"%ingredient)
        return results

    def listDrinksByPopularity(self,ingredient):
        self.log.info("Entering -> listDrinksByPopularity()")
        sql = "SELECT * FROM drinks ORDER BY popularity DESC"

        results = self.listDrinks(sql)
        self.log.info("Leaving -> listDrinksByPopularity()")
        return results

    def listDrinksByDateCreated(self):
        self.log.info("Entering -> listDrinksByDateCreated()")
        sql = "SELECT * FROM drinks ORDER BY date_created DESC"
        results = self.listDrinks(sql)
        self.log.info("Leaving -> listDrinksByDateCreated()")
        return results



    ##########################
    ###MASTER LIST FUNCTIONMASTERLOL###
    ##########################
    def listDrinks(self, sql, values):
        self.log.info("Entering-> listDrinks()")
        cursor = self.grab_cursor()

        #Shooting off SQL to DB and pulling returned list as tuples.
        if values is None:
            cursor.execute(sql)
        elif values is not None:
            cursor.execute(sql, values)
        else:
            self.log.error("listDrinks -> Cannot resolve Values parameter")

        drinkList = cursor.fetchall()
        #cursor.commit()

        #Checking integrity and returning to Drinkatron.py
        if drinkList == None:
            self.log.error("No rows returned, empty DB? Wrong Table?")
        else:
            self.log.info("Grabbed Drink list...")

        self.log.info("Leaving -> listDrinks")

        return drinkList



    ########################
    #NON-LIST Functions#####
    ########################

    def grab_cursor(self):
        try:
            cursor = self.conn.cursor()
        except:
            self.log.error("Couldn't grab a cursor. Quitting listDrinksByname")
            return None
        self.log.info("Grabbed a cursor...")
        return cursor

    def createNewDrink(self,ingredient1, amount1, ingredient2, amount2, ingredient3, amount3, ingredient4, amount4):
        pass

    def updateDrink(self, drink):
        self.log.info("Entering -> updateDrink()")
        sql = "UPDATE drinks SET popularity=%, dispenseCount=% WHERE drink_id=%" %(drink.popularity, drink.dispenseCount,drink.id)
        cursor = self.grab_cursor()
        cursor.execute(sql)
        cursor.commit()
        self.log.info("Leaving -> updateDrink()")

    def removeDrink(self, drink_id):
        self.log.info("Entering -> RemoveDrink()")
        cursor = self.grab_cursor()
        sql = "DELETE * FROM drinks WHERE drink_id = ?"
        cursor.execute(sql,drink_id)
        cursor.commit()

        sql = "SELECT * FROM drinks WHERE drink_id = ?"
        cursor.execute(sql,drink_id)
        results = cursor.fetchall()
        cursor.commit()
        if results == None or results == []:
            self.log.info("Leaving -> removeDrink")
            return True
        else:
            self.log.warning("removeDrink -> unable to delete drinkID: %"%drink_id)
            self.log.info("Leaving -> removeDrink")
            return False







    
        
