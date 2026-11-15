/* Lee County Websites: shared by every page. Menu, town finder, featured
   carousel, capsule strips, tabs, the contact form and analytics events
   (pushed to the Google Tag Manager dataLayer when GTM is installed). */
(function () {
  "use strict";

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var track = function (name, params) {
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

  /* ---------- Town and service finder ---------- */
  var finder = document.querySelector(".finder");
  if (finder) {
    var input = finder.querySelector("input");
    var opts = Array.prototype.slice.call(finder.querySelectorAll("option")).map(function (o) {
      return { label: o.value, url: o.getAttribute("data-url") };
    });
    var find = function (q) {
      q = (q || "").trim().toLowerCase();
      if (!q) return null;
      for (var i = 0; i < opts.length; i++) if (opts[i].label.toLowerCase() === q) return opts[i];
      for (var j = 0; j < opts.length; j++) if (opts[j].label.toLowerCase().indexOf(q) !== -1) return opts[j];
      return null;
    };
    input.addEventListener("change", function () {
      var hit = find(input.value);
      if (hit && hit.label.toLowerCase() === input.value.trim().toLowerCase()) location.href = hit.url;
    });
    finder.addEventListener("submit", function (e) {
      e.preventDefault();
      var hit = find(input.value);
      location.href = hit ? hit.url : "/areas/";
    });
  }

  /* ---------- Featured carousel ---------- */
  var feat = document.querySelector(".feat");
  if (feat) {
    var ftrack = feat.querySelector(".feat-track");
    var slides = feat.querySelectorAll(".fs");
    var dots = feat.querySelectorAll(".dot");
    var current = 0;
    var go = function (i, user) {
      current = (i + slides.length) % slides.length;
      ftrack.scrollTo({ left: slides[current].offsetLeft - ftrack.offsetLeft, behavior: reduce ? "auto" : "smooth" });
      if (user) stop();
    };
    var mark = function (i) {
      current = i;
      dots.forEach(function (d, j) { if (j === i) d.setAttribute("aria-current", "true"); else d.removeAttribute("aria-current"); });
    };
    feat.querySelector(".feat-arr.prev").addEventListener("click", function () { go(current - 1, true); });
    feat.querySelector(".feat-arr.next").addEventListener("click", function () { go(current + 1, true); });
    dots.forEach(function (d) { d.addEventListener("click", function () { go(+d.getAttribute("data-i"), true); }); });
    var raf = null;
    ftrack.addEventListener("scroll", function () {
      if (raf) return;
      raf = requestAnimationFrame(function () {
        raf = null;
        mark(Math.round(ftrack.scrollLeft / ftrack.clientWidth));
      });
    }, { passive: true });
    ftrack.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); go(current + 1, true); }
      if (e.key === "ArrowLeft") { e.preventDefault(); go(current - 1, true); }
    });
    var timer = null;
    var stop = function () { if (timer) { clearInterval(timer); timer = null; } };
    var start = function () { if (!reduce && !timer) timer = setInterval(function () { go(current + 1); }, 7000); };
    feat.addEventListener("mouseenter", stop);
    feat.addEventListener("mouseleave", start);
    feat.addEventListener("focusin", stop);
    ftrack.addEventListener("touchstart", stop, { passive: true });
    document.addEventListener("visibilitychange", function () { if (document.hidden) stop(); });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) start(); else stop(); }); }).observe(feat);
    } else start();
  }

  /* ---------- Capsule strips ---------- */
  document.querySelectorAll(".strip").forEach(function (s) {
    var t = s.querySelector(".strip-track");
    var by = function (dir) { t.scrollBy({ left: dir * t.clientWidth, behavior: reduce ? "auto" : "smooth" }); };
    var p = s.querySelector(".arr.prev"), n = s.querySelector(".arr.next");
    if (p) p.addEventListener("click", function () { by(-1); });
    if (n) n.addEventListener("click", function () { by(1); });
  });

  /* ---------- Tabs with hover preview ---------- */
  var tabs = document.querySelectorAll(".tabs [role=tab]");
  var select = function (tab) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute("aria-selected", on ? "true" : "false");
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
    });
  };
  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () { select(t); });
    t.addEventListener("keydown", function (e) {
      var k = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
      if (!k) return;
      var nx = tabs[(i + k + tabs.length) % tabs.length];
      select(nx); nx.focus();
    });
  });
  document.querySelectorAll(".tab-panel").forEach(function (panel) {
    var rows = panel.querySelectorAll(".tr");
    var show = function (row) {
      rows.forEach(function (r) { r.classList.toggle("on", r === row); });
      panel.querySelectorAll(".pv").forEach(function (pv) { pv.hidden = pv.id !== "pv-" + row.getAttribute("data-pv"); });
    };
    rows.forEach(function (r) {
      r.addEventListener("mouseenter", function () { show(r); });
      r.addEventListener("focus", function () { show(r); });
    });
    if (rows[0]) show(rows[0]);
  });

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
        form.reset();
        if (pageField) pageField.value = location.pathname;
        setStatus("Got it. I'll reply within a business day.", "ok");
        track("generate_lead", { form_id: "contact", page_path: location.pathname });
      })
      .catch(function () {
        setStatus("That didn't go through. " + (form.getAttribute("data-fallback") || "Please try again in a few minutes."), "error");
        track("form_error", { form_id: "contact" });
      })
      .finally(function () { submitBtn.disabled = false; });
  });
})();
