<!DOCTYPE html>
<html>
<head>
<title>Botender | Beta v.0.01</title>

<link rel="stylesheet" type="text/css" href="/static/css/bt-style.css">
<link href='http://fonts.googleapis.com/css?family=Lato:700,900' rel='stylesheet' type='text/css'>

<meta name="author" content="Ryan Novak" />
<meta charset="UTF-8" />

<script type="text/javascript" src="http://code.jquery.com/jquery-latest.js"></script>
<script type="text/javascript">
$(document).ready(function() {
    $("li").click(function()
        {
             $.ajax({
                url: $(this).attr("id"),
                type: "get",
                success: function(data){
                    $("#ingDiv").html(data);
                }
            });
        });

    $("li").click(function()
        {
            $("#nameDiv").html("<p>" + $(this).text() + "</p>")
        });
    });
</script>

</head>

<body>

<div id="interface">
<div class="container">

	<div class="ui-left">

        <img class="bt-logo" src="/static/images/bt-logo.png"/>


		<div class="d-preview">

        <ul>

        	<li><img src="/static/images/drink1.png" alt="Blue Moon Martini"></li>

        </ul>

        </div><!-- /end .d-preview -->

        <div class="d-head" id='nameDiv'>

            <p> DRINK NAME GOES HERE </p>

        </div><!-- /end .d-head -->

        <div class="d-control" id="ingDiv">

            <ul>
                <li><p>ING. ONE</p></li>
                <li><p>ING. TWO</p></li>
                <li><p>ING. THREE</p></li>
                <li><p>ING. FOUR</p></li>
                <li><p>ING. FIVE</p></li>
            </ul>


        </div><!-- /end .d-control -->

        <div class="d-selection">
        	<button onclick="Javascript: alert('Pouring meow')">POUR IT</button>
            <button onclick="Javascript: alert ('I too like to live dangerously')">SURPRISE ME!</button>
        </div>

     </div><!-- /end .ui-left -->



    <div class="ui-right">
        <div class="d-list">

            <ul>
                %for drink in drinkList:
                <li id="/getDrink/{{drink['name']}}"><p>{{drink['name']}}</p></li>
                %end
            </ul>



        </div><!-- /end .d-list -->

        <ul class="d-list-nav">
            <li>1</li>
            <li>2</li>
            <li>3</li>
            <li>4</li>
        </ul>
	</div><!-- /end .ui-right -->

</div><!-- /end .container -->
</div><!-- /end #interface -->

</body>

</html>