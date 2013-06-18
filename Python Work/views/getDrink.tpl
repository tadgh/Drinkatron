%import settings
<ul>

%for ingredient in selected_drink.keys():
	%if ingredient in settings.INGREDIENTLIST:
		<li>
			<p>{{ingredient.upper()}} : {{selected_drink[ingredient]}} </p>
			<input class="slider" id="{{ingredient}}" type="range" min="0" max="100" step="1" value='{{( selected_drink[ingredient] / selected_drink['totalSize']) * 100}}' />
		</li>
	%end
%end
</ul
>

