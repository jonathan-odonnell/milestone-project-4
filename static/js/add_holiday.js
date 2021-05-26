$(document).ready(function () {
    $('.btn-file').addClass('mt-2')
    $('.custom-checkbox').addClass('form-check ms-1')
    $('.form-check input').addClass('form-check-input')
    $('.form-check label').addClass('form-check-label')
    $('fieldset .row').addClass('mb-3')
    if(!$('select').val()) {
        $('select').css('color', '#a9a9a9');
    };
})
$("select").change(function () {
    if (!$(this).val()) {
        $(this).css("color", "#a9a9a9");
    } else {
        $(this).css("color", "#4a4a4a");
    }
});
$('#new-image').change(function () {
    var file = $('#new-image')[0].files[0];
    $('#filename').text(`Image will be set to: ${file.name}`);
    $('#filename').addClass('mt-3');
});
activityCounter = 1
let addedActivity = function () {
    $('fieldset .row').addClass('mb-3');
    activityCounter += 1
    $('.activity').last().find('legend').text(`Activity ${activityCounter}`)
    $('.delete-row').remove()
}
itineraryCounter = 1
let addedItinerary = function () {
    $('fieldset .row').addClass('mb-3');
    itineraryCounter += 1
    $('.itinerary').last().find('legend').text(`Itinerary ${itineraryCounter}`)
    $('.delete-row').remove()
}
$('#next').click(function () {
    if ($('form')[0].reportValidity()) {
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