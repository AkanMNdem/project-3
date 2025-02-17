import json
import pandas as pd
import matplotlib.pyplot as plt

# Load the JSONL data into a DataFrame
file_path = 'DATA/Handmade_Products.jsonl'

# Read data from the file
data = []
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        review = json.loads(line.strip())
        data.append(review)

# Convert the list of reviews to a DataFrame
df = pd.DataFrame(data)

# Drop reviews with text less than 200 characters
df_filtered = df[df['text'].str.len() >= 200]

# Add a column for review text length
df_filtered['text_length'] = df_filtered['text'].str.len()

# Define an upper bound for review lengths
upper_bound = 1000  # Set your desired upper bound here

# Filter the DataFrame to include only reviews within the upper bound
df_filtered = df_filtered[df_filtered['text_length'] <= upper_bound]

# Create bins for review lengths
bins = range(0, upper_bound + 100, 100)
df_filtered['length_bins'] = pd.cut(df_filtered['text_length'], bins)

# Count the number of reviews in each bin
review_counts = df_filtered['length_bins'].value_counts().sort_index()

# Plotting the distribution of review lengths as a histogram
plt.figure(figsize=(12, 6))

# Histogram
plt.subplot(1, 2, 1)  # 1 row, 2 columns, 1st subplot
plt.hist(df_filtered['text_length'], bins=50, edgecolor='black')
plt.title('Distribution of Review Lengths (Histogram)')
plt.xlabel('Review Length (characters)')
plt.ylabel('Number of Reviews')
plt.grid(axis='y')

# Frequency plot for binned review lengths
plt.subplot(1, 2, 2)  # 1 row, 2 columns, 2nd subplot
plt.scatter(review_counts.index.astype(str), review_counts.values, color='blue', alpha=0.6)
plt.title('Distribution of Review Lengths (Binned)')
plt.xlabel('Review Length Bins (characters)')
plt.ylabel('Number of Reviews')
plt.grid(axis='y')

# Clean x-axis by limiting ticks and rotating labels
plt.xticks(ticks=range(len(review_counts)), labels=review_counts.index.astype(str), rotation=45, ha='right')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

