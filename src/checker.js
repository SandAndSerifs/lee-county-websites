// AI Search Readiness Checker: the scan engine.
//
// Given a website address (and optionally the town the business serves), it fetches
// the home page, robots.txt, llms.txt and the sitemap, then scores how easy the site
// is for AI search tools (ChatGPT search, Google AI Overviews, Perplexity, Claude,
// Copilot) to find, read and quote, with a local-business angle.
//
// Plain JavaScript with no dependencies, so the same file runs in a Cloudflare Worker
// and in Node (for tests). The caller passes in `fetch`, which keeps it testable.
//
// Outside requests per scan: home page (plus up to 4 redirects), robots.txt,
// llms.txt, sitemap. At most 10, well under the Workers free plan's 50.

export const VERSION = "1.0.0";

const MAX_HTML_BYTES = 350_000; // keeps parsing under the free plan's 10 ms CPU limit (about 1 ms per 50 KB)
const MAX_TEXT_BYTES = 200_000;
const FETCH_TIMEOUT_MS = 8000;
const MAX_REDIRECTS = 4;

// Crawlers that decide whether you can show up in AI answers. `search` bots fetch
// pages to answer questions; `training` bots collect pages to train models. Blocking
// training bots is a fair choice and costs no points.
export const BOTS = [
  { token: "Googlebot", who: "Google", role: "search", weight: 6, what: "Google Search, including AI Overviews and AI Mode" },
  { token: "Bingbot", who: "Microsoft", role: "search", weight: 4, what: "Bing and Microsoft Copilot; also feeds other AI tools" },
  { token: "OAI-SearchBot", who: "OpenAI", role: "search", weight: 4, what: "ChatGPT search results" },
  { token: "ChatGPT-User", who: "OpenAI", role: "search", weight: 0, what: "Visits a page when someone asks ChatGPT to look at it" },
  { token: "PerplexityBot", who: "Perplexity", role: "search", weight: 3, what: "Perplexity answers" },
  { token: "Claude-SearchBot", who: "Anthropic", role: "search", weight: 3, what: "Claude's web search results" },
  { token: "Claude-User", who: "Anthropic", role: "search", weight: 0, what: "Visits a page when someone asks Claude to look at it" },
  { token: "Applebot", who: "Apple", role: "search", weight: 0, what: "Siri and Spotlight suggestions" },
  { token: "GPTBot", who: "OpenAI", role: "training", weight: 0, what: "Collects pages to train OpenAI's models" },
  { token: "ClaudeBot", who: "Anthropic", role: "training", weight: 0, what: "Collects pages to train Anthropic's models" },
  { token: "Google-Extended", who: "Google", role: "training", weight: 0, what: "Gemini training; does not affect Google Search or AI Overviews" },
  { token: "Applebot-Extended", who: "Apple", role: "training", weight: 0, what: "Apple's AI training" },
];

// schema.org types that describe a local business (LocalBusiness and its common subtypes).
const LOCAL_TYPES = new Set(
  `LocalBusiness ProfessionalService HomeAndConstructionBusiness Plumber Electrician HVACBusiness
  RoofingContractor GeneralContractor HousePainter Locksmith MovingCompany AutomotiveBusiness AutoRepair
  AutoBodyShop AutoDealer AutoWash GasStation FoodEstablishment Restaurant CafeOrCoffeeShop Bakery BarOrPub
  Brewery Winery Distillery FastFoodRestaurant IceCreamShop Store HealthAndBeautyBusiness BeautySalon
  HairSalon NailSalon DaySpa TattooParlor MedicalBusiness MedicalClinic Dentist Physician Optician Pharmacy
  Physiotherapy Chiropractor LegalService Attorney Notary AccountingService FinancialService InsuranceAgency
  RealEstateAgent LodgingBusiness Hotel Motel BedAndBreakfast Campground ChildCare DryCleaningOrLaundry
  EntertainmentBusiness SportsActivityLocation ExerciseGym HealthClub GolfCourse BowlingAlley VeterinaryCare
  AnimalShelter EmploymentAgency TravelAgency SelfStorage ShoppingCenter TouristInformationCenter
  EmergencyService RecyclingCenter InternetCafe Florist PetStore`.split(/\s+/).filter(Boolean)
);
const LOCAL_SUFFIX = /(Store|Restaurant|Business|Contractor|Agency|Clinic|Salon|Shop|Service)$/;

const PROFILE_HOSTS = [
  ["google", /(^|\.)google\.[a-z.]+$|(^|\.)g\.page$|(^|\.)goo\.gl$|^maps\.app\.goo\.gl$|(^|\.)business\.site$/],
  ["Yelp", /(^|\.)yelp\.[a-z.]+$/],
  ["Facebook", /(^|\.)facebook\.com$|(^|\.)fb\.com$/],
  ["Nextdoor", /(^|\.)nextdoor\.com$/],
  ["BBB", /(^|\.)bbb\.org$/],
  ["Instagram", /(^|\.)instagram\.com$/],
  ["LinkedIn", /(^|\.)linkedin\.com$/],
  ["Angi", /(^|\.)angi\.com$|(^|\.)angieslist\.com$/],
  ["Houzz", /(^|\.)houzz\.com$/],
  ["Thumbtack", /(^|\.)thumbtack\.com$/],
  ["TripAdvisor", /(^|\.)tripadvisor\.[a-z.]+$/],
];

// ---------------------------------------------------------------------------
// Address checks (blocks local, private and odd addresses before any fetch)

export function normalizeUrl(raw) {
  let s = String(raw || "").trim();
  if (!s) throw new CheckError("Enter a website address.", "bad_url");
  if (s.length > 300) throw new CheckError("That address is too long.", "bad_url");
  if (!/^[a-z][a-z0-9+.-]*:\/\//i.test(s)) s = "https://" + s;
  let u;
  try {
    u = new URL(s);
  } catch {
    throw new CheckError("That doesn't look like a website address.", "bad_url");
  }
  assertPublicUrl(u);
  return new URL("/", u.origin).toString();
}

export function assertPublicUrl(u) {
  if (u.protocol !== "https:" && u.protocol !== "http:") {
    throw new CheckError("Only http and https addresses can be checked.", "bad_url");
  }
  if (u.username || u.password) throw new CheckError("Leave the username and password out of the address.", "bad_url");
  if (u.port && u.port !== "80" && u.port !== "443") {
    throw new CheckError("Only standard web ports can be checked.", "bad_url");
  }
  const host = u.hostname.toLowerCase().replace(/\.$/, "");
  if (!host.includes(".") || host.startsWith("[") || /^[\d.]+$/.test(host) || /^0x/i.test(host)) {
    throw new CheckError("Enter a domain name, like example.com.", "bad_url");
  }
  if (/(^|\.)(localhost|local|internal|intranet|lan|home|corp|test|invalid|example|onion|arpa)$/.test(host)) {
    throw new CheckError("That address isn't on the public web.", "bad_url");
  }
  if (!/^[a-z0-9.-]+$/.test(host)) throw new CheckError("That domain name has characters we can't check.", "bad_url");
}

export class CheckError extends Error {
  constructor(message, code) {
    super(message);
    this.code = code;
  }
}

// ---------------------------------------------------------------------------
// Fetching

async function fetchLimited(fetchFn, startUrl, { maxBytes, userAgent, accept }) {
  let url = new URL(startUrl);
  const chain = [];
  for (let hop = 0; hop <= MAX_REDIRECTS; hop++) {
    assertPublicUrl(url);
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
    let res;
    try {
      res = await fetchFn(url.toString(), {
        method: "GET",
        redirect: "manual",
        signal: controller.signal,
        headers: { "User-Agent": userAgent, Accept: accept || "text/html,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.8" },
      });
    } catch (err) {
      clearTimeout(timer);
      const timedOut = err && (err.name === "AbortError" || /abort/i.test(String(err.message)));
      return { ok: false, status: 0, error: timedOut ? "timeout" : "network", url: url.toString(), chain };
    }
    if (res.status >= 300 && res.status < 400 && res.headers.get("location")) {
      clearTimeout(timer);
      try { await res.body?.cancel(); } catch {}
      const next = new URL(res.headers.get("location"), url);
      chain.push({ from: url.toString(), to: next.toString(), status: res.status });
      url = next;
      continue;
    }
    let text = "";
    let truncated = false;
    try {
      ({ text, truncated } = await readCapped(res, maxBytes));
    } catch {
      clearTimeout(timer);
      return { ok: false, status: res.status, error: "read", url: url.toString(), chain };
    }
    clearTimeout(timer);
    return {
      ok: res.status >= 200 && res.status < 300,
      status: res.status,
      url: url.toString(),
      headers: res.headers,
      contentType: (res.headers.get("content-type") || "").toLowerCase(),
      text,
      truncated,
      chain,
    };
  }
  return { ok: false, status: 0, error: "redirects", url: url.toString(), chain };
}

async function readCapped(res, maxBytes) {
  if (!res.body || typeof res.body.getReader !== "function") {
    const t = await res.text();
    return { text: t.slice(0, maxBytes), truncated: t.length > maxBytes };
  }
  const reader = res.body.getReader();
  const decoder = new TextDecoder("utf-8", { fatal: false });
  let text = "";
  let bytes = 0;
  let truncated = false;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    bytes += value.byteLength;
    if (bytes > maxBytes) {
      text += decoder.decode(value.subarray(0, value.byteLength - (bytes - maxBytes)), { stream: true });
      truncated = true;
      try { await reader.cancel(); } catch {}
      break;
    }
    text += decoder.decode(value, { stream: true });
  }
  text += decoder.decode();
  return { text, truncated };
}

// ---------------------------------------------------------------------------
// robots.txt (RFC 9309: groups by user-agent, longest matching rule wins, allow wins ties)

export function parseRobots(text) {
  const groups = [];
  let current = null;
  let lastWasAgent = false;
  const sitemaps = [];
  const contentSignals = [];
  for (const rawLine of String(text || "").split(/\r?\n/)) {
    const line = rawLine.replace(/#.*/, "").trim();
    if (!line) continue;
    const m = line.match(/^([A-Za-z-]+)\s*:\s*(.*)$/);
    if (!m) continue;
    const key = m[1].toLowerCase();
    const value = m[2].trim();
    if (key === "user-agent") {
      if (!current || !lastWasAgent) {
        current = { agents: [], rules: [] };
        groups.push(current);
      }
      current.agents.push(value.toLowerCase());
      lastWasAgent = true;
      continue;
    }
    lastWasAgent = false;
    if (key === "sitemap") sitemaps.push(value);
    else if (key === "content-signal") contentSignals.push(value);
    else if ((key === "allow" || key === "disallow") && current) {
      current.rules.push({ allow: key === "allow", path: value });
    }
  }
  return { groups, sitemaps, contentSignals };
}

function groupFor(robots, token) {
  const t = token.toLowerCase();
  const exact = robots.groups.filter((g) => g.agents.includes(t));
  if (exact.length) return { rules: exact.flatMap((g) => g.rules), matched: token };
  const star = robots.groups.filter((g) => g.agents.includes("*"));
  if (star.length) return { rules: star.flatMap((g) => g.rules), matched: "*" };
  return { rules: [], matched: null };
}

function ruleMatches(pattern, path) {
  if (pattern === "") return false;
  let re = "";
  for (const ch of pattern) {
    if (ch === "*") re += ".*";
    else if (ch === "$") re += "$";
    else re += ch.replace(/[.+?^{}()|[\]\\]/g, "\\$&");
  }
  return new RegExp("^" + re).test(path);
}

export function robotsVerdict(robots, token, path = "/") {
  const { rules, matched } = groupFor(robots, token);
  let best = null;
  for (const r of rules) {
    if (!ruleMatches(r.path, path)) continue;
    const len = r.path.replace(/[*$]/g, "").length;
    if (!best || len > best.len || (len === best.len && r.allow && !best.allow)) best = { ...r, len };
  }
  return { allowed: !best || best.allow, matched, rule: best ? `${best.allow ? "Allow" : "Disallow"}: ${best.path}` : null };
}

// ---------------------------------------------------------------------------
// HTML reading (light regex parsing: no DOM in Workers, and it keeps CPU low)

const ENTITIES = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " ", ndash: "-", mdash: "-", rsquo: "'", lsquo: "'", ldquo: '"', rdquo: '"', hellip: "...", middot: "·", copy: "©" };

export function decodeEntities(s) {
  return String(s || "").replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (m, e) => {
    if (e[0] === "#") {
      const code = e[1] === "x" || e[1] === "X" ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
      return Number.isFinite(code) && code > 0 && code < 0x110000 ? String.fromCodePoint(code) : " ";
    }
    return ENTITIES[e.toLowerCase()] ?? m;
  });
}

function stripTags(s) {
  return decodeEntities(String(s || "").replace(/<[^>]*>/g, " ")).replace(/\s+/g, " ").trim();
}

function attr(tag, name) {
  const m = tag.match(new RegExp(`\\s${name}\\s*=\\s*("([^"]*)"|'([^']*)'|([^\\s>]+))`, "i"));
  return m ? decodeEntities(m[2] ?? m[3] ?? m[4] ?? "") : null;
}

export function readHtml(html, pageUrl) {
  const h = String(html || "");
  const head = (h.match(/<head[\s>][\s\S]*?<\/head>/i) || [h.slice(0, 60000)])[0];

  const title = stripTags((h.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1] || "");
  const metas = h.match(/<meta\b[^>]*>/gi) || [];
  const metaBy = (key, val) => metas.find((m) => (attr(m, key) || "").toLowerCase() === val);
  const description = attr(metaBy("name", "description") || "", "content") || "";
  const robotsMeta = metas
    .filter((m) => /^(robots|googlebot|bingbot)$/i.test(attr(m, "name") || ""))
    .map((m) => (attr(m, "content") || "").toLowerCase())
    .join(", ");
  const ogTitle = attr(metaBy("property", "og:title") || "", "content");
  const ogImage = attr(metaBy("property", "og:image") || "", "content");
  const lang = attr((h.match(/<html\b[^>]*>/i) || [""])[0], "lang");
  const canonicalTag = (head.match(/<link\b[^>]*rel\s*=\s*["']?canonical[^>]*>/i) || [])[0];
  const canonical = canonicalTag ? attr(canonicalTag, "href") : null;

  // Structured data
  const jsonLd = [];
  const jsonLdErrors = [];
  for (const m of h.matchAll(/<script\b[^>]*type\s*=\s*["']?application\/ld\+json["']?[^>]*>([\s\S]*?)<\/script>/gi)) {
    const raw = m[1].trim().replace(/^<!--|-->$/g, "");
    try {
      jsonLd.push(JSON.parse(raw));
    } catch {
      jsonLdErrors.push(raw.slice(0, 80));
    }
  }
  const nodes = flattenLd(jsonLd);
  const microdataLocal = /itemtype\s*=\s*["']https?:\/\/schema\.org\/(LocalBusiness|[A-Za-z]+(Store|Business|Service|Restaurant|Contractor))["']/i.test(h);

  // Visible text (what a crawler sees without running JavaScript)
  const body = (h.match(/<body[\s>][\s\S]*$/i) || [h])[0];
  const cleaned = body
    .replace(/<!--[\s\S]*?-->/g, " ")
    .replace(/<(script|style|noscript|svg|template|iframe|canvas)\b[\s\S]*?<\/\1>/gi, " ");
  const text = stripTags(cleaned);
  const words = text ? text.split(/\s+/).filter((w) => /[a-z0-9]/i.test(w)).length : 0;
  const scriptCount = (h.match(/<script\b/gi) || []).length;
  const appShell = /<div[^>]+id\s*=\s*["'](root|app|__next|__nuxt|svelte)["'][^>]*>\s*<\/div>/i.test(h);

  const headings = [];
  for (const m of cleaned.matchAll(/<h([1-3])\b[^>]*>([\s\S]*?)<\/h\1>/gi)) {
    const t = stripTags(m[2]);
    if (t) headings.push({ level: Number(m[1]), text: t.slice(0, 160) });
  }

  // Links
  const links = [];
  for (const m of cleaned.matchAll(/<a\b[^>]*>/gi)) {
    const href = attr(m[0], "href");
    if (href) links.push(href.trim());
  }
  const telLinks = links.filter((l) => /^tel:/i.test(l));
  const base = new URL(pageUrl);
  const external = [];
  const internal = [];
  for (const l of links) {
    try {
      const u = new URL(l, base);
      if (u.protocol !== "http:" && u.protocol !== "https:") continue;
      (sameSite(u.hostname, base.hostname) ? internal : external).push(u);
    } catch {}
  }

  return {
    title, description, robotsMeta, ogTitle, ogImage, lang, canonical,
    jsonLd, jsonLdErrors, nodes, microdataLocal,
    text, words, scriptCount, appShell, headings,
    telLinks, internal, external,
  };
}

function sameSite(a, b) {
  const strip = (h) => h.toLowerCase().replace(/^www\./, "");
  return strip(a) === strip(b);
}

function flattenLd(items) {
  const out = [];
  const visit = (v, depth) => {
    if (!v || depth > 6) return;
    if (Array.isArray(v)) return v.forEach((x) => visit(x, depth + 1));
    if (typeof v !== "object") return;
    if (v["@type"]) out.push(v);
    if (v["@graph"]) visit(v["@graph"], depth + 1);
    for (const key of ["mainEntity", "about", "provider", "publisher", "author", "brand", "parentOrganization", "subOrganization", "department"]) {
      if (v[key] && typeof v[key] === "object") visit(v[key], depth + 1);
    }
  };
  visit(items, 0);
  return out;
}

function typesOf(node) {
  const t = node["@type"];
  return (Array.isArray(t) ? t : [t]).filter(Boolean).map(String).map((s) => s.replace(/^https?:\/\/schema\.org\//, ""));
}

function isLocalType(t) {
  return LOCAL_TYPES.has(t) || LOCAL_SUFFIX.test(t);
}

function asList(v) {
  return v == null ? [] : Array.isArray(v) ? v : [v];
}

function placeNames(v) {
  const out = [];
  for (const x of asList(v)) {
    if (typeof x === "string") out.push(x);
    else if (x && typeof x === "object") {
      if (x.name) out.push(String(x.name));
      if (x.addressLocality) out.push(String(x.addressLocality));
    }
  }
  return out;
}

// ---------------------------------------------------------------------------
// Town matching

function normPlace(s) {
  return String(s || "")
    .toLowerCase()
    .replace(/\bft\.?\s/g, "fort ")
    .replace(/\bst\.?\s/g, "saint ")
    .replace(/\bmt\.?\s/g, "mount ")
    .replace(/[’']/g, "")
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

export function mentionsTown(haystack, town) {
  const t = normPlace(town).replace(/\s+(ny|fl|new york|florida)$/, "");
  if (!t) return false;
  return (" " + normPlace(haystack) + " ").includes(" " + t + " ");
}

function countTown(haystack, town) {
  const t = normPlace(town).replace(/\s+(ny|fl|new york|florida)$/, "");
  if (!t) return 0;
  const hay = " " + normPlace(haystack) + " ";
  let n = 0;
  let i = 0;
  const needle = " " + t + " ";
  while ((i = hay.indexOf(needle, i)) !== -1) {
    n++;
    i += needle.length - 1;
  }
  return n;
}

export function cleanTown(raw) {
  const s = String(raw || "").replace(/[^\p{L}\p{N}\s.'’,-]/gu, "").replace(/\s+/g, " ").trim();
  return s.slice(0, 60);
}

// ---------------------------------------------------------------------------
// The scan

export async function runCheck({ url, town }, { fetch: fetchFn, now = new Date(), userAgent } = {}) {
  if (typeof fetchFn !== "function") throw new Error("runCheck needs a fetch function");
  const start = normalizeUrl(url);
  const givenTown = cleanTown(town);
  const ua = userAgent || "AISearchReadinessChecker/1.0 (+free website check)";

  const home = await fetchLimited(fetchFn, start, { maxBytes: MAX_HTML_BYTES, userAgent: ua });
  if (!home.ok || !/html|xml|text\/plain|^$/.test(home.contentType || "")) {
    const why =
      home.error === "timeout" ? "The site took too long to answer." :
      home.error === "redirects" ? "The site redirects too many times." :
      home.status ? `The site answered with an error (HTTP ${home.status}).` :
      "We couldn't reach the site. Check the address and try again.";
    // A 403 or 503 often means a firewall turned the checker away, which AI crawlers can hit too.
    const blocked = home.status === 403 || home.status === 503 || home.status === 429;
    throw new CheckError(blocked ? `${why} A firewall or bot protection may be turning automated visitors away, and AI crawlers can get the same answer.` : why, blocked ? "blocked" : "unreachable");
  }

  const finalUrl = new URL(home.url);
  const origin = finalUrl.origin;
  const [robotsRes, llmsRes] = await Promise.all([
    fetchLimited(fetchFn, origin + "/robots.txt", { maxBytes: MAX_TEXT_BYTES, userAgent: ua, accept: "text/plain,*/*;q=0.5" }),
    fetchLimited(fetchFn, origin + "/llms.txt", { maxBytes: MAX_TEXT_BYTES, userAgent: ua, accept: "text/plain,text/markdown,*/*;q=0.5" }),
  ]);

  const robotsText = robotsRes.ok && !/html/.test(robotsRes.contentType) ? robotsRes.text : "";
  const robots = parseRobots(robotsText);

  let sitemapUrl = origin + "/sitemap.xml";
  const declared = robots.sitemaps.find((s) => { try { return sameSite(new URL(s).hostname, finalUrl.hostname); } catch { return false; } });
  if (declared) sitemapUrl = declared;
  const sitemapRes = await fetchLimited(fetchFn, sitemapUrl, { maxBytes: MAX_TEXT_BYTES, userAgent: ua, accept: "application/xml,text/xml,*/*;q=0.5" });

  const page = readHtml(home.text, home.url);
  const report = buildReport({
    start, finalUrl, home, page, robots, robotsRes, robotsText, llmsRes, sitemapRes, sitemapUrl, givenTown, now,
  });
  return report;
}

function buildReport(ctx) {
  const { start, finalUrl, home, page, robots, robotsRes, robotsText, llmsRes, sitemapRes, givenTown, now } = ctx;
  const checks = [];
  const add = (c) => checks.push({ points: 0, ...c });
  const headers = home.headers;
  const fullText = `${page.title} ${page.description} ${page.text}`;

  // --- Business facts from structured data
  const localNodes = page.nodes.filter((n) => typesOf(n).some(isLocalType));
  const biz = localNodes[0] || null;
  const orgNode = page.nodes.find((n) => typesOf(n).some((t) => t === "Organization" || t === "Corporation"));
  const bizAddress = biz && (Array.isArray(biz.address) ? biz.address[0] : biz.address);
  const bizLocality = bizAddress && typeof bizAddress === "object" ? bizAddress.addressLocality : null;
  const areaServed = biz ? placeNames(biz.areaServed) : [];

  // The town we judge against: what they typed, else what their markup says.
  const town = givenTown || bizLocality || areaServed[0] || "";
  const townSource = givenTown ? "the town you entered" : bizLocality ? "your business address markup" : areaServed[0] ? "your service area markup" : "";

  // =========================================================================
  // 1. Can AI tools get in?
  const botRows = BOTS.map((b) => {
    const v = robotsVerdict(robots, b.token);
    return { ...b, allowed: v.allowed, rule: v.rule, matched: v.matched };
  });
  const searchBots = botRows.filter((b) => b.weight > 0);
  const maxBotPts = searchBots.reduce((s, b) => s + b.weight, 0);
  const botPts = searchBots.reduce((s, b) => s + (b.allowed ? b.weight : 0), 0);
  const blockedSearch = botRows.filter((b) => b.role === "search" && !b.allowed);
  const blockedTraining = botRows.filter((b) => b.role === "training" && !b.allowed);
  add({
    id: "robots_search", group: "access",
    label: "AI search crawlers are allowed in",
    status: blockedSearch.length === 0 ? "pass" : botPts >= maxBotPts / 2 ? "warn" : "fail",
    points: botPts, max: maxBotPts,
    detail: !robotsRes.ok
      ? robotsRes.status === 404
        ? "No robots.txt file, so every crawler is allowed by default."
        : `We couldn't read your robots.txt${robotsRes.status ? ` (HTTP ${robotsRes.status})` : ""}. If crawlers can't read it either, some will hold off.`
      : blockedSearch.length
        ? `Your robots.txt blocks ${listNames(blockedSearch.map((b) => b.token))}.`
        : "Your robots.txt lets the main AI search crawlers in.",
    fix: blockedSearch.length
      ? `Remove the Disallow lines for ${listNames(blockedSearch.map((b) => b.token))} in robots.txt. You can still block the training-only bots if you prefer.`
      : null,
    why: "If a crawler can't visit your site, that AI tool can only repeat what other sites say about you.",
  });
  if (blockedTraining.length) {
    add({
      id: "robots_training", group: "access", label: "Training bots blocked (your choice)", status: "info", max: 0,
      detail: `You block ${listNames(blockedTraining.map((b) => b.token))}. These only collect pages for model training, so blocking them doesn't hide you from AI search answers.`,
    });
  }

  // Cloudflare: its AI-bot setting can block crawlers at the firewall, which robots.txt can't show.
  const onCloudflare = /cloudflare/i.test(headers.get("server") || "") || !!headers.get("cf-ray");
  const cfManaged = /cloudflare managed|content-signal/i.test(robotsText);
  const signals = robots.contentSignals.join(", ").toLowerCase();
  if (/search\s*=\s*no/.test(signals)) {
    add({
      id: "content_signal", group: "access", label: "Content Signals allow search", status: "fail", max: 0,
      detail: "Your robots.txt has a Content-Signal line with search=no, which asks crawlers not to use your pages in search results.",
      fix: "Change it to search=yes (you can keep ai-train=no).",
    });
  }
  if (onCloudflare) {
    add({
      id: "cloudflare", group: "access", label: "Cloudflare's AI bot setting", status: "check", max: 0,
      detail: cfManaged
        ? "Your site runs through Cloudflare and uses its managed robots.txt. Cloudflare can also block AI crawlers at its firewall, which no outside check can see."
        : "Your site runs through Cloudflare, which can block AI crawlers at its firewall. Newer Cloudflare sites may have this switched on by default, and no outside check can see it.",
      fix: "In Cloudflare, open your domain's Security settings, find the AI crawlers or bots setting, and make sure search crawlers aren't blocked.",
    });
  }

  // noindex / nosnippet
  const xRobots = (headers.get("x-robots-tag") || "").toLowerCase();
  const robotsDirectives = `${page.robotsMeta}, ${xRobots}`;
  const noindex = /\bnoindex\b|\bnone\b/.test(robotsDirectives);
  const nosnippet = /\bnosnippet\b|max-snippet\s*:\s*0\b/.test(robotsDirectives);
  add({
    id: "indexable", group: "access", label: "Pages can be indexed and quoted",
    status: noindex ? "fail" : nosnippet ? "warn" : "pass",
    points: noindex ? 0 : nosnippet ? 3 : 6, max: 6,
    detail: noindex
      ? "Your home page tells search engines not to index it (noindex)."
      : nosnippet
        ? "Your home page asks search engines not to show snippets (nosnippet), which also keeps Google's AI answers from quoting it."
        : "Nothing on your home page tells search engines to skip it or not quote it.",
    fix: noindex ? "Remove noindex from the robots meta tag or X-Robots-Tag header." : nosnippet ? "Remove nosnippet unless you have a reason to keep it." : null,
    why: "Google uses the same index and snippet rules for AI Overviews and AI Mode.",
  });

  const https = finalUrl.protocol === "https:";
  add({
    id: "https", group: "access", label: "Secure (https) and loads cleanly",
    status: https && home.chain.length <= 2 ? "pass" : https ? "warn" : "fail",
    points: https ? (home.chain.length <= 2 ? 4 : 2) : 0, max: 4,
    detail: !https
      ? "Your site loads without https."
      : home.chain.length > 2
        ? `Your address goes through ${home.chain.length} redirects before the page loads.`
        : "Your site loads over https.",
    fix: !https ? "Turn on https (free with Cloudflare or most hosts) and redirect http to it." : home.chain.length > 2 ? "Point links and redirects straight at the final address." : null,
  });

  // =========================================================================
  // 2. Can AI tools read it?
  const thinShell = page.words < 120 && (page.appShell || page.scriptCount > 10);
  add({
    id: "text_html", group: "read", label: "Your words are in the page itself",
    status: page.words >= 250 ? "pass" : page.words >= 120 ? "warn" : "fail",
    points: page.words >= 250 ? 10 : page.words >= 120 ? 5 : 0, max: 10,
    detail: thinShell
      ? `We found ${page.words ? `only ${page.words}` : "no"} words before JavaScript runs. Your page seems to build itself with JavaScript, and most AI crawlers don't run it.`
      : `We found ${page.words.toLocaleString("en-US")} words of readable text on your home page${page.words < 250 ? ", which is thin" : ""}.`,
    fix: page.words >= 250 ? null : thinShell
      ? "Have the page's text delivered in the HTML (server rendering or a static build), not added later by JavaScript."
      : "Add a few short paragraphs saying what you do, for whom, where, and what it costs.",
    why: "AI crawlers mostly read the raw HTML. Text that only appears after scripts run is often invisible to them.",
  });
  const titleOk = page.title.length >= 10 && page.title.length <= 70;
  const descOk = page.description.length >= 50 && page.description.length <= 170;
  add({
    id: "title_desc", group: "read", label: "Clear page title and description",
    status: titleOk && descOk ? "pass" : page.title ? "warn" : "fail",
    points: (titleOk ? 3 : page.title ? 1 : 0) + (descOk ? 2 : page.description ? 1 : 0), max: 5,
    detail: `Title: ${page.title ? `"${clip(page.title, 90)}"` : "missing"}. Description: ${page.description ? `"${clip(page.description, 120)}"` : "missing"}.`,
    fix: titleOk && descOk ? null : "Write a title like \"Service in Town | Business Name\" (under 60 characters) and a one-sentence description of what you do and where.",
  });

  // =========================================================================
  // 3. Does AI know where you are? (the local part)
  const hasLocalMarkup = !!biz || page.microdataLocal;
  add({
    id: "local_markup", group: "local", label: "Local business markup",
    status: biz ? "pass" : page.microdataLocal ? "warn" : "fail",
    points: biz ? 10 : page.microdataLocal ? 6 : orgNode ? 3 : 0, max: 10,
    detail: biz
      ? `Found ${typesOf(biz).join(", ")} markup${biz.name ? ` for "${clip(String(biz.name), 60)}"` : ""}.`
      : page.microdataLocal
        ? "Found local business microdata, an older format that AI tools read less reliably than JSON-LD."
        : orgNode
          ? "Found Organization markup, but nothing that says you're a local business."
          : page.jsonLdErrors.length
            ? "Your page has structured data that's broken (it isn't valid JSON), so nothing could be read from it."
            : "No local business markup (schema.org LocalBusiness) on your home page.",
    fix: biz ? null : "Add LocalBusiness JSON-LD (or a closer type like Plumber or Restaurant) with your name, phone, address or service area, and hours.",
    why: "This is the machine-readable version of who you are, where you are and how to reach you.",
  });

  const phoneInMarkup = !!(biz && biz.telephone);
  const placeInMarkup = !!(bizLocality || areaServed.length);
  const hoursInMarkup = !!(biz && (biz.openingHoursSpecification || biz.openingHours));
  add({
    id: "markup_details", group: "local", label: "Phone, place and hours in that markup",
    status: !biz ? "fail" : phoneInMarkup && placeInMarkup && hoursInMarkup ? "pass" : "warn",
    points: biz ? (phoneInMarkup ? 3 : 0) + (placeInMarkup ? 3 : 0) + (hoursInMarkup ? 3 : 0) : 0, max: 9,
    detail: biz
      ? `Phone: ${phoneInMarkup ? "yes" : "missing"}. Town or service area: ${placeInMarkup ? listNames([bizLocality, ...areaServed].filter(Boolean).slice(0, 4)) : "missing"}. Hours: ${hoursInMarkup ? "yes" : "missing"}.`
      : "No local business markup to check.",
    fix: biz && !(phoneInMarkup && placeInMarkup && hoursInMarkup)
      ? `Add ${listNames([!phoneInMarkup && "telephone", !placeInMarkup && "address or areaServed", !hoursInMarkup && "openingHoursSpecification"].filter(Boolean))} to your LocalBusiness markup.`
      : biz ? null : "Add LocalBusiness markup first (see above).",
  });

  const titleH1 = `${page.title} ${page.headings.filter((h) => h.level === 1).map((h) => h.text).join(" ")}`;
  const townInTop = town ? mentionsTown(titleH1, town) : false;
  const townCount = town ? countTown(fullText, town) : 0;
  add({
    id: "town_top", group: "local", label: "Your town is in the title or main heading",
    status: !town ? "fail" : townInTop ? "pass" : "warn",
    points: townInTop ? 6 : 0, max: 6,
    detail: !town
      ? "We couldn't tell which town you serve: none was entered and your markup doesn't say. AI tools have the same problem."
      : townInTop
        ? `"${town}" (from ${townSource}) appears in your page title or main heading.`
        : `"${town}" (from ${townSource}) isn't in your page title or main heading.`,
    fix: townInTop ? null : town ? `Put "${town}" in your page title and main heading, like "Plumbing repair in ${town}".` : "Name your town in the title and main heading, and add it to your markup.",
    why: "People ask AI for businesses \"near me\" or in a town, and AI tools often add a location to the search on their own.",
  });
  add({
    id: "town_text", group: "local", label: "Your town is named in the page text",
    status: !town ? "fail" : townCount >= 2 ? "pass" : townCount === 1 ? "warn" : "fail",
    points: townCount >= 2 ? 4 : townCount === 1 ? 2 : 0, max: 4,
    detail: town ? `"${town}" appears ${townCount} time${townCount === 1 ? "" : "s"} on your home page.` : "No town to look for.",
    fix: townCount >= 2 ? null : town ? `Mention ${town} and the nearby towns you serve in plain sentences, like "We serve ${town} and nearby towns."` : null,
  });

  // 555-01xx numbers are reserved for fiction and samples, so they don't count.
  const phoneVisible = page.telLinks.length > 0 || [...page.text.matchAll(/\(?\b\d{3}\)?[\s.-](\d{3})[\s.-](\d{4})\b/g)].some((m) => !(m[1] === "555" && m[2].startsWith("01")));
  add({
    id: "phone_visible", group: "local", label: "Phone number on the page",
    status: phoneVisible ? (page.telLinks.length ? "pass" : "warn") : "fail",
    points: phoneVisible ? (page.telLinks.length ? 3 : 2) : 0, max: 3,
    detail: page.telLinks.length ? "Your phone number is on the page as a tap-to-call link." : phoneVisible ? "Your phone number is on the page, but not as a tap-to-call link." : "We couldn't find a phone number on your home page.",
    fix: page.telLinks.length ? null : "Show your phone number as text and make it a tap-to-call (tel:) link.",
  });

  const profileLinks = new Set();
  const sameAs = biz ? asList(biz.sameAs) : orgNode ? asList(orgNode.sameAs) : [];
  for (const s of [...sameAs.map(String), ...page.external.map((u) => u.toString())]) {
    try {
      const hostName = new URL(s).hostname.toLowerCase();
      for (const [name, re] of PROFILE_HOSTS) if (re.test(hostName)) profileLinks.add(name === "google" ? "Google" : name);
    } catch {}
  }
  const profiles = [...profileLinks];
  add({
    id: "profiles", group: "local", label: "Links to your review and business profiles",
    status: profiles.length >= 2 ? "pass" : profiles.length === 1 ? "warn" : "fail",
    points: profiles.length >= 2 ? 3 : profiles.length === 1 ? 2 : 0, max: 3,
    detail: profiles.length ? `Found links to ${listNames(profiles)}.` : "No links to profiles like Google, Yelp, Facebook, Nextdoor or BBB.",
    fix: profiles.length >= 2 ? null : "Link to your Google, Yelp, Facebook or other profiles, and list them in your markup's sameAs.",
    why: "AI tools lean on review sites for local questions. Linking them helps tie those profiles to your site.",
  });

  // =========================================================================
  // 4. Will AI quote you?
  const faqMarkup = page.nodes.some((n) => typesOf(n).includes("FAQPage"));
  const questionHeadings = page.headings.filter((x) => /\?\s*$/.test(x.text)).length;
  const faqHeading = page.headings.some((x) => /\bfaq|frequently asked|questions\b/i.test(x.text));
  const hasFaq = faqMarkup || faqHeading || questionHeadings >= 3;
  add({
    id: "faq", group: "quote", label: "Questions answered on the page",
    status: hasFaq ? "pass" : questionHeadings >= 1 ? "warn" : "fail",
    points: hasFaq ? 5 : questionHeadings >= 1 ? 2 : 0, max: 5,
    detail: faqMarkup ? "Found an FAQ section with FAQ markup." : hasFaq ? "Found a questions-and-answers section." : questionHeadings ? "Found a question heading, but not a full FAQ section." : "No questions-and-answers section on your home page.",
    fix: hasFaq ? null : "Add 4 to 6 real customer questions with short, direct answers (cost, area served, how long, how to book).",
    why: "AI answers are built from direct answers. A page that asks and answers the question in plain words is easy to quote.",
  });

  const prices = /(\$\s?\d[\d,]*(\.\d\d)?)|(\b\d[\d,]*\s?(dollars|usd)\b)/i.test(page.text) || page.nodes.some((n) => n.priceRange || n.offers);
  add({
    id: "prices", group: "quote", label: "Prices or price ranges shown",
    status: prices ? "pass" : "warn",
    points: prices ? 4 : 0, max: 4,
    detail: prices ? "Your home page mentions prices." : "No prices or price ranges on your home page.",
    fix: prices ? null : "Show starting prices or typical ranges, even a \"from $\" figure. Cost is one of the first things people ask AI.",
    why: "A 2026 study of 193,507 AI answers found pages showing prices were cited more often.",
  });

  const year = now.getUTCFullYear();
  const modified = page.nodes.map((n) => n.dateModified || n.datePublished).filter(Boolean).map((d) => new Date(d)).filter((d) => !isNaN(d));
  const latest = modified.length ? new Date(Math.max(...modified)) : null;
  const recentMarkup = latest && now - latest < 365 * 864e5;
  const yearInText = new RegExp(`\\b(${year}|${year - 1})\\b`).test(page.text.replace(/©\s*\d{4}|copyright\s*\d{4}/gi, ""));
  const fresh = recentMarkup || yearInText;
  add({
    id: "fresh", group: "quote", label: "Looks up to date",
    status: fresh ? "pass" : "warn",
    points: fresh ? 4 : 0, max: 4,
    detail: recentMarkup ? `Your markup says the page was updated ${latest.toISOString().slice(0, 10)}.` : yearInText ? `Your page mentions ${year} or ${year - 1} outside the copyright line.` : "Nothing on the page shows it was updated in the last year (a copyright year doesn't count).",
    fix: fresh ? null : "Add a dated update (like \"Prices updated March " + year + "\") or dateModified in your markup, and refresh the page at least once a year.",
    why: "The same study found pages updated within the last 12 months were cited noticeably more.",
  });

  const sitemapOk = sitemapRes.ok && /<(urlset|sitemapindex)\b/i.test(sitemapRes.text || "");
  add({
    id: "sitemap", group: "quote", label: "Sitemap that lists your pages",
    status: sitemapOk ? "pass" : "warn",
    points: sitemapOk ? 3 : 0, max: 3,
    detail: sitemapOk ? `Found a sitemap${robots.sitemaps.length ? " and it's listed in robots.txt" : ""}.` : "No sitemap found at /sitemap.xml or in robots.txt.",
    fix: sitemapOk ? null : "Add a sitemap.xml (most site builders can make one) and list it in robots.txt.",
  });

  const h1s = page.headings.filter((x) => x.level === 1).length;
  const h2s = page.headings.filter((x) => x.level === 2).length;
  const structureOk = h1s === 1 && h2s >= 3;
  add({
    id: "structure", group: "quote", label: "Clear headings that split up the page",
    status: structureOk ? "pass" : h1s >= 1 || h2s >= 1 ? "warn" : "fail",
    points: structureOk ? 2 : h1s >= 1 || h2s >= 1 ? 1 : 0, max: 2,
    detail: `${h1s} main heading${h1s === 1 ? "" : "s"} (H1) and ${h2s} section heading${h2s === 1 ? "" : "s"} (H2).`,
    fix: structureOk ? null : "Use one main heading, then a heading for each section (services, area, prices, questions).",
  });

  const llmsOk = llmsRes.ok && !/html/.test(llmsRes.contentType) && (llmsRes.text || "").trim().length > 20;
  add({
    id: "llms", group: "quote", label: "llms.txt summary file (optional)",
    status: llmsOk ? "pass" : "info",
    points: llmsOk ? 2 : 0, max: 2,
    detail: llmsOk ? "Found an llms.txt file." : "No llms.txt file. It's a newer, optional plain-text summary of your site for AI tools.",
    fix: llmsOk ? null : "Optional: add /llms.txt with a short summary of your business, services, area and contact details. It's cheap to add, though the big AI tools haven't said they use it.",
  });

  // =========================================================================
  const scored = checks.filter((c) => c.max > 0);
  const total = scored.reduce((s, c) => s + c.points, 0);
  const max = scored.reduce((s, c) => s + c.max, 0);
  const score = Math.round((total / max) * 100);
  const groups = Object.entries(GROUPS).map(([id, g]) => {
    const cs = scored.filter((c) => c.group === id);
    const p = cs.reduce((s, c) => s + c.points, 0);
    const m = cs.reduce((s, c) => s + c.max, 0);
    return { id, label: g.label, blurb: g.blurb, points: p, max: m, pct: m ? Math.round((p / m) * 100) : 0 };
  });
  const topFixes = checks
    .filter((c) => c.fix && (c.status === "fail" || c.status === "warn" || c.status === "check"))
    .sort((a, b) => (b.max - b.points) - (a.max - a.points) || (a.status === "check") - (b.status === "check"))
    .slice(0, 3)
    .map((c) => ({ id: c.id, label: c.label, fix: c.fix }));

  return {
    version: VERSION,
    checkedAt: now.toISOString(),
    input: { url: start, town: givenTown || null },
    site: { url: home.url, host: finalUrl.hostname, title: page.title || null },
    town: town || null,
    townSource: townSource || null,
    score,
    grade: score >= 85 ? "Ready for AI search" : score >= 65 ? "Close" : score >= 40 ? "Needs work" : "Hard for AI to find",
    groups,
    checks,
    bots: botRows.map(({ token, who, role, what, allowed, rule }) => ({ token, who, role, what, allowed, rule })),
    topFixes,
    notes: [home.truncated ? "Your home page is very large, so we only read the first 350 KB." : null].filter(Boolean),
  };
}

const GROUPS = {
  access: { label: "Can AI tools get in?", blurb: "Crawler access, indexing and https" },
  read: { label: "Can they read it?", blurb: "Text in the page, title and description" },
  local: { label: "Do they know where you are?", blurb: "Business markup, town, phone, profiles" },
  quote: { label: "Will they quote you?", blurb: "Answers, prices, freshness, structure" },
};

function listNames(items) {
  const a = items.filter(Boolean);
  if (a.length <= 1) return a.join("");
  if (a.length === 2) return `${a[0]} and ${a[1]}`;
  return `${a.slice(0, -1).join(", ")} and ${a[a.length - 1]}`;
}

function clip(s, n) {
  s = String(s);
  return s.length > n ? s.slice(0, n - 1).trimEnd() + "…" : s;
}
