import pandas as pd
import numpy as np
import hashlib
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), 'ecommerce_dynamic_pricing_dataset.csv')

# Curated Primary Catalog: High quality, accurate, stunning products with 100% matching real photos,
# realistic low-stock quantity alerts, varied real-world bank credit card offers, and clothing size options.
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
        "image": "https://images.pexels.com/photos/3394650/pexels-photo-3394650.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Industry-leading dual processor noise cancellation with 8 mics, LDAC lossless codec, and 30-hour battery life.",
        "badge": "🔥 Best Seller",
        "badge_class": "badge-bestseller",
        "in_stock": True,
        "stock_quantity": 3,
        "colors": None,
        "sizes": None,
        "card_offer": {
            "bank": "HDFC Bank",
            "card": "Millennia / Regalia",
            "discount_pct": 10,
            "max_discount": 50.0,
            "label": "10% Instant Off on HDFC Bank Cards"
        },
        "min_price": 319.99,
        "max_price": 479.99,
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
        "image": "https://images.pexels.com/photos/267394/pexels-photo-267394.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "S9 SiP chip, double tap gesture control, 2000-nit edge-to-edge Retina display, ECG and blood oxygen tracking.",
        "badge": "⚡ Flash Deal -20%",
        "badge_class": "badge-deal",
        "in_stock": True,
        "stock_quantity": 2,
        "colors": None,
        "sizes": None,
        "card_offer": {
            "bank": "Chase",
            "card": "Sapphire Reserve",
            "discount_pct": 15,
            "max_discount": 75.0,
            "label": "15% Bonus Savings with Chase Cards"
        },
        "min_price": 340.00,
        "max_price": 510.00,
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
        "image": "https://images.pexels.com/photos/1714208/pexels-photo-1714208.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Brilliant 4K UHD color accuracy with IPS Black technology, 90W power delivery USB-C, and RJ45 ethernet hub.",
        "badge": "🏆 Editor's Choice",
        "badge_class": "badge-editor",
        "in_stock": True,
        "stock_quantity": 7,
        "colors": None,
        "sizes": None,
        "card_offer": {
            "bank": "ICICI Bank",
            "card": "Amazon Pay / Coral",
            "discount_pct": 7.5,
            "max_discount": 45.0,
            "label": "7.5% Instant Off with ICICI Cards"
        },
        "min_price": 460.00,
        "max_price": 690.00,
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
        "image": "https://images.pexels.com/photos/2115257/pexels-photo-2115257.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Ergonomic quiet click mouse with 8K DPI glass sensor and ultra-fast MagSpeed electromagnetic scrolling.",
        "badge": "🚀 Trending Now",
        "badge_class": "badge-trending",
        "in_stock": True,
        "stock_quantity": 3,
        "colors": None,
        "sizes": None,
        "card_offer": None,
        "min_price": 79.99,
        "max_price": 119.99,
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
        "image": "https://images.pexels.com/photos/1279365/pexels-photo-1279365.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "True 360-degree deep, immersive sound with durable, water-resistant design and flexible fabric handle.",
        "badge": "⭐ 4.7 Top Rated",
        "badge_class": "badge-top",
        "in_stock": True,
        "stock_quantity": 6,
        "colors": None,
        "sizes": None,
        "card_offer": {
            "bank": "Citi",
            "card": "Citi Premier Rewards",
            "discount_pct": 5,
            "max_discount": 20.0,
            "label": "5% Extra Savings on Citi Cards"
        },
        "min_price": 260.00,
        "max_price": 395.00,
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
        "image": "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "33MP full-frame Exmor R sensor, real-time AI autofocus for humans and animals, and 4K 60p recording.",
        "badge": "💎 Luxury Edition",
        "badge_class": "badge-luxury",
        "in_stock": True,
        "stock_quantity": 2,
        "colors": None,
        "sizes": None,
        "card_offer": {
            "bank": "Amex",
            "card": "American Express Platinum",
            "discount_pct": 12,
            "max_discount": 120.0,
            "label": "12% Instant Cashback with Amex"
        },
        "min_price": 720.00,
        "max_price": 1080.00,
        "features": ["33MP BSI CMOS Sensor", "4K 60p 10-bit 4:2:2", "759-pt Fast Hybrid AF", "5-axis Stabilization"]
    },
    {
        "id": "P4794",
        "name": "Apple MacBook Pro 16\" M3 Max Laptop",
        "category": "Electronics",
        "price": 1299.00,
        "discount": 150.00,
        "rating": 5,
        "review_score": 4.9,
        "reviews_count": 1840,
        "image": "https://images.pexels.com/photos/18105/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=800",
        "description": "Blazing fast computing with Liquid Retina XDR display, up to 22 hours of battery life, and pro connectivity.",
        "badge": "✨ New Arrival",
        "badge_class": "badge-new",
        "in_stock": True,
        "stock_quantity": 4,
        "colors": None,
        "sizes": None,
        "card_offer": None,
        "min_price": 1050.00,
        "max_price": 1550.00,
        "features": ["Liquid Retina XDR Display", "Up to 22h Battery", "Unified Memory Architecture", "MagSafe Fast Charging"]
    },
    {
        "id": "P1511",
        "name": "True Wireless Noise-Canceling In-Ear Earbuds Pro",
        "category": "Electronics",
        "price": 49.99,
        "discount": 8.00,
        "rating": 4,
        "review_score": 4.3,
        "reviews_count": 620,
        "image": "https://images.pexels.com/photos/3780681/pexels-photo-3780681.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Ergonomic true wireless in-ear earbuds with compact charging case, dynamic drivers, and crisp hands-free audio.",
        "badge": None,
        "badge_class": None,
        "in_stock": True,
        "stock_quantity": 14,
        "colors": None,
        "sizes": None,
        "card_offer": None,
        "min_price": 39.99,
        "max_price": 59.99,
        "features": ["Wireless Charging Case", "28h Total Battery", "Sweat Resistant", "Built-in HD Mic"]
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
        "image": "https://images.pexels.com/photos/1370295/pexels-photo-1370295.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "The definitive guide to breaking bad behaviors and adopting good habits in four easy, science-backed steps.",
        "badge": "🔥 Best Seller",
        "badge_class": "badge-bestseller",
        "in_stock": True,
        "stock_quantity": 60,
        "colors": None,
        "sizes": None,
        "card_offer": {
            "bank": "ICICI Bank",
            "card": "Amazon Pay ICICI",
            "discount_pct": 10,
            "max_discount": 10.0,
            "label": "10% Cashback on ICICI Cards"
        },
        "min_price": 21.00,
        "max_price": 32.00,
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
        "image": "https://images.pexels.com/photos/256541/pexels-photo-256541.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Martin Kleppmann's comprehensive exploration of distributed systems, storage engines, stream processing and fault tolerance.",
        "badge": "🏆 Editor's Choice",
        "badge_class": "badge-editor",
        "in_stock": True,
        "stock_quantity": 4,
        "colors": None,
        "sizes": None,
        "card_offer": None,
        "min_price": 43.99,
        "max_price": 65.99,
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
        "image": "https://images.pexels.com/photos/159711/books-bookstore-book-reading-159711.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Morgan Housel shares 19 short stories exploring the strange ways people think about money, greed, and risk.",
        "badge": "⭐ 4.7 Top Rated",
        "badge_class": "badge-top",
        "in_stock": True,
        "stock_quantity": 18,
        "colors": None,
        "sizes": None,
        "card_offer": {
            "bank": "Axis Bank",
            "card": "Axis Neo / Ace",
            "discount_pct": 8,
            "max_discount": 5.0,
            "label": "8% Off on Axis Bank Cards"
        },
        "min_price": 18.00,
        "max_price": 27.00,
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
        "image": "https://images.pexels.com/photos/1181671/pexels-photo-1181671.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "The quintessential textbook on AI by Stuart Russell and Peter Norvig, covering modern search, probabilistic reasoning, and ML.",
        "badge": "💎 Luxury Edition",
        "badge_class": "badge-luxury",
        "in_stock": True,
        "stock_quantity": 2,
        "colors": None,
        "sizes": None,
        "card_offer": {
            "bank": "HDFC Bank",
            "card": "HDFC Millennia",
            "discount_pct": 10,
            "max_discount": 20.0,
            "label": "10% Instant Off on HDFC Bank Cards"
        },
        "min_price": 120.00,
        "max_price": 180.00,
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
        "image": "https://images.pexels.com/photos/415071/pexels-photo-415071.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Cal Newport's framework to master cognitive tasks and transform your productivity through uninterrupted focus.",
        "badge": "🚀 Trending Now",
        "badge_class": "badge-trending",
        "in_stock": True,
        "stock_quantity": 8,
        "colors": None,
        "sizes": None,
        "card_offer": None,
        "min_price": 22.00,
        "max_price": 34.00,
        "features": ["Productivity Guide", "Actionable Frameworks", "Cal Newport", "Paperback"]
    },
    {
        "id": "P6280",
        "name": "The Pragmatic Programmer: Your Journey to Mastery",
        "category": "Books",
        "price": 38.50,
        "discount": 5.00,
        "rating": 4,
        "review_score": 4.7,
        "reviews_count": 2450,
        "image": "https://images.pexels.com/photos/2465877/pexels-photo-2465877.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Timeless principles and battle-tested guidance on writing robust, maintainable, and elegant software.",
        "badge": None,
        "badge_class": None,
        "in_stock": True,
        "stock_quantity": 25,
        "colors": None,
        "sizes": None,
        "card_offer": None,
        "min_price": 30.00,
        "max_price": 46.00,
        "features": ["20th Anniversary Edition", "Software Craftsmanship", "Classic Wisdom", "David Thomas & Andrew Hunt"]
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
        "image": "https://images.pexels.com/photos/1124465/pexels-photo-1124465.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "All-weather thermal insulation jacket featuring taped seams, breathable membrane, and fleece-lined storm hood.",
        "badge": "🔥 Best Seller",
        "badge_class": "badge-bestseller",
        "in_stock": True,
        "stock_quantity": 3,
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "colors": None,
        "card_offer": {
            "bank": "Axis Bank",
            "card": "Axis Flipkart / Magnus",
            "discount_pct": 8,
            "max_discount": 30.0,
            "label": "8% Instant Discount with Axis Bank"
        },
        "min_price": 150.00,
        "max_price": 225.00,
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
        "image": "https://images.pexels.com/photos/45982/pexels-photo-45982.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "100% extra-fine Australian Merino wool that delivers breathable warmth, luxuriously soft hand-feel, and timeless drape.",
        "badge": "⭐ 4.7 Top Rated",
        "badge_class": "badge-top",
        "in_stock": True,
        "stock_quantity": 5,
        "sizes": ["XS", "S", "M", "L", "XL"],
        "colors": None,
        "card_offer": {
            "bank": "ICICI Bank",
            "card": "ICICI Coral / Rubyx",
            "discount_pct": 7.5,
            "max_discount": 20.0,
            "label": "7.5% Off with ICICI Bank Cards"
        },
        "min_price": 88.00,
        "max_price": 132.00,
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
        "image": "https://images.pexels.com/photos/1598507/pexels-photo-1598507.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "14oz selvedge denim crafted on vintage shuttle looms for authentic wear patterns and lifetime durability.",
        "badge": "🏆 Editor's Choice",
        "badge_class": "badge-editor",
        "in_stock": True,
        "stock_quantity": 12,
        "sizes": ["30W 32L", "32W 32L", "34W 32L", "36W 34L"],
        "colors": None,
        "card_offer": None,
        "min_price": 108.00,
        "max_price": 162.00,
        "features": ["Selvedge Red-Line Stitch", "Reinforced Rivets", "Custom Button Fly", "Sanforized Denim"]
    },
    {
        "id": "P6065",
        "name": "Breathable Cushion-Padded Athletic Running Sneakers",
        "category": "Clothing",
        "price": 145.00,
        "discount": 30.00,
        "rating": 5,
        "review_score": 4.9,
        "reviews_count": 2300,
        "image": "https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "High-rebound responsive foam sole with breathable engineered knit upper designed for running performance and street style.",
        "badge": "💎 Luxury Edition",
        "badge_class": "badge-luxury",
        "in_stock": True,
        "stock_quantity": 4,
        "sizes": ["US 8", "US 9", "US 10", "US 11", "US 12"],
        "colors": None,
        "card_offer": {
            "bank": "Chase",
            "card": "Chase Freedom Unlimited",
            "discount_pct": 10,
            "max_discount": 25.0,
            "label": "10% Off with Chase Credit Cards"
        },
        "min_price": 115.00,
        "max_price": 175.00,
        "features": ["High-Energy Return Midsole", "Breathable Engineered Mesh", "Anti-Slip Rubber Grip", "OrthoLite Footbed"]
    },
    {
        "id": "P6271",
        "name": "Heavyweight Fleece Streetwear Pullover Hoodie",
        "category": "Clothing",
        "price": 79.99,
        "discount": 15.00,
        "rating": 4,
        "review_score": 4.5,
        "reviews_count": 860,
        "image": "https://images.pexels.com/photos/1183266/pexels-photo-1183266.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Four-way stretch heavy fleece hoodie tailored with drop shoulders, front pouch pocket, and rib-knit cuffs for premium comfort.",
        "badge": "🚀 Trending Now",
        "badge_class": "badge-trending",
        "in_stock": True,
        "stock_quantity": 28,
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "colors": None,
        "card_offer": None,
        "min_price": 64.00,
        "max_price": 96.00,
        "features": ["Heavyweight 450 GSM Cotton", "Double-Layered Hood", "Kangaroo Front Pocket", "Drop Shoulder Fit"]
    },
    {
        "id": "P2945",
        "name": "Essential 100% Organic Cotton Crewneck T-Shirt",
        "category": "Clothing",
        "price": 29.99,
        "discount": 4.00,
        "rating": 3,
        "review_score": 3.4,
        "reviews_count": 310,
        "image": "https://images.pexels.com/photos/996329/pexels-photo-996329.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Everyday premium combed organic cotton crewneck tee designed with relaxed drape, tagless comfort, and enduring shape.",
        "badge": None,
        "badge_class": None,
        "in_stock": True,
        "stock_quantity": 40,
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "colors": None,
        "card_offer": None,
        "min_price": 24.00,
        "max_price": 36.00,
        "features": ["100% Ring-Spun Cotton", "Pre-Shrunk Fabric", "Ribbed Collar", "Machine Washable"]
    },

    # Home & Kitchen Top Picks
    {
        "id": "P5136",
        "name": "Stainless Steel Barista Espresso & Cappuccino Machine",
        "category": "Home & Kitchen",
        "price": 799.95,
        "discount": 95.00,
        "rating": 5,
        "review_score": 4.9,
        "reviews_count": 3400,
        "image": "https://images.pexels.com/photos/324028/pexels-photo-324028.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Commercial-grade 15-bar espresso machine with precision conical burr grinder, 3-second rapid heating, and microfoam steam wand.",
        "badge": "🔥 Best Seller",
        "badge_class": "badge-bestseller",
        "in_stock": True,
        "stock_quantity": 2,
        "colors": None,
        "sizes": None,
        "card_offer": {
            "bank": "HDFC Bank",
            "card": "Infinia / Regalia Gold",
            "discount_pct": 12,
            "max_discount": 100.0,
            "label": "12% Instant Savings with HDFC Bank"
        },
        "min_price": 640.00,
        "max_price": 960.00,
        "features": ["15-Bar Italian Pump", "ThermoJet Fast Heating", "Integrated Steam Wand", "Commercial 54mm Portafilter"]
    },
    {
        "id": "P8427",
        "name": "Digital Touchscreen Air Fryer & Convection Cooker XL",
        "category": "Home & Kitchen",
        "price": 219.99,
        "discount": 45.00,
        "rating": 5,
        "review_score": 4.8,
        "reviews_count": 5200,
        "image": "https://images.pexels.com/photos/4397916/pexels-photo-4397916.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "High-capacity air fryer with dual heating zones, crisp finish convection fan, and 8 one-touch digital cooking presets.",
        "badge": "⚡ Flash Deal -25%",
        "badge_class": "badge-deal",
        "in_stock": True,
        "stock_quantity": 7,
        "colors": None,
        "sizes": None,
        "card_offer": {
            "bank": "Citi",
            "card": "Citi Rewards",
            "discount_pct": 5,
            "max_discount": 20.0,
            "label": "5% Extra Discount with Citi Cards"
        },
        "min_price": 175.00,
        "max_price": 265.00,
        "features": ["Rapid 360° Air Circulation", "8 One-Touch Presets", "Non-Stick Dishwasher Safe Basket", "Up to 85% Less Oil"]
    },
    {
        "id": "P4759",
        "name": "Cordless Multi-Surface Stick Vacuum Cleaner",
        "category": "Home & Kitchen",
        "price": 549.00,
        "discount": 70.00,
        "rating": 5,
        "review_score": 4.9,
        "reviews_count": 2100,
        "image": "https://images.pexels.com/photos/4108714/pexels-photo-4108714.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Powerful cordless vacuum with optical dust illumination, whole-machine HEPA filtration, and 60 minutes of uninterrupted suction.",
        "badge": "⭐ 4.9 Top Rated",
        "badge_class": "badge-top",
        "in_stock": True,
        "stock_quantity": 3,
        "colors": None,
        "sizes": None,
        "card_offer": {
            "bank": "Amex",
            "card": "Amex Membership Rewards",
            "discount_pct": 15,
            "max_discount": 95.0,
            "label": "15% Instant Cashback with Amex"
        },
        "min_price": 440.00,
        "max_price": 660.00,
        "features": ["High-Torque Brush Bar", "60-Minute Fade-Free Power", "Whole-Machine HEPA Filtration", "Wall-Mounted Dock"]
    },
    {
        "id": "P8535",
        "name": "Heavy-Duty Multi-Speed Stand Food & Dough Mixer",
        "category": "Home & Kitchen",
        "price": 189.00,
        "discount": 25.00,
        "rating": 4,
        "review_score": 4.6,
        "reviews_count": 1380,
        "image": "https://images.pexels.com/photos/4397920/pexels-photo-4397920.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Durable metal gear stand mixer with 5.5-quart stainless steel bowl, planetary mixing action, and dishwasher-safe attachments.",
        "badge": "🚀 Trending Now",
        "badge_class": "badge-trending",
        "in_stock": True,
        "stock_quantity": 11,
        "colors": None,
        "sizes": None,
        "card_offer": None,
        "min_price": 150.00,
        "max_price": 228.00,
        "features": ["5.5-Qt Stainless Steel Bowl", "10 Optimized Speeds", "Tilt-Head Design", "Dough Hook, Whisk & Beater Included"]
    },
    {
        "id": "P8458",
        "name": "Pre-Seasoned Heavy Duty Cast Iron Skillet (10-Inch)",
        "category": "Home & Kitchen",
        "price": 29.99,
        "discount": 4.00,
        "rating": 4,
        "review_score": 4.5,
        "reviews_count": 1290,
        "image": "https://images.pexels.com/photos/3490257/pexels-photo-3490257.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Traditional pre-seasoned cast iron skillet with dual pour spouts, exceptional heat retention, and lifetime cooking durability.",
        "badge": None,
        "badge_class": None,
        "in_stock": True,
        "stock_quantity": 35,
        "colors": None,
        "sizes": None,
        "card_offer": None,
        "min_price": 24.00,
        "max_price": 36.00,
        "features": ["100% Pure Cast Iron", "Pre-Seasoned with Vegetable Oil", "Superior Heat Retention", "Oven & Campfire Safe"]
    }
]

# Additional procedural catalogs for remaining dataset Product_IDs using verified high-resolution Pexels URLs
EXPANDED_IMAGE_POOLS = {
    "Electronics": [
        ("Wireless Noise-Canceling Headphones", "https://images.pexels.com/photos/3394650/pexels-photo-3394650.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("Ultra-Slim 27-inch 4K UHD Desktop Monitor", "https://images.pexels.com/photos/1714208/pexels-photo-1714208.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("Ergonomic Wireless Optical Mouse", "https://images.pexels.com/photos/2115257/pexels-photo-2115257.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("Portable 360° Wireless Bluetooth Speaker", "https://images.pexels.com/photos/1279365/pexels-photo-1279365.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("Smart Fitness Watch with Heart Rate Monitor", "https://images.pexels.com/photos/267394/pexels-photo-267394.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("True Wireless In-Ear Earbuds with Charging Case", "https://images.pexels.com/photos/3780681/pexels-photo-3780681.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("Mirrorless 4K Full-Frame Digital Camera", "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("Ultra-Thin Pro 15.6-inch Laptop", "https://images.pexels.com/photos/18105/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=800")
    ],
    "Books": [
        ("The Habit Blueprint & Peak Performance", "https://images.pexels.com/photos/1370295/pexels-photo-1370295.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("Data Systems Architecture & Engineering", "https://images.pexels.com/photos/256541/pexels-photo-256541.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("The Psychology of Wealth & Decision Making", "https://images.pexels.com/photos/159711/books-bookstore-book-reading-159711.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("Foundations of Philosophy & Modern Logic", "https://images.pexels.com/photos/2465877/pexels-photo-2465877.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("Deep Focus: Productivity in the Digital Age", "https://images.pexels.com/photos/415071/pexels-photo-415071.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("The Pragmatic Developer's Field Guide", "https://images.pexels.com/photos/1181671/pexels-photo-1181671.jpeg?auto=compress&cs=tinysrgb&w=800")
    ],
    "Clothing": [
        ("All-Weather Insulated Winter Parka Jacket", "https://images.pexels.com/photos/1124465/pexels-photo-1124465.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("Classic Soft Knit Crewneck Pullover Sweater", "https://images.pexels.com/photos/45982/pexels-photo-45982.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("Straight-Fit Stretch Denim Jeans", "https://images.pexels.com/photos/1598507/pexels-photo-1598507.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("Cushioned Breathable Athletic Running Sneakers", "https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("Heavyweight Cotton Fleece Pullover Hoodie", "https://images.pexels.com/photos/1183266/pexels-photo-1183266.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("Essential 100% Organic Cotton Casual T-Shirt", "https://images.pexels.com/photos/996329/pexels-photo-996329.jpeg?auto=compress&cs=tinysrgb&w=800")
    ],
    "Home & Kitchen": [
        ("Stainless Steel Barista Espresso & Coffee Machine", "https://images.pexels.com/photos/324028/pexels-photo-324028.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("Digital Touchscreen Air Fryer & Convection Cooker", "https://images.pexels.com/photos/4397916/pexels-photo-4397916.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("Cordless Multi-Surface Stick Vacuum Cleaner", "https://images.pexels.com/photos/4108714/pexels-photo-4108714.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("Heavy-Duty Multi-Speed Stand Food & Dough Mixer", "https://images.pexels.com/photos/4397920/pexels-photo-4397920.jpeg?auto=compress&cs=tinysrgb&w=800"),
        ("Pre-Seasoned Heavy Duty Cast Iron Skillet (10-Inch)", "https://images.pexels.com/photos/3490257/pexels-photo-3490257.jpeg?auto=compress&cs=tinysrgb&w=800")
    ]
}

# Bank card templates for procedural products
BANK_OFFER_TEMPLATES = [
    {"bank": "HDFC Bank", "card": "Millennia / Regalia", "discount_pct": 10, "max_discount": 50.0, "label": "10% Instant Off on HDFC Bank Cards"},
    {"bank": "Chase", "card": "Sapphire / Freedom", "discount_pct": 15, "max_discount": 75.0, "label": "15% Savings with Chase Credit Cards"},
    {"bank": "ICICI Bank", "card": "Amazon Pay / Coral", "discount_pct": 7.5, "max_discount": 40.0, "label": "7.5% Off with ICICI Bank Cards"},
    {"bank": "Amex", "card": "American Express Platinum", "discount_pct": 12, "max_discount": 100.0, "label": "12% Instant Cashback with Amex"},
    {"bank": "Axis Bank", "card": "Axis Flipkart / Magnus", "discount_pct": 8, "max_discount": 45.0, "label": "8% Instant Discount on Axis Bank"},
    {"bank": "Citi", "card": "Citi Premier / Rewards", "discount_pct": 5, "max_discount": 25.0, "label": "5% Extra Savings on Citi Cards"},
    {"bank": "Capital One", "card": "Venture X / Savor", "discount_pct": 10, "max_discount": 50.0, "label": "10% Off with Capital One Cards"}
]

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
        item_copy = dict(item)
        item_copy.setdefault('stock_quantity', 25)
        item_copy.setdefault('colors', None)
        item_copy.setdefault('sizes', None)
        item_copy.setdefault('card_offer', None)
        catalog.append(item_copy)
        _CATALOG_MAP[item['id']] = item_copy
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

        # Realistic stock distribution: low stock for some items (critical: 2-4, warning: 5-9)
        if (h_val % 11 == 0):
            stock_qty = int(2 + (h_val % 3)) # 2, 3, 4 left (Critical alert)
        elif (h_val % 6 == 0):
            stock_qty = int(5 + (h_val % 5)) # 5, 6, 7, 8, 9 left (Limited stock)
        else:
            stock_qty = int(18 + (h_val % 70)) # normal stock

        # Varied realistic credit card offers with specific bank names for ~35% of products
        card_offer = None
        if (h_val % 3 == 0):
            template = BANK_OFFER_TEMPLATES[h_val % len(BANK_OFFER_TEMPLATES)]
            card_offer = dict(template)

        # No color pickers (colors dropped for all products)
        colors = None

        # Realistic Size Options for Clothing
        sizes = None
        if cat == "Clothing":
            if (h_val % 3 == 0):
                sizes = ["US 8", "US 9", "US 10", "US 11", "US 12"]
            elif (h_val % 3 == 1):
                sizes = ["30W", "32W", "34W", "36W", "38W"]
            else:
                sizes = ["S", "M", "L", "XL", "XXL"]

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
            "stock_quantity": stock_qty,
            "card_offer": card_offer,
            "colors": colors,
            "sizes": sizes,
            "min_price": round(price * 0.8, 2),
            "max_price": round(price * 1.2, 2),
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
