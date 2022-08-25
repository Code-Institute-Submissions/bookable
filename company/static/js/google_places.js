googleApiKey = google_api_key.innerText.replace(/\\/g, '');
googleApiKey = googleApiKey.replace(/\"/g, '');

// The $.getScript() below is from Did Coding's tutorial
// https://www.youtube.com/watch?v=-uxxRx2eZ70

$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + googleApiKey + "&libraries=places");

// The code below is part of the sample code by google
// https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete-addressform#try-sample

let autocomplete;
let address;

function initAutocomplete() {
  address = document.querySelector("#id_address");
  autocomplete = new google.maps.places.Autocomplete(address, {
    fields: ["address_components", "geometry"],
    types: ["address"],
  });
  // When the user selects an address from the drop-down, populate the
  // address fields in the form.
}

window.addEventListener('load', initAutocomplete);
