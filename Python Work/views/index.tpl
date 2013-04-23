
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
});


</script>
<body>
<button id="btnGetDrinks">get all drinks</button>
<button id="getDrinkDetails">get drink details</button>
<div id="divDrinkList"></div>
</body>
</html>