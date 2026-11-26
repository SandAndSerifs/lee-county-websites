# Lee County Websites: notes for Claude

## Design work uses the design skills

For any design work in this repo (a new page, a section, a restyle, a redesign or a full
rebuild), use the skills in `.claude/skills/`:

1. **design-systems**: when starting a new look or a rebuild, pick a starting system from its
   library and write this site's own `DESIGN.md` from it (system, not another brand's identity).
2. **design-taste-frontend** (Taste): the main build rules that keep pages away from generic
   AI-template looks. Run its gate before calling a page done.
3. **impeccable**: the design commands (`audit`, `critique`, `polish`, `typeset`,
   `layout`, `adapt`, `colorize`, `animate` and the rest). Its engine is not installed on
   purpose (see `.claude/skills/VENDORED.md`), so skip its launcher commands and follow its
   "Launcher unavailable" path; the playbooks in `reference/` still apply.
4. **playwright-cli**: check the real pages in a browser before shipping.

## Check pages with Playwright before shipping

Before pushing any visual change, open the changed pages in a real browser and look at them at
1440, 1024, 768 and 390 px wide: screenshots, console errors, broken images, sideways scroll,
the contact form still present. Run Playwright from the official npm registry without adding
it to `package.json`:

```
npx -y @playwright/cli@0.1.25 --help
npx -y playwright@latest install chromium   # first time on a machine, if no browser is found
```

Serve the site with `npm run dev` (http://localhost:8787) or any static server on `public/`.
Installing anything on Dan's own laptop needs his yes first; cloud sessions can run the
commands above.

## This site's facts win over the skills

The skills were written for generic company sites. Where they conflict with this site, this
site wins:

- Use the real business details from `site.config.json` (email, phone, booking link). Ignore
  Taste's rule about placeholder contacts on `.example` and fake-format phone numbers; that is
  for demo pages only (the `/samples/` or `/work/` demo sites).
- Prices are $500, $1,500 and Custom. Don't invent other prices, packages or claims.
- Portfolio pieces are "Our work". Never call them examples or samples on the main site, and
  never claim they are paying clients.
- Lee County Websites serves Fort Myers, Cape Coral and the rest of Lee County, FL. Keep its copy
  distinct from Sand And Serifs, and keep the two sites visually different.
- Keep a Contact button in the header at every width.
- Don't copy a real company's look from the design-systems library; use it for structure only.
- Keep the build steps in `README.md`: edit `content/` or the builder, run the build script,
  and commit what changes in `public/`. Only `public/` is deployed.
