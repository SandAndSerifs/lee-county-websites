"""Service pages. Each entry becomes /services/<slug>/.

Write in Daniel's voice (first person), plain words, no dashes. This copy is written
fresh for Lee County: never paste text from sandandserifs.com, because the same
wording on two sites hurts both in Google. Never add client names, quotes, reviews
or results that aren't real.
"""

SERVICES = [
    {
        "slug": "small-business-website-design",
        "name": "Small business website design",
        "short": "New websites",
        "icon": "browser",
        "hue": 205,
        "tags": ["Fixed price", "Phone first", "Local search ready"],
        "seo_title": "Small Business Website Design in Fort Myers & Cape Coral",
        "description": "Small business websites for Fort Myers, Cape Coral and Lee County: one page for $500 or up to five pages for $1,500, fixed price, fast on phones.",
        "h1": "Small business website design for Fort Myers and Cape Coral",
        "lede": "A website that answers the three things every visitor wants to know straight away: what you do, whether you cover their part of Lee County, and how to reach you. Built by hand, priced up front, and owned by you.",
        "price": "From $500",
        "time": "2 to 4 weeks",
        "answer": "I build websites for small businesses in Fort Myers, Cape Coral and the rest of Lee County. The Starter package is one page for $500 and the Business package is up to five pages for $1,500, both at a fixed price agreed before any work starts. Every site is designed for phones first, loads quickly and goes live with the basics Google needs to show it in local searches.",
        "sections": [
            ("Who this is for", """
<p>Contractors, pool and lawn companies, salons, restaurants, charter captains, clinics, shops and nonprofits across Lee County. Most of the people who get in touch with me have one of three problems: no website at all, a site somebody built years ago that nobody can update, or a social media page that has quietly become the only place customers can find them.</p>
<p>If you need an online store, bookings tied into your scheduling software, or a large site, that's a <a href="/pricing/">Custom project</a>. I'll quote it after a short call.</p>
"""),
            ("The two packages", """
<h3>Starter, $500</h3>
<p>A single, well organized page: what you do, the services you offer, your hours, the towns you cover and a contact form that sends each enquiry to your inbox. You give me the words and photos you already have, I shape them into something clear, and you get one round of changes. Plan on about two weeks.</p>
<h3>Business, $1,500</h3>
<p>Up to five pages, laid out around the way your customers decide. That usually means a home page, a page for each main service, an about page and a contact or booking page. I interview you for half an hour and write the first draft of the words myself, add a quote or booking form, and set up local search. You get two rounds of design changes and 30 days of fixes after launch. Plan on about four weeks.</p>
"""),
            ("How the build works", """
<p>You see the design on a private preview link before anything is final, so there are no surprises at launch. I design in Figma, then write the site by hand and host it on Cloudflare. No page builder, no stack of plugins to keep patched, and pages that open almost instantly on a phone, even on a weak signal at the beach.</p>
<p>Anything you change often, like a menu, seasonal hours or a price list, I set up so you can edit it yourself without calling me.</p>
"""),
            ("Ready for local search on day one", """
<p>Each page launches with its own title and description, structured data that tells Google and AI assistants your business name, services and the parts of Lee County you cover, a sitemap, and Google Search Console connected so we can watch which searches you start to appear in. I also go through your Google Business Profile with you, since that listing drives most map results. The <a href="/services/local-seo/">local SEO page</a> explains what that involves.</p>
"""),
            ("Running costs after launch", """
<p>Hosting sits on a Cloudflare account in your name. For most small business sites it costs nothing or a few dollars a month. A domain name is typically $10 to $20 a year. A care plan is optional; <a href="/services/website-care-plans/">here's what one covers</a> if you'd rather hand the upkeep to me.</p>
"""),
        ],
        "included": [
            "Designed for phones first, previewed before launch",
            "Fast pages, even on a weak signal",
            "A contact or quote form that emails you",
            "Search Console, analytics and a sitemap",
            "Structured data for Google and AI answers",
            "Readable contrast, headings and alt text",
            "Your domain, code and hosting, in your name",
        ],
        "faq": [
            ("What does a small business website cost in Fort Myers?", "With me it's $500 for a one-page Starter site or $1,500 for a Business site of up to five pages, at a fixed price. Stores, booking systems and bigger sites get a fixed quote after a free 20-minute call."),
            ("Do I have to write all the words?", "Not for a Business site. I write the first draft from a half-hour interview and we edit it together. For a Starter site you send what you have and I tidy it up."),
            ("Can I change things myself later?", "Yes, for whatever changes often, such as hours, prices or a menu. I set it up during the build and walk you through it at launch."),
            ("Do you only work in Fort Myers and Cape Coral?", "No. Those are the two biggest places I serve, but I work with businesses anywhere in Lee County and beyond. Everything runs over video calls, email and a shared preview link."),
        ],
        "areas": ["fort-myers-fl", "cape-coral-fl", "estero-fl", "lehigh-acres-fl"],
        "posts": ["website-cost-fort-myers-cape-coral", "google-business-profile-lee-county"],
    },
    {
        "slug": "website-redesign",
        "name": "Website redesign",
        "short": "Redesigns",
        "icon": "refresh",
        "hue": 265,
        "tags": ["Keeps your rankings", "Redirects mapped", "Faster pages"],
        "seo_title": "Website Redesign for Lee County Small Businesses",
        "description": "Website redesigns for Fort Myers, Cape Coral and Lee County businesses: a faster, clearer site that keeps your Google traffic. Up to five pages for $1,500.",
        "h1": "Website redesign for Lee County small businesses",
        "lede": "Your old site still brings in some calls, so a redesign shouldn't throw that away. I rebuild what isn't working, keep what is, and make sure Google follows every old page to its new home.",
        "price": "$1,500 for up to 5 pages",
        "time": "About 4 weeks",
        "answer": "I redesign websites for small businesses in Fort Myers, Cape Coral and across Lee County. A redesign of up to five pages costs $1,500 at a fixed price and takes about four weeks. Before anything changes I record which pages bring you visitors, then point every old address to its replacement so the search traffic you've already earned carries over.",
        "sections": [
            ("Signs it's time", """
<ul>
<li>The site is awkward on a phone: tiny text, buttons that are hard to tap, or a menu that doesn't open.</li>
<li>You can't update it, or the one person who could has moved on.</li>
<li>It still shows old hours, an old phone number or a storm closure notice from a season ago.</li>
<li>People call and ask questions the site should already answer.</li>
<li>It takes several seconds to load, or your browser flags it as not secure.</li>
</ul>
"""),
            ("Keeping the traffic you have", """
<p>The biggest risk in any redesign is losing search visibility you built up over years. Before I touch the design I export your pages, the searches they show up for and the sites that link to you. Every old page address gets a permanent redirect to the matching new page, and after launch I check Search Console for errors and broken links for the following month.</p>
<p>I wrote about the full process in <a href="/blog/website-redesign-keep-google-rankings/">how to redesign a site without losing your Google rankings</a>.</p>
"""),
            ("What changes, and what stays", """
<p>Your name, your reputation and whatever already works stay. A page that brings in steady calls keeps its address and its best wording. What changes is everything that gets in a customer's way: slow pages, cramped phone layouts, buried phone numbers and forms that never arrive. If your logo needs a refresh too, I can do that at the same time.</p>
"""),
            ("Moving off WordPress, Wix or Squarespace", """
<p>Most sites I rebuild started on one of those. I move your words, photos and any page that's earning traffic, then rebuild the site by hand so it's quicker and has far less to maintain. If you'd rather stay on your current platform, tell me on the call and I'll say honestly whether a redesign there makes sense.</p>
"""),
        ],
        "included": [
            "Audit of the pages and searches that matter now",
            "Redirect map for every old page address",
            "New mobile layout with tap-to-call",
            "Your content moved and tightened up",
            "Faster pages with modern image formats",
            "A month of Search Console checks after launch",
        ],
        "faq": [
            ("Will I lose my Google rankings after a redesign?", "Not if it's handled properly. I keep your best pages at the same addresses where I can and redirect the rest, then watch Search Console after launch and fix anything that slips."),
            ("How much does a website redesign cost?", "Up to five pages is $1,500 at a fixed price. Bigger sites and stores get a fixed quote after a free 20-minute call."),
            ("Can I keep my domain name and email?", "Yes. Your domain and email stay exactly as they are. Only the website itself changes."),
            ("My site is on Wix. Can you redesign it?", "Yes. I bring across your content and any pages earning traffic, then rebuild the site so it loads faster and you're not tied to a monthly builder subscription."),
        ],
        "areas": ["fort-myers-fl", "cape-coral-fl", "bonita-springs-fl", "north-fort-myers-fl"],
        "posts": ["website-redesign-keep-google-rankings", "website-cost-fort-myers-cape-coral"],
    },
    {
        "slug": "local-seo",
        "name": "Local SEO and Google Business Profile",
        "short": "Local SEO",
        "icon": "pin",
        "hue": 145,
        "tags": ["Map results", "Business Profile", "Town pages"],
        "seo_title": "Local SEO & Google Business Profile, Fort Myers & Cape Coral",
        "description": "Local SEO for Lee County small businesses: Google Business Profile setup, town and service pages, and structured data so customers in Fort Myers and Cape Coral find you.",
        "h1": "Local SEO and Google Business Profile help in Lee County",
        "lede": "When someone in Cape Coral types \"near me\" into their phone, Google picks a handful of businesses to show. Local SEO is the plain, unglamorous work of making sure yours is one of them.",
        "price": "Included in every site",
        "time": "Set up at launch",
        "answer": "Local SEO means making your business easy for Google Maps, regular search results and AI assistants to find and trust when someone nearby looks for what you sell. For Lee County businesses I set up and tidy the Google Business Profile, write pages for the services and towns you actually cover, add structured data, and connect Search Console. The basics are included with every website I build, and I can also do them for a site you already have.",
        "sections": [
            ("Your Google Business Profile comes first", """
<p>For most local searches the map results appear above the regular links, and those come from Google Business Profiles, not websites. So I start there: the right primary category, your real service area, accurate hours (including the slow season and holidays), services, photos and a description written the way customers search. Then I make sure your name, phone number and address read exactly the same on your site and your profile.</p>
<p>If you work out of your truck or from home, you can hide your address and list the towns you serve instead. That's common in Lee County trades, and I'll set it up correctly.</p>
"""),
            ("Pages for the places you work", """
<p>A roofer based in Fort Myers who also works in Lehigh Acres and Bonita Springs needs the site to say so clearly. Where it makes sense I write a short page for each main service and each town you cover, with something specific to that place on every one. Copy and paste pages with only the town name swapped don't help, and Google has said as much.</p>
"""),
            ("Being the answer in AI search", """
<p>More people now ask ChatGPT, Gemini or Google's AI answers which business to call. Those tools lean on the same signals: a clear statement of what you do and where, structured data, consistent details across the web and real reviews. I write each page so the first lines answer the question a customer would ask, which is also what AI tools quote.</p>
"""),
            ("Reviews, without the tricks", """
<p>Reviews matter a lot for map rankings. I'll give you a short link and a simple routine for asking happy customers, plus template replies for good and bad reviews. I won't buy reviews, filter out unhappy customers or pad your listing with keywords. Those shortcuts get listings suspended.</p>
"""),
        ],
        "included": [
            "Google Business Profile audit and cleanup",
            "Correct categories, services and service area",
            "Matching business details across the web",
            "Service and town pages where they fit",
            "Structured data for search and AI tools",
            "Search Console and a simple review routine",
        ],
        "faq": [
            ("How long does local SEO take to work?", "Fixes to your Google Business Profile can show up within a few weeks. New pages usually take one to three months to settle. Anyone who promises the top spot is guessing."),
            ("Do I need an office address to show up on Google Maps?", "No. Service businesses can hide their address and list the towns they serve. You do need a real location where you're based; virtual offices break Google's rules."),
            ("Is local SEO included with a website?", "The basics are included with every site I build: Business Profile cleanup, structured data, Search Console and a sitemap. Town and service pages are part of the Business package or quoted separately."),
            ("Can you help with SEO if you didn't build my site?", "Yes. I start by looking at your Business Profile and your site, then tell you what's worth fixing first and what it would cost."),
        ],
        "areas": ["cape-coral-fl", "lehigh-acres-fl", "fort-myers-fl", "estero-fl"],
        "posts": ["google-business-profile-lee-county", "hurricane-season-website-checklist"],
    },
    {
        "slug": "logo-and-branding",
        "name": "Logo and brand identity",
        "short": "Logos and branding",
        "icon": "spark",
        "hue": 32,
        "tags": ["Logo files", "Colors and fonts", "One page guide"],
        "seo_title": "Logo Design & Branding for Fort Myers Small Businesses",
        "description": "Logo design and brand identity for Fort Myers, Cape Coral and Lee County small businesses: a logo that works on a truck, a shirt and a phone screen.",
        "h1": "Logo design and brand identity for Lee County businesses",
        "lede": "A good logo has to work at the size of a thumbnail and on the side of a box truck parked on Colonial Boulevard. I design simple marks with the colors, fonts and files to use them properly.",
        "price": "Fixed quote",
        "time": "2 to 3 weeks",
        "answer": "I design logos and small brand identities for businesses in Fort Myers, Cape Coral and the rest of Lee County. A project includes a primary logo and a compact version, a color palette, a font pairing, every file you'll need for print, signs and the web, and a one page guide on how to use them. Brand work is quoted at a fixed price after a short call, and it can be added to a website project.",
        "sections": [
            ("What you get", """
<ul>
<li>A main logo and a compact version for small spaces like a profile picture or an embroidered shirt.</li>
<li>A color palette that holds up in bright Florida sun, on a phone screen and on vinyl.</li>
<li>A font pairing for your website, menus and printed pieces.</li>
<li>Files for every job: vector files for sign shops and wraps, transparent PNGs, and a one color version.</li>
<li>A single page guide so whoever prints your next shirt or sign gets it right.</li>
</ul>
"""),
            ("How it goes", """
<p>We talk for half an hour about your customers, your competition and where the logo will live. I come back with two or three directions shown on real things like a van door, a business card and a social profile, not floating on a white page. You pick one, we refine it over two rounds, and you get the final files.</p>
"""),
            ("Built to work outdoors", """
<p>A lot of Lee County branding lives outside: on trucks, yard signs, boats, uniforms and shopfronts that sit in full sun all year. I avoid thin lines and pale colors that disappear in glare, and I test each logo in one color so it still works as a cut vinyl decal or a stitched patch.</p>
"""),
        ],
        "included": [
            "Main logo plus a compact version",
            "Color palette and font pairing",
            "Vector, PNG and one color files",
            "Mockups on signs, vehicles and screens",
            "A one page usage guide",
        ],
        "faq": [
            ("How much does a logo cost?", "Brand projects get a fixed quote after a free 20-minute call, based on how many pieces you need. It's often cheaper added to a website project."),
            ("Do I own the logo?", "Yes. Once the project is paid, the logo and all of its files are yours to use anywhere."),
            ("Can you freshen up my current logo instead?", "Often, yes. If people already know your logo, a careful cleanup can be the better choice. I'll tell you which I'd recommend."),
        ],
        "areas": ["fort-myers-fl", "bonita-springs-fl", "sanibel-fl", "cape-coral-fl"],
        "posts": [],
    },
    {
        "slug": "print-design",
        "name": "Print design",
        "short": "Print",
        "icon": "print",
        "hue": 350,
        "tags": ["Rack cards", "Door hangers", "Menus and signs"],
        "seo_title": "Print Design in Fort Myers: Rack Cards, Menus & Signs",
        "description": "Print design for Lee County small businesses: rack cards, door hangers, menus, flyers, yard signs and business cards, made to match your website.",
        "h1": "Print design for Fort Myers and Lee County businesses",
        "lede": "Rack cards in hotel lobbies, door hangers in new Cape Coral neighborhoods, menus that survive a humid patio. Print still earns its keep here, and it works best when it sends people to a website that's ready for them.",
        "price": "Fixed quote per piece",
        "time": "About 1 week",
        "answer": "I design print pieces for small businesses in Fort Myers, Cape Coral and around Lee County: rack cards, door hangers, flyers, menus, postcards, business cards and yard signs. Each piece is set up to your printer's exact specifications and matched to your website, often with a QR code that leads to the right page. Print design is quoted per piece at a fixed price.",
        "sections": [
            ("Pieces that work around here", """
<ul>
<li><strong>Rack cards</strong> for hotel, rental and visitor center displays, aimed at people deciding what to do this week.</li>
<li><strong>Door hangers and postcards</strong> for trades working new construction neighborhoods in Cape Coral and Lehigh Acres.</li>
<li><strong>Menus</strong> that stay readable on a bright patio and can be updated without starting from scratch.</li>
<li><strong>Yard signs and banners</strong> with a phone number big enough to read from a moving car.</li>
<li><strong>Business cards</strong> and appointment cards that match everything else.</li>
</ul>
"""),
            ("Print that sends people somewhere useful", """
<p>A QR code on a rack card is only useful if it opens a page made for that person. I can point each piece to its own page, such as a seasonal offer or a booking form, so you can see in your analytics how many people actually scanned it.</p>
"""),
            ("Ready for your printer", """
<p>Every file comes set up for the printer you use, local or online, with the right bleed, margins and color settings. I'm happy to talk to them directly so nothing gets lost in an email chain.</p>
"""),
        ],
        "included": [
            "Design matched to your brand and site",
            "Printer-ready files with bleed and margins",
            "QR codes pointing to the right page",
            "Two rounds of changes",
            "Editable templates for repeat pieces",
        ],
        "faq": [
            ("Do you print as well as design?", "I design and prepare the files, then hand them to your printer, or recommend one. You pay the printer directly, so there's no markup from me."),
            ("How much do rack cards or door hangers cost to design?", "Each piece gets a fixed quote after a quick call. Pieces designed alongside a website or logo usually cost less."),
            ("Can you redo a menu I already have?", "Yes. Send me the current one and I'll redesign it so it's easier to read and easier for you to update next season."),
        ],
        "areas": ["fort-myers-beach-fl", "sanibel-fl", "cape-coral-fl", "north-fort-myers-fl"],
        "posts": ["seasonal-business-website-southwest-florida"],
    },
    {
        "slug": "website-care-plans",
        "name": "Website care plans",
        "short": "Care plans",
        "icon": "shield",
        "hue": 185,
        "tags": ["Edits on request", "Storm updates", "Monthly checks"],
        "seo_title": "Website Care Plans for Lee County Small Businesses",
        "description": "Optional website care plans for Fort Myers and Cape Coral businesses: small edits, seasonal and storm updates, monthly checks and a short report. Cancel any time.",
        "h1": "Website care plans for Lee County small businesses",
        "lede": "You don't need one. But if you'd rather text me a change and forget about it, including the hours update when a storm closes you for three days, a care plan covers it.",
        "price": "Quoted monthly",
        "time": "Ongoing, cancel any time",
        "answer": "My care plans are an optional monthly service for owners who would rather not touch their own website. A plan covers small edits on request, seasonal hour and menu changes, closure notices during storms, monthly checks that the site, forms and Google listing are working, and a short monthly note on how it's doing. Plans are quoted based on how often things change, and you can stop any time.",
        "sections": [
            ("What's covered", """
<ul>
<li>Small edits whenever you need them: prices, photos, staff, specials.</li>
<li>Seasonal changes, like winter hours when visitors arrive and summer hours when they leave.</li>
<li>Closure and reopening notices during hurricane season, on the site and on your Google Business Profile.</li>
<li>A monthly check that pages load, forms deliver and nothing is broken.</li>
<li>A short monthly note: visits, calls and form enquiries, and anything worth changing.</li>
</ul>
"""),
            ("Storm season, handled", """
<p>When a storm is coming, the last thing you want is to be logging into a website. On a care plan you send me one text, and I post the closure notice, update your Google hours and put a banner on the site. When you reopen, one more text and it all changes back. My <a href="/blog/hurricane-season-website-checklist/">hurricane season checklist</a> covers what to prepare either way.</p>
"""),
            ("No lock-in", """
<p>You own the domain, code and hosting from the start, so a care plan never holds anything hostage. Stop whenever you like and everything stays exactly where it is.</p>
"""),
        ],
        "included": [
            "Edits on request, usually done the same day",
            "Seasonal hour and menu updates",
            "Storm closure notices on site and Google",
            "Monthly uptime, form and link checks",
            "A short monthly report",
        ],
        "faq": [
            ("Do I need a care plan?", "No. Every site I build is set up so you can run it yourself, and hosting is on your own account. A care plan is for people who'd rather hand it off."),
            ("How much is a care plan?", "It depends on how often your site changes, so I quote it after a quick chat. You can cancel any time."),
            ("Can I get a care plan for a site you didn't build?", "Sometimes. I'd need to look at how it's built first. If it's a heavily customised WordPress site, I may suggest a different approach."),
        ],
        "areas": ["fort-myers-beach-fl", "sanibel-fl", "bonita-springs-fl", "fort-myers-fl"],
        "posts": ["hurricane-season-website-checklist", "seasonal-business-website-southwest-florida"],
    },
]
