/* Updates the currentUrl pathname and page search perameter when a page link is clicked. An AJAX get request
for the filterUrl is then submitted and the HTML inside the holidays ID is replaced with the HTML returned in
the response and the generateStars function is called to generate new star ratings. A new entry is added to the
browser's session history to update the page URL. Code for the delegate target jQuery is from 
https://api.jquery.com/event.delegateTarget/#event-delegateTarget1. */

$('#holidays').on('click', '.page-link', function () {
    let page = $(this).data('page');
    let currentUrl = new URL(window.location);
    /* Code for replacing the URL pathname is from 
    https://stackoverflow.com/questions/61896535/how-to-change-js-url-object-pathname-and-protocol-properties */
    currentUrl.pathname = `${currentUrl.pathname}filter/`;
    currentUrl.searchParams.set('page', page);
    $.get(currentUrl).done(function (data) {
        $('#holidays').html(data.holidays);
        generateStars();
        /* Code for replacing the URL pathname is from 
        https://stackoverflow.com/questions/61896535/how-to-change-js-url-object-pathname-and-protocol-properties */
        currentUrl.pathname = currentUrl.pathname.replace('filter/', '');
        /*  Code for adding a new entry to the browser's session history is from
        https://developer.mozilla.org/en-US/docs/Web/API/History/pushState */
        window.history.pushState({}, '', currentUrl);
    });
});


/* Updates the currentUrl pathname and sort, direction and page search perameters when the value of the sort-selector ID
changes. An AJAX get request for the currentUrl is then submitted and the HTML inside the holidays ID is replaced with the
HTML returned in the response and the generateStars function is called to generate new star ratings. A new entry is added
to the browser's session history to update the page URL. */

$('#sort-selector').change(function () {
    let sortSelector = $(this).val();
    let currentUrl = new URL(window.location);
    /* Code for replacing the URL pathname is from 
    https://stackoverflow.com/questions/61896535/how-to-change-js-url-object-pathname-and-protocol-properties */
    currentUrl.pathname = `${currentUrl.pathname}filter/`;
    currentUrl.searchParams.delete('page');
    if (sortSelector !== 'reset') {
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
        /* Code for replacing the URL pathname is from 
        https://stackoverflow.com/questions/61896535/how-to-change-js-url-object-pathname-and-protocol-properties */
        currentUrl.pathname = currentUrl.pathname.replace('filter/', '');
        /*  Code for adding a new entry to the browser's session history is from
        https://developer.mozilla.org/en-US/docs/Web/API/History/pushState */
        window.history.pushState({}, '', currentUrl);
    });
});

/* Updates the currentUrl pathname and categories and page search perameters when one of the category
filters is toggled on or off. An AJAX get request for the filterUrl is then submitted and the HTML inside
the holidays ID is replaced with the HTML returned in the response and the generateStars function is called
to generate new star ratings. A new entry is added to the browser's session history to update the page URL.
Code for the toggleClass jQuery method is from https://api.jquery.com/toggleClass/#toggleClass1 */

$('#category-filters a').on('click', function () {
    $(this).find('span').toggleClass('bg-primary text-dark');
    let categories = [];
    let currentUrl = new URL(window.location);
    /* Code for replacing the URL pathname is from 
    https://stackoverflow.com/questions/61896535/how-to-change-js-url-object-pathname-and-protocol-properties */
    currentUrl.pathname = `${currentUrl.pathname}filter/`;
    currentUrl.searchParams.delete('page');
    // Code for the each jQuery method is from https://api.jquery.com/each/#each-function
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
        /* Code for replacing the URL pathname is from 
        https://stackoverflow.com/questions/61896535/how-to-change-js-url-object-pathname-and-protocol-properties */
        currentUrl.pathname = currentUrl.pathname.replace('filter/', '');
        /*  Code for adding a new entry to the browser's session history is from
        https://developer.mozilla.org/en-US/docs/Web/API/History/pushState */
        window.history.pushState({}, '', currentUrl);
    });
});

/* Updates the currentUrl pathname and countries and page search perameters when one of the country
filters is toggled on or off. An AJAX get request for the currentUrl is then submitted and the HTML
inside the holidays ID is replaced with the HTML returned in the response and the generateStars function
is called to generate new star ratings. A new entry is added to the browser's session history to update
the page URL. Code for the toggleClass jQuery method is from https://api.jquery.com/toggleClass/#toggleClass1 */

$('#country-filters a').on('click', function () {
    $(this).find('span').toggleClass('bg-primary text-dark');
    let countries = [];
    let currentUrl = new URL(window.location);
    /* Code for replacing the URL pathname is from 
    https://stackoverflow.com/questions/61896535/how-to-change-js-url-object-pathname-and-protocol-properties */
    currentUrl.pathname = `${currentUrl.pathname}filter/`;
    currentUrl.searchParams.delete('page');
    // Code for the each jQuery method is from https://api.jquery.com/each/#each-function
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
        /* Code for replacing the URL pathname is from 
        https://stackoverflow.com/questions/61896535/how-to-change-js-url-object-pathname-and-protocol-properties */
        currentUrl.pathname = currentUrl.pathname.replace('filter/', '');
        /*  Code for adding a new entry to the browser's session history is from
        https://developer.mozilla.org/en-US/docs/Web/API/History/pushState */
        window.history.pushState({}, '', currentUrl);
    });
});