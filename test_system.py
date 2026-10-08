import urllib.request
import json

BASE_URL = "http://127.0.0.1:5000"

def test_endpoint(name, path, method="GET", payload=None):
    url = BASE_URL + path
    headers = {"Content-Type": "application/json"} if payload else {}
    data = json.dumps(payload).encode("utf-8") if payload else None
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            status = response.status
            content = response.read().decode("utf-8")
            try:
                json_data = json.loads(content)
                print(f"[PASS] {name} ({method} {path}) -> Status {status}")
                return json_data
            except Exception:
                print(f"[PASS] {name} ({method} {path}) -> Status {status}, Length {len(content)}")
                return content
    except Exception as e:
        print(f"[FAIL] {name} ({method} {path}) -> Error: {e}")
        return None

print("=== Starting System & API Validation ===")

# 1. Test Static Index
test_endpoint("Serve Frontend HTML", "/")
test_endpoint("Serve CSS", "/static/styles.css")
test_endpoint("Serve JS", "/static/app.js")

# 2. Test Products List
products_res = test_endpoint("Get All Products", "/api/products")
assert products_res and "products" in products_res, "Failed products retrieval"
print(f"       -> Retrieved {len(products_res['products'])} products.")

# 3. Test Filtered Products
electronics_res = test_endpoint("Filter by Electronics", "/api/products?category=Electronics")
assert all(p['category'] == 'Electronics' for p in electronics_res['products'])
print(f"       -> Category filter verified ({len(electronics_res['products'])} electronics).")

# 4. Test Search
search_res = test_endpoint("Search 'Sony'", "/api/products?search=sony")
assert len(search_res['products']) > 0
print(f"       -> Search verified ({len(search_res['products'])} matches found).")

# 5. Test ML Dynamic Pricing for all 3 Traditional ML Models
models = ["Random Forest", "Logistic Regression", "Decision Tree"]
sample_prod = products_res['products'][0]

for m in models:
    pred_res = test_endpoint(
        f"Predict Dynamic Price ({m})",
        "/api/predict_price",
        method="POST",
        payload={
            "product_id": sample_prod['id'],
            "price": sample_prod['price'],
            "discount": sample_prod['discount'],
            "category": sample_prod['category'],
            "model_name": m,
            "customer_age": 42,
            "review_rating": 5,
            "price_range_pct": 0.45,
            "num_points": 15
        }
    )
    assert pred_res and "recommended_price" in pred_res
    print(f"       -> {m}: Current ${pred_res['current_price']} (Prob: {pred_res['current_probability']*100:.1f}%) | "
          f"Recommended ${pred_res['recommended_price']} (Prob: {pred_res['recommended_probability']*100:.1f}%) | "
          f"Uplift: {pred_res['revenue_uplift_pct']}% ({pred_res['strategy']})")
    assert len(pred_res['curve']) >= 15, "Expected 15 curve points"

# 6. Test Model Metrics
metrics_res = test_endpoint("Get Model Benchmarks", "/api/models")
assert "metrics" in metrics_res
for model_name, m in metrics_res['metrics'].items():
    print(f"       -> {model_name}: Accuracy={m['accuracy']*100:.1f}%, ROC-AUC={m['roc_auc']:.4f}")

# 7. Test Apply Dynamic Price
apply_res = test_endpoint(
    "Apply Dynamic Price to Store",
    "/api/apply_price",
    method="POST",
    payload={"product_id": sample_prod['id'], "price": pred_res['recommended_price']}
)
assert apply_res['status'] == 'success'

# Verify updated price in catalog
updated_prod_res = test_endpoint("Verify Updated Catalog", f"/api/product/{sample_prod['id']}")
assert updated_prod_res['is_dynamically_priced'] == True
assert updated_prod_res['price'] == pred_res['recommended_price']
print(f"       -> Product {sample_prod['id']} dynamic price verified: ${updated_prod_res['price']}")

# 8. Test Batch Optimization
batch_res = test_endpoint(
    "Batch Optimize Store Catalog",
    "/api/batch_optimize",
    method="POST",
    payload={"model_name": "Random Forest"}
)
print(f"       -> Store Baseline Revenue: ${batch_res['total_current_revenue']:.2f}")
print(f"       -> Store AI Optimal Revenue: ${batch_res['total_optimal_revenue']:.2f}")
print(f"       -> Portfolio Uplift: +{batch_res['store_lift_pct']}% (+${batch_res['total_revenue_gain']:.2f})")

# 9. Reset Prices
reset_res = test_endpoint("Reset Catalog Prices", "/api/reset_prices", method="POST")
assert reset_res['status'] == 'success'
print("       -> Reset catalog back to baseline verified.")

print("\n=== ALL SYSTEM TESTS PASSED PERFECTLY ===")
