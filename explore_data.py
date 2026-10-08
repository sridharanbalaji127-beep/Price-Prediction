import pandas as pd
import json

df = pd.read_csv('ecommerce_dynamic_pricing_dataset.csv')
print("Dataset Shape:", df.shape)
print("\nColumns and Dtypes:")
print(df.dtypes)
print("\nMissing values:")
print(df.isnull().sum())
print("\nSummary Statistics:")
print(df.describe())

print("\nCategories distribution:")
print(df['Product_Category'].value_counts())

print("\nPurchase Probability (Target) distribution:")
print(df['Purchase Probability'].value_counts(normalize=True))

print("\nAverage Price & Discount by Category:")
print(df.groupby('Product_Category')[['Price', 'Discount', 'Review_Rating', 'Purchase Probability']].mean())

# Sample unique products per category
sample_products = df.groupby('Product_Category').head(5)
print("\nSample Rows:")
print(sample_products[['Product_ID', 'Product_Category', 'Price', 'Discount', 'Review_Rating', 'Purchase Probability']])
