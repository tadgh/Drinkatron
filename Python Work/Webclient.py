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


            <p>Click the button to trigger a function.</p>
            <script type="text/javascript" src="http://code.jquery.com/jquery-latest.js"></script>

            <script type="text/javascript">
            $(document).ready(function() {

                $("button").click(function()
                    {
                         $.ajax({
                            url: "/getDrinks",
                            type: "get",
                            success: function(data){
                                alert(data);
                            }
                        });
                    });
            });


            </script>
            <body>
            <button>button1</button>
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

