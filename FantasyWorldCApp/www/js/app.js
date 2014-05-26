var myPlayers;


$(function(){

	//pantalla de atract
	// Bind the swiperightHandler callback function to the swipe event on div.box
	  $( "div.swipebox" ).on( "swiperight", swiperightHandler );
	 
	  // Callback function references the event target and adds the 'swiperight' class to it
	  function swiperightHandler( event ){
	    window.location.href="#login"
	  }

	//botones de pantalla de login
	$("#btnRegister").click( function()
    {
        window.location.href="#register"
    });
    

    $("#btnLogin").click( function()
	{
		var email= $("#txtEmail").val();
		var	password =$("#txtPassword").val();
		$.get( "http://tranquil-earth-6141.herokuapp.com/logIn", { email: email, password: password } )
			.done(function(data){
				if(data.error==1){
					alert("Login failed");
				}
				else{
					window.location.href="#mainMenu";	
				}
			});

	});

	//botones de pantall de registro
    $("#btnSubmit").click( function()
	{
		var tempEmail= $("#txtFormEmail").val();
		var	tempPassword =$("#txtFormPassword").val();
		var tempCountry=$("#selectCountries option:selected").text();
		var send={"email":tempEmail, "password": tempPassword, "country":tempCountry};

		$.post( "http://tranquil-earth-6141.herokuapp.com/registerUser", { email: tempEmail, password: tempPassword, country: tempCountry })
		  .done(function( data ) {
		    if(data.error==1){
					alert("Registration failed");
				}
				else{
					alert("Success!. Welcome!");
					window.location.href="#mainMenu";	
				}
		  });
		
	});

	//botones del menu

	$("#btnMyTeam").click( function()
	{
		window.location.href="#myTeam";
		
	});
	$("barMyTeam").click( function()
	{
		window.location.href="#myTeam";
		
	});

	$("#btnTransfers").click( function()
	{
		window.location.href="#transfers"
		drawPlayers("#display");
	});
	$("#barTransfers").click( function()
	{
		window.location.href="#transfers"
		drawPlayers("#display");
	});

	$("#btnResults").click( function()
	{
		window.location.href="#results"
	});
	$("#btnLeagues").click( function()
	{
		window.location.href="#leagues"
	});
	$("#btnLogOut").click( function()
	{
		window.location.href="#login"
	});

});

var loadPlayers = function(callback){

	$.get( "http://tranquil-earth-6141.herokuapp.com/players")
		.done(function(data){
			if(data.error==1){
				alert("Login failed");
			}
			else{
					callback(data.player);	
				}
			});

	};

var drawPlayers= function(location){
        loadPlayers(function(playerList){
            var container=$("<div width:100%></div>");
            for(var i=0;i<playerList.length;i++){
                var player=playerList[i];
                
                var root=$('<div width:100% class="playerView"></div>');
                /*
                var picture=$('<img/>');
                picture.attr('src',player.get("image").url());
                picture.attr('width',"100%");
                root.append(picture);*/

                var name=$('<h2></h2>');
                name.text(player.name);
                root.append(name);

                var team=$('<h3></h3>');
                team.text("Team: "+player.team);
                root.append(team);

                var position=$('<h3></h3>');
                position.text("Position: "+player.position);
                root.append(position);

                var price=$('<h3></h3>');
                price.text("Price :"+player.price);
                root.append(price);

                root.append('<input id="btn" type="button" data-icon="plus" value="Buy">')

                container.append(root);
            }

            $(location).append(container);


        });

        
    }


