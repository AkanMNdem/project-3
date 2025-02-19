import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Load the AI detection results
df = pd.read_csv("DATA/ai_detection_results.csv")

# Chi-Square Test for AI Usage Rate
threshold = 50  # threshhol, >= 50% we'll say it's AI generated
df["ai_generated"] = df["ai_score"] > threshold

ai_counts = df.groupby("category")["ai_generated"].sum()
total_counts = df["category"].value_counts()
contingency_table = pd.DataFrame({"AI-Generated": ai_counts, "Human-Written": total_counts - ai_counts})

chi2_stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)

print("Chi-Square Test for AI Usage Rate")
print(contingency_table)
print(f"Chi-Square Statistic: {chi2_stat:.3f}, p-value: {p_value:.5f}")
print("Significant difference in AI usage rates." if p_value < 0.05 else "No significant difference in AI usage rates.")
print("\n" + "-" * 50 + "\n")

# plot chi-square results
ai_usage_rate = (ai_counts / total_counts) * 100
plt.figure(figsize=(8, 5))
ai_usage_rate.plot(kind='bar', color=['blue', 'orange', 'green'], alpha=0.7)
plt.title("AI Usage Rate by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Percentage of AI-Generated Reviews (%)")
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.show()

#One-Way ANOVA for AI Score Differences
categories = df["category"].unique()
grouped_scores = [df[df["category"] == cat]["ai_score"].dropna() for cat in categories]

f_stat, p_value = stats.f_oneway(*grouped_scores)

print("One-Way ANOVA for AI Scores")
print(f"F-Statistic: {f_stat:.3f}, p-value: {p_value:.5f}")
print("Significant difference in AI scores across categories." if p_value < 0.05 else "No significant difference in AI scores.")
print("\n" + "-" * 50 + "\n")

# plot one-way ANOVA results
plt.figure(figsize=(10, 6))
sns.boxplot(x=df["category"], y=df["ai_score"], palette="Set2")
plt.title("Distribution of AI Scores by Product Category")
plt.xlabel("Product Category")
plt.ylabel("AI Score (%)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# 3 pairwise Two-Sample t-Tests
for i in range(len(categories)):
    for j in range(i + 1, len(categories)):
        cat1 = categories[i]
        cat2 = categories[j]
        
        group1 = df[df["category"] == cat1]["ai_score"].dropna()
        group2 = df[df["category"] == cat2]["ai_score"].dropna()
        
        t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)

        print(f"T-test between {cat1} and {cat2}")
        print(f"T-Statistic: {t_stat:.3f}, p-value: {p_value:.5f}")
        print("Significant difference." if p_value < 0.05 else "No significant difference.")
        print("\n" + "-" * 50 + "\n")

# use a violin plot to show results of the two-sample t-tests
plt.figure(figsize=(10, 6))
sns.violinplot(x=df["category"], y=df["ai_score"], palette="pastel")
plt.title("AI Score Distributions by Product Category")
plt.xlabel("Product Category")
plt.ylabel("AI Score (%)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()