
<!DOCTYPE html>
<html>

<p>Click the button to trigger a function.</p>
<script type="text/javascript" src="http://code.jquery.com/jquery-latest.js"></script>

<script type="text/javascript">
$(document).ready(function() {

    $("#btnGetDrinks").click(function()
        {
             $.ajax({
                url: "/getDrinks",
                type: "get",
                success: function(data){
                    //alert(data);
                    $("#divDrinkList").html(data)
                }
            });
        });
    $("a").click(function()
        {
             $.ajax({
                url: $(this).attr("id"),
                type: "get",
                success: function(data){
                    //alert(data);
                    $("#detailView").html(data)
                }
            });
        });
});


</script>
<body>
<div id="list1">
    <ul>
        %for drink in drinkList:
        <li><a href="#" id="/getDrink/{{drink['name']}}">{{drink['name']}}</a></li> <br>
        %end
    </ul>
</div>
<div id="detailView">


</div>
<div id="divDrinkList"></div>
</body>
</html>
<style>
    body
    {
        background-color: #2a2a2a
    }
    #list1 { }
    #list1 ul { list-style:none; text-align:left; border-top:1px solid #eee; border-bottom:1px solid #eee; padding:10px 0; }
    #list1 ul li { display:inline; text-transform:uppercase; padding:0 10px; letter-spacing:10px; }
    #list1 ul li a { text-decoration:none; color:#eee; }
    #list1 ul li a:hover { text-decoration:underline; }
    #list1 { width: 500px; float: left}
    #detailView { width: 500px;float: left}
</style>