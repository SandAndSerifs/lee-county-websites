# Lee County Websites

Marketing site for Lee County Websites (leecountywebsites.com): fixed-price websites for small businesses in Fort Myers, Cape Coral and the rest of Lee County, Florida, by Daniel of Sand And Serifs.

Dark storefront look: deep navy and blue-gray panels, bright blue accents, a featured carousel of sample builds, capsule cards in scrolling rows, and a tabbed list with a hover preview. Plain HTML, CSS and JavaScript, built by a small Python script, deployed on Cloudflare Workers with static assets.

## What's in the repo

```
content/            The words: services.py, areas.py, blog.py, samples.py
site.config.json    Domain, name, email, phone, GTM and Search Console settings
scripts/build_site.py  Builds every page into public/
public/             Everything the browser loads (built pages are committed)
  assets/css/styles.css  Design tokens and all styles
  assets/js/site.js      Menu, finder, carousel, tabs, contact form, analytics events
src/worker.js       Handles POST /api/contact (everything else is static)
wrangler.jsonc      Cloudflare config, including the custom domains
```

After any change in `content/`, `site.config.json` or the builder, run:

```
python3 scripts/build_site.py
```

and commit the changed files in `public/` too.

## Deploy

Cloudflare dashboard: Workers & Pages, Create, Import a repository, pick `SandAndSerifs/lee-county-websites`. Leave the build command empty and the deploy command as `npx wrangler deploy`. Every push to `main` then redeploys.

`wrangler.jsonc` lists `leecountywebsites.com` and `www.leecountywebsites.com` as custom domains, so the first deploy attaches them. If Cloudflare says a hostname already has DNS records, delete the old A, AAAA or CNAME records for `@` and `www` in the domain's DNS settings and deploy again.

## Contact form

The form posts to `/api/contact`, which emails each enquiry through Resend. `CONTACT_TO` and `CONTACT_FROM` are in `wrangler.jsonc` (sending from the sandandserifs.com domain, already verified in Resend). Add the API key in the dashboard: the worker's Settings, Variables and Secrets, add a secret named `RESEND_API_KEY`. Until it exists the form tells visitors to email instead.

## Analytics and Search Console

- Google Tag Manager: put a container ID (`GTM-...`) in `site.config.json` as `gtm_container_id`, rebuild and push. GA4 is set up inside GTM.
- Search Console: add `leecountywebsites.com` as a Domain property (verify with a TXT record in Cloudflare DNS), then submit `https://leecountywebsites.com/sitemap.xml`. Or put an HTML tag code in `gsc_verification`.

## Content rules

- Copy is written fresh for Lee County. Don't paste wording from sandandserifs.com: duplicate text on two sites hurts both in Google.
- No invented clients, reviews, results or statistics. The four businesses in the carousel are made up and labelled as samples on the page. Their photos were generated with Figma AI and contain no people, text or logos.
- No address or office claims. Towns are service areas; work happens by video call and email.
