import pandas as pd
import numpy as np
import hashlib
import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), 'ecommerce_dynamic_pricing_dataset.csv')

# Curated image pools per sub-category for accurate imagery
ELECTRONICS_ITEMS = [
    {"type": "Headphones", "keywords": ["Wireless", "Noise-Canceling", "Studio", "Over-Ear"], "brands": ["Sony", "Bose", "Sennheiser", "Audio-Technica", "Apple AirPods Max"], "images": [
        "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=800&auto=format&fit=crop&q=80"
    ]},
    {"type": "Smartwatch", "keywords": ["Fitness Tracker", "Cellular", "Titanium", "GPS Sport"], "brands": ["Apple Watch Series 9", "Samsung Galaxy Watch 6", "Garmin Fenix 7", "Fitbit Sense 2"], "images": [
        "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=800&auto=format&fit=crop&q=80"
    ]},
    {"type": "Laptop & Monitor", "keywords": ["Ultra-Thin", "4K Retina", "Gaming OLED", "Pro Creator"], "brands": ["MacBook Pro 16\"", "Dell XPS 15", "ASUS ROG Zephyrus", "LG UltraFine 27\""], "images": [
        "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&auto=format&fit=crop&q=80"
    ]},
    {"type": "Camera", "keywords": ["Mirrorless 4K", "Full Frame", "Cinema Lens", "Compact Vlog"], "brands": ["Sony Alpha 7 IV", "Canon EOS R6", "Fujifilm X-T5", "Nikon Z6 II"], "images": [
        "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1512790182412-b19e6d62bc39?w=800&auto=format&fit=crop&q=80"
    ]},
    {"type": "Speaker & Audio", "keywords": ["Spatial Audio", "Portable 360", "Hi-Fi DAC", "Smart Home Sound"], "brands": ["Bose SoundLink", "Sonos Move 2", "JBL Charge 5", "Marshall Stanmore III"], "images": [
        "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=800&auto=format&fit=crop&q=80"
    ]},
    {"type": "Accessories", "keywords": ["Ergonomic Wireless", "Mechanical Custom", "Fast Charging 100W", "Thunderbolt 4"], "brands": ["Logitech MX Master 3S", "Keychron Q1 Pro", "Anker Prime Hub", "Razer DeathAdder"], "images": [
        "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=800&auto=format&fit=crop&q=80"
    ]}
]

BOOKS_ITEMS = [
    {"type": "Tech & AI", "keywords": ["System Design", "Machine Learning", "Cloud Architecture", "Clean Code"], "titles": ["Designing Data-Intensive Applications", "Hands-On Machine Learning with Scikit-Learn", "Artificial Intelligence: A Modern Approach", "The Pragmatic Programmer: 20th Edition"], "images": [
        "https://images.unsplash.com/photo-1532012164546-f432f2e3edd4?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=800&auto=format&fit=crop&q=80"
    ]},
    {"type": "Self-Help & Habits", "keywords": ["Habit Mastery", "Mindset Shift", "Deep Concentration", "High Performance"], "titles": ["Atomic Habits: Proven Framework", "Deep Work: Rules for Focused Success", "Thinking, Fast and Slow", "The 7 Habits of Highly Effective People"], "images": [
        "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=800&auto=format&fit=crop&q=80"
    ]},
    {"type": "Business & Finance", "keywords": ["Wealth Creation", "Venture Capital", "Economic Strategy", "Market Mastery"], "titles": ["The Psychology of Money", "Zero to One: Notes on Startups", "Principles for Navigating Big Debt Crises", "Good to Great: Why Some Companies Leap"], "images": [
        "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1507842229451-79b1be886a27?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=800&auto=format&fit=crop&q=80"
    ]},
    {"type": "Literature & Science", "keywords": ["Cosmos & Physics", "Humanity History", "Epic Philosophy", "Classic Fiction"], "titles": ["Sapiens: A Brief History of Humankind", "Cosmos: Journey Through the Universe", "Klara and the Sun", "Meditations by Marcus Aurelius"], "images": [
        "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1476275466078-4007374efbbe?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1491841573634-28140fc7ced7?w=800&auto=format&fit=crop&q=80"
    ]}
]

CLOTHING_ITEMS = [
    {"type": "Jackets & Coats", "keywords": ["StormTech Waterproof", "Thermal Down", "Heritage Denim", "Tailored Wool"], "names": ["Water-Resistant Alpine Parka", "Heritage Raw Denim Trucker Jacket", "Tailored Wool Overcoat", "Fleece-Lined Windbreaker"], "images": [
        "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1548883354-7622d03aca27?w=800&auto=format&fit=crop&q=80"
    ]},
    {"type": "Sweaters & Tops", "keywords": ["100% Merino Wool", "Organic Cotton", "Breathable Linen", "Cashmere Blend"], "names": ["Merino Wool Crewneck Knit Sweater", "Classic Oxford Button-Down Shirt", "Luxury Cashmere V-Neck", "Relaxed Heavyweight Cotton Tee"], "images": [
        "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800&auto=format&fit=crop&q=80"
    ]},
    {"type": "Footwear & Shoes", "keywords": ["Calfskin Leather", "Cushioned Running", "Weatherproof Chelsea", "Suede Minimalist"], "names": ["Minimalist Italian Leather Sneakers", "Waterproof Chelsea Leather Boots", "Cloud-Cushioned Carbon Running Shoes", "Handmade Suede Loafers"], "images": [
        "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=800&auto=format&fit=crop&q=80"
    ]},
    {"type": "Pants & Denim", "keywords": ["Japanese Selvedge", "4-Way Stretch Chino", "Relaxed Linen Trouser", "Performance Athletic"], "names": ["Heritage 14oz Selvedge Denim Jeans", "Smart Stretch Commuter Chino", "Athletic Fleece Joggers", "Pleated Linen Summer Trousers"], "images": [
        "https://images.unsplash.com/photo-1542272604-780c96856592?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=800&auto=format&fit=crop&q=80"
    ]}
]

HOME_KITCHEN_ITEMS = [
    {"type": "Coffee & Espresso", "keywords": ["Barista Touch", "Conical Burr Grinder", "ThermoJet 3s", "Cold Brew System"], "names": ["Barista Touch Espresso Machine", "Precision Conical Burr Coffee Grinder", "Pour-Over Temperature Control Kettle", "Compact Pod Espresso Maker"], "images": [
        "https://images.unsplash.com/photo-1585515320310-259814833e62?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&auto=format&fit=crop&q=80"
    ]},
    {"type": "Cooking & Cookware", "keywords": ["DualZone 10Qt", "Enameled Cast Iron", "Damascus Steel", "Tri-Ply Stainless"], "names": ["DualZone 8-in-1 Air Fryer XL", "Enameled Cast Iron Dutch Oven (5.5 Qt)", "Japanese Damascus Steel Chef Knife 8\"", "Tri-Ply Clad Stainless Steel Cookware Set"], "images": [
        "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1584992236310-6edddc08acff?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1593618998160-e34014e67546?w=800&auto=format&fit=crop&q=80"
    ]},
    {"type": "Smart Home & Cleaning", "keywords": ["Laser Particle Detect", "H13 True HEPA", "Smart Sensor Wi-Fi", "Dual Cyclonic"], "names": ["Cordless Laser Detect Vacuum Cleaner", "Smart PureAir H13 True HEPA Air Purifier", "Smart ThermoControl Precision Sous Vide", "High-Velocity Professional Blender 1800W"], "images": [
        "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=800&auto=format&fit=crop&q=80"
    ]}
]

def generate_full_catalog():
    df = pd.read_csv(DATA_PATH)
    
    # Aggregate stats per unique Product_ID and Category
    grouped = df.groupby(['Product_ID', 'Product_Category']).agg({
        'Price': 'mean',
        'Discount': 'mean',
        'Review_Rating': 'mean',
        'Customer_Age': 'mean',
        'Transaction_ID': 'count'
    }).reset_index()
    
    catalog = []
    
    for idx, row in grouped.iterrows():
        pid = row['Product_ID']
        cat = row['Product_Category']
        price = round(float(row['Price']), 2)
        discount = round(float(row['Discount']), 2)
        rating = int(round(float(row['Review_Rating'])))
        review_score = round(3.8 + (float(row['Review_Rating']) * 0.22) + (hash(pid) % 10)*0.02, 1)
        review_score = min(5.0, max(4.0, review_score))
        reviews_count = 150 + int(hash(pid) % 4800)
        
        # Determine appealing badge
        disc_pct = discount / (price + 1e-5)
        h_val = int(hashlib.md5(pid.encode()).hexdigest(), 16)
        
        if disc_pct >= 0.25:
            badge = f"⚡ Flash Deal -{int(disc_pct*100)}%"
            badge_type = "deal"
        elif rating == 5 or review_score >= 4.9:
            badge = "⭐ 4.9 Top Rated"
            badge_type = "top"
        elif h_val % 7 == 0:
            badge = "🔥 Best Seller"
            badge_type = "bestseller"
        elif h_val % 7 == 1:
            badge = "🏆 Editor's Choice"
            badge_type = "editor"
        elif h_val % 7 == 2:
            badge = "🚀 Trending Now"
            badge_type = "trending"
        elif h_val % 7 == 3:
            badge = "✨ New Arrival"
            badge_type = "new"
        elif h_val % 7 == 4:
            badge = "💎 Premium Edition"
            badge_type = "premium"
        else:
            badge = "🎯 Staff Pick"
            badge_type = "staff"
            
        # Select category-accurate name & image
        if cat == 'Electronics':
            pool = ELECTRONICS_ITEMS[h_val % len(ELECTRONICS_ITEMS)]
            brand = pool['brands'][h_val % len(pool['brands'])]
            kw = pool['keywords'][(h_val // 2) % len(pool['keywords'])]
            name = f"{brand} ({kw} Edition)"
            image = pool['images'][h_val % len(pool['images'])]
            desc = f"Engineered with cutting-edge technology, superior performance, and high durability for everyday and professional use."
            features = ["High Performance Chipset", "Quick Charge USB-C", "Intelligent Power Management", "1-Year Warranty"]
            
        elif cat == 'Books':
            pool = BOOKS_ITEMS[h_val % len(BOOKS_ITEMS)]
            title = pool['titles'][h_val % len(pool['titles'])]
            kw = pool['keywords'][(h_val // 2) % len(pool['keywords'])]
            name = f"{title}: {kw} Edition"
            image = pool['images'][h_val % len(pool['images'])]
            desc = f"Comprehensive insights and transformative frameworks written by leading industry authorities."
            features = ["Hardcover / Collector's Edition", "Includes Reader's Companion Guide", "High-Quality Print Stock", "Worldwide Bestseller"]
            
        elif cat == 'Clothing':
            pool = CLOTHING_ITEMS[h_val % len(CLOTHING_ITEMS)]
            item_name = pool['names'][h_val % len(pool['names'])]
            kw = pool['keywords'][(h_val // 2) % len(pool['keywords'])]
            name = f"{item_name} [{kw}]"
            image = pool['images'][h_val % len(pool['images'])]
            desc = f"Crafted from premium sustainably-sourced textiles with tailored ergonomic fit and all-day comfort."
            features = ["Ultra-Soft Breathable Fabric", "Reinforced Double Stitching", "Machine Washable", "Designed in Italy"]
            
        else: # Home & Kitchen
            pool = HOME_KITCHEN_ITEMS[h_val % len(HOME_KITCHEN_ITEMS)]
            item_name = pool['names'][h_val % len(pool['names'])]
            kw = pool['keywords'][(h_val // 2) % len(pool['keywords'])]
            name = f"{item_name} ({kw})"
            image = pool['images'][h_val % len(pool['images'])]
            desc = f"Modern culinary and home essential engineered for effortless everyday convenience and gourmet results."
            features = ["Food-Grade BPA-Free Materials", "Intuitive Touch Controls", "Energy-Efficient Operation", "Dishwasher Safe Components"]
            
        catalog.append({
            "id": pid,
            "name": name,
            "category": cat,
            "price": price,
            "discount": discount,
            "rating": rating,
            "review_score": review_score,
            "reviews_count": reviews_count,
            "image": image,
            "description": desc,
            "badge": badge,
            "badge_type": badge_type,
            "in_stock": True,
            "features": features
        })
        
    return catalog

if __name__ == '__main__':
    cat = generate_full_catalog()
    print(f"Generated {len(cat)} total products across all dataset Product_IDs!")
    df_cat = pd.DataFrame(cat)
    print("\nCategory distribution:")
    print(df_cat['Product_Category' if 'Product_Category' in df_cat else 'category'].value_counts())
    print("\nBadges breakdown:")
    print(df_cat['badge_type'].value_counts())
    print("\nSample 5 products:")
    print(df_cat[['id', 'name', 'category', 'price', 'discount', 'badge']].head(5))
