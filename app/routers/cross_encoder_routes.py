from typing import List
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.utils.classes import SimilarityRequest, CandidateScore, SimilarityResponse
from hf_models.cross_incoder_model import score_similarity

router = APIRouter()

@router.post("/similarity", response_model=SimilarityResponse)
async def similarity_endpoint(request: SimilarityRequest):
    scores = score_similarity(request.question, request.candidates)
    results = [CandidateScore(id=cand_id, score=score) for cand_id, score in zip(request.candidate_ids, scores)]
    return SimilarityResponse(results=sorted(results, key=lambda x: x.score, reverse=True))