//ESte se llama para tener la posicion
    function encontrarPosicion()
    {
        //alert("encontrarPosicion");
        navigator.geolocation.getCurrentPosition(onSuccess, onError,{ timeout: 20000 });
    }

    //Si hay un error en 20 segundos se llama a este metodo por default
    function onError(error) {
        alert('Revise que el gps este activado y que se encuentre en una zona donde se pueda usar');
    }
    // 
    // Si se obtiene la posicion se llama a este metodo por default
    function onSuccess(position) {
        /*var element = document.getElementById('geolocation');
        element.innerHTML = 'Latitude: '           + position.coords.latitude              + '<br />' +
                            'Longitude: '          + position.coords.longitude             + '<br />' +
                            'Altitude: '           + position.coords.altitude              + '<br />' +
                            'Accuracy: '           + position.coords.accuracy              + '<br />' +
                            'Altitude Accuracy: '  + position.coords.altitudeAccuracy      + '<br />' +
                            'Heading: '            + position.coords.heading               + '<br />' +
                            'Speed: '              + position.coords.speed                 + '<br />' +
                            'Timestamp: '          +                                   position.timestamp          + '<br />';
        //Lo unico que importa es la latitud y la longitud*/
        encontrarPais(position.coords.latitude,position.coords.longitude);

    }
   
   //Aqui se obtiene el pais con la longitud y latitud que devuelve onSuccess
    function encontrarPais(longitud,latitud)
    {   
        //alert("encontrarPais");        
        $.ajax({
            //url: "http://dev.virtualearth.net/REST/v1/Locations/9.95262,-83.853149",
            url: "http://dev.virtualearth.net/REST/v1/Locations/"+longitud+","+latitud,
        dataType: "jsonp",
        data: {
            key: 'AjtUzWJBHlI3Ma_Ke6Qv2fGRXEs0ua5hUQi54ECwfXTiWsitll4AkETZDihjcfeI',
            o: 'json'
        },
        jsonp: "jsonp",
        success: function (data) {
            //var element = document.getElementById('pais');
            //El pais es =   data.resourceSets[0].resources[0].address.countryRegion
            //element.innerHTML = 'Pais: ' + data.resourceSets[0].resources[0].address.countryRegion + '<br />';
            //$('#selectCountries option:eq('+data.resourceSets[0].resources[0].address.countryRegion +')').prop('selected', true);
            alert(data.resourceSets[0].resources[0].address.countryRegion);
            }
        });        
    }