import drinks
import logging
import constants
import arduinocomm
import bottle
import bottle_sqlite
import sqlite3
import socket

arduino = arduinocomm.Connection()
app = bottle.Bottle()
plugin = bottle_sqlite.Plugin(dbfile=constants.DBLOCATION, autocommit=True)
app.install(plugin)

log = logging.getLogger("WEB")
log.setLevel(logging.INFO)
log.info("Entering -> WebClient")
bottle.debug(True)
drinkDictList = []


@app.route('/')
def index():
    drinkList = []
    del drinkDictList[:]
    conn = sqlite3.connect(constants.DBLOCATION)
    cursor = conn.cursor()
    drinkList = cursor.execute("SELECT * FROM drinks ORDER BY drink_name ASC").fetchall()
    for currentDrink in range(len(drinkList)):
        print('found drink')
        tempDrink = drinks.drink(*drinkList[currentDrink])
        drinkDictList.append(tempDrink.convertToDict())
    conn.close()
    return bottle.template('index', drinkList=drinkDictList)


@app.route('/static/:path#.+#', name='static')
def static(path):
    return bottle.static_file(path, root='./static/')


@app.route('/getDrinks')
def getDrinks():
    return bottle.template('getDrinks', drinkDictList=drinkDictList)


@app.route('/getDrink/:name')
def getDrink(name):
    print(name)
    for drink in drinkDictList:
        if drink['name'] == name:
            print(drink)
            # return bottle.template('getDrink', selectedDrink=drink)
            return bottle.template('getDrinkProto', selectedDrink=drink)


@app.route('/dispense/known/:name')
def dispense(name, db):
    log.info("Entering -> Dispense(name) for %s" % name)
    dirtyList = []
    for drink in drinkDictList:
        if drink['name'] == name:
            dirtyList = convertDictToList(drink)
    ident = (drink['drinkID'],)
    db.execute("UPDATE drinks SET dispense_count = dispense_count + 1 WHERE drink_id = ?", ident)
    db.execute("INSERT INTO dispenses (drink_id) VALUES (?)", ident)
    arduino.sendDrink(dirtyList)
    log.info("Leaving -> Dispense(name) for %s. Found Drink." % name)
    return "Drink successfully passed off to arduino."
    log.error("Leaving -> Dispense(name) for %s. Drink could not be found" % name)
    return "Drink could not be found!"


@app.route('/createDrink/', method='POST')
def createDrinkGet(db):
    drinkName = bottle.request.forms.get('drinkName')
    ing1 = int(bottle.request.forms.get('ing1'))
    ing2 = int(bottle.request.forms.get('ing2'))
    ing3 = int(bottle.request.forms.get('ing3'))
    ing4 = int(bottle.request.forms.get('ing4'))
    ing5 = int(bottle.request.forms.get('ing5'))
    ing6 = int(bottle.request.forms.get('ing6'))
    ing7 = int(bottle.request.forms.get('ing7'))
    ing8 = int(bottle.request.forms.get('ing8'))
    ing9 = int(bottle.request.forms.get('ing9'))
    ing10 = int(bottle.request.forms.get('ing10'))
    ing11 = int(bottle.request.forms.get('ing11'))
    ing12 = int(bottle.request.forms.get('ing12'))
    description = bottle.request.forms.get('description')
    print(drinkName + ", " + str(ing1) + ", " + str(ing2) + ", " + str(ing3) + ", " + str(ing4) + ", " + str(ing5) + ", " + str(ing6) + ", " + str(ing7)
          + ", " + str(ing8) + ", " + str(ing9) + ", " + str(ing10) + ", " + str(ing11) + ", " + str(ing12))
    args = (drinkName, ing1, ing2, ing3, ing4, ing5, ing6, ing7, ing8, ing9, ing10, ing11, ing12, description)
    res = db.execute("INSERT INTO drinks(drink_name, ingredient1, ingredient2, \
                                    ingredient3, ingredient4, ingredient5, \
                                    ingredient6, ingredient7, ingredient8, \
                                    ingredient9, ingredient10, ingredient11, \
                                    ingredient12, description) \
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", args)
    print(res)
    return res


@app.route('/createDrink/', method='GET')
def createDrinkPost(db):
    dataDict = bottle.request.json['theDict']
    print(dataDict)
    dirtyList = convertDictToList(dataDict)
    res = db.execute("INSERT INTO drinks(drink_name, ingredient1, ingredient2, \
                                    ingredient3, ingredient4, ingdredient5, \
                                    ingredient6, ingredient7, ingredient8, \
                                    ingredient9, ingredient10, ingredient11, \
                                    ingredient12, description) \
                            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                     % (dataDict['name'], dirtyList[0], dirtyList[1],
                        dirtyList[2], dirtyList[3], dirtyList[4],
                        dirtyList[5], dirtyList[6], dirtyList[7],
                        dirtyList[8], dirtyList[9], dirtyList[10],
                        dirtyList[11], dataDict['description']))
    print(res)
    return "Call successul!"


@app.route('/dispense/custom/:adHocList')
def dispense_custom(adHocList):
    adHocList = adHocList.split('_')
    dirtyList = []
    for item in adHocList:
        dirtyList.append(int(item))
    arduino.sendDrink(dirtyList)


@app.route('/dispenseProto/', method='POST')
def dispenseProto():
    ingDict = bottle.request.json['theDict']
    print(ingDict)
    drinkName = bottle.request.json['name']
    print(drinkName)
    dirtyList = convertDictToList(ingDict)
    arduino.sendDrink(dirtyList)
    return "Call successul!"


def convertDictToList(ingredientDict):
    dirtyList = []
    for ingredient in range(len(constants.INGREDIENTLIST)):
        try:
            dirtyList.append(int(ingredientDict[constants.INGREDIENTLIST[ingredient]]))
        except KeyError:
            dirtyList.append(0)
    print(dirtyList)
    return dirtyList


@app.route('/wip/')
def wip():
    return bottle.template('createNewDrink')


@app.route('/Analytics')
def Analytics():
    drinkData = []
    return bottle.template('Analytics', data=drinkData)


if __name__ == '__main__':
    localIP = socket.gethostbyname(socket.gethostname())
    bottle.run(app, host='0.0.0.0', port=8083, server='cherrypy')
