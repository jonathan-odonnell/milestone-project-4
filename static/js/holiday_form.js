// Amends the form styling and removes the delete link

$(document).ready(function() {
	$('.custom-checkbox').addClass('form-check');
	$('.form-check input').addClass('form-check-input').attr('type', 'checkbox');
	$('.form-check label').addClass('form-check-label').show();
	$('fieldset .row').addClass('mb-3');
	$('.feature, .activity, .itinerary').each(function () {
		$(this).find('.form-check').last().addClass('delete-check');
	});
	$('.delete-check label').addClass('text-danger');
	$('.delete-row').remove();
})

// Adds the name of the file selected and styling to the filename ID when an image is selected

$('#new-image').change(function () {
	let file = $('#new-image')[0].files[0];
	$('#filename').text(`Image will be set to: ${file.name}`);
});

/* Adds the relevant legend text and styling to the added row when the add another 
button is clicked in the activities section of the add holiday form */

let activityCounter = $('.activity').length;

function addActivity() {
	$('fieldset .row').addClass('mb-3');
	activityCounter += 1;
	$('.activity').last().find('legend').text(`Activity ${activityCounter}`);
	$('.delete-row').remove();
}

/* Adds the relevant legend text, delete checkbox and styling to the added row when the add another
button is clicked in the activities section of the edit holiday form */

function editActivity() {
	$('fieldset .row').addClass('mb-3');
	$(`#div_id_activities-${activityCounter}-DELETE`).addClass('form-check');
	$(`#div_id_activities-${activityCounter}-DELETE`).addClass('delete-check');
	$(`<input type="checkbox" name="activities-${activityCounter}-DELETE" id="id_activities-${activityCounter}
    -DELETE" class="form-check-input">`).insertBefore(`#div_id_activities-${activityCounter}-DELETE label`);
	$(`#div_id_activities-${activityCounter}-DELETE label`).addClass('form-check-label, text-danger').show();
	activityCounter += 1;
	$('.activity').last().find('legend').text(`Activity ${activityCounter}`);
	$('.delete-row').remove();
}

/* Adds the relevant legend text and styling to the added row when the add another 
button is clicked in the itineraries section of the add holiday form */

let itineraryCounter = $('.itinerary').length;

function addItinerary() {
	$('fieldset .row').addClass('mb-3');
	itineraryCounter += 1;
	$('.itinerary').last().find('legend').text(`Itinerary ${itineraryCounter}`);
	$('.delete-row').remove();
}

/* Adds the relevant legend text, delete checkbox and styling to the added row when the add another
button is clicked in the itineraries section of the edit holiday form */

function editItinerary() {
	$('fieldset .row').addClass('mb-3');
	$(`#div_id_itineraries-${itineraryCounter}-DELETE`).addClass('form-check delete-check');
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