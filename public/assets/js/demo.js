/* Sample demo sites: forms are for show and never send anything. */
(function () {
  "use strict";
  document.querySelectorAll("form[data-demo]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var s = form.querySelector(".d-status");
      if (s) s.textContent = "This is a sample design, so nothing was sent. On a real site this goes straight to the owner's inbox.";
    });
  });
})();
