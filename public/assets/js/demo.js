/* Demo sites: forms show a thank-you and never send anything. */
(function () {
  "use strict";
  document.querySelectorAll("form[data-demo]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var s = form.querySelector(".d-status");
      if (s) s.textContent = "Thanks! We'll get back to you soon.";
    });
  });
})();
