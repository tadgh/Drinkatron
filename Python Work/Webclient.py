import logging
import settings
import arduinocomm
import bottle
import bottle_sqlite
import sqlite3
import Canister
import random
import time

arduino = arduinocomm.Connection()

# initializing all the canisters with the ingredients pulled from the DB
canisterList = []
for ingredient in settings.INGREDIENTLIST:
    canisterList.append(Canister.Canister(ingredient))

# quick check to display canister fullness.
for canister in canisterList:
            canister.status()

# setting up the SQLITE plugin
app = bottle.Bottle()
plugin = bottle_sqlite.Plugin(dbfile=settings.DBLOCATION, autocommit=True)
app.install(plugin)


# setting up the logger, and setting bottle to debug mode.
log = logging.getLogger("WEB")
log.setLevel(logging.INFO)
log.info("Entering -> WebClient")
bottle.debug(True)
# initializaing a master list for all drinks that is accessible all
# around webclient.
drinkNames = []
drinkDictList = []
drinkIndexes = {}


def initDrinkList():
    global drinkNames
    global drinkDictList
    drinkList = []
    del drinkDictList[:]
    # one-time SQL connection to snag all drinks in the DB, based on which
    # ingredients are currently in canisters. If an ingredient is not in a
    # canister, it is skipped.
    conn = sqlite3.connect(settings.DBLOCATION)
    cursor = conn.cursor()
    tempDict = {}
    drinkList = cursor.execute('''SELECT T_DRINK.drink_id, T_DRINK.drink_name,
                                T_DRINK.description, T_DRINK.dispense_count,
                                T_DRINK.upvotes, T_DRINK.downvotes,
                                T_DRINK.image_path
                                FROM T_INGREDIENT_INSTANCE
                                INNER JOIN T_DRINK
                                ON T_INGREDIENT_INSTANCE.drink_id = T_DRINK.drink_id
                                LEFT JOIN T_CANISTER
                                ON T_INGREDIENT_INSTANCE.ingredient_id = T_CANISTER.ingredient_id
                                GROUP BY T_DRINK.drink_name
                                HAVING sum(case when T_CANISTER.ingredient_id is null then 1 else 0 end) = 0;
                                ''').fetchall()

    # This whole section is to take the unorganized dict list from the DB
    # and set it to a known list where the keys are all known and obvious.
    # This makes it easier to work with and we can also add validity checks
    # to the data.
    for drink in drinkList:
        keys = ['drinkID', 'name', 'description', 'dispenseCount', 'upvotes', 'downvotes', 'imagePath']
        tempDict = {keys[i]: drink[i] for i in range(7)} #swapped to a comprehension RANGE 7 IS CURRENTLY IMPORTANT
        strID = (str(drink[0]),)
        drink_ing = cursor.execute('''SELECT T_INGREDIENT.ingredient_name, T_INGREDIENT_INSTANCE.amount
                                    FROM  T_Ingredient_instance
                                    INNER JOIN T_INGREDIENT
                                    ON T_INGREDIENT_INSTANCE.ingredient_id = T_INGREDIENT.ingredient_id
                                    LEFT JOIN T_CANISTER
                                    ON T_INGREDIENT_INSTANCE.ingredient_id = T_CANISTER.ingredient_id
                                    WHERE T_INGREDIENT_INSTANCE.drink_id = ? ''', strID).fetchall()
        tempDict.update({ing_pair[0]: ing_pair[1] for ing_pair in drink_ing})
        tempDict['totalSize'] = sum([ing_pair[1] for ing_pair in drink_ing])
        drinkDictList.append(tempDict)
        #stores index of drink in the list for later lookup.
        drinkIndexes[tempDict['name']] = drinkDictList.index(tempDict)


    log.info(drinkIndexes)
    drinkNames = list(drink['name'] for drink in drinkDictList)
    conn.close()


# this is the main page.
@app.route('/')
def index():
    return bottle.template('index', drinkList=drinkNames)


# this is the static file server. TODO: add some validations based on
# extensions.
@app.route('/static/:path#.+#', name='static')
def static(path):
    return bottle.static_file(path, root='./static/')


@app.route('/getDrinks')
def getDrinks():
    return bottle.template('getDrinks', drinkDictList=drinkDictList)

# this sends off the correct drink, from the list, to the template
# that strips out all relevant ingredient data and returns it to the client.


@app.route('/getDrink/:name')
def getDrink(name):
    log.info(name)
    drink = drinkDictList[drinkIndexes[name]]
    log.info(drink)
    # return bottle.template('getDrink', selectedDrink=drink)
    return bottle.template('getDrinkProto', selectedDrink=drink)


# this route allows for the creation of new drinks, and is currently non-
# functional while I work on it to accomodate the DB changes.
@app.route('/createDrink', method='POST')
@app.route('/createDrink/', method='POST')
def createDrinkGet(db):
    newDrink = bottle.request.json['newDrink']
    log.info(newDrink)
    argList = (newDrink['name'], newDrink['description'])
    try:
        # inserting drink information(non-ingredient)
        db.execute("INSERT INTO T_DRINK(drink_name, description) \
                    VALUES(?,?)", argList)

        # grabbing ID of drink we just created
        newDrinkId = db.execute("SELECT T_DRINK.drink_id FROM T_DRINK \
                    WHERE T_DRINK.drink_name = ?", (newDrink['name'],)).fetchone()[0]
        log.info("newDrink ID is: " + str(newDrinkId))
        # using that just-grabbed ID to insert ingredient instances.
        for key in newDrink.keys():
            if key in settings.INGREDIENTLIST:
                # grabbing ingredient ID based on the name.
                ingID = db.execute("SELECT T_INGREDIENT.ingredient_id \
                                    FROM T_INGREDIENT \
                                    WHERE T_INGREDIENT.ingredient_name = ?", (key,)).fetchone()[0]
                log.info("ING ID FOR " + str(key) + " is " + str(ingID))
                # using that ingredient ID and Drink ID to generate the actual
                # instance.
                db.execute("INSERT INTO T_INGREDIENT_INSTANCE(drink_id,ingredient_id,amount) \
                            VALUES (?, ?, ?)", (newDrinkId, ingID, newDrink[key]))

    except Exception as e:
        log.info("Unexpected error in DB insert: " + str(e))

    return "Drink Created"


@app.route('/sortByIngredient/', method="POST")
def sortByIngredient(db):
    log.info("Sorting by ingredient!")
    ingredientDict = bottle.request.json['selectedIngredients']
    if not ingredientDict:
        log.info("no boxes checkd, returning full list")
        return bottle.template('drinkList',
                               drinkList=drinkNames)

    ingList = []

    sqlString = '''SELECT T_INGREDIENT.ingredient_id
                FROM T_INGREDIENT
                WHERE T_INGREDIENT.ingredient_name = ?'''

    for ingredient in ingredientDict.values():
        ingID = db.execute(sqlString, (ingredient,)).fetchone()[0]
        log.info("RETURNED ING ID IS : " + str(ingID))
        ingList.append(ingID)

    sqlString = ""
    argString = []
    for ingredient in ingList:
        if sqlString == "":
            sqlString += '''SELECT T_DRINK.drink_name
                            FROM T_DRINK inner join T_INGREDIENT_INSTANCE
                            ON T_DRINK.drink_id = T_INGREDIENT_INSTANCE.drink_id
                            WHERE T_INGREDIENT_INSTANCE.ingredient_id = ? '''
        else:
            sqlString += '''INTERSECT
                            SELECT T_DRINK.drink_name
                            FROM T_DRINK inner join T_INGREDIENT_INSTANCE
                            ON T_DRINK.drink_id = T_INGREDIENT_INSTANCE.drink_id
                            WHERE T_INGREDIENT_INSTANCE.ingredient_id = ?'''
        argString.append(int(ingredient))

    dbResponse = db.execute(sqlString, argString).fetchall()

    newDrinkNames = [item[0] for item in dbResponse]
    return bottle.template('drinkList', drinkList=newDrinkNames)


@app.route('/remove/:name')
def removeDrink(name,db):

    drinkIndex = drinkIndexes[name]
    try:
        drinkID = drinkDictList[drinkIndex]['drinkID']
    except KeyError:
        log.error("Couldnt find drink named: " + name)

    log.info("Found drink id is: " + str(drinkID))
    args = (drinkID,)

    sql = '''DELETE FROM T_DRINK
            WHERE T_DRINK.drink_id = ?
          '''
    try:
        db.execute(sql, args)
    except:
        log.error("Could not delete " +  name)

    sql ='''DELETE FROM T_INGREDIENT_INSTANCE
            WHERE T_INGREDIENT_INSTANCE.drink_id = ?
        '''

    try:
        db.execute(sql, args)
    except:
        log.error("Could not Delete" + name)

@app.route('/save/', method='POST')
@app.route('/save' , method='POST')
def saveSettings():
    cupType = bottle.request.forms.get('selectedCup')
    settings.change('Current Cup', cupType)
    log.info(cupType)


# simple route which allows a user to increase upvote count on a drink
@app.route('/upvote/:name')
def upvote(name, db):
    start_time = time.time()
    try:
        drinkID = drinkDictList[drinkIndexes[name]]['drinkID']
    except KeyError:
        return 'Could not find drink to upvote'
    sql = '''UPDATE T_DRINK
        SET upvotes = upvotes + 1
        WHERE drink_id = ?
        '''
    args = (drinkID,)
    try:
        db.execute(sql, args).fetchone()
    except:
        log.error("Could not upvote!!")
    log.info("execution time for optimized upvote is " + str(time.time() - start_time) + " seconds.")
    return 'Your vote has been saved. Thank you!'

# simple route which allows a user to increase downvote count on a drink
@app.route('/downvote/:name')
def downvote(name, db):
    start_time = time.time()
    try:
        drinkID = drinkDictList[drinkIndexes[name]]['drinkID']
    except KeyError:
        return 'Could not find drink to downvote'
    sql = '''UPDATE drinks
        SET downvotes = downvotes + 1
        WHERE drink_id = ?
        '''
    args = (drinkID,)
    db.execute(sql, args).fetchone()
    log.info("execution time for optimized upvote is " + str(time.time() - start_time) + " seconds.")
    return 'success'




# This is now the primary createDrink method.
@app.route('/createDrink/', method='GET')
@app.route('/createDrink', method='GET')
def createDrinkPost(db):
    return bottle.template('createNewDrink')
    # pulling the JSON out of the AJAX call from the client.
    dataDict = bottle.request.json['theDict']
    log.info(dataDict)
    dirtyList = convertDictToList(dataDict)

    try:
        # inserting drink information(non-ingredient)
        db.execute("INSERT INTO T_DRINK(drink_name, description \
                    VALUES(?,?)")

        # grabbing ID of drink we just created
        newDrinkId = db.execute("SELECT T_DRINK.drink_id FROM T_DRINK \
                    WHERE T_DRINK.drink_name = ?").fetchone()[0]

        # using that just-grabbed ID to insert ingredient instances.
        for ingredient in newDrinkIngredients:
            # grabbing ingredient ID based on the name.
            ingID = db.execute("SELECT T_INGREDIENT.ingredient_id \
                                FROM T_INGREDIENT \
                                WHERE T_INGREDIENT.ingredient_name = ?").fetchone()[0]
            # using that ingredient ID and Drink ID to generate the actual
            # instance.
            db.execute("INSERT INTO T_INGREDIENT_INSTANCE(drink_id,ingredient_id,amount) \
                        VALUES (?, ?, ?)", (newDrinkId, ingID, amount))

    except:
        return("Unexpected error in DB insert")

    log.info(res)
    return "Call successul!"


# route which grabs a random drink out of the list, and dispenses it.
@app.route('/dispense/random')
def randomDrink(db):
    randomDrink = drinkDictList[random.randint(0, len(drinkDictList))]
    # DB method is included here because the subsequent dispense call needs it.
    # This is a re-route to /dispense/known/:name
    dispense(randomDrink['name'], db)
    return "You received: " + randomDrink['name']

# Old primary dispense tool. Dispenses by name lookup in the dictionary list.




# Old primary custom dispenser based on an ingredientlist delimited by
# underscores.
@app.route('/dispense/custom/:adHocList')
def dispense_custom(adHocList):
    adHocList = adHocList.split('_')
    dirtyList = []
    for item in adHocList:
        dirtyList.append(int(item))
    response = pourDrink(dirtyList)
    return response

# This is the new dispense route, currently a prototype, which simply accepts
# JSON dicts and has them dispensed based on the ConvertDictToList function.
# TODO: add dispense logging based on drinkName.


@app.route('/dispenseProto/', method='POST')
def dispenseProto():
    ingDict = bottle.request.json['theDict']
    drinkName = bottle.request.json['name']
    dirtyList = convertDictToList(ingDict)
    response = pourDrink(dirtyList)
    return response

# This is the hackiest shit ever, but the arduino only accepts precisely 12
# numbers. Therefore, before a drink is dispensed, we have to stuff the list
# in the right order.


def convertDictToList(ingredientDict):
    dirtyList = []

    # Here is what is happening:
    # 1. There are 12 canisters. The For Loop goes through each of them in order.(i)
    # 2. It attempts to append the value of the particular ingredient frmo the ingredientDict
    # 3. If it results in a key error, that is, that key does not exist, that is, that ingredient is not used in the drink,
    # Then it simply appends 0. We need to do this, because the arduino always accepts exactly 12 numbers, and no keys, only their
    # Physical canister positions are important.
    # 4. Seeing as when we initialize all the ingredients in the canisters at the start, this will work even if we move where
    # Each ingredient is.
    for ingredient in range(len(settings.INGREDIENTLIST)):
        try:
            dirtyList.append(int(ingredientDict[settings.INGREDIENTLIST[ingredient]]))
        except KeyError:
            dirtyList.append(0)
    log.info(dirtyList)
    return dirtyList

# All dispense methods eventually
# route here. Here we calculated proportions to ensure that all drinks
# are crunched into 75 units(our approximate solo cup size)


def pourDrink(drinkArray):
    drinkSize = 0
    for item in drinkArray:
        drinkSize += item
    #todo change this 75 value to the value from settings.py that is generated.
    cleanedList = [round(drinkArray[i] / float(drinkSize) * 75) for i in range(len(drinkArray))]
    index = 0
    # Preliminary check that we can dispense all necessary ingredients without
    # hitting under a certain threshold(<10%)
    for units in cleanedList:
        if not canisterList[index].canDispense(units):
            log.error("Not enough units, couldnt finish dispensing: " + canisterList[
                      index].getContents())
            return "Couldnt finish dispensing: " + canisterList[index].getContents()
        index += 1

    index = 0
    # actual units are removed from the canisters here.
    for units in cleanedList:
        try:
            canisterList[index].dispense(units)
            index += 1
        except ValueError as e:
            log.error("Couldnt finish dispensing: " + str(e))
            return "Couldnt finish dispensing: " + str(e)

    for canister in canisterList:
        canister.status()
    # the magic. Sends each ingredient off to the arduino, returns the response
    # from arduinocomm as to the failure or success value.
    resp = arduino.sendDrink(cleanedList)
    # this response is then returned to the webpage.
    return resp


@app.route('/Settings', method='GET')
@app.route('/Settings/', method='GET')
def userSettings():
    return bottle.template('settings', userSettings=settings.USERSETTINGS,
                           cupInfo=settings.CUPINFO)

#THIS IS DEPRECATED AND UNUSED. Keeping it around because who knows.
@app.route('/dispense/known/:name')
def dispense(name, db):
    log.info("Entering -> Dispense(name) for %s" % name)
    dirtyList = []
    for drink in drinkDictList:
        if drink['name'] == name:
            dirtyList = convertDictToList(drink)
            ident = (drink['drinkID'],)
            db.execute(
                "UPDATE T_DRINK SET dispense_count = dispense_count + 1 WHERE drink_id = ?", ident)
            db.execute("INSERT INTO T_DISPENSE (drink_id) VALUES (?)", ident)
            response = pourDrink(dirtyList)
            return response
            log.info("Leaving -> Dispense(name) for %s. Found Drink." % name)
    log.error("Leaving -> Dispense(name) for %s. Drink could not be found" %
              name)
    return "Drink could not be found!"


@app.route('/Analytics')
def Analytics():
    drinkData = []
    return bottle.template('Analytics', data=drinkData)


@app.error(404)
def mistake404(code):
    return bottle.template('404')

if __name__ == '__main__':
    initDrinkList()
    bottle.run(app, host='0.0.0.0', port=80, server='cherrypy')
