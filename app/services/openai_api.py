from openai import OpenAI
from dotenv import load_dotenv
import os

ASP_NET_API = os.getenv("ASPNET_API_URL")
OPENAI_API_KEY = os.getenv("GITHUB_TOKEN")

client = OpenAI(
        base_url = "https://models.inference.ai.azure.com",
        api_key = OPENAI_API_KEY,
    )

def generate_gpt_response(prompt: str) -> str:
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o",
        temperature=1,
        max_tokens=4096,
        top_p=1
    )
    return response.choices[0].message.content
