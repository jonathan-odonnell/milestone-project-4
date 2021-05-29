/* Renders the PayPal button inside the paypal ID. Code is from 
https://developer.paypal.com/docs/checkout/integrate/ */
paypal.Buttons({
    // Button styling
    style: { color: 'white' },
    /* onInit is called when the PayPal button first renders. Code is from 
    https://developer.paypal.com/docs/checkout/integration-features/validation/ */
    onInit: function (data, actions) {
        // Disables the paypal button if the payment form is not valid
        if(!$('#payment-form')[0].checkValidity()) {
            actions.disable();
        }
        // Enables the PayPal button when any of the payment form fields are changed and the form is valid.
        $('#payment-form').find('input, select').change(function () {
            if ($('#payment-form')[0].checkValidity()) {
                actions.enable();
            } else {
                actions.disable();
            }
        });
    },
    /* onClick is called when the PayPal button is clicked. Code is from 
    https://developer.paypal.com/docs/checkout/integration-features/validation/ */
    onClick: function () {
        /* Calls the reportValidity method on the payment form to show error messages 
        on any invalid fields */
        $('#payment-form')[0].reportValidity();
    },
    createOrder: function () {
        /* Submits a post request to the server to set up the PayPal transaction and
        returns the id sent in the server's response. Code is from 
        https://developer.paypal.com/docs/checkout/reference/server-integration/set-up-transaction/
        and https://stackoverflow.com/questions/43606056/proper-django-csrf-validation-using-fetch-post-request */
        return fetch('/checkout/paypal/', {
            method: 'post',
            headers: {
                'content-type': 'application/json',
                'X-CSRFToken': csrfToken
        }}).then(function (res) {
            return res.json();
        }).then(function (data) {
            return data.id;
        });
    },
    onApprove: function (data) {
        /* Gets the orderID from the data and submits a post request to the server to capture the
        PayPal transaction funds. The paypal_pid input field is then updated with the orderID sent
        in the server's response and the form is submitted. Code is from 
        https://developer.paypal.com/docs/checkout/reference/server-integration/capture-transaction/
        and https://stackoverflow.com/questions/43606056/proper-django-csrf-validation-using-fetch-post-request
        */
        return fetch(`/checkout/paypal/approve/`, {
            method: 'post',
            headers: {
                'content-type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                'order_id': data.orderID,
            })
        }).then(function (res) {
            return res.json();
        }).then(function (data) {
            $('input[name="paypal_pid"]').val(data.id);
            $('#payment-form').submit();
        });
    }
}).render('#paypal');
