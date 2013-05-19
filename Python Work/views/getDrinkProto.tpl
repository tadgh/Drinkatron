%import constants
<ul>

%for ingredient in selectedDrink.keys():
	%if ingredient in constants.INGREDIENTLIST:
		<li>
			<p>{{ingredient.upper()}} : {{selectedDrink[ingredient]}} </p>
			<input class="slider" id="{{ingredient}}" type="range" min="0" max="100" step="1" value='{{( selectedDrink[ingredient] / selectedDrink['totalSize']) * 100}}' />
		</li>
	%end
%end
</ul
>

