import urllib.request
import json

req = urllib.request.urlopen('http://127.0.0.1:5000/api/products?limit=24')
data = json.loads(req.read().decode('utf-8'))

print(f"Total matching products: {data['total']}")
print(f"Category counts: {data['category_counts']}")
print("\n--- First 16 Products on Default Landing Page ---")

for i, p in enumerate(data['products'][:16], 1):
    badge = p.get('badge') or '[Clean / No Badge]'
    print(f"{i:2d}. [{p['category']:<14}] {p['name']:<55} | ${p['price']:>6.2f} | {p['review_score']}★ ({p['reviews_count']:>4} reviews) | {badge}")
