/* AI search readiness checker. Generated from src/page.html in the ai-search-checker project. */
(function () {
  "use strict";
  var CFG = window.AI_CHECK_CONFIG || {};
  var BRANDS = {
    ss: { name: "Sand And Serifs", contact: "https://sandandserifs.com/contact/", town: "Webster", owner: "Daniel", area: "Rochester-area" },
    lcw: { name: "Lee County Websites", contact: "https://leecountywebsites.com/contact/", town: "Cape Coral", owner: "Daniel", area: "Lee County" }
  };
  var demo = CFG.mode === "demo";
  var brandId = CFG.brand || "ss";
  var root = document.documentElement;
  var $ = function (id) { return document.getElementById(id); };
  var form = $("ac-form"), urlIn = $("ac-url"), townIn = $("ac-town"), msg = $("ac-msg"), prog = $("ac-progress"), out = $("ac-result");
  var lastReport = null;

  function brand() { return Object.assign({}, BRANDS[brandId] || BRANDS.ss, (CFG.brands || {})[brandId] || {}); }
  function setBrand(id) {
    brandId = BRANDS[id] ? id : "ss";
    if (brandId === "lcw") $("ac").setAttribute("data-brand", "lcw"); else $("ac").removeAttribute("data-brand");
    $("ac-brandname").textContent = brand().name;
    townIn.placeholder = brand().town;
    document.querySelectorAll("#ac-brandbar button").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.brand === brandId)); });
    if (lastReport) render(lastReport, true);
  }

  // Tiny element builder: text always goes in as textContent, so nothing from a scanned site can inject markup.
  function h(tag, attrs, kids) {
    var el = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === "class") el.className = attrs[k].split(" ").map(function (c) { return "ac-" + c; }).join(" ");
      else if (k === "text") el.textContent = attrs[k];
      else if (attrs[k] != null) el.setAttribute(k, attrs[k]);
    });
    (kids || []).forEach(function (c) { if (c != null) el.appendChild(typeof c === "string" ? document.createTextNode(c) : c); });
    return el;
  }

  var STATUS = { pass: "Good", warn: "Improve", fail: "Fix", check: "Check", info: "FYI" };

  function showMsg(text, isErr) { msg.textContent = text; msg.className = "ac-msg" + (isErr ? " ac-err" : ""); msg.hidden = !text; }

  function runProgress() {
    prog.hidden = false;
    var steps = prog.querySelectorAll("div"), i = 0;
    steps.forEach(function (s) { s.className = ""; });
    steps[0].className = "ac-on";
    var t = setInterval(function () {
      if (i < steps.length - 1) { steps[i].className = "ac-done"; i++; steps[i].className = "ac-on"; }
    }, 900);
    return function () { clearInterval(t); prog.hidden = true; };
  }

  function hostOf(raw) {
    var s = String(raw || "").trim();
    if (!/^[a-z][a-z0-9+.-]*:\/\//i.test(s)) s = "https://" + s;
    try { return new URL(s).hostname.toLowerCase().replace(/^www\./, ""); } catch (e) { return ""; }
  }

  function check(rawUrl, town) {
    showMsg("");
    if (!String(rawUrl || "").trim()) { showMsg("Enter your website address, like yourbusiness.com.", true); urlIn.focus(); return; }
    out.hidden = true;
    var stop = runProgress();
    $("ac-go").disabled = true;
    var done = function () { stop(); $("ac-go").disabled = false; };

    if (demo) {
      var host = hostOf(rawUrl);
      var rep = (CFG.reports || {})[host];
      setTimeout(function () {
        done();
        if (!rep) { showMsg("This preview can't reach the internet, so it only has saved results for the sample sites below. The live version on your site will scan any address."); return; }
        render(rep);
      }, 1700);
      return;
    }

    var api = (CFG.apiUrl || "/api/ai-check") + "?url=" + encodeURIComponent(rawUrl) + (town ? "&town=" + encodeURIComponent(town) : "");
    fetch(api, { headers: { "X-Requested-With": "ai-check" } })
      .then(function (r) { return r.json().catch(function () { return { ok: false, error: "The checker didn't answer properly. Please try again." }; }); })
      .then(function (data) {
        done();
        if (!data.ok) { showMsg(data.error || "Something went wrong. Please try again.", true); return; }
        render(data.report);
        try {
          var q = new URLSearchParams({ url: data.report.site.host });
          if (town) q.set("town", town);
          history.replaceState(null, "", location.pathname + "?" + q.toString());
        } catch (e) {}
        if (window.dataLayer) window.dataLayer.push({ event: "ai_check", ai_check_score: data.report.score });
        if (window.gtag) window.gtag("event", "ai_check", { score: data.report.score });
      })
      .catch(function () { done(); showMsg("We couldn't run the check just now. Please try again in a minute.", true); });
  }

  function dial(score) {
    var r = 54, c = 2 * Math.PI * r, color = score >= 85 ? "var(--pass)" : score >= 65 ? "var(--accent)" : score >= 40 ? "var(--warn)" : "var(--fail)";
    var wrap = h("div", { class: "dial", role: "img", "aria-label": "Score " + score + " out of 100" });
    wrap.innerHTML = '<svg viewBox="0 0 132 132" aria-hidden="true"><circle cx="66" cy="66" r="' + r + '" fill="none" stroke="var(--line)" stroke-width="12"/><circle cx="66" cy="66" r="' + r + '" fill="none" stroke="' + color + '" stroke-width="12" stroke-linecap="round" stroke-dasharray="' + c.toFixed(1) + '" stroke-dashoffset="' + (c * (1 - score / 100)).toFixed(1) + '" style="transition:stroke-dashoffset .8s ease"/></svg>';
    wrap.appendChild(h("div", { class: "num" }, [h("div", null, [h("b", { text: String(score) }), h("small", { text: "OUT OF 100" })])]));
    return wrap;
  }

  function render(rep, quiet) {
    lastReport = rep;
    var b = brand();
    out.innerHTML = "";
    var when = new Date(rep.checkedAt);
    var whenText = isNaN(when) ? "" : when.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });

    // Summary
    var actions = h("div", { class: "actions" });
    var copyBtn = h("button", { class: "linkbtn", type: "button", text: demo ? "Share links work on the live version" : "Copy link to this result" });
    if (demo) copyBtn.disabled = true;
    copyBtn.addEventListener("click", function () {
      var link = location.href;
      var ok = function () { copyBtn.textContent = "Link copied"; };
      try { navigator.clipboard.writeText(link).then(ok, function () { copyBtn.textContent = link; }); } catch (e) { copyBtn.textContent = link; }
    });
    var again = h("button", { class: "linkbtn", type: "button", text: "Check another site" });
    again.addEventListener("click", function () { out.hidden = true; urlIn.value = ""; townIn.value = ""; urlIn.focus(); window.scrollTo({ top: 0, behavior: "smooth" }); });
    actions.appendChild(copyBtn); actions.appendChild(again);
    out.appendChild(h("div", { class: "summary" }, [
      dial(rep.score),
      h("div", { class: "summary-text" }, [
        h("div", { class: "eyebrow", text: rep.site.host }),
        h("div", { class: "grade", text: rep.grade }),
        rep.sampleNote ? h("p", { class: "meta", text: rep.sampleNote }) : null,
        h("p", { class: "meta", text: (rep.town ? "Town: " + rep.town + (rep.townSource ? " (" + rep.townSource + ")" : "") + " · " : "No town found · ") + "Checked " + whenText }),
        actions
      ])
    ]));

    // Sectors
    var sectors = h("div", { class: "sectors" });
    rep.groups.forEach(function (g) {
      var bar = h("div", { class: "bar" }, [h("i", { style: "width:" + g.pct + "%" })]);
      sectors.appendChild(h("div", { class: "sector" }, [
        h("div", { class: "name" }, [g.label, h("small", { text: g.blurb })]),
        bar,
        h("div", { class: "pts", text: g.points + "/" + g.max })
      ]));
    });
    out.appendChild(h("section", { class: "sectors-wrap" }, [h("h2", { text: "Where you stand", style: "margin-bottom:14px" }), sectors]));

    // Fix first
    if (rep.topFixes && rep.topFixes.length) {
      var ol = h("ol", { class: "fixes" });
      rep.topFixes.forEach(function (f) { ol.appendChild(h("li", null, [h("div", null, [h("b", { text: f.label }), h("p", { text: f.fix })])])); });
      out.appendChild(h("section", null, [h("h2", { text: "Fix these first", style: "margin-bottom:14px" }), ol]));
    }

    // Call to action
    var topic = "AI search fixes for " + rep.site.host + " (score " + rep.score + ")";
    var href = b.contact + "?topic=" + encodeURIComponent(topic).replace(/%20/g, "+");
    var ctaBtn = h("a", { class: "btn", href: href, text: rep.score >= 85 ? "Ask about a second look" : "Get these fixed" });
    if (demo) ctaBtn.setAttribute("target", "_blank");
    ctaBtn.addEventListener("click", function () { if (window.dataLayer) window.dataLayer.push({ event: "ai_check_contact", ai_check_score: rep.score }); });
    out.appendChild(h("section", { class: "cta" }, [
      h("h2", { text: rep.score >= 85 ? "You're in good shape" : "Want this fixed for you?" }),
      h("p", { text: rep.score >= 85
        ? "Your site gives AI tools what they need. If you'd like, " + b.owner + " can check what ChatGPT, Google and Perplexity actually say about you and close any gaps."
        : b.name + " fixes these for " + b.area + " small businesses at a fixed price, and checks what ChatGPT, Google and Perplexity say about you before and after. Free 20-minute call, no obligation." }),
      ctaBtn
    ]));

    // Crawler table
    var tbody = h("tbody");
    rep.bots.forEach(function (bot) {
      var st = bot.allowed ? "pass" : bot.role === "training" ? "info" : "fail";
      tbody.appendChild(h("tr", null, [
        h("td", null, [h("code", { text: bot.token }), h("span", { class: "role", text: bot.who })]),
        h("td", null, [bot.what, h("span", { class: "role", text: bot.role === "training" ? "Model training only" : "Search and answers" })]),
        h("td", null, [h("span", { class: "pill s-" + st, text: bot.allowed ? "Allowed" : "Blocked" })])
      ]));
    });
    out.appendChild(h("section", null, [
      h("h2", { text: "AI crawlers and your robots.txt", style: "margin-bottom:6px" }),
      h("p", { class: "formnote", text: "Blocking the training-only crawlers is your call and doesn't cost points. Blocking the search ones keeps you out of their answers.", style: "margin-bottom:12px" }),
      h("div", { class: "tablewrap" }, [h("table", { class: "bots" }, [h("thead", null, [h("tr", null, [h("th", { text: "Crawler" }), h("th", { text: "What it does" }), h("th", { text: "Your site" })])]), tbody])])
    ]));

    // Full sheet
    var sheet = h("div", { class: "sheet" });
    rep.groups.forEach(function (g) {
      var sec = h("section", null, [h("h3", null, [g.label, h("span", { text: g.points + "/" + g.max })])]);
      rep.checks.filter(function (c) { return c.group === g.id; }).forEach(function (c) {
        var body = h("div", null, [h("b", { text: c.label }), h("p", { text: c.detail })]);
        if (c.fix && c.status !== "pass") body.appendChild(h("p", { class: "fix", text: c.fix }));
        if (c.why && c.status !== "pass") body.appendChild(h("p", { class: "why", text: c.why }));
        sec.appendChild(h("div", { class: "item" }, [
          h("span", { class: "pill s-" + c.status, text: STATUS[c.status] || c.status }),
          body,
          h("span", { class: "pts", text: c.max ? c.points + "/" + c.max : "" })
        ]));
      });
      sheet.appendChild(sec);
    });
    out.appendChild(h("section", null, [h("h2", { text: "Every check", style: "margin-bottom:14px" }), sheet]));
    (rep.notes || []).forEach(function (n) { out.appendChild(h("p", { class: "formnote", text: n })); });

    out.hidden = false;
    if (!quiet) out.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  form.addEventListener("submit", function (e) { e.preventDefault(); check(urlIn.value, townIn.value.trim()); });

  if (demo) {
    $("ac-brandbar").hidden = false;
    $("ac-demonote").hidden = false;
    document.querySelectorAll("#ac-brandbar button").forEach(function (btn) { btn.addEventListener("click", function () { setBrand(btn.dataset.brand); }); });
    var box = $("ac-samples");
    box.hidden = false;
    box.appendChild(h("span", { text: "Try a saved sample:" }));
    (CFG.samples || []).forEach(function (s) {
      var chip = h("button", { class: "chip", type: "button" }, [s.label + " ", s.note ? h("small", { text: s.note }) : null]);
      chip.addEventListener("click", function () { urlIn.value = s.url; townIn.value = s.town || ""; check(s.url, s.town); });
      box.appendChild(chip);
    });
  }
  setBrand(brandId);

  // Shared result links: ?url=example.com&town=Webster runs the check on load (live version only).
  if (!demo) {
    try {
      var q = new URLSearchParams(location.search);
      if (q.get("url")) { urlIn.value = q.get("url"); townIn.value = q.get("town") || ""; check(q.get("url"), q.get("town") || ""); }
    } catch (e) {}
  } else if (CFG.autoload) {
    var s0 = CFG.samples[0];
    urlIn.value = s0.url; townIn.value = s0.town || "";
    render(CFG.reports[hostOf(s0.url)], true);
  }
})();
