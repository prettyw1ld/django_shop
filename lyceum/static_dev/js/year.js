(function () {
var el = document.getElementById("year");
if (!el) return;
var serverMs = Date.parse("{% now 'c' %}");
var clientMs = Date.now();
if (Math.abs(serverMs - clientMs) <= 24 * 60 * 60 * 1000) {
    el.textContent = "© " + new Date(clientMs).getFullYear();
}
})();