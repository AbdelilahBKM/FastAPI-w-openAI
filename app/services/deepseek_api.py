import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
import asyncio

from app.utils.classes import Question

endpoint = "https://models.github.ai/inference"
model = "deepseek/DeepSeek-V3-0324"
token = os.environ["DEEPSEEK_API_KEY"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

prompt = """
You are an AI assistant designed to help users and developers by providing clear, concise,
and informative answers to technical questions. 
Your responses should be factual, neutral, and helpful, explaining concepts in a straightforward way. 
Make sure your answers sound like they come from an AI: objective, precise, and without personal opinions. 
Keep the tone professional and polite. 
Inform the user if there are any assumptions or limitations in your response.
"""

async def generate_answer_with_deepseek(question: Question) -> str:
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(
        None,
        lambda: client.complete(
            messages=[
                SystemMessage(prompt),
                UserMessage(f"Title: {question.title}\nContent: {question.content}")
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model
        )
    )
    return response.choices[0].message.content.strip()