// Generates HTML for the star ratings based on the value inside the rating class
function generateStars() {
    let fullStar = '<i class="fas fa-star" aria-hidden="true"></i>'
    let halfStar = '<i class="fas fa-star-half-alt" aria-hidden="true"></i>'
    let emptyStar = '<i class="far fa-star" aria-hidden="true"></i>'
    $('.rating').each(function () {
        rating = parseFloat($(this).html());
        displayStars = "";
        for (let i = 1; i <= 5; i++) {
            if (rating >= i) {
                displayStars += fullStar;
            } else if (Math.ceil(rating) === i && !Number.isInteger(rating)) {
                displayStars += halfStar;
            } else {
                displayStars += emptyStar;
            }
        }
        $(this).html(displayStars);
    });
}

// Calls the generateStars function when the DOM has finished loading
$(document).ready(function () {
    generateStars();
});