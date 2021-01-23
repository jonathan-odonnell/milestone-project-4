// jQuery for each function is from https://stackoverflow.com/questions/17258119/jquery-each-run-function-for-each-instance-of-selector
function generateStars() {
    let fullStar = "<i class='fas fa-star pe-1'></i>"
    let halfStar = "<i class='fas fa-star-half-alt pe-1'></i>"
    let emptyStar = "<i class='far fa-star pe-1'></i>"
    $('.rating').each(function () {
        rating = parseFloat($(this).html())
        displayStars = ""
        for (let i = 1; i <= 5; i++) {
            if (Math.round(rating) >= i) {
                displayStars += fullStar
            } else if (rating >= i - 1) {
                displayStars += halfStar
            } else {
                displayStars += emptyStar
            }
        }
        $(this).html(displayStars)
    })
}

$(document).ready(function () {
    generateStars()
})

let currentUrl = window.location
let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
let postData = {
    csrfmiddlewaretoken: csrfToken,
}

$('#sort-selector').change(function () {
    let sortSelector = $(this).val();
    if (sortSelector !== 'featured') {
        let sort = sortSelector.split("_")[0];
        let direction = sortSelector.split("_")[1];
        postData["sort"] = sort;
        postData["direction"] = direction;
    } else {
        delete postData["sort", "direction"]
    }
    $.post(currentUrl, postData).done(function (data) {
        $('#holidays').html(data)
        generateStars()
    })
})

$('#category-filters a').on('click', function () {
    $(this).find('span').toggleClass('bg-primary text-dark');
    let filters = []
    $('#category-filters').find('.bg-primary').each(function () {
        filters.push($(this).text().toLowerCase().replace(' ', '_'))
    })
    if (filters.length > 0) {
        filters = filters.join(',')
        postData["category"] = filters;
    } else {
        delete postData["category"];
    }
    $.post(currentUrl, postData).done(function (data) {
        $('#holidays').html(data)
        generateStars()
    })
})

$('#country-filters a').on('click', function () {
    $(this).find('span').toggleClass('bg-primary text-dark');
    let filters = []
    $('#country-filters').find('.bg-primary').each(function () {
        filters.push($(this).text().toLowerCase().replace(' ', '_'))
    })
    if (filters.length > 0) {
        filters = filters.join(',')
        postData["country"] = filters;
    } else {
        delete postData["country"];
    }
    $.post(currentUrl, postData).done(function (data) {
        $('#holidays').html(data)
        generateStars()
    })
})