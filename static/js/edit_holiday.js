$(document).ready(function () {
    $('.btn-file').addClass('mt-2')
    $('.custom-checkbox').addClass('form-check ms-1')
    $('.form-check input').addClass('form-check-input').attr('type', 'checkbox')
    $('.form-check label').addClass('form-check-label').show()
    $('fieldset .row').addClass('mb-3')
    $('.feature, .activity, .itinerary').each(function () {
        $(this).find('.form-check').last().addClass('delete-check')
    })
    $('.delete-check label').addClass('text-danger')
})
$('#new-image').change(function () {
    var file = $('#new-image')[0].files[0];
    $('#filename').text(`Image will be set to: ${file.name}`);
    $('#filename').addClass('mt-3');
});
activityCounter = $('.activity').length
let addedActivity = function () {
    $('fieldset .row').addClass('mb-3');
    $(`#div_id_activities-${activityCounter}-DELETE`).addClass('form-check ms-1')
    $(`#div_id_activities-${activityCounter}-DELETE`).addClass('delete-check')
    $(`<input type="checkbox" name="activities-${activityCounter}-DELETE" id="id_activities-${activityCounter}-DELETE" class="form-check-input">`).insertBefore(`#div_id_activities-${activityCounter}-DELETE label`)
    $(`#div_id_activities-${activityCounter}-DELETE label`).addClass('form-check-label, text-danger').show()
    activityCounter += 1
    $('.activity').last().find('legend').text(`Activity ${activityCounter}`)
}
itineraryCounter = $('.itinerary').length
let addedItinerary = function () {
    $('fieldset .row').addClass('mb-3');
    $(`#div_id_itineraries-${itineraryCounter}-DELETE`).addClass('form-check delete-check ms-1')
    $(`<input type="checkbox" name="itineraries-${itineraryCounter}-DELETE" id="id_itineraries-${itineraryCounter}-DELETE" class="form-check-input">`).insertBefore(`#div_id_itineraries-${itineraryCounter}-DELETE label`)
    $(`#div_id_itineraries-${itineraryCounter}-DELETE label`).addClass('form-check-label, text-danger').show()
    itineraryCounter += 1
    $('.itinerary').last().find('legend').text(`Itinerary ${itineraryCounter}`)
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