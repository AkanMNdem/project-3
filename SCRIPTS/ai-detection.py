import requests
import pandas as pd
import matplotlib.pyplot as plt
import time
import random

# Load pre-processed review file
input_file = "DATA/cleaned_reviews.csv"
API_KEY = "FTUMG7UJ0712VEGLF1Z7D1852A8B12K0"
API_URL = "https://api.sapling.ai/api/v1/aidetect"

# Load dataset
df_reviews = pd.read_csv(input_file)

# Ensure required columns exist
if "text" not in df_reviews.columns or "category" not in df_reviews.columns:
    raise ValueError("The input file must contain 'text' and 'category' columns.")

# Sample 500 random reviews per category
df_sampled = df_reviews.groupby("category", group_keys=False).apply(
    lambda x: x.sample(n=min(50, len(x)), random_state=42)
)

def get_ai_detection_score_sapling(text, max_retries=5):
    """Sends review text to Sapling AI Detector API with retry logic for rate limits."""
    payload = {"key": API_KEY, "text": text}
    retries = 0

    while retries < max_retries:
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                result = response.json()
                return result.get("score", 0) * 100  # Convert to percentage
            elif response.status_code == 429:  # Too Many Requests
                wait_time = (2 ** retries) + random.uniform(0, 1)  # Exponential backoff with jitter
                print(f"Rate limited. Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
                retries += 1
            else:
                print(f"API request failed: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None

    print("Max retries reached. Skipping this review.")
    return None

# Process sampled reviews
ai_scores = []
for i, review in enumerate(df_sampled["text"]):
    print(f"Processing review {i + 1}/{len(df_sampled)}")
    score = get_ai_detection_score_sapling(review)
    ai_scores.append(score)
    time.sleep(3)  # Small delay to prevent unnecessary API throttling

# Add AI detection scores to DataFrame
df_sampled["ai_score"] = ai_scores

# Save AI detection results
results_file = "DATA/ai_detection_results.csv"
df_sampled.to_csv(results_file, index=False)
print(f"Results saved to {results_file}")

# Plot AI Detection Score Distribution
plt.figure(figsize=(10, 6))
plt.hist(df_sampled["ai_score"].dropna(), bins=20, alpha=0.5, color="blue")
plt.title("Distribution of AI Detection Scores")
plt.xlabel("AI Detection Score (%)")
plt.ylabel("Number of Reviews")
plt.grid(axis="y")
plt.show()