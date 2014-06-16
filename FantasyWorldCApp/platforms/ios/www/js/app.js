//no se si esto se usa
var myPlayers;
//todos los jugadores en la base
var allPlayers;
//al suave no me acuerdo que era esto
var playerNumber;
//list de jugadores filtrados
var currentList;
//usuario actual
var user;
var userPassword;

//todas las ligas del usuario
var allLeagues;
//liga seleccionada
var currentLeague;
//jugador seleccionado
var currentPlayer;

//titulares del usuario
var playerList=[];
var playerCountryList=[];
var playerPositionList=[];
var playerPriceList=[];

//banca del usuario
var benchList=[];
var benchCountryList=[];
var benchPositionList=[];
var benchPriceList=[];


$(function(){
	$.mobile.defaultPageTransition   = 'none';
	$.mobile.defaultDialogTransition = 'none';
	$.mobile.buttonMarkup.hoverDelay = 0;



	//popup
	$( "#popupDialog" ).on({
    popupbeforeposition: function() {
        var h = $( window ).width();

        $( "#popupDialog" ).css( "width", h-(h/5) );
    }
});

	//pantalla de atract
	// Bind the swiperightHandler callback function to the swipe event on div.box
	  $( "div.swipebox" ).on( "swiperight", swiperightHandler );
	 
	  // Callback function references the event target and adds the 'swiperight' class to it
	  function swiperightHandler( event ){
	    window.location.href="#login"
	  }

	//botones de pantalla de login
	$("#btnRegister").on( "vclick", function()
    {
        window.location.href="#register"
    });
    

    $("#btnLogin").on( "vclick", function()
	{		
		var email= $("#txtEmail").val();
		var	password =$("#txtPassword").val();
		var compressed=email+password;
		$.get( "http://tranquil-earth-6141.herokuapp.com/logIn", { password: compressed } )
			.done(function(data){
				if(data.error==1){
					alert("Login failed");
				}
				else{
					user=data.user;
					userPassword=compressed;
					getStartersList(user.fantasyTeam.startingPlayers,playerList,playerCountryList,playerPositionList,playerPriceList);
					getBenchList(user.fantasyTeam.bench,benchList,benchCountryList,benchPositionList,benchPriceList);

					window.location.href="#mainMenu";	
				}
			});

	});

	//botones de pantall de registro
    $("#btnSubmit").on( "vclick", function()
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
					$.get( "http://tranquil-earth-6141.herokuapp.com/logIn", { password: tempEmail+tempPassword } )
						.done(function(data){
							if(data.error==1){
								alert("Error in the system");
							}
							else{
								user=data.user;
								userPassword=tempEmail+tempPassword;
								getStartersList(user.fantasyTeam.startingPlayers,playerList,playerCountryList,playerPositionList,playerPriceList);
								getBenchList(user.fantasyTeam.bench,benchList,benchCountryList,benchPositionList,benchPriceList);
								alert("Success!. Welcome!");
								window.location.href="#mainMenu";	
							}
						});
					
				}
		  });
		
	});

	//botones del menu

	//my Team
	$("#btnMyTeam").on( "vclick", function()
	{
		window.location.href="#myTeam";
		
	});
	$("barMyTeam").on( "vclick", function()
	{
		window.location.href="#myTeam";
		
	});

	//Leagues
	$('#btnMyLeagues').on( "vclick", function()
	{
		window.location.href="#leagues";
		initialDrawLeagues();
	});

	$('#barLeagues').on( "vclick", function()
	{
		window.location.href="#leagues";
		initialDrawLeagues();
	});

	$('#btnCreateLeague').on("vclick",function(){
		window.location.href="#createLeague";

	});

	$('#btnCreate').on("vclick",function(){
		var leagueName= $("#txtLeagueName").val();
		$.post( "http://tranquil-earth-6141.herokuapp.com/crearLiga", { name: leagueName, email: user.email, password: userPassword } )
			.done(function(data){
				if(data.error==1){
					alert("Creation Failed");
				}
				else{
					alert('Succes! New League!')
					//TODO refrescar ligas
					window.location.href="#leagues";	
				}
			});
	});


	//Transfers
	$("#btnTransfers").on( "vclick", function()
	{
		window.location.href="#transfers";
		initialDrawPlayers();
	});
	
	$("#barTransfers").on( "vclick", function()
	{
		window.location.href="#transfers";
		initialDrawPlayers();
	});


	$("#btnResults").on( "vclick", function()
	{
		window.location.href="#results"
	});

	$("#btnLogOut").on( "vclick", function()
	{
		user=null;
		window.location.href="#login"
	});

	$("#btnLoadMore").on("vclick", function()
	{
		loadPlayers(DrawPlayers,20,currentList);
	});

	$("#btnFilter").on("vclick", function()
	{
		var clone=allPlayers.slice(0);
		var positions=checkBoxes();
		var min=$("#rangeMin").val();
		var max=$("#rangeMax").val();
		var country=$("#selectTeam").val();
		var sortingChoice=sortings();

		clone=filterTeam(clone,country);
		//clone=filterPrice(clone,min,max);
		clone=filterPosition(clone,positions);
		clone=sortPlayers(sortingChoice,clone);
		currentList=clone.slice(0);

		playerNumber=0;
		loadPlayers(DrawPlayers,20,currentList);
		


		window.location.href="#transfers";
		

	});

	$("#btnAddUser").on("vclick",function(){
		var userEmail=$("#txtUsrEmail").val();
		var leagueName=allLeagues[currentLeague].name;
		//alert(userEmail);
		addUserToLeague(leagueName,userEmail);

	});


});


var moveToTransfers=function(){
	window.location.href="#leagues";
	initialDrawLeagues();

}

