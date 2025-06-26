import pandas as pd
import numpy as np

# Load Telegram data
df = pd.read_csv('telegram_data.csv')

# Adjust column names to match your CSV
# Assumptions:
# - 'Channel Title' is the vendor/channel name
# - 'Date' is the timestamp
# - 'Message' is the post text
# - 'views', 'product', 'price' may not be present; handle gracefully

# Rename for convenience
vendor_col = 'Channel Title'
date_col = 'Date'
text_col = 'Message'
views_col = 'views'  # If not present, will be handled
product_col = 'product'  # If not present, will be handled
price_col = 'price'  # If not present, will be handled

# Ensure timestamp is datetime
if date_col in df.columns:
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
else:
    raise ValueError(f"'{date_col}' column not found in CSV.")

# If price is present, ensure numeric
if price_col in df.columns:
    df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
else:
    df[price_col] = np.nan

# If views is present, ensure numeric
if views_col in df.columns:
    df[views_col] = pd.to_numeric(df[views_col], errors='coerce')
else:
    df[views_col] = np.nan

scorecard = []
for vendor, group in df.groupby(vendor_col):
    # Posting frequency (posts per week)
    weeks = (group[date_col].max() - group[date_col].min()).days / 7
    posts_per_week = len(group) / weeks if weeks > 0 else len(group)
    # Avg. views per post (if available)
    avg_views = group[views_col].mean() if views_col in group else np.nan
    # Top performing post (if views available)
    if views_col in group and group[views_col].notna().any():
        top_post = group.loc[group[views_col].idxmax()]
        top_product = top_post.get(product_col, 'N/A')
        top_price = top_post.get(price_col, np.nan)
    else:
        top_product = 'N/A'
        top_price = np.nan
    # Avg. price point (if available)
    avg_price = group[price_col].dropna().mean() if price_col in group else np.nan
    # Lending Score (customizable weights, ignore NaN)
    lending_score = 0
    if not np.isnan(avg_views):
        lending_score += avg_views * 0.5
    lending_score += posts_per_week * 0.5
    scorecard.append({
        'Vendor': vendor,
        'Avg. Views/Post': round(avg_views, 1) if not np.isnan(avg_views) else 'N/A',
        'Posts/Week': round(posts_per_week, 2),
        'Avg. Price (ETB)': round(avg_price, 2) if not np.isnan(avg_price) else 'N/A',
        'Lending Score': round(lending_score, 2),
        'Top Post Product': top_product,
        'Top Post Price': top_price
    })

scorecard_df = pd.DataFrame(scorecard)
scorecard_df = scorecard_df.sort_values('Lending Score', ascending=False)

# Display as markdown table for your report
print(scorecard_df[['Vendor', 'Avg. Views/Post', 'Posts/Week', 'Avg. Price (ETB)', 'Lending Score']].to_markdown(index=False))

# Optionally, save to CSV
scorecard_df.to_csv('vendor_scorecard.csv', index=False) 