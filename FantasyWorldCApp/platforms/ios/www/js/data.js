////////////////////// TRANSFERS ///////////////////

var getStartersList=function(startersList, resultPlayers,resultCountries, resultPositions, resultPrice){
	resultPlayers.length=0;
	resultCountries.length=0;
	resultPositions.length=0;
	resultPrice.length=0;
	for(var positions=0;positions<startersList.length;positions++){
		for(var currPlayer=0;currPlayer<startersList[positions].length;currPlayer++){

			resultPlayers.push(startersList[positions][currPlayer].player.name);
			resultCountries.push(startersList[positions][currPlayer].player.team);
			resultPositions.push(startersList[positions][currPlayer].player.position);
			resultPrice.push(startersList[positions][currPlayer].player.price);
		}
	}
}

var getBenchList=function(benchList,resultPlayers,resultCountries,resultPositions, resultPrice){
	resultPlayers.length=0;
	resultCountries.length=0;
	resultPositions.length=0;
	resultPrice.length=0;
		for(var currPlayer=0;currPlayer<benchList.length;currPlayer++){
			resultPlayers.push(benchList[currPlayer].player.name);
			resultCountries.push(benchList[currPlayer].player.team);
			resultPositions.push(benchList[currPlayer].player.position);
			resultPrice.push(benchList[currPlayer].player.price);
		}

}

var transferPlayer=function(){
	var sendNames;
	var sendTeams;
	var replaceName=$("#selectPlayers option:selected").text();
	var replace=playerList.indexOf(replaceName);
		
		if(replace==-1){ //va a reemplazar a un banca
			replace=benchList.indexOf(replaceName);
			
			if((user.fantasyTeam.transfers+benchPriceList[replace])>=currentPlayer.price){

				dataTransfers(benchList[replace],benchCountryList[replace],currentPlayer.name,currentPlayer.team);
				//alert('success, player transfered');
				//arrangeArray(benchList,benchCountryList,sendNames,sendTeams);
				//TODO SUBIR A LA BASE

			}
			else{
				alert('You do not have enough funds');
			}

		}
		else{ //va a reemplazar un titular
			if((user.fantasyTeam.transfers+playerPriceList[replace])>=currentPlayer.price){
				dataTransfers(playerList[replace],playerCountryList[replace],currentPlayer.name,currentPlayer.team);
			}
			else{
				alert('You do not have enough funds');
			}
		}
	

}

var dataTransfers=function(player1,team1,player2,team2){
	$.post( "http://tranquil-earth-6141.herokuapp.com/transferencia", 
	{ player1: player1, team1: team1, player2: player2,team2: team2, password: userPassword } )
	.done(function(data){
		if(data.error==1){
			alert("Operation Failed");
		}
		else{
			alert('Player Transfered');
			$.get( "http://tranquil-earth-6141.herokuapp.com/logIn", { password: userPassword } )
			.done(function(data){
				if(data.error==1){
					alert("Error");
				}
				else{
					user=data.user;
					getStartersList(user.fantasyTeam.startingPlayers,playerList,playerCountryList,playerPositionList,playerPriceList);
					getBenchList(user.fantasyTeam.bench,benchList,benchCountryList,benchPositionList,benchPriceList);
					window.location.href="#transfers";
				}
			});
			
		}
	});
}
/*
var buyPlayer=function(){
	if(user.fantasyTeam.transfers<currentPlayer.price){
		alert("You do not have enough funds");
	}
	else{
		if(checkPositions(currentPlayer.position)){

		}
		else{
			alert("The amount of players allowed in this position is full")
		}
	}
}
*/

var displayPlayersToTransfer=function(Position,direction){
	for(var i=0;i<playerList.length;i++){
		if(playerPositionList[i]===Position){
			if(!(playerList[i]===currentPlayer.name)){
				direction.append(new Option(playerList[i], playerList[i]));
			}
		}
	}
	for(var j=0;j<benchList.length;j++){
		if(benchPositionList[j]===Position){
			if(!(benchList[j]===currentPlayer.name)){
				direction.append(new Option(benchList[j],benchList[j]));
			}
		}
	}
}

////////////////////// DISPLAY Y SORTING DE TRANSFERS /////////////////////////////

var downloadPlayers = function(callback,last){

	$.get( "http://tranquil-earth-6141.herokuapp.com/players")
		.done(function(data){
			if(data.error==1){
				alert("Load failed");
			}
			else{
					allPlayers=data.player;
					currentList=allPlayers.slice(0);
					var clone=allPlayers.slice(0);
					callback(clone.splice(0,last));	
					playerNumber=last;
					//$("#btnLoadMore").removeAttr("disabled");

				}
			});
	};

var loadPlayers=function(callback,increment,playerList){
	
	var clone=playerList.slice(0);
	resetDraw();
	var newLast=playerNumber+increment;
	callback(clone.splice(0,newLast));
	playerNumber+=increment;

}

var individual=function(index){
	window.location.href="#playerData";
	currentPlayer=currentList[index];
	drawIndividualPlayer(currentList[index]);

}

var drawIndividualPlayer=function(player){

	$("#dataDisplay").empty();
	var search='data-filtertext="'+player.name+'"';        
        var root=$('<div class="showPlayer"></div>');

        var money=$('<h3></h3>');
        money.text("Available Funds :"+user.fantasyTeam.transfers);
        root.append(money);

        var picture=$('<img class="displayImage">');
    	var adress='img/shirts/'+player.team+'.png';
        //alert(adress);
        picture.attr('src',adress);
        picture.attr('margin-top',"20px");
        //picture.attr('height',"25%");
        root.append(picture);

        var name=$('<h1></h1>');
        name.text(player.name);
        root.append(name);

        var team=$('<h2></h2>');
        team.text(player.team);
        root.append(team);

        var pos=$('<h2></h2>');
        pos.text(player.position);
        root.append(pos); 

        var price=$('<h2></h2>');
        price.text("Price :"+player.price);
        root.append(price);

        var tpoints=$('<h2></h2>');
        tpoints.text("Points :"+player.totalPoints);
        root.append(tpoints);   

        var select=$('<div class="ui-field-contain" width="75%"></div>');
        var choices=$('<select name="select-native-1" id="selectPlayers" ></select>');
        displayPlayersToTransfer(player.position,choices);

        var btnTransfer=$('<button onClick="transferPlayer()" class="ui-btn">Transfer</button>');
        var btnBuy=$('<button onClick="buyPlayer()" class="ui-btn">Buy</button>');

        select.append(choices);
        root.append(select);
        /*if(playerList.length+benchList.length<15){
        	root.append(btnBuy);
        }*/
        root.append(btnTransfer);


        $("#dataDisplay").append(root);
}


var DrawPlayers=function(playerList){
	for(var i=0;i<playerList.length;i++){
        var player=playerList[i];
                
        var search='data-filtertext="'+player.name+'"';        
        var container=$('<li '+search+' class="ui-li-has-thumb"></li>')
        var root=$('<a class="ui-btn ui-btn-icon-right ui-icon-carat-r" onClick="individual('+i+')" ></a>');
        //root.append('click',individual(i));


        var picture=$('<img>');
    	var adress='img/shirts/'+player.team+'.png';
        //alert(adress);
        picture.attr('src',adress);
        picture.attr('margin-top',"20px");
        //picture.attr('height',"25%");
        root.append(picture);

        var name=$('<h2></h2>');
        name.text(player.name);
        root.append(name);

        var team=$('<p></p>');
        team.text(player.team+" | "+ player.position+" | "+"Price :"+player.price+ "  |  "+"Points :"+player.totalPoints);
        root.append(team); 


        container.append(root);
        $("#display").append(container);
    }

}

var resetDraw=function(){
	$("#display").empty();
}

var initialDrawPlayers= function(){
        downloadPlayers(DrawPlayers,46);
    }

var filterTeam=function(itemList,teamName){
	var filteringResults=[];
	if(teamName==="all"){
		filteringResults=itemList;
	}
	else{
		for(var i=0;i<itemList.length;i++){
			if(itemList[i].team===teamName){
				filteringResults.push(itemList[i]);
			}
		}
	}
	return filteringResults;

}

var filterPosition=function(itemList,positionList){
	var filteringResults=[];
	for(var i=0;i<itemList.length;i++){
		for(var pos=0;pos<positionList.length;pos++){
			if(itemList[i].position===positionList[pos]){
				filteringResults.push(itemList[i]);
			}
		}
	}
	return filteringResults;

}
var filterPrice=function(itemList,priceLow,priceHigh){
	var filteringResults=[];
	for(var i=0;i<itemList.length;i++){
		if((itemList[i].price>=priceLow) && (itemList[i].price<=priceHigh)){
			filteringResults.push(itemList[i]);
		}
	}
	return filteringResults;
}

var sortPlayers=function(sortingFunction, playerList){
	playerList.sort(sortingFunction);
	return playerList;
}

var sortings=function(){
	if($("#checkSortPrice").prop("checked")){
		return (function(a,b) { return parseFloat(b.price) - parseFloat(a.price) } );
	};
	if($("#checkSortPoints").prop("checked")){
		return (function(a,b) { return parseFloat(b.totalPoints) - parseFloat(a.totalPoints) } );
	};
}

var checkBoxes=function(){
	var result=[];

	if($('#checkGK').prop("checked")){
		result.push("Goalkeeper");
	};
	if($('#checkDF').prop("checked")){
		result.push("Defender");
	};
	if($('#checkMF').prop("checked")){
		result.push("Midfielder");
	};
	if($('#checkST').prop("checked")){
		result.push("Forward");
	};

	return result;
}

///////////////////////// LEAGUES ////////////////////////

var resetLeagues=function(){
	$("#leaguesDisplay").empty();
}


var initialDrawLeagues=function(){
	resetLeagues();
	loadLeagues(displayLeagues);
}

var loadLeagues=function(callback){
	$.get( "http://tranquil-earth-6141.herokuapp.com/obtenerLigasUsuario", { email: user.email, password: userPassword })
		.done(function(data){
			if(data.error==1){
				alert("Load failed");
			}
			else{
					allLeagues=data.liga;
					callback(data.liga);	
				}
			});

}

var displayLeagues=function(leagues){
	for(var i=0;i<leagues.length;i++){
        var league=leagues[i];
                    
        var container=$('<li class="ui-li-has-thumb"></li>')
        var root=$('<a class="ui-btn ui-btn-icon-right ui-icon-carat-r" onClick="individualLeague('+i+')" ></a>');
        //root.append('click',individual(i));

        var picture=$('<img>');
    	var adress='img/iconStadium.png';
        //alert(adress);
        picture.attr('src',adress);
        picture.attr('margin-top',"20px");
        //picture.attr('height',"25%");
        root.append(picture);


        var name=$('<h2></h2>');
        name.text(league.name);
        root.append(name);

        var owner=$('<p></p>');
        var ownerName;
        if(league.owner===user.email){
        	ownerName="You";
        }
        else{
        	ownerName=league.owner;
        }
        owner.text("Owner : "+ownerName+" | "+"Players :"+league.users.length);
        root.append(owner); 


        container.append(root);
        $("#leaguesDisplay").append(container);
    }


}


//////// INDIVIDUAL LEAGUE ///////////

var resetTable=function(){
	$("#UserTable").empty();
}

var individualLeague=function(index){
	resetTable();
	var lname=allLeagues[index].name;
	currentLeague=index;
	loadIndividualLeague(lname,drawIndividualLeague);
	window.location.href="#informationLeague"
}

var loadIndividualLeague=function(Lname,callback){
	$.get( "http://tranquil-earth-6141.herokuapp.com//obtenerInfoLiga", { name: Lname, password: userPassword })
		.done(function(data){
			if(data.error==1){
				alert("Error");
			}
			else{
					var users=data.user;
					users.sort(function(a,b) { return parseFloat(b.totalPoints) - parseFloat(a.totalPoints) });
					callback(users);	
				}
			});

}

var drawIndividualLeague=function(leagueTable){
	for(var i=0;i<leagueTable.length;i++){
        var user=leagueTable[i];
                    
        var container=$('<li class="ui-li-has-thumb"></li>')
        var root=$('<a class="ui-btn ui-btn-icon-right ui-icon-carat-r" ></a>');
        //class="ui-btn ui-btn-icon-right ui-icon-carat-r"

        var picture=$('<img class="displayImage">');
    	var adress='img/shirts/'+user.country+'.png';
        //alert(adress);
        picture.attr('src',adress);
        picture.attr('margin-top',"20px");
        //picture.attr('height',"25%");
        root.append(picture);

        var email=$('<h2></h2>');
        email.text(user.email);
        root.append(email);

        var points=$('<p></p>');
        points.text("Points : "+user.totalPoints);
        root.append(points); 


        container.append(root);
        $("#UserTable").append(container);
    }


}

var addUserToLeague=function(leagueName,email){
		alert(leagueName+email+userPassword);
		$.post( "http://tranquil-earth-6141.herokuapp.com/agregarUsuarioLiga", { name: leagueName, newUser: email, password: userPassword } )
			.done(function(data){
				if(data.error==1){
					alert("Operation Failed");
				}
				else{
					alert('Succes! You have added a member to the league!');
					resetTable();
					individualLeague(currentLeague);
					//TODO refrescar ligas
				}
			});

}




