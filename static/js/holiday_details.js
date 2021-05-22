let airports
let today = new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate());

$(document).ready(function () {
    $('#departure_date').removeClass('gj-textbox-md')
    $.get('{% url "airports" holiday.id %}').done(function (data) {
        airports = data.airports
    })
})

$("#departure_date").keydown(function (e) {
    e.preventDefault();
});

$('#airports-list').on('mousedown', 'li', function () {
    $('#departure_airport').val($(this).text())
})

function validateAirport() {
    if ($('#departure_airport').val()) {
        $('#airports-list').toggleClass('d-none')
    }
    if (!airports.includes($('#departure_airport').val())) {
        $('#departure_airport').val('')
    }
}

$('#departure_airport').on('blur', function () {
    validateAirport()
})

$('#departure-airport-container').on('mouseleave', function () {
    validateAirport()
})

$('#departure_airport').on('input click', function () {
    let search = $(this).val()
    let matches = airports.filter(function (airport) {
        let regex = new RegExp(`^${search}`, 'gi')
        return airport.match(regex)
    })
    if (matches.length === 0) {
        $('#airports-list').html('<ul class="list-group"><li class="list-group-item border-0 small">No search results</li></ul>').removeClass('d-none')
    } else if (search.length === 0) {
        matches = []
        $('#airports-list').html('').addClass('d-none')
    } else {
        let html = matches.map(function (match) {
            // Code for substring method is from https://www.w3schools.com/jsref/jsref_substr.asp
            let innerHtml = `<li class="list-group-item border-0 small"><strong>${match.substr(0, search.length)}</strong>`
            innerHtml += `${match.substr(search.length, match.length)}</li>`
            return innerHtml
        }).join('')
        html = `<ul class="list-group shadow rounded-0">${html}</ul>`
        $('#airports-list').html(html).removeClass('d-none')
    }
})

$('#departure_date').datepicker({
    footer: true,
    modal: true,
    minDate: today,
    showRightIcon: false,
    format: 'dd/mm/yyyy'
});

$('.plus').click(function () {
    let currentValue = parseInt($(this).prev().val())
    if (currentValue < 10) {
        $(this).prev().val(currentValue + 1);
    }
});

$('.minus').click(function () {
    let currentValue = parseInt($(this).next().val())
    if (currentValue > 1) {
        $(this).next().val(currentValue - 1);
    }
});

$('#guests').change(function (e) {
    let guests = parseInt($(this).val())
    if (!guests <= 10 || !guests >= 1)
        $(this).val('1')
})