google_api_key = google_api_key.innerText.replace(/\\/g, '');
google_api_key = google_api_key.replace(/\"/g, '');
$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places")
.done(function( script, textStatus ) {
  window.addEventListener('load', initAutocomplete)
})
/**
 * @license
 * Copyright 2019 Google LLC. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
// This sample uses the Places Autocomplete widget to:
// 1. Help the user select a place
// 2. Retrieve the address components associated with that place
// 3. Populate the form fields with those address components.
// This sample requires the Places library, Maps JavaScript API.
// Include the libraries=places parameter when you first load the API.
// For example: <script
// src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">
let autocomplete;
let address;

function initAutocomplete() {
  address = document.querySelector("#id_address");
  autocomplete = new google.maps.places.Autocomplete(address, {
    // componentRestrictions: { country: ["us", "ca"] },
    fields: ["address_components", "geometry"],
    types: ["address"],
  });
  // address.focus();
  // When the user selects an address from the drop-down, populate the
  // address fields in the form.
  // autocomplete.addListener("place_changed", fillInAddress);
}

window.initAutocomplete = initAutocomplete;
