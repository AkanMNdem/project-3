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
1. We first need to figure out what to dataset to analyze. For our group, we decided to analyze Amazon Product Reviews and gathered this data from a GitHub Repository.
2. We then decided how we are going to analyze this data, which we did on the basis of AI usage in reviews.
3. We searched for AI detection software, specifically ones where we had easy access (account creation is simple) to an API to send requests on the AI detection results.
4. After downloading the dataset for 3 different types of products, we graphically analyzed the character count of the reviews to create lower and upper bound on the character count per review.
5. We then cleaned the data to fit our data dictionary and pooled a random sample of 1000 reviews for each product set.
6. This random sample was sent to the Sappling AI detector using the Sappling AI detection API, but an even smaller sample from this was sent due to rate limiting by Sappling.
7. After gathering the data on AI detection, we ran a one-way ANOVA test, two sample t-test (comparing each group against another), and a chi-squared test to analyze statistical significance of AI usage between groups.
