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

$('#plus,#plus-sm').click(function () {
    let currentValue = parseInt($(this).prev().val())
    if (currentValue < 10) {
        $(this).prev().val(currentValue + 1);
    }
});

$('#minus,#minus-sm').click(function () {
    let currentValue = parseInt($(this).next().val())
    if (currentValue > 1) {
        $(this).next().val(currentValue - 1);
    }
});

$('.guests-form').submit(function (e) {
    e.preventDefault()
    let guests = $(this).find("input[name='guests']").val()
    let csrfToken = $(this).find('input[name="csrfmiddlewaretoken"]').val();
    let postData = {
        'guests': guests,
        'csrfmiddlewaretoken': csrfToken,
    }
    $.post('/booking/update_guests/', postData).done(function (data) {
        let subtotal = $('#subtotal')
        if (subtotal) {
            $(this).children().last().text('£' + data.subtotal)
        }
        $('#total').children().last().text('£' + data.total)
    })
})

let prevValue = $("input[name='guests']").val()

$("input[name='guests']").change(function () {
    let input = parseInt($(this).val())
    if (input <= 10 && input >= 1) {
        prevValue = input
        $(this).closest('.guests-form').submit()
    } else {
        $(this).val(prevValue)
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
            if (discount.length > 0) {
                discount.find('small').text(`${data.coupon}`)
                discount.find('span').text(`£${data.discount}`)

            } else {
                $(`<li id="discount" class="list-group-item d-flex justify-content-between">
                <div class="text-success"><h6 class="my-0">Promo code</h6><small>${data.coupon}</small>
                </div><span class="text-success">-£${data.discount}</span></li>`).insertBefore('#total')
            }
            if (subtotal.length > 0) {
                subtotal.children().last().text(`£${data.subtotal}`)
            } else {
                $(`<li id="subtotal" class="list-group-item d-flex justify-content-between">
                <span class="my-0">Base Price</span><span>£${data.discount}</span>
                </li>`).insertBefore('#total')
            }
            $('#total').children().last().text('£' + data.total)
            $('.coupon-form').find('input').removeClass('is-invalid')

        } else {
            let invalidFeedback = $('.invalid-feedback')
            if (invalidFeedback.length > 0) {
                invalidFeedback.text(`Promo code ${coupon} is not valid. Please try again.`)
            } else {
                $('.coupon-form .input-group').append(`<div class="invalid-feedback mt-2">Promo code ${coupon} is not valid. Please try again.</div>`)
            }
            $('.coupon-form').find("input[name='coupon']").addClass('is-invalid')
        }
    })
})