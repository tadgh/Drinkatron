<html>
<head>
	<title>Settings</title>
	<script type="text/javascript" src="http://code.jquery.com/jquery-latest.js"></script>
	<script type="text/javascript" src="http://code.jquery.com/ui/1.9.2/jquery-ui.js"></script>

<script>
	$(document).ready(function() {
		// $("#save").click(function()
  //       {
  //            $.ajax({
  //               url: "/save/"
  //               type: "get",
  //               success: function(data){
  //               	$("#save").text(data);
  //               }
  //           });
  //       });
};
</script>


</head>
<body>
	<form action='/save/' method='POST'>
		<p>Cup Type:
			<select name="selectedCup">
				%for cupType in cupInfo.keys():
					%if cupType == userSettings['current cup']:
						<option value='{{cupType}}' selected="selected">{{cupType}}</option>
					%else:
						<option value='{{cupType}}'>{{cupType}}</option>
					%end
				%end
			</select>
		</p>
		<p>Cup Size: {{cupInfo[userSettings['current cup']]}} {{userSettings['unit of measurement']}}</p>
		<input type="submit">Save Changes</input>

	</form>
</body>
</html>