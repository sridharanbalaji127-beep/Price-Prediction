import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ml_engine import DynamicPricingEngine
from products_catalog import get_all_products, get_product_by_id, get_category_counts

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Initialize and load ML engine
engine = DynamicPricingEngine()

# Admin-configurable price bounds (percentage of base price)
ADMIN_PRICE_LOWER_FACTOR = 0.5  # 50% of base price
ADMIN_PRICE_UPPER_FACTOR = 1.5  # 150% of base price

# Simple currency conversion rates (USD base)
CURRENCY_RATES = {
    'USD': 1.0,
    'EUR': 0.91,
    'GBP': 0.78,
    'INR': 82.5
}

try:
    if not engine.load_models():
        print("Training models on dataset...")
        engine.train_all_models()
    else:
        print("Loaded existing trained ML models.")
except Exception as e:
    print(f"Model initialization error: {e}")
    engine.train_all_models()

# In-memory dynamic prices state (allows live storefront price updates)
dynamic_price_overrides = {}


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


@app.route('/api/products', methods=['GET'])
def list_products():
    category = request.args.get('category')
    search = request.args.get('search', '').lower().strip()
    sort_by = request.args.get('sort', 'default')

    # Pagination
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 24))

    products = get_all_products()
    result = []

    for p in products:
        item = dict(p)

        # Ensure inventory and pricing guard fields exist
        item.setdefault('stock_quantity', None)
        item.setdefault('min_price', None)
        item.setdefault('max_price', None)

        # Derive review sentiment from review_score
        rs = item.get('review_score', 0)
        if rs >= 4.5:
            item['review_sentiment'] = 'positive'
        elif rs >= 3.5:
            item['review_sentiment'] = 'neutral'
        else:
            item['review_sentiment'] = 'negative'

        # Check for dynamic price override
        if item['id'] in dynamic_price_overrides:
            item['original_base_price'] = item['price']
            item['price'] = dynamic_price_overrides[item['id']]['price']
            item['is_dynamically_priced'] = True
            item['price_change_pct'] = round(
                ((item['price'] - item['original_base_price']) / (item['original_base_price'] + 1e-5)) * 100, 1
            )
        else:
            item['original_base_price'] = item['price']
            item['is_dynamically_priced'] = False
            item['price_change_pct'] = 0.0

        if category and category.lower() != 'all' and item['category'].lower() != category.lower():
            continue

        if search:
            if (search not in item['name'].lower() and
                    search not in item['description'].lower() and
                    search not in item['category'].lower() and
                    search not in item['id'].lower() and
                    search not in (item.get('badge') or '').lower()):
                continue

        result.append(item)

    # Sort
    if sort_by == 'price_asc':
        result.sort(key=lambda x: x['price'])
    elif sort_by == 'price_desc':
        result.sort(key=lambda x: x['price'], reverse=True)
    elif sort_by == 'rating' or sort_by == 'rating_desc':
        result.sort(key=lambda x: x['review_score'], reverse=True)
    elif sort_by == 'rating_asc':
        result.sort(key=lambda x: x['review_score'])
    elif sort_by == 'discount':
        result.sort(key=lambda x: x['discount'], reverse=True)

    total_matching = len(result)

    # Slice pagination if requested (or return all if limit is <= 0 or huge)
    if limit > 0:
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_products = result[start_idx:end_idx]
    else:
        paginated_products = result

    category_counts = get_category_counts()

    return jsonify({
        'products': paginated_products,
        'total': total_matching,
        'page': page,
        'limit': limit,
        'total_pages': (total_matching + limit - 1) // limit if limit > 0 else 1,
        'categories': ['All', 'Electronics', 'Books', 'Clothing', 'Home & Kitchen'],
        'category_counts': category_counts
    })


@app.route('/api/product/<product_id>', methods=['GET'])
def get_product(product_id):
    p = get_product_by_id(product_id)
    if not p:
        return jsonify({'error': 'Product not found'}), 404

    item = dict(p)
    if item['id'] in dynamic_price_overrides:
        item['original_base_price'] = item['price']
        item['price'] = dynamic_price_overrides[item['id']]['price']
        item['is_dynamically_priced'] = True
    else:
        item['original_base_price'] = item['price']
        item['is_dynamically_priced'] = False

    return jsonify(item)


@app.route('/api/predict_price', methods=['POST'])
def predict_price():
    data = request.get_json() or {}

    product_id = data.get('product_id')
    product = get_product_by_id(product_id) if product_id else None

    price = float(data.get('price', product['price'] if product else 100.0))
    discount = float(data.get('discount', product['discount'] if product else 10.0))
    category = data.get('category', product['category'] if product else 'Electronics')

    model_name = data.get('model_name', 'Random Forest')
    customer_age = int(data.get('customer_age', 35))
    customer_gender = data.get('customer_gender', 'Male')
    payment_method = data.get('payment_method', 'Credit Card')
    shipping_type = data.get('shipping_type', 'Express')
    review_rating = int(data.get('review_rating', product['rating'] if product else 4))
    price_range_pct = float(data.get('price_range_pct', 0.45))
    num_points = int(data.get('num_points', 15))

    base_item = {
        'price': price,
        'discount': discount,
        'category': category,
        'customer_age': customer_age,
        'customer_gender': customer_gender,
        'payment_method': payment_method,
        'shipping_type': shipping_type,
        'review_rating': review_rating
    }

    res = engine.optimize_price(
        base_item,
        model_name=model_name,
        price_range_pct=price_range_pct,
        num_points=num_points
    )

    res['product_id'] = product_id
    res['product_name'] = product['name'] if product else 'Custom Item'
    res['product_image'] = product['image'] if product else ''
    res['category'] = category
    res['simulation_profile'] = {
        'customer_age': customer_age,
        'customer_gender': customer_gender,
        'payment_method': payment_method,
        'shipping_type': shipping_type,
        'review_rating': review_rating
    }

    return jsonify(res)


@app.route('/api/apply_price', methods=['POST'])
def apply_price():
    data = request.get_json() or {}
    product_id = data.get('product_id')
    new_price = float(data.get('price', 0))

    if not product_id or new_price <= 0:
        return jsonify({'error': 'Invalid product ID or price'}), 400

    # Enforce admin price limits
    product = get_product_by_id(product_id)
    if product:
        min_allowed = product.get('min_price') or round(product['price'] * ADMIN_PRICE_LOWER_FACTOR, 2)
        max_allowed = product.get('max_price') or round(product['price'] * ADMIN_PRICE_UPPER_FACTOR, 2)
        if not (min_allowed <= new_price <= max_allowed):
            return jsonify({
                'error': f'Price out of allowed range [{min_allowed:.2f}, {max_allowed:.2f}] for product {product_id}'
            }), 400

    dynamic_price_overrides[product_id] = {
        'price': round(new_price, 2),
        'applied_at': data.get('timestamp', 'Just now')
    }

    return jsonify({
        'status': 'success',
        'product_id': product_id,
        'applied_price': round(new_price, 2),
        'message': f"Dynamic price ${new_price:.2f} successfully applied to live catalog!"
    })


@app.route('/api/reset_prices', methods=['POST'])
def reset_prices():
    dynamic_price_overrides.clear()
    return jsonify({'status': 'success', 'message': 'All store prices reset to catalog baseline.'})


@app.route('/api/models', methods=['GET'])
def get_models():
    return jsonify({
        'available_models': list(engine.models.keys()),
        'metrics': engine.model_metrics,
        'dataset_summary': engine.dataset_summary,
        'algorithms_info': {
            'Random Forest': {
                'type': 'Ensemble (Bagging of 120 Decision Trees)',
                'description': 'Captures non-linear price sensitivity & customer interaction features with high generalization.',
                'best_for': 'Complex multi-variable demand modeling'
            },
            'Logistic Regression': {
                'type': 'Linear Probabilistic Classifier',
                'description': 'Provides smooth, monotonic sigmoid probability output and clear price elasticity coefficient.',
                'best_for': 'Well-calibrated continuous probability estimation'
            },
            'Decision Tree': {
                'type': 'Hierarchical Partitioning Classifier',
                'description': 'Provides rule-based boundary splits on review ratings, age, and price brackets.',
                'best_for': 'Interpretable decision boundary visualization'
            }
        }
    })


@app.route('/api/batch_optimize', methods=['POST'])
def batch_optimize():
    data = request.get_json() or {}
    model_name = data.get('model_name', 'Random Forest')

    # Run batch on all products (or sample top 40 for instant snappy responsiveness)
    all_prods = get_all_products()
    sample_prods = all_prods[:40]

    results = []
    total_current_revenue = 0.0
    total_optimal_revenue = 0.0

    for p in sample_prods:
        base_item = {
            'price': p['price'],
            'discount': p['discount'],
            'category': p['category'],
            'customer_age': 35,
            'customer_gender': 'Male',
            'payment_method': 'Credit Card',
            'shipping_type': 'Express',
            'review_rating': p['rating']
        }
        res = engine.optimize_price(base_item, model_name=model_name, price_range_pct=0.4, num_points=11)

        total_current_revenue += res['current_expected_revenue']
        total_optimal_revenue += res['recommended_expected_revenue']

        results.append({
            'id': p['id'],
            'name': p['name'],
            'category': p['category'],
            'current_price': res['current_price'],
            'recommended_price': res['recommended_price'],
            'current_prob': res['current_probability'],
            'recommended_prob': res['recommended_probability'],
            'current_rev': res['current_expected_revenue'],
            'optimal_rev': res['recommended_expected_revenue'],
            'lift_pct': res['revenue_uplift_pct'],
            'strategy': res['strategy']
        })

    store_lift_pct = round(((total_optimal_revenue - total_current_revenue) / (total_current_revenue + 1e-5)) * 100, 1)

    return jsonify({
        'model_used': model_name,
        'products_count': len(sample_prods),
        'total_current_revenue': round(total_current_revenue, 2),
        'total_optimal_revenue': round(total_optimal_revenue, 2),
        'total_revenue_gain': round(total_optimal_revenue - total_current_revenue, 2),
        'store_lift_pct': store_lift_pct,
        'optimizations': results
    })


@app.route('/api/convert_price', methods=['GET'])
def convert_price():
    amount = float(request.args.get('amount', 0))
    target = request.args.get('currency', 'USD').upper()
    rate = CURRENCY_RATES.get(target)
    if rate is None:
        return jsonify({'error': f'Unsupported currency: {target}. Supported: {list(CURRENCY_RATES.keys())}'}), 400
    converted = round(amount * rate, 2)
    return jsonify({'original_amount': amount, 'converted_amount': converted, 'currency': target})


@app.route('/api/update_inventory', methods=['POST'])
def update_inventory():
    data = request.get_json() or {}
    product_id = data.get('product_id')
    delta = int(data.get('delta', 0))
    if not product_id:
        return jsonify({'error': 'Missing product_id'}), 400
    prod = get_product_by_id(product_id)
    if not prod:
        return jsonify({'error': 'Product not found'}), 404
    current_qty = prod.get('stock_quantity', 0) or 0
    new_qty = max(0, current_qty + delta)
    prod['stock_quantity'] = new_qty
    prod['in_stock'] = new_qty > 0
    return jsonify({'product_id': product_id, 'new_stock_quantity': new_qty, 'in_stock': prod['in_stock']})


if __name__ == '__main__':
    print("Starting AI Dynamic Pricing E-Commerce Server on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
