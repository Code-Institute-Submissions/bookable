// Code to display the google map on booking page.

googleApiKey = google_api_key.innerText.replace(/\\/g, '');
googleApiKey = googleApiKey.replace(/\"/g, '');
companyName = company_name.innerText.replace(/\\/g, '');
companyName = companyName.replace(/\"/g, '');
lat = latitude.innerText.replace(/\\/g, '');
lat = lat.replace(/\"/g, '');
lng = longitude.innerText.replace(/\\/g, '');
lng = lng.replace(/\"/g, '');

// The $.getScript() below is from Did Coding's tutorial
// https://www.youtube.com/watch?v=-uxxRx2eZ70

$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + googleApiKey + "&callback=initMap&libraries=places&v=weekly");

// The code below is part of the sample code by google
// https://developers.google.com/maps/documentation/javascript/examples/place-search

let map;
let service;
let infowindow;

function initMap() {
  const company = new google.maps.LatLng(parseFloat(lat), parseFloat(lng));

  infowindow = new google.maps.InfoWindow();
  map = new google.maps.Map(document.getElementById("map"), {
    center: company,
    zoom: 15,
  });

  const request = {
    query: companyName,
    fields: ["name", "geometry"],
  };

  service = new google.maps.places.PlacesService(map);
  service.findPlaceFromQuery(request, (results, status) => {
    if (status === google.maps.places.PlacesServiceStatus.OK && results) {
      for (let i = 0; i < results.length; i++) {
        createMarker(results[i]);
      }

      map.setCenter(results[0].geometry.location);
    }
  });
}

function createMarker(place) {
  if (!place.geometry || !place.geometry.location) return;

  const marker = new google.maps.Marker({
    map,
    position: place.geometry.location,
  });

  google.maps.event.addListener(marker, "click", () => {
    infowindow.setContent(place.name || "");
    infowindow.open(map);
  });
}

window.initMap = initMap;
