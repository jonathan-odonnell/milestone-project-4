// Declares the autocomplete global variable

let autocomplete;

/* Sets the address input's parent element's ID to locationField. Code is from 
https://stackoverflow.com/questions/10219396/jquery-update-element-id */

$('#id_address').parent().attr('id', 'locationField');

// Clears the address input and calls the geolocate function when the user focuses in the address field

$('#id_address').on('focus', function () {
    $(this).val('');
    geolocate();
});

/* Creates the autocomplete object, restricting the search predictions to addresses in the UK.
Calls the fillInAddress function when the user selects an address from the drop-down. Code is from 
https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete-addressform */

function initAutocomplete() {
    let addressField = document.getElementById('id_address');
    autocomplete = new google.maps.places.Autocomplete(addressField, {
        componentRestrictions: {
            country: 'gb'
        },
        fields: ['address_components', 'geometry'],
        types: ['address'],
    });
    autocomplete.addListener("place_changed", fillInAddress);
}

/* Gets the place details from the autocomplete object and populates the address fields in the form. Code is from 
https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete-addressform */

function fillInAddress() {
    let place = autocomplete.getPlace();
    let streetAddress1 = '';
    $(`#id_street_address2`).val('');

    for (let component of place.address_components) {
        let componentType = component.types[0];

        switch (componentType) {
            case 'street_number': {
                streetAddress1 = `${component.long_name} `;
                break;
            }
            case 'route': {
                streetAddress1 += `${component.long_name}`;
                $('#id_street_address1').val(`${streetAddress1}`);
                break;
            }
            case 'sublocality_level_1': {
                $('#id_street_address2').val(component.long_name);
                break;
            }
            case 'locality': {
                if (!$('#id_street_address2').val()) {
                    $('#id_street_address2').val(component.long_name);
                }
                break;
            }
            case 'postal_town': {
                $('#id_town_or_city').val(component.long_name);
                break;
            }
            case 'administrative_area_level_2': {
                $('#id_county').val(component.long_name);
                break;
            }
            case 'country': {
                $(`#id_country option[value=${component.short_name}]`).prop('selected', true);
                break;
            }
            case 'postal_code': {
                $('#id_postcode').val(component.long_name);
                break;
            }
        }
    }
}

/* Bias the autocomplete object to the user's geographical location as supplied by the browser's 
'navigator.geolocation' object. Code is from 
https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete-addressform */

function geolocate() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            geolocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude,
            };
            let circle = new google.maps.Circle({
                center: geolocation,
                radius: position.coords.accuracy,
            });
            autocomplete.setBounds(circle.getBounds());
        });
    }
}