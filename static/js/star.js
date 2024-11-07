document.addEventListener("DOMContentLoaded", function() {
    const stars = document.querySelectorAll(".star");
    const rateInput = document.getElementById("rate-value");

    stars.forEach(star => {
        star.addEventListener("click", function() {
            const rating = this.getAttribute("data-value");
            rateInput.value = rating;

            stars.forEach(s => {
                s.style.color = s.getAttribute("data-value") <= rating ? "gold" : "black";
            });
        });
    });
});