import bottle
import bottle_sqlite
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

# todo write code to do a lookup through getDrink/:name and then dispense
# based upon default ingredient proportions
@bottle.route('/dispense/:name')
def dispense(name):
    print(name)
    cleanList = []
    for drink in drinkDictList:
        if drink['name'] == name:
            cleanList.append(drink[constants.INGREDIENTLIST[0]])
            cleanList.append(drink[constants.INGREDIENTLIST[1]])
            cleanList.append(drink[constants.INGREDIENTLIST[2]])
            cleanList.append(drink[constants.INGREDIENTLIST[3]])
            cleanList.append(drink[constants.INGREDIENTLIST[4]])
            cleanList.append(drink[constants.INGREDIENTLIST[5]])
            cleanList.append(drink[constants.INGREDIENTLIST[6]])
            cleanList.append(drink[constants.INGREDIENTLIST[7]])
            cleanList.append(drink[constants.INGREDIENTLIST[8]])
            cleanList.append(drink[constants.INGREDIENTLIST[9]])
            cleanList.append(drink[constants.INGREDIENTLIST[10]])
            cleanList.append(drink[constants.INGREDIENTLIST[11]])
            print(cleanList)
            db.dispenseOccured(drink['drinkID'])
            arduino.sendDrink(cleanList)
            return json.dumps(drink, indent=4)

    return "Drink Could not be found!"

@bottle.route('/Analytics')
def Analytics():
    return bottle.template('Analytics', data = drinkData)


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

