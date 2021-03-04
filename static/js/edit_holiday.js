$(document).ready(function () {
    $('.btn-file').addClass('mt-2')
    $('.custom-checkbox').addClass('form-check ms-1')
    $('.form-check input').addClass('form-check-input').attr('type', 'checkbox')
    $('.form-check label').addClass('form-check-label').show()
    $('fieldset .row').addClass('mb-3')
    $('.price, .itinerary').each(function() {
        $(this).find('.form-check').last().addClass('delete-check')
    })
    $('.delete-check label').addClass('text-danger')
    $('.itinerary').last().find('select').val('')
})
$('#new-image').change(function () {
    var file = $('#new-image')[0].files[0];
    $('#filename').text(`Image will be set to: ${file.name}`);
    $('#filename').addClass('mt-3');
});
priceCounter = $('.price').length
let addedPrice = function () {
    $('fieldset .row').addClass('mb-3');
    $(`#div_id_price_set-${priceCounter}-offer, #div_id_price_set-${priceCounter}-DELETE`).addClass('form-check ms-1')
    $(`#div_id_price_set-${priceCounter}-offer input`).addClass('form-check-input')
    $(`#div_id_price_set-${priceCounter}-offer label`).addClass('form-check-label')
    $(`#div_id_price_set-${priceCounter}-DELETE`).addClass('delete-check')
    $(`<input type="checkbox" name="price_set-${priceCounter}-DELETE" id="id_price_set-${priceCounter}-DELETE" class="form-check-input">`).insertBefore(`#div_id_price_set-${priceCounter}-DELETE label`)
    $(`#div_id_price_set-${priceCounter}-DELETE label`).addClass('form-check-label, text-danger').show()
    priceCounter += 1
    $('.price').last().find('legend').text(`Price ${priceCounter}`)
}
itineraryCounter = $('.itinerary').length
let addedItinerary = function () {
    $('fieldset .row').addClass('mb-3');
    $(`#div_id_itinerary_set-${itineraryCounter}-DELETE`).addClass('form-check delete-check ms-1')
    $(`<input type="checkbox" name="itinerary_set-${itineraryCounter}-DELETE" id="id_itinerary_set-${itineraryCounter}-DELETE" class="form-check-input">`).insertBefore(`#div_id_itinerary_set-${itineraryCounter}-DELETE label`)
    $(`#div_id_itinerary_set-${itineraryCounter}-DELETE label`).addClass('form-check-label, text-danger').show()
    itineraryCounter += 1
    $('.itinerary').last().find('legend').text(`Itinerary ${itineraryCounter}`)
    $('.itinerary').find('select').val('')
}
$('#next').click(function () {
    $('fieldset').not('.d-none').next().removeClass('d-none')
    $('fieldset').not('.d-none').first().addClass('d-none')
    if ($('fieldset').not('.d-none').attr('id') === 'package') {
        $('#back').addClass('d-none')
    } else {
        $('#back').removeClass('d-none')
    }
    if ($('fieldset').not('.d-none').attr('id') === 'itineraries') {
        $('#next').addClass('d-none')
        $('button[type="submit"]').removeClass('d-none')
    } else {
        $('button[type="submit"]').addClass('d-none')
        $('#next').removeClass('d-none')
    }
})
$('#back').click(function () {
    $('fieldset').not('.d-none').prev().removeClass('d-none')
    $('fieldset').not('.d-none').last().addClass('d-none')
    if ($('fieldset').not('.d-none').attr('id') === 'package') {
        $('#back').addClass('d-none')
    } else {
        $('#back').removeClass('d-none')
    }
    if ($('fieldset').not('.d-none').attr('id') === 'itineraries') {
        $('#next').addClass('d-none')
        $('button[type="submit"]').removeClass('d-none')
    } else {
        $('button[type="submit"]').addClass('d-none')
        $('#next').removeClass('d-none')
    }
})