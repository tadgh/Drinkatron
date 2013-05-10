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

arduino = arduinocomm.Connection()

#initializing all the canisters with the ingredients pulled from the DB
canisterList = []
for ingredient in constants.INGREDIENTLIST:
    canisterList.append(Canister.Canister(ingredient))

#quick check to display canister fullness.
for canister in canisterList:
            canister.status()

#setting up the SQLITE plugin
app = bottle.Bottle()
plugin = bottle_sqlite.Plugin(dbfile=constants.DBLOCATION, autocommit=True)
app.install(plugin)


#setting up the logger, and setting bottle to debug mode.
log = logging.getLogger("WEB")
log.setLevel(logging.INFO)
log.info("Entering -> WebClient")
bottle.debug(True)
#initializaing a master list for all drinks that is accessible all
#around webclient.
drinkDictList = []

#this is the main page.
@app.route('/')
def index():
    drinkList = []
    del drinkDictList[:]
    #one-time SQL connection to snag all drinks in the DB, based on which
    #ingredients are currently in canisters. If an ingredient is not in a
    #canister, it is skipped.
    conn = sqlite3.connect(constants.DBLOCATION)
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

    print(drinkList)
    #This whole section is to take the unorganized dict list from the DB
    #and set it to a known list where the keys are all known and obvious.
    #This makes it easier to work with and we can also add validity checks
    #to the data.
    for drink in drinkList:
        tempDict = {}
        tempDict['drinkID'] = drink[0]
        tempDict['name'] = drink[1]
        tempDict['description'] = drink[2]
        tempDict['dispenseCount'] = drink[3]
        tempDict['upvotes'] = drink[4]
        tempDict['downvotes'] = drink[5]
        tempDict['imagePath'] = drink[6]
        #initially set all ingredients to 0 for KeyError avoidance
        for ingredient in constants.INGREDIENTLIST:
            tempDict[ingredient] = 0
        print(tempDict)
        #The following SQLITE call hits the ingredient_instance table
        #in order to grab all associated ingredients based on drink_id.
        strID = (str(drink[0]),)
        drinkIng = cursor.execute('''SELECT T_INGREDIENT.ingredient_name, T_INGREDIENT_INSTANCE.amount
                                    FROM  T_Ingredient_instance
                                    INNER JOIN T_INGREDIENT
                                    ON T_INGREDIENT_INSTANCE.ingredient_id = T_INGREDIENT.ingredient_id
                                    LEFT JOIN T_CANISTER
                                    ON T_INGREDIENT_INSTANCE.ingredient_id = T_CANISTER.ingredient_id
                                    WHERE T_INGREDIENT_INSTANCE.drink_id = ? ''', strID).fetchall()
        totalSize = 0
        #setting relevant ingredients to non-zero, and also getting
        #total size of the drink for future calculations.
        for ingPair in drinkIng:
            tempDict[ingPair[0]] = ingPair[1]
            totalSize += ingPair[1]
        tempDict['totalSize'] = totalSize
        drinkDictList.append(tempDict)

    conn.close()
    return bottle.template('index', drinkList=drinkDictList)


#this is the static file server. TODO: add some validations based on
#extensions.
@app.route('/static/:path#.+#', name='static')
def static(path):
    return bottle.static_file(path, root='./static/')


@app.route('/getDrinks')
def getDrinks():
    return bottle.template('getDrinks', drinkDictList=drinkDictList)

#this sends off the correct drink, from the list, to the template
#that strips out all relevant ingredient data and returns it to the client.
@app.route('/getDrink/:name')
def getDrink(name):
    print(name)
    for drink in drinkDictList:
        if drink['name'] == name:
            print(drink)
            # return bottle.template('getDrink', selectedDrink=drink)
            return bottle.template('getDrinkProto', selectedDrink=drink)


#this route allows for the creation of new drinks, and is currently non-
#functional while I work on it to accomodate the DB changes.
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

    try:
        #inserting drink information(non-ingredient)
        db.execute("INSERT INTO T_DRINK(drink_name, description \
                    VALUES(?,?)")

        #grabbing ID of drink we just created
        newDrinkId = db.execute("SELECT T_DRINK.drink_id FROM T_DRINK \
                    WHERE T_DRINK.drink_name = ?").fetchone()

        #using that just-grabbed ID to insert ingredient instances.
        for ingredient in newDrinkIngredients:

            #grabbing ingredient ID based on the name.
            ingID = db.execute("SELECT T_INGREDIENT.ingredient_id \
                                FROM T_INGREDIENT \
                                WHERE T_INGREDIENT.drink_name = ?")

            #using that ingredient ID and Drink ID to generate the actual
            #instance.
            db.execute("INSERT INTO T_INGREDIENT_INSTANCE(drink_id,ingredient_id,amount) \
                        VALUES (?, ?, ?)")

    except:
        return("Unexpected error in DB insert")

    return "Drink Created"

#simple route which allows a user to increase upvote count on a drink
@app.route('/upvote/:name')
def upvote(name, db):
    for drink in drinkDictList:
        if drink['name'] == name:
            drinkID = drink['drinkID']
            sql = '''UPDATE T_DRINK
                SET upvotes = upvotes + 1
                WHERE drink_id = ?
                '''
            args = (drinkID,)
            db.execute(sql, args).fetchone()
            return 'success'
        else:
            drinkID = None
    return 'Could not find drink to upvote'

#simple route which allows a user to increase downvote count on a drink
@app.route('/downvote/:name')
def downvote(name, db):
    for drink in drinkDictList:
        if drink['name'] == name:
            drinkID = drink['drinkID']
            sql = '''UPDATE drinks
                SET downvotes = downvotes + 1
                WHERE drink_id = ?
                '''
            args = (drinkID,)
            db.execute(sql, args).fetchone()
            return 'success'
        else:
            drinkID = None
    return 'Could not find drink to downvote'

#this is the GET version of createdrink, which just does the same thing
#in a different way. Will probably delete this or the other once i fix the DB thing.
@app.route('/createDrink/', method='GET')
@app.route('/createDrink', method='GET')
def createDrinkPost(db):
    return bottle.template('createNewDrink')
    #pulling the JSON out of the AJAX call from the client.
    dataDict = bottle.request.json['theDict']
    print(dataDict)
    dirtyList = convertDictToList(dataDict)
    res = db.execute("INSERT INTO T_DRINK(drink_name, ingredient1, ingredient2, \
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


#route which grabs a random drink out of the list, and dispenses it.
@app.route('/dispense/random')
def randomDrink(db):
    randomDrink = drinkDictList[random.randint(0, len(drinkDictList))]
    # DB method is included here because the subsequent dispense call needs it.
    # This is a re-route to /dispense/known/:name
    dispense(randomDrink['name'], db)
    return "You received: " + randomDrink['name']

#Old primary dispense tool. Dispenses by name lookup in the dictionary list.
@app.route('/dispense/known/:name')
def dispense(name, db):
    log.info("Entering -> Dispense(name) for %s" % name)
    dirtyList = []
    for drink in drinkDictList:
        if drink['name'] == name:
            dirtyList = convertDictToList(drink)
            ident = (drink['drinkID'],)
            db.execute("UPDATE T_DRINK SET dispense_count = dispense_count + 1 WHERE drink_id = ?", ident)
            db.execute("INSERT INTO T_DISPENSE (drink_id) VALUES (?)", ident)
            response = pourDrink(dirtyList)
            return response
            log.info("Leaving -> Dispense(name) for %s. Found Drink." % name)
    log.error("Leaving -> Dispense(name) for %s. Drink could not be found" % name)
    return "Drink could not be found!"


#Old primary custom dispenser based on an ingredientlist delimited by underscores.
@app.route('/dispense/custom/:adHocList')
def dispense_custom(adHocList):
    adHocList = adHocList.split('_')
    dirtyList = []
    for item in adHocList:
        dirtyList.append(int(item))
    response = pourDrink(dirtyList)
    return response

#This is the new dispense route, currently a prototype, which simply accepts
#JSON dicts and has them dispensed based on the ConvertDictToList function.
#TODO: add dispense logging based on drinkName.
@app.route('/dispenseProto/', method='POST')
def dispenseProto():
    ingDict = bottle.request.json['theDict']
    drinkName = bottle.request.json['name']
    dirtyList = convertDictToList(ingDict)
    response = pourDrink(dirtyList)
    return response

#This is the hackiest shit ever, but the arduino only accepts precisely 12
#numbers. Therefore, before a drink is dispensed, we have to stuff the list
#in the right order.
def convertDictToList(ingredientDict):
    dirtyList = []
    for ingredient in range(len(constants.INGREDIENTLIST)):
        try:
            dirtyList.append(int(ingredientDict[constants.INGREDIENTLIST[ingredient]]))
        except KeyError:
            dirtyList.append(0)
    print(dirtyList)
    return dirtyList

#This is the grand-daddy of all dispensing, All dispense methods eventually
#route here. Here we calculated proportions to ensure that all drinks
#are crunched into 75 units(our approximate solo cup size)
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
    #Preliminary check that we can dispense all necessary ingredients without
    #hitting under a certain threshold(<10%)
    for units in cleanedList:
        if not canisterList[index].canDispense(units):
            log.error("Not enough units, couldnt finish dispensing: " + canisterList[index].getContents())
            return "Couldnt finish dispensing: " + canisterList[index].getContents()
        index += 1

    index = 0
    #actual units are removed from the canisters here.
    for units in cleanedList:
        try:
            canisterList[index].dispense(units)
            index += 1
        except ValueError as e:
            log.error("Couldnt finish dispensing: " + str(e))
            return "Couldnt finish dispensing: " + str(e)

    for canister in canisterList:
        canister.status()
    #the magic. Sends each ingredient off to the arduino, returns the response
    #from arduinocomm as to the failure or success value.
    resp = arduino.sendDrink(cleanedList)
    #this response is then returned to the webpage.
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
