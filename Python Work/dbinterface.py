import sqlite3
import logging
import constants
import datetime
import time

logging.basicConfig(file="runLog.txt", level=logging.INFO)
log = logging.getLogger("Master")


class DB:

    def __init__(self):
        logging.basicConfig(file="runLog.txt", level=logging.INFO)
        self.log = logging.getLogger("DB")
        self.log.info("Initializing DB Connection...")
        try:
            self.conn = sqlite3.connect(constants.DBLOCATION)
        except:
            self.log.critical(
                "Could not open connection to DB at %s" % constants.DBLOCATION)
            return
        if self.conn:
            self.log.info("Connection to DB established.")
            # test

    #
    # LIST FUNCTIONS####
    #
    def listDrinksByName(self):
        self.log.info("Entering -> listDrinksByName()")
        sql = "SELECT * FROM drinks ORDER BY drink_name ASC"
        results = self.executeSql(sql, None)
        self.log.info("Leaving -> listDrinksByName()")
        # for item in results:
        #    print(item)
        # temp commented out for readability
        return results

    def listDrinksByIngredient(self, ingredient):
        self.log.info("Entering -> listDrinksByIngredient()")
        sql = "SELECT * FROM drinks WHERE ? <> 0 "
        results = self.executeSql(sql, ingredient)
        self.log.info("Leaving -> listDrinksByIngredient(%)" % ingredient)
        return results

    def listDrinksByPopularity(self, ingredient):
        self.log.info("Entering -> listDrinksByPopularity()")
        sql = "SELECT * FROM drinks ORDER BY popularity DESC"

        results = self.executeSql(sql)
        self.log.info("Leaving -> listDrinksByPopularity()")
        return results

    def listDrinksByDateCreated(self):
        self.log.info("Entering -> listDrinksByDateCreated()")
        sql = "SELECT * FROM drinks ORDER BY date_created DESC"
        results = self.executeSql(sql)
        self.log.info("Leaving -> listDrinksByDateCreated()")
        return results

    def getOverdueCustomers(self):
        self.log.info("Entering -> getOverdueCustomers")
        # TODO fix this for sqlite
        sql = '''SELECT *
                 FROM customers
                 WHERE current_balance > 0
                 AND last_paid_date > today() - 30'''
        results = self.executeSql(sql)
        return results

    def getOverallDrinkDataBetweenDates(self, startDate=None, endDate=None):
        # this checks the cases where the dates are not selected
        # properly by the user, and puts in assumed data
        # (i.e. today, a month ago, whateva whateva i do what i want)
        if startDate is not None and endDate is None:
            endDate = datetime.datetime.now()
        elif startDate is None and endDate is None:
            endDate = datetime.datetime.now()
            startDate = endDate - datetime.timedelta(days=30)
            print("Start date is: " + startDate)
            print("End date is: " + endDate)
        elif startDate is None and endDate is not None:
            startDate = endDate - datetime.timedelta(days=30)

        #if isinstance(endDate, time.struct_time):
        #    endDate = endDate.strftime('%Y-%m-%d')
        #    print("WOOP")
        #if isinstance(startDate, time.struct_time):
        #    startDate = startDate.strftime('%Y-%m-%d')
        #    print("WOOP")

        self.log.info("Start Date is: %s" % str(startDate))
        self.log.info("End Date is: %s" % str(endDate))
        args = (startDate, endDate)
        sql = '''
                SELECT drinks.drink_name , Count(*)
                FROM dispenses, drinks
                WHERE dispenses.drink_id = drinks.drink_id
                AND dispenses.dispense_timestamp > ?
                AND dispenses.dispense_timestamp < ?
                group by drinks.drink_name
              '''
        resultSet = self.executeSql(sql, args)
        return resultSet



        def getAllTimeDrinkData():
            sql = '''SELECT drink_name, dispense_count,
                            positive_votes, negative_votes
                     FROM drinks
                  '''
            results = self.executeSql(sql)



    def dispenseOccured(self, drink_id):
        self.log.info("Entering -> dispenseOccured")
        args = (drink_id,)
        sql = '''UPDATE drinks
                 SET dispense_count = dispense_count + 1
                 WHERE drink_id = ?'''
        result1 = self.executeSql(sql, args)
        sql = '''INSERT INTO dispenses (drink_id)
                 VALUES (?)
              '''
        result2 = self.executeSql(sql, args)
        return result1, result2
    #
    # MASTER LIST FUNCTIONMASTERLOL###

    def executeSql(self, sql, args=None):
        self.log.info("Entering-> executeSql()")
        cursor = self.grab_cursor()

        # Shooting off SQL to DB and pulling returned list as tuples.
        if args is None:
            cursor.execute(sql)
        elif args is not None:
            cursor.execute(sql, args)
        else:
            self.log.error("listDrinks -> Cannot resolve args parameter")
        self.conn.commit()
        resultSet = cursor.fetchall()

        # Checking integrity and returning
        if resultSet is None:
            self.log.error("No rows returned, empty DB? Wrong Table?")
        else:
            self.log.info("Grabbed resultSet list...")

        self.log.info("Leaving -> executeSql")

        return resultSet

    #
    # NON-LIST Functions#####
    #
    def grab_cursor(self):
        try:
            cursor = self.conn.cursor()
        except:
            self.log.error("Couldn't grab a cursor. Quitting listDrinksByname")
            return None
        self.log.info("Grabbed a cursor...")
        return cursor

    def createNewDrink(self, ingredient1, amount1, ingredient2, amount2,
                       ingredient3, amount3, ingredient4, amount4):
        pass

    def updateDrink(self, drink):
        self.log.info("Entering -> updateDrink()")
        sql = '''UPDATE drinks
                 SET popularity=%,
                 dispenseCount=%
                 WHERE drink_id=%''' % (drink.popularity,
                                        drink.dispenseCount,
                                        drink.id)

        cursor = self.grab_cursor()
        cursor.execute(sql)
        self.log.info("Leaving -> updateDrink()")

    def removeDrink(self, drink_id):
        self.log.info("Entering -> RemoveDrink()")
        cursor = self.grab_cursor()
        sql = "DELETE * FROM drinks WHERE drink_id = ?"
        cursor.execute(sql, drink_id)
        sql = "SELECT * FROM drinks WHERE drink_id = ?"
        cursor.execute(sql, drink_id)
        results = cursor.fetchall()
        if results is None or results == []:
            self.log.info("Leaving -> removeDrink")
            return True
        else:
            self.log.warning(
                "removeDrink -> unable to delete drinkID: %" % drink_id)
            self.log.info("Leaving -> removeDrink")
            return False
