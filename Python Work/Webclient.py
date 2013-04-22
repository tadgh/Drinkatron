import bottle
import dbinterface
import drinks
import logging
import json
import constants
import arduinocomm

arduino = arduinocomm.Connection()


@bottle.route('/')
def index():
    return bottle.template('index')


@bottle.route('/getDrinks')
def getDrinks():
    return bottle.template('getDrinks', drinkDictList=drinkDictList)


@bottle.route('/getDrink/:name')
def getDrink(name):
    print(name)
    for drink in drinkDictList:
        if drink['name'] == name:
            print(drink)
            return drink


@bottle.route('/dispense/known/:name')
def dispense(name):
    print(name)
    dirtyList = []
    for drink in drinkDictList:
        if drink['name'] == name:
            dirtyList.append(drink[constants.INGREDIENTLIST[0]])
            dirtyList.append(drink[constants.INGREDIENTLIST[1]])
            dirtyList.append(drink[constants.INGREDIENTLIST[2]])
            dirtyList.append(drink[constants.INGREDIENTLIST[3]])
            dirtyList.append(drink[constants.INGREDIENTLIST[4]])
            dirtyList.append(drink[constants.INGREDIENTLIST[5]])
            dirtyList.append(drink[constants.INGREDIENTLIST[6]])
            dirtyList.append(drink[constants.INGREDIENTLIST[7]])
            dirtyList.append(drink[constants.INGREDIENTLIST[8]])
            dirtyList.append(drink[constants.INGREDIENTLIST[9]])
            dirtyList.append(drink[constants.INGREDIENTLIST[10]])
            dirtyList.append(drink[constants.INGREDIENTLIST[11]])
            print(dirtyList)
            db.dispenseOccured(drink['drinkID'])
    return "Drink Could not be found!"


@bottle.route('/dispense/custom/:adhocList')
def dispense_custom(adhocList):
    adhocList = adhocList.split('_')
    dirtyList = []
    for item in adhocList:
        dirtyList.append(int(item))
    print(dirtyList)
    pourDrink(dirtyList)


def pourDrink(dirtyList):
    #making the drink proportional given a 100% is a full drink.
    drinkSize = 0
    cleanedList = []
    for item in dirtyList:
        drinkSize += item
    if drinkSize != 100:
        for i in range(len(dirtyList)):
            cleanedList.append(round(dirtyList[i] / float(drinkSize) * 100))

    print(cleanedList)
    arduino.sendDrink(cleanedList)

@bottle.route('/Analytics')
def Analytics():
    drinkData = []
    return bottle.template('Analytics', data=drinkData)


# todo Write code to split up the string into sections indicating proportions.
# @bottle.route('/dispense/custom/:proportions')
# def dispense_custom(proportions):
#    pass
if __name__ == '__main__':
    log = logging.getLogger("WEB")
    log.info("Entering -> WebClient")
    bottle.debug(True)
    db = dbinterface.DB()
    drinkList = db.listDrinksByName()

    # THIS IS CRUCIAL. this code initializes ALL drinks into an array,
    # all at once. DO NOT FUCK WITH THIS CODE.
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
        #

    for item in drinkDictList:
        print(item)
    bottle.run(host='localhost', port=8082)

