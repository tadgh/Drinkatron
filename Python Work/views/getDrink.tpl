%import constants
<html>
<head>
	<title>{{selectedDrink['name']}}</title>
	<script type="text/javascript" src='/static/jquery-2.0.0.min.js'></script>


<script type="text/javascript">
$(document).ready(function() {

    $("#btnDispense").click(function()
        {
             $.ajax({
                url: "/dispense/known/{{selectedDrink['name']}}",
                type: "get"
            });
        });
});

</script>
</head>
<body>
<h2>{{selectedDrink['name']}}</h2> <br>
{{constants.INGREDIENTLIST[0]}} : {{selectedDrink[constants.INGREDIENTLIST[0]]}} <br>
{{constants.INGREDIENTLIST[1]}} : {{selectedDrink[constants.INGREDIENTLIST[1]]}} <br>
{{constants.INGREDIENTLIST[2]}} : {{selectedDrink[constants.INGREDIENTLIST[2]]}} <br>
{{constants.INGREDIENTLIST[3]}} : {{selectedDrink[constants.INGREDIENTLIST[3]]}} <br>
{{constants.INGREDIENTLIST[4]}} : {{selectedDrink[constants.INGREDIENTLIST[4]]}} <br>
{{constants.INGREDIENTLIST[5]}} : {{selectedDrink[constants.INGREDIENTLIST[5]]}} <br>
{{constants.INGREDIENTLIST[6]}} : {{selectedDrink[constants.INGREDIENTLIST[6]]}} <br>
{{constants.INGREDIENTLIST[7]}} : {{selectedDrink[constants.INGREDIENTLIST[7]]}} <br>
{{constants.INGREDIENTLIST[8]}} : {{selectedDrink[constants.INGREDIENTLIST[8]]}} <br>
{{constants.INGREDIENTLIST[9]}} : {{selectedDrink[constants.INGREDIENTLIST[9]]}} <br>
{{constants.INGREDIENTLIST[10]}} :{{selectedDrink[constants.INGREDIENTLIST[10]]}} <br>
{{constants.INGREDIENTLIST[11]}} :{{selectedDrink[constants.INGREDIENTLIST[11]]}} <br>
<button id="btnDispense">Dispense</button>
<img src="/static/resources/images/{{selectedDrink['imagePath']}}">
</body>
</html>