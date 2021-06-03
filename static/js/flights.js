/* Updates the currentUrl pathname and the sort, direction and page search perameters when the
value of the flight-sort-selector ID changes. An AJAX get request for the currentUrl is then
submitted and the HTML inside the flights-table ID is replaced with the HTML returned. A new
entry is added to the browser's session history to update the page URL. Code for adding a new entry 
to the browser's session history is from 
https://developer.mozilla.org/en-US/docs/Web/API/History/pushState */
$('#flight-sort-selector').change(function () {
    let sortSelector = $(this).val();
    let currentUrl = new URL(window.location);
    currentUrl.searchParams.delete("page");
    if (sortSelector !== "reset") {
        let sort = sortSelector.split("_")[0];
        let direction = sortSelector.split("_")[1];

        currentUrl.searchParams.set("sort", sort);
        currentUrl.searchParams.set("direction", direction);
        currentUrl.searchParams.delete("page");
    } else {
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");
    }
    $.get(currentUrl).done(function (data) {
        $('#flights-table').html(data.flights);
        window.history.pushState({}, '', currentUrl);
    });
});

/* Updates the currentUrl pathname and page search perameter when a page link is clicked. 
An AJAX get request for the currentUrl is then submitted and the HTML inside the flights-table
ID is replaced with the HTML returned. A new entry is added to the browser's session history 
to update the page URL. Code for the delegate target jQuery is from 
https://api.jquery.com/event.delegateTarget/#event-delegateTarget1 and code for adding a new entry
to the browser's session history is from 
https://developer.mozilla.org/en-US/docs/Web/API/History/pushState */
$('#flights-table').on('click', '.page-link', function () {
    let page = $(this).data('page');
    let currentUrl = new URL(window.location);
    currentUrl.searchParams.set("page", page);
    $.get(currentUrl).done(function (data) {
        $('#flights-table').html(data.flights);
        window.history.pushState({}, '', currentUrl);
    });
});