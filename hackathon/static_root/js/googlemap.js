$('.field').hide();

var markers;
var locations1= new Array;
function getLocation(){
if(navigator.geolocation){
navigator.geolocation.getCurrentPosition(locationSuccess, locationError, geo_options);
}else{
console.log("지오 로케이션 없음")
}
};
// getLocation
var latitude, longitude;
function locationSuccess(p){
latitude = p.coords.latitude,
longitude = p.coords.longitude;
    initMap();

}
// locationSuccess
function locationError(error){
var errorTypes = {
0 : "무슨 에러냥~",
1 : "허용 안눌렀음",
2 : "위치가 안잡힘",
3 : "응답시간 지남"
};
var errorMsg = errorTypes[error.code];
}
// locationError

var geo_options = {
enableHighAccuracy: true,
maximumAge        : 30000,
timeout           : 27000
};
// geo_options


function initMap() {


var myLatLng = new google.maps.LatLng(latitude, longitude);

var map = new google.maps.Map(document.getElementById('map'), {
  center: myLatLng,
  zoom: 5
});

var myIcon = new google.maps.MarkerImage("https://cdn.pixabay.com/photo/2016/03/31/17/53/communication-1293975_960_720.png", null, null, null, new google.maps.Size(25,40));
        var marker = new google.maps.Marker({
            position: myLatLng,
            map: map,
            animation: google.maps.Animation.DROP,

            draggable: false,
            icon: myIcon
        });
// Create an array of alphabetical characters used to label the markers.
var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

// Add some markers to the map.
// Note: The code uses the JavaScript Array.prototype.map() method to
// create an array of markers based on a given "locations" array.
// The map() method here has nothing to do with the Google Maps API.
var infoWin = new google.maps.InfoWindow();
var markers = locations1.map(function(location, i) {
var marker = new google.maps.Marker({
position: location,
animation: google.maps.Animation.DROP,  

});
google.maps.event.addListener(marker, 'click', function(evt) {

var infowindow = new google.maps.InfoWindow;

$.ajax({
        type:"GET",
        url : "/address/",
        datatype: 'json',
        error : function(){
        alert('통신실패!!');    
    },

        success:function (data){
          var address = data['address'];
            var content = address[i % address.length]['address'];
            infowindow.setContent(content);
      infowindow.open(map, marker);
        }});
})
return marker;
});

var mcOptions = {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m',  disableClickZoom: true};
// Add a marker clusterer to manage the markers.
var markerCluster = new MarkerClusterer(map, markers,mcOptions);

google.maps.event.addListener(markerCluster, 'clusterclick', 
function() {var level = map.getLevel();

// 지도를 클릭된 클러스터의 마커의 위치를 기준으로 확대합니다
map.setLevel(level, {anchor: cluster.getCenter()});

}); 

var card = document.getElementById('pac-card');
var input = document.getElementById('pac-input');
var types = document.getElementById('type-selector');
var strictBounds = document.getElementById('strict-bounds-selector');

map.controls[google.maps.ControlPosition.TOP_RIGHT].push(card);

var autocomplete = new google.maps.places.Autocomplete(input);

// Bind the map's bounds (viewport) property to the autocomplete object,
// so that the autocomplete requests use the current map bounds for the
// bounds option in the request.
autocomplete.bindTo('bounds', map);

// Set the data fields to return when the user selects a place.
autocomplete.setFields(
    ['address_components', 'geometry', 'icon', 'name']);

var infowindow = new google.maps.InfoWindow();
var infowindowContent = document.getElementById('infowindow-content');
infowindow.setContent(infowindowContent);
var searchmarker = new google.maps.Marker({
  map: map,
  anchorPoint: new google.maps.Point(0, -29),
  animation: google.maps.Animation.DROP,

});

autocomplete.addListener('place_changed', function() {
  
  infowindow.close();
  searchmarker.setVisible(false);

  var place = autocomplete.getPlace();

  if (!place.geometry) {
    // User entered the name of a Place that was not suggested and
    // pressed the Enter key, or the Place Details request failed.
    window.alert("No details available for input: '" + place.name + "'");
    return;
  }

  // If the place has a geometry, then present it on a map.
  if (place.geometry.viewport) {
    map.fitBounds(place.geometry.viewport);
  } else {
    map.setCenter(place.geometry.location);
    map.setZoom(17);  // Why 17? Because it looks good.
    
  }
  searchmarker.setPosition(place.geometry.location);
  searchmarker.setVisible(true);
  

  var address = '';
  if (place.address_components) {
    address = [
      (place.address_components[0] && place.address_components[0].short_name || ''),
      (place.address_components[1] && place.address_components[1].short_name || ''),
      (place.address_components[2] && place.address_components[2].short_name || '')
    ].join(' ');
  }
  // console.log(place.formatted_address);
  infowindowContent.children['place-icon'].src = place.icon;
  infowindowContent.children['place-name'].textContent = place.name;
  infowindowContent.children['place-address'].textContent = address;
  infowindow.open(map, searchmarker);
  function fillInAddress() {
    var geocoder = new google.maps.Geocoder;

    var currentposition = {'lat' : place.geometry.location.lat(), 'lng' :place.geometry.location.lng()};
    geocoder.geocode({ 'location': currentposition }, function (results, status) {
      index = results.length - 1; 
  if (status === 'OK') {
    if (results[index]) {
      document.getElementById("nation_post").value=results[index].formatted_address;
    } else {
      window.alert('No results found');
    }
  } else {
    window.alert('Geocoder failed due to: ' + status);
  }

})
document.getElementById("lat_post").value=place.geometry.location.lat();
document.getElementById("lng_post").value=place.geometry.location.lng();
document.getElementById("attraction_post").value=place.name;
document.getElementById("address_post").value=place.name +", " + address;
}
   fillInAddress();
}
);

// Sets a listener on a radio button to change the filter type on Places
// Autocomplete.
function setupClickListener(id, types) {
  var radioButton = document.getElementById(id);
  radioButton.addEventListener('click', function() {
    autocomplete.setTypes(types);
  });
}

setupClickListener('changetype-all', []);
setupClickListener('changetype-address', ['address']);
setupClickListener('changetype-establishment', ['establishment']);
setupClickListener('changetype-geocode', ['geocode']);

document.getElementById('use-strict-bounds')
    .addEventListener('click', function() {
      console.log('Checkbox clicked! New state=' + this.checked);
      autocomplete.setOptions({strictBounds : this.checked});
    });
}

window.onload = $(function() {
$.ajax({
        type:"GET",
        url : "/latlng/",
        datatype: 'json',
        error : function(){
        alert('통신실패!!');    
    },
        success:function (data){
          locations1 = data['posts']
        },
        complete: function(){
          getLocation();
        }

    });
});


