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

function pagination(data) {
    let nextPage = postData['page'] + 1
    let prevPage = postData['page'] - 1
    let currentPage = postData['page']
    let totalPages = data.pages
    $('.pagination').html('')
    if (totalPages > 1) {
        if (prevPage > 0) {
            $('.pagination').append(`<li class="page-item"><a class="page-link" href="javascript:void(0)" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span></a></li><li class="page-item"><a class="page-link" href="javascript:void(0)">${prevPage}</a></li>`)
        } else {
            $('.pagination').append(`<li class="page-item disabled"><a class="page-link" href="javascript:void(0)" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span></a></li>`)
        }
        $('.pagination').append(`<li class="page-item active"><a class="page-link" href="javascript:void(0)">${currentPage}</a></li>`)
        if (nextPage <= totalPages) {
            $('.pagination').append(`<li class="page-item"><a class="page-link" href="javascript:void(0)">${nextPage}</a></li><li class="page-item"><a class="page-link" href="javascript:void(0)" aria-label="Next">
                <span aria-hidden="true">&raquo;</span></a></li>`)
        } else {
            $('.pagination').append(`<li class="page-item disabled"><a class="page-link" href="javascript:void(0)" aria-label="Next">
                <span aria-hidden="true">&raquo;</span></a></li>`)
        }
    }
}

$(document).ready(function () {
    generateStars()
})

let currentUrl = window.location
let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

let postData = {
    csrfmiddlewaretoken: csrfToken,
    page: 1,
}

$('body').delegate('.page-link', 'click', function () {
    postData['page'] = parseInt($(this).closest('a').text())
    $.post(currentUrl, postData).done(function (data) {
        let nextPage = postData['page'] + 1
        let prevPage = postData['page'] - 1
        let currentPage = postData['page']
        let totalPages = data.pages
        $('#holidays').html(data.holidays)
        generateStars()
        pagination(data)
    })
})

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
        $('#holidays').html(data.holidays)
        generateStars()
        pagination(data)
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
        $('#holidays').html(data.holidays)
        generateStars()
        pagination(data)
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
        $('#holidays').html(data.holidays)
        generateStars()
        pagination(data)
    })
})