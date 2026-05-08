import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load the data, some rows are broken so skip them
df = pd.read_csv('products_asos.csv', on_bad_lines='skip')

# price column has some weird values, force them to numbers and drop the ones that didnt work
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df = df.dropna(subset=['price'])

print(f"loaded {len(df)} rows")
print(df.head())

# some descriptions are missing, just fill with empty string so we dont get errors later
df['description'] = df['description'].fillna('').astype(str)

# most descriptions look like "Floral dress by River Island"
# so i split on "by" and grab the next word as the brand
def get_brand(text):
    if 'by' not in text:
        return 'Unknown'
    try:
        return text.split('by')[1].strip().split()[0]
    except:
        return 'Unknown'

df['brand_raw'] = df['description'].apply(get_brand)

# the extracted word is sometimes just the first word of the brand name
# or a messy version, so i map them manually to clean names
brand_map = {
    'New': 'New Look',
    'River': 'River Island',
    'Miss': 'Miss Selfridge',
    'TopshopWelcome': 'Topshop',
    'True': 'True Religion',
    'Polo': 'Polo Ralph Lauren',
    'Whistles': 'Whistles',
    'WhistlesAll': 'Whistles',
    'WhistlesDaywear': 'Whistles',
    'MayaAll': 'Maya',
    'StarletExclusive': 'Starlet',
    'sister': 'Sister Jane',
    'Armani': 'Armani',
    'Barbour': 'Barbour',
}

df['Brand'] = df['brand_raw'].map(brand_map).fillna(df['brand_raw'])

# drop brands with very few products, probably extraction errors
counts = df['Brand'].value_counts()
df = df[df['Brand'].isin(counts[counts > 5].index)].copy()

print(df['Brand'].value_counts().head(5))

# i wanted to see which sizes are out of stock
# the size column looks like: "UK 6, UK 8 - Out of stock, UK 10"
def stockout_rate(size_str):
    if not isinstance(size_str, str):
        return 0, 0.0
    
    sizes = size_str.split(',')
    out_of_stock = size_str.count('Out of stock')
    rate = out_of_stock / len(sizes)
    return out_of_stock, rate

# chart 1 - which brands have the most products
top_brands = df['Brand'].value_counts().head(10).index
df_top = df[df['Brand'].isin(top_brands)]

fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=df_top, y='Brand', order=top_brands, ax=ax)
ax.set_title('Top 10 Brands by Number of Products')
ax.set_xlabel('Count')
ax.set_ylabel('Brand')
plt.tight_layout()
plt.show()

# chart 2 - price range per brand, boxplot is good for this
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=df_top, x='Brand', y='price', ax=ax)
plt.xticks(rotation=45, ha='right')
ax.set_title('Price Distribution by Top 10 Brands')
ax.set_xlabel('Brand')
ax.set_ylabel('Price (£)')
plt.tight_layout()
plt.show()

# chart 3 - average price per brand
avg_price = df.groupby('Brand')['price'].mean().sort_values(ascending=False)

top_avg = avg_price.head(10).index
df_top_avg = df[df['Brand'].isin(top_avg)]

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=df_top_avg, x='Brand', y='price', estimator='mean', ax=ax)
plt.xticks(rotation=45, ha='right')
ax.set_title('Average Price by Top 10 Brands')
ax.set_xlabel('Brand')
ax.set_ylabel('Average Price (£)')
plt.tight_layout()
plt.show()

# quick summary
print(f"\nbrand with most products: {df['Brand'].value_counts().idxmax()}")
print(f"most expensive brand on average: {avg_price.idxmax()} at £{avg_price.max():.2f}")
print(f"\naverage price by brand:\n{avg_price.head(10)}")
