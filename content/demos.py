"""Clickable demo sites for the four sample businesses in samples.py.

Each demo lives at /work/<id>/ and is clearly marked as a sample design on
every page. The businesses are invented: phone numbers use the 555-01xx range
that is reserved for fiction, emails use the reserved .example domain, and no
street addresses are given. Demo pages are kept out of search (noindex, not in
the sitemap).

Block types used in "blocks":
  ("cards", heading, [(title, text, price)])
  ("features", heading, [(title, text)])
  ("list", heading, [item, ...])
  ("table", heading, (col, col, ...), [(cell, cell, ...), ...])
  ("faq", heading, [(question, answer)])
  ("text", heading, [paragraph, ...])
  ("form", heading, [(label, kind, options)], button, note)
"""

DEMOS = {
    "charter": {
        "email": "captain@tidewell.example",
        "hours": "Trips daily, weather permitting. Calls answered 7am to 8pm.",
        "area": "Leaving from Cape Coral canals. Pine Island Sound, Matlacha Pass and the Gulf.",
        "tagline": "Private fishing trips for up to four guests.",
        "action": ("book", "Check dates"),
        "home": [
            ("cards", "Pick your trip", None),
            ("features", "Why anglers book with us", [
                ("Everything's on board", "Rods, reels, live bait, ice and fishing licenses for every guest."),
                ("Kids and first timers", "Patient, hands-on help. Plenty of families fish with us every week."),
                ("Weather call by 6am", "If it's not safe, we move your trip or refund it in full."),
            ]),
            ("list", "What you might catch", ["Snook and redfish in the mangroves", "Spotted seatrout on the grass flats",
                                             "Tarpon from May to July", "Grouper and snapper offshore"]),
        ],
        "pages": [
            {"slug": "trips", "nav": "Trips", "title": "Trips", "intro": "Every trip is private: just your group and the captain.",
             "blocks": [
                 ("cards", "Our trips", [
                     ("Half day inshore", "4 hours in the canals, mangroves and bay. Best for families and first timers.", "From $550"),
                     ("Full day", "8 hours, inshore or out to the nearshore reefs, depending on the season.", "From $950"),
                     ("Sunset cruise", "2 hours of easy fishing and dolphin watching as the sun goes down.", "From $300"),
                     ("Tarpon trip", "6 hours chasing the silver king, May through July.", "From $800"),
                 ]),
                 ("list", "Every trip includes", ["Licensed captain", "Rods, reels and tackle", "Live bait and ice",
                                                 "Fishing licenses", "Cleaning your keepers at the dock"]),
                 ("list", "Bring along", ["Sunscreen and sunglasses", "A hat", "Snacks and drinks (no glass)", "A cooler for your fish"]),
             ]},
            {"slug": "rates", "nav": "Rates", "title": "Rates", "intro": "Prices are per boat, up to four guests. No hidden fees.",
             "blocks": [
                 ("table", "Trip rates", ("Trip", "Length", "Price"), [
                     ("Sunset cruise", "2 hours", "$300"), ("Half day inshore", "4 hours", "$550"),
                     ("Tarpon trip", "6 hours", "$800"), ("Full day", "8 hours", "$950"),
                 ]),
                 ("text", "Deposits and weather", [
                     "A $100 deposit holds your date. The rest is due on the day of the trip.",
                     "If the captain calls the trip off for weather, you can move it or get your deposit back in full.",
                 ]),
             ]},
            {"slug": "faq", "nav": "FAQ", "title": "Questions", "intro": "The things people ask before they book.",
             "blocks": [
                 ("faq", "Before your trip", [
                     ("Do we need fishing licenses?", "No. Your licenses are covered by the boat's charter license."),
                     ("Can kids come?", "Yes. Kids of any age are welcome, and we have life jackets in every size."),
                     ("What if someone gets seasick?", "Inshore trips stay in calm water. If you're worried, ask about the half day."),
                     ("Can we keep the fish?", "Yes, within Florida's limits. We clean and bag them at the dock."),
                     ("Where do we meet?", "We send the meeting spot with your booking confirmation."),
                 ]),
             ]},
        ],
        "action_page": {"title": "Check dates", "intro": "Tell us when you'd like to go and we'll confirm within a day.",
                        "form": [("Your name", "text", None), ("Email", "email", None), ("Phone", "tel", None),
                                 ("Trip", "select", ["Half day inshore", "Full day", "Sunset cruise", "Tarpon trip"]),
                                 ("Preferred date", "date", None), ("Guests", "select", ["1", "2", "3", "4"]),
                                 ("Anything we should know?", "textarea", None)],
                        "button": "Request my date"},
    },
    "hvac": {
        "layout": "pro",
        "logo_sub": "A/C repair and installs",
        "band": "A/C out? We can usually be there today.",
        "email": "service@pelicanrowair.example",
        "hours": "Repairs 7 days a week, 7am to 9pm. Emergency calls after hours.",
        "area": "Fort Myers, Lehigh Acres, Cape Coral, Estero and North Fort Myers.",
        "tagline": "Air conditioning repair, installs and tune-ups.",
        "action": ("request", "Request service"),
        "home": [
            ("cards", "How can we help?", None),
            ("features", "What to expect", [
                ("Upfront prices", "You approve the price before any work starts. No surprises on the bill."),
                ("Same day visits", "Call before noon and we'll usually be there the same day."),
                ("Licensed and insured", "Every tech is trained, background checked and fully insured."),
            ]),
            ("list", "Signs it's time to call", ["Air blowing warm or weak", "Water around the indoor unit",
                                                "Strange noises or smells", "Power bills climbing for no reason"]),
        ],
        "pages": [
            {"slug": "repair", "nav": "Repair", "title": "A/C repair", "intro": "Fast, honest repairs for every major brand.",
             "blocks": [
                 ("cards", "Common repairs", [
                     ("No cooling", "Capacitors, contactors, refrigerant leaks and frozen coils.", "Diagnostic $89"),
                     ("Water leaks", "Clogged drain lines and float switches cleared and tested.", "From $129"),
                     ("Thermostats", "Replacements and smart thermostat setup.", "From $149"),
                 ]),
                 ("text", "The $89 diagnostic", ["We find the problem and give you a written price. If you go ahead with the repair, the $89 comes off the bill."]),
             ]},
            {"slug": "installs", "nav": "Installs", "title": "New systems", "intro": "Free in-home quotes on new air conditioners and heat pumps.",
             "blocks": [
                 ("features", "How a new system goes in", [
                     ("1. Free quote", "We measure your home and show you two or three options, with prices."),
                     ("2. Install day", "Most installs take one day. We protect your floors and haul the old unit away."),
                     ("3. Check-up", "We come back after a month to make sure everything runs right."),
                 ]),
                 ("list", "Every install includes", ["Permits and inspection", "New thermostat", "Hurricane straps on the outdoor unit",
                                                    "10 year parts warranty", "First year of tune-ups free"]),
             ]},
            {"slug": "areas", "nav": "Areas", "title": "Areas we serve", "intro": "Our vans cover most of Lee County every day.",
             "blocks": [
                 ("table", "Service areas", ("Town", "Same day visits", "Trip fee"), [
                     ("Fort Myers", "Yes", "None"), ("Lehigh Acres", "Yes", "None"), ("Cape Coral", "Yes", "None"),
                     ("Estero", "Most days", "None"), ("North Fort Myers", "Most days", "None"),
                 ]),
                 ("text", "Outside these towns?", ["Call us anyway. We often cover Bonita Springs and Alva on scheduled days."]),
             ]},
        ],
        "action_page": {"title": "Request service", "intro": "Tell us what's going on and we'll call you back to set a time.",
                        "form": [("Your name", "text", None), ("Phone", "tel", None), ("Email", "email", None),
                                 ("Town", "select", ["Fort Myers", "Lehigh Acres", "Cape Coral", "Estero", "North Fort Myers", "Other"]),
                                 ("What do you need?", "select", ["Repair", "New system quote", "Tune-up", "Not sure"]),
                                 ("What's happening?", "textarea", None)],
                        "button": "Send my request"},
    },
    "coffee": {
        "layout": "cafe",
        "logo_name": "Little Spoonbill",
        "logo_sub": "Coffee + Bakery",
        "ribbon": "Open every day 7am to 3pm \u00b7 Pastries out of the oven by 7",
        "headline_html": "Iced coffee <em>&amp;</em> fresh bakes, downtown.",
        "email": "hello@littlespoonbill.example",
        "hours": "Open every day, 7am to 3pm.",
        "area": "In the River District, Fort Myers. Street parking and the nearby city garage.",
        "tagline": "Espresso, cold brew and pastries baked here every morning.",
        "action": ("order", "Order ahead"),
        "home": [
            ("cards", "Customer favorites", None),
            ("features", "Why stop in", [
                ("Baked here", "Croissants, guava pastries and banana bread, out of the oven by 7."),
                ("Local roast", "Our house espresso is roasted in small batches in Southwest Florida."),
                ("Room to stay", "Big tables, outdoor seats and fast Wi-Fi."),
            ]),
            ("list", "Good to know", ["Oat, almond and whole milk at no extra charge", "Dogs welcome on the patio",
                                     "Gluten-free bakes most days", "Gift cards at the counter"]),
        ],
        "pages": [
            {"slug": "menu", "nav": "Menu", "title": "Menu", "intro": "Prices include tax. Ask about today's bakes.",
             "blocks": [
                 ("table", "Coffee", ("Drink", "Small", "Large"), [
                     ("Espresso", "$3.25", "-"), ("Cortado", "$4.25", "-"), ("Latte", "$4.75", "$5.50"),
                     ("Iced oat latte", "$5.50", "$6.25"), ("Cold brew", "$4.75", "$5.50"), ("Cafe con leche", "$4.25", "$4.95"),
                 ]),
                 ("table", "Bakes", ("Item", "", "Price"), [
                     ("Butter croissant", "", "$3.50"), ("Guava pastry", "", "$3.75"), ("Banana bread", "", "$3.25"),
                     ("Breakfast sandwich", "", "$7.95"),
                 ]),
             ]},
            {"slug": "hours", "nav": "Hours", "title": "Hours", "intro": "Same hours all year, closed on a few holidays.",
             "blocks": [
                 ("table", "Opening hours", ("Day", "Open", "Close"), [
                     ("Monday to Friday", "7am", "3pm"), ("Saturday", "7am", "3pm"), ("Sunday", "8am", "2pm"),
                 ]),
                 ("text", "Holidays", ["Closed Thanksgiving, Christmas Day and New Year's Day. Holiday hours are posted here and on our Google listing."]),
             ]},
            {"slug": "visit", "nav": "Visit", "title": "Visit", "intro": "Find us in the River District, a short walk from the river.",
             "blocks": [
                 ("list", "Getting here", ["Street parking right outside, free for 2 hours", "The city garage is a two minute walk",
                                          "Bike rack by the front door", "Step-free entrance"]),
                 ("text", "Events and groups", ["Planning a meeting or a small event? We can hold the big table on weekday mornings. Send us a note."]),
             ]},
        ],
        "action_page": {"title": "Order ahead", "intro": "Order before you leave and we'll have it ready at the counter.",
                        "form": [("Your name", "text", None), ("Phone", "tel", None),
                                 ("Pickup time", "select", ["As soon as possible", "In 15 minutes", "In 30 minutes", "In 1 hour"]),
                                 ("Your order", "textarea", None)],
                        "button": "Place my order"},
    },
    "cottage": {
        "layout": "coastal",
        "logo_name": "Seagrape Lane",
        "logo_sub": "Cottages \u00b7 Fort Myers Beach",
        "email": "stay@seagrapelane.example",
        "hours": "Check-in 4pm, check-out 10am. Office line 9am to 6pm.",
        "area": "On Estero Island, Fort Myers Beach. A short walk to the sand.",
        "tagline": "Four beach cottages with bikes, chairs and an outdoor shower.",
        "action": ("book", "Check availability"),
        "home": [
            ("cards", "Our cottages", None),
            ("features", "Every stay includes", [
                ("Beach gear", "Two bikes, chairs, an umbrella and a cooler for every cottage."),
                ("Full kitchens", "Cook your catch, or grab takeout and eat on your porch."),
                ("No cleaning list", "No chores at check-out. Just leave the keys on the counter."),
            ]),
            ("list", "Nearby", ["The beach, about a two minute walk", "Restaurants and the trolley stop",
                               "Kayak and paddleboard rentals", "Lovers Key State Park, a short drive south"]),
        ],
        "pages": [
            {"slug": "cottages", "nav": "Cottages", "title": "The cottages", "intro": "Each cottage has its own porch, kitchen and parking spot.",
             "blocks": [
                 ("cards", "Choose your cottage", [
                     ("The Pelican", "Studio with a queen bed. Sleeps 2.", "From $139/night"),
                     ("The Sandpiper", "2 bedrooms, 1 bath. Sleeps 4.", "From $189/night"),
                     ("The Heron", "3 bedrooms, 2 baths. Sleeps 6.", "From $249/night"),
                     ("The Osprey", "2 bedrooms with a screened porch. Sleeps 4.", "From $209/night"),
                 ]),
                 ("list", "In every cottage", ["Wi-Fi and smart TV", "Washer and dryer", "Beach towels",
                                              "Outdoor shower", "Pet friendly in The Osprey"]),
             ]},
            {"slug": "rates", "nav": "Rates", "title": "Rates", "intro": "Nightly rates by season. Three night minimum.",
             "blocks": [
                 ("table", "Nightly rates", ("Cottage", "May to Dec", "Jan to Apr"), [
                     ("The Pelican", "$139", "$199"), ("The Sandpiper", "$189", "$259"),
                     ("The Osprey", "$209", "$279"), ("The Heron", "$249", "$339"),
                 ]),
                 ("text", "Booking terms", [
                     "A 30% deposit holds your dates. The rest is due 30 days before arrival.",
                     "Free cancellation up to 30 days before arrival.",
                 ]),
             ]},
            {"slug": "guide", "nav": "Guide", "title": "Island guide", "intro": "Our favorite ways to spend a few days on the beach.",
             "blocks": [
                 ("features", "Things to do", [
                     ("Morning shelling", "Walk the beach at low tide for the best shells."),
                     ("Paddle the back bay", "Rent a kayak and look for dolphins and manatees."),
                     ("Sunset on the sand", "Grab two chairs from the shed and head west around 6."),
                 ]),
                 ("faq", "Good to know", [
                     ("Is there parking?", "Yes, one spot per cottage, right outside."),
                     ("Are pets allowed?", "Dogs are welcome in The Osprey, with a small fee."),
                     ("What happens in a storm?", "If a hurricane warning is issued, you can move your stay or get a full refund."),
                 ]),
             ]},
        ],
        "action_page": {"title": "Check availability", "intro": "Send your dates and we'll reply with what's open and the total.",
                        "form": [("Your name", "text", None), ("Email", "email", None),
                                 ("Cottage", "select", ["Any cottage", "The Pelican", "The Sandpiper", "The Osprey", "The Heron"]),
                                 ("Arrival", "date", None), ("Departure", "date", None), ("Guests", "select", ["1", "2", "3", "4", "5", "6"]),
                                 ("Questions", "textarea", None)],
                        "button": "Check my dates"},
    },
}
