import bottle
import bottle_sqlite
import dbinterface
import drinks




db = dbinterface.DB()
drinkList = db.listDrinksByName()
drinkList = db.listDrinksByName()
########################################
#THIS IS CRUCIAL. this code initializes ALL drinks into an array, all at once. DO NOT FUCK WITH THIS CODE.
drinkObjArray = []
for currentDrink in range(len(drinkList)):
    drinkObjArray.append(drinks.drink(*drinkList[currentDrink]))
    db.log.info(drinkObjArray[currentDrink].drinkName)
    #######################################





@bottle.route('/')
def index():
    return '''
            <!DOCTYPE html>
            <html>
            <body>

            <p>Click the button to trigger a function.</p>
            <a href="/getDrinks">get Drinks</a>
            <button onclick="$.ajax({url='localhost:8082/getDrinks'})"> button 1</button>


            </body>
            </html>
    '''


@bottle.route('/getDrinks')
def getDrinks():
    drinkList = db.listDrinksByName()
    returnHTML = ""
    print("WOOHOO")
    for item in drinkList:
        returnHTML += item[1] + "</br>"
    return returnHTML



bottle.run(host='localhost', port=8082)

