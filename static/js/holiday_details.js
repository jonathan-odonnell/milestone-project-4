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

/* Removes the default datepicker input styling from the departure date input and configures the related
holidays slider when the DOM has finished loading. Code for the related holidays slider is from 
https://kenwheeler.github.io/slick/ */

$(document).ready(function () {
    $('#departure_date').removeClass(
        'gj-textbox-md'
    );
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
                breakpoint: 768,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                },
            },
        ],
        appendArrows: "#arrows",
        prevArrow: `<button type="button" class="btn shadow-0 ps-0">
                <i class="fas fa-arrow-left fa-2x"></i></button>`,
        nextArrow: `<button type="button" class="btn shadow-0 pe-md-0">
                <i class="fas fa-arrow-right fa-2x"></i></button>`,
    });
});

/* Changes the tabs dropdown button text and shows the relevant tab when a button in the tabs dropdown
menu is clicked */

$('#tabs-dropdown')
    .next()
    .find('button')
    .click(function () {
        let tab = $(this).html();
        $('.tab-content .tab-pane').removeClass(
            'show active'
        );
        $(`#${tab}`).addClass("show active");
        $('#tabs-dropdown').html(`${tab}`);
    });

// Prevents the user from being able to manually change the value of the departure date input

$('#departure_date').keydown(function (e) {
    e.preventDefault();
});

/* When the user clicks on an item in the airports list, hides the airports list and sets the selected item
as the value of the departure airport field. Code for the delegate target jQuery is from 
https://api.jquery.com/event.delegateTarget/#event-delegateTarget1 */

$('#airports-list').on(
    'mousedown',
    'li',
    function () {
        $('#departure_airport').val($(this).text());
        $(this).addClass('d-none');
    }
);

/* Hides the airports list and sets the value of the departure airport input to an empty string if the 
current value of the input is not in the airports list. Code for the includes method is from 
https://www.w3schools.com/jsref/jsref_includes_array.asp */

function validateAirport() {
    if ($('#departure_airport').val()) {
        $('#airports-list').addClass('d-none');
    }
    if (
        !airports.includes(
            $('#departure_airport').val()
        )
    ) {
        $('#departure_airport').val('');
    }
}

// Calls the validateAirport function when the departure airport input blurs

$('#departure_airport').on("blur", function () {
    validateAirport();
});

// Calls the validateAirport function when the mouse leaves the departure airport container ID.

$('#departure-airport-container').on(
    'mouseleave',
    function () {
        validateAirport();
    }
);

/* Filters the airports list for matches, shows the airports list ID and adds the relevant HTML 
inside it. Code is from https://www.youtube.com/watch?v=1iysNUrI3lw and 
https://www.w3schools.com/jsref/jsref_substr.asp */

$('#departure_airport').on(
    'input',
    function () {
        let search = $(this).val();
        let matches = airports.filter(function (
            airport
        ) {
            let regex = new RegExp(
                `^${search}`,
                'gi'
            );
            return airport.match(regex);
        });
        if (matches.length === 0) {
            $('#airports-list')
                .html(
                    `<ul class="list-group">
                        <li class="list-group-item border-0 small">No search results</li>
                    </ul>`
                )
                .removeClass("d-none");
        } else if (search.length === 0) {
            matches = [];
            $('#airports-list')
                .html('')
                .addClass('d-none');
        } else {
            let html = matches
                .map(function (match) {
                    let innerHtml = `<li class="list-group-item border-0 small"><strong>${match
                        .substr(0, search.length)}</strong>${match
                        .substr(search.length, match.length)}</li>`;
                    return innerHtml;
                })
                .join('');
            html = `<ul class="list-group shadow rounded-0">${html}</ul>`;
            $('#airports-list')
                .html(html)
                .removeClass('d-none');
        }
    }
);

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
    if (!( guests >= 1 && guests <= 10)) {
        $(this).val(1);
    };
});