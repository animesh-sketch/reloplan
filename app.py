import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

# ─────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────
WA_NUMBER  = "919999999999"
WA_DEFAULT = "Hi! I saw ReloPlan and I'd like help planning my relocation."

# ─────────────────────────────────────────────────────────────────
# DATA — Cities & Areas
# ─────────────────────────────────────────────────────────────────
CITIES = {
    "Bangalore": {
        "areas": {
            "Koramangala": {
                "avg_rent": 25000, "safety": 4, "commute": 3, "social": 5,
                "gym": True, "temple": True,
                "desc": "Bangalore's startup soul — buzzing cafes, rooftop bars and co-working spaces on every corner.",
                "tags": ["Startup Hub", "Nightlife", "Cafes", "Pet-Friendly"],
                "restaurants": [
                    {"name": "Truffles",          "cuisine": "American",     "rating": 4.5, "price": "₹₹",  "vibe": "Burgers & shakes"},
                    {"name": "Brahmin's Coffee",   "cuisine": "South Indian", "rating": 4.7, "price": "₹",   "vibe": "Iconic breakfast spot"},
                    {"name": "The Permit Room",    "cuisine": "Kerala",       "rating": 4.4, "price": "₹₹₹","vibe": "Craft cocktails"},
                    {"name": "Communiti",          "cuisine": "Continental",  "rating": 4.3, "price": "₹₹",  "vibe": "Brunch favourite"},
                ],
                "parties": [
                    {"name": "Arbor Brewing Co.", "type": "Craft Beer Bar",   "vibe": "Live music weekends",   "cover": "Free–₹500"},
                    {"name": "Vapour Bar Exchange","type": "Sports Bar",       "vibe": "NFL & watch parties",   "cover": "Free"},
                    {"name": "Toit Brewpub",       "type": "Microbrewery",     "vibe": "Rooftop house parties", "cover": "Free"},
                    {"name": "The Humming Tree",   "type": "Live Music Venue", "vibe": "Indie gigs & DJ nights","cover": "₹500–₹1,500"},
                ],
            },
            "HSR Layout": {
                "avg_rent": 22000, "safety": 5, "commute": 4, "social": 4,
                "gym": True, "temple": True,
                "desc": "Tree-lined streets, weekend farmer's markets and a thriving young professional crowd.",
                "tags": ["Family-Friendly", "Walkable", "Parks", "Safe"],
                "restaurants": [
                    {"name": "Meghana Foods",      "cuisine": "Andhra",       "rating": 4.6, "price": "₹₹",  "vibe": "Famous biryani"},
                    {"name": "CTR",                "cuisine": "South Indian", "rating": 4.8, "price": "₹",   "vibe": "Legendary dosas"},
                    {"name": "Onesta Pizza",       "cuisine": "Pizza",        "rating": 4.4, "price": "₹₹",  "vibe": "Family casual"},
                    {"name": "Big Bowl",           "cuisine": "Asian Fusion", "rating": 4.2, "price": "₹₹",  "vibe": "Quick & healthy"},
                ],
                "parties": [
                    {"name": "Foxtrot Bar",        "type": "Bar & Lounge",    "vibe": "Rooftop deck, chill vibes",   "cover": "Free"},
                    {"name": "Plan B",             "type": "Sports Bar",      "vibe": "IPL screenings & parties",    "cover": "Free"},
                    {"name": "Social HSR",         "type": "Social Club",     "vibe": "Weekend DJ + indie pop-ups",  "cover": "Free–₹300"},
                    {"name": "House of Commons",   "type": "Pub",             "vibe": "Karaoke & game nights",       "cover": "Free"},
                ],
            },
            "Whitefield": {
                "avg_rent": 18000, "safety": 4, "commute": 2, "social": 3,
                "gym": True, "temple": True,
                "desc": "IT corridor with gated communities, expat clubs and weekend escape vibes.",
                "tags": ["IT Hub", "Expat-Friendly", "Malls", "Gated Communities"],
                "restaurants": [
                    {"name": "Windmills Craftworks","cuisine": "Continental", "rating": 4.5, "price": "₹₹₹","vibe": "Live jazz & craft beer"},
                    {"name": "Fatty Bao",           "cuisine": "Asian",       "rating": 4.4, "price": "₹₹₹","vibe": "Pan-Asian tapas"},
                    {"name": "Byg Brewski",         "cuisine": "Multi",       "rating": 4.3, "price": "₹₹",  "vibe": "Brewery in the woods"},
                    {"name": "Punjabi Tadka",       "cuisine": "North Indian","rating": 4.2, "price": "₹₹",  "vibe": "Daily comfort food"},
                ],
                "parties": [
                    {"name": "Byg Brewski Brewing Co.","type": "Microbrewery","vibe": "Outdoor parties, fire pits","cover": "Free"},
                    {"name": "Whitefield Arms",     "type": "Pub",             "vibe": "Expat mixer nights",        "cover": "Free"},
                    {"name": "Windmills",           "type": "Live Music",      "vibe": "Jazz & rock weekends",      "cover": "₹500"},
                    {"name": "Zara's",              "type": "Lounge",          "vibe": "Saturday house parties",    "cover": "₹300–₹800"},
                ],
            },
        }
    },
    "Mumbai": {
        "areas": {
            "Andheri West": {
                "avg_rent": 35000, "safety": 3, "commute": 4, "social": 5,
                "gym": True, "temple": True,
                "desc": "Bollywood's backyard — film sets, casting studios and the best nightlife in the suburbs.",
                "tags": ["Bollywood", "Nightlife", "Metro Access", "Foodie"],
                "restaurants": [
                    {"name": "Pali Village Cafe",  "cuisine": "Continental",  "rating": 4.5, "price": "₹₹₹","vibe": "Brunch with a view"},
                    {"name": "Bademiya",           "cuisine": "Mughlai",      "rating": 4.6, "price": "₹",   "vibe": "Late-night seekh kebabs"},
                    {"name": "Hakkasan",           "cuisine": "Cantonese",    "rating": 4.7, "price": "₹₹₹₹","vibe": "Premium dim sum"},
                    {"name": "Candies",            "cuisine": "Bakery Cafe",  "rating": 4.4, "price": "₹₹",  "vibe": "Best cheesecake in Mumbai"},
                ],
                "parties": [
                    {"name": "Loco Locale",        "type": "Club",            "vibe": "EDM & Bollywood nights",    "cover": "₹500–₹1,500"},
                    {"name": "The Little Door",    "type": "Speakeasy",       "vibe": "Secret house parties",      "cover": "₹800"},
                    {"name": "Khar Social",        "type": "Social Club",     "vibe": "Weekend ragers + live acts","cover": "Free–₹500"},
                    {"name": "AntiSocial Andheri", "type": "Underground",     "vibe": "Indie & hip-hop nights",    "cover": "₹500–₹1,000"},
                ],
            },
            "Powai": {
                "avg_rent": 40000, "safety": 5, "commute": 3, "social": 4,
                "gym": True, "temple": False,
                "desc": "Lakeside luxury — IIT Bombay alumni energy meets scenic joggers' paradise.",
                "tags": ["Lakeside", "Premium", "Safe", "IIT Crowd"],
                "restaurants": [
                    {"name": "Noodle Bar",         "cuisine": "Asian",        "rating": 4.4, "price": "₹₹",  "vibe": "Quick lakeside bites"},
                    {"name": "Out of the Blue",    "cuisine": "Continental",  "rating": 4.5, "price": "₹₹₹","vibe": "Romantic lakeside dining"},
                    {"name": "Spice Klub",         "cuisine": "Indian Fusion","rating": 4.3, "price": "₹₹₹","vibe": "Molecular gastronomy"},
                    {"name": "Mainland China",     "cuisine": "Chinese",      "rating": 4.2, "price": "₹₹₹","vibe": "Family dinners"},
                ],
                "parties": [
                    {"name": "TGIF Powai",         "type": "Bar & Grill",     "vibe": "Friday night parties",      "cover": "Free"},
                    {"name": "Hakone",             "type": "Lounge Bar",      "vibe": "Lakeside sundowners",       "cover": "Free"},
                    {"name": "Hiranandani Club",   "type": "Members Club",    "vibe": "Pool parties & socials",    "cover": "Members only"},
                    {"name": "The Bierhaus",       "type": "Beer Garden",     "vibe": "Oktoberfest-style events",  "cover": "Free"},
                ],
            },
            "Thane": {
                "avg_rent": 22000, "safety": 4, "commute": 3, "social": 3,
                "gym": True, "temple": True,
                "desc": "Affordable, green and fast-growing — lakes, malls and a rising food scene.",
                "tags": ["Affordable", "Green", "Family", "Growing"],
                "restaurants": [
                    {"name": "Barbeque Nation",    "cuisine": "BBQ",          "rating": 4.3, "price": "₹₹₹","vibe": "Live grill weekends"},
                    {"name": "Hotel Sujata",       "cuisine": "Maharashtrian","rating": 4.5, "price": "₹",   "vibe": "Authentic local thali"},
                    {"name": "Cream Centre",       "cuisine": "Vegetarian",   "rating": 4.2, "price": "₹₹",  "vibe": "Comfort veg food"},
                    {"name": "Punjabi Dhaba",      "cuisine": "Punjabi",      "rating": 4.1, "price": "₹₹",  "vibe": "Late night dal makhani"},
                ],
                "parties": [
                    {"name": "Xoho The Resto Bar", "type": "Bar",             "vibe": "Weekend DJ nights",         "cover": "Free"},
                    {"name": "Viviana Social",     "type": "Social Club",     "vibe": "Pop-up events & mixers",    "cover": "Free–₹300"},
                    {"name": "F Bar & Lounge",     "type": "Lounge",          "vibe": "Ladies nights & B-days",    "cover": "Free"},
                    {"name": "Crafters Bar",       "type": "Craft Beer Bar",  "vibe": "Quiz & trivia nights",      "cover": "Free"},
                ],
            },
        }
    },
    "Hyderabad": {
        "areas": {
            "Gachibowli": {
                "avg_rent": 20000, "safety": 4, "commute": 3, "social": 4,
                "gym": True, "temple": True,
                "desc": "The Silicon Valley of Hyderabad — global IT offices, modern malls, wide roads.",
                "tags": ["IT Hub", "Modern", "Upscale", "Expat"],
                "restaurants": [
                    {"name": "Paradise Biryani",   "cuisine": "Hyderabadi",   "rating": 4.7, "price": "₹₹",  "vibe": "The OG biryani spot"},
                    {"name": "AB's Absolute Barbecues","cuisine":"BBQ",       "rating": 4.4, "price": "₹₹₹","vibe": "Live grill experience"},
                    {"name": "Ohri's Gufaa",       "cuisine": "Multi-Cuisine","rating": 4.3, "price": "₹₹₹","vibe": "Cave dining concept"},
                    {"name": "Chutneys",           "cuisine": "South Indian", "rating": 4.6, "price": "₹",   "vibe": "Best pesarattu in town"},
                ],
                "parties": [
                    {"name": "10D Bar & Kitchen",  "type": "Lounge Bar",      "vibe": "EDM Fridays & Saturdays",   "cover": "₹500"},
                    {"name": "The Grid",           "type": "Sports Bar",      "vibe": "IPL & Champions League",    "cover": "Free"},
                    {"name": "Farzi Café",         "type": "Bar + Dining",    "vibe": "Molecular cocktail nights", "cover": "Free"},
                    {"name": "Aloft WXYZ Bar",     "type": "Hotel Bar",       "vibe": "Rooftop house parties",     "cover": "₹500–₹1,000"},
                ],
            },
            "Banjara Hills": {
                "avg_rent": 30000, "safety": 5, "commute": 3, "social": 5,
                "gym": True, "temple": True,
                "desc": "Hyderabad's Beverly Hills — celebrity restaurants, boutique stores, old money vibes.",
                "tags": ["Premium", "Trendy", "Restaurants", "Boutiques"],
                "restaurants": [
                    {"name": "Flechazo",           "cuisine": "Spanish",      "rating": 4.6, "price": "₹₹₹₹","vibe": "Tapas & flamenco"},
                    {"name": "Bikkgane Biryani",   "cuisine": "Biryani",      "rating": 4.5, "price": "₹₹",  "vibe": "Dum biryani specialists"},
                    {"name": "Jewel of Nizam",     "cuisine": "Hyderabadi",   "rating": 4.7, "price": "₹₹₹₹","vibe": "Royal dining experience"},
                    {"name": "Silver Spoon",       "cuisine": "Continental",  "rating": 4.4, "price": "₹₹₹","vibe": "Power lunches"},
                ],
                "parties": [
                    {"name": "Aer Lounge",         "type": "Rooftop Lounge",  "vibe": "City view house parties",   "cover": "₹800–₹1,500"},
                    {"name": "Park Hyatt Bar",     "type": "Hotel Bar",       "vibe": "Upscale Saturday nights",   "cover": "₹1,000"},
                    {"name": "Kismet",             "type": "Club",            "vibe": "Bollywood & retro nights",  "cover": "₹500–₹1,000"},
                    {"name": "The Wine Rack",      "type": "Wine Bar",        "vibe": "Wine tasting & socials",    "cover": "Free–₹500"},
                ],
            },
            "Kondapur": {
                "avg_rent": 18000, "safety": 4, "commute": 4, "social": 3,
                "gym": True, "temple": True,
                "desc": "Quiet residential stretch near HITEC City — best value for IT professionals.",
                "tags": ["Value for Money", "Residential", "Near HITEC", "Peaceful"],
                "restaurants": [
                    {"name": "Cafe Niloufer",      "cuisine": "Bakery",       "rating": 4.5, "price": "₹",   "vibe": "Iconic Hyd chai & bun"},
                    {"name": "Pista House",        "cuisine": "Hyderabadi",   "rating": 4.6, "price": "₹",   "vibe": "Haleem capital"},
                    {"name": "Fusion 9",           "cuisine": "Multi-Cuisine","rating": 4.2, "price": "₹₹",  "vibe": "IT crowd favourite"},
                    {"name": "Bawarchi",           "cuisine": "Biryani",      "rating": 4.4, "price": "₹₹",  "vibe": "2am biryani fix"},
                ],
                "parties": [
                    {"name": "Zero40 Brewing",     "type": "Microbrewery",    "vibe": "Craft beer & live sport",   "cover": "Free"},
                    {"name": "Hyderama",           "type": "Club",            "vibe": "Friday night dance party",  "cover": "₹400–₹800"},
                    {"name": "Social Kondapur",    "type": "Social Club",     "vibe": "Weekend brunch parties",    "cover": "Free"},
                    {"name": "Rafter's Bar",       "type": "Pub",             "vibe": "Karaoke & trivia nights",   "cover": "Free"},
                ],
            },
        }
    },
    "Delhi": {
        "areas": {
            "Hauz Khas": {
                "avg_rent": 32000, "safety": 3, "commute": 4, "social": 5,
                "gym": True, "temple": True,
                "desc": "Delhi's coolest village — medieval ruins, lakeside cafes and underground clubs.",
                "tags": ["Bohemian", "Art Scene", "Nightlife", "Heritage"],
                "restaurants": [
                    {"name": "Naivedyam",          "cuisine": "South Indian", "rating": 4.6, "price": "₹₹",  "vibe": "Banana leaf meals"},
                    {"name": "Yeti",               "cuisine": "Himalayan",    "rating": 4.5, "price": "₹₹",  "vibe": "Momos & thukpa"},
                    {"name": "Kunzum Travel Cafe", "cuisine": "Cafe",         "rating": 4.4, "price": "₹",   "vibe": "Pay-what-you-want chill"},
                    {"name": "Soda Bottle Opener Wala","cuisine":"Parsi",     "rating": 4.5, "price": "₹₹₹","vibe": "Dhansak & lagan nu custard"},
                ],
                "parties": [
                    {"name": "Hauz Khas Social",   "type": "Social Club",     "vibe": "Rooftop over the lake",     "cover": "Free–₹500"},
                    {"name": "Raasta",             "type": "Reggae Bar",      "vibe": "Bob Marley vibes all night","cover": "Free"},
                    {"name": "Privee",             "type": "Club",            "vibe": "Delhi's top house parties", "cover": "₹1,000–₹2,000"},
                    {"name": "Town Hall",          "type": "Gastropub",       "vibe": "Trivia + DJ nights",        "cover": "Free"},
                ],
            },
            "Dwarka": {
                "avg_rent": 18000, "safety": 5, "commute": 4, "social": 3,
                "gym": True, "temple": True,
                "desc": "India's largest planned township — wide roads, metro at doorstep, very safe.",
                "tags": ["Planned Township", "Very Safe", "Metro Access", "Affordable"],
                "restaurants": [
                    {"name": "Sagar Ratna",        "cuisine": "South Indian", "rating": 4.3, "price": "₹₹",  "vibe": "Family breakfast staple"},
                    {"name": "Bikanervala",        "cuisine": "North Indian", "rating": 4.4, "price": "₹",   "vibe": "Sweets & chaat"},
                    {"name": "The Backyard",       "cuisine": "Continental",  "rating": 4.2, "price": "₹₹",  "vibe": "Casual weekend dining"},
                    {"name": "Haldiram's",         "cuisine": "Multi",        "rating": 4.1, "price": "₹",   "vibe": "Quick comfort food"},
                ],
                "parties": [
                    {"name": "Bottoms Up Pub",     "type": "Pub",             "vibe": "Darts & beer pitchers",     "cover": "Free"},
                    {"name": "Club 100",           "type": "Club",            "vibe": "Saturday Bollywood night",  "cover": "₹300–₹600"},
                    {"name": "The Deck",           "type": "Lounge",          "vibe": "Terrace sundowner parties", "cover": "Free"},
                    {"name": "Sector 10 Social",   "type": "Bar",             "vibe": "Quiz nights & live music",  "cover": "Free"},
                ],
            },
            "Lajpat Nagar": {
                "avg_rent": 25000, "safety": 3, "commute": 5, "social": 4,
                "gym": False, "temple": True,
                "desc": "Delhi's shopping mecca — street food paradise, vintage stores, metro central.",
                "tags": ["Shopping", "Street Food", "Metro Central", "Vibrant"],
                "restaurants": [
                    {"name": "Ustad Moinuddin",    "cuisine": "Mughlai",      "rating": 4.7, "price": "₹",   "vibe": "Best nihari in Delhi"},
                    {"name": "Kake Da Hotel",      "cuisine": "Punjabi",      "rating": 4.6, "price": "₹₹",  "vibe": "Legendary dal makhani"},
                    {"name": "Nathu's",            "cuisine": "Bengali",      "rating": 4.5, "price": "₹₹",  "vibe": "Sweets & snacks since 1939"},
                    {"name": "Punjabi Rasoi",      "cuisine": "Punjabi",      "rating": 4.3, "price": "₹",   "vibe": "Home-style meals"},
                ],
                "parties": [
                    {"name": "The Flying Saucer",  "type": "Rooftop Bar",     "vibe": "Weekend terrace parties",   "cover": "Free"},
                    {"name": "Vapour Lajpat",      "type": "Sports Bar",      "vibe": "Match day gatherings",      "cover": "Free"},
                    {"name": "The Piano Man Jazz", "type": "Jazz Club",       "vibe": "Live jazz every weekend",   "cover": "₹500–₹1,000"},
                    {"name": "Café Lota",          "type": "Bistro",          "vibe": "Indie pop-up nights",       "cover": "Free"},
                ],
            },
        }
    },
    "Pune": {
        "areas": {
            "Koregaon Park": {
                "avg_rent": 28000, "safety": 4, "commute": 3, "social": 5,
                "gym": True, "temple": False,
                "desc": "Pune's Bandra — leafy lanes, Osho ashram energy, rooftop parties and world-class cafes.",
                "tags": ["Cosmopolitan", "Osho Ashram", "Expat", "Rooftops"],
                "restaurants": [
                    {"name": "Café Peter",         "cuisine": "European",     "rating": 4.6, "price": "₹₹₹","vibe": "Pune's oldest fine dine"},
                    {"name": "Arthur's Theme",     "cuisine": "Continental",  "rating": 4.5, "price": "₹₹₹","vibe": "Quirky theme dining"},
                    {"name": "Dario's",            "cuisine": "Italian",      "rating": 4.4, "price": "₹₹₹","vibe": "Authentic wood-fired pizza"},
                    {"name": "Café Goodluck",      "cuisine": "Iranian Café", "rating": 4.7, "price": "₹",   "vibe": "Bun maska since 1935"},
                ],
                "parties": [
                    {"name": "High Spirits Café",  "type": "Live Music",      "vibe": "Biggest indie gig venue",   "cover": "₹300–₹800"},
                    {"name": "Hard Rock Cafe Pune","type": "Club",            "vibe": "Rock & Bollywood nights",   "cover": "₹500–₹1,000"},
                    {"name": "Effingut KP",        "type": "Microbrewery",    "vibe": "Rooftop beer garden",       "cover": "Free"},
                    {"name": "Copa",               "type": "Rooftop Lounge",  "vibe": "House parties every Fri",   "cover": "₹500–₹1,200"},
                ],
            },
            "Baner": {
                "avg_rent": 22000, "safety": 4, "commute": 3, "social": 4,
                "gym": True, "temple": True,
                "desc": "New-age Pune — IT parks, modern apartments and Balewadi's sports scene nearby.",
                "tags": ["IT Hub", "Modern", "Sports Scene", "Growing"],
                "restaurants": [
                    {"name": "Flour Works",        "cuisine": "European",     "rating": 4.5, "price": "₹₹₹","vibe": "Best brunch in Baner"},
                    {"name": "Stone Water Grill",  "cuisine": "Multi",        "rating": 4.4, "price": "₹₹₹","vibe": "Poolside dining & drinks"},
                    {"name": "Wadeshwar",          "cuisine": "Maharashtrian","rating": 4.6, "price": "₹",   "vibe": "Morning misal pav ritual"},
                    {"name": "Boteco Do Brasil",   "cuisine": "Brazilian",    "rating": 4.3, "price": "₹₹₹","vibe": "Churrasco & caipirinhas"},
                ],
                "parties": [
                    {"name": "Effingut Baner",     "type": "Microbrewery",    "vibe": "Craft beer + live sport",   "cover": "Free"},
                    {"name": "Balewadi High St.",  "type": "Multi-venue",     "vibe": "Street parties & events",   "cover": "Free"},
                    {"name": "The Poona Club",     "type": "Heritage Club",   "vibe": "Members events & socials",  "cover": "Members only"},
                    {"name": "Toit Baner",         "type": "Brewpub",         "vibe": "Live music & pub quiz",     "cover": "Free"},
                ],
            },
            "Viman Nagar": {
                "avg_rent": 20000, "safety": 5, "commute": 4, "social": 4,
                "gym": True, "temple": True,
                "desc": "Near the airport, upscale gated societies and a rapidly growing food & nightlife strip.",
                "tags": ["Near Airport", "Upscale", "Safe", "Upcoming"],
                "restaurants": [
                    {"name": "The Corinthians",    "cuisine": "Multi",        "rating": 4.5, "price": "₹₹₹₹","vibe": "Luxury resort dining"},
                    {"name": "Mainland China",     "cuisine": "Chinese",      "rating": 4.3, "price": "₹₹₹","vibe": "Date night dimsum"},
                    {"name": "Café Vohuman",       "cuisine": "Iranian",      "rating": 4.6, "price": "₹",   "vibe": "Historic Irani chai"},
                    {"name": "Barbeque Nation",    "cuisine": "BBQ",          "rating": 4.3, "price": "₹₹₹","vibe": "Family weekend grills"},
                ],
                "parties": [
                    {"name": "Kava Lounge",        "type": "Lounge Bar",      "vibe": "Saturday night socials",    "cover": "Free–₹500"},
                    {"name": "Stories Viman Nagar","type": "Bar",             "vibe": "Retro & Bollywood nights",  "cover": "₹300–₹600"},
                    {"name": "Iron House Brewing", "type": "Craft Brewery",   "vibe": "Live trivia & tap takeovers","cover": "Free"},
                    {"name": "Novotel Pool Bar",   "type": "Hotel Bar",       "vibe": "Pool parties & sundowners", "cover": "Free–₹500"},
                ],
            },
        }
    },
}

VENDORS = {
    "Bangalore": {"accommodation":"NoBroker / MagicBricks","bike":"Royal Brothers · ₹3,000/mo","tiffin":"Homely Meals · ₹2,500/mo","maid":"UrbanCompany · ₹2,500/mo","gym":"Cult.fit · ₹1,999/mo","mall":"Phoenix Marketcity","temple":"ISKCON / Bull Temple"},
    "Mumbai":    {"accommodation":"NoBroker / Housing.com","bike":"Bounce · ₹4,000/mo","tiffin":"Mumbai Dabba · ₹3,500/mo","maid":"UrbanCompany · ₹3,000/mo","gym":"Cult.fit · ₹1,999/mo","mall":"Phoenix Palladium","temple":"Siddhivinayak Temple"},
    "Hyderabad": {"accommodation":"NoBroker / 99acres","bike":"Vogo · ₹1,500/mo","tiffin":"HydTiffin · ₹2,000/mo","maid":"UrbanCompany · ₹2,200/mo","gym":"Cult.fit · ₹1,999/mo","mall":"Inorbit Mall","temple":"Birla Mandir"},
    "Delhi":     {"accommodation":"NoBroker / CommonFloor","bike":"Royal Brothers · ₹3,500/mo","tiffin":"Delhi Dabba · ₹2,800/mo","maid":"UrbanCompany · ₹2,500/mo","gym":"Cult.fit · ₹1,999/mo","mall":"Select City Walk","temple":"Akshardham Temple"},
    "Pune":      {"accommodation":"NoBroker / MagicBricks","bike":"Royal Brothers · ₹2,800/mo","tiffin":"Pune Tiffin · ₹2,200/mo","maid":"UrbanCompany · ₹2,000/mo","gym":"Cult.fit · ₹1,999/mo","mall":"Phoenix Marketcity Pune","temple":"Dagdusheth Temple"},
}

ADDON_COSTS = {"bike": 3000, "tiffin": 2500, "maid": 2500, "gym": 1999}

# ─────────────────────────────────────────────────────────────────
# SCORING
# ─────────────────────────────────────────────────────────────────
def score_area(area, budget, lifestyle):
    diff = area["avg_rent"] - budget
    b = 1.0 if diff <= 0 else max(0.0, 1 - diff / budget)
    c = area["commute"] / 5.0
    lc = [area["safety"] / 5.0]
    if "Nightlife & Social" in lifestyle: lc.append(area["social"] / 5.0)
    if "Fitness"            in lifestyle: lc.append(1.0 if area["gym"]    else 0.0)
    if "Spiritual / Temple" in lifestyle: lc.append(1.0 if area["temple"] else 0.0)
    if "Safety"             in lifestyle: lc.append(area["safety"] / 5.0)
    l = sum(lc) / len(lc)
    return round((b * 0.40 + c * 0.30 + l * 0.30) * 100, 1)

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(page_title="ReloPlan", page_icon="🏙️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
*{box-sizing:border-box}
html,body,[class*="css"]{font-family:'Inter',sans-serif}
.main>div{padding-top:.5rem}
footer,header,#MainMenu{display:none}

/* ── Base Cards ── */
.card{background:#fff;border:1px solid #e5e7eb;border-radius:16px;padding:1.4rem;margin-bottom:.75rem;
      box-shadow:0 1px 4px rgba(0,0,0,.06);transition:box-shadow .2s}
.card:hover{box-shadow:0 4px 16px rgba(0,0,0,.1)}
.card-winner{border:2px solid #6366f1;box-shadow:0 0 0 4px rgba(99,102,241,.08)}

/* ── Hero ── */
.hero{background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);
  border-radius:20px;padding:3rem 2rem;color:#fff;text-align:center;margin-bottom:1.5rem;
  box-shadow:0 8px 32px rgba(99,102,241,.25)}

/* ── Badges & Tags ── */
.badge{display:inline-block;background:rgba(255,255,255,.12);color:#fff;border-radius:999px;
  padding:.25rem 1rem;font-size:.78rem;font-weight:600;margin-bottom:.8rem;
  border:1px solid rgba(255,255,255,.2)}
.tag{display:inline-block;background:#f0f0ff;color:#4338ca;border-radius:6px;
  padding:.2rem .6rem;font-size:.72rem;font-weight:600;margin:2px 2px 2px 0}
.tag-green{background:#f0fdf4;color:#16a34a}
.tag-orange{background:#fff7ed;color:#c2410c}

/* ── Score Bar ── */
.score-bar-bg{background:#e5e7eb;border-radius:999px;height:7px;margin:4px 0 10px}
.score-bar{height:7px;border-radius:999px;transition:width .6s ease}

/* ── Metric Box ── */
.metric{background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:.8rem;text-align:center}
.metric-label{font-size:.7rem;color:#94a3b8;font-weight:500;text-transform:uppercase;letter-spacing:.05em}
.metric-value{font-size:1.2rem;font-weight:800;margin-top:.1rem}

/* ── Place Card (restaurant / party) ── */
.place-card{background:#fff;border:1px solid #f1f5f9;border-radius:12px;padding:1rem;
  display:flex;align-items:flex-start;gap:.75rem;margin-bottom:.6rem;
  box-shadow:0 1px 3px rgba(0,0,0,.04);transition:transform .15s,box-shadow .15s}
.place-card:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,.08)}
.place-icon{width:40px;height:40px;border-radius:10px;display:flex;align-items:center;
  justify-content:center;font-size:1.2rem;flex-shrink:0}
.place-name{font-weight:700;font-size:.9rem;margin-bottom:.1rem}
.place-sub{font-size:.78rem;color:#6b7280}
.price-dot{font-size:.78rem;font-weight:700;color:#10b981}
.rating{font-size:.78rem;color:#f59e0b;font-weight:700}

/* ── Cost Row ── */
.cost-row{display:flex;justify-content:space-between;align-items:center;
  padding:.5rem 0;border-bottom:1px solid #f1f5f9;font-size:.9rem}
.cost-total{background:linear-gradient(135deg,#1e1b4b,#4c1d95);border-radius:12px;
  padding:1rem 1.25rem;margin-top:.75rem;display:flex;justify-content:space-between;align-items:center}

/* ── Buttons ── */
.stButton>button{background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;border:none;
  border-radius:10px;font-weight:700;width:100%;padding:.6rem 1rem;letter-spacing:.01em;
  transition:all .2s}
.stButton>button:hover{background:linear-gradient(135deg,#4f46e5,#7c3aed);
  box-shadow:0 6px 20px rgba(99,102,241,.45);transform:translateY(-1px)}

/* ── Nav ── */
.nav-bar{display:flex;align-items:center;justify-content:space-between;
  padding:.5rem 0;margin-bottom:.5rem}

/* ── WhatsApp float ── */
.wa-float{position:fixed;bottom:1.5rem;right:1.5rem;z-index:9999;background:#25d366;
  color:#fff;border-radius:999px;padding:.7rem 1.2rem;font-weight:700;font-size:.88rem;
  text-decoration:none;display:flex;align-items:center;gap:.5rem;
  box-shadow:0 4px 20px rgba(37,211,102,.5);transition:all .2s}
.wa-float:hover{transform:translateY(-2px);box-shadow:0 6px 24px rgba(37,211,102,.6);
  color:#fff;text-decoration:none}

/* ── Instagram Form ── */
.ig-border{background:linear-gradient(135deg,#833ab4,#fd1d1d,#fcb045);
  border-radius:18px;padding:2px}
.ig-inner{background:#fff;border-radius:16px;padding:1.5rem}

/* ── Section header ── */
.sec-header{font-size:1.1rem;font-weight:700;color:#111827;margin:1.2rem 0 .8rem;
  display:flex;align-items:center;gap:.4rem}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# STATE
# ─────────────────────────────────────────────────────────────────
for k, v in [("page","landing"),("fd",{}),("res",{}),("subs",[]),("admin_ok",False),("ig_leads",[])]:
    if k not in st.session_state: st.session_state[k] = v

def go(p): st.session_state.page = p; st.rerun()

# ─────────────────────────────────────────────────────────────────
# NAV
# ─────────────────────────────────────────────────────────────────
n = st.columns([3,1,1,1,1])
n[0].markdown("## 🏙️ **ReloPlan**")
with n[1]:
    if st.button("🏠 Home"):     go("landing")
with n[2]:
    if st.button("📋 Plan"):     go("form")
with n[3]:
    if st.button("📊 Results"):  go("results")
with n[4]:
    if st.button("🔐 Admin"):    go("admin")
st.markdown("<hr style='margin:.5rem 0 1rem;border:none;border-top:1px solid #e5e7eb'>",
            unsafe_allow_html=True)

# WhatsApp float on every page
st.markdown(
    f'<a class="wa-float" href="https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(WA_DEFAULT)}" target="_blank">'
    f'💬 WhatsApp Us</a>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────
def stars(n): return "★"*n + "☆"*(5-n)

def score_color(s):
    if s >= 75: return "#10b981"
    if s >= 55: return "#f59e0b"
    return "#ef4444"

def place_cards(places, icon, bg):
    for p in places:
        rating_str = f"⭐ {p['rating']}" if "rating" in p else ""
        price_str  = p.get("price","")
        cover_str  = p.get("cover","")
        detail1    = p.get("cuisine", p.get("type",""))
        detail2    = p.get("vibe","")
        st.markdown(f"""
        <div class="place-card">
          <div class="place-icon" style="background:{bg}">{icon}</div>
          <div style="flex:1">
            <div class="place-name">{p['name']}</div>
            <div class="place-sub">{detail1} · {detail2}</div>
          </div>
          <div style="text-align:right;flex-shrink:0">
            <div class="rating">{rating_str}</div>
            <div class="price-dot">{price_str or cover_str}</div>
          </div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# PAGE: LANDING
# ─────────────────────────────────────────────────────────────────
if st.session_state.page == "landing":

    st.markdown("""
    <div class="hero">
      <div class="badge">✨ Smart Relocation · 5 Cities · 15 Areas</div>
      <h1 style="font-size:2.8rem;font-weight:800;margin:.4rem 0;color:#fff;line-height:1.15">
        Find Your Perfect<br>City & Neighbourhood
      </h1>
      <p style="opacity:.8;max-width:540px;margin:.75rem auto 2rem;font-size:1.05rem;font-weight:400">
        Budget match · commute score · restaurants · house parties · starter bundle —
        your full relocation plan in 60 seconds.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature tiles
    tiles = [
        ("🎯","Smart Match",    "Scored on budget, commute & lifestyle"),
        ("🍽","Restaurants",    "Top eats per area, curated & rated"),
        ("🎉","House Parties",  "Best venues & social events nearby"),
        ("📦","Full Bundle",    "Housing, tiffin, maid, gym & more"),
        ("💰","Cost Planner",   "See total monthly spend upfront"),
        ("⚡","60-sec Plan",    "Instant results, no sign-up needed"),
    ]
    r1 = st.columns(3)
    r2 = st.columns(3)
    for col, (icon, title, desc) in zip(r1+r2, tiles):
        col.markdown(f"""
        <div class="card" style="text-align:center;padding:1.2rem .8rem">
          <div style="font-size:1.8rem;margin-bottom:.35rem">{icon}</div>
          <div style="font-weight:700;font-size:.95rem;margin-bottom:.2rem">{title}</div>
          <div style="color:#6b7280;font-size:.8rem">{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1,1,1])
    with mid:
        if st.button("🚀  Start Planning My Move"): go("form")

    # Instagram Lead Form
    st.markdown("<br>", unsafe_allow_html=True)
    _, ig_col, _ = st.columns([1, 1.4, 1])
    with ig_col:
        st.markdown("""
        <div class="ig-border">
          <div class="ig-inner">
            <div style="display:flex;align-items:center;gap:.6rem;margin-bottom:.8rem">
              <div style="width:34px;height:34px;background:linear-gradient(135deg,#833ab4,#fd1d1d,#fcb045);
                border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:1.1rem">📸</div>
              <div>
                <div style="font-weight:700;font-size:.9rem">ReloPlan</div>
                <div style="color:#9ca3af;font-size:.72rem">Sponsored · Free relocation plan</div>
              </div>
            </div>
            <p style="font-size:.85rem;color:#374151;margin-bottom:.75rem">
              Moving cities? Drop your details — we'll WhatsApp your personalised area guide instantly.
            </p>
          </div>
        </div>
        """, unsafe_allow_html=True)
        with st.form("ig_lead"):
            st.text_input("Name",  placeholder="Your full name",  label_visibility="collapsed")
            st.text_input("Phone", placeholder="📞 Phone number", label_visibility="collapsed")
            st.selectbox("City",   list(CITIES.keys()),            label_visibility="collapsed")
            if st.form_submit_button("📲  Get My Free Plan", use_container_width=True):
                st.success("✅ We'll WhatsApp your plan shortly!")

    # Cities strip
    st.markdown("### Cities We Cover")
    city_cols = st.columns(5)
    icons = {"Bangalore":"🌿","Mumbai":"🌊","Hyderabad":"🍖","Delhi":"🏛️","Pune":"🎓"}
    for col,(city,icon) in zip(city_cols, icons.items()):
        col.markdown(f"""
        <div class="metric">
          <div style="font-size:1.8rem">{icon}</div>
          <div style="font-weight:700;font-size:.9rem;margin-top:.2rem">{city}</div>
          <div style="color:#94a3b8;font-size:.72rem">3 areas · curated</div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# PAGE: FORM
# ─────────────────────────────────────────────────────────────────
elif st.session_state.page == "form":

    st.markdown("## 📋 Plan Your Relocation")
    st.markdown("<p style='color:#6b7280;margin-top:-.5rem'>Takes 60 seconds. No sign-up required.</p>",
                unsafe_allow_html=True)

    with st.form("relo_form"):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**👤 About You**")
            name   = st.text_input("Your Name",   placeholder="Rahul Sharma")
            phone  = st.text_input("Phone (optional)", placeholder="For WhatsApp delivery")
            city   = st.selectbox("Target City",  list(CITIES.keys()))
            budget = st.slider("Monthly Rent Budget", 10000, 60000, 22000, 1000, format="₹%d")
        with c2:
            st.markdown("**🎯 Your Priorities**")
            lifestyle = st.multiselect("Lifestyle Preferences",
                ["Safety","Nightlife & Social","Fitness","Spiritual / Temple","Family-Friendly","Foodie"],
                default=["Safety","Fitness"])
            work_loc = st.text_input("Work Location", placeholder="e.g. Electronic City, Cyber City")
            st.markdown("**🛍 Add-on Services**")
            a1,a2,a3,a4 = st.columns(4)
            bike   = a1.checkbox("🛵 Bike",   value=True)
            tiffin = a2.checkbox("🍱 Tiffin", value=True)
            maid   = a3.checkbox("🧹 Maid",   value=False)
            gym    = a4.checkbox("🏋 Gym",    value=True)

        sub = st.form_submit_button("🔍  Find My Best Areas →", use_container_width=True)

    if sub:
        if not name:
            st.error("Please enter your name.")
        else:
            areas  = CITIES[city]["areas"]
            scored = {n: {"score": score_area(d, budget, lifestyle), "data": d}
                      for n, d in areas.items()}
            top2   = sorted(scored.items(), key=lambda x: x[1]["score"], reverse=True)[:2]
            td     = top2[0][1]["data"]
            costs  = {"🏠 Rent": td["avg_rent"], "⚡ Utilities": 1500, "📱 Internet + Mobile": 800}
            if tiffin: costs["🍱 Tiffin"]      = ADDON_COSTS["tiffin"]
            else:      costs["🍽 Self Cooking"] = 5500
            if bike:   costs["🛵 Bike Rental"]  = ADDON_COSTS["bike"]
            if maid:   costs["🧹 Maid Service"] = ADDON_COSTS["maid"]
            if gym:    costs["🏋 Gym"]           = ADDON_COSTS["gym"]

            st.session_state.fd  = {"name":name,"phone":phone,"city":city,"budget":budget,
                                    "lifestyle":lifestyle,"work_loc":work_loc,
                                    "bike":bike,"tiffin":tiffin,"maid":maid,"gym":gym,
                                    "ts":datetime.now().strftime("%d %b %Y %H:%M")}
            st.session_state.res = {"top2":top2,"all":scored,"costs":costs,
                                    "total":sum(costs.values()),"vendors":VENDORS[city]}
            st.session_state.subs.append(st.session_state.fd)
            go("results")

# ─────────────────────────────────────────────────────────────────
# PAGE: RESULTS
# ─────────────────────────────────────────────────────────────────
elif st.session_state.page == "results":

    if not st.session_state.res:
        st.info("No results yet — fill the form first.")
        if st.button("← Go to Form"): go("form")
        st.stop()

    fd   = st.session_state.fd
    res  = st.session_state.res
    top2 = res["top2"]; costs = res["costs"]; total = res["total"]
    vnd  = res["vendors"]; city = fd["city"]
    top_name = top2[0][0]
    top_data = top2[0][1]["data"]

    # Header banner
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f0c29,#302b63);border-radius:16px;
         padding:1.4rem 2rem;color:#fff;margin-bottom:1.5rem;
         box-shadow:0 4px 20px rgba(99,102,241,.2)">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <div>
          <h2 style="margin:0;color:#fff;font-size:1.6rem">👋 Hi {fd['name']}!</h2>
          <p style="margin:.3rem 0 0;opacity:.8;font-size:.9rem">
            Your top 2 areas in <b>{city}</b> · matched to your preferences
          </p>
        </div>
        <div style="text-align:right">
          <div style="font-size:.75rem;opacity:.7">Best match</div>
          <div style="font-size:1.8rem;font-weight:800;color:#a5b4fc">{top2[0][1]['score']}%</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Top 2 Area Cards ──
    st.markdown('<div class="sec-header">🏆 Recommended Areas</div>', unsafe_allow_html=True)
    ac = st.columns(2)
    for i, (aname, ainfo) in enumerate(top2):
        d = ainfo["data"]; s = ainfo["score"]
        col = score_color(s)
        winner = i == 0
        with ac[i]:
            tag_html = "".join(f'<span class="tag">{t}</span>' for t in d.get("tags",[]))
            st.markdown(f"""
            <div class="card {'card-winner' if winner else ''}">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.6rem">
                <div>
                  <h3 style="margin:0;font-size:1.2rem">{aname}</h3>
                  <div style="margin-top:.3rem">{tag_html}</div>
                </div>
                <span style="background:{'#ede9fe' if winner else '#f0fdf4'};
                  color:{'#6d28d9' if winner else '#16a34a'};border-radius:999px;
                  padding:.2rem .8rem;font-size:.72rem;font-weight:800;white-space:nowrap">
                  {'🥇 Best Match' if winner else '🥈 Runner-Up'}
                </span>
              </div>
              <p style="color:#6b7280;font-size:.83rem;margin-bottom:1rem;line-height:1.5">{d['desc']}</p>

              <div style="display:flex;gap:.75rem;margin-bottom:1rem">
                <div class="metric" style="flex:1">
                  <div class="metric-label">Avg Rent</div>
                  <div class="metric-value" style="color:#6366f1">₹{d['avg_rent']:,}</div>
                </div>
                <div class="metric" style="flex:1">
                  <div class="metric-label">Match Score</div>
                  <div class="metric-value" style="color:{col}">{s}%</div>
                </div>
                <div class="metric" style="flex:1">
                  <div class="metric-label">Social Life</div>
                  <div class="metric-value" style="color:#f59e0b">{stars(d['social'])}</div>
                </div>
              </div>

              <div style="font-size:.82rem">
                <div style="display:flex;justify-content:space-between;margin-bottom:.15rem">
                  <span style="color:#6b7280">🛡 Safety</span>
                  <span style="font-weight:600">{stars(d['safety'])}</span>
                </div>
                <div class="score-bar-bg"><div class="score-bar"
                  style="width:{d['safety']*20}%;background:#6366f1"></div></div>

                <div style="display:flex;justify-content:space-between;margin-bottom:.15rem">
                  <span style="color:#6b7280">🚇 Commute</span>
                  <span style="font-weight:600">{stars(d['commute'])}</span>
                </div>
                <div class="score-bar-bg"><div class="score-bar"
                  style="width:{d['commute']*20}%;background:#10b981"></div></div>

                <div style="margin-top:.4rem;font-size:.8rem">
                  🏋 Gym: {"✅" if d['gym'] else "❌"} &nbsp;·&nbsp;
                  🛕 Temple: {"✅" if d['temple'] else "❌"} &nbsp;·&nbsp;
                  📍 {d.get('landmark','')}
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Nearby Places tabs ──
    st.markdown(f'<div class="sec-header">📍 Nearby Places — {top_name}</div>', unsafe_allow_html=True)
    tab_r, tab_p = st.tabs(["🍽 Restaurants & Cafes", "🎉 House Parties & Nightlife"])

    with tab_r:
        r_cols = st.columns(2)
        rests = top_data.get("restaurants", [])
        for j, r in enumerate(rests):
            with r_cols[j % 2]:
                place_cards([r], "🍽", "#fff7ed")

    with tab_p:
        p_cols = st.columns(2)
        parties = top_data.get("parties", [])
        for j, p in enumerate(parties):
            with p_cols[j % 2]:
                place_cards([p], "🎉", "#fdf4ff")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Bundle + Cost ──
    b_col, c_col = st.columns(2)

    with b_col:
        st.markdown(f'<div class="sec-header">📦 Starter Bundle — {top_name}</div>', unsafe_allow_html=True)
        bundle = [("🏠","Accommodation", vnd["accommodation"]),("🛍","Nearest Mall",vnd["mall"]),("🛕","Temple / Meditation",vnd["temple"])]
        if fd["tiffin"]: bundle.insert(1,("🍱","Tiffin Plan",    vnd["tiffin"]))
        if fd["bike"]:   bundle.insert(2,("🛵","Bike Rental",    vnd["bike"]))
        if fd["maid"]:   bundle.insert(3,("🧹","Maid Service",   vnd["maid"]))
        if fd["gym"]:    bundle.insert(4,("🏋","Gym",             vnd["gym"]))
        for icon, label, vendor in bundle:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:.7rem;padding:.55rem 0;border-bottom:1px solid #f1f5f9">
              <span style="font-size:1.1rem;min-width:1.4rem">{icon}</span>
              <span style="flex:1;font-weight:600;font-size:.88rem">{label}</span>
              <span style="color:#6366f1;font-size:.78rem;font-weight:600">{vendor}</span>
            </div>""", unsafe_allow_html=True)

    with c_col:
        st.markdown(f'<div class="sec-header">💰 Monthly Breakdown — {top_name}</div>', unsafe_allow_html=True)
        for item, amt in costs.items():
            st.markdown(f"""
            <div class="cost-row">
              <span style="color:#374151">{item}</span>
              <span style="font-weight:700">₹{amt:,}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="cost-total">
          <span style="color:#fff;font-weight:600;font-size:1rem">Total / Month</span>
          <span style="color:#fff;font-weight:800;font-size:1.4rem">₹{total:,}</span>
        </div>""", unsafe_allow_html=True)

    # ── CTA Buttons ──
    st.markdown("<br>", unsafe_allow_html=True)
    btn1, btn2 = st.columns(2)
    with btn1:
        if st.button(f"⚡  Activate My Move to {top_name}"):
            st.balloons()
            st.success(f"🎉 Plan activated for **{top_name}, {city}**! We'll be in touch shortly.")
    with btn2:
        wa_msg = (f"Hi! I used ReloPlan and matched to {top_name}, {city}. "
                  f"Budget ₹{fd['budget']:,}/mo. Please help me activate my move!")
        st.markdown(
            f'<a href="https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(wa_msg)}" target="_blank"'
            f' style="display:block;background:#25d366;color:#fff;text-align:center;'
            f'border-radius:10px;padding:.62rem;font-weight:700;font-size:.9rem;'
            f'text-decoration:none;box-shadow:0 4px 16px rgba(37,211,102,.35)">💬  WhatsApp My Plan</a>',
            unsafe_allow_html=True)

    # ── All scores expander ──
    with st.expander("📊 All Area Scores"):
        rows = [{"Area":k,"Score":f"{v['score']}%","Rent":f"₹{v['data']['avg_rent']:,}",
                 "Safety":stars(v['data']['safety']),"Commute":stars(v['data']['commute']),
                 "Social":stars(v['data']['social'])}
                for k,v in sorted(res["all"].items(), key=lambda x:x[1]["score"], reverse=True)]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ── Roadmap ──
    with st.expander("🚀 Scale-up Roadmap"):
        r1,r2 = st.columns(2)
        r1.markdown("""
**Now — MVP**
- ✅ Smart area matching · scoring algorithm
- ✅ Restaurants & nightlife per area
- ✅ Starter bundle + cost planner
- ✅ Instagram leads + WhatsApp CTA

**Phase 2 — Monetize**
- 💳 Razorpay payments
- 🤝 Vendor rev-share partnerships
- 🏢 Corporate relocation packages
        """)
        r2.markdown("""
**Phase 3 — Intelligence**
- 🗺 Google Maps (live commute times)
- 🤖 AI area recommendations (Claude API)
- 📊 Live rental & restaurant data APIs
- 📱 WhatsApp bot for plan delivery

**Phase 4 — Enterprise**
- 🏢 B2B HR relocation dashboard
- 🌍 Pan-India + international
- 🔗 White-label API
        """)

# ─────────────────────────────────────────────────────────────────
# PAGE: ADMIN
# ─────────────────────────────────────────────────────────────────
elif st.session_state.page == "admin":

    st.markdown("## 🔐 Admin Panel")

    if not st.session_state.admin_ok:
        _, mid, _ = st.columns([1,1,1])
        with mid:
            with st.form("login"):
                st.markdown("#### Enter password to continue")
                pwd = st.text_input("Password", type="password")
                if st.form_submit_button("Login", use_container_width=True):
                    if pwd == "admin123": st.session_state.admin_ok = True; st.rerun()
                    else: st.error("Incorrect password.")
        st.stop()

    if st.button("Logout"): st.session_state.admin_ok = False; st.rerun()

    t1, t2, t3, t4 = st.tabs(["📋 Submissions","📸 Instagram Leads","🏘 Areas","🏪 Vendors"])

    with t1:
        subs = st.session_state.subs
        st.markdown(f"**{len(subs)} submission(s)**")
        if subs: st.dataframe(pd.DataFrame(subs), use_container_width=True, hide_index=True)
        else: st.info("No submissions yet.")

    with t2:
        ig = st.session_state.ig_leads
        st.markdown(f"**{len(ig)} Instagram lead(s)**")
        if ig: st.dataframe(pd.DataFrame(ig), use_container_width=True, hide_index=True)
        else: st.info("No Instagram leads yet.")

    with t3:
        city = st.selectbox("City", list(CITIES.keys()), key="adm_city")
        for aname, ad in CITIES[city]["areas"].items():
            with st.expander(f"📍 {aname}  ·  ₹{ad['avg_rent']:,}/mo  ·  Match tags: {', '.join(ad.get('tags',[]))}"):
                c1,c2 = st.columns(2)
                c1.write(f"**Rent:** ₹{ad['avg_rent']:,} | **Safety:** {ad['safety']}/5 | **Commute:** {ad['commute']}/5")
                c2.write(f"**Social:** {ad['social']}/5 | **Gym:** {'✅' if ad['gym'] else '❌'} | **Temple:** {'✅' if ad['temple'] else '❌'}")
                st.markdown(f"**Restaurants:** {len(ad.get('restaurants',[]))} listed · **Party venues:** {len(ad.get('parties',[]))} listed")

    with t4:
        city = st.selectbox("City", list(VENDORS.keys()), key="adm_vendor")
        for cat, val in VENDORS[city].items():
            st.markdown(f"**{cat.title()}:** {val}")
