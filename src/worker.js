/**
 * Lee County Websites site worker.
 *
 * Static files in ./public are served by Cloudflare's asset handling before this
 * code runs. Only requests that don't match a file reach the worker:
 *   POST /api/contact  -> validates the form and emails it (via Resend) if configured
 *   GET /api/ai-check  -> the free AI search readiness checker (see ai-check.js)
 *   anything else      -> the site's 404 page
 *
 * Email is optional. Until RESEND_API_KEY, CONTACT_TO and CONTACT_FROM are set
 * (see README), the endpoint answers 503 and the page asks visitors to email directly.
 */
import { handleAiCheck } from "./ai-check.js";

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (url.pathname === "/api/contact") {
      if (request.method !== "POST") {
        return json({ ok: false, error: "Method not allowed" }, 405, { Allow: "POST" });
      }
      return handleContact(request, env);
    }

    if (url.pathname === "/api/ai-check") {
      return handleAiCheck(request, env, ctx, { site: "Lee County Websites" });
    }

    // Unknown path: serve the 404 page with a 404 status.
    const notFound = await env.ASSETS.fetch(new Request(new URL("/404.html", url), request));
    return new Response(notFound.body, { status: 404, headers: notFound.headers });
  },
};

async function handleContact(request, env) {
  let data;
  try {
    const type = request.headers.get("content-type") || "";
    if (type.includes("application/json")) {
      data = await request.json();
    } else {
      data = Object.fromEntries(await request.formData());
    }
  } catch {
    return json({ ok: false, error: "Could not read the form." }, 400);
  }

  // Honeypot: bots fill hidden fields. Pretend success and drop it.
  if (data.company_site) return json({ ok: true });

  const name = clean(data.name, 120);
  const email = clean(data.email, 200);
  const site = clean(data.site, 200);
  const message = clean(data.message, 5000);
  const business = clean(data.business, 200);
  const needs = clean(data.needs, 300);
  const budget = clean(data.budget, 80);
  const timeline = clean(data.timeline, 80);
  const page = clean(data.page, 200);

  if (!name || !message || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return json({ ok: false, error: "Name, a valid email and a message are required." }, 422);
  }

  if (!env.RESEND_API_KEY || !env.CONTACT_TO || !env.CONTACT_FROM) {
    return json({ ok: false, error: "The contact form isn't connected yet." }, 503);
  }

  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: env.CONTACT_FROM,
      to: [env.CONTACT_TO],
      reply_to: email,
      subject: `New Lee County Websites inquiry from ${name}`,
      text: [
        `Name: ${name}`,
        `Email: ${email}`,
        `Business: ${business || "not given"}`,
        `Current site: ${site || "none given"}`,
        `Needs: ${needs || "not given"}`,
        `Budget: ${budget || "not given"}`,
        `Timeline: ${timeline || "not given"}`,
        `Sent from: ${page || "/"}`,
        "",
        message,
      ].join("\n"),
    }),
  });

  if (!res.ok) {
    return json({ ok: false, error: "The message could not be sent." }, 502);
  }
  return json({ ok: true });
}

function clean(value, max) {
  return String(value ?? "").replace(/[\u0000-\u001f\u007f]/g, (c) => (c === "\n" ? "\n" : " ")).trim().slice(0, max);
}

function json(body, status = 200, extra = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...extra },
  });
}
