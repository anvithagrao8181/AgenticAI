import faiss
import numpy as np
from models.model_loader import model
from utils.text_cleaner import clean_log
from utils.error_extractor import extract_error
from utils.protocol_interpreter import enrich_protocol_errors


index = faiss.read_index("data/incident_index.faiss")
labels = np.load("data/incident_labels.npy", allow_pickle=True)

def classify_log(log_text: str):

    log_text = enrich_protocol_errors(log_text)

    error_text = extract_error(log_text)
    cleaned = clean_log(error_text)

    emb = model.encode([cleaned], convert_to_numpy=True)

    D, I = index.search(emb, k=1)

    predicted_label = labels[I[0][0]]
    distance = float(D[0][0])

    confidence = 1 / (1 + distance)

    return predicted_label, round(confidence, 3)

