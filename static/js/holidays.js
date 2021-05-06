// jQuery for each function is from https://stackoverflow.com/questions/17258119/jquery-each-run-function-for-each-instance-of-selector
let currentUrl = new URL(window.location)

$('#holidays').on('click', '.page-link', function () {
    currentUrl.searchParams.set("page", parseInt($(this).closest('a').text()));
    $.get(currentUrl).done(function (data) {
        $('#holidays').html(data.holidays)
        generateStars()
    })
})

$('#sort-selector').change(function () {
    let sortSelector = $(this).val();
    currentUrl.searchParams.set("page", 1);
    if (sortSelector !== 'featured') {
        let sort = sortSelector.split("_")[0];
        let direction = sortSelector.split("_")[1];
        currentUrl.searchParams.set("sort", sort);
        currentUrl.searchParams.set("direction", direction);
    } else {
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");
    }
    $.get(currentUrl).done(function (data) {
        $('#holidays').html(data.holidays)
        generateStars()
    })
})

$('#category-filters a').on('click', function () {
    $(this).find('span').toggleClass('bg-primary text-dark');
    let categories = []
    currentUrl.searchParams.set("page", 1);
    $('#category-filters').find('.bg-primary').each(function () {
        categories.push($(this).text().toLowerCase().replace(' ', '_'))
    })
    if (categories.length > 0) {
        categories = categories.join(',')
        currentUrl.searchParams.set("categories", categories)
    } else {
        currentUrl.searchParams.delete("categories");
    }
    $.get(currentUrl).done(function (data) {
        $('#holidays').html(data.holidays)
        generateStars()
    })
})

$('#country-filters a').on('click', function () {
    $(this).find('span').toggleClass('bg-primary text-dark');
    let countries = []
    currentUrl.searchParams.set("page", 1);
    $('#country-filters').find('.bg-primary').each(function () {
        countries.push($(this).text().toLowerCase().replace(' ', '_'))
    })
    if (countries.length > 0) {
        countries = countries.join(',')
        currentUrl.searchParams.set("countries", countries)
    } else {
        currentUrl.searchParams.delete("countries");
    }
    $.get(currentUrl).done(function (data) {
        $('#holidays').html(data.holidays)
        generateStars()
    })
})