import drinks
import logging
import constants
import arduinocomm
import bottle
import bottle_sqlite
import sqlite3
import socket
import Canister
import random
import pickle

arduino = arduinocomm.Connection()

canisterList = []
for ingredient in constants.INGREDIENTLIST:
    canisterList.append(Canister.Canister(ingredient))

for canister in canisterList:
            canister.status()

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
    tempDict = {}
    #drinkList = cursor.execute("SELECT * FROM drinks ORDER BY drink_name ASC").fetchall()
    drinkList = cursor.execute('''SELECT T_DRINK.drink_id, T_DRINK.drink_name, T_DRINK.description, T_DRINK.dispense_count
                                FROM T_INGREDIENT_INSTANCE
                                INNER JOIN T_DRINK
                                ON T_INGREDIENT_INSTANCE.drink_id = T_DRINK.drink_id
                                LEFT JOIN T_CANISTER
                                ON T_INGREDIENT_INSTANCE.ingredient_id = T_CANISTER.ingredient_id
                                GROUP BY T_DRINK.drink_name
                                HAVING sum(case when T_CANISTER.ingredient_id is null then 1 else 0 end) = 0;
                                ''').fetchall()

    print(drinkList)
    for drink in drinkList:
        tempDict = {}
        tempDict['drinkID'] = drink[0]
        tempDict['name'] = drink[1]
        tempDict['description'] = drink[2]
        tempDict['dispenseCount'] = drink[3]
        #initially set all ingredients to 0
        for ingredient in constants.INGREDIENTLIST:
            tempDict[ingredient] = 0

        print(tempDict)
        strID = (str(drink[0]),)
        drinkIng = cursor.execute('''SELECT T_INGREDIENT.ingredient_name, T_INGREDIENT_INSTANCE.amount
                                    FROM  T_Ingredient_instance
                                    INNER JOIN T_INGREDIENT
                                    ON T_INGREDIENT_INSTANCE.ingredient_id = T_INGREDIENT.ingredient_id
                                    LEFT JOIN T_CANISTER
                                    ON T_INGREDIENT_INSTANCE.ingredient_id = T_CANISTER.ingredient_id
                                    WHERE T_INGREDIENT_INSTANCE.drink_id = ? ''', strID).fetchall()
        totalSize = 0
        #setting relevant ingredients to non-zero.
        for ingPair in drinkIng:
            tempDict[ingPair[0]] = ingPair[1]
            totalSize += ingPair[1]

        tempDict['totalSize'] = totalSize
        drinkDictList.append(tempDict)




    #for currentDrink in range(len(drinkList)):
    #    tempDrink = drinks.drink(*drinkList[currentDrink])
    #    drinkDictList.append(tempDrink.convertToDict())
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


@app.route('/createDrink', method='POST')
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
    try:
        db.execute("INSERT INTO drinks(drink_name, ingredient1, ingredient2, \
                                        ingredient3, ingredient4, ingredient5, \
                                        ingredient6, ingredient7, ingredient8, \
                                        ingredient9, ingredient10, ingredient11, \
                                        ingredient12, description) \
                                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", args)
    except:
        print("Unexpected error in DB insert")

    return "Drink Created"


@app.route('/upvote/:name')
def upvote(name, db):
    for drink in drinkDictList:
        if drink['name'] == name:
            drinkID = drink['drinkID']
            sql = '''UPDATE drinks
                SET positive_vote_count = positive_vote_count + 1
                WHERE drink_id = ?
                '''
            args = (drinkID,)
            db.execute(sql, args).fetchone()
            return 'success'
        else:
            drinkID = None
    return 'Could not find drink to upvote'


@app.route('/downvote/:name')
def downvote(name, db):
    for drink in drinkDictList:
        if drink['name'] == name:
            drinkID = drink['drinkID']
            sql = '''UPDATE drinks
                SET negative_vote_count = negative_vote_count + 1
                WHERE drink_id = ?
                '''
            args = (drinkID,)
            db.execute(sql, args).fetchone()
            return 'success'
        else:
            drinkID = None
    return 'Could not find drink to downvote'


@app.route('/createDrink/', method='GET')
@app.route('/createDrink', method='GET')
def createDrinkPost(db):
    return bottle.template('createNewDrink')
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


@app.route('/dispense/random')
def randomDrink(db):
    randomDrink = drinkDictList[random.randint(0, len(drinkDictList))]
    # DB method is included here because the subsequent dispense call needs it.
    dispense(randomDrink['name'], db)
    return "You received: " + randomDrink['name']


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
            response = pourDrink(dirtyList)
            return response
            log.info("Leaving -> Dispense(name) for %s. Found Drink." % name)
    log.error("Leaving -> Dispense(name) for %s. Drink could not be found" % name)
    return "Drink could not be found!"


@app.route('/dispense/custom/:adHocList')
def dispense_custom(adHocList):
    adHocList = adHocList.split('_')
    dirtyList = []
    for item in adHocList:
        dirtyList.append(int(item))
    response = pourDrink(dirtyList)
    return response


@app.route('/dispenseProto/', method='POST')
def dispenseProto():
    ingDict = bottle.request.json['theDict']
    drinkName = bottle.request.json['name']
    dirtyList = convertDictToList(ingDict)
    response = pourDrink(dirtyList)
    return response


def convertDictToList(ingredientDict):
    dirtyList = []
    for ingredient in range(len(constants.INGREDIENTLIST)):
        try:
            dirtyList.append(int(ingredientDict[constants.INGREDIENTLIST[ingredient]]))
        except KeyError:
            dirtyList.append(0)
    print(dirtyList)
    return dirtyList


def pourDrink(drinkArray):
    cleanedList = []
    drinkSize = 0
    for item in drinkArray:
        drinkSize += item
    for i in range(len(drinkArray)):
        # this is disgusting and we need to find proper dispense time.
        # can use list comprehension instead here.
        cleanedList.append(round(drinkArray[i]/float(drinkSize)*75))

    index = 0
    for units in cleanedList:
        if not canisterList[index].canDispense(units):
            log.error("Not enough units, couldnt finish dispensing: " + canisterList[index].getContents())
            return "Couldnt finish dispensing: " + canisterList[index].getContents()
        index += 1

    index = 0
    for units in cleanedList:
        try:
            canisterList[index].dispense(units)
            index += 1
        except ValueError as e:
            log.error("Couldnt finish dispensing: " + str(e))
            return "Couldnt finish dispensing: " + str(e)

    for canister in canisterList:
        canister.status()

    resp = arduino.sendDrink(cleanedList)
    return resp

@app.route('/Settings', method='GET')
@app.route('/Settings/', method='GET')
def userSettings():
    return bottle.template('settings', userSettings=constants.USERSETTINGS,
                           cupInfo=constants.CUPINFO)


@app.route('/Analytics')
def Analytics():
    drinkData = []
    return bottle.template('Analytics', data=drinkData)


@app.error(404)
def mistake404(code):
    return bottle.template('404')

if __name__ == '__main__':
    localIP = socket.gethostbyname(socket.gethostname())
    bottle.run(app, host='0.0.0.0', port=80, server='cherrypy')
