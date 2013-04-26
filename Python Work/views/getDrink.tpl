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
<div id="ingList">
	<ul><br>
		%for ingredient in constants.INGREDIENTLIST:
			%if selectedDrink[ingredient] != 0:
				<li>{{ingredient}} : {{selectedDrink[ingredient]}}</li>
			%end
		%end
	</ul>

</div>
<div>
	<button id="btnDispense" ><img src="/static/resources/images/green_checkmark.gif"></img></button>
</div>
<img src="/static/resources/images/{{selectedDrink['imagePath']}}">
</body>


<style type="text/css">
li
{
	color: white
}
h2
{
	color: white
}
div
{
	float: left
}
button
{
	width: 100; height: 100; float: right;
}
</style>

</html>

