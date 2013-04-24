import bottle
import dbinterface
import drinks
import logging
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
    log.info("Entering -> Dispense(name) for %s" % name)
    dirtyList = []
    for drink in drinkDictList:
        if drink['name'] == name:
            for ingredient in range(len(constants.INGREDIENTLIST)):
                dirtyList.append(drink[constants.INGREDIENTLIST[ingredient]])

    db.dispenseOccured(drink['drinkID'])
    arduino.sendDrink(dirtyList)
    log.info("Leaving -> Dispense(name) for %s. Found Drink." % name)
    return "Drink successfully passed off to arduino."
    log.error("Leaving -> Dispense(name) for %s. Drink could not be found" % name)
    return "Drink could not be found!"


@bottle.route('/dispense/custom/:adHocList')
def dispense_custom(adHocList):
    adHocList = adHocList.split('_')
    dirtyList = []
    for item in adHocList:
        dirtyList.append(int(item))
    arduino.sendDrink(dirtyList)


@bottle.route('/Analytics')
def Analytics():
    drinkData = []
    return bottle.template('Analytics', data=drinkData)

if __name__ == '__main__':
    log = logging.getLogger("WEB")
    log.setLevel(logging.ERROR)
    log.info("Entering -> WebClient")
    bottle.debug(True)
    db = dbinterface.DB()
    drinkList = db.listDrinksByName()

    drinkObjArray = []
    ingredientDict = {}
    for ingredient in constants.INGREDIENTLIST:
        ingredientDict[ingredient] = 0
    log.info(ingredientDict)
    drinkDictList = []
    for currentDrink in range(len(drinkList)):
        tempDrink = drinks.drink(*drinkList[currentDrink])
        drinkObjArray.append(tempDrink)
        drinkDictList.append(tempDrink.convertToDict())
        db.log.info(drinkObjArray[currentDrink].drinkName)

    bottle.run(host='192.168.0.10', port=8082)
