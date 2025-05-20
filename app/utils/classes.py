from typing import List
from pydantic import BaseModel, Field

class CaseInsensitiveModel(BaseModel):
    class Config:
        alias_generator = lambda x: x.lower()
        allow_population_by_field_name = True
        extra = 'ignore'

class Question(CaseInsensitiveModel):
    id: int = Field(..., alias="id")
    title: str = Field(..., alias="title")
    content: str = Field(..., alias="content")

class CandidateScore(CaseInsensitiveModel):
    id: int
    score: float

class SimilarityRequest(CaseInsensitiveModel):
    question: Question = Field(..., alias="question")
    candidate_ids: List[int] = Field(..., alias="candidateIds")
    candidates: List[Question] = Field(..., alias="candidates")

class SimilarityResponse(CaseInsensitiveModel):
    results: List[CandidateScore]