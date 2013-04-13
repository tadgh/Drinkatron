<!DOCTYPE html>
<html>
<head>
    <title>getDrinks</title>
</head>
<body>
    <table border = '1'>
        <tr>
            %for headerItem in ["Drink ID", "Drink Name",'ing1','ing2','ing3','ing4','ing5','ing6','ing7','ing8','ing9','ing10','ing11','ing12','Total Size', 'Dispense Count', 'Star Rating']:
                <td>{{headerItem}}</td>
            %end
        </tr>
        %for drink in drinkDictList:
        <tr>
            <td>{{drink['drinkID']}}</td>
            <td>{{drink['name']}}</td>
            <td>{{int(drink['ing1'])}}</td>
            <td>{{int(drink['ing2'])}}</td>
            <td>{{int(drink['ing3'])}}</td>
            <td>{{int(drink['ing4'])}}</td>
            <td>{{int(drink['ing5'])}}</td>
            <td>{{int(drink['ing6'])}}</td>
            <td>{{int(drink['ing7'])}}</td>
            <td>{{int(drink['ing8'])}}</td>
            <td>{{int(drink['ing9'])}}</td>
            <td>{{int(drink['ing10'])}}</td>
            <td>{{int(drink['ing11'])}}</td>
            <td>{{int(drink['ing12'])}}</td>
            <td>{{drink['totalSize']}}</td>
            <td>{{drink['dispenseCount']}}</td>
            <td>{{drink['starRating']}}</td>
        </tr>
        %end
     </table>
</body>
</html>