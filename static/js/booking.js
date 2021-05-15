$(document).ready(function generateStars() {
    let fullStar = "<i class='fas fa-star pe-1'></i>"
    let halfStar = "<i class='fas fa-star-half-alt pe-1'></i>"
    let emptyStar = "<i class='far fa-star pe-1'></i>"
    $('.rating').each(function () {
        rating = parseFloat($(this).html())
        displayStars = ""
        for (let i = 1; i <= 5; i++) {
            if (Math.round(rating) >= i) {
                displayStars += fullStar
            } else if (rating >= i - 1) {
                displayStars += halfStar
            } else {
                displayStars += emptyStar
            }
        }
        $(this).html(displayStars)
    })
})

let maxValue = 10
let initialGuests = $('input[name="guests"]').val()
let initialQuantity = $('input[name="quantity"]').val()
let action

// Manual change trigger code is from https://stackoverflow.com/questions/53894042/change-not-triggered-if-change-the-value-by-js

$('.plus').click(function () {
    let currentValue = parseInt($(this).parent().prev().val())
    let maxValue = 10
    action = 'increase'
    if ($(this).closest('form').hasClass('quantity-form')) {
        maxValue = $('.guests-form').find("input[name='guests']").val()
    }
    if (currentValue < maxValue) {
        $(this).parent().prev().val(currentValue + 1).trigger('change');
    }
});

$('.minus').click(function () {
    let currentValue = parseInt($(this).parent().prev().val())
    if (currentValue > 1) {
        action = 'decrease'
        $(this).parent().prev().val(currentValue - 1).trigger('change');
    }
});

$('input[name="guests"]').on('change', function () {
    let guests = parseInt($(this).val())
    maxValue = 10
    let csrfToken = $('.guests-form').find('input[name="csrfmiddlewaretoken"]').val();
    let postData = {
        'guests': guests,
        'csrfmiddlewaretoken': csrfToken,
    }
    if (guests <= maxValue && guests >= 1) {
        initialGuests = guests
        $.post('/booking/update_guests/', postData).done(function (data) {
            if ($('#subtotal').length) {
                $('#subtotal').children().last().text('£' + data.subtotal)
                $('#extras').children().last().text('£' + data.extras)
            }
            $('#total').children().last().text('£' + data.total)
            if (action === 'decrease') {
                $('input[name="quantity"]').val(guests)
            }
        })
    } else {
        $(this).val(initialGuests)
    }
})

$('input[name="quantity"]').on('change', function () {
    if ($(this).closest('tr').find('input[type="checkbox"]').is(':checked')) {
        let quantity = parseInt($(this).val())
        maxValue = $('.guests-form').find("input[name='guests']").val()
        let id = $(this).data('extra')
        let csrfToken = $('.quantity-form').find('input[name="csrfmiddlewaretoken"]').val();
        let postData = {
            'csrfmiddlewaretoken': csrfToken,
            'quantity': quantity
        }
        if (quantity <= maxValue && quantity >= 1) {
            initialQuantity = quantity
            $.post(`/booking/update_extra/${id}/`, postData).done(function (data) {
                $('#total strong').text(`£${data.total}`)
                $('#extras span').last().text(`£${data.extras}`)
            })
        } else {
            $(this).val(initialQuantity)
        }
    }
})

$('.coupon-form').submit(function (e) {
    e.preventDefault()
    let coupon = $(this).find("input[name='coupon']").val()
    let csrfToken = $(this).find('input[name="csrfmiddlewaretoken"]').val();
    let postData = {
        'coupon': coupon,
        'csrfmiddlewaretoken': csrfToken,
    }
    $.post('/booking/add_coupon/', postData).done(function (data) {
        if (data.success) {
            let subtotal = $('#subtotal')
            let discount = $('#discount')
            if (discount.length) {
                discount.find('small').text(`${data.coupon}`)
                discount.find('span').text(`£${data.discount}`)

            } else {
                $(`<li id="discount" class="list-group-item d-flex justify-content-between">
                <div class="text-success"><h6 class="my-0">Promo code</h6><small>${data.coupon}</small>
                </div><span class="text-success">-£${data.discount}</span></li>`).insertBefore('#total')
            }
            if (subtotal.length) {
                subtotal.children().last().text(`£${data.subtotal}`)
            } else {
                $(`<li id="subtotal" class="list-group-item d-flex justify-content-between">
                <span class="my-0">Base Price</span><span>£${data.discount}</span>
                </li>`).insertBefore('#total')
            }
            $('#total').children().last().text('£' + data.total)
            $('.coupon-form').find('input').removeClass('is-invalid')
            $('.coupon-form').find('.w-100').remove()
        } else {
            if ($('.invalid-feedback').length) {
                ('.invalid-feedback').text(`Promo code ${data.coupon} is not valid. Please try again.`)
            } else {
                $('.coupon-form .input-group').append(`<div class="w-100"><div class="invalid-feedback d-block mt-2">Promo code ${data.coupon} is not valid. Please try again.</div></div>`)
            }
            $('.coupon-form').find("input[name='coupon']").addClass('is-invalid')
        }
    })
})

$('input[type="checkbox"]').change(function () {
    let id = $(this).attr('id')
    let csrfToken = $('.quantity-form').find('input[name="csrfmiddlewaretoken"]').val();
    let quantity = $(this).closest('tr').find('input[name="quantity"]').val()
    let postData = {
        'csrfmiddlewaretoken': csrfToken,
        'quantity': quantity,
    }
    if ($(this).prop('checked')) {
        $.post(`/booking/add_extra/${id}/`, postData).done(function (data) {
            $('#total strong').text(`£${data.total}`)
            if ($('#extras').length) {
                $('#extras span').last().text(`£${data.extras}`)

            } else if ($('#subtotal').length) {
                $(`<li id="extras" class="list-group-item d-flex justify-content-between">
                <span class="my-0">Options and Extras</span>
                <span>£${data.extras}</span>
            </li>`).insertAfter('#subtotal')
            }
            else {
                $(`<li id="subtotal" class="list-group-item d-flex justify-content-between">
                <span class="my-0">Base Price</span><span>£${data.subtotal}</span></li>
                <li id="extras" class="list-group-item d-flex justify-content-between">
                <span class="my-0">Options and Extras</span>
                <span>£${data.extras}</span>
            </li>`).insertBefore('#transfers')
            }
            $('.add-extra .btn').removeClass('btn-outline-primary')
            $('.add-extra').find('i').addClass('fa-times')
            $('.add-extra').find('i').removeClass('fa-plus')
        })
    } else {
        $.post(`/booking/remove_extra/${id}/`, postData).done(function (data) {
            $('#total strong').text(`£${data.total}`)
            if (data.extras > 0) {
                $('#extras span').last().text(`£${data.extras}`)
                $('#subtotal strong').text(`£${data.subtotal}`)
            } else {
                $('#extras').remove()
                $('#subtotal').remove()
            }
            $('.add-extra .btn').addClass('btn-outline-primary')
            $('.add-extra').find('i').addClass('fa-plus')
            $('.add-extra').find('i').removeClass('fa-times')
        })
    }
})