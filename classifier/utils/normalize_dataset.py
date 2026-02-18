import pandas as pd

INPUT_FILE = "data/dataset.csv"
OUTPUT_FILE = "data/dataset_normalized.csv"

df = pd.read_csv(INPUT_FILE)

df["text"] = df["text"].astype(str).str.lower()
df["normalized_label"] = df["label"]

df.to_csv(OUTPUT_FILE, index=False)

print("Dataset normalized")
