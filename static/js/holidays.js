/* Updates the page search perameter in the currentUrl when a page link is clicked
and replaces the currentUrl pathname to get the filterUrl. An AJAX get request for
the filterUrl is then submitted and the HTML inside the holidays ID is replaced with
the HTML returned in the response and the generateStars function is called to generate
new star ratings. The currentUrl is added to the browser's session history to update
the page's URL. Code for the delegate target jQuery is from 
https://api.jquery.com/event.delegateTarget/#event-delegateTarget1, code for updating the URL's
pathname is from https://developer.mozilla.org/en-US/docs/Web/API/URL/pathname 
and code for adding a new entry to the browser's session history is from
https://developer.mozilla.org/en-US/docs/Web/API/History/pushState */

$('#holidays').on('click', '.page-link', function () {
    let page = $(this).data('page');
    let currentUrl = new URL(window.location);
    currentUrl.searchParams.set('page', page);
    let filterUrl = new URL(currentUrl)
    filterUrl.pathname = filterUrl.pathname.replace('holidays', 'holidays/filter')
    $.get(filterUrl).done(function (data) {
        $('#holidays').html(data.holidays);
        generateStars();
        window.history.pushState({}, '', currentUrl);
    });
});

/* Updates the currentUrl pathname and sort, direction and page search perameters
when the value of the sort-selector ID changes and replaces the currentUrl pathname
to get the filterUrl. An AJAX get request for the filterUrl is then submitted and the
HTML inside the holidays ID is replaced with the HTML returned in the response and
the generateStars function is called to generate new star ratings. The currentUrl is
added to the browser's session history to update the page's URL. Code for updating the
URL's pathname is from https://developer.mozilla.org/en-US/docs/Web/API/URL/pathname 
and code for adding a new entry to the browser's session history is from
https://developer.mozilla.org/en-US/docs/Web/API/History/pushState */

$('#sort-selector').change(function () {
    let sortSelector = $(this).val();
    let currentUrl = new URL(window.location);
    currentUrl.searchParams.delete('page');
    if (sortSelector !== 'reset') {
        let sort = sortSelector.split("_")[0];
        let direction = sortSelector.split("_")[1];
        currentUrl.searchParams.set('sort', sort);
        currentUrl.searchParams.set('direction', direction);
    } else {
        currentUrl.searchParams.delete('sort');
        currentUrl.searchParams.delete('direction');
    };
    let filterUrl = new URL(currentUrl)
    filterUrl.pathname = filterUrl.pathname.replace('holidays', 'holidays/filter')
    $.get(filterUrl).done(function (data) {
        $('#holidays').html(data.holidays);
        generateStars();
        window.history.pushState({}, '', currentUrl);
    });
});

/* Updates the categories and page search perameters in the currentUrl when one of the category
filters is toggled on or off and replaces the currentUrl pathname to get the filterUrl. An AJAX
get request for the filterUrl is then submitted and the HTML inside the holidays ID is replaced
with the HTML returned in the response and the generateStars function is called to generate new
star ratings. The currentUrl is added to the browser's session history to update the page's URL.
Code for the toggleClass jQuery method is from https://api.jquery.com/toggleClass/#toggleClass1,
code for the each jQuery method is from https://api.jquery.com/each/#each-function, code for
updating the URL's pathname is from https://developer.mozilla.org/en-US/docs/Web/API/URL/pathname 
and code for adding a new entry to the  browser's session history is from
https://developer.mozilla.org/en-US/docs/Web/API/History/pushState */

$('#category-filters a').on('click', function () {
    $(this).find('span').toggleClass('bg-primary text-black');
    let categories = [];
    let currentUrl = new URL(window.location);
    currentUrl.searchParams.delete('page');
    $('#category-filters').find('.bg-primary').each(function () {
        categories.push($(this).text().toLowerCase().replace(' ', '_'));
    });
    if (categories.length > 0) {
        categories = categories.join(',');
        currentUrl.searchParams.set('categories', categories);
    } else {
        currentUrl.searchParams.delete('categories');
    };
    let filterUrl = new URL(currentUrl)
    filterUrl.pathname = filterUrl.pathname.replace('holidays', 'holidays/filter')
    $.get(filterUrl).done(function (data) {
        $('#holidays').html(data.holidays);
        generateStars();
        window.history.pushState({}, '', currentUrl);
    });
});

/* Updates the countries and page search perameters in the currentUrl when one of the country
filters is toggled on or off and replaces the currentUrl pathname to get the filterUrl. An AJAX
get request for the filterUrl is then submitted and the HTML inside the holidays ID is replaced
with the HTML returned in the response and the generateStars function is called to generate new
star ratings. The currentUrl is added to the browser's session history to update the page's URL.
Code for the toggleClass jQuery method is from https://api.jquery.com/toggleClass/#toggleClass1,
code for the each jQuery method is from https://api.jquery.com/each/#each-function, code for
updating the URL's pathname is from https://developer.mozilla.org/en-US/docs/Web/API/URL/pathname 
and code for adding a new entry to the  browser's session history is from
https://developer.mozilla.org/en-US/docs/Web/API/History/pushState */

$('#country-filters a').on('click', function () {
    $(this).find('span').toggleClass('bg-primary text-black');
    let countries = [];
    let currentUrl = new URL(window.location);
    currentUrl.searchParams.delete('page');
    $('#country-filters').find('.bg-primary').each(function () {
        countries.push($(this).text().toLowerCase().replace(' ', '_'));
    });
    if (countries.length > 0) {
        countries = countries.join(',');
        currentUrl.searchParams.set('countries', countries);
    } else {
        currentUrl.searchParams.delete('countries');
    };
    let filterUrl = new URL(currentUrl)
    filterUrl.pathname = filterUrl.pathname.replace('holidays', 'holidays/filter')
    $.get(filterUrl).done(function (data) {
        $('#holidays').html(data.holidays);
        generateStars();
        window.history.pushState({}, '', currentUrl);
    });
});