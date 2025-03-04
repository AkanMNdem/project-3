# Amazon Review Authenticity Analysis

## Repository Overview
Welcome to the DS4002 Project 1 Repo for Hudson Noyes, Akan Ndem, and Ali Nilforoush. Our project focused analyzing what percent of Amazon reviews are AI generated. This repo contains: this README and a LICENSE file and DATA, SCRIPT, and OUTPUT folders.

---

## Section 1: Software and Platform  
This project was developed using the following software and tools:

- **Software Used:**  
  - [Python]
  - [Sapling AI Detector]   
  
- **Add-On Packages:**  
  - [PANDAS] – [Used for data manipulation and analysis]
  - [REQUESTS] - [Used for JSON accessing]
  - [MAPLOTLIB.PYPLOT] - [Used for data visualization]
  - [TIME] - [Used for time related functions]
  - [SCIPY] - [Used for analysis of AI detection results]
 
- **Platform Compatibility:**  
  - ✅ Windows  
  - ✅ macOS (used during project)  
  - ✅ Linux  

Ensure you have the required software installed before proceeding.

---

## Section 2: Project Structure  
Below is a map of the repository, illustrating the hierarchy of files and folders:

📂 Project_Folder/ │-- 📂 DATA/ # Raw and processed datasets │-- 📂 SCRIPTS/ # Code for data processing & analysis │ │-- main.py # Main script for data analysis │ │-- preprocess.py # Data cleaning and preprocessing │-- 📂 RESULTS/ # Output files (graphs, models, reports) │-- 📂 RESULTS/ # results of analysis performed on data │ │-- README.md # This orientation file

## Section 3: Results Reproduction Instructions
1. We first need to figure out what dataset to analyze. For our group, we decided to analyze Amazon Product Reviews and gathered this data from a GitHub Repository. This is the repository the Amazon Product Reviews came from: https://amazon-reviews-2023.github.io/
2. We then decided how we are going to analyze this data, which we did on the basis of AI usage in reviews 
3. We searched for AI detection software, specifically ones where we had easy access (account creation is simple) to an API to send requests on the AI detection results. This lead to us using the Sappling AI detector API: https://sapling.ai/docs/api/detector/ (see ai_detection.py)
4. After downloading the dataset for 3 different types of products (Software, Handmade Products, and Video Games), we graphically analyzed the character count of the reviews to create lower and upper bound on the character count per review. We settled on an upper bound of 600 characters. To visualize our data, we used pandas, matplotlib, and json libraries. (see main.py)
   ```python
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
   ```
5. We then cleaned the data to fit our data dictionary and pooled a random sample of 1000 reviews for each product set. (see data_processing.py)
   ```python
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
   ```
6. This random sample was sent to the Sappling AI detector using the Sappling AI detection API, but an even smaller sample from this was sent due to rate limiting by Sappling.
    ```python
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
    ```
7. After gathering the data on AI detection, we ran a one-way ANOVA test, two sample t-test (comparing each group against another), and a chi-squared test to analyze statistical significance of AI usage between groups. We used scipy and pandas for converting the data to a data frame then conducting statistical analysis. After that we visualized the results using matplotlib and seaborn. (see analysis.py)
    ```python
    # Chi-Square Test for AI Usage Rate
    threshold = 50  # threshhol, >= 50% we'll say it's AI generated
    df["ai_generated"] = df["ai_score"] > threshold
    
    ai_counts = df.groupby("category")["ai_generated"].sum()
    total_counts = df["category"].value_counts()
    contingency_table = pd.DataFrame({"AI-Generated": ai_counts, "Human-Written": total_counts - ai_counts})
    
    chi2_stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)

    # One-way ANOVA test for AI usage
    categories = df["category"].unique()
    grouped_scores = [df[df["category"] == cat]["ai_score"].dropna() for cat in categories]
    
    f_stat, p_value = stats.f_oneway(*grouped_scores)

    # 3 pairwise two-sample t-test for ai usage between 2 groups
    for i in range(len(categories)):
    for j in range(i + 1, len(categories)):
        cat1 = categories[i]
        cat2 = categories[j]
        
        group1 = df[df["category"] == cat1]["ai_score"].dropna()
        group2 = df[df["category"] == cat2]["ai_score"].dropna()
        
        t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)
    ```
