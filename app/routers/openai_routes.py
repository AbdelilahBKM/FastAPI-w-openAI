from fastapi import APIRouter, Request
from app.services.openai_api import  generate_gpt_response

router = APIRouter()

@router.get("/ping")
def ping_openai():
    try:
        response = generate_gpt_response("ping")
        return {"message": response}
    except Exception as ex:
        return {"error": str(ex)}

@router.post("/request")
def create_openai_request(request: Request):
    try:
        body = request.json()
        response = generate_gpt_response(body["prompt"])
        return {"message": response}
    except Exception as ex:
        return {"error": str(ex)}
