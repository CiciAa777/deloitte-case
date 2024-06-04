import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
fact_table = pd.read_csv('./fact_table.csv', encoding='ISO-8859-1')
item_dim = pd.read_csv('./item_dim.csv', encoding='ISO-8859-1')

# Merge fact_table with item_dim to link item details with transactional data
merged_data = pd.merge(fact_table, item_dim, on='item_key', how='left')

# Calculate total sales for each supplier
supplier_sales = merged_data.groupby('supplier')['total_price'].sum()
supplier_sales = supplier_sales.sort_values(ascending=False)

# Display top suppliers and their contribution to total sales
print("Top suppliers and their contribution to total sales:")
print(supplier_sales.head())

# Visualization of supplier sales distribution
plt.figure(figsize=(10, 6))
bar_plot = supplier_sales.head(10).plot(kind='bar', color='skyblue')
plt.title('Top 10 Suppliers by Sales')
plt.xlabel('Supplier')
plt.ylabel('Total Sales (in Millions of USD)')
plt.grid(True)

# Tilt x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()

# Calculate market share for the top suppliers
total_sales = supplier_sales.sum()
top_suppliers_market_share = supplier_sales.head(2) / total_sales * 100

print("Market share of top suppliers:")
print(top_suppliers_market_share)

# Count of different products per product description
product_counts = item_dim.groupby('desc')['item_key'].nunique()

# Visualization of product counts per description
plt.figure(figsize=(12, 8))
product_counts.plot(kind='bar', color='green')
plt.title('Number of Different Products per Product Description')
plt.xlabel('Product Description')
plt.ylabel('Number of Products')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.show()

# Strategic Recommendations
print("\nStrategic Recommendations:")
print("- Diversify suppliers to reduce dependency on a few key suppliers.")
print("- Consider establishing backup suppliers to enhance supply chain resilience.")
print("- Regularly review supplier performance to ensure they meet demand and quality standards.")
