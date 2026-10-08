import pandas as pd
import numpy as np
import hashlib
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), 'ecommerce_dynamic_pricing_dataset.csv')

# Curated Primary Catalog: High quality, iconic, realistic flagship and popular products
# that will always appear at the top of the storefront and categories!
CURATED_FEATURED_PRODUCTS = [
    # Electronics Top Picks
    {
        "id": "P9994",
        "name": "Sony WH-1000XM5 Wireless Noise-Canceling Headphones",
        "category": "Electronics",
        "price": 399.99,
        "discount": 50.00,
        "rating": 5,
        "review_score": 4.9,
        "reviews_count": 3420,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80",
        "description": "Industry-leading dual processor noise cancellation with 8 mics, LDAC lossless codec, and 30-hour battery life.",
        "badge": "🔥 Best Seller",
        "badge_class": "badge-bestseller",
        "in_stock": True,
        "features": ["30-hour Battery", "Speak-to-Chat", "LDAC Hi-Res Audio", "Ultra-comfortable fit"]
    },
    {
        "id": "P8173",
        "name": "Apple Watch Series 9 GPS + Cellular 45mm",
        "category": "Electronics",
        "price": 429.00,
        "discount": 45.00,
        "rating": 5,
        "review_score": 4.8,
        "reviews_count": 2190,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80",
        "description": "S9 SiP chip, double tap gesture control, 2000-nit edge-to-edge Retina display, ECG and blood oxygen tracking.",
        "badge": "⚡ Flash Deal -20%",
        "badge_class": "badge-deal",
        "in_stock": True,
        "features": ["Always-On Retina", "ECG & Blood Oxygen", "Crash Detection", "50m Water Resistant"]
    },
    {
        "id": "P5945",
        "name": "Dell UltraSharp 27\" 4K USB-C Hub Monitor (IPS Black)",
        "category": "Electronics",
        "price": 579.50,
        "discount": 65.00,
        "rating": 4,
        "review_score": 4.6,
        "reviews_count": 980,
        "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&auto=format&fit=crop&q=80",
        "description": "Brilliant 4K UHD color accuracy with IPS Black technology, 90W power delivery USB-C, and RJ45 ethernet hub.",
        "badge": "🏆 Editor's Choice",
        "badge_class": "badge-editor",
        "in_stock": True,
        "features": ["4K UHD 3840x2160", "98% DCI-P3 Color", "90W USB-C PD Hub", "Height Adjustable"]
    },
    {
        "id": "P2756",
        "name": "Logitech MX Master 3S Wireless Performance Mouse",
        "category": "Electronics",
        "price": 99.99,
        "discount": 15.00,
        "rating": 5,
        "review_score": 4.9,
        "reviews_count": 5120,
        "image": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800&auto=format&fit=crop&q=80",
        "description": "Ergonomic quiet click mouse with 8K DPI glass sensor and ultra-fast MagSpeed electromagnetic scrolling.",
        "badge": "🚀 Trending Now",
        "badge_class": "badge-trending",
        "in_stock": True,
        "features": ["8000 DPI Glass Track", "Quiet Clicks", "USB-C Quick Charge", "Multi-OS Flow"]
    },
    {
        "id": "P4543",
        "name": "Bose SoundLink Revolve+ II Bluetooth Speaker",
        "category": "Electronics",
        "price": 329.00,
        "discount": 35.00,
        "rating": 4,
        "review_score": 4.7,
        "reviews_count": 1340,
        "image": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800&auto=format&fit=crop&q=80",
        "description": "True 360-degree deep, immersive sound with durable, water-resistant design and flexible fabric handle.",
        "badge": "⭐ 4.7 Top Rated",
        "badge_class": "badge-top",
        "in_stock": True,
        "features": ["True 360° Sound", "17h Playtime", "IP55 Water/Dust Resistant", "Built-in Mic"]
    },
    {
        "id": "P1170",
        "name": "Sony Alpha 7 IV Full-Frame Mirrorless Pro Camera",
        "category": "Electronics",
        "price": 899.00,
        "discount": 110.00,
        "rating": 5,
        "review_score": 4.9,
        "reviews_count": 780,
        "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&auto=format&fit=crop&q=80",
        "description": "33MP full-frame Exmor R sensor, real-time AI autofocus for humans and animals, and 4K 60p recording.",
        "badge": "💎 Luxury Edition",
        "badge_class": "badge-luxury",
        "in_stock": True,
        "features": ["33MP BSI CMOS Sensor", "4K 60p 10-bit 4:2:2", "759-pt Fast Hybrid AF", "5-axis Stabilization"]
    },
    {
        "id": "P4794",
        "name": "Anker Prime 100W GaN Multi-Port Fast Charger",
        "category": "Electronics",
        "price": 79.99,
        "discount": 12.00,
        "rating": 4,
        "review_score": 4.5,
        "reviews_count": 1840,
        "image": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=800&auto=format&fit=crop&q=80",
        "description": "Compact 3-port GaN charger delivering up to 100W high-speed charging for laptops, phones, and tablets.",
        "badge": "✨ New Arrival",
        "badge_class": "badge-new",
        "in_stock": True,
        "features": ["100W Max Output", "ActiveShield 2.0 Protection", "3 Ports (2 USB-C, 1 USB-A)", "Ultra-Compact"]
    },
    {
        "id": "P1511",
        "name": "Basic Stereo In-Ear Earphones with 3.5mm Jack",
        "category": "Electronics",
        "price": 24.99,
        "discount": 3.00,
        "rating": 3,
        "review_score": 3.4,
        "reviews_count": 210,
        "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&auto=format&fit=crop&q=80",
        "description": "Standard entry-level wired earbuds with inline microphone. Lightweight plastic construction.",
        "badge": None,
        "badge_class": None,
        "in_stock": True,
        "features": ["3.5mm Audio Jack", "Built-in Mic", "1.2m Cable", "Basic Sound"]
    },

    # Books Top Picks
    {
        "id": "P8392",
        "name": "Atomic Habits: Tiny Changes, Remarkable Results",
        "category": "Books",
        "price": 27.00,
        "discount": 5.00,
        "rating": 5,
        "review_score": 4.9,
        "reviews_count": 19400,
        "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&auto=format&fit=crop&q=80",
        "description": "The definitive guide to breaking bad behaviors and adopting good habits in four easy, science-backed steps.",
        "badge": "🔥 Best Seller",
        "badge_class": "badge-bestseller",
        "in_stock": True,
        "features": ["Hardcover Edition", "Includes Habit Tracker templates", "Over 15M copies sold", "James Clear"]
    },
    {
        "id": "P5778",
        "name": "Designing Data-Intensive Applications",
        "category": "Books",
        "price": 54.99,
        "discount": 10.00,
        "rating": 5,
        "review_score": 4.9,
        "reviews_count": 4120,
        "image": "https://images.unsplash.com/photo-1532012164546-f432f2e3edd4?w=800&auto=format&fit=crop&q=80",
        "description": "Martin Kleppmann's comprehensive exploration of distributed systems, storage engines, stream processing and fault tolerance.",
        "badge": "🏆 Editor's Choice",
        "badge_class": "badge-editor",
        "in_stock": True,
        "features": ["Definitive Architecture Reference", "Reliability & Scalability", "O'Reilly Media", "Paperback"]
    },
    {
        "id": "P4670",
        "name": "The Psychology of Money: Timeless Lessons on Wealth",
        "category": "Books",
        "price": 22.50,
        "discount": 4.00,
        "rating": 4,
        "review_score": 4.7,
        "reviews_count": 9800,
        "image": "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=800&auto=format&fit=crop&q=80",
        "description": "Morgan Housel shares 19 short stories exploring the strange ways people think about money, greed, and risk.",
        "badge": "⭐ 4.7 Top Rated",
        "badge_class": "badge-top",
        "in_stock": True,
        "features": ["19 Short Lessons", "Behavioral Finance", "Compact & Engaging", "Morgan Housel"]
    },
    {
        "id": "P1036",
        "name": "Artificial Intelligence: A Modern Approach (4th Ed)",
        "category": "Books",
        "price": 149.99,
        "discount": 25.00,
        "rating": 5,
        "review_score": 4.8,
        "reviews_count": 1640,
        "image": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=800&auto=format&fit=crop&q=80",
        "description": "The quintessential textbook on AI by Stuart Russell and Peter Norvig, covering modern search, probabilistic reasoning, and ML.",
        "badge": "💎 Luxury Edition",
        "badge_class": "badge-luxury",
        "in_stock": True,
        "features": ["Full Color Global Edition", "Covers Probabilistic & Search Algorithms", "Comprehensive 1100+ pages"]
    },
    {
        "id": "P9890",
        "name": "Deep Work: Rules for Focused Success",
        "category": "Books",
        "price": 28.00,
        "discount": 6.00,
        "rating": 4,
        "review_score": 4.6,
        "reviews_count": 7100,
        "image": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=800&auto=format&fit=crop&q=80",
        "description": "Cal Newport's framework to master cognitive tasks and transform your productivity through uninterrupted focus.",
        "badge": "🚀 Trending Now",
        "badge_class": "badge-trending",
        "in_stock": True,
        "features": ["Productivity Guide", "Actionable Frameworks", "Cal Newport", "Paperback"]
    },
    {
        "id": "P6280",
        "name": "Quick Reference Pocket Handbook for Engineers",
        "category": "Books",
        "price": 18.50,
        "discount": 2.00,
        "rating": 3,
        "review_score": 3.3,
        "reviews_count": 145,
        "image": "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=800&auto=format&fit=crop&q=80",
        "description": "Compact mass-market reference booklet for student formulas and basic calculations.",
        "badge": None,
        "badge_class": None,
        "in_stock": True,
        "features": ["Pocket Sized", "Formula Tables", "Spiral Bound", "Student Edition"]
    },

    # Clothing Top Picks
    {
        "id": "P1628",
        "name": "Men's StormTech All-Weather Alpine Parka Jacket",
        "category": "Clothing",
        "price": 189.00,
        "discount": 35.00,
        "rating": 5,
        "review_score": 4.8,
        "reviews_count": 1420,
        "image": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=800&auto=format&fit=crop&q=80",
        "description": "All-weather thermal insulation jacket featuring taped seams, breathable membrane, and fleece-lined storm hood.",
        "badge": "🔥 Best Seller",
        "badge_class": "badge-bestseller",
        "in_stock": True,
        "features": ["10K Waterproof Rating", "Thermal Tech Insulation", "Multiple Concealed Pockets", "Windproof"]
    },
    {
        "id": "P4211",
        "name": "Classic 100% Merino Wool Crewneck Knit Sweater",
        "category": "Clothing",
        "price": 110.00,
        "discount": 20.00,
        "rating": 4,
        "review_score": 4.7,
        "reviews_count": 980,
        "image": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=800&auto=format&fit=crop&q=80",
        "description": "100% extra-fine Australian Merino wool that delivers breathable warmth, luxuriously soft hand-feel, and timeless drape.",
        "badge": "⭐ 4.7 Top Rated",
        "badge_class": "badge-top",
        "in_stock": True,
        "features": ["100% Merino Wool", "Naturally Odor-Resistant", "Ribbed Collar & Cuffs", "Hand Washable"]
    },
    {
        "id": "P7502",
        "name": "Heritage 14oz Japanese Selvedge Raw Denim Jeans",
        "category": "Clothing",
        "price": 135.00,
        "discount": 25.00,
        "rating": 4,
        "review_score": 4.6,
        "reviews_count": 1540,
        "image": "https://images.unsplash.com/photo-1542272604-780c96856592?w=800&auto=format&fit=crop&q=80",
        "description": "14oz selvedge denim crafted on vintage shuttle looms for authentic wear patterns and lifetime durability.",
        "badge": "🏆 Editor's Choice",
        "badge_class": "badge-editor",
        "in_stock": True,
        "features": ["Selvedge Red-Line Stitch", "Reinforced Rivets", "Custom Button Fly", "Sanforized Denim"]
    },
    {
        "id": "P6065",
        "name": "Minimalist Handcrafted Italian Calfskin Sneakers",
        "category": "Clothing",
        "price": 165.00,
        "discount": 30.00,
        "rating": 5,
        "review_score": 4.9,
        "reviews_count": 2300,
        "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=800&auto=format&fit=crop&q=80",
        "description": "Full-grain calfskin leather low-tops with Margom rubber soles and memory foam ortholite insoles.",
        "badge": "💎 Luxury Edition",
        "badge_class": "badge-luxury",
        "in_stock": True,
        "features": ["Full-Grain Leather", "Cushioned OrthoLite Sole", "Handcrafted Stitching", "Made in Italy"]
    },
    {
        "id": "P6271",
        "name": "Athletic 4-Way Stretch Performance Training Hoodie",
        "category": "Clothing",
        "price": 79.99,
        "discount": 15.00,
        "rating": 4,
        "review_score": 4.5,
        "reviews_count": 860,
        "image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=800&auto=format&fit=crop&q=80",
        "description": "Four-way stretch moisture-wicking fleece hoodie tailored for training sessions and casual weekend comfort.",
        "badge": "🚀 Trending Now",
        "badge_class": "badge-trending",
        "in_stock": True,
        "features": ["Moisture-Wicking Tech", "Thumbhole Cuffs", "Zippered Security Pocket", "Breathable Fleece"]
    },
    {
        "id": "P2945",
        "name": "Basic Crewneck Cotton T-Shirt (3-Pack)",
        "category": "Clothing",
        "price": 29.99,
        "discount": 4.00,
        "rating": 3,
        "review_score": 3.4,
        "reviews_count": 310,
        "image": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800&auto=format&fit=crop&q=80",
        "description": "Everyday standard cotton-poly blend tees for casual loungewear and layering.",
        "badge": None,
        "badge_class": None,
        "in_stock": True,
        "features": ["60/40 Cotton-Poly", "Tagless Collar", "Machine Washable", "Value Pack"]
    },

    # Home & Kitchen Top Picks
    {
        "id": "P5136",
        "name": "Breville Barista Touch Automated Espresso Machine",
        "category": "Home & Kitchen",
        "price": 799.95,
        "discount": 95.00,
        "rating": 5,
        "review_score": 4.9,
        "reviews_count": 3400,
        "image": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=800&auto=format&fit=crop&q=80",
        "description": "Automated touchscreen with integrated conical burr grinder, 3-second ThermoJet heat up, and microfoam texturing.",
        "badge": "🔥 Best Seller",
        "badge_class": "badge-bestseller",
        "in_stock": True,
        "features": ["Touch Screen Interface", "ThermoJet 3s Heating", "Auto Microfoam Milk", "Integrated Grinder"]
    },
    {
        "id": "P8427",
        "name": "Ninja DualZone 8-in-1 Air Fryer XL (10 Qt)",
        "category": "Home & Kitchen",
        "price": 219.99,
        "discount": 45.00,
        "rating": 5,
        "review_score": 4.8,
        "reviews_count": 5200,
        "image": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800&auto=format&fit=crop&q=80",
        "description": "Two independent cooking baskets let you cook 2 foods, 2 ways at the same time with Smart Finish sync.",
        "badge": "⚡ Flash Deal -25%",
        "badge_class": "badge-deal",
        "in_stock": True,
        "features": ["2 Independent Baskets", "Smart Finish Sync", "Air Fry, Roast, Dehydrate", "Dishwasher Safe"]
    },
    {
        "id": "P4759",
        "name": "Dyson V15 Detect Cordless Vacuum Cleaner",
        "category": "Home & Kitchen",
        "price": 649.00,
        "discount": 80.00,
        "rating": 5,
        "review_score": 4.9,
        "reviews_count": 2100,
        "image": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=800&auto=format&fit=crop&q=80",
        "description": "Laser illumination reveals invisible dust on hard floors, with piezoelectric sensor for automatic suction adaptation.",
        "badge": "⭐ 4.9 Top Rated",
        "badge_class": "badge-top",
        "in_stock": True,
        "features": ["Laser Fluffy Cleaner Head", "60min Runtime", "LCD Particle Counter", "Anti-Tangle Hair Screw"]
    },
    {
        "id": "P6673",
        "name": "Le Creuset Enameled Cast Iron Dutch Oven (5.5 Qt)",
        "category": "Home & Kitchen",
        "price": 385.00,
        "discount": 45.00,
        "rating": 5,
        "review_score": 4.9,
        "reviews_count": 2450,
        "image": "https://images.unsplash.com/photo-1584992236310-6edddc08acff?w=800&auto=format&fit=crop&q=80",
        "description": "Iconic French-made enameled cast iron delivers superior heat distribution and moisture retention for braising and baking.",
        "badge": "💎 Luxury Edition",
        "badge_class": "badge-luxury",
        "in_stock": True,
        "features": ["Enameled Cast Iron", "Oven-safe to 500°F", "Lifetime Warranty", "Handcrafted in France"]
    },
    {
        "id": "P8535",
        "name": "Smart PureAir H13 True HEPA Air Purifier",
        "category": "Home & Kitchen",
        "price": 149.00,
        "discount": 20.00,
        "rating": 4,
        "review_score": 4.6,
        "reviews_count": 1380,
        "image": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=800&auto=format&fit=crop&q=80",
        "description": "True HEPA H13 3-stage filtration capturing 99.97% of airborne particles, allergens, pet dander and VOCs.",
        "badge": "🌿 Eco-Friendly",
        "badge_class": "badge-eco",
        "in_stock": True,
        "features": ["H13 True HEPA Filter", "Real-time PM2.5 Sensor", "Whisper Quiet Sleep Mode", "App Controlled"]
    },
    {
        "id": "P8458",
        "name": "Basic Non-Stick 8-inch Aluminum Frying Pan",
        "category": "Home & Kitchen",
        "price": 21.99,
        "discount": 3.00,
        "rating": 3,
        "review_score": 3.2,
        "reviews_count": 290,
        "image": "https://images.unsplash.com/photo-1593618998160-e34014e67546?w=800&auto=format&fit=crop&q=80",
        "description": "Standard aluminum everyday skillet with non-stick coating and heat-resistant handle.",
        "badge": None,
        "badge_class": None,
        "in_stock": True,
        "features": ["Aluminum Construction", "Non-Stick Surface", "Bakelite Handle", "Hand Wash Recommended"]
    }
]

# Additional procedural catalogs for remaining dataset Product_IDs
EXPANDED_IMAGE_POOLS = {
    "Electronics": [
        ("Wireless Noise-Canceling Earbuds Pro", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80"),
        ("Ultra-Slim 10000mAh Power Bank (Fast Charge)", "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=800&auto=format&fit=crop&q=80"),
        ("Mechanical RGB Gaming Keyboard (Hot-Swap)", "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&auto=format&fit=crop&q=80"),
        ("Dual-Band Wi-Fi 6 Gigabit Router", "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=800&auto=format&fit=crop&q=80"),
        ("27-inch 144Hz Gaming Monitor (QHD)", "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&auto=format&fit=crop&q=80"),
        ("4K Streaming Media Player with Voice Remote", "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800&auto=format&fit=crop&q=80")
    ],
    "Books": [
        ("Clean Code: A Handbook of Agile Software Craftsmanship", "https://images.unsplash.com/photo-1532012164546-f432f2e3edd4?w=800&auto=format&fit=crop&q=80"),
        ("Thinking, Fast and Slow by Daniel Kahneman", "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=800&auto=format&fit=crop&q=80"),
        ("The Lean Startup: Continuous Innovation Guide", "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?w=800&auto=format&fit=crop&q=80"),
        ("Sapiens: A Brief History of Humankind", "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=800&auto=format&fit=crop&q=80"),
        ("Meditations by Marcus Aurelius (Modern Translation)", "https://images.unsplash.com/photo-1476275466078-4007374efbbe?w=800&auto=format&fit=crop&q=80"),
        ("The Pragmatic Programmer: Your Journey to Mastery", "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=800&auto=format&fit=crop&q=80")
    ],
    "Clothing": [
        ("Classic Oxford Cotton Button-Down Shirt", "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=800&auto=format&fit=crop&q=80"),
        ("Waterproof Chelsea Leather Boots", "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&auto=format&fit=crop&q=80"),
        ("Smart 4-Way Stretch Commuter Chino Pants", "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=800&auto=format&fit=crop&q=80"),
        ("Luxury Cashmere V-Neck Knit Pullover", "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=800&auto=format&fit=crop&q=80"),
        ("Heritage Raw Denim Trucker Jacket", "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=800&auto=format&fit=crop&q=80"),
        ("Cloud-Cushioned Carbon Running Shoes", "https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=800&auto=format&fit=crop&q=80")
    ],
    "Home & Kitchen": [
        ("Precision Conical Burr Coffee Grinder", "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=800&auto=format&fit=crop&q=80"),
        ("Japanese Damascus Steel 8\" Chef Knife", "https://images.unsplash.com/photo-1593618998160-e34014e67546?w=800&auto=format&fit=crop&q=80"),
        ("Smart Precision Sous Vide Immersion Cooker", "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800&auto=format&fit=crop&q=80"),
        ("Tri-Ply Clad Stainless Steel Cookware Set (10-Pc)", "https://images.unsplash.com/photo-1584992236310-6edddc08acff?w=800&auto=format&fit=crop&q=80"),
        ("High-Velocity Professional Blender 1800W", "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=800&auto=format&fit=crop&q=80"),
        ("Gooseneck Electric Temperature Control Kettle", "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&auto=format&fit=crop&q=80")
    ]
}

# Cache singleton
_CATALOG_CACHE = None
_CATALOG_MAP = {}

def build_full_catalog():
    global _CATALOG_CACHE, _CATALOG_MAP
    if _CATALOG_CACHE is not None:
        return _CATALOG_CACHE

    df = pd.read_csv(DATA_PATH)
    grouped = df.groupby(['Product_ID', 'Product_Category']).agg({
        'Price': 'mean',
        'Discount': 'mean',
        'Review_Rating': 'mean',
        'Customer_Age': 'mean',
        'Transaction_ID': 'count'
    }).reset_index()

    catalog = []
    seen_ids = set()

    # 1. First add curated high-quality featured products (ensures page 1 is always premium & balanced!)
    for item in CURATED_FEATURED_PRODUCTS:
        catalog.append(item)
        _CATALOG_MAP[item['id']] = item
        seen_ids.add(item['id'])

    # 2. Add remaining dataset Product_IDs
    for idx, row in grouped.iterrows():
        pid = row['Product_ID']
        if pid in seen_ids:
            continue

        cat = row['Product_Category']
        price = round(float(row['Price']), 2)
        discount = round(float(row['Discount']), 2)
        raw_rating = float(row['Review_Rating'])
        rating_int = int(round(raw_rating))

        h_val = int(hashlib.md5(pid.encode()).hexdigest(), 16)
        noise = ((h_val % 100) / 100.0) * 0.6 - 0.3

        # Balanced star rating mapping
        if rating_int == 1:
            review_score = round(min(2.2, max(1.3, 1.8 + noise)), 1)
            reviews_count = 18 + int(h_val % 190)
        elif rating_int == 2:
            review_score = round(min(2.9, max(2.3, 2.6 + noise)), 1)
            reviews_count = 35 + int(h_val % 380)
        elif rating_int == 3:
            review_score = round(min(3.7, max(3.1, 3.4 + noise)), 1)
            reviews_count = 90 + int(h_val % 850)
        elif rating_int == 4:
            review_score = round(min(4.4, max(3.8, 4.1 + noise)), 1)
            reviews_count = 210 + int(h_val % 1950)
        else: # 5
            review_score = round(min(4.9, max(4.5, 4.7 + noise)), 1)
            reviews_count = 420 + int(h_val % 4200)

        # Balanced badge assignment (~45-50% of items have badges, others clean)
        disc_pct = discount / (price + 1e-5)
        badge = None
        badge_class = None

        if disc_pct >= 0.25:
            badge = f"⚡ Flash Deal -{int(disc_pct*100)}%"
            badge_class = "badge-deal"
        elif rating_int == 5 and (h_val % 4 == 0):
            badge = "🔥 Best Seller"
            badge_class = "badge-bestseller"
        elif rating_int == 5 and (h_val % 4 == 1):
            badge = "⭐ 4.9 Top Rated"
            badge_class = "badge-top"
        elif rating_int == 4 and (h_val % 4 == 0):
            badge = "🏆 Editor's Choice"
            badge_class = "badge-editor"
        elif (h_val % 5 == 0):
            badge = "🚀 Trending Now"
            badge_class = "badge-trending"
        elif (h_val % 6 == 0):
            badge = "✨ New Arrival"
            badge_class = "badge-new"
        elif (h_val % 7 == 0) and rating_int >= 4:
            badge = "💎 Luxury Edition"
            badge_class = "badge-luxury"

        # Image and name selection
        pool = EXPANDED_IMAGE_POOLS.get(cat, EXPANDED_IMAGE_POOLS["Electronics"])
        base_name, base_img = pool[h_val % len(pool)]
        
        item_name = f"{base_name} (#{pid[1:]})"
        desc = f"Verified {cat.lower()} item with reliable construction and performance for everyday demands."

        item_obj = {
            "id": pid,
            "name": item_name,
            "category": cat,
            "price": price,
            "discount": discount,
            "rating": rating_int,
            "review_score": review_score,
            "reviews_count": reviews_count,
            "image": base_img,
            "description": desc,
            "badge": badge,
            "badge_class": badge_class,
            "in_stock": True,
            "features": ["Quality Tested", "Standard Warranty", "Certified Safety Standards", "Easy 30-Day Returns"]
        }
        catalog.append(item_obj)
        _CATALOG_MAP[pid] = item_obj
        seen_ids.add(pid)

    _CATALOG_CACHE = catalog
    return _CATALOG_CACHE

def get_all_products():
    return build_full_catalog()

def get_product_by_id(product_id):
    if not _CATALOG_MAP:
        build_full_catalog()
    return _CATALOG_MAP.get(product_id)

def get_category_counts():
    cat = build_full_catalog()
    counts = {"All": len(cat), "Electronics": 0, "Books": 0, "Clothing": 0, "Home & Kitchen": 0}
    for item in cat:
        c = item['category']
        if c in counts:
            counts[c] += 1
    return counts
