/* Increases the guests or quantity field values by 1 when the user clicks the plus button next to the
field if it already has a value less than 10 or the guests field quantity for the quantity field.
The change event is then manually triggered for the closest number input field. Code for the hasClass
jQuery method is from https://api.jquery.com/hasclass/ and code for triggering the change event is from
https://stackoverflow.com/questions/3179385/val-doesnt-trigger-change-in-jquery */

$('.plus').click(function () {
    let currentValue = parseInt($(this).closest('.input-group').find('input[type="number"]').val());
    let maxValue = 10;
    if ($(this).closest('form').hasClass('quantity-form')) {
        maxValue = parseInt($('input[name="guests"]').val());
    }
    if (currentValue < maxValue) {
        $(this).closest('.input-group').find('input[type="number"]').val(currentValue + 1);
        $(this).closest('.input-group').find('input[type="number"]').trigger('change');
    }
});

/* Reduces the guests or quantity field value by 1 when the user clicks the minus button if the field 
already has a value greater than 1 and triggers the change event for the closest number input field.
Code for triggering the change event is from 
https://stackoverflow.com/questions/3179385/val-doesnt-trigger-change-in-jquery */

$('.minus').click(function () {
    let currentValue = parseInt($(this).parent().prev().val());
    if (currentValue > 1) {
        $("input[name='guests']").val(currentValue - 1);
        $(this).closest('.input-group').find('input[type="number"]').trigger('change');
    }
});

/* Submits an AJAX post request when the value of the guests field changes if the value of the field
is between 1 and 10. The total, subtotal and extras values are then updated in the HTML from the data
returned in the response and the extras quantities are updated if they are greater than the new guests
value. Code for the each jQuery method is from https://api.jquery.com/jquery.each/ */

$('input[name="guests"]').on('change', function () {
    let guests = parseInt($(this).val());
    let extras = $('input[name="quantity"]');
    let csrfToken = $('.guests-form').find('input[name="csrfmiddlewaretoken"]').val();
    let postData = {
        'guests': guests,
        'csrfmiddlewaretoken': csrfToken,
    };
    if (guests >= 1 && guests <= 10 ) {
        $.post('/booking/update_guests/', postData).done(function (data) {
            if ($('#subtotal').length) {
                $('#subtotal').children().last().text('£' + data.subtotal);
                $('#extras').children().last().text('£' + data.extras);
            }
            $('#total').children().last().text('£' + data.total);
            $('input[name="guests"]').val(guests);
            $.each($('input[name="quantity"]'), function() {
                if ($(this).val() > guests) {
                    $(this).val(guests);
                }
            });
        });
    } else {
        $('input[name="guests"]').val(1);
    }
});

/* Submits an AJAX post request when the value of the quantity field changes if the closest switch is
in the on position and the value of the quantity field is between 1 and the guests input value. 
The total and extras values are then updated in the HTML from the data returned in the response.
Code for the is checked jQuery method is from 
https://stackoverflow.com/questions/7960208/jquery-if-checkbox-is-checked  */

$('input[name="quantity"]').on('change', function () {
    let quantity = parseInt($(this).val());
    let guests = parseInt($('.guests-form').find("input[name='guests']").val());
    let id = $(this).data('extra');
    let csrfToken = $('.quantity-form').find('input[name="csrfmiddlewaretoken"]').val();
    let postData = {
        'csrfmiddlewaretoken': csrfToken,
        'quantity': quantity
    };
    if ($(this).closest('tr').find('input[type="checkbox"]').is(':checked')) {
        console.log(quantity)
        console.log(guests)
        if (quantity >= 1 && quantity <= guests) {
            $.post(`/booking/update_extra/${id}/`, postData).done(function (data) {
                $('#total strong').text(`£${data.total}`);
                $('#extras span').last().text(`£${data.extras}`);
                $('.quantity-form').find(`input[data-extra="${id}"]`).val(quantity);
            });
        } else {
            $(`#extra-${id}`).find('input[name="quantity"]').val(1);
            $(`#mobile-extra-${id}`).find('input[name="quantity"]').val(1);
        }
    }
});

/* When the coupon form is submitted, prevents the default behaviour and submits an AJAX post request.
If the request returns a success status code the total, subtotal, discount and extras values are then
updated in the HTML from the data returned in the response. If the request returns a failure status code,
invalud feedback will be added below the promo code input field. Code for the input before jQuery method
is from https://api.jquery.com/insertBefore/#insertBefore-target  */

$('.coupon-form').submit(function (e) {
    e.preventDefault();
    let coupon = $(this).find("input[name='coupon']").val();
    let csrfToken = $(this).find('input[name="csrfmiddlewaretoken"]').val();
    let postData = {
        'coupon': coupon,
        'csrfmiddlewaretoken': csrfToken,
    };
    $.post('/booking/add_coupon/', postData).done(function (data) {
        let subtotal = $('#subtotal');
        let discount = $('#discount');
        if (discount.length) {
            discount.find('small').text(`${data.coupon}`);
            discount.find('span').text(`£${data.discount}`);

        } else {
            $(`<li id="discount" class="list-group-item d-flex justify-content-between">
            <div class="text-success"><h6 class="my-0">Promo code</h6><small>${data.coupon}</small>
            </div><span class="text-success">-£${data.discount}</span></li>`).insertBefore('#total');
        }
        if (subtotal.length) {
            subtotal.children().last().text(`£${data.subtotal}`);
        } else {
            $(`<li id="subtotal" class="list-group-item d-flex justify-content-between">
            <span class="my-0">Base Price</span><span>£${data.discount}</span>
            </li>`).insertBefore('#total');
        }
        $('#total').children().last().text('£' + data.total);
        $('.coupon-form').find('input').removeClass('is-invalid');
        $('.coupon-form').find('.w-100').remove();
    }).fail(function () {
        if ($('.invalid-feedback').length) {
            ('.invalid-feedback').text(`Promo code ${coupon} is not valid. Please try again.`);
        } else {
            $('.coupon-form .input-group').append(`<div class="w-100">
            <div class="invalid-feedback d-block mt-2">Promo code ${coupon} is not valid. Please try again.</div></div>`);
        }
        $('.coupon-form').find("input[name='coupon']").addClass('is-invalid');
    });
});

/* When the checkbox is changed, submits an AJAX post request to the add extra URL if the closest switch 
is in the on position or to the delete extra URL if the checkbox is in the off position. The total, 
subtotal, and extras values are then updated in the HTML from the data returned in the response. Code for
the is checked jQuery method is from 
https://stackoverflow.com/questions/7960208/jquery-if-checkbox-is-checked and code for checking or
unchecking the switches is from 
https://stackoverflow.com/questions/426258/setting-checked-for-a-checkbox-with-jquery */

$('input[type="checkbox"]').change(function () {
    let id = $(this).attr('id');
    let csrfToken = $('.quantity-form').find('input[name="csrfmiddlewaretoken"]').val();
    let quantity = parseInt($(this).closest('tr').find('input[name="quantity"]').val());
    let postData = {
        'csrfmiddlewaretoken': csrfToken,
        'quantity': quantity,
    };
    if ($(this).is(':checked')) {
        $.post(`/booking/add_extra/${id}/`, postData).done(function (data) {
            $('#total strong').text(`£${data.total}`);
            if ($('#extras').length) {
                $('#extras span').last().text(`£${data.extras}`);

            } else if ($('#subtotal').length) {
                $(`<li id="extras" class="list-group-item d-flex justify-content-between">
                <span class="my-0">Options and Extras</span>
                <span>£${data.extras}</span>
            </li>`).insertAfter('#subtotal');
            } else {
                $(`<li id="subtotal" class="list-group-item d-flex justify-content-between">
                <span class="my-0">Base Price</span><span>£${data.subtotal}</span></li>
                <li id="extras" class="list-group-item d-flex justify-content-between">
                <span class="my-0">Options and Extras</span>
                <span>£${data.extras}</span>
            </li>`).insertBefore('#transfers');
            }
            $(`#extra-${id}`).find(`input[name="quantity"]`).val(quantity);
            $(`#extra-${id}`).find(`input[type="checkbox"]`).prop('checked', true);
            $(`#mobile-extra-${id}`).find(`input[name="quantity"]`).val(quantity);
            $(`#mobile-extra-${id}`).find(`input[type="checkbox"]`).prop('checked', true);
        });
    } else {
        $.post(`/booking/remove_extra/${id}/`, postData).done(function (data) {
            $('#total strong').text(`£${data.total}`);
            if (data.extras > 0) {
                $('#extras span').last().text(`£${data.extras}`);
                $('#subtotal strong').text(`£${data.subtotal}`);
            } else {
                $('#extras').remove();
                $('#subtotal').remove();
            }
            $(`#extra-${id}`).find(`input[name="quantity"]`).val(1);
            $(`#extra-${id}`).find(`input[type="checkbox"]`).prop('checked', false);
            $(`#mobile-extra-${id}`).find(`input[name="quantity"]`).val(1);
            $(`#mobile-extra-${id}`).find(`input[type="checkbox"]`).prop('checked', false);
        });
    }
});