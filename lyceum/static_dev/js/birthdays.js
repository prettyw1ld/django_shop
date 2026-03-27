(function () {
    const serverBanner = document.getElementById("server-birthday-banner");
    if (serverBanner) serverBanner.style.display = "none";
    
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