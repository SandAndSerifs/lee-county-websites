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
<p>Take an example: an air conditioning company based off Colonial Boulevard. In August, a homeowner with a dead unit is searching on a phone in a hot house. The site I'd build opens with a big tap-to-call button, \"same day service in Fort Myers, Cape Coral and Lehigh Acres\", and a short form for people who'd rather text. Each main service gets its own page, and the Google Business Profile lists the same towns, word for word.</p>
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
<p>Picture a fishing charter that runs out of Cape Coral. Most bookings come from visitors planning a trip a few weeks ahead, often on a phone. The site would open with trip lengths, prices and what's included, then a booking request form with dates and party size. A short page answers the usual questions: what to bring, whether licenses are covered, what happens if the weather turns.</p>
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
<p>Say a massage and skincare studio near Bonita Beach Road. The site would show the treatments with lengths and prices, a gallery of the actual rooms, gift cards for visiting family, and a booking button that goes straight to their scheduling tool. A short page for seasonal residents explains how to book ahead for the busy months.</p>
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
<p>Imagine a boutique fitness studio near Estero Parkway. The site would put the class schedule right up front, offer a first class free with a short sign-up form, and have a page that explains what to expect for complete beginners. The Google Business Profile would match the class times and link straight to sign-up.</p>
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
<p>Take a pavers and driveway company. Its home page leads with a photo of a finished driveway, the towns covered (Lehigh Acres, Fort Myers, Cape Coral), and a quote form that asks for the size of the job and a couple of photos. A gallery page shows before and after pairs, and each page has an English and Spanish version.</p>
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
<p>Consider a beach cottage rental near the lighthouse end of the island. The site would lead with photos, the number of guests and bedrooms, rates by season and an availability calendar or booking link. A short local guide covers parking, bikes and the best shelling times, which also gives Google more reasons to show the page.</p>
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
<p>Picture a small engine and golf cart repair shop. The site would put the phone number and hours at the top in large type, list what they fix and whether they offer pickup, and include a simple map. A short page explains how long typical repairs take and what they cost, so customers know before they call.</p>
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
<p>Think of a watersports rental near the pier. The site opens with today's hours and a weather note you can change in seconds, a short price list for jet skis, paddleboards and parasailing, and a booking button. A page covers what to bring, age limits and the cancellation policy for bad weather.</p>
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
    {
        "slug": "pine-island-fl",
        "town": "Pine Island",
        "place": "Pine Island, FL",
        "hue": 135,
        "blurb": "Matlacha galleries, groves, nurseries, fishing",
        "seo_title": "Pine Island & Matlacha Web Design for Small Businesses",
        "description": "Web design for Pine Island and Matlacha, FL small businesses: websites from $500 for galleries, nurseries, fruit stands, fishing guides and rentals.",
        "h1": "Web design for small businesses on Pine Island and in Matlacha",
        "lede": "Pine Island is Old Florida on purpose: fruit groves and plant nurseries along Stringfellow Road, fishing villages at either end, and the painted galleries of Matlacha on the way in. Businesses here are small and personal, and their websites should feel the same.",
        "answer": "Lee County Websites makes fixed-price websites for local businesses on Pine Island and in Matlacha, Florida, including galleries, nurseries, fruit stands, fishing guides and rentals. A one-page site is $500 and a five-page site is $1,500, with the price set before any work begins. Each one shows what you make or offer, when you're open and how to find you, in a way that suits the island.",
        "sections": [
            ("Two very different customers", """
<p>Plenty of Pine Island businesses sell to two groups at once. Landscapers and homeowners from across the county come for palms, tropical plants and fruit trees, and they want to know what's in stock and whether you deliver. Day trippers come for Matlacha's galleries, a seafood lunch and a few hours fishing off the bridge locals call the \"fishingest bridge in the world\", and they want to know what's open today. One site can serve both if it's organized around those two questions.</p>
"""),
            ("Where on the island you are", """
<p>The island has several communities, and people don't always know them apart. Bokeelia and Pineland sit up north, Pine Island Center is in the middle, and St. James City, the hub for fishing and watersports, is at the south tip. Matlacha is on its own small island along Pine Island Road, the way in from Cape Coral. Saying which one you're in, and how long the drive is from the Matlacha bridge, saves a visitor a wrong turn.</p>
<p>The island was hit hard by Hurricane Ian in 2022, and not everything has reopened. A current \"we're open\" line with this season's hours is worth more here than most anywhere.</p>
"""),
            ("What that could look like", """
<p>Take a tropical fruit nursery off Stringfellow Road. The home page would show what's ripe or in stock this month (mango, lychee, avocado trees, palms) on a list the owner can update from a phone, the farm stand hours, and whether they deliver to Cape Coral and Fort Myers. A second page covers wholesale orders for landscapers, with a simple request form.</p>
"""),
        ],
        "checklist": [
            "Which island community you're in",
            "What's in stock or on the wall this month",
            "Hours you can change by season",
            "Delivery or wholesale details for mainland buyers",
            "Photos of your real place and work",
        ],
        "faq": [
            ("I mostly sell at my stand or gallery. Do I need a website?", "If people drive out to see you, yes. A simple site tells them what you have, when you're open and that the trip is worth it. A one-page $500 site covers that well."),
            ("What does a website cost for a Pine Island business?", "It's $500 for a one-page site and $1,500 for up to five pages, with the price agreed before I start."),
            ("Can I update my own stock list or art?", "Yes. I set up the parts that change often so you can edit them yourself without calling me."),
        ],
        "nearby": ["cape-coral-fl", "north-fort-myers-fl", "captiva-fl", "boca-grande-fl"],
        "services": ["small-business-website-design", "logo-and-branding", "print-design"],
    },
    {
        "slug": "san-carlos-park-fl",
        "town": "San Carlos Park",
        "place": "San Carlos Park, FL",
        "hue": 250,
        "blurb": "Neighborhood services and shops off Alico Road",
        "seo_title": "San Carlos Park Web Design for Small Businesses",
        "description": "Web design for San Carlos Park, FL small businesses: affordable, phone-first websites from $500 for home services, contractors, auto shops and local stores.",
        "h1": "Web design for small businesses in San Carlos Park, FL",
        "lede": "San Carlos Park is a busy residential community between Fort Myers and Estero, with US 41 along its west side and the Alico Road business parks just to the north. A lot of hard-working local businesses are based here, and many of them still rely on word of mouth alone.",
        "answer": "Lee County Websites makes fixed-price websites for local businesses in San Carlos Park, Florida, including home services, contractors, auto shops and neighborhood stores. A one-page site is $500 and a five-page site is $1,500, with the price set before any work begins. Each one is built for phones first and set up so nearby customers in San Carlos Park, Estero and south Fort Myers can find you.",
        "sections": [
            ("A place people don't always know by name", """
<p>San Carlos Park is unincorporated, and a lot of its addresses say Fort Myers. That means customers may not search for it by name. A site that says \"San Carlos Park, off US 41 between Fort Myers and Estero\" covers both: people who know the community and people who only know the main roads.</p>
"""),
            ("Businesses that run out of a warehouse unit", """
<p>Between US 41 and I-75, the Alico Road corridor is full of commercial and industrial parks. Cabinet makers, sign shops, pool suppliers, auto and boat repair and contractors work out of units there. Customers rarely walk in, so the website is their first look. Clear photos of finished work, the towns you cover and a quote form that takes photos do most of the selling.</p>
"""),
            ("What that could look like", """
<p>Imagine a custom cabinet and countertop shop in a unit off Alico Road. The home page would lead with a kitchen they built, the areas they install in (San Carlos Park, Estero, Bonita Springs, Fort Myers), and a request form that asks for room measurements and a photo. A gallery page groups jobs by room, and a short page explains how long a typical job takes from measure to install.</p>
"""),
        ],
        "checklist": [
            "Main roads people know, named plainly",
            "Towns you serve beyond San Carlos Park",
            "Quote form that accepts photos",
            "A gallery of finished jobs",
            "Hours and whether walk-ins are welcome",
        ],
        "faq": [
            ("My address says Fort Myers. Should my site say San Carlos Park?", "Say both. Use your real mailing address, and describe where you are in words locals use, like San Carlos Park or off Alico Road. That covers every way people search."),
            ("How much is a website for a San Carlos Park business?", "A one-page site is $500 and a site with up to five pages is $1,500. The price is agreed before any work starts."),
            ("We get most work from referrals. What would a site add?", "A place to send people. When someone hears your name and looks you up, a clear site with your work and a quote form turns that referral into a call."),
        ],
        "nearby": ["estero-fl", "fort-myers-fl", "gateway-fl", "bonita-springs-fl"],
        "services": ["small-business-website-design", "local-seo", "website-redesign"],
    },
    {
        "slug": "alva-fl",
        "town": "Alva",
        "place": "Alva, FL",
        "hue": 75,
        "blurb": "Ranches, farms and river life out east",
        "seo_title": "Alva Web Design for Small Businesses",
        "description": "Web design for Alva, FL small businesses: simple, fast websites from $500 for farms, horse barns, nurseries, river guides and rural trades.",
        "h1": "Web design for small businesses in Alva, FL",
        "lede": "Alva is the country side of Lee County: a small community on the Caloosahatchee River along State Road 80, with farms, ranches and big lots between Fort Myers and LaBelle. Businesses here are often a family and a few acres, and the website should be just as straightforward.",
        "answer": "Lee County Websites makes fixed-price websites for local businesses in Alva, Florida, including farms, horse barns, nurseries, river guides and rural trades. A one-page site is $500 and a five-page site is $1,500, with the price set before any work begins. Each one is light enough to load on a slow country connection and tells people exactly how to find you.",
        "sections": [
            ("Getting people down the right road", """
<p>Rural addresses trip up map apps, and the last mile is often a dirt road or an unmarked gate. A good Alva site gives plain directions from State Road 80 or North River Road, says where to park a truck and trailer, and lists the hours someone is there to open up. That one section prevents a lot of lost visitors and missed sales.</p>
"""),
            ("Built for the way people out here live", """
<p>Alva draws riders and campers to Caloosahatchee Regional Park's equestrian and bike trails, boaters through the W.P. Franklin Lock, and families looking for land, horses and a slower pace. That supports boarding barns, riding lessons, farm stands, feed and tack, fishing guides, well and septic services, fencing and land clearing. Many of those customers are on a phone with weak signal, so I keep pages light, photos compressed and the phone number at the top.</p>
"""),
            ("What that could look like", """
<p>Picture a horse boarding barn off North River Road. The site would show the barn, paddocks and arena in real photos, list boarding options with prices or price ranges, and explain what's included, like feed, turnout and stall cleaning. A short form lets an owner ask about openings and book a visit, and a directions section covers the trailer entrance.</p>
"""),
        ],
        "checklist": [
            "Directions that work on rural roads",
            "Light pages for slow connections",
            "Phone number at the top of every page",
            "Real photos of your land, animals or work",
            "Prices or price ranges and what's included",
        ],
        "faq": [
            ("My customers mostly call or text. Is a website worth it?", "Yes, as long as it makes calling and texting easy. Most visitors will just check who you are, what you offer and how to reach you, so that's what I put first."),
            ("What does a website cost for an Alva business?", "$500 for a one-page site or $1,500 for up to five pages, settled before I start."),
            ("Can you help with a logo or signs for the farm too?", "Yes. I do logos, flyers and print design as well, so your sign, truck and website can match."),
        ],
        "nearby": ["lehigh-acres-fl", "north-fort-myers-fl", "fort-myers-fl", "gateway-fl"],
        "services": ["small-business-website-design", "logo-and-branding", "print-design"],
    },
    {
        "slug": "captiva-fl",
        "town": "Captiva",
        "place": "Captiva, FL",
        "hue": 300,
        "blurb": "Sunsets, weddings, boat trips and rentals",
        "seo_title": "Captiva Island Web Design for Small Businesses",
        "description": "Web design for Captiva, FL small businesses: websites from $500 for rentals, restaurants, boat tours, wedding pros and galleries on Captiva Island.",
        "h1": "Web design for small businesses on Captiva Island",
        "lede": "Captiva is a narrow island at the end of the road, past Sanibel and over the Blind Pass bridge. It's known for sunsets over the Gulf, a small village of restaurants and galleries, and boat trips to islands you can't drive to. Its customers plan trips around a feeling, and your site has to deliver it.",
        "answer": "Lee County Websites makes fixed-price websites for local businesses on Captiva Island, Florida, including rentals, restaurants, boat tours, wedding pros and galleries. A one-page site is $500 and a five-page site is $1,500, with the price set before any work begins. Each one is built for visitors planning ahead: strong photos, clear prices and dates, and a booking or inquiry button on the first screen.",
        "sections": [
            ("Selling an evening, not just a service", """
<p>People come to Captiva for sunset dinners, beach weddings, boat trips to Cabbage Key and Cayo Costa, and a slower few days than the mainland offers. They often book from far away and months ahead. A site that shows the experience in real photos, then answers the practical questions (price, dates, what's included, how to get here) is the one that gets the inquiry.</p>
"""),
            ("Help visitors with the drive", """
<p>Getting to Captiva means the Sanibel Causeway and the full length of Sanibel first, so timing matters, especially for anything at sunset. A short \"getting here\" note with realistic drive times from the causeway, parking details and when to leave keeps guests from showing up late and unhappy.</p>
<p>The island has also been through Hurricane Ian in 2022 and Milton in 2024. Recent photos and a clear line about what's open now reassure people who remember the news.</p>
"""),
            ("What that could look like", """
<p>Consider a wedding photographer who shoots on Captiva's beaches. The site would open with a few of their best sunset ceremonies, then packages with prices or starting prices, the beaches and venues they work at, and an inquiry form that asks for the date and guest count. A planning page covers beach rules, the best months and how to time a ceremony to the sunset.</p>
"""),
        ],
        "checklist": [
            "Photos that show the real experience",
            "Prices, packages or starting rates",
            "Inquiry or booking on the first screen",
            "Getting here: drive time, parking, timing",
            "A clear line about what's open now",
        ],
        "faq": [
            ("Most of my clients book from out of state. Does that change the site?", "It changes the priorities. People planning from afar need more detail on dates, prices, travel and what to expect, and they need to trust you without meeting you. I build for that."),
            ("What does a Captiva business website cost?", "$500 for a single page or $1,500 for up to five pages, agreed up front. Larger booking setups get a fixed quote."),
            ("Can visitors book or pay online?", "Usually, yes. Most booking and payment tools give you a link or a widget that can sit on your site. I'll look at yours on our first call."),
        ],
        "nearby": ["sanibel-fl", "pine-island-fl", "fort-myers-beach-fl", "boca-grande-fl"],
        "services": ["small-business-website-design", "logo-and-branding", "website-care-plans"],
    },
    {
        "slug": "boca-grande-fl",
        "town": "Boca Grande",
        "place": "Boca Grande, FL",
        "hue": 175,
        "blurb": "Tarpon season, golf carts and island homes",
        "seo_title": "Boca Grande Web Design for Small Businesses",
        "description": "Web design for Boca Grande, FL small businesses: refined websites from $500 for fishing guides, rentals, shops, home watch and island trades.",
        "h1": "Web design for small businesses in Boca Grande, FL",
        "lede": "Boca Grande is a quiet village at the south end of Gasparilla Island, reached by a toll causeway and best explored by golf cart. Many homes belong to seasonal owners, and every spring and summer anglers arrive for the tarpon in Boca Grande Pass. That makes for a small, discerning market that plans ahead.",
        "answer": "Lee County Websites makes fixed-price websites for local businesses in Boca Grande, Florida, including fishing guides, rentals, shops, home watch and island trades. A one-page site is $500 and a five-page site is $1,500, with the price set before any work begins. Each one is designed to look refined, load quickly and make it easy for seasonal residents and visiting anglers to book.",
        "sections": [
            ("Owners who aren't here all year", """
<p>A lot of Boca Grande homes sit empty part of the year, and their owners hire people they trust to look after them: home watch, property managers, landscapers, pool care, cleaners and contractors, many of whom come over the causeway from the mainland. Those owners hire from a distance, so the site has to earn trust on its own: who you are, what each visit includes, how you report back and how you handle storm prep.</p>
"""),
            ("Tarpon season books early", """
<p>Boca Grande Pass is known around the world for tarpon fishing, and serious anglers book their guide and their lodging well before the season. A guide's site needs open dates, trip lengths, rates and what's included, plus a fast way to hold a date. The same goes for golf cart and bike rentals, which visitors line up before they arrive.</p>
"""),
            ("What that could look like", """
<p>Say a home watch company that covers the village. The site would explain each visit in plain steps, show a sample of the photo report owners get after each check, list storm-prep and return-prep services, and offer a simple form to request a quote by home size. A page for owners up north answers how keys, alarms and emergencies are handled.</p>
"""),
        ],
        "checklist": [
            "A refined look that matches the village",
            "Clear explanation of how you work from afar",
            "Open dates and rates for the season",
            "A fast way to hold a booking",
            "Storm prep and off-season details",
        ],
        "faq": [
            ("Is Boca Grande really in Lee County?", "The village is, at the south end of Gasparilla Island. The causeway onto the island is in Charlotte County, which is why some businesses here serve both counties. I'll make sure your site names the areas you cover."),
            ("What does a website cost for a Boca Grande business?", "A one-page site is $500 and up to five pages is $1,500, set before I begin."),
            ("Can you keep the site updated when the season changes?", "Yes. You can edit hours and dates yourself, or a care plan covers seasonal updates for you."),
        ],
        "nearby": ["pine-island-fl", "captiva-fl", "cape-coral-fl", "sanibel-fl"],
        "services": ["small-business-website-design", "website-care-plans", "logo-and-branding"],
    },
    {
        "slug": "gateway-fl",
        "town": "Gateway",
        "place": "Gateway, FL",
        "hue": 280,
        "blurb": "Planned neighborhoods near the airport",
        "seo_title": "Gateway Web Design for Small Businesses",
        "description": "Web design for Gateway, FL small businesses: clean, phone-first websites from $500 for home services, wellness, tutoring and family businesses.",
        "h1": "Web design for small businesses in Gateway, FL",
        "lede": "Gateway is a master-planned community east of I-75, just north of Southwest Florida International Airport and close to JetBlue Park, the Red Sox spring training home. It's full of families and busy households who hire local help and do their research on a phone first.",
        "answer": "Lee County Websites makes fixed-price websites for local businesses in Gateway, Florida, including home services, wellness, tutoring and other family businesses. A one-page site is $500 and a five-page site is $1,500, with the price set before any work begins. Each one is built for phones, shows that you're licensed, insured and reliable, and is set up for searches from Gateway and nearby Fort Myers.",
        "sections": [
            ("Selling into planned communities", """
<p>Gateway's neighborhoods have homeowners associations, gated entries and plenty of rules for vendors. Residents want a pool company, lawn crew, cleaner or handyman who already knows how that works. Showing your license and insurance, saying you work in Gateway's communities and explaining how you schedule around gate access and HOA rules makes you the easy choice.</p>
"""),
            ("Busy households, short attention", """
<p>Many Gateway families are juggling school runs, commutes and sports, and they book help in the gaps. They want to see a price or a price range, read a few real reviews and request a time in under a minute. Online booking, text-friendly contact and clear service areas matter more than a long story.</p>
"""),
            ("What that could look like", """
<p>Imagine a mobile dog grooming van that serves Gateway and nearby neighborhoods. The site would open with prices by dog size, the neighborhoods covered and a booking button. A short page explains how the van works in a driveway, what it needs from the home, and how to handle gate access, so first-time customers know exactly what to expect.</p>
"""),
        ],
        "checklist": [
            "License and insurance shown plainly",
            "Neighborhoods and communities you cover",
            "Prices or price ranges up front",
            "Online booking or a quick request form",
            "Text-friendly contact for busy families",
        ],
        "faq": [
            ("Should my site mention Gateway specifically?", "If you work there a lot, yes. Naming Gateway and the nearby areas you serve helps you show up when residents search, and tells them you know the community."),
            ("How much does a website cost for a Gateway business?", "It's $500 for one page or $1,500 for up to five pages, and that price is fixed before I start."),
            ("Can customers book appointments from my site?", "Yes. I can link or embed most booking tools, so people can pick a time right from their phone."),
        ],
        "nearby": ["fort-myers-fl", "lehigh-acres-fl", "san-carlos-park-fl", "estero-fl"],
        "services": ["small-business-website-design", "local-seo", "website-care-plans"],
    },
]
