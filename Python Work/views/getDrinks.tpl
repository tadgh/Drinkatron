%import constants
<!DOCTYPE html>
<html>
<head>
    <title>getDrinks</title>
</head>
<body>
    <table border = '1'>
        <tr>
            %for headerItem in ["Drink ID", "Drink Name",'Total Size', 'Dispense Count', 'Star Rating']:
                <td>{{headerItem}}</td>
            %end
            %for headerItem in constants.INGREDIENTLIST:
                <td>{{headerItem}}</td>
            %end
        </tr>
        %for drink in drinkDictList:
        <tr>
            <td>{{drink['drinkID']}}</td>
            <td>{{drink['name']}}</td>
            <td>{{drink['totalSize']}}</td>
            <td>{{drink['dispenseCount']}}</td>
            <td>{{drink['starRating']}}</td>
            <td>{{int(drink[constants.INGREDIENTLIST[0]])}}</td>
            <td>{{int(drink[constants.INGREDIENTLIST[1]])}}</td>
            <td>{{int(drink[constants.INGREDIENTLIST[2]])}}</td>
            <td>{{int(drink[constants.INGREDIENTLIST[3]])}}</td>
            <td>{{int(drink[constants.INGREDIENTLIST[4]])}}</td>
            <td>{{int(drink[constants.INGREDIENTLIST[5]])}}</td>
            <td>{{int(drink[constants.INGREDIENTLIST[6]])}}</td>
            <td>{{int(drink[constants.INGREDIENTLIST[7]])}}</td>
            <td>{{int(drink[constants.INGREDIENTLIST[8]])}}</td>
            <td>{{int(drink[constants.INGREDIENTLIST[9]])}}</td>
            <td>{{int(drink[constants.INGREDIENTLIST[10]])}}</td>
            <td>{{int(drink[constants.INGREDIENTLIST[11]])}}</td>
        </tr>
        %end
     </table>
</body>
</html>