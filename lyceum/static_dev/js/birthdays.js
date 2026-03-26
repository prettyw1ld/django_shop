const slides = document.querySelectorAll(".birthday-slide");
let current = 0;
slides[current].style.display = "block";

setInterval(() => {
    slides[current].style.display = "none";
    current = (current + 1) % slides.length;
    slides[current].style.display = "block";
}, 10000);