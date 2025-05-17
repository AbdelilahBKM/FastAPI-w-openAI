from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from sqlalchemy.orm import Session
from typing import List, Tuple
import uuid
from datetime import datetime

# Configuration
MODEL = SentenceTransformer("all-MiniLM-L6-v2")  # Local model for duplicate detection
TEXT_GENERATOR = pipeline("text-generation", model="distilbert-base-uncased")  # Local model for text generation

async def generate_grok_response(prompt: str, max_tokens: int = 200) -> str:
    try:
        # Simulate AI response using local Hugging Face model
        result = TEXT_GENERATOR(
            prompt,
            max_length=max_tokens,
            num_return_sequences=1,
            truncation=True,
            pad_token_id=50256  # Default for DistilBERT
        )
        response = result[0]["generated_text"].strip()
        # Clean up response (DistilBERT may generate noisy output)
        if len(response) > len(prompt):
            response = response[len(prompt):].strip()
        return response[:200] if len(response) > 200 else response
    except Exception as e:
        raise Exception(f"Local model error: {str(e)}")

def detect_duplicate_post(question: str, existing_questions: List[str]) -> dict:
    if not existing_questions:
        return {"is_duplicate": False, "similarity_score": 0.0, "message": "No existing questions."}
    question_embedding = MODEL.encode(question, convert_to_tensor=True)
    existing_embeddings = MODEL.encode(existing_questions, convert_to_tensor=True)
    similarities = util.cos_sim(question_embedding, existing_embeddings)[0]
    max_similarity = float(max(similarities))
    threshold = 0.85
    is_duplicate = max_similarity > threshold
    return {
        "is_duplicate": is_duplicate,
        "similarity_score": max_similarity,
        "message": "Duplicate question detected." if is_duplicate else "Question appears unique."
    }

async def get_chatbot_response(session_id: str, user_id: str, message: str, db: Session) -> Tuple[str, str]:
    session_id = session_id or str(uuid.uuid4())
    # Load or initialize history
    result = db.execute(
        text("SELECT history FROM conversation_history WHERE session_id = :session_id AND user_id = :user_id"),
        {"session_id": session_id, "user_id": user_id}
    )
    history = result.fetchone()
    history_text = history[0] if history else "You are a programming expert. Provide concise, accurate, and friendly responses.\n"
    # Append message
    history_text += f"User: {message}\n"
    # Generate response
    prompt = f"{history_text}Assistant: "
    response = await generate_grok_response(prompt, max_tokens=200)
    # Update history
    history_text += f"Assistant: {response}\n"
    db.execute(
        text("""
            INSERT OR REPLACE INTO conversation_history (session_id, user_id, history, created_at)
            VALUES (:session_id, :user_id, :history, :created_at)
        """),
        {"session_id": session_id, "user_id": user_id, "history": history_text, "created_at": datetime.utcnow()}
    )
    db.commit()
    return response, session_id

async def get_personalized_recommendations(user_id: str, db: Session) -> List[dict]:
    result = db.execute(
        text("SELECT content FROM posts WHERE user_id = :user_id AND is_answer = 0"),
        {"user_id": user_id}
    )
    user_questions = [row[0] for row in result.fetchall()]
    if not user_questions:
        return []
    keywords = set()
    for question in user_questions:
        words = question.lower().split()
        keywords.update([w for w in words if w in ["python", "javascript", "sql", "algorithm", "debugging"]])
    recommendations = []
    for keyword in keywords:
        prompt = f"You are a programming expert. Suggest a learning resource or tip for {keyword} programming."
        rec = await generate_grok_response(prompt, max_tokens=100)
        recommendations.append({"topic": keyword, "recommendation": rec})
    return recommendations