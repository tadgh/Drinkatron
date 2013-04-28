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
<h2>{{selectedDrink['name']}}</h2>

<table width="400px">
	<tr>
		<td width="70%" height='200px'>
			<div id="ingList">
				<ul><br>
					%for ingredient in constants.INGREDIENTLIST:
						%if selectedDrink[ingredient] != 0:
							<li><font size='5'>{{ingredient}} : {{selectedDrink[ingredient]}}</font></li>

						%end
					%end
				</ul>
			</div>
		</td>
		<td width="30%" height='200px'>
			<div>
				<button id="btnDispense" ><img src="/static/resources/images/green_checkmark.gif"></img></button>
			</div>
		</td>
	</tr>
	<tr>
		<td colspan="2" height='400px'>
			<img src="/static/resources/images/{{selectedDrink['imagePath']}}">
		</td>
	</tr>
</table>
</body></html>

