$(document).ready(function () {
    $('.btn-file').addClass('mt-2')
    $('#div_id_transfers_included, #div_id_price_set-0-offer').addClass('form-check ms-1')
    $('#div_id_transfers_included, #div_id_price_set-0-offer').find('input').addClass('form-check-input')
    $('#div_id_transfers_included, #div_id_price_set-0-offer').find('input').addClass('form-check-label')
    $('fieldset .row').addClass('mb-3')
    $('.delete-row').remove()
    $('.itinerary').find('select').val('')
})
$('#new-image').change(function () {
    var file = $('#new-image')[0].files[0];
    $('#filename').text(`Image will be set to: ${file.name}`);
    $('#filename').addClass('mt-3');
});
priceCounter = 1
let addedPrice = function () {
    $('fieldset .row').addClass('mb-3');
    $(`#div_id_price_set-${priceCounter}-offer`).addClass('form-check ms-1')
    $(`#div_id_price_set-${priceCounter}-offer`).find('input').addClass('form-check-input')
    $(`#div_id_price_set-${priceCounter}-offer`).find('input').addClass('form-check-label')
    priceCounter += 1
    $('.price').last().find('legend').text(`Price ${priceCounter}`)
    $('.delete-row').remove()
}
itineraryCounter = 1
let addedItinerary = function () {
    $('fieldset .row').addClass('mb-3');
    itineraryCounter += 1
    $('.itinerary').last().find('legend').text(`Itinerary ${itineraryCounter}`)
    $('.itinerary').find('select').val('')
    $('.delete-row').remove()
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