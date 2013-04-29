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
drinkList = []
drinkObjArray = []
drinkDictList = []


@app.route('/')
def index():
    #return bottle.template('index', drinkList=drinkDictList)
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
            #return bottle.template('getDrink', selectedDrink=drink)
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



@app.route('/Analytics')
def Analytics():
    drinkData = []
    return bottle.template('Analytics', data=drinkData)


if __name__ == '__main__':
    conn = sqlite3.connect(constants.DBLOCATION)
    cursor = conn.cursor()
    drinkList = cursor.execute("SELECT * FROM drinks ORDER BY drink_name ASC").fetchall()
    for currentDrink in range(len(drinkList)):
        tempDrink = drinks.drink(*drinkList[currentDrink])
        drinkDictList.append(tempDrink.convertToDict())
    conn.close()
    localIP = socket.gethostbyname(socket.gethostname())
    bottle.run(app, host='0.0.0.0', port=8083, server='cherrypy')
