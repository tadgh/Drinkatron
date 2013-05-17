<ul>
    %for drink in drinkList:
    	<li id="{{drink['name']}}"><p>{{drink['name'].upper()}}</p></li>
    %end
</ul>
