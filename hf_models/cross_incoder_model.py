from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_name = 'cross-encoder/ms-marco-MiniLM-L6-v2'

# Load tokenizer and model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Set model to evaluation mode (disables dropout etc.)
model.eval()

def score_similarity(query: str, candidates: list[str]) -> list[float]:
    # Tokenize pairs: each candidate paired with the same query
    features = tokenizer(
        [query] * len(candidates),  # Repeat query for each candidate
        candidates,
        padding=True,
        truncation=True,
        return_tensors="pt"  # Return PyTorch tensors
    )

    # Disable gradient calculations (we don't train here)
    with torch.no_grad():
        # Pass inputs to model, get raw output logits
        logits = model(**features).logits.squeeze(-1)
        # logits shape: [num_candidates], squeeze removes extra dimensions

    # Return logits as a normal Python list of floats
    return logits.tolist()
