// Amends the form styling and removes the delete link when the DOM has finished loading

$(document).ready(function () {
	$('.custom-checkbox').addClass('form-check ms-1');
	$('.form-check input').addClass('form-check-input').attr('type', 'checkbox');
	$('.form-check label').addClass('form-check-label').show();
	$('fieldset .row').addClass('mb-3');
	$('.feature, .activity, .itinerary').each(function () {
		$(this).find('.form-check').last().addClass('delete-check');
	});
	$('.delete-check label').addClass('text-danger');
	$('.delete-row').remove();
	if (!$('select').val()) {
		$('select').css('color', '#a9a9a9');
	}
});

// Adds the name of the file selected and styling to the filename ID when an image is selected

$('#new-image').change(function () {
	var file = $('#new-image')[0].files[0];
	$('#filename').text(`Image will be set to: ${file.name}`);
	$('#filename').addClass('mt-3');
});

/* Adds the relevant legend text, delete checkbox and form styling to the added row when the add another 
activity button is clicked */

let activityCounter = $('.activity').length;

function addedActivity() {
	$('fieldset .row').addClass('mb-3');
	$(`#div_id_activities-${activityCounter}-DELETE`).addClass('form-check ms-1');
	$(`#div_id_activities-${activityCounter}-DELETE`).addClass('delete-check');
	$(`<input type="checkbox" name="activities-${activityCounter}-DELETE" id="id_activities-${activityCounter}
    -DELETE" class="form-check-input">`).insertBefore(`#div_id_activities-${activityCounter}-DELETE label`);
	$(`#div_id_activities-${activityCounter}-DELETE label`).addClass('form-check-label, text-danger').show();
	activityCounter += 1;
	$('.activity').last().find('legend').text(`Activity ${activityCounter}`);
	$('.delete-row').remove();
}

/* Adds the relevant legend text, delete checkbox and form styling to the added row when the add another 
itinerary button is clicked */

let itineraryCounter = $('.itinerary').length;

function addedItinerary() {
	$('fieldset .row').addClass('mb-3');
	$(`#div_id_itineraries-${itineraryCounter}-DELETE`).addClass('form-check delete-check ms-1');
	$(`<input type="checkbox" name="itineraries-${itineraryCounter}-DELETE" id="id_itineraries-${itineraryCounter}
    -DELETE" class="form-check-input">`).insertBefore(`#div_id_itineraries-${itineraryCounter}-DELETE label`);
	$(`#div_id_itineraries-${itineraryCounter}-DELETE label`).addClass('form-check-label, text-danger').show();
	itineraryCounter += 1;
	$('.itinerary').last().find('legend').text(`Itinerary ${itineraryCounter}`);
	$('.delete-row').remove();
}

/* Checks the shown fieldset is valid and shows and hides the relevant fieldsets and buttons when the 
back button is clicked */

$('#next').click(function () {
	if ($('form')[0].reportValidity()) {
		$('fieldset').not('.d-none').next().removeClass('d-none');
		$('fieldset').not('.d-none').first().addClass('d-none');
		if ($('fieldset').not('.d-none').attr('id') === 'package') {
			$('#back').addClass('d-none');
		} else {
			$('#back').removeClass('d-none');
		}
		if ($('fieldset').not('.d-none').attr('id') === 'itineraries') {
			$('#next').addClass('d-none');
			$('button[type="submit"]').removeClass('d-none');
		} else {
			$('button[type="submit"]').addClass('d-none');
			$('#next').removeClass('d-none');
		}
	}
})

// Shows and hides the relevant fieldsets and buttons when the back button is clicked

$('#back').click(function () {
	$('fieldset').not('.d-none').prev().removeClass('d-none');
	$('fieldset').not('.d-none').last().addClass('d-none');
	if ($('fieldset').not('.d-none').attr('id') === 'package') {
		$('#back').addClass('d-none');
	} else {
		$('#back').removeClass('d-none');
	}
	if ($('fieldset').not('.d-none').attr('id') === 'itineraries') {
		$('#next').addClass('d-none');
		$('button[type="submit"]').removeClass('d-none');
	} else {
		$('button[type="submit"]').addClass('d-none');
		$('#next').removeClass('d-none');
	}
})