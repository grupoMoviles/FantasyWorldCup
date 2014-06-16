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

//vars de my team
var dragging = false;
var playerOut = "";
var playerIn = "";
var globalSquad = [];
var globalBench = [];


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

	$("#btnFormation").on("vclick",function()
	{
		var newFormation = $("#selectFormation").val();
		createNewFormation(newFormation);

	});


});


var moveToTransfers=function(){

	window.location.href="#transfers";
	initialDrawPlayers();

}

var moveToLeagues=function(){
	window.location.href="#leagues";
	initialDrawLeagues();

}

var moveToMyTeam=function(){
	window.location.href="#myTeam";
	downloadMyTeam();
}

// BRUNO FUNCIONES ======================================================================


function allowDrop(ev) 
{
	ev.preventDefault();
}

function drag(ev) 
{            
	ev.dataTransfer.setData("Text", ev.target.id);
}

function drop(ev,id) {
	ev.preventDefault();
    var id1 = ev.dataTransfer.getData("Text");
    //ev.target.appendChild(document.getElementById(data));
    var id2 = ev.target.id;

    doChange(id1,id2);

}



function doChange(id1,id2)
{
	//verificar posiciones
	var number1 = 0;
	if(id1.length > 2)
		number1 = 10;
	else
		number1 = parseInt(id1[1]);
    var benchOrSquad1 = 0;
    if(id1[0]=='e' || id1[0]=='b')
    {
    	benchOrSquad1 = 1;
    }


    var number2 = 0;
	if(id2.length > 2)
		number2 = 10;
	else
		number2 = parseInt(id2[1]);
    var benchOrSquad2 = 0;
    if(id2[0]=='e' || id2[0]=='b')
    {
    	benchOrSquad2 = 1;
    }

    var player1 = 0;
    if(benchOrSquad1 == 0)
    {
    	var cont1 = 0;
    	// SQUAD
    	for(var line = 0 ; line < globalSquad.length ; line++)
    	{
    		for(var p = 0 ; p < globalSquad[line].length ; p++)
    		{
    			if(cont1 == number1)
    			{
    				player1 = globalSquad[line][p].player;
    			}
    			cont1++;
    		}
    	}
    }
    else
    {
    	// BENCH
    	player1 = globalBench[number1].player;
    }


    var player2 = 0;
    if(benchOrSquad2 == 0)
    {
    	var cont1 = 0;
    	// SQUAD
    	for(var line = 0 ; line < globalSquad.length ; line++)
    	{
    		for(var p = 0 ; p < globalSquad[line].length ; p++)
    		{
    			if(cont1 == number2)
    			{
    				player2 = globalSquad[line][p].player;
    			}
    			cont1++;
    		}
    	}
    }
    else
    {
    	// BENCH
    	player2 = globalBench[number2].player;
    }


    if(player1.position == player2.position)
    {
    	for(var line = 0 ; line < globalSquad.length ; line++)
    	{
    		for(var p = 0 ; p < globalSquad[line].length ; p++)
    		{
    			if(player1 == globalSquad[line][p].player)
    			{
    				globalSquad[line][p].player = player2;
    			}
    			else
    			{
    				if(player2 == globalSquad[line][p].player)
	    			{
	    				globalSquad[line][p].player = player1;
	    			}
	    		}
    		}
    	}	
    	for(var sub = 0 ; sub < globalBench.length ; sub++)
    	{
    		if(globalBench[sub].player == player1)
    		{
    			globalBench[sub].player = player2;
    		}
    		else
    		{
    			if(globalBench[sub].player == player2)
	    		{
	    			globalBench[sub].player = player1;
	    		}
	    	}
    	}


    	var team = [];
		team.push(globalSquad);
		team.push(globalBench);
		submitFormation(team);
    }
    else
    {
    	alert("The players of the substitution have to play the same position.");
    }


    

}





var barMyTeamAction = function()
{
	window.location.href="#myTeam";
	downloadMyTeam();
}


var createNewFormation = function(newFormation)
{

	$.get( "http://tranquil-earth-6141.herokuapp.com/logIn", { password: userPassword } )
		.done(function(data){
			if(data.error==1){
				alert("Load failed");
			}
			else
			{
					var squad = data.user.fantasyTeam.startingPlayers;
					var bench = data.user.fantasyTeam.bench;
					var positions = ["Goalkeeper","Defender","Midfielder","Forward"];
					var subs = [];

					for(var i = 1 ; i < squad.length ; i++)
					{
						var line = squad[i];
						var players = 0 ;
						subs = [];

						if(parseInt(newFormation[i-1]) < line.length )
						{
							var contador  = 0;
							for(var aux = parseInt(newFormation[i-1]) ;  aux < line.length ; aux++)
							{
								var playerOut = line[aux];
								bench.push(playerOut);
								contador ++;								
							}			

							while(contador!=0)
							{
								squad[i].splice( parseInt(newFormation[i-1]) ,1);
								contador--;
							}


							
						}
						else
						{
							var cont = parseInt(newFormation[i-1]) -  line.length  ;
							
							for(var sub = 0 ; sub < bench.length ; sub++)
							{
								if(bench[sub].player.position == positions[i] && cont!=0)
								{
									subs.push(sub);
									squad[i].push(bench[sub]);
									cont--;
								}
							}				

							for(var last = subs.length - 1  ; last > -1 ; last--)
							{
								bench.splice(subs[last],1);
							}			
							
						}

					}


					var team = [];
					team.push(squad);
					team.push(bench);
					submitFormation(team);

			}
		});
};



var submitFormation = function(team)
{
	var bench = team[1];
	var squad = team[0];
	var userPassword = "oleole";

	var names = "[";
	var positions = "[";

	for(var sub = 0 ; sub < bench.length ; sub++)
	{
		if(sub!=0)
		{
			names += ',';
			positions += ',';
		}
		names += bench[sub].player.name ;
		positions += bench[sub].player.team ;
	}

	names += ']';
	positions += ']';

	var namesBench = names;
	var teamsBench = positions;


	names = "[";
	positions = "[";



	for(var line = 0 ; line < squad.length ; line++)
	{

		if(line!= 0)
		{
			names += ',';
		}

		names += "[";

		
		for(var player = 0 ; player < squad[line].length ; player++)
		{
			if(player!=0)
			{
				names += ',';
			}

			if(player!=0 || line!=0)
			{

				positions += ',';
			}

			names += squad[line][player].player.name ;
			positions += squad[line][player].player.team ;
		}

		names += "]";
	}

	names += ']';
	positions += ']';


	$.post( "http://tranquil-earth-6141.herokuapp.com/establecerEquipo", { startingTeams: positions, startingPlayers: names, benchPlayers: namesBench, benchTeams:teamsBench, password: userPassword } )
			.done(function(data){
				if(data.error==1){	
					alert("Operation Failed");
				}
				else{
					window.location.href="#myTeam";
					downloadMyTeam();
				}
			});
}


var removePlayers = function()
{

	var player = "player";

	for(var id = 0 ; id < 11 ; id++)
	{
		var aux = player + id;
		$("#"+aux).remove();
	}

	player += "bench";

	for(var id = 0 ; id < 4 ; id++)
	{
		var aux = player + id;
		$("#"+aux).remove();
	}

}


var downloadMyTeam = function()
{

	$.get( "http://tranquil-earth-6141.herokuapp.com/logIn", { password: userPassword } )
		.done(function(data)
		{

			if(data.error==1)
			{
				alert("LOAD FAILED");
			}
			else
			{

				removePlayers();

				var squad = data.user.fantasyTeam.startingPlayers;
				globalSquad = squad;
				var idPlayer = 0;
				var positions = ["#GK","#DF","#MF","#FW"];

				var formation = [];
				for(var i = 1 ; i < squad.length ; i++)
				{
					formation.push(squad[i].length);
				}
				var infoPlayer = squad[0][0].player;
				var player=$('<td ALIGN=CENTER  id="player0" ><div ondrop="drop(event,this.id)" ondragover="allowDrop(event)" class="playerSpace"><img id="p0" draggable="true" ondragstart="drag(event)" class="playerShirt" src="img/shirts/' + infoPlayer.team + '.png"><div id="d0" class="playerName">' + infoPlayer.name + '</div></div></td>');
				$(positions[0]).append(player);
				idPlayer++;

				for(var i = 0 ; formation.length > i ; i++)
				{
					for(var j = 0 ; formation[i] > j ; j++)
					{
						var infoPlayer = squad[i+1][j].player;
						var player=$('<td ALIGN=CENTER id="player' + idPlayer +'"><div ondrop="drop(event,this.id)" ondragover="allowDrop(event)" class="playerSpace"><img id="p' + idPlayer + '"  draggable="true" ondragstart="drag(event)" class="playerShirt" src="img/shirts/' + infoPlayer.team + '.png"><div id="d'+idPlayer+'" class="playerName">' + infoPlayer.name + '</div></div></td>');
						$(positions[i+1]).append(player);


						idPlayer++;
					}
				}


				var substitutions = data.user.fantasyTeam.bench;
				globalBench = substitutions;
				for(var k = 0 ; k < substitutions.length ; k++)
				{
					var infoPlayer = substitutions[k].player;
					var player=$('<td ALIGN=CENTER  id="playerbench' +  k +'"><div ondrop="drop(event,this.id)" ondragover="allowDrop(event)" class="playerSpace"><img id="b' + k + '" draggable="true" ondragstart="drag(event)" class="playerShirt" src="img/shirts/' + infoPlayer.team + '.png"><div id="e'+ k +'" class="playerName">' + infoPlayer.name + '</div></div></td>');
					$("#bench").append(player);
				}



				var count = 0;
				for(var i = 0 ; i < positions.length ; i++)
				{

					for(var j = 0 ; j < squad[i].length ; j++ )
					{
						$(positions[i]).on("click","#player"+count,function()
						{
							if(dragging)
							{
								// alert(playerOut + " / " + this.id);
								dragging = false;
							}
							else
							{
								dragging = true;
								playerOut = this.id;
							}
							
						});
						

						count++;
					}
					
				}
				



			}
				

		});




};


// ====================================================================================================



