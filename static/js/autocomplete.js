$('#id_address').on('focus', function () {
    $(this).val("")
    geolocate()
})

$('#id_address').parent().attr('id', 'locationField')

let placeSearch;
let autocomplete;
const componentForm = {
    route: "street_address1",
    locality: "street_address2",
    postal_town: "town_or_city",
    administrative_area_level_2: "county",
    country: "country",
    postal_code: "postcode",
};

function initAutocomplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById("id_address"),
        { types: ["address"] }
    );
    autocomplete.setFields(["address_component"]);
    autocomplete.addListener("place_changed", fillInAddress);
    
}

function fillInAddress() {
    const place = autocomplete.getPlace();

    for (const component in componentForm) {
        $(`#id_${componentForm[component]}`).val("");
      }
    
    for (const component of place.address_components) {
        const addressType = component.types[0];
        if (componentForm[addressType] === 'street_address1') {
            if (place.address_components[0].types[0] === 'street_number') {
                $(`#id_${componentForm[addressType]}`).val(`${place.address_components[0]['long_name']} ${component['long_name']}`)
            } else {
                $(`#id_${componentForm[addressType]}`).val(`${place.address_components[0]['long_name']}`)
            }
        } else if (componentForm[addressType] === 'country') {
            $(`#id_${componentForm[addressType]} option[value=${component['short_name']}]`).prop('selected', true)
            continue
        } else if (componentForm[addressType]) {
            $(`#id_${componentForm[addressType]}`).val(component['long_name'])
        }
    }
}

function geolocate() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            const geolocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude,
            };
            const circle = new google.maps.Circle({
                center: geolocation,
                radius: position.coords.accuracy,
            });
            autocomplete.setBounds(circle.getBounds());
        });
    }
}