/* Sets the start date and end date as the startDate and endDate variables.
Code is from https://gijgo.com/datepicker/configuration/minDate and 
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

/* Changes the tabs dropdown button text and shows the relevant tab when a button in the tabs dropdown
menu is clicked */

$('#tabs-dropdown').next().find('button').click(function () {
    let tab = $(this).html();
    $('.tab-content .tab-pane').removeClass('show active');
    $(`#${tab}`).addClass("show active");
    $('#tabs-dropdown').html(`${tab}`);
});

/* Configures the departure date datepicker. Code is from https://gijgo.com/datepicker/ 
and https://gijgo.com/datepicker/configuration */

$('#departure_date').datepicker({
    footer: true,
    modal: true,
    minDate: startDate,
    maxDate: endDate,
    showRightIcon: false,
    format: 'dd/mm/yyyy',
});

// Removes the default datepicker input styling from the departure date input

$('#departure_date').removeClass('gj-textbox-md');

// Prevents the user from being able to manually change the value of the departure date input

$('#departure_date').keydown(function (e) {
    e.preventDefault();
});

/* Increases the guests field value by 1 when the user clicks the plus button if the guest 
field already has a value less than 10. */

$('.plus').click(function () {
    let currentValue = parseInt(
        $(this).prev().val()
    );
    if (currentValue < 10) {
        $(this)
            .prev()
            .val(currentValue + 1);
    }
});

/* Reduces the guests field value by 1 when the user clicks the minus button if the guest field already
has a value greater than 1. */

$('.minus').click(function () {
    let currentValue = parseInt(
        $(this).next().val()
    );
    if (currentValue > 1) {
        $(this)
            .next()
            .val(currentValue - 1);
    }
});

// Resets the guests field value to 1 if the user enters a value other than a number between 1 and 10

$('#guests').change(function () {
    let guests = parseInt($(this).val());
    if (!(guests >= 1 && guests <= 10)) {
        $(this).val(1);
    }
});

/* Configures the related holidays slider. Code for the related holidays slider is
from https://kenwheeler.github.io/slick/ */

$('#related-holidays').slick({
    infinite: true,
    slidesToShow: 4,
    slidesToScroll: 1,
    responsive: [{
            breakpoint: 1200,
            settings: {
                slidesToShow: 3,
                slidesToScroll: 1,
            },
        },
        {
            breakpoint: 998,
            settings: {
                slidesToShow: 2,
                slidesToScroll: 1,
            },
        },
        {
            breakpoint: 576,
            settings: {
                slidesToShow: 1,
                slidesToScroll: 1,
            },
        },
    ],
    appendArrows: "#arrows",
    prevArrow: `<button type="button" class="btn shadow-0 ps-0 pe-3" aria-label="previous">
            <i class="fas fa-arrow-left fa-2x" aria-hidden="true"></i></button>`,
    nextArrow: `<button type="button" class="btn shadow-0 ps-3 pe-0" aria-label="next">
            <i class="fas fa-arrow-right fa-2x" aria-hidden="true"></i></button>`,
});