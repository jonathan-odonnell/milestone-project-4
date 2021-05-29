// Sets the page's URL as the currentUrl variable.

let currentUrl = new URL(window.location);

/* Updates the page search perameter in the currentUrl variable when a page link is clicked. 
An AJAX get request for the URL is then submitted and the HTML inside the holidays ID is replaced
with the HTML returned in the response and the generateStars function is called to generate new star
ratings. Code for the delegate target jQuery is from
https://api.jquery.com/event.delegateTarget/#event-delegateTarget1 */

$('#holidays').on('click', '.page-link', function () {
    let page = $(this).data('page');
    currentUrl.searchParams.set('page', page);
    $.get(currentUrl).done(function (data) {
        $('#holidays').html(data.holidays);
        generateStars();
    });
});


/* Updates the sort, direction and page search perameters in the currentUrl variable when the value of 
the sort-selector ID changes. An AJAX get request for the URL is then submitted and the HTML inside the
holidays ID is replaced with the HTML returned in the response and the generateStars function is called
to generate new star ratings. */

$('#sort-selector').change(function () {
    let sortSelector = $(this).val();
    currentUrl.searchParams.set('page', 1);
    if (sortSelector !== 'featured') {
        let sort = sortSelector.split("_")[0];
        let direction = sortSelector.split("_")[1];
        currentUrl.searchParams.set('sort', sort);
        currentUrl.searchParams.set('direction', direction);
    } else {
        currentUrl.searchParams.delete('sort');
        currentUrl.searchParams.delete('direction');
    }
    $.get(currentUrl).done(function (data) {
        $('#holidays').html(data.holidays);
        generateStars();
    });
});

/* Updates the categories and page search perameters in the currentUrl variable when one of the category
filters is toggled on or off. An AJAX get request for the URL is then submitted and the HTML inside the
holidays ID is replaced with the HTML returned in the response and the generateStars function is called
to generate new star ratings. Code for the toggleClass jQuery method is from 
https://api.jquery.com/toggleClass/#toggleClass1 */

$('#category-filters a').on('click', function () {
    $(this).find('span').toggleClass('bg-primary text-dark');
    let categories = [];
    currentUrl.searchParams.set('page', 1);
    $('#category-filters').find('.bg-primary').each(function () {
        categories.push($(this).text().toLowerCase().replace(' ', '_'));
    });
    if (categories.length > 0) {
        categories = categories.join(',');
        currentUrl.searchParams.set('categories', categories);
    } else {
        currentUrl.searchParams.delete('categories');
    }
    $.get(currentUrl).done(function (data) {
        $('#holidays').html(data.holidays);
        generateStars();
    });
});

/* Updates the countries and page search perameters in the currentUrl variable when one of the coountry
filters is toggled on or off. An AJAX get request for the URL is then submitted and the HTML inside the
holidays ID is replaced with the HTML returned in the response and the generateStars function is called
to generate new star ratings. Code for the toggleClass jQuery method is from 
https://api.jquery.com/toggleClass/#toggleClass1 */

$('#country-filters a').on('click', function () {
    $(this).find('span').toggleClass('bg-primary text-dark');
    let countries = [];
    currentUrl.searchParams.set('page', 1);
    $('#country-filters').find('.bg-primary').each(function () {
        countries.push($(this).text().toLowerCase().replace(' ', '_'));
    });
    if (countries.length > 0) {
        countries = countries.join(',');
        currentUrl.searchParams.set('countries', countries);
    } else {
        currentUrl.searchParams.delete('countries');
    }
    $.get(currentUrl).done(function (data) {
        $('#holidays').html(data.holidays);
        generateStars();
    });
});