import bottle
import bottle_sqlite
import dbinterface
import drinks
import logging
import time
import json
import constants


log = logging.getLogger("WEB")
log.info("Entering -> WebClient")
bottle.debug(True)
db = dbinterface.DB()
drinkList = db.listDrinksByName()
drinkList = db.listDrinksByName()
########################################
#THIS IS CRUCIAL. this code initializes ALL drinks into an array, all at once. DO NOT FUCK WITH THIS CODE.
drinkObjArray = []
ingredientDict = {}
for ingredient in constants.INGREDIENTLIST:
    ingredientDict[ingredient] = 0

print(ingredientDict)

drinkDictList = []
for currentDrink in range(len(drinkList)):
    tempDrink = drinks.drink(*drinkList[currentDrink])
    drinkObjArray.append(tempDrink)
    drinkDictList.append(tempDrink.convertToDict())
    db.log.info(drinkObjArray[currentDrink].drinkName)
    #######################################



for item in drinkDictList:
    print(item)

@bottle.route('/')
def index():
    return bottle.template('index')

@bottle.route('/getDrinks')
def getDrinks():
    return bottle.template('getDrinks', drinkDictList = drinkDictList)

@bottle.route('/getDrink/:name')
def getDrink(name):
    print(name)
    for drink in drinkDictList:
        if drink['name'] == name:
            print(drink)
            return drink


#todo write code to do a lookup through getDrink/:name and then dispense based upon default ingredient proportions
@bottle.route('/dispense/:name')
def dispense(name):
    print(name)
    cleanList = []
    for drink in drinkDictList:
        if drink['name'] == name:
            cleanList.append(drink['ing1'])
            cleanList.append(drink['ing2'])
            cleanList.append(drink['ing3'])
            cleanList.append(drink['ing4'])
            cleanList.append(drink['ing5'])
            cleanList.append(drink['ing6'])
            cleanList.append(drink['ing7'])
            cleanList.append(drink['ing8'])
            cleanList.append(drink['ing9'])
            cleanList.append(drink['ing10'])
            cleanList.append(drink['ing11'])
            cleanList.append(drink['ing12'])
            print(cleanList)
            return cleanList



#todo Write code to split up the string into sections indicating proportions.
#@bottle.route('/dispense/custom/:proportions')
#def dispense_custom(proportions):
#    pass

bottle.run(host='localhost', port=8082)

