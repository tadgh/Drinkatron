%import constants
<html>
<head>
	<title>createDrink</title>
	<meta name="author" content="Ryan Novak" />
	<meta charset="UTF-8" />
	<script type="text/javascript" src="../static/jquery-2.0.0.min.js"></script>
	<script type="text/javascript" src="http://code.jquery.com/ui/1.9.2/jquery-ui.js"></script>


	<script type="text/javascript">

		$(document).ready(function() {
			$("#createDrink").click(function()
			{
				drinkDict = {};
				drinkDict['name'] = $("input[name=drinkName]").val();
				drinkDict['description'] = $("input[name=description]").val()
				$(".ingBox").each(function()
				{
					if($(this).val() != 0)
					{
						drinkDict[$(this).attr("name")] = $(this).val();
					}
				});
				console.log(drinkDict);
		        $.ajax({
		            type: "POST",
		            url:  "/createDrink/",
		            data: JSON.stringify(
		            {
		                newDrink: drinkDict
		            }),
		            contentType: "application/json; charset=utf-8",
		            success: function(data)
		            {
		                alert(data)
	           		}
        	});

			});
		});
	</script>
</head>
<body>
<form name="newDrinkForm" action="*" method="post">
	<input name='drinkName' type="text" value="name"><br>
	<input name='{{constants.INGREDIENTLIST[0]}}' class='ingBox' type="number" value='0'>{{constants.INGREDIENTLIST[0]}}<br>
	<input name='{{constants.INGREDIENTLIST[1]}}' class='ingBox' type="number" value='0'>{{constants.INGREDIENTLIST[1]}}<br>
	<input name='{{constants.INGREDIENTLIST[2]}}' class='ingBox' type="number" value='0'>{{constants.INGREDIENTLIST[2]}}<br>
	<input name='{{constants.INGREDIENTLIST[3]}}' class='ingBox' type="number" value='0'>{{constants.INGREDIENTLIST[3]}}<br>
	<input name='{{constants.INGREDIENTLIST[4]}}' class='ingBox' type="number" value='0'>{{constants.INGREDIENTLIST[4]}}<br>
	<input name='{{constants.INGREDIENTLIST[5]}}' class='ingBox' type="number" value='0'>{{constants.INGREDIENTLIST[5]}}<br>
	<input name='{{constants.INGREDIENTLIST[6]}}' class='ingBox' type="number" value='0'>{{constants.INGREDIENTLIST[6]}}<br>
	<input name='{{constants.INGREDIENTLIST[7]}}' class='ingBox' type="number" value='0'>{{constants.INGREDIENTLIST[7]}}<br>
	<input name='{{constants.INGREDIENTLIST[8]}}' class='ingBox' type="number" value='0'>{{constants.INGREDIENTLIST[8]}}<br>
	<input name='{{constants.INGREDIENTLIST[9]}}' class='ingBox' type="number" value='0'>{{constants.INGREDIENTLIST[9]}}<br>
	<input name='{{constants.INGREDIENTLIST[10]}}' class='ingBox' type="number" value='0'>{{constants.INGREDIENTLIST[10]}}<br>
	<input name='{{constants.INGREDIENTLIST[11]}}' class='ingBox' type="number" value='0'>{{constants.INGREDIENTLIST[11]}}<br>
	<input name='description' type="text" value="Description"><br>
	<input type="submit" id='submitBut' value="submit" />
</form>
<button id='createDrink'>create Drink</button>
</body>
</html>