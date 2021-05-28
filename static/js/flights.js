/* Stores start date and end date. Code is from https://gijgo.com/datepicker/configuration/minDate and 
https://gijgo.com/datepicker/configuration/maxDate */
let startDate = new Date(
	new Date().getFullYear(),
	new Date().getMonth(),
	new Date().getDate() + 14
);
let endDate = new Date(
	new Date().getFullYear() + 1,
	new Date().getMonth(),
	new Date().getDate()
);

/* Adds the blank option to the destination time zone input and removes the default datepicker input
 styling from the departure time and arrival time inputs */
$(document).ready(function () {
	$("#div_id_departure_time input").removeClass(
		"gj-textbox-md"
	);
	$("#div_id_arrival_time input").removeClass(
		"gj-textbox-md"
	);
	$("#id_destination_time_zone").prepend(
		'<option value="" selected></option>'
	);
});

/* Configures the departure time datetime picker. Code is from https://gijgo.com/datetimepicker/, 
https://gijgo.com/datepicker/configuration and https://gijgo.com/datetimepicker/configuration */
$("#id_departure_time").datetimepicker({
	footer: true,
	modal: true,
	datepicker: {
		minDate: startDate,
		maxDate: endDate,
		showRightIcon: false,
	},
	format: "dd/mm/yyyy HH:MM",
});

/* Configures the arrival time datetime picker. Code is from https://gijgo.com/datetimepicker/, 
https://gijgo.com/datepicker/configuration and https://gijgo.com/datetimepicker/configuration */
$("#id_arrival_time").datetimepicker({
	footer: true,
	modal: true,
	datepicker: {
		minDate: startDate,
		maxDate: endDate,
		showRightIcon: false,
	},
	format: "dd/mm/yyyy HH:MM",
});

// Prevents the user from being able to enter text in the departure time or arrival time fields.
$(
	"#id_dearture_time, #id_arrival_time"
).keydown(function (e) {
	e.preventDefault();
});