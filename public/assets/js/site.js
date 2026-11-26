/* Lee County Websites: shared by every page. Mobile menu, the contact form
   and analytics events (pushed to the Google Tag Manager dataLayer when GTM
   is installed). */
(function () {
  "use strict";

  // With gtag.js on the page (no GTM), events go to GA4 through gtag(), since
  // GA4 ignores plain dataLayer objects. With GTM, they go on the dataLayer
  // for a Custom Event trigger to pick up.
  var track = function (name, params) {
    var hasGtm = !!document.querySelector("script[src*='googletagmanager.com/gtm.js']");
    if (!hasGtm && typeof window.gtag === "function") {
      window.gtag("event", name, params || {});
      return;
    }
    var ev = { event: name };
    for (var k in params || {}) ev[k] = params[k];
    (window.dataLayer = window.dataLayer || []).push(ev);
  };

  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  /* ---------- Mobile menu ---------- */
  var menuBtn = document.querySelector(".gh-menu");
  var nav = document.getElementById("gh-nav");
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      var open = menuBtn.getAttribute("aria-expanded") === "true";
      menuBtn.setAttribute("aria-expanded", open ? "false" : "true");
      nav.classList.toggle("open", !open);
    });
  }

  /* ---------- Clicks worth counting ---------- */
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a");
    if (!a) return;
    var href = a.getAttribute("href") || "";
    if (href.indexOf("mailto:") === 0) track("click_email", { page_path: location.pathname });
    else if (href.indexOf("/contact/") === 0) track("click_contact", { page_path: location.pathname, link_text: (a.textContent || "").trim().slice(0, 40) });
  });

  /* ---------- Contact form ---------- */
  var form = document.getElementById("contact-form");
  if (!form) return;
  var statusEl = document.getElementById("form-status");
  var submitBtn = document.getElementById("cf-submit");
  var msgEl = document.getElementById("cf-msg");
  var setStatus = function (msg, kind) {
    statusEl.textContent = msg;
    statusEl.className = "form-status" + (kind ? " is-" + kind : "");
  };
  try {
    var topic = new URLSearchParams(location.search).get("topic");
    if (topic && msgEl && !msgEl.value) msgEl.value = "I'm interested in: " + topic.slice(0, 80) + "\n\n";
  } catch (err) { /* old browser */ }
  var pageField = form.querySelector("input[name='page']");
  if (pageField) pageField.value = location.pathname;
  var started = false;
  form.addEventListener("input", function () {
    if (!started) { started = true; track("form_start", { form_id: "contact", page_path: location.pathname }); }
  });
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var firstBad = null;
    form.querySelectorAll("[required]").forEach(function (f) {
      var v = f.value.trim();
      var bad = !v || (f.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v));
      f.setAttribute("aria-invalid", bad ? "true" : "false");
      if (bad && !firstBad) firstBad = f;
    });
    if (firstBad) {
      setStatus("I need your name, an email I can reply to, and a line about the project.", "error");
      firstBad.focus();
      return;
    }
    var data = {};
    new FormData(form).forEach(function (v, k) { v = String(v); data[k] = data[k] ? data[k] + ", " + v : v; });
    submitBtn.disabled = true;
    setStatus("Sending…");
    fetch("/api/contact", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) })
      .then(function (res) {
        if (!res.ok) throw new Error(String(res.status));
        return res.json().catch(function () { return {}; });
      })
      .then(function (body) {
        form.reset();
        if (pageField) pageField.value = location.pathname;
        setStatus("Got it. I'll reply within a business day.", "ok");
        // Count a lead only when the email to Dan actually went out
        // (the server answers sent: true), never for honeypot drops.
        if (body && body.sent) track("generate_lead", { form_id: "contact", page_path: location.pathname });
      })
      .catch(function () {
        setStatus("That didn't go through. " + (form.getAttribute("data-fallback") || "Please try again in a few minutes."), "error");
        track("form_error", { form_id: "contact" });
      })
      .finally(function () { submitBtn.disabled = false; });
  });
})();
