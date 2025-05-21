from fastapi import APIRouter

from app.services.deepseek_api import generate_answer_with_deepseek
from app.utils.classes import Question

router = APIRouter()

@router.post("/assist")
async def get_ai_answer(question: Question):
    answer = await generate_answer_with_deepseek(question)
    return {"answer": answer, "source": "AI"}
