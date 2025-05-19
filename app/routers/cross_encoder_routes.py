from typing import List
from fastapi import APIRouter
from pydantic import BaseModel, Field
from hf_models.cross_incoder_model import score_similarity, Question

router = APIRouter()

class CandidateScore(BaseModel):
    id: int
    score: float

class SimilarityRequest(BaseModel):
    question: Question = Field(..., alias="Question")
    candidate_ids: List[int] = Field(..., alias="CandidateIds")
    candidates: List[Question] = Field(..., alias="Candidates")
    class Config:
        allow_population_by_field_name = True

class SimilarityResponse(BaseModel):
    results: List[CandidateScore]

@router.post("/similarity", response_model=SimilarityResponse)
async def similarity_endpoint(request: SimilarityRequest):
    scores = score_similarity(request.question, request.candidates)
    results = [CandidateScore(id=cand_id, score=score) for cand_id, score in zip(request.candidate_ids, scores)]
    return SimilarityResponse(results=results)