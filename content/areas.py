"""Town pages. Each entry becomes /areas/<slug>/.

Each page needs something true and specific to that place: how people there
search, the local business mix, and what I'd put on a site for a business there.
Never swap town names into the same text. Keep local facts to well known, checkable
ones. Examples are hypothetical and say so. Never claim an office or address in Lee
County: Daniel serves these towns by video call and email.
"""

AREAS = [
    {
        "slug": "fort-myers-fl",
        "town": "Fort Myers",
        "place": "Fort Myers, FL",
        "hue": 205,
        "blurb": "River District shops, trades and clinics",
        "seo_title": "Fort Myers Web Design for Small Businesses",
        "description": "Web design for Fort Myers, FL small businesses: fast, mobile-first websites from $500, built to show up when locals and visitors search.",
        "h1": "Web design for small businesses in Fort Myers, FL",
        "lede": "Fort Myers has two audiences at once: people who live here year round and a winter wave of visitors and seasonal residents. A good site speaks to both without making either one dig for the phone number.",
        "answer": "Lee County Websites makes fixed-price websites for local businesses in Fort Myers, Florida. A one-page site is $500 and a five-page site is $1,500, with the price set before any work begins. Every site loads quickly on a phone and is set up to appear in searches from year-round locals and seasonal visitors alike.",
        "sections": [
            ("Two kinds of customer, one website", """
<p>From January into April the city fills up with seasonal residents, spring training crowds heading to JetBlue Park and Hammond Stadium, and visitors staying near the River District. The rest of the year your customers are mostly neighbors. Those groups search differently. Visitors search \"near me\" and want hours, directions and whether you take walk-ins. Locals search by service and want to know you're reliable.</p>
<p>So a Fort Myers site needs hours that are easy to change by season, a short answer to \"are you near me\" for people who don't know the roads yet, and service pages that give locals a reason to call you rather than the next listing.</p>
"""),
            ("Businesses I build for in Fort Myers", """
<ul>
<li><strong>Restaurants, cafés and shops</strong> downtown and along McGregor Boulevard, where hours, menus and parking questions come first.</li>
<li><strong>Home services</strong> like air conditioning, pool care, roofing and pest control, where jobs go to whoever has a quick quote form and a plain list of the areas covered.</li>
<li><strong>Medical, dental and wellness practices</strong> that need clear new patient information and a simple way to book.</li>
<li><strong>Tour, rental and event businesses</strong> selling to visitors who plan from their phone.</li>
</ul>
"""),
            ("How I'd approach it", """
<p>Take a made-up example: an air conditioning company based off Colonial Boulevard. In August, a homeowner with a dead unit is searching on a phone in a hot house. The site I'd build opens with a big tap-to-call button, \"same day service in Fort Myers, Cape Coral and Lehigh Acres\", and a short form for people who'd rather text. Each main service gets its own page, and the Google Business Profile lists the same towns, word for word.</p>
"""),
        ],
        "checklist": [
            "Hours that change easily by season",
            "Clear service area for locals and newcomers",
            "Tap-to-call at the top of every page",
            "Directions and parking for walk-in businesses",
            "Business Profile that matches the site exactly",
        ],
        "faq": [
            ("How do we work together if you're not in my shop?", "Mostly over video and email. After a 20-minute kickoff, you follow the build on a private preview link, and I answer messages within one business day."),
            ("How much does a website cost in Fort Myers?", "It's $500 for a single-page site and $1,500 for a site with as many as five pages, and the price is locked in before I start."),
            ("Should my site mention seasonal visitors?", "If they're a real part of your business, yes. Say plainly what visitors need to know, like whether you take walk-ins, and keep your seasonal hours current."),
        ],
        "nearby": ["cape-coral-fl", "north-fort-myers-fl", "lehigh-acres-fl", "estero-fl"],
        "services": ["small-business-website-design", "local-seo", "website-care-plans"],
    },
    {
        "slug": "cape-coral-fl",
        "town": "Cape Coral",
        "place": "Cape Coral, FL",
        "hue": 190,
        "blurb": "Canal-front trades, marine and new builds",
        "seo_title": "Cape Coral Web Design for Small Businesses",
        "description": "Web design for Cape Coral, FL small businesses: mobile-first websites from $500 for trades, marine services, restaurants and shops.",
        "h1": "Web design for small businesses in Cape Coral, FL",
        "lede": "Cape Coral is the biggest city in Lee County and still growing, with new homes going up across the north end and a canal system longer than most people can picture. The businesses that keep it running need websites that work as hard as they do.",
        "answer": "Lee County Websites makes fixed-price websites for local businesses in Cape Coral, Florida, including trades, marine services, restaurants and shops. A one-page site is $500 and a five-page site is $1,500, with the price set before any work begins. Every site is designed for phones first and set up to show up in Cape Coral searches and map results.",
        "sections": [
            ("A city of new homeowners", """
<p>A lot of Cape Coral residents arrived recently, so they don't have a go-to plumber, pool company or dentist yet. They search, read a couple of websites and call whoever looks most trustworthy and clearly covers their part of the city. Naming the areas you work, like the southeast, the northwest or along Pine Island Road, helps a new resident feel sure you'll come out to them.</p>
"""),
            ("Built around the water", """
<p>With hundreds of miles of canals, Cape Coral has a big marine economy: boat lifts, dock and seawall builders, detailing, mobile mechanics, charters and rentals. Those customers want to see your work and know you handle their kind of job. For a marine business I'd lead with real project photos, the services you actually offer and a quote form that asks the right questions, like boat length or lift capacity, so your first call is a useful one.</p>
"""),
            ("What that could look like", """
<p>Picture a made-up fishing charter that runs out of Cape Coral. Most bookings come from visitors planning a trip a few weeks ahead, often on a phone. The site would open with trip lengths, prices and what's included, then a booking request form with dates and party size. A short page answers the usual questions: what to bring, whether licenses are covered, what happens if the weather turns.</p>
"""),
        ],
        "checklist": [
            "Parts of the city you serve, named plainly",
            "Real project photos, not stock pictures",
            "Quote forms that ask the right questions",
            "Booking requests for charters and rentals",
            "Business Profile categories that fit your trade",
        ],
        "faq": [
            ("How do we work together?", "Over video and email. Progress shows up on a private preview link and I answer within one business day, so you don't need to take time off the job."),
            ("How much does a website cost in Cape Coral?", "It's $500 for a single-page site and $1,500 for a site with as many as five pages, and the price is locked in before I start."),
            ("Can you help my business show up in Cape Coral map results?", "Yes. I configure your Google Business Profile with accurate categories and a service area, match your details everywhere, and give you a simple way to ask for reviews."),
        ],
        "nearby": ["fort-myers-fl", "north-fort-myers-fl", "lehigh-acres-fl", "sanibel-fl"],
        "services": ["small-business-website-design", "local-seo", "print-design"],
    },
    {
        "slug": "bonita-springs-fl",
        "town": "Bonita Springs",
        "place": "Bonita Springs, FL",
        "hue": 160,
        "blurb": "Beach, golf and wellness between two cities",
        "seo_title": "Bonita Springs Web Design for Small Businesses",
        "description": "Web design for Bonita Springs, FL small businesses: polished, fast websites from $500 for wellness, home services, dining and retail.",
        "h1": "Web design for small businesses in Bonita Springs, FL",
        "lede": "Bonita Springs sits between Fort Myers and Naples, and its customers come from both directions. Many of them have high expectations and very little patience for a clunky website.",
        "answer": "Lee County Websites makes fixed-price websites for local businesses in Bonita Springs, Florida. A one-page site is $500 and a five-page site is $1,500, with the price set before any work begins. They're built to look polished, load fast on a phone and show up for customers searching from Bonita, Estero and the north end of Naples.",
        "sections": [
            ("Customers from both sides of the county line", """
<p>Being in the far south of Lee County means plenty of your customers live in Collier County, just across the line. If you serve both, the site should say so: Bonita Springs, Estero and the parts of Naples you'll travel to. That one clear sentence keeps you in front of people searching from either side.</p>
"""),
            ("Polish matters here", """
<p>Bonita has a lot of golf and gated communities, a busy wellness and medical scene, and dining and shops around the old downtown along the Imperial River. Customers compare options carefully. A clean design with good photos, clear prices or price ranges, and easy booking does a lot of the selling before anyone calls.</p>
"""),
            ("What that could look like", """
<p>Say a made-up massage and skincare studio near Bonita Beach Road. The site would show the treatments with lengths and prices, a gallery of the actual rooms, gift cards for visiting family, and a booking button that goes straight to their scheduling tool. A short page for seasonal residents explains how to book ahead for the busy months.</p>
"""),
        ],
        "checklist": [
            "Service area covering Bonita, Estero and nearby",
            "Real photos of your space or work",
            "Prices or clear price ranges",
            "Booking or gift cards on the first screen",
            "Seasonal booking notes for winter residents",
        ],
        "faq": [
            ("Do you build sites for businesses near Naples too?", "Yes. Plenty of Bonita businesses serve Naples customers, and I'll write the site to cover both clearly. I work by video call and email, so distance doesn't matter."),
            ("How much does a website cost in Bonita Springs?", "It's $500 for a single-page site and $1,500 for a site with as many as five pages, and the price is locked in before I start."),
            ("Can my site connect to my booking software?", "Usually, yes. Most scheduling tools offer a booking link or an embed. More involved setups are a Custom project with a fixed quote."),
        ],
        "nearby": ["estero-fl", "fort-myers-beach-fl", "fort-myers-fl", "lehigh-acres-fl"],
        "services": ["small-business-website-design", "logo-and-branding", "website-redesign"],
    },
    {
        "slug": "estero-fl",
        "town": "Estero",
        "place": "Estero, FL",
        "hue": 230,
        "blurb": "Shopping, students and growing neighborhoods",
        "seo_title": "Estero Web Design for Small Businesses",
        "description": "Web design for Estero, FL small businesses: mobile-first websites from $500 for restaurants, retail, fitness, clinics and home services.",
        "h1": "Web design for small businesses in Estero, FL",
        "lede": "Estero is one of Lee County's younger municipalities, with big shopping destinations, a university nearby and new neighborhoods filling in around them. That mix of shoppers, students and families searches on phones, constantly.",
        "answer": "Lee County Websites makes fixed-price websites for local businesses in Estero, Florida. A one-page site is $500 and a five-page site is $1,500, with the price set before any work begins. Every site is designed for phones first, with clear hours, location details and booking, so shoppers, students and new residents can act on the spot.",
        "sections": [
            ("Where people already go", """
<p>Coconut Point, Miromar Outlets and Hertz Arena pull in crowds from across the region, and Florida Gulf Coast University brings students and staff close by. If you're near one of those, say so, because it's how people find their way to you. \"Two minutes from Coconut Point\" is more useful to a visitor than a street address they don't recognize.</p>
"""),
            ("Families settling in", """
<p>A lot of Estero's newer neighborhoods are full of families looking for dentists, pediatricians, tutors, gyms, cleaners and lawn care for the first time. They read reviews and websites closely. Pages that explain how a first visit works, what it costs and how to book give them the confidence to pick you.</p>
"""),
            ("What that could look like", """
<p>Imagine a made-up boutique fitness studio near Estero Parkway. The site would put the class schedule right up front, offer a first class free with a short sign-up form, and have a page that explains what to expect for complete beginners. The Google Business Profile would match the class times and link straight to sign-up.</p>
"""),
        ],
        "checklist": [
            "Location described by nearby landmarks",
            "First visit or first class explained",
            "Schedule, menu or hours up front",
            "Simple online booking or sign-up",
            "Business Profile that matches the site",
        ],
        "faq": [
            ("How do we work together?", "Video calls and email, plus a private preview link where you can watch the site take shape. Expect an answer from me within one business day."),
            ("How much does a website cost in Estero?", "It's $500 for a single-page site and $1,500 for a site with as many as five pages, and the price is locked in before I start."),
            ("Can you add a class schedule or menu I can update myself?", "Yes. I set up anything that changes often so you can edit it without calling me."),
        ],
        "nearby": ["bonita-springs-fl", "fort-myers-fl", "fort-myers-beach-fl", "lehigh-acres-fl"],
        "services": ["small-business-website-design", "local-seo", "website-care-plans"],
    },
    {
        "slug": "lehigh-acres-fl",
        "town": "Lehigh Acres",
        "place": "Lehigh Acres, FL",
        "hue": 95,
        "blurb": "Fast-growing, trades-heavy, bilingual",
        "seo_title": "Lehigh Acres Web Design for Small Businesses",
        "description": "Web design for Lehigh Acres, FL small businesses: affordable, fast websites from $500 for contractors and local services, with optional Spanish pages.",
        "h1": "Web design for small businesses in Lehigh Acres, FL",
        "lede": "Lehigh Acres is a huge, fast-growing community east of Fort Myers, with new homes on what used to be empty lots and plenty of contractors, landscapers and local services working to keep up.",
        "answer": "Lee County Websites makes fixed-price websites for local businesses in Lehigh Acres, Florida. A one-page site is $500 and a five-page site is $1,500, with the price set before any work begins. They're built for phones first, can include Spanish language pages, and are set up so local customers can find you on Google Maps.",
        "sections": [
            ("Trades and services first", """
<p>A lot of Lehigh's businesses are owner operated: general contractors, concrete and pavers, lawn care, fencing, mobile mechanics, cleaners and handymen. Many get most of their work from referrals and Facebook groups, which works until a customer looks you up and finds nothing. A simple, professional site with your services, photos of your work and a quote form turns that word of mouth into a call.</p>
"""),
            ("Speak your customers' language", """
<p>Many Lehigh Acres households are more comfortable in Spanish. If that's true of your customers, a site with Spanish versions of the key pages is easy to set up and tells people straight away that you'll understand them. I build them as proper pages Google can show to Spanish searchers, not an automatic translate button.</p>
"""),
            ("What that could look like", """
<p>Take a made-up pavers and driveway company. Its home page leads with a photo of a finished driveway, the towns covered (Lehigh Acres, Fort Myers, Cape Coral), and a quote form that asks for the size of the job and a couple of photos. A gallery page shows before and after pairs, and each page has an English and Spanish version.</p>
"""),
        ],
        "checklist": [
            "Services and towns covered, front and center",
            "Photos of your real work",
            "Quote form that accepts photos",
            "Optional Spanish versions of key pages",
            "A Google Business Profile with a service area",
        ],
        "faq": [
            ("Can my website be in English and Spanish?", "Yes. I build proper Spanish versions of the pages that matter, so Google can show them to people searching in Spanish."),
            ("How much does a website cost in Lehigh Acres?", "It's $500 for a single-page site and $1,500 for a site with as many as five pages, and the price is locked in before I start."),
            ("I work from my truck. Can I still show up on Google Maps?", "Yes. You can hide your home address and list the areas you serve. I'll set that up correctly."),
        ],
        "nearby": ["fort-myers-fl", "cape-coral-fl", "estero-fl", "north-fort-myers-fl"],
        "services": ["small-business-website-design", "local-seo", "print-design"],
    },
    {
        "slug": "sanibel-fl",
        "town": "Sanibel",
        "place": "Sanibel, FL",
        "hue": 45,
        "blurb": "Island rentals, tours, dining and shops",
        "seo_title": "Sanibel Island Web Design for Small Businesses",
        "description": "Web design for Sanibel, FL small businesses: websites from $500 for rentals, tours, restaurants and shops, built for visitors planning a trip.",
        "h1": "Web design for small businesses on Sanibel Island",
        "lede": "Most of a Sanibel business's customers make up their mind before they cross the causeway. Your website is where they decide, often months ahead and on a phone in another state.",
        "answer": "Lee County Websites makes fixed-price websites for local businesses on Sanibel Island, Florida, including vacation rentals, tours, restaurants and shops. A one-page site is $500 and a five-page site is $1,500, with the price set before any work begins. Each one is built for visitors planning a trip: clear availability, prices, directions and booking, fast on a phone.",
        "sections": [
            ("Selling to people who aren't here yet", """
<p>Sanibel is known for shelling, beaches and the J.N. \"Ding\" Darling National Wildlife Refuge, and the people who come for those things plan carefully. They compare rentals, tours and places to eat from home. The questions they ask are practical: is it open, what does it cost, how do I book, and how far is it from where I'm staying. A site that answers those quickly gets the booking.</p>
"""),
            ("Show that you're open", """
<p>Since Hurricane Ian in 2022, many island businesses have rebuilt, reopened or moved. Visitors still wonder what's open. A clear \"open daily\" line with current hours, recent photos and an updated Google Business Profile removes that doubt, and it's worth checking every season.</p>
"""),
            ("What that could look like", """
<p>Consider a made-up beach cottage rental near the lighthouse end of the island. The site would lead with photos, the number of guests and bedrooms, rates by season and an availability calendar or booking link. A short local guide covers parking, bikes and the best shelling times, which also gives Google more reasons to show the page.</p>
"""),
        ],
        "checklist": [
            "Open status and current hours, always",
            "Prices or seasonal rates you can update",
            "Booking or availability on the first screen",
            "Recent photos of the real place",
            "Practical visitor info: parking, bikes, directions",
        ],
        "faq": [
            ("How do we work together?", "Over video calls and email, with a private preview link. Nothing needs to happen in person."),
            ("How much does a website cost for a Sanibel business?", "It's $500 for a single-page site and $1,500 for a site with as many as five pages, and the price is locked in before I start. Booking engines and larger rental sites get a fixed quote."),
            ("Can you connect my rental calendar?", "Usually. Most rental and booking platforms offer a calendar or booking link that can sit on your site. I'll check yours on our first call."),
        ],
        "nearby": ["fort-myers-beach-fl", "cape-coral-fl", "fort-myers-fl", "bonita-springs-fl"],
        "services": ["small-business-website-design", "print-design", "website-care-plans"],
    },
    {
        "slug": "north-fort-myers-fl",
        "town": "North Fort Myers",
        "place": "North Fort Myers, FL",
        "hue": 15,
        "blurb": "Across the river: retirees, boaters, trades",
        "seo_title": "North Fort Myers Web Design for Small Businesses",
        "description": "Web design for North Fort Myers, FL small businesses: clear, easy-to-read websites from $500 for home services, repair shops, marine and local retail.",
        "h1": "Web design for small businesses in North Fort Myers, FL",
        "lede": "North of the Caloosahatchee, North Fort Myers has a steady, loyal customer base with many retirees and long-time residents. They value clear information and a real person who picks up the phone.",
        "answer": "Lee County Websites makes fixed-price websites for local businesses in North Fort Myers, Florida. A one-page site is $500 and a five-page site is $1,500, with the price set before any work begins. They're designed to be easy to read, with large text and a phone number front and center, and set up to show up in local searches north of the river.",
        "sections": [
            ("Easy to read, easy to call", """
<p>A lot of customers here are retirees in established neighborhoods and manufactured home communities. That means larger text, strong contrast, plain wording and a phone number that's impossible to miss. Accessible design isn't a niche feature in North Fort Myers; it's how you keep a caller from giving up.</p>
"""),
            ("Your side of the river", """
<p>For many people here, crossing a bridge into Fort Myers is a real trip, so they look for businesses close by. If you're north of the river, say so plainly, along with the roads people know, like Business 41, Pondella Road or Bayshore Road. It helps you show up for searches from North Fort Myers and nearby Cape Coral.</p>
"""),
            ("What that could look like", """
<p>Picture a made-up small engine and golf cart repair shop. The site would put the phone number and hours at the top in large type, list what they fix and whether they offer pickup, and include a simple map. A short page explains how long typical repairs take and what they cost, so customers know before they call.</p>
"""),
        ],
        "checklist": [
            "Large text and strong contrast",
            "Phone number pinned to every page",
            "Local roads and landmarks named",
            "Typical prices and turnaround explained",
            "Business Profile with current hours",
        ],
        "faq": [
            ("Can you make my site easy for older customers to use?", "Yes. I design with large, readable text, high contrast and clear buttons as standard, and I check it against accessibility guidelines."),
            ("How much does a website cost in North Fort Myers?", "It's $500 for a single-page site and $1,500 for a site with as many as five pages, and the price is locked in before I start."),
            ("Do you also serve Pine Island and Cape Coral?", "Yes. I work with businesses anywhere in Lee County, and I'll make sure your site names the areas you actually cover."),
        ],
        "nearby": ["cape-coral-fl", "fort-myers-fl", "lehigh-acres-fl", "sanibel-fl"],
        "services": ["small-business-website-design", "website-redesign", "local-seo"],
    },
    {
        "slug": "fort-myers-beach-fl",
        "town": "Fort Myers Beach",
        "place": "Fort Myers Beach, FL",
        "hue": 330,
        "blurb": "Rebuilding beach town, visitors year round",
        "seo_title": "Fort Myers Beach Web Design for Small Businesses",
        "description": "Web design for Fort Myers Beach, FL businesses: fast, visitor-friendly websites from $500 for rentals, restaurants, watersports and shops.",
        "h1": "Web design for small businesses on Fort Myers Beach",
        "lede": "Fort Myers Beach has been rebuilding since Hurricane Ian, and visitors are coming back to a town that looks different from the one they remember. A current website is how they find out you're here and open.",
        "answer": "Lee County Websites makes fixed-price websites for local businesses on Fort Myers Beach, Florida, including rentals, restaurants, watersports and shops. A one-page site is $500 and a five-page site is $1,500, with the price set before any work begins. Each one is built for visitors on a phone: current hours, location, prices and booking right on the first screen.",
        "sections": [
            ("Tell people what's changed", """
<p>Many businesses on Estero Island reopened in new buildings, temporary spaces or new locations after the 2022 storm. Returning visitors search for the places they remember and often find old information. A site that clearly says where you are now, what you offer and when you're open, backed by a matching Google Business Profile, wins those searches.</p>
"""),
            ("Decisions made on the sand", """
<p>A lot of beach customers decide on the spot, standing on the sand or walking toward Times Square, looking for lunch, a parasail, a bike or a boat. They need prices, hours and a booking button without scrolling. Heavy pages and pop-ups lose them on a weak beach signal, so I keep pages light and fast.</p>
"""),
            ("What that could look like", """
<p>Think of a made-up watersports rental near the pier. The site opens with today's hours and a weather note you can change in seconds, a short price list for jet skis, paddleboards and parasailing, and a booking button. A page covers what to bring, age limits and the cancellation policy for bad weather.</p>
"""),
        ],
        "checklist": [
            "Where you are now, stated plainly",
            "Today's hours and a quick status note",
            "Prices and booking without scrolling",
            "Light pages for weak beach signal",
            "Business Profile updated with your new details",
        ],
        "faq": [
            ("We reopened in a new spot. How do we make sure people find us?", "Update your Google Business Profile with the new address and hours, put the new location clearly on your site, and ask a few regulars for fresh reviews. I can handle all of that for you."),
            ("How much does a website cost on Fort Myers Beach?", "It's $500 for a single-page site and $1,500 for a site with as many as five pages, and the price is locked in before I start."),
            ("Can I change my hours quickly when the weather turns?", "Yes. I set up a quick status note you can edit from your phone, and a care plan can cover storm updates for you."),
        ],
        "nearby": ["sanibel-fl", "estero-fl", "bonita-springs-fl", "fort-myers-fl"],
        "services": ["small-business-website-design", "website-care-plans", "print-design"],
    },
]
