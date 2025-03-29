from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
import os
from faker import Faker

load_dotenv()
OPENAI_API_KEY = os.getenv("GITHUB_TOKEN")
ASP_NET_API = os.getenv("ASPNET_API_URL")

client = OpenAI(
        base_url = "https://models.inference.ai.azure.com",
        api_key = OPENAI_API_KEY,
    )

app = FastAPI()
fake = Faker()


def generated_user(user_id):
    return {
        "id": user_id,
        "firstName": fake.first_name(),
        "LastName": fake.last_name(),
        "userName": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(length=12)
    }

@app.get("/ping")
async def root():
    return {"message": "Hello World"}

@app.get("/pingOpenAI")
async def pingOpenAI():
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "",
                },
                {
                    "role": "user",
                    "content": "ping",
                }
            ],
            model="gpt-4o",
            temperature=1,
            max_tokens=4096,
            top_p=1
        )
        return {"message": response.choices[0].message.content}
    except Exception as ex:
        return {"error": str(ex)}

