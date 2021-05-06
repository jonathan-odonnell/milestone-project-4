function generateStars() {
    let fullStar = "<i class='fas fa-star'></i>"
    let halfStar = "<i class='fas fa-star-half-alt'></i>"
    let emptyStar = "<i class='far fa-star'></i>"
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

