function generateStars() {
    let fullStar = '<i class="fas fa-star"></i>'
    let halfStar = '<i class="fas fa-star-half-alt"></i>'
    let emptyStar = '<i class="far fa-star"></i>'
    $('.rating').each(function () {
        rating = parseFloat($(this).html())
        displayStars = ""
        for (let i = 1; i <= 5; i++) {
            if (rating >= i) {
                displayStars += fullStar
            } else if (Math.ceil(rating) === i && !Number.isInteger(rating)) {
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

