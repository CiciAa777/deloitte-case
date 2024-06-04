import pandas as pd
import numpy as np

# Load the datasets
fact_table = pd.read_csv('./fact_table.csv')
item_dim = pd.read_csv('./item_dim.csv', encoding='ISO-8859-1')

# Merge fact_table with item_dim to link item details with transactional data
merged_data = pd.merge(fact_table, item_dim, on='item_key', how='left')

# Calculate total cost and total quantity for each item_key and supplier
supplier_costs = merged_data.groupby(['desc', 'supplier']).agg(
    total_cost=pd.NamedAgg(column='total_price', aggfunc='sum'),
    total_quantity=pd.NamedAgg(column='quantity', aggfunc='sum')
)
supplier_costs['avg_cost_per_unit'] = supplier_costs['total_cost'] / supplier_costs['total_quantity']

# Function to select optimal suppliers based on a higher quantile for cost per unit for each product type
def select_optimal_suppliers(data, quantile=1):
    optimal_suppliers = pd.DataFrame()
    for desc, group in data.groupby('desc'):
        threshold = group['avg_cost_per_unit'].quantile(quantile)
        selected_suppliers = group[group['avg_cost_per_unit'] <= threshold]
        optimal_suppliers = pd.concat([optimal_suppliers, selected_suppliers], ignore_index=True)
    return optimal_suppliers

# Select optimal suppliers and further reduce to minimal set
optimal_suppliers = select_optimal_suppliers(supplier_costs.reset_index())
unique_desc = optimal_suppliers['desc'].unique()
selected_suppliers = pd.DataFrame()

while len(unique_desc) > 0:
    coverage = optimal_suppliers[optimal_suppliers['desc'].isin(unique_desc)]
    coverage = coverage.groupby('supplier').agg({'desc': 'nunique'}).reset_index()
    coverage = coverage.sort_values('desc', ascending=False)
    best_supplier = coverage.iloc[0]
    selected_suppliers = pd.concat([selected_suppliers, optimal_suppliers[optimal_suppliers['supplier'] == best_supplier['supplier']]])
    covered_descs = optimal_suppliers[optimal_suppliers['supplier'] == best_supplier['supplier']]['desc'].unique()
    unique_desc = np.setdiff1d(unique_desc, covered_descs)

# Print selected suppliers
print("Selected suppliers after optimization:")
for supplier in selected_suppliers['supplier'].unique():
    print("   ", supplier)


# Calculate total cost with current suppliers
total_current_cost = supplier_costs['total_cost'].sum()

# Calculate total cost with optimal suppliers
optimal_total_cost = selected_suppliers['total_cost'].sum()

# Calculate savings
savings = total_current_cost - optimal_total_cost

print(f"Reduced number of suppliers to {selected_suppliers['supplier'].nunique()}.")
print(f"By optimizing our supplier list, we were able to reduce our total procurement cost from ${total_current_cost:.2f} to ${optimal_total_cost:.2f}.")
print(f"This strategic supplier consolidation resulted in savings of ${savings:.2f}.")
