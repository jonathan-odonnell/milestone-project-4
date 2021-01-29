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

$('form').submit(function (e) {
    e.preventDefault()
    let guests = $(this).find("input[name='guests']").val()
    let csrfToken = $(this).find('input[name="csrfmiddlewaretoken"]').val();
    let postData = {
        'guests': guests,
        'csrfmiddlewaretoken': csrfToken,
    }
    $.post('/booking/update_guests/', postData).done(function(data) {
        let subtotal = $('#subtotal')
        if (subtotal) {
            $(this).children().last().text('£' + data.subtotal)
        }
        $('#total').children().last().text('£' + data.total)
    })
})

$("input[name='guests']").change(function () {
    $(this).closest('form').submit()
})