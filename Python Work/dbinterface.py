import re
import sqlite3
import logging

logging.basicConfig(file="runLog.txt", level=logging.INFO)
log = logging.getLogger("DB")

class DB:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('D:\Drinkatron\DB\Drinkatron.s3db')
        except :
            log.critical("Could not open connection to DB!!")




            ####ADDING FATTY COMMENTS

    #####################
    ###LIST FUNCTIONS####
    #####################
    def listDrinksByName(self):
        sql = "SELECT * FROM drinks ORDER BY drink_name ASC"
        results = self.listDrinks(sql)
        log.info("Leaving -> listDrinksByName()")
        return results


    def listDrinksByIngredient(self, ingredient):
        sql = "SELECT * FROM drinks WHERE ? <> 0 "
        results = self.listDrinks(sql, ingredient)
        log.info("Leaving -> listDrinksByIngredient(%)"%ingredient)
        return results

    def listDrinksByPopularity(self,ingredient):

        sql = "SELECT * FROM drinks ORDER BY popularity DESC"

        results = self.listDrinks(sql)
        log.info("Leaving -> listDrinksByPopularity()")
        return results

    def listDrinksByDateCreated(self):
        sql = "SELECT * FROM drinks ORDER BY date_created DESC"
        results = self.listDrinks(sql)
        log.info("Leaving -> listDrinksByDateCreated()")
        return results





    ##########################
    ###MASTER LIST FUNCTIONMASTERLOL###
    ##########################
    def listDrinks(self, sql, values):
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
        return cursor

    def createNewDrink(self,ingredient1, amount1, ingredient2, amount2, ingredient3, amount3, ingredient4, amount4):
        pass

    def updateDrink(self, drink):
        pass

    def removeDrink(self, drink_id):


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



    

    

    
        
