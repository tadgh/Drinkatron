<!DOCTYPE html>
<html>
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
    $("li").click(function()
        {
            window.currentDrink = $(this).attr("id");
            console.log(window.currentDrink);
             $.ajax({
                url: "/getDrink/" + $(this).attr("id"),
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

            <div class="d-list">
                <ul>
                    %for drink in drinkList:
                    <li id="{{drink['name']}}"><p>{{drink['name'].upper()}}</p></li>
                    %end
                </ul>
            </div>



        </div><!-- /end .d-list -->

        <ul class="d-list-nav">
            <button class="btn-up"><img src="../static/images/btn_up.png"/></button>
            <button class="btn-down"><img src="../static/images/btn_down.png"/></button>
            <button class="btn-shuffle"><img src="../static/images/btn_shuffle.png"/></button>
            <button class="btn-alpha"><img src="../static/images/btn_alpha.png"/></button>
        </ul>
	</div><!-- /end .ui-right -->

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