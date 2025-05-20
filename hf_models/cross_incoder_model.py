from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

from app.utils.classes import Question

model_name = 'cross-encoder/ms-marco-MiniLM-L6-v2'

# Load tokenizer and model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
model.eval()


def question_to_text(q: Question) -> str:
    return q.title


def score_similarity(question: Question, candidates: list[Question]) -> list[float]:
    question_text = question_to_text(question)
    candidate_texts = [question_to_text(c) for c in candidates]
    features = tokenizer(
        [question_text] * len(candidates),
        candidate_texts,
        padding=True,
        truncation=True,
        return_tensors="pt"
    )
    with torch.no_grad():
        logits = model(**features).logits.squeeze(-1)
        probabilities = torch.sigmoid(logits)
    return probabilities.tolist()

