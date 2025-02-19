import json
import pandas as pd
import random

# Define file paths
file_paths = {
    'Software': 'DATA/Software.jsonl',
    'Handmade Products': 'DATA/Handmade_Products.jsonl',
    'Video Games': 'DATA/Video_Games.jsonl'
}

metadata_paths = {
    'Software': 'DATA/meta_Software.jsonl',
    'Handmade Products': 'DATA/meta_Handmade_Products.jsonl',
    'Video Games': 'DATA/meta_Video_Games.jsonl'
}

# Function to load and filter reviews
def load_and_filter_reviews(file_path, category, min_length=200, max_length=600):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            review = json.loads(line.strip())
            if min_length <= len(review.get('text', '')) <= max_length:
                review["category"] = category  # Add category column
                data.append(review)
    
    df = pd.DataFrame(data)
    
    if df.empty:
        return pd.DataFrame(columns=["text", "parent_asin", "rating", "title", "user_id", "timestamp", "verified_purchase", "helpful_vote", "category"])
    
    return df

# Function to load metadata
def load_metadata(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line.strip())
            data.append(entry)
    
    df = pd.DataFrame(data)
    
    if df.empty:
        return pd.DataFrame(columns=["parent_asin", "main_category", "title", "average_rating", "rating_number", "store"])
    
    return df

# Load reviews & metadata
df_reviews = {category: load_and_filter_reviews(path, category) for category, path in file_paths.items()}
df_metadata = {category: load_metadata(path) for category, path in metadata_paths.items()}

# Merge reviews with metadata on 'parent_asin'
for category in df_reviews:
    df_reviews[category] = df_reviews[category].merge(df_metadata[category], on='parent_asin', how='left')

# Ensure all necessary columns are present
for category in df_reviews:
    df_reviews[category] = df_reviews[category][["text", "parent_asin", "rating", "verified_purchase", "helpful_vote", "main_category", "category"]]

    # Fill missing categories
    df_reviews[category]["main_category"] = df_reviews[category]["main_category"].fillna("Unknown")

# Sample exactly 1000 reviews from each category file
df_sampled = []
for category, df in df_reviews.items():
    if len(df) >= 1000:
        df_sampled.append(df.sample(n=1000, random_state=42))
    else:
        print(f"Warning: {category} has only {len(df)} reviews, using all available.")
        df_sampled.append(df)

# Combine all sampled data
df_final = pd.concat(df_sampled, ignore_index=True)

# Save cleaned dataset
output_file = "DATA/cleaned_reviews.csv"
df_final.to_csv(output_file, index=False, columns=["text", "main_category", "rating", "verified_purchase", "helpful_vote", "category"])

print(f"Pre-processed data saved to {output_file}")
print(f"Final Sampled Shape: {df_final.shape}")