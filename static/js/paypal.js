let csrfToken = $('input[name="csrfmiddlewaretoken"]').val()
paypal.Buttons({
    style: { color: 'white' },
    onInit: function (data, actions) {
        if ($('#id-default-address').html() === undefined) {
            actions.disable()
        } else {
            actions.enable()
        }
    },
    onClick: function () {
        if ($('#id-default-address').html() === undefined) {
            $('#payment-form')[0].reportValidity()
        }
    },
    createOrder: function () {
        return fetch('/checkout/create-paypal-transaction/', {
            method: 'post',
            headers: {
                'content-type': 'application/json',
                'X-CSRFToken': csrfToken
            },
        }).then(function (res) {
            return res.json();
        }).then(function (data) {
            return data.id;
        });
    },
    onApprove: function (data, actions) {
        return actions.order.capture().then(function (details) {
            let form = $('#payment-form').serializeArray()
            let formData = {}
            for (i in form) {
                formData[form.i.name] = formData[form.i.value]
            }
            formData['paypal_payment_id'] = details.id
            $.post('/checkout', formData)
        });
    }
}).render('#paypal');
