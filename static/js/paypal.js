paypal.Buttons({
    style: { color: 'white' },
    onInit: function (data, actions) {
        if(!$('#payment-form')[0].checkValidity()) {
            actions.disable()
        }
        $('#payment-form').find('input, select').change(function () {
            if ($('#payment-form')[0].checkValidity()) {
                actions.enable()
            } else {
                actions.disable()
            }
        })
    },
    onClick: function () {
        if (!$('#payment-form')[0].checkValidity()) {
            $('#payment-form')[0].reportValidity()
        }
    },
    createOrder: function () {
        return fetch('/checkout/paypal/', {
            method: 'post',
            headers: {
                'content-type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                'full_name': $('#payment-form').find('#id_full_name').val(),
                'email': $('#payment-form').find('#id_email').val(),
                'phone_number': $('#payment-form').find('#id_phone_number').val(),
                'street_address1': $('#payment-form').find('#id_street_address1').val(),
                'street_address2': $('#payment-form').find('#id_street_address2').val(),
                'town_or_city': $('#payment-form').find('#id_town_or_city').val(),
                'county': $('#payment-form').find('#id_county').val(),
                'country': $('#payment-form').find('#id_country').val(),
                'postcode': $('#payment-form').find('#id_postcode').val(),
                'save_info': $('#payment-form').find('#id_save_info').val(),
            })
        }).then(function (res) {
            return res.json();
        }).then(function (data) {
            return data.id;
        });
    },
    onApprove: function (data, actions) {
        return fetch(`/checkout/paypal/approve/`, {
            method: 'post',
            headers: {
                'content-type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                'order_id': data.orderID
            })
        }).then(function (res) {
            return res.json();
        }).then(function (details) {
            location.replace(`/checkout/checkout_success/${details.purchase_units[0].reference_id}/`)
        })
    }
}).render('#paypal');
