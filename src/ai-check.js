// AI search readiness checker API (the page lives at /tools/ai-search-checker/).
//
// GET /api/ai-check?url=example.com&town=Cape+Coral  -> JSON report (see ./checker.js)
//
// Works on the Workers free plan: each scan makes at most 10 outside requests
// (the free limit is 50) and results are cached for 6 hours per address and town,
// so repeat checks and shared links cost nothing. Source and tests live in the
// separate ai-search-checker project; copy both files from there when they change.

import { runCheck, CheckError } from "./checker.js";

const CACHE_SECONDS = 6 * 60 * 60;
const RATE_LIMIT = { max: 12, windowMs: 10 * 60 * 1000 };
const recent = new Map(); // ip -> [timestamps]. Best effort: each Cloudflare location keeps its own.

export async function handleAiCheck(request, env = {}, ctx = {}, opts = {}) {
  if (request.method !== "GET") return json({ ok: false, error: "Method not allowed" }, 405, { Allow: "GET" });
  const url = new URL(request.url);
  const target = url.searchParams.get("url") || "";
  const town = url.searchParams.get("town") || "";

  // The page sends this header. It keeps casual hotlinking and link previews from running scans.
  if (request.headers.get("x-requested-with") !== "ai-check") {
    return json({ ok: false, error: "Use the checker page to run a scan." }, 400);
  }

  const cacheKey = new Request(`https://ai-check.cache/v1?u=${encodeURIComponent(target.trim().toLowerCase())}&t=${encodeURIComponent(town.trim().toLowerCase())}`);
  const cache = typeof caches !== "undefined" ? caches.default : null;
  if (cache) {
    const hit = await cache.match(cacheKey);
    if (hit) {
      const body = await hit.text();
      return new Response(body, { headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", "X-Cache": "HIT" } });
    }
  }

  const ip = request.headers.get("cf-connecting-ip") || "unknown";
  if (!allow(ip)) {
    return json({ ok: false, error: "That's a lot of checks in a short time. Please try again in a few minutes." }, 429, { "Retry-After": "300" });
  }

  try {
    const report = await runCheck(
      { url: target, town },
      {
        fetch: (u, init) => fetch(u, { ...init, cf: { cacheTtl: 300 } }),
        userAgent: `AISearchReadinessChecker/1.0 (free website check by ${opts.site || "a web designer"})`,
      }
    );
    const body = JSON.stringify({ ok: true, report });
    if (cache) {
      const toCache = new Response(body, { headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": `public, max-age=${CACHE_SECONDS}` } });
      const put = cache.put(cacheKey, toCache);
      if (ctx.waitUntil) ctx.waitUntil(put); else await put;
    }
    return new Response(body, { headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", "X-Cache": "MISS" } });
  } catch (err) {
    if (err instanceof CheckError) return json({ ok: false, error: err.message, code: err.code }, 422);
    console.error("ai-check failed", err && err.stack);
    return json({ ok: false, error: "Something went wrong running the check. Please try again." }, 500);
  }
}

function allow(ip) {
  const now = Date.now();
  const list = (recent.get(ip) || []).filter((t) => now - t < RATE_LIMIT.windowMs);
  if (list.length >= RATE_LIMIT.max) {
    recent.set(ip, list);
    return false;
  }
  list.push(now);
  recent.set(ip, list);
  if (recent.size > 5000) recent.clear();
  return true;
}

function json(body, status = 200, extra = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...extra },
  });
}
