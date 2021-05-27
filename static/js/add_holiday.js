// Amends the form styling when the DOM has finished loading
$(document).ready(function () {
	$('.btn-file').addClass('mt-2');
	$('.custom-checkbox').addClass('form-check ms-1');
	$('.form-check input').addClass('form-check-input');
	$('.form-check label').addClass('form-check-label');
	$('fieldset .row').addClass('mb-3');
	if (!$('select').val()) {
		$('select').css('color', '#a9a9a9');
	}
});

/* Changes the colour of the select menu when it is changed depending 
on whether a valid option or the blank label has been selected */
$("select").change(function () {
	if (!$(this).val()) {
		$(this).css("color", "#a9a9a9");
	} else {
		$(this).css("color", "#4a4a4a");
	}
});

// Adds the name of the file selected and styling to the filename ID when an image is selected
$('#new-image').change(function () {
	let file = $('#new-image')[0].files[0];
	$('#filename').text(`Image will be set to: ${file.name}`);
	$('#filename').addClass('mt-3');
});

/* Adds the relevant legend text and form styling to the added row when the add another activity 
button is clicked */
let activityCounter = 1;

function addedActivity() {
	$('fieldset .row').addClass('mb-3');
	activityCounter += 1;
	$('.activity').last().find('legend').text(`Activity ${activityCounter}`);
	$('.delete-row').remove();
}

/* Adds the relevant legend text and form styling to the added row when the add another itinerary 
button is clicked */
let itineraryCounter = 1;

function addedItinerary() {
	$('fieldset .row').addClass('mb-3');
	itineraryCounter += 1;
	$('.itinerary').last().find('legend').text(`Itinerary ${itineraryCounter}`);
	$('.delete-row').remove();
}

/* Checks the shown fieldset is valid and shows and hides the relevant fieldsets 
and buttons when the back button is clicked */
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
});

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
});
