from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

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



async def generate_discussion_question(discussion_name: str) -> dict:
    response = await client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": f"""
            Generate a short, beginner-friendly, and engaging technical discussion post about {discussion_name}. 
            Format the output as follows:
            - Start with a compelling title (do not include the word 'Title:' in the output).
            - Then provide the content (do not include the word 'Content:' in the output).
            The post should be under 150 words, written in a conversational tone, and feel human-made.
            Avoid using complex jargon. Instead, explain the concepts in simple terms that someone new to the topic could understand.
            The content should introduce the topic, give a brief and easy-to-understand explanation, and end with an open-ended question to encourage discussion.
            After the title, separate it from the content using the delimiter ':0'.
            """
        }],
        model="gpt-4",
        temperature=1,
        max_tokens=4096,
        top_p=1
    )

    # Extracting the content of the message
    results = response.choices[0].message['content'].strip()

    # Separate title and content using the delimiter ":0"
    delimiter = ":0"
    title, content = results.split(delimiter, 1)

    post = {"Title": title.strip(), "Content": content.strip()}
    return post

async def generate_answer_to_question(question: dict) -> str:
    response = await client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": f"""
            You're answering a technical discussion post from a beginner.
            Here’s the original question:
            Title: {question['title']}
            Content: {question['content']}

            Write a short, beginner-friendly, and helpful answer in a conversational tone.
            The answer should:
            - Be under 150 words
            - Feel human-made (not robotic)
            - Avoid complex jargon
            - Include a simple explanation or example if useful
            - Include variation across answers: sometimes accurate, sometimes mildly incorrect or oversimplified (like a real user might do)

            Only output the answer content (no title, no labels, no formatting).
            """
        }],
        model="gpt-4",
        temperature=1,
        max_tokens=4096,
        top_p=1
    )

    return response.choices[0].message['content'].strip()

