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
            type: 'buy',
            theme: 'light-outline',
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

$('#id-saved-cards').find('input[type=checkbox]').change(function () {
    $('#id-saved-cards').find('input[type=checkbox]').not(this).prop('checked', false);
    $('#address').find('input,select').attr('required', false)
    $('#id-save-info').prop('checked', false)
    $('#id-save-card').prop('checked', false)
})

$('#id-default-address').change(function () {
    $('#address').find('input,select').attr('required', false)
})

$('#id-save-info').change(function() {
    if ($(this).prop('checked', false)) {
        $('id-save-card').prop('checked', false)
        $('id-save-card').parent().hide()
    }
})

// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    card.update({ 'disabled': true });
    $('#submit-button').attr('disabled', true);
    loading(true)
    var saveInfo = $('#id-save-info').is(':checked');
    var saveCard = $('#id-save-card').is(':checked');
    var defaultAddress = $('#id-default-address').is(':checked');
    var savedCard = $('#id-saved-cards').find('input:checked').attr('id');
    var paymentDetails
    var profile

    $.get('/checkout/get_profile/').done(function (data) {
        profile = data.profile
    }).then(function () {
        if (defaultAddress) {
            paymentDetails = {
                payment_method: {
                    card: card,
                    billing_details: {
                        name: profile.name,
                        phone: profile.phone_number,
                        email: profile.email,
                        address: {
                            line1: profile.street_address1,
                            line2: profile.street_address2,
                            city: profile.town_or_city,
                            state: profile.county,
                            country: profile.country,
                            postal_code: profile.postcode,
                        }
                    }
                },
                setup_future_usage: saveCard ? "off_session" : ""
            }
        } else if (savedCard) {
            paymentDetails = {
                payment_method: savedCard,
            }
        } else {
            paymentDetails = {
                payment_method: {
                    card: card,
                    billing_details: {
                        name: billingDetails(form.full_name.value),
                        phone: billingDetails(form.phone_number.value),
                        email: billingDetails(form.email.value),
                        address: {
                            line1: billingDetails(form.street_address1.value),
                            line2: billingDetails(form.street_address2.value),
                            city: billingDetails(form.town_or_city.value),
                            state: billingDetails(form.county.value),
                            country: billingDetails(form.country.value),
                            postal_code: billingDetails(form.postcode.value),
                        }
                    }
                },
                setup_future_usage: saveCard ? "off_session" : ""
            }
        }
    }).then(function () {
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        var postData = {
            'csrfmiddlewaretoken': csrfToken,
            'client_secret': clientSecret,
            'save_info': saveInfo,
            'save_card': saveCard,
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
                    $('#id_street_address1').change(function () {
                        $('address').find('input,select').attr('required', true)
                    })
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        loading(false)
                        form.submit();
                    }
                }
            })
        })
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

// Handle payment request button
paymentRequest.on('paymentmethod', function (ev) {
    stripe.confirmCardPayment(
        clientSecret,
        { payment_method: ev.paymentMethod.id },
        { handleActions: false }
    ).then(function (confirmResult) {
        if (confirmResult.error) {
            ev.complete('fail');
        } else {
            ev.complete('success');
            if (confirmResult.paymentIntent.status === "requires_action") {
                stripe.confirmCardPayment(clientSecret).then(function (result) {
                    if (result.error) {
                        var errorDiv = document.getElementById('card-errors');
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
    });
});

function billingDetails(item) {
    if (typeof (item) === undefined) {
        return ""
    } else {
        return $.trim(item)
    }
}