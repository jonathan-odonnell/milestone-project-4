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
        }}).then(function (res) {
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
            $('input[name="paypal_pid"]').val(details.id)
            $('#payment-form').submit()
        })
    }
}).render('#paypal');
