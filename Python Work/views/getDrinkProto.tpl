%import constants
<html>
<head>
	<title>{{selectedDrink['name']}}</title>
	<script type="text/javascript" src='/static/jquery-2.0.0.min.js'></script>
	<link rel="stylesheet" type="text/css" href="/static/css/bt-style.css">
	<link href='http://fonts.googleapis.com/css?family=Lato:700,900' rel='stylesheet' type='text/css'>


</head>
<body>
	%for ingredient in constants.INGREDIENTLIST:
		%if selectedDrink[ingredient] != 0:
			<li>{{ingredient}} : {{selectedDrink[ingredient]}}</li>
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

