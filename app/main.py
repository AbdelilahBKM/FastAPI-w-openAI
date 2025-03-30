from fastapi import FastAPI
from dotenv import load_dotenv
from app.services.openai_api import generate_gpt_response


load_dotenv()
app = FastAPI()

@app.get("/ping")
async def root():
    return {"message": "Hello World"}

@app.get("/pingOpenAI")
async def pingOpenAI():
    try:
        response = generate_gpt_response("ping")
        return {"message": response}
    except Exception as ex:
        return {"error": str(ex)}

