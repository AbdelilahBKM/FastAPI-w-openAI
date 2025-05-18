from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from hf_models.cross_incoder_model import score_similarity

router = APIRouter()

class CandidateScore(BaseModel):
    id: int
    score: float

class SimilarityRequest(BaseModel):
    query: str
    candidate_ids: List[int]
    candidates: List[str]

class SimilarityResponse(BaseModel):
    results: List[CandidateScore]

@router.post("/similarity", response_model=SimilarityResponse)
async def similarity_endpoint(request: SimilarityRequest):
    scores = score_similarity(request.query, request.candidates)
    results = [CandidateScore(id=cand_id, score=score) for cand_id, score in zip(request.candidate_ids, scores)]
    return SimilarityResponse(results=results)
