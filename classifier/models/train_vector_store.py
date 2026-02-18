import pandas as pd
import numpy as np
import faiss
from models.model_loader import model


df = pd.read_csv("data/dataset_normalized.csv")

texts = df["text"].astype(str).tolist()
labels = df["normalized_label"].tolist()

embeddings = model.encode(texts, convert_to_numpy=True)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, "data/incident_index.faiss")
np.save("data/incident_labels.npy", labels)

print("AIOps memory trained successfully")
