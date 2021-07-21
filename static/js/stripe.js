// Sets the stripe public key and client secret as variables

let stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
let clientSecret = $('#id_client_secret').text().slice(1, -1);

// Sets the country, currency and total as variables

let country = $('#id_stripe_country').text().slice(1, -1);
let currency = $('#id_stripe_currency').text().slice(1, -1);
let total = parseInt($('#id_stripe_total').text());

/* Sets the save info, csrf token, post data and url as variables. Code for the is checked jQuery method is from 
https://stackoverflow.com/questions/7960208/jquery-if-checkbox-is-checked */

let saveInfo = $('#id_save_info').is(':checked');
let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
let postData = {
    'csrfmiddlewaretoken': csrfToken,
    'client_secret': clientSecret,
    'save_info': saveInfo,
};
let url = '/checkout/cache_checkout_data/';

// Creates an instance of Elements 

let stripe = Stripe(stripePublicKey);
let elements = stripe.elements();

/* Creates an instance of the card element, sets the custom styling
and mounts the card element */

let style = {
    base: {
        color: '#4f4f4f',
        fontFamily: '"PT Sans", sans-serif',
        fontSize: '16px',
        '::placeholder': {
            color: '#a9a9a9'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

let card = elements.create('card', { style: style });
card.mount('#card-element');

// Sets the payment form element as a variable

let form = document.getElementById('payment-form');

// Handles realtime validation errors on the card element

card.addEventListener('change', function (event) {
    let errorDiv = document.getElementById('card-errors');
    if (event.error) {
        let html = `
              <span class="icon" role="alert">
                  <i class="fas fa-times me-2" aria-hidden="true"></i>
              </span>
              <span>${event.error.message}</span>
          `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handles selecting or unselecting of saved card checkboxes.

$('#saved-cards input').change(function () {
    /* Sets all other saved cards checkboxes to false. Code for the is checked jQuery method is from 
    https://stackoverflow.com/questions/7960208/jquery-if-checkbox-is-checked */
    $('#saved-cards input').not(this).prop('checked', false);
    if ($(this).is(':checked')) {
        /* Hides the save card checkbox, destroys the card element and creates and 
        mounts a cvv element. Code for mounting the cvc element and unmounting the 
        card element is from https://stripe.com/docs/js/element/other_methods/ and
        code for creating the cvc element is from 
        https://stripe.com/docs/payments/save-during-payment */
        $('#id_save_card').parent().hide();
        $('#card-element').addClass('w-50');
        card.destroy();
        card = elements.create('cardCvc', { style: style });
        card.mount('#card-element');
    } else {
        /* Shows the save card checkbox, destroys the cvc element and creates and 
        mounts a card element. Code for mounting the card element and unmounting the 
        cvv element is from https://stripe.com/docs/js/element/other_methods/ */
        $('#id_save_card').parent().show();
        $('#card-element').removeClass('w-50');
        card.destroy();
        card = elements.create('card', { style: style });
        card.mount('#card-element');
    }
});

// Handles card payments and form submission. 

form.addEventListener('submit', function (e) {
    // Prevents the form's default behaviour
    e.preventDefault();
    // Disables the card element and calls the loading function
    card.update({ 'disabled': true });
    loading(true);
    /* Sets the checked attribute of the save card checkbox and the ID of the checked saved card 
    checkbox as variables. Code for the is checked jQuery method is from 
    https://stackoverflow.com/questions/7960208/jquery-if-checkbox-is-checked */ 
    let saveCard = $('#id_save_card').is(':checked');
    let savedCard = $('#saved-cards input:checked').attr('id');
    // Declares the payment details variable
    let paymentDetails;
    // Deletes any error messages from the payment request button errors div
    $('#card-errors, #payment-request-button-errors').html('');
    /* Updates the paymentDetails variable with the payment details. Code for saving the card is from 
    https://github.com/stripe-samples/saving-card-after-payment/blob/master/using-webhooks/client/script.js#L86-L91
    and code for charging a saved card is from https://stripe.com/docs/payments/save-during-payment */
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
        };
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
        };
    }
    // Submits an AJAX post request to the cache checkout URL with postData 
    $.post(url, postData).done(function () {
        // Confirm the PaymentIntent and add the payment details to the PaymentIntent
        stripe.confirmCardPayment(clientSecret, paymentDetails
        ).then(function (result) {
            if (result.error) {
                /* The payment failed so the loading circle is hidden in the submit button and 
                the error is displayed in the card errors div */
                loading(false);
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times me-2" aria-hidden="true"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                card.update({ 'disabled': false });
            } else {
                // Payment has succeeded and the form is submited
                if (result.paymentIntent.status === 'succeeded') {
                    loading(false);
                    form.submit();
                }
            }
        });
    }).fail(function() {
        /* Reloads the page if the AJAX post to cache checkout returns an error status code as
        the error will be in django messages */
        location.reload();
    });
});


// Show a spinner on payment submission. Code is from https://stripe.com/docs/payments/integration-builder
var loading = function (isLoading) {
    if (isLoading) {
        // Disables the button and shows the spinner
        document.querySelector("#payment-btn").disabled = true;
        document.querySelector("#spinner").classList.remove("d-none");
        document.querySelector("#button-text").classList.add("d-none");
    } else {
        // Enables the button and hides the spinner
        document.querySelector("#payment-btn").disabled = false;
        document.querySelector("#spinner").classList.add("d-none");
        document.querySelector("#button-text").classList.remove("d-none");
    }
};

// Creates a paymentRequest instance. Code is from https://stripe.com/docs/stripe-js/elements/payment-request-button

let paymentRequest = stripe.paymentRequest({
    country: country,
    currency: currency,
    total: {
        label: 'Total',
        amount: total,
    },
    requestPayerName: true,
    requestPayerEmail: true,
});

// Creates the paymentRequestButton Element. Code is from https://stripe.com/docs/stripe-js/elements/payment-request-button

let prButton = elements.create('paymentRequestButton', {
    paymentRequest: paymentRequest,
    style: {
        paymentRequestButton: {
            type: 'book',
            theme: 'dark',
            height: '55px',
        },
    },
});

/* Checks the availability of the Payment Request API and shows the payment request button
if the API is available. Code is from https://stripe.com/docs/stripe-js/elements/payment-request-button */

paymentRequest.canMakePayment().then(function (result) {
    if (result) {
        prButton.mount('#payment-request-button');
    } else {
        document.getElementById('payment-request-button').style.display = 'none';
    }
});

/* Handles form validation for payment request button. Code is from 
https://stackoverflow.com/questions/53707534/how-can-i-disable-the-stripe-payment-request-button-until-a-form-is-complete */

prButton.on('click', function (e) {
    if (!form.reportValidity()) {
        e.preventDefault();
    }
});

/* Handles payment request button payments and form submission.
Code is from https://stripe.com/docs/stripe-js/elements/payment-request-button */

paymentRequest.on('paymentmethod', function (e) {
    // Deletes any error messages from the payment request button errors div
    $('#card-errors, #payment-request-button-errors').html('');
    // Submits an AJAX post request to the cache checkout URL with postData 
    $.post(url, postData).done(function () {
        // Confirm the PaymentIntent and add shipping details to the PaymentIntent
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
            { handleActions: false }
        ).then(function (confirmResult) {
            /* Reports to the browser that the payment failed, prompting it to
            re-show the payment interface, or show an error message and close
            the payment interface. */
            if (confirmResult.error) {
                e.complete('fail');
            } else {
                /* Reports to the browser that the payment was successful, prompting
                it to close the browser payment method collection interface. */
                e.complete('success');
                // Checks if the PaymentIntent requires any actions
                if (confirmResult.paymentIntent.status === "requires_action") {
                    stripe.confirmCardPayment(clientSecret).then(function (result) {
                        /* The payment failed and the error is displayed in the payment request button
                        errors div */
                        if (result.error) {
                            var errorDiv = document.getElementById('payment-request-button-errors');
                            var html = `
                                <span class="icon" role="alert">
                                <i class="fas fa-times me-2" aria-hidden="true"></i>
                                </span>
                                <span>${result.error.message}</span>`;
                            $(errorDiv).html(html);
                        } else {
                            // Payment has succeeded and the form is submited
                            form.submit();
                        }
                    });
                } else {
                    // Payment has succeeded and the form is submited
                    form.submit();
                }
            }
        });
    }).fail(function() {
        /* Reloads the page if the AJAX post request to cache checkout fails as the error will be
        in django messages */
        location.reload();
    });
});