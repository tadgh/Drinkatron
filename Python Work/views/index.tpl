%import settings
<!DOCTYPE html>
<html id="theHtml">
<head>
<title>Botender | Beta v.0.01</title>

<link rel="stylesheet" type="text/css" href="../static/css/bt-style.css">
<link href='http://fonts.googleapis.com/css?family=Lato:700,900' rel='stylesheet' type='text/css'>
<link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
<script type="text/javascript" src="http://code.jquery.com/jquery-latest.js"></script>
<script type="text/javascript" src="http://code.jquery.com/ui/1.9.2/jquery-ui.js"></script>

<script type="text/javascript">

$(document).ready(function() {

    window.currentDrink = "";

    $("#upVote").click(function()
    {
        $.ajax({
            url: "/upvote/" + window.currentDrink,
            type: "get"
        });
    });
    $("#downVote").click(function()
    {
        $.ajax({
            url: "/downvote/" + window.currentDrink,
            type: "get"
        });
    });
    //$("li").click(function()
    $("#drinkList").on('click','li', function()
        {
            window.currentDrink = $(this).attr("id");
            $("#nameDiv").html("<p>" + $(this).text() + "</p>");
            console.log(window.currentDrink);
             $.ajax({
                url: "/getDrink/" + $(this).attr("id"),
                type: "get",
                success: function(data){
                    $("#ingDiv").html(data);
                }
            });
        });

    $(".ingBox").click(function()
    {
        console.log("IN THE CHECKBOX CLICKER");
        var selIngDict = {};
        $('input:checked').each(function(index, domEle){
                        var x = $(this).val();
                        var y = $(this).val();
                        console.log("shi")
                        console.log(y)
                        console.log(x)
                        console.log('shit')
                        selIngDict[x] = y;
        });

        $.ajax({
            type: "POST",
            url:  "/sortByIngredient/",
            data: JSON.stringify(
            {
                selectedIngredients: selIngDict
            }),
            contentType: "application/json; charset=utf-8",
            success: function(data){
                var curList = $("#drinkList").contents();
                console.log(curList);
                $("#drinkList").empty()
                $("#drinkList").append(data)
            }
        });
    });


    $("#surpriseBut").click(function()
    {
        $.ajax({
            url: "/dispense/random",
            type: "GET",
            success: function(data){
                alert(data);
            }
        });
    });
    $("#dispBut").click(function()
            {
                var temp = 0;
                var myDict = {};
                $('.slider').each(function(index, domEle){
                    var x = $(this).attr("id");
                    var y = $(this).val();
                    myDict[x] = y;
                });
                $.ajax({
                    type: "POST",
                    url: "/dispenseProto/",
                    data: JSON.stringify(
                    {
                        theDict: myDict,
                        name: $('#nameDiv').html()
                    }),
                    contentType: "application/json; charset=utf-8",
                    success: function(data){
                        alert(data);
                    }
                });
            });
        $("#upBut").click(function()
        {
            var tempDict = {};
            tempDict['ingredient1'] = 'Vodka';
            $.ajax({
                type: "POST",
                url:  "/sortByIngredient/",
                data: JSON.stringify(
                {
                    selectedIngredients: tempDict
                }),
                contentType: "application/json; charset=utf-8",
                success: function(data){
                    var curList = $("#drinkList").contents();
                    console.log(curList);
                    $("#drinkList").empty()
                    $("#drinkList").append(data)

                }
            });
        });
    });
</script>


</head>

<body>

<div id="interface">
<div class="container">

	<div class="ui-left">

        <img class="bt-logo" src="../static/images/bt-logo.png"/>


		<div class="d-preview">

        <ul>
        	<li><img src="../static/images/drink1.png" alt="Blue Moon Martini"></li>
        </ul>

        </div><!-- /end .d-preview -->

        <div class="d-head" id='nameDiv'>

            <p> DRINK NAME GOES HERE</p>

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
        	<button id="dispBut">POUR IT</button>
            <button id="surpriseBut">SURPRISE ME!</button>
        </div>

     </div><!-- /end .ui-left -->



    <div class="ui-right">
        <div class="d-list-container">

            <div id = "drinkList" class="d-list">
                <ul>
                    %for drink in displayed_drinks:
                    <li id="{{drink}}"><p>{{drink.upper()}}</p></li>
                    %end
                </ul>
            </div>



        </div><!-- /end .d-list -->

        <ul class="d-list-nav">
            <button id="upBut" class="btn-up"><img src="../static/images/btn_up.png"/></button>
            <button class="btn-down"><img src="../static/images/btn_down.png"/></button>
            <button class="btn-shuffle"><img src="../static/images/btn_shuffle.png"/></button>
            <button class="btn-alpha"><img src="../static/images/btn_alpha.png"/></button>
        </ul>


	</div><!-- /end .ui-right -->
    <form>
        %for ingredient in settings.INGREDIENTLIST:
            <input type="checkbox" class="ingBox" value="{{ingredient}}">{{ingredient}}<br>
        %end
    </form>
<script>
    var dlimit = $(".d-list").height() - 697.5;

    console.log(dlimit);
    var listheight = $(".d-list").height();
    console.log(listheight);
    $(function () {
        $(".d-list").draggable({ axis: "y", scroll: true, containment:[0,-dlimit,0,0]});
     });

</script>

</div><!-- /end .container -->


</div><!-- /end #interface -->

</body>

</html>