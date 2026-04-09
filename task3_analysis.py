# Task 3 — Data Analysis using Pandas & NumPy, this script loads cleaned data, performs analysis, adds new columns, and saves the result for further use.

import pandas as pd
import numpy as np
import os

# Step 1 — Load and Explore


file_path = "data/trends_clean.csv"

try:
    df = pd.read_csv(file_path)
    print(f"Loaded data: {df.shape}")
except Exception as e:
    print("Error loading file:", e)
    exit()

# Print first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Average values using pandas
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {int(avg_score)}")
print(f"Average comments: {int(avg_comments)}")

# Step 2 — Analysis with NumPy

scores = df["score"].values
comments = df["num_comments"].values

print("\n--- NumPy Stats ---")

# Mean, median, std
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

print(f"Mean score   : {int(mean_score)}")
print(f"Median score : {int(median_score)}")
print(f"Std deviation: {int(std_score)}")

# Max and Min
print(f"Max score    : {np.max(scores)}")
print(f"Min score    : {np.min(scores)}")

# Category with most stories
top_category = df["category"].value_counts().idxmax()
top_count = df["category"].value_counts().max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Story with most comments
max_comments_idx = np.argmax(comments)
top_story_title = df.iloc[max_comments_idx]["title"]
top_story_comments = df.iloc[max_comments_idx]["num_comments"]

print(f'\nMost commented story: "{top_story_title}" — {top_story_comments} comments')


# Step 3 — Add New Columns

# Engagement = comments per upvote
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Popular if score > average score
df["is_popular"] = df["score"] > avg_score


# Step 4 — Save Result

os.makedirs("data", exist_ok=True)

output_path = "data/trends_analysed.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved to {output_path}")