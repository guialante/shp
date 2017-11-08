$( document ).ready(function() {
    var csrftoken = Cookies.get('csrftoken');
    var validTypes = ["route", "street_address", "intersection"];
    var geocoder = new google.maps.Geocoder;
    
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    
    function updateMarkers(map, refresh){
        var options = {
            select: '\'location\'',
            from: '18rhJFN48wNEtoQ3mHO4ePlbxaH0hRS8TBH48WBxX'
        };
        if (refresh){
            // refresh table base on https://stackoverflow.com/questions/11245680/how-to-reload-google-maps-layer
            options.where = "location not equal to" + (-1 * Math.floor(Math.random() * 10000000)).toString()
        }
        map.loadFromFusionTables({
            query: options
        });
        
        GMaps.geolocate({
            success: function(position){
              map.setCenter(position.coords.latitude, position.coords.longitude);
            },
            error: function(error){
              alert('Geolocation failed: '+error.message);
            },
            not_supported: function(){
              alert("Your browser does not support geolocation");
            }
        });
    }

    var map = new GMaps({
        el: '#map',
        lat: -12.043333,
        lng: -77.028333,
        zoom: 11,
        mapTypeControl: false,
        fullscreenControl: false,
        streetViewControl: false,
        click: function (event) {
            geocoder.geocode({'location': event.latLng}, function(results, status) {
                if (status === 'OK') {
                    var result = results[0];
                    if (result.types.every(elem => validTypes.indexOf(elem) > -1)){
                        var address = result.formatted_address;
                        var lat = result.geometry.location.lat();
                        var lng = result.geometry.location.lng();
                        $.ajax({
                            url: '/save-location/',
                            data:  {address: address, lat:lat, lng:lng},
                            type: 'POST',
                            dataType: 'json',
                            success: function (data, textStatus, jqXHR) {
                                $('#no-result').hide();
                                $('.list-group').append('<li>' + data.address + '</li>');
                                updateMarkers(map, true);
                            },
                            error: function (jqXHR, textStatus, errorThrown) {
                                var data = jqXHR.responseJSON;
                                alert('Point can be created');
                            }
                        });
                    }
                }else{
                    alert('Point can be created')
                }
            });
        }
    });
    
    updateMarkers(map, true);
    
    $('#delete').on('click', function (event) {
        event.preventDefault();
        alert('data is being reset, please wait');
        $('button').blur();
        $.ajax({
            url: '/delete-locations/',
            data:  {delete: true},
            type: 'POST',
            dataType: 'json',
            success: function (data, textStatus, jqXHR) {
                $('.list-group').html('').append('<span id="no-result">There is not addresses</span>');
                updateMarkers(map, true);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                var data = jqXHR.responseJSON;
            }
        });
    });
});








