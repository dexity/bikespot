
// Google map

// Default values: near Golden Gate Bridge
var curr_lat = 37.795232;
var curr_lng = -122.450742;

var parking_map = null;
var blue_icon = "http://maps.google.com/mapfiles/ms/icons/blue-dot.png";

var loadMap    = function(){
    // Loads map
    var location = new google.maps.LatLng(curr_lat, curr_lng);
    var mapOptions = {
        center: location,
        zoom: 14,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
    };
    var map = new google.maps.Map(document.getElementById("parking-map"), mapOptions);

    var marker	= new google.maps.Marker({
        position:  	new google.maps.LatLng(curr_lat, curr_lng),
        title:      "Current location",
        map:        map
    });

    parking_map = map;
}

var drawStep = function(map, step){
    var decodedPath = google.maps.geometry.encoding.decodePath(step);
    var directionPath = new google.maps.Polyline({
        path: decodedPath,
        geodesic: true,
        strokeColor: '#0000FF',
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
    directionPath.setMap(map);
}

var showInfo = function(map, marker, parking){
    var iw = new google.maps.InfoWindow();
    iw.setContent($.tmpl($("#info-tmpl").template(), parking).html() );
    iw.open(map, marker);
}

var parkingMarker = function(map, parking){
    var latlng = parking.location;
    var marker = new google.maps.Marker({
        position:  	new google.maps.LatLng(latlng[0], latlng[1]),
        title:      parking.location_name,
        icon:       blue_icon,
        map:        map
    });
    // Click marker
    google.maps.event.addListener(marker, 'click', function() {
        showInfo(map, marker, parking);
    });
}

var loadParkings = function(lat, lng){
    // Display parking spots
    var parkings_url = "/parkings?origin=" + lat + "," + lng;
    $.get(parkings_url, function(data){
        for (var i = 0; i<data.data.length; i++){
            parkingMarker(parking_map, data.data[i]);
        }
    })
}

// google.maps.event.addDomListener(window, 'load', loadMap);

// Utils

var directionsUrl = function(lat, lng){
    return "/directions?origin=" + lat + "," + lng;
}

var initMap = function(lat, lng){
    loadMap();
    loadParkings(lat, lng);
}

// Geolocation

var successLocation = function(position){
    var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
    // Set new current location and reload map
    curr_lat = latlng.lat();
    curr_lng = latlng.lng();
    initMap(curr_lat, curr_lng);
}

var errorLocation = function(){
    initMap(curr_lat, curr_lng);
    $("#error").removeClass("hide").html("Current location is set to default");
}

