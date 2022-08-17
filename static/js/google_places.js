google_api_key = google_api_key.innerText.replace(/\\/g, '');
google_api_key = google_api_key.replace(/\"/g, '');

// The code below is the same code done by Did Coding's tutorial with minor changes
// https://www.youtube.com/watch?v=-uxxRx2eZ70

$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places")
.done(function( script, textStatus ) {
  window.addEventListener('load', initAutocomplete)
})

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

window.initAutocomplete = initAutocomplete;
