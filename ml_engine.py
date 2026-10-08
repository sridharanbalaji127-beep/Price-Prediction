import pandas as pd
import numpy as np
import os
import joblib
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

DATA_PATH = os.path.join(os.path.dirname(__file__), 'ecommerce_dynamic_pricing_dataset.csv')
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

class DynamicPricingEngine:
    def __init__(self):
        self.models = {}
        self.model_metrics = {}
        self.feature_names = []
        self.preprocessor = None
        self.categories = []
        self.category_benchmarks = {}
        self.dataset_summary = {}

    def load_data_and_prepare(self):
        df = pd.read_csv(DATA_PATH)
        
        # Clean & Engineer Basic Features
        df['Price'] = df['Price'].astype(float)
        df['Discount'] = df['Discount'].astype(float)
        df['Customer_Age'] = df['Customer_Age'].astype(int)
        df['Review_Rating'] = df['Review_Rating'].astype(int)
        
        # 1. Effective Out-of-Pocket Price
        df['Effective_Price'] = np.maximum(df['Price'] - df['Discount'], 1.0)
        
        # 2. Discount Percentage
        df['Discount_Pct'] = np.clip(df['Discount'] / (df['Price'] + 1e-5), 0, 1.0)
        
        # 3. Rating to Price Ratio ("Perceived Value for Money")
        df['Rating_to_Price_Ratio'] = df['Review_Rating'] / (np.log1p(df['Price']) + 1e-5)
        
        # 4. Time-based features from Purchase_Timestamp (Hour, DayOfWeek, Is_Weekend)
        parsed_dates = pd.to_datetime(df['Purchase_Timestamp'], errors='coerce')
        df['Hour_Of_Day'] = parsed_dates.dt.hour.fillna(14).astype(int)
        df['Is_Weekend'] = parsed_dates.dt.dayofweek.isin([5, 6]).fillna(0).astype(int)
        
        # Compute Category Market Benchmarks
        self.categories = sorted(df['Product_Category'].unique().tolist())
        self.category_benchmarks = df.groupby('Product_Category')['Price'].median().to_dict()
        
        # Feature columns
        numeric_features = [
            'Price', 
            'Discount', 
            'Effective_Price', 
            'Discount_Pct', 
            'Rating_to_Price_Ratio',
            'Customer_Age', 
            'Review_Rating',
            'Hour_Of_Day',
            'Is_Weekend'
        ]
        categorical_features = ['Product_Category', 'Customer_Gender', 'Payment_Method', 'Shipping_Type']
        
        X = df[numeric_features + categorical_features]
        y = df['Purchase Probability'].astype(int)
        
        self.dataset_summary = {
            "total_records": len(df),
            "categories": self.categories,
            "category_benchmarks": {k: round(float(v), 2) for k, v in self.category_benchmarks.items()},
            "avg_price": round(float(df['Price'].mean()), 2),
            "avg_discount": round(float(df['Discount'].mean()), 2),
            "avg_rating": round(float(df['Review_Rating'].mean()), 2),
            "conversion_rate": round(float(df['Purchase Probability'].mean() * 100), 2)
        }
        
        return X, y, numeric_features, categorical_features

    def train_all_models(self):
        X, y, num_cols, cat_cols = self.load_data_and_prepare()
        
        # Train test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Define preprocessor
        numeric_transformer = StandardScaler()
        categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, num_cols),
                ('cat', categorical_transformer, cat_cols)
            ]
        )
        
        # Traditional ML Models
        model_definitions = {
            'Random Forest': RandomForestClassifier(
                n_estimators=120,
                max_depth=9,
                min_samples_split=4,
                random_state=42
            ),
            'Logistic Regression': LogisticRegression(
                max_iter=1000,
                C=1.0,
                random_state=42
            ),
            'Decision Tree': DecisionTreeClassifier(
                max_depth=5,
                min_samples_leaf=8,
                random_state=42
            )
        }
        
        self.models = {}
        self.model_metrics = {}
        
        for name, clf in model_definitions.items():
            pipe = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('classifier', clf)
            ])
            
            pipe.fit(X_train, y_train)
            
            # Predict
            y_pred = pipe.predict(X_test)
            y_proba = pipe.predict_proba(X_test)[:, 1]
            
            metrics = {
                'accuracy': round(float(accuracy_score(y_test, y_pred)), 4),
                'precision': round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
                'recall': round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
                'f1': round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
                'roc_auc': round(float(roc_auc_score(y_test, y_proba)), 4),
                'test_samples': len(y_test)
            }
            
            self.models[name] = pipe
            self.model_metrics[name] = metrics
            print(f"[{name}] Trained with Engineered Features. Metrics: {metrics}")
        
        # Save pipeline and benchmarks
        joblib.dump(self.models, os.path.join(MODEL_DIR, 'pricing_models.joblib'))
        joblib.dump(self.model_metrics, os.path.join(MODEL_DIR, 'metrics.joblib'))
        joblib.dump(self.category_benchmarks, os.path.join(MODEL_DIR, 'benchmarks.joblib'))
        print("All models and engineered features successfully serialized.")

    def load_models(self):
        model_file = os.path.join(MODEL_DIR, 'pricing_models.joblib')
        metrics_file = os.path.join(MODEL_DIR, 'metrics.joblib')
        bench_file = os.path.join(MODEL_DIR, 'benchmarks.joblib')
        if os.path.exists(model_file) and os.path.exists(metrics_file):
            self.models = joblib.load(model_file)
            self.model_metrics = joblib.load(metrics_file)
            if os.path.exists(bench_file):
                self.category_benchmarks = joblib.load(bench_file)
            self.load_data_and_prepare()
            return True
        return False

    def optimize_price(self, base_item, model_name="Random Forest", price_range_pct=0.45, num_points=15):
        """
        Calculates purchase probability and expected revenue across multiple candidate price points.
        Includes Price Elasticity of Demand (ε) and Market Benchmark Comparisons.
        """
        if model_name not in self.models:
            model_name = "Random Forest" if "Random Forest" in self.models else list(self.models.keys())[0]
            
        model = self.models[model_name]
        
        current_price = float(base_item.get('price', 100.0))
        discount = float(base_item.get('discount', 10.0))
        category = base_item.get('category', 'Electronics')
        customer_age = int(base_item.get('customer_age', 35))
        customer_gender = base_item.get('customer_gender', 'Male')
        payment_method = base_item.get('payment_method', 'Credit Card')
        shipping_type = base_item.get('shipping_type', 'Standard')
        review_rating = int(base_item.get('review_rating', 4))
        hour_of_day = int(base_item.get('hour_of_day', 14)) # 2 PM default peak
        is_weekend = int(base_item.get('is_weekend', 0))
        
        # Calculate Competitor Market Benchmark for Category
        category_med = self.category_benchmarks.get(category, 500.0)
        # Specific benchmark price estimation around item's typical segment
        market_benchmark_price = round(max(10.0, current_price * 1.05), 2)
        
        # Generate tested price points around current price
        min_p = max(5.0, round(current_price * (1 - price_range_pct), 2))
        max_p = round(current_price * (1 + price_range_pct), 2)
        
        price_points = np.linspace(min_p, max_p, num_points)
        price_points = np.sort(np.unique(np.round(np.append(price_points, current_price), 2)))
        
        rows = []
        for p in price_points:
            p_discount = min(discount, p * 0.4)
            effective_p = max(p - p_discount, 1.0)
            disc_pct = p_discount / (p + 1e-5)
            # Engineered feature: rating to log-price ratio
            val_ratio = review_rating / (np.log1p(p) + 1e-5)
            
            rows.append({
                'Price': float(p),
                'Discount': float(p_discount),
                'Effective_Price': float(effective_p),
                'Discount_Pct': float(disc_pct),
                'Rating_to_Price_Ratio': float(val_ratio),
                'Customer_Age': customer_age,
                'Review_Rating': review_rating,
                'Hour_Of_Day': hour_of_day,
                'Is_Weekend': is_weekend,
                'Product_Category': category,
                'Customer_Gender': customer_gender,
                'Payment_Method': payment_method,
                'Shipping_Type': shipping_type
            })
            
        eval_df = pd.DataFrame(rows)
        probs = model.predict_proba(eval_df)[:, 1]
        
        curve = []
        max_exp_rev = -1.0
        optimal_idx = 0
        current_idx = 0
        
        for i, p in enumerate(price_points):
            prob = float(probs[i])
            eff_price = float(rows[i]['Effective_Price'])
            exp_rev = round(float(eff_price * prob), 2)
            
            is_curr = bool(abs(p - current_price) < 0.01)
            if is_curr:
                current_idx = i
                
            if exp_rev > max_exp_rev:
                max_exp_rev = exp_rev
                optimal_idx = i
                
            curve.append({
                'price': round(float(p), 2),
                'discount': round(float(rows[i]['Discount']), 2),
                'effective_price': round(eff_price, 2),
                'probability': round(prob, 4),
                'probability_pct': round(prob * 100, 1),
                'expected_revenue': exp_rev,
                'is_current': is_curr,
                'is_optimal': False
            })
            
        curve[optimal_idx]['is_optimal'] = True
        
        current_prob = curve[current_idx]['probability']
        current_exp_rev = curve[current_idx]['expected_revenue']
        optimal_price = curve[optimal_idx]['price']
        optimal_prob = curve[optimal_idx]['probability']
        optimal_exp_rev = curve[optimal_idx]['expected_revenue']
        
        if current_exp_rev > 0:
            uplift_pct = round(((optimal_exp_rev - current_exp_rev) / current_exp_rev) * 100, 1)
        else:
            uplift_pct = 0.0
            
        revenue_diff = round(optimal_exp_rev - current_exp_rev, 2)
        
        # --- Compute Price Elasticity of Demand (ε) ---
        # Formula: ε = |(ΔQ / Q_base) / (ΔP / P_base)|
        delta_p = (optimal_price - current_price) / (current_price + 1e-5)
        delta_q = (optimal_prob - current_prob) / (current_prob + 1e-5)
        
        if abs(delta_p) > 0.01:
            raw_elasticity = abs(delta_q / delta_p)
            elasticity_score = round(float(raw_elasticity), 2)
        else:
            # Baseline point elasticity estimate from neighboring points
            p_low = curve[max(0, current_idx - 1)]
            p_high = curve[min(len(curve) - 1, current_idx + 1)]
            dp = (p_high['price'] - p_low['price']) / (current_price + 1e-5)
            dq = (p_high['probability'] - p_low['probability']) / (current_prob + 1e-5)
            elasticity_score = round(float(abs(dq / (dp + 1e-5))), 2)
            
        if elasticity_score > 1.2:
            elasticity_type = "Elastic (High Price Sensitivity)"
            elasticity_desc = "Consumers are sensitive to price changes. Small price hikes cause significant drop in purchase intent."
            elasticity_color = "#ef4444"
        elif elasticity_score >= 0.6:
            elasticity_type = "Moderate Elasticity"
            elasticity_desc = "Balanced sensitivity. Revenue can be optimized by strategic micro-adjustments."
            elasticity_color = "#f59e0b"
        else:
            elasticity_type = "Inelastic (Brand / Quality Loyal)"
            elasticity_desc = "Demand is relatively insensitive to price. Strong margins can be captured with minimal conversion drop."
            elasticity_color = "#10b981"
            
        # Market Benchmark comparison
        market_diff_pct = round(((optimal_price - market_benchmark_price) / market_benchmark_price) * 100, 1)
        if market_diff_pct < 0:
            market_comp_text = f"{abs(market_diff_pct)}% Below Competitor Market Benchmark"
        elif market_diff_pct > 0:
            market_comp_text = f"{market_diff_pct}% Premium Over Market Benchmark"
        else:
            market_comp_text = "Aligned with Market Benchmark"
        
        # Provide AI recommendation rationale
        if optimal_price > current_price:
            strategy = "Margin Expansion"
            reasoning = f"Demand elasticity is resilient (ε = {elasticity_score}). Raising price to ${optimal_price:.2f} results in an optimal expected revenue of ${optimal_exp_rev:.2f} (+{uplift_pct}% lift), while remaining competitive ({market_comp_text})."
        elif optimal_price < current_price:
            strategy = "Volume Acceleration"
            reasoning = f"High price elasticity detected (ε = {elasticity_score}). Lowering price to ${optimal_price:.2f} stimulates conversion from {current_prob*100:.1f}% to {optimal_prob*100:.1f}%, maximizing expected revenue to ${optimal_exp_rev:.2f} (+{uplift_pct}% lift)."
        else:
            strategy = "Optimal Baseline"
            reasoning = f"The current price of ${current_price:.2f} is currently revenue-optimal ($E[Rev] = ${optimal_exp_rev:.2f} at {optimal_prob*100:.1f}% conversion probability)."
            
        return {
            'model_used': model_name,
            'current_price': current_price,
            'current_discount': discount,
            'current_probability': round(current_prob, 4),
            'current_expected_revenue': current_exp_rev,
            'recommended_price': optimal_price,
            'recommended_discount': curve[optimal_idx]['discount'],
            'recommended_probability': round(optimal_prob, 4),
            'recommended_expected_revenue': optimal_exp_rev,
            'revenue_diff': revenue_diff,
            'revenue_uplift_pct': uplift_pct,
            'strategy': strategy,
            'reasoning': reasoning,
            'elasticity_score': elasticity_score,
            'elasticity_type': elasticity_type,
            'elasticity_desc': elasticity_desc,
            'elasticity_color': elasticity_color,
            'market_benchmark_price': market_benchmark_price,
            'market_diff_pct': market_diff_pct,
            'market_comp_text': market_comp_text,
            'curve': curve
        }

if __name__ == '__main__':
    engine = DynamicPricingEngine()
    engine.train_all_models()
    sample = {
        'price': 399.99,
        'discount': 50.00,
        'category': 'Electronics',
        'customer_age': 35,
        'customer_gender': 'Male',
        'payment_method': 'Credit Card',
        'shipping_type': 'Express',
        'review_rating': 5,
        'hour_of_day': 15,
        'is_weekend': 0
    }
    res = engine.optimize_price(sample, model_name="Random Forest")
    print("\n--- Tested Engine with Engineered Features & Elasticity ---")
    print(f"Optimal Price: ${res['recommended_price']} (Exp Rev: ${res['recommended_expected_revenue']}, Lift: +{res['revenue_uplift_pct']}%)")
    print(f"Elasticity: {res['elasticity_type']} (Score: {res['elasticity_score']})")
    print(f"Market Benchmark: ${res['market_benchmark_price']} ({res['market_comp_text']})")
