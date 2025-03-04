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
1. Run main.py: After downloading the dataset for 3 different types of products (Software, Handmade Products, and Video Games), graphically analyzes the character count of the reviews to create lower and upper bound on the character count per review. Settled on an upper bound of 600 characters. Visualizes using json and pandas
2. Run data_processing.py: this script cleans the data to fit data dictionary and pools a random sample of 1000 reviews for each product set.
3. Run ai_detection.py: this script sends a random sample to the Sappling AI detector using the Sappling AI detection API
4. Run analysis.py: after gathering the data on AI detection, this script runs a one-way ANOVA test, two sample t-test (comparing each group against another), and a chi-squared test to analyze statistical significance of AI usage between groups. Uses scipy and pandas for converting the data to a data frame then conducting statistical analysis. After that, visualizes the results using matplotlib and seaborn.
