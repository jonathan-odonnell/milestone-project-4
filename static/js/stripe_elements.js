var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var country = $('#id_stripe_country').text().slice(1, -1);
var currency = $('#id_stripe_currency').text().slice(1, -1);
var total = parseInt($('#id_stripe_total').text());
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"PT Sans", sans-serif',
        fontSize: '16px',
        '::placeholder': {
            color: '#4f4f4f'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

var card = elements.create('card', { style: style });
card.mount('#card-element');

// Handle form submit
var form = document.getElementById('payment-form');

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
              <span class="icon" role="alert">
                  <i class="fas fa-times"></i>
              </span>
              <span>${event.error.message}</span>
          `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

$('#saved-cards input').change(function () {
    $('#saved-cards input').not(this).prop('checked', false);
    if ($(this).is(':checked')) {
        $('#id_save_card').parent().hide()
        $('#card-element').addClass('w-50')
        card.destroy()
        card = elements.create('cardCvc', { style: style });
        card.mount('#card-element');
    } else {
        $('#id_save_card').parent().show()
        $('#card-element').removeClass('w-50')
        card.destroy()
        card = elements.create('card', { style: style });
        card.mount('#card-element');
    }
})

form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    card.update({ 'disabled': true });
    $('#submit-button').attr('disabled', true);
    loading(true)
    var saveInfo = $('#id_save_info').is(':checked');
    var saveCard = $('#id_save_card').is(':checked');
    var savedCard = $('#saved-cards').find('input').is(':checked').attr('id');
    var paymentDetails
    $('#card-errors, #payment-request-button-errors').html('')

    if (savedCard) {
        paymentDetails = {
            payment_method: savedCard,
            payment_method_options: {
                card: {
                    cvc: card,
                },
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    state: $.trim(form.county.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                }
            },
        }
    } else {
        paymentDetails = {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address: {
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        state: $.trim(form.county.value),
                        country: $.trim(form.country.value),
                        postal_code: $.trim(form.postcode.value),
                    }
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    state: $.trim(form.county.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                }
            },
            setup_future_usage: saveCard ? "on_session" : ""
        }
    }
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    var url = '/checkout/cache_checkout_data/';

    $.post(url, postData).done(function () {
        stripe.confirmCardPayment(clientSecret, paymentDetails
        ).then(function (result) {
            if (result.error) {
                loading(false)
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                card.update({ 'disabled': false });
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    loading(false)
                    form.submit();
                }
            }
        })
    }).fail(function() {
        location.reload();
    })
});


// Show a spinner on payment submission
var loading = function (isLoading) {
    if (isLoading) {
        // Disable the button and show a spinner
        document.querySelector("button").disabled = true;
        document.querySelector("#spinner").classList.remove("hidden");
        document.querySelector("#button-text").classList.add("hidden");
    } else {
        document.querySelector("button").disabled = false;
        document.querySelector("#spinner").classList.add("hidden");
        document.querySelector("#button-text").classList.remove("hidden");
    }
};

var paymentRequest = stripe.paymentRequest({
    country: country,
    currency: currency,
    total: {
        label: 'Total',
        amount: total,
    },
    requestPayerName: true,
    requestPayerEmail: true,
});

var prButton = elements.create('paymentRequestButton', {
    paymentRequest: paymentRequest,
    style: {
        paymentRequestButton: {
            type: 'book',
            theme: 'dark',
            height: '64px'
        },
    },
});

paymentRequest.canMakePayment().then(function (result) {
    if (result) {
        prButton.mount('#payment-request-button');
    } else {
        document.getElementById('payment-request-button').style.display = 'none';
    }
});

// Handles form validation for payment request button. Code is from https://stackoverflow.com/questions/53707534/how-can-i-disable-the-stripe-payment-request-button-until-a-form-is-complete
prButton.on('click', function (e) {
    if (!form.reportValidity()) {
        e.preventDefault();
    }
});

// Handle payment request button
paymentRequest.on('paymentmethod', function (ev) {
    $('#card-errors, #payment-request-button-errors').html('')
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    var url = '/checkout/cache_checkout_data/';
    $.post(url, postData).done(function () {
        stripe.confirmCardPayment(
            clientSecret,
            {
                payment_method: ev.paymentMethod.id,
                shipping: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    address: {
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        state: $.trim(form.county.value),
                        country: $.trim(form.country.value),
                        postal_code: $.trim(form.postcode.value),
                    }
                },
            },
            { handleActions: false },
        )
    }).then(function (confirmResult) {
        if (confirmResult.error) {
            ev.complete('fail');
        } else {
            ev.complete('success');
            if (confirmResult.paymentIntent.status === "requires_action") {
                stripe.confirmCardPayment(clientSecret).then(function (result) {
                    if (result.error) {
                        var errorDiv = document.getElementById('payment-request-button-errors');
                        var html = `
                            <span class="icon" role="alert">
                            <i class="fas fa-times"></i>
                            </span>
                            <span>${result.error.message}</span>`;
                        $(errorDiv).html(html);
                    } else {
                        form.submit()
                    }
                });
            } else {
                form.submit()
            }
        }
    }).fail(function() {
        location.reload();
    });
});