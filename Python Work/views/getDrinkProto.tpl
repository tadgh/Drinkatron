%import constants
<html>
<head>
	<title>{{selectedDrink['name']}}</title>
	<script type="text/javascript" src='/static/jquery-2.0.0.min.js'></script>
	<link rel="stylesheet" type="text/css" href="/static/css/bt-style.css">
	<link href='http://fonts.googleapis.com/css?family=Lato:700,900' rel='stylesheet' type='text/css'>

%totalSize = 0
%for ingredient in constants.INGREDIENTLIST:
	%totalSize += selectedDrink[ingredient]
%end
</head>
<body>
	%for ingredient in constants.INGREDIENTLIST:
		%if selectedDrink[ingredient] != 0:
			<li>{{ingredient}} : {{selectedDrink[ingredient]}}</li> <br>
			<input id="defaultSlider" type="range" min="0" max="100" step="1" value='{{( selectedDrink[ingredient] / totalSize) * 100}}' />
		%end
	%end
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
li
{
	font-size: 15; fon
}
</style>

</html>

