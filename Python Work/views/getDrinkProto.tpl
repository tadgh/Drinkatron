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
	<ul>
	%for ingredient in constants.INGREDIENTLIST:
		%if selectedDrink[ingredient] != 0:
			<li>
				<p>{{ingredient.upper()}} : {{selectedDrink[ingredient]}} </p>
				<input class="slider" id="{{ingredient}}" type="range" min="0" max="100" step="1" value='{{( selectedDrink[ingredient] / totalSize) * 100}}' />
			</li>
		%end
	%end
	</ul>
</body>
</html>

