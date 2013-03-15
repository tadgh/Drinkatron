import bottle
import bottle_sqlite
import dbinterface
import drinks
import logging

log = logging.getLogger("WEB")
log.info("Entering -> WebClient")

db = dbinterface.DB()
drinkList = db.listDrinksByName()
drinkList = db.listDrinksByName()
########################################
#THIS IS CRUCIAL. this code initializes ALL drinks into an array, all at once. DO NOT FUCK WITH THIS CODE.
drinkObjArray = []
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
    return '''
            <!DOCTYPE html>
            <html>


            <p>Click the button to trigger a function.</p>
            <script type="text/javascript" src="http://code.jquery.com/jquery-latest.js"></script>

            <script type="text/javascript">
            $(document).ready(function() {

                $("#btnGetDrinks").click(function()
                    {
                         $.ajax({
                            url: "/getDrinks",
                            type: "get",
                            success: function(data){
                                //alert(data);
                                $("#divDrinkList").html(data)
                            }
                        });
                    });
            });


            </script>
            <body>
            <button id="btnGetDrinks">button1</button>
            <div id="divDrinkList"></div>
            </body>
            </html>
    '''


@bottle.route('/getDrinks')
def getDrinks():
    drinkList = db.listDrinksByName()
    returnHTML = ""
    for item in drinkDictList:
        returnHTML += item['name'] + "</br>"
    return returnHTML
@bottle.route('/getDrink/:name')
def getDrink(name):
    pass



bottle.run(host='localhost', port=8082)

