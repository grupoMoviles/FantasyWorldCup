
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
				alert("data"+ data.length);
			});
		/*
		var email= $("#txtEmail").val();
		var	password =$("#txtPassword").val();
		var send={"email":email, "password": password};
		var jdata = JSON.stringify(send);

		jQuery.ajax({
	        type: "GET",
	        url: "http://tranquil-earth-6141.herokuapp.com/logIn",
	        contentType: "application/json; charset=utf-8",
	        data: jdata,
	        dataType: 'json',
	        success: function (data, status, jqXHR) {
				alert(data.length);
				window.location.href="#mainMenu";

	        },

	        error: function (jqXHR, status) {
	            alert('connection failed');
	        }
		});*/

	});

	//botones de pantall de registro
    $("#btnSubmit").click( function()
	{
		var tempEmail= $("#txtFormEmail").val();
		var	tempPassword =$("#txtFormPassword").val();
		var tempCountry=$("#selectCountries option:selected").text();
		var send={"email":tempEmail, "password": tempPassword, "country":tempCountry};
		var jdata = JSON.stringify(send);

		jQuery.ajax({
	        type: "POST",
	        url: "http://tranquil-earth-6141.herokuapp.com/registerUser",
	        data: jdata,
	        contentType: "application/json",
	        dataType: "json",
	        success: function (data, status, jqXHR) {
				window.location.href="#mainMenu";
	        },

	        error: function (jqXHR, status) {
	            alert('connection failed');
	        }
		});
		
	});

	//botones del menu

	$("#btnMyTeam").click( function()
	{
		window.location.href="#myTeam";
		drawPlayers();
	});
	$("#btnTransfers").click( function()
	{
		window.location.href="#transfers"
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
	jQuery.ajax({
        type: "GET",
	        url: "http://tranquil-earth-6141.herokuapp.com/players",
	        contentType: "application/json; charset=utf-8",
	        dataType: "json",
	        success: function (data, status, jqXHR) {
	           	alert(data.length);
				callback(data);

	        },

	        error: function (jqXHR, status) {
	            alert('connection failed');
	        }
		});
	};

var drawPlayers= function(){
        loadPlayers(function(playerList){

            var container=$("<div width:100%></div>");
            for(var i=0;i<playerList.length;i++){
                var player=playerList[i];
                
                var root=$('<div width:100%></div>');
                /*
                var picture=$('<img/>');
                picture.attr('src',player.get("image").url());
                picture.attr('width',"100%");
                root.append(picture);*/

                var Name=$('<center></center>');
                var name=$('<h2></h2>');
                name.text(player.get("name"));
                alert(player.get("name"));
                Name.append(name);
                root.append(Name);

                var Position=$('<center></center>');
                var position=$('<h3></h3>');
                position.text(player.get("position"));
                Position.append(position);
                root.append(Position);

                container.append(root);
            }

            $("#display").append(container);


        });

        
    }


