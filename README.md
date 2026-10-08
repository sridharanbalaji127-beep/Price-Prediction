# 🛒 ApexMart AI - Dynamic Pricing Recommendation System

> **6-Hour ML Hackathon Project**: Real-time E-Commerce Dynamic Pricing Engine powered exclusively by **Traditional Machine Learning**.

---

## 🌟 Overview & Architecture

**ApexMart AI** is a modern e-commerce platform integrated with an **AI Dynamic Pricing Intelligence System**. Rather than relying on static or arbitrary discounts, ApexMart utilizes trained traditional classification models to estimate customer purchase probability $\hat{P}(\text{Purchase} \mid P, X)$ across continuous price spectrums and dynamically identify the price $P^*$ that **maximizes expected revenue**.

```
[ Customer Features (Age, Rating, Gender, Payment, Shipping) ]
                               +
                    [ Candidate Price: P ]
                               │
                               ▼
        ┌─────────────────────────────────────────────┐
        │        Traditional ML Pipeline              │
        │  • Random Forest (120 Trees)                │
        │  • Logistic Regression (Calibrated Logits)  │
        │  • Decision Tree (Interpretable Rules)      │
        └──────────────────────┬──────────────────────┘
                               │
                               ▼
              Purchase Probability: P̂(Buy | P, X)
                               │
                               ▼
        Expected Revenue: E[Rev](P) = (P - Discount) × P̂
                               │
                               ▼
          Optimal Recommendation: P* = argmax E[Rev](P)
```
🔗 **Live Demo:** [ApexMart AI Demo](http://127.0.0.1:5000)
---

## 🎯 Key Features

### 1. 🛍️ Modern E-Commerce Storefront
- Clean, crisp white & light-slate aesthetic with modern indigo/blue accents.
- Responsive product catalog grid across **Electronics**, **Books**, **Clothing**, and **Home & Kitchen**.
- Instant search, category filtering, and multi-parameter price sorting.
- Interactive Shopping Cart drawer with real-time dynamic savings calculation.

### 2. ⚡ AI Dynamic Pricing Intelligence Modal
- **Revenue Maximizer Recommendation Card**: Compares current catalog price vs AI-recommended price, showing conversion probability shift and expected revenue lift ($\Delta R$).
- **Interactive Dual-Curve Visualizations** (powered by Chart.js):
  - **Revenue Curve**: Price ($) vs Expected Revenue ($), with the optimal peak price marked.
  - **Demand Elasticity Curve**: Price ($) vs Purchase Probability (%).
- **Tested Price Variations Table**: Full breakdown of 15 candidate price points, effective prices, conversion rates, and revenue projections.
- **Demographic Simulation Sandbox**: Real-time sliders for Customer Age, Product Review Rating, Payment Method, and Shipping Speed to see elasticity shifts live.
- **"Apply AI Price to Store"**: Immediately updates the storefront catalog in real-time.

### 3. 🤖 100% Traditional Machine Learning (No DL/LLMs)
- **Random Forest Classifier**: Non-linear multi-variable interactions (Accuracy: **96.8%**, ROC-AUC: **0.9956**).
- **Logistic Regression**: Standardized linear logit boundary with sigmoid calibrated elasticity (Accuracy: **99.3%**, ROC-AUC: **0.9997**).
- **Decision Tree Classifier**: Rule-based partition tree (Accuracy: **96.6%**, ROC-AUC: **0.9789**).

### 4. 📊 Store-Wide Batch Optimizer
- Simulates dynamic pricing across all catalog products simultaneously, reporting portfolio-level revenue gains (+27.6% portfolio uplift).

---

## 🚀 Quick Start Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Dependencies: `scikit-learn`, `pandas`, `numpy`, `flask`, `flask-cors`, `joblib`)*

### 2. Train the ML Models
```bash
python ml_engine.py
```

### 3. Start the Web Application
```bash
python app.py
```

Open your browser at: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 📁 Project Structure

```
├── app.py                                   # Flask backend API & static server
├── ml_engine.py                             # Traditional ML training pipeline & pricing optimizer
├── products_catalog.py                      # Multi-category product catalog
├── test_system.py                           # Automated end-to-end integration test suite
├── ecommerce_dynamic_pricing_dataset.csv     # 2,044 transaction training dataset
├── requirements.txt                         # Project dependencies
├── models/                                  # Serialized ML models (.joblib)
│   ├── pricing_models.joblib
│   └── metrics.joblib
└── static/                                  # Modern Frontend UI
    ├── index.html                           # Semantic responsive HTML5 structure
    ├── styles.css                           # Modern Vanilla CSS design system
    └── app.js                               # Interactive Chart.js & dynamic pricing client
```

---

## 📐 Mathematical Formulation

For any product with attributes $X$ and candidate price $P$:
1. **Purchase Probability**: $\hat{P}(\text{Buy} \mid P, X) = \text{Model.predict\_proba}([P, \text{Discount}, X])_1$
2. **Expected Revenue**: $E[\text{Revenue}](P) = (P - \text{Discount}) \times \hat{P}(\text{Buy} \mid P, X)$
3. **Optimal Price**: $P^* = \arg\max_{P \in [P_{\min}, P_{\max}]} E[\text{Revenue}](P)$
4. **Revenue Lift**: $\text{Uplift} = \frac{E[\text{Revenue}](P^*) - E[\text{Revenue}](P_{\text{current}})}{E[\text{Revenue}](P_{\text{current}})} \times 100\%$
