(function () {
    const now = new Date();
    const todayMonth = now.getMonth() + 1;
    const todayDay = now.getDate();
    
    const slides = [...document.querySelectorAll(".birthday-slide")].filter(el => {
        return (
            parseInt(el.dataset.month) === todayMonth &&
            parseInt(el.dataset.day) === todayDay
        );
    });

    if (slides.length === 0) return

    let current = 0;
    slides[current].style.display = "block";

    setInterval(() => {
        slides[current].style.display = "none";
        current = (current + 1) % slides.length;
        slides[current].style.display = "block";
    }, 10000);
})();