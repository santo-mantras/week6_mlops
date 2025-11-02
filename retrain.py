import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib
import os

# --- 1. Load and Combine Data ---
# We'll combine the two raw CSVs to create the
# same augmented dataset we used in our previous assignments.
print("Loading and combining v1/data.csv and v2/data.csv...")
try:
    df_v1 = pd.read_csv("v1/data.csv")
    df_v2 = pd.read_csv("v2/data.csv")
except FileNotFoundError:
    print("Error: v1/data.csv or v2/data.csv not found.")
    print("Please copy the raw data files into the v1/ and v2/ folders.")
    exit(1)

df = pd.concat([df_v1, df_v2], ignore_index=True)
print(f"Total rows in combined dataset: {len(df)}")

# --- 2. Train the Model ---

X = df.drop('species', axis=1)
y = df['species']

# Using max_depth=10
model = DecisionTreeClassifier(max_depth=10, random_state=1)

print("Training the model...")
model.fit(X, y)
print("Model training complete.")

# --- 3. Save the New, Compatible Model ---
output_file = "model.joblib"
joblib.dump(model, output_file)
print(f"New, compatible model saved successfully as '{output_file}'")
