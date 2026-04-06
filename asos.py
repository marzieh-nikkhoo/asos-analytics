import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv('/Users/marzieh/Desktop/project/asos analytics/products_asos.csv', on_bad_lines='skip')

df['price']=pd.to_numeric(df['price'],errors='coerce')
df=df.dropna(subset=['price'])

print(f"Data Loaded:{len(df)} rows")
print(df.head())

df['description']=df['description'].fillna('').astype(str)

def get_brand(text):
    if 'by' in text:
        try:
          return text.split('by')[1].strip().split(' ')[0]
        except:
           return "Unknown"
    else:
        return "Unknown"
    
df['brand_raw']=df['description'].apply(get_brand) 

brand_map = {
'New': 'New Look',
'River': 'River Island',
'Miss':'Miss Selfridge',
'TopshopWelcome':'Topshop'
}

df ['Brand'] = df[ 'brand_raw']. map(brand_map). fillna(df ['brand_raw'])

brand_counts = df['Brand'].value_counts()
valid_brands = brand_counts[brand_counts > 5].index

df_clean = df[df['Brand'].isin(valid_brands)].copy()

print(df_clean['Brand'].value_counts().head(5))

# 1.Function to analyze stockouts
def calculate_phantom_revenue(size_str):
    if not isinstance(size_str, str):
        return 0, 0.0
    # Split "UK 6, UK 8 - Out of stock" into list
    sizes = size_str.split(',')
    total_sizes = len(sizes)
    # Count how many items are out of stock
    out_of_stock_count = size_str.count('Out of stock')
    # Calculate Rate (0.0 to 1.0)
    rate = out_of_stock_count / total_sizes if total_sizes > 0 else 0.0
    return out_of_stock_count, rate
# Chart 1
top_brands = df_clean['Brand'].value_counts().head(10).index
df_top = df_clean[df_clean['Brand'].isin(top_brands)]

plt.figure(figsize=(10,6))
sns.countplot(data=df_top, y='Brand', order=top_brands)
plt.title('Top 10 Brands by Number of Products')
plt.xlabel('Count')
plt.ylabel('Brand')
plt.tight_layout()
plt.show()

# Chart 2 - only top 10 brands
top_brands = df_clean['Brand'].value_counts().head(10).index
df_top = df_clean[df_clean['Brand'].isin(top_brands)]

plt.figure(figsize=(12,6))
sns.boxplot(data=df_top, x='Brand', y='price')
plt.xticks(rotation=90)
plt.title('Price Distribution by Top 10 Brands')
plt.xlabel('Brand')
plt.ylabel('Price')
plt.tight_layout()
plt.show()

avg_price = df_clean.groupby('Brand')['price'].mean().sort_values(ascending=False)

print("\nAverage Price by Brand:")
print(avg_price.head(10))

top_brands = avg_price.head(10).index
df_top_avg = df_clean[df_clean['Brand'].isin(top_brands)]

plt.figure(figsize=(10,6))
sns.barplot(data=df_top_avg, x='Brand', y='price', estimator='mean')
plt.xticks(rotation=45)
plt.title('Average Price of Top Brands')
plt.xlabel('Brand')
plt.ylabel('Average Price')
plt.tight_layout()
plt.show()

print("\n--- Simple Insights ---")

most_products = df_clean['Brand'].value_counts().idxmax()
print(f"Brand with most products: {most_products}")

most_expensive = avg_price.idxmax()
print(f"Most expensive brand (on average): {most_expensive}")





















