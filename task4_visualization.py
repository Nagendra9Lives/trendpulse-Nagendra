# Task 4 — Data Visualization using Matplotlib, this script creates charts from analysed data and saves them as images.
import pandas as pd
import matplotlib.pyplot as plt
import os



# Step 1 — Setup

file_path = "data/trends_analysed.csv"

try:

  df = pd.read_csv(file_path)

except Exception as e:

  print("Error loading file:", e)

  exit()

# Create outputs folder if not exists

os.makedirs("outputs", exist_ok=True)

# Chart 1 — Top 10 Stories by Score
# Sort and take top 10

top_stories = df.sort_values(by="score", ascending=False).head(10)

# Shorten long titles
top_stories["short_title"] = top_stories["title"].apply(

  lambda x: x[:50] + "..." if len(x) > 50 else x

)

plt.figure()

plt.barh(top_stories["short_title"], top_stories["score"])

plt.xlabel("Score")

plt.ylabel("Story Title")

plt.title("Top 10 Stories by Score")

plt.gca().invert_yaxis() # Highest score on top

plt.tight_layout()

plt.savefig("outputs/chart1_top_stories.png")

plt.close()

# Chart 2 — Stories per Category

category_counts = df["category"].value_counts()

plt.figure()

plt.bar(category_counts.index, category_counts.values)

plt.xlabel("Category")

plt.ylabel("Number of Stories")

plt.title("Stories per Category")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig("outputs/chart2_categories.png")

plt.close()


# Chart 3 — Score vs Comments

plt.figure()



# Separate popular vs non-popular

popular = df[df["is_popular"] == True]

not_popular = df[df["is_popular"] == False]

plt.scatter(popular["score"], popular["num_comments"], label="Popular")

plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")

plt.ylabel("Number of Comments")

plt.title("Score vs Comments")

plt.legend()



plt.tight_layout()

plt.savefig("outputs/chart3_scatter.png")

plt.close()

# Overall title

plt.suptitle("TrendPulse Dashboard")

plt.tight_layout()

plt.savefig("outputs/dashboard.png")

plt.close()


print("All charts saved in outputs/ folder")
